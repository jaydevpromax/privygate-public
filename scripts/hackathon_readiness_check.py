from __future__ import annotations

import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    status: str
    name: str
    detail: str


REQUIRED_FILES = [
    "README.md",
    "scripts/generate_storage_audit_manifest.py",
    "scripts/privygate_cli.py",
    "scripts/external_dependency_check.py",
    "scripts/generate_hackathon_assets.py",
    "scripts/update_submission_links.py",
    "app/web/index.html",
    "app/web/styles.css",
    "app/web/app.js",
    "app/web/README.md",
    "storage/package.json",
    "storage/upload-audit.mjs",
    "storage/README.md",
    "src/privygate/core.py",
    "tests/test_core_flow.py",
    "tests/test_api_service.py",
    "contracts/contracts/PrivyGateRegistry.sol",
    "contracts/package.json",
    "contracts/hardhat.config.js",
    "contracts/.env.example",
    "contracts/test/PrivyGateRegistry.test.js",
    "contracts/scripts/check-network.js",
    "contracts/scripts/deploy.js",
    "contracts/scripts/record-demo-events.js",
    "docs/hackathon/0g_submission_checklist.md",
    "docs/hackathon/0g_deployment_notes.md",
    "docs/hackathon/hackquest_submission_fields.md",
    "docs/hackathon/submission_workplan.md",
    "docs/hackathon/final_submission_runbook.md",
    "docs/hackathon/public_release_checklist.md",
    "docs/hackathon/external_setup_guide.md",
    "docs/hackathon/submission_links.template.json",
    "docs/hackathon/video_recording_plan.md",
    "docs/hackathon/demo_voiceover_script.md",
    "docs/hackathon/demo_subtitles_en.srt",
    "docs/hackathon/x_post_draft.md",
    "docs/hackathon/architecture.md",
    "docs/hackathon/privygate_0g_storage_audit_manifest.json",
    "docs/hackathon/assets/privygate-share-card.png",
    "docs/hackathon/assets/privygate-mobile-story.png",
]


README_SECTIONS = [
    "## Problem",
    "## Solution",
    "## Why 0G",
    "## Demo",
    "## Run Tests",
    "## Contract Workflow",
    "## 0G Evidence",
    "## 0G Storage Audit Package",
    "## Current Cryptographic Boundary",
]


PUBLIC_PLACEHOLDER_FILES = [
    "README.md",
    "docs/hackathon/0g_deployment_notes.md",
    "docs/hackathon/hackquest_submission_fields.md",
    "docs/hackathon/x_post_draft.md",
]


PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"<GITHUB_REPO_URL>",
    r"<DEMO_VIDEO_URL>",
    r"<0G_MAINNET_CONTRACT_ADDRESS>",
    r"<0G_EXPLORER_ACTIVITY_LINK>",
    r"TODO_[A-Z0-9_]+",
]


EXPECTED_WEB_REFS = ["./styles.css", "./app.js"]


PUBLIC_SCAN_ROOTS = [
    "README.md",
    "app/web",
    "contracts",
    "docs/hackathon",
    "storage",
]

PUBLIC_EXCLUDE_NAMES = {
    "__pycache__",
    ".env",
    "node_modules",
    "artifacts",
    "cache",
    "types",
    ".hardhat-home",
    ".hardhat-local",
}


PUBLIC_TEXT_SUFFIXES = {
    "",
    ".css",
    ".example",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".srt",
    ".sol",
    ".txt",
}


LOCAL_PATH_PATTERNS = [
    r"C:\\Users\\",
    r"D:\\",
    r"\.cache\\codex-runtimes",
    r"codex-runtimes",
]


SECRET_PATTERNS = [
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "possible inline secret",
        re.compile(
            r"(?i)(?:private[_-]?key|secret|api[_-]?key|token|mnemonic|seed phrase)"
            r"[^\n]{0,48}(?:0x)?[a-f0-9]{64}"
        ),
    ),
]


BLOCKED_RELEASE_PATHS = [
    "contracts/.env",
    "docs/hackathon/submission_links.local.json",
]


GENERATED_LOCAL_PATHS = [
    "node_modules",
    "contracts/node_modules",
    "contracts/artifacts",
    "contracts/cache",
    "contracts/types",
    "storage/node_modules",
]


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    return path.read_text(encoding="utf-8")


def check_required_files() -> list[Check]:
    checks: list[Check] = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if path.exists():
            checks.append(Check("OK", f"file:{relative}", "present"))
        else:
            checks.append(Check("FAIL", f"file:{relative}", "missing"))
    return checks


def check_readme() -> list[Check]:
    path = ROOT / "README.md"
    if not path.exists():
        return [Check("FAIL", "README", "README.md is missing")]
    text = read_text("README.md")
    checks = []
    for section in README_SECTIONS:
        status = "OK" if section in text else "FAIL"
        detail = "present" if status == "OK" else "missing"
        checks.append(Check(status, f"README section:{section}", detail))
    if "symbolic-field-v1" in text and "not production cryptography" in text.lower():
        checks.append(Check("OK", "README crypto boundary", "symbolic backend boundary is explicit"))
    else:
        checks.append(Check("FAIL", "README crypto boundary", "missing explicit non-production wording"))
    return checks


def check_static_web() -> list[Check]:
    html_path = ROOT / "app/web/index.html"
    if not html_path.exists():
        return [Check("FAIL", "static web", "app/web/index.html is missing")]
    html = html_path.read_text(encoding="utf-8")
    checks = []
    for ref in EXPECTED_WEB_REFS:
        status = "OK" if ref in html else "FAIL"
        checks.append(Check(status, f"static ref:{ref}", "referenced by index.html" if status == "OK" else "not referenced"))
    for expected in ["ACCEPT", "REJECT", "0G REGISTRY", "0G STORAGE", "symbolic-field-v1"]:
        status = "OK" if expected in html or expected in read_text("app/web/app.js") else "FAIL"
        checks.append(Check(status, f"static content:{expected}", "present" if status == "OK" else "missing"))
    return checks


def check_contract_scaffold() -> list[Check]:
    checks: list[Check] = []
    contract_path = ROOT / "contracts/contracts/PrivyGateRegistry.sol"
    contract = read_text("contracts/contracts/PrivyGateRegistry.sol") if contract_path.exists() else ""
    for symbol in ["registerAuthority", "registerPolicy", "setRevoked", "recordVerification"]:
        status = "OK" if symbol in contract else "FAIL"
        checks.append(Check(status, f"contract:{symbol}", "present" if status == "OK" else "missing"))

    env_example = read_text("contracts/.env.example") if (ROOT / "contracts/.env.example").exists() else ""
    for name in ["OG_RPC_URL", "OG_PRIVATE_KEY", "OG_CHAIN_ID", "OG_EXPLORER_URL", "PRIVYGATE_REGISTRY_ADDRESS"]:
        status = "OK" if name in env_example else "FAIL"
        checks.append(Check(status, f"env example:{name}", "present" if status == "OK" else "missing"))

    env_path = ROOT / "contracts/.env"
    if env_path.exists():
        checks.append(Check("BLOCKED", "contracts/.env", "local secret file exists; do not commit or expose it"))
    else:
        checks.append(Check("OK", "contracts/.env", "not present"))
    return checks


def check_media_assets() -> list[Check]:
    expected = {
        "docs/hackathon/assets/privygate-share-card.png": (1600, 900),
        "docs/hackathon/assets/privygate-mobile-story.png": (1080, 1920),
    }
    checks: list[Check] = []
    for relative, dimensions in expected.items():
        path = ROOT / relative
        if not path.exists():
            checks.append(Check("FAIL", f"asset:{relative}", "missing"))
            continue
        actual = png_dimensions(path)
        if actual == dimensions:
            checks.append(Check("OK", f"asset:{relative}", f"{actual[0]}x{actual[1]}"))
        else:
            checks.append(Check("FAIL", f"asset:{relative}", f"expected {dimensions[0]}x{dimensions[1]}, got {actual[0]}x{actual[1]}"))
    return checks


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return (0, 0)
    return struct.unpack(">II", header[16:24])


def check_placeholders() -> list[Check]:
    checks: list[Check] = []
    pattern = re.compile("|".join(f"(?:{item})" for item in PLACEHOLDER_PATTERNS))
    for relative in PUBLIC_PLACEHOLDER_FILES:
        path = ROOT / relative
        if not path.exists():
            checks.append(Check("FAIL", f"placeholders:{relative}", "file missing"))
            continue
        matches = sorted(set(pattern.findall(path.read_text(encoding="utf-8"))))
        if matches:
            sample = ", ".join(matches[:6])
            checks.append(Check("BLOCKED", f"placeholders:{relative}", f"replace before submission: {sample}"))
        else:
            checks.append(Check("OK", f"placeholders:{relative}", "no public placeholders found"))
    return checks


def iter_public_text_files() -> list[Path]:
    files: list[Path] = []
    for relative in PUBLIC_SCAN_ROOTS:
        root = ROOT / relative
        if not root.exists():
            continue
        if root.is_file():
            candidates = [root]
        else:
            candidates = [path for path in root.rglob("*") if path.is_file()]
        for path in candidates:
            relative_parts = path.relative_to(ROOT).parts
            if any(part in PUBLIC_EXCLUDE_NAMES for part in relative_parts):
                continue
            if path.suffix.lower() in PUBLIC_TEXT_SUFFIXES:
                files.append(path)
    return files


def check_public_release_safety() -> list[Check]:
    checks: list[Check] = []

    blocked_found = []
    for relative in BLOCKED_RELEASE_PATHS:
        path = ROOT / relative
        if path.exists():
            blocked_found.append(relative)
    if blocked_found:
        checks.append(Check("BLOCKED", "release blocked paths", ", ".join(blocked_found)))
    else:
        checks.append(Check("OK", "release blocked paths", "no local secret or local-only submission files found"))

    generated_found = []
    for relative in GENERATED_LOCAL_PATHS:
        path = ROOT / relative
        if path.exists():
            generated_found.append(relative)
    if generated_found:
        checks.append(Check("OK", "release generated paths", "ignored/excluded locally: " + ", ".join(generated_found)))
    else:
        checks.append(Check("OK", "release generated paths", "no local generated dependency paths found"))

    local_path_hits: list[str] = []
    secret_hits: list[str] = []
    local_path_regex = re.compile("|".join(f"(?:{pattern})" for pattern in LOCAL_PATH_PATTERNS))
    for path in iter_public_text_files():
        relative = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if local_path_regex.search(text):
            local_path_hits.append(relative)
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                secret_hits.append(f"{relative}:{label}")

    if local_path_hits:
        checks.append(Check("BLOCKED", "public local paths", ", ".join(sorted(set(local_path_hits))[:8])))
    else:
        checks.append(Check("OK", "public local paths", "no local absolute paths in public materials"))

    if secret_hits:
        checks.append(Check("BLOCKED", "public secret scan", ", ".join(sorted(set(secret_hits))[:8])))
    else:
        checks.append(Check("OK", "public secret scan", "no obvious private key or token patterns found"))

    return checks


def check_tooling() -> list[Check]:
    checks: list[Check] = []
    python = sys.executable
    checks.append(Check("OK", "python", python))

    node_commands = command_candidates("node")
    bundled_node = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe"
    if bundled_node.exists():
        node_commands.append([str(bundled_node), "--version"])

    working_node = first_working_command(node_commands)
    if working_node:
        checks.append(Check("OK", "node", working_node))
    else:
        checks.append(Check("BLOCKED", "node", "node not found or not executable"))

    package_managers = []
    for name in ("npm", "pnpm", "yarn", "corepack"):
        version = first_working_command(command_candidates(name))
        if version:
            package_managers.append(f"{name} {version}")
    if package_managers:
        checks.append(Check("OK", "package manager", ", ".join(package_managers)))
    else:
        checks.append(Check("BLOCKED", "package manager", "npm/pnpm/yarn/corepack not available; Hardhat cannot run"))
    return checks


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


def command_candidates(name: str) -> list[list[str]]:
    return [[executable, "--version"] for executable in candidate_executables(name)]


def first_working_command(commands: list[list[str]]) -> str:
    for command in commands:
        try:
            result = subprocess.run(
                command,
                cwd=ROOT,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            return f"{command[0]} {version}".strip()
    return ""


def check_git() -> list[Check]:
    try:
        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        return [Check("WARN", "git status", f"could not run git: {exc}")]
    if status.returncode != 0:
        return [Check("WARN", "git status", status.stderr.strip() or "git status failed")]
    if status.stdout.strip():
        return [Check("WARN", "git status", "working tree has uncommitted changes")]
    return [Check("OK", "git status", "working tree clean")]


def run_checks() -> list[Check]:
    checks: list[Check] = []
    checks.extend(check_required_files())
    checks.extend(check_readme())
    checks.extend(check_static_web())
    checks.extend(check_contract_scaffold())
    checks.extend(check_media_assets())
    checks.extend(check_placeholders())
    checks.extend(check_public_release_safety())
    checks.extend(check_tooling())
    checks.extend(check_git())
    return checks


def print_report(checks: list[Check]) -> None:
    counts = {status: 0 for status in ("OK", "WARN", "BLOCKED", "FAIL")}
    for check in checks:
        counts[check.status] = counts.get(check.status, 0) + 1

    print("PrivyGate Hackathon Readiness Check")
    print("=" * 39)
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
        items = [check for check in checks if check.status == status]
        if not items:
            continue
        print(status)
        print("-" * len(status))
        for item in items:
            print(f"- {item.name}: {item.detail}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Check PrivyGate hackathon submission readiness.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a non-zero exit code if any FAIL or BLOCKED item remains.",
    )
    args = parser.parse_args()

    checks = run_checks()
    print_report(checks)

    if any(check.status == "FAIL" for check in checks):
        return 1
    if args.strict and any(check.status == "BLOCKED" for check in checks):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
