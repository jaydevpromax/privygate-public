from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    status: str
    name: str
    detail: str


def run(command: list[str], cwd: Path = ROOT, timeout: int = 20, env: dict[str, str] | None = None) -> tuple[int, str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)
    return result.returncode, result.stdout.strip()


def command_names(name: str) -> list[str]:
    candidates = [name]
    if os.name == "nt" and not name.lower().endswith((".exe", ".cmd", ".bat")):
        candidates.extend([f"{name}.cmd", f"{name}.exe", f"{name}.bat"])
    return candidates


def candidate_executables(name: str) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()
    for candidate in command_names(name):
        executable = shutil.which(candidate)
        if executable and executable not in seen:
            candidates.append(executable)
            seen.add(executable)

    if os.name == "nt":
        roots: list[Path] = []
        for variable in ("ProgramFiles", "ProgramW6432", "ProgramFiles(x86)"):
            value = os.environ.get(variable)
            if value:
                roots.append(Path(value) / "nodejs")
        for drive in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            roots.append(Path(f"{drive}:\\Program Files\\nodejs"))
        for root in roots:
            for candidate in command_names(name):
                path = root / candidate
                key = str(path)
                if path.exists() and key not in seen:
                    candidates.append(key)
                    seen.add(key)
    return candidates


def resolve_working_command(command: list[str]) -> tuple[str | None, str]:
    failures: list[str] = []
    for executable in candidate_executables(command[0]):
        code, output = run([executable, *command[1:]])
        if code == 0:
            return executable, first_line(output)
        failures.append(first_line(output) or f"{executable} failed")
    detail = failures[0] if failures else f"{command[0]} not found in PATH"
    return None, detail


def command_version(name: str, command: list[str]) -> Check:
    executable, output = resolve_working_command(command)
    if not executable:
        return Check("BLOCKED", name, output)
    return Check("OK", name, f"{executable} :: {output}")


def first_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:180]
    return ""


def check_git_remote() -> list[Check]:
    checks: list[Check] = []
    code, remote = run(["git", "remote", "get-url", "origin"])
    if code == 0 and remote:
        checks.append(Check("OK", "git origin", remote))
    else:
        checks.append(Check("BLOCKED", "git origin", "origin remote is not configured"))

    code, upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    if code == 0 and upstream:
        checks.append(Check("OK", "git upstream", upstream))
    else:
        checks.append(Check("WARN", "git upstream", "main is not tracking origin/main; run `git push -u origin main`"))

    code, status = run(["git", "status", "--short"])
    if code == 0 and not status:
        checks.append(Check("OK", "git working tree", "clean"))
    elif code == 0:
        checks.append(Check("WARN", "git working tree", "uncommitted local changes"))
    else:
        checks.append(Check("WARN", "git working tree", first_line(status) or "git status failed"))
    return checks


def check_node_toolchain() -> list[Check]:
    checks = [
        command_version("node", ["node", "--version"]),
        command_version("npm", ["npm", "--version"]),
        command_version("npx", ["npx", "--version"]),
    ]
    package_json = ROOT / "contracts/package.json"
    if package_json.exists():
        checks.append(Check("OK", "contracts/package.json", "present"))
    else:
        checks.append(Check("FAIL", "contracts/package.json", "missing"))
    node_modules = ROOT / "contracts/node_modules"
    if node_modules.exists():
        checks.append(Check("OK", "contracts/node_modules", "installed"))
    else:
        checks.append(Check("BLOCKED", "contracts/node_modules", "not installed; run `cd contracts && npm install`"))
    return checks


def check_0g_env() -> list[Check]:
    env_path = ROOT / "contracts/.env"
    example = ROOT / "contracts/.env.example"
    checks: list[Check] = []
    if example.exists():
        checks.append(Check("OK", "contracts/.env.example", "present"))
    else:
        checks.append(Check("FAIL", "contracts/.env.example", "missing"))
    if not env_path.exists():
        checks.append(Check("BLOCKED", "contracts/.env", "missing; copy `.env.example` and fill OG_PRIVATE_KEY before deployment"))
        return checks

    raw = env_path.read_text(encoding="utf-8", errors="ignore")
    required = ["OG_RPC_URL", "OG_PRIVATE_KEY", "OG_CHAIN_ID", "OG_EXPLORER_URL"]
    missing = []
    values: dict[str, str] = {}
    for key in required:
        value = ""
        for line in raw.splitlines():
            if line.startswith(f"{key}="):
                value = line.split("=", 1)[1].strip()
                values[key] = value
                break
        if not value:
            missing.append(key)
    if missing:
        checks.append(Check("BLOCKED", "contracts/.env", f"missing values: {', '.join(missing)}"))
    else:
        checks.append(Check("OK", "contracts/.env", "required deployment keys are present; do not commit this file"))
        if values.get("OG_CHAIN_ID") == "16661":
            checks.append(Check("OK", "0G chain id", "mainnet 16661"))
        elif values.get("OG_CHAIN_ID") == "16602":
            checks.append(Check("WARN", "0G chain id", "Galileo testnet 16602; final submission should use mainnet if required"))
        else:
            checks.append(Check("WARN", "0G chain id", f"unexpected value: {values.get('OG_CHAIN_ID', '')}"))
    return checks


def check_hardhat_commands() -> list[Check]:
    npm, _ = resolve_working_command(["npm", "--version"])
    if not npm:
        return [Check("BLOCKED", "hardhat tests", "npm is not available")]
    env = os.environ.copy()
    env["APPDATA"] = str(ROOT / "contracts/.hardhat-home")
    env["LOCALAPPDATA"] = str(ROOT / "contracts/.hardhat-local")
    code, output = run([npm, "test"], cwd=ROOT / "contracts", timeout=120, env=env)
    if code == 0:
        return [Check("OK", "hardhat tests", "npm test passed")]
    return [Check("BLOCKED", "hardhat tests", first_line(output) or "npm test failed")]


def collect_checks() -> list[Check]:
    checks: list[Check] = []
    checks.extend(check_git_remote())
    checks.extend(check_node_toolchain())
    checks.extend(check_0g_env())
    checks.extend(check_hardhat_commands())
    return checks


def print_report(checks: list[Check]) -> None:
    counts = {status: 0 for status in ("OK", "WARN", "BLOCKED", "FAIL")}
    for check in checks:
        counts[check.status] = counts.get(check.status, 0) + 1
    print("PrivyGate External Dependency Check")
    print("=" * 38)
    print(f"Root: {ROOT}")
    print(
        "Summary: "
        f"OK={counts.get('OK', 0)} "
        f"WARN={counts.get('WARN', 0)} "
        f"BLOCKED={counts.get('BLOCKED', 0)} "
        f"FAIL={counts.get('FAIL', 0)}"
    )
    print()
    for status in ("FAIL", "BLOCKED", "WARN", "OK"):
        items = [item for item in checks if item.status == status]
        if not items:
            continue
        print(status)
        print("-" * len(status))
        for item in items:
            print(f"- {item.name}: {item.detail}")
        print()


def main() -> int:
    checks = collect_checks()
    print_report(checks)
    if any(item.status == "FAIL" for item in checks):
        return 1
    if any(item.status == "BLOCKED" for item in checks):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
