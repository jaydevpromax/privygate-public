from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class LinkSet:
    github_url: str = ""
    demo_video_url: str = ""
    x_post_url: str = ""
    contract_address: str = ""
    explorer_url: str = ""
    deploy_tx_url: str = ""
    authority_tx_url: str = ""
    policy_tx_url: str = ""
    verify_success_tx_url: str = ""
    revocation_tx_url: str = ""
    verify_failure_tx_url: str = ""

    @property
    def any_value(self) -> bool:
        return any(self.__dict__.values())

    @property
    def all_submission_links(self) -> bool:
        required = [
            self.github_url,
            self.demo_video_url,
            self.x_post_url,
            self.contract_address,
            self.explorer_url,
            self.deploy_tx_url,
            self.authority_tx_url,
            self.policy_tx_url,
            self.verify_success_tx_url,
            self.revocation_tx_url,
            self.verify_failure_tx_url,
        ]
        return all(required)


def markdown_link(label: str, value: str) -> str:
    if not value:
        return "TBD"
    if value.startswith("http://") or value.startswith("https://"):
        return f"[{label}]({value})"
    return f"`{value}`"


def load_config(path: str) -> dict[str, str]:
    if not path:
        return {}
    raw = json.loads((ROOT / path).read_text(encoding="utf-8"))
    return {str(key): str(value) for key, value in raw.items() if value}


def build_links(args: argparse.Namespace) -> LinkSet:
    config = load_config(args.config)
    values: dict[str, str] = {}
    for field in LinkSet.__dataclass_fields__:
        values[field] = getattr(args, field) or config.get(field, "")
    return LinkSet(**values)


def replace_exact(text: str, old: str, new: str) -> str:
    return text.replace(old, new) if new else text


def replace_table_row(text: str, label: str, columns: list[str]) -> str:
    escaped = re.escape(label)
    replacement = "| " + label + " | " + " | ".join(columns) + " |"
    return re.sub(rf"^\| {escaped} \|.*\|$", replacement, text, flags=re.MULTILINE)


def update_readme(text: str, links: LinkSet) -> str:
    rows = {
        "0G contract address": markdown_link("contract", links.contract_address),
        "Explorer link": markdown_link("explorer", links.explorer_url),
        "Authority registration tx": markdown_link("authority tx", links.authority_tx_url),
        "Policy registration tx": markdown_link("policy tx", links.policy_tx_url),
        "Verification success tx": markdown_link("verification success", links.verify_success_tx_url),
        "Revocation tx": markdown_link("revocation", links.revocation_tx_url),
        "Verification failure tx": markdown_link("verification failure", links.verify_failure_tx_url),
    }
    for label, value in rows.items():
        text = replace_table_row(text, label, [value])
    if links.explorer_url and links.contract_address:
        text = text.replace("Current status: deployment pending.", "Current status: deployed evidence recorded.")
    return text


def update_deployment_notes(text: str, links: LinkSet) -> str:
    rows = {
        "Registry contract address": markdown_link("contract", links.contract_address),
        "Explorer link": markdown_link("explorer", links.explorer_url),
        "Authority registration tx": markdown_link("authority tx", links.authority_tx_url),
        "Policy registration tx": markdown_link("policy tx", links.policy_tx_url),
        "Verification success tx": markdown_link("verification success", links.verify_success_tx_url),
        "Revocation tx": markdown_link("revocation", links.revocation_tx_url),
        "Verification failure tx": markdown_link("verification failure", links.verify_failure_tx_url),
    }
    for label, value in rows.items():
        status = "READY" if value != "TBD" else "TODO"
        text = replace_table_row(text, label, [status, value])
    if links.contract_address and links.explorer_url:
        text = text.replace("- Deployment transaction.", "- Deployment transaction recorded.")
        text = text.replace("- Explorer links and transaction hashes.", "- Explorer links and transaction hashes recorded.")
    return text


def update_hackquest_fields(text: str, links: LinkSet) -> str:
    row_values = {
        "Repository": links.github_url,
        "Demo video": links.demo_video_url,
        "0G contract address": links.contract_address,
        "0G explorer link": links.explorer_url,
        "X public post": links.x_post_url,
    }
    for label, value in row_values.items():
        if value:
            text = replace_table_row(text, label, [markdown_link(label, value)])

    replacements = {
        "TODO_GITHUB_REPO_URL": links.github_url,
        "TODO_DEMO_VIDEO_URL": links.demo_video_url,
        "TODO_X_POST_URL": links.x_post_url,
        "TODO_0G_CONTRACT_ADDRESS": links.contract_address,
        "TODO_0G_EXPLORER_CONTRACT_URL": links.explorer_url,
        "TODO_DEPLOY_TX_URL": links.deploy_tx_url,
        "TODO_AUTHORITY_TX_URL": links.authority_tx_url,
        "TODO_POLICY_TX_URL": links.policy_tx_url,
        "TODO_VERIFY_SUCCESS_TX_URL": links.verify_success_tx_url,
        "TODO_REVOCATION_TX_URL": links.revocation_tx_url,
        "TODO_VERIFY_FAILURE_TX_URL": links.verify_failure_tx_url,
    }
    for old, new in replacements.items():
        text = replace_exact(text, old, new)

    if links.all_submission_links:
        checklist_items = [
            "GitHub repository is public and contains the latest commit.",
            "Root `README.md` contains real 0G evidence links.",
            "`docs/hackathon/0g_deployment_notes.md` contains deployed contract and transaction URLs.",
            "Demo video is under 3 minutes and shows local CLI plus 0G explorer evidence.",
            "X post is public and points to the project or demo.",
        ]
        for item in checklist_items:
            text = text.replace(f"| TODO | {item} |", f"| READY | {item} |")
    return text


def update_x_post(text: str, links: LinkSet) -> str:
    replacements = {
        "<GITHUB_REPO_URL>": links.github_url,
        "<DEMO_VIDEO_URL>": links.demo_video_url,
        "<0G_MAINNET_CONTRACT_ADDRESS>": links.contract_address,
        "<0G_EXPLORER_ACTIVITY_LINK>": links.explorer_url,
    }
    for old, new in replacements.items():
        text = replace_exact(text, old, new)
    return text


def update_video_plan(text: str, links: LinkSet) -> str:
    replacements = {
        "<0G_MAINNET_CONTRACT_ADDRESS>": links.contract_address,
        "<0G_EXPLORER_ACTIVITY_LINK>": links.explorer_url,
        "<AUTHORITY_REGISTRATION_TX>": links.authority_tx_url,
        "<POLICY_REGISTRATION_TX>": links.policy_tx_url,
        "<VERIFICATION_SUCCESS_TX>": links.verify_success_tx_url,
        "<REVOCATION_TX>": links.revocation_tx_url,
        "<VERIFICATION_FAILURE_TX>": links.verify_failure_tx_url,
    }
    for old, new in replacements.items():
        text = replace_exact(text, old, new)
    return text


def update_checklist(text: str, links: LinkSet) -> str:
    if links.github_url:
        text = text.replace("| TODO | GitHub 仓库 |", "| READY | GitHub 仓库 |")
    if links.contract_address:
        text = text.replace("| TODO | 0G mainnet contract address |", "| READY | 0G mainnet contract address |")
    if links.explorer_url:
        text = text.replace("| TODO | 0G Explorer link |", "| READY | 0G Explorer link |")
        text = text.replace("| TODO | 0G 集成证明 |", "| READY | 0G 集成证明 |")
    return text


def update_workplan(text: str, links: LinkSet) -> str:
    replacements = {
        "| GitHub repo URL | `README.md` / HackQuest 表单 | TODO |": f"| GitHub repo URL | `README.md` / HackQuest 表单 | {markdown_link('GitHub repo', links.github_url)} |",
        "| 0G contract address | `docs/hackathon/0g_deployment_notes.md` | TODO |": f"| 0G contract address | `docs/hackathon/0g_deployment_notes.md` | {markdown_link('contract', links.contract_address)} |",
        "| Explorer deploy tx | `docs/hackathon/0g_deployment_notes.md` | TODO |": f"| Explorer deploy tx | `docs/hackathon/0g_deployment_notes.md` | {markdown_link('deploy tx', links.deploy_tx_url)} |",
        "| Authority registration tx | `docs/hackathon/0g_deployment_notes.md` | TODO |": f"| Authority registration tx | `docs/hackathon/0g_deployment_notes.md` | {markdown_link('authority tx', links.authority_tx_url)} |",
        "| Policy registration tx | `docs/hackathon/0g_deployment_notes.md` | TODO |": f"| Policy registration tx | `docs/hackathon/0g_deployment_notes.md` | {markdown_link('policy tx', links.policy_tx_url)} |",
        "| Verification event tx | `docs/hackathon/0g_deployment_notes.md` | TODO |": f"| Verification event tx | `docs/hackathon/0g_deployment_notes.md` | {markdown_link('verification success', links.verify_success_tx_url)} |",
        "| Revocation tx | `docs/hackathon/0g_deployment_notes.md` | TODO |": f"| Revocation tx | `docs/hackathon/0g_deployment_notes.md` | {markdown_link('revocation', links.revocation_tx_url)} |",
        "| Demo video URL | HackQuest 表单 / README | TODO |": f"| Demo video URL | HackQuest 表单 / README | {markdown_link('demo video', links.demo_video_url)} |",
        "| X post URL | HackQuest 表单 | TODO |": f"| X post URL | HackQuest 表单 | {markdown_link('X post', links.x_post_url)} |",
    }
    for old, new in replacements.items():
        text = replace_exact(text, old, new)
    return text


TARGETS: dict[str, Any] = {
    "README.md": update_readme,
    "docs/hackathon/0g_deployment_notes.md": update_deployment_notes,
    "docs/hackathon/hackquest_submission_fields.md": update_hackquest_fields,
    "docs/hackathon/x_post_draft.md": update_x_post,
    "docs/hackathon/video_recording_plan.md": update_video_plan,
    "docs/hackathon/0g_submission_checklist.md": update_checklist,
    "docs/hackathon/submission_workplan.md": update_workplan,
}


URL_FIELDS = [
    "github_url",
    "demo_video_url",
    "x_post_url",
    "explorer_url",
    "deploy_tx_url",
    "authority_tx_url",
    "policy_tx_url",
    "verify_success_tx_url",
    "revocation_tx_url",
    "verify_failure_tx_url",
]


EVM_ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")


def validate_links(links: LinkSet) -> list[str]:
    errors: list[str] = []
    for field in URL_FIELDS:
        value = getattr(links, field)
        if value and not (value.startswith("https://") or value.startswith("http://")):
            errors.append(f"{field} must start with http:// or https://")
        if value and any(char.isspace() for char in value):
            errors.append(f"{field} must not contain whitespace")
    if links.contract_address and not EVM_ADDRESS_RE.fullmatch(links.contract_address):
        errors.append("contract_address must be an EVM-style address like 0x followed by 40 hex characters")
    return errors


def planned_updates(links: LinkSet) -> list[tuple[str, int]]:
    changes: list[tuple[str, int]] = []
    for relative, updater in TARGETS.items():
        path = ROOT / relative
        original = path.read_text(encoding="utf-8")
        updated = updater(original, links)
        if original != updated:
            changes.append((relative, changed_line_count(original, updated)))
    return changes


def changed_line_count(original: str, updated: str) -> int:
    original_lines = original.splitlines()
    updated_lines = updated.splitlines()
    return sum(1 for old, new in zip(original_lines, updated_lines) if old != new) + abs(len(original_lines) - len(updated_lines))


def apply_updates(links: LinkSet) -> list[tuple[str, int]]:
    changes: list[tuple[str, int]] = []
    for relative, updater in TARGETS.items():
        path = ROOT / relative
        original = path.read_text(encoding="utf-8")
        updated = updater(original, links)
        if original != updated:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changes.append((relative, changed_line_count(original, updated)))
    return changes


def print_missing(links: LinkSet) -> None:
    missing = [key for key, value in links.__dict__.items() if not value]
    if missing:
        print("Missing values:")
        for key in missing:
            print(f"- {key}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill final HackQuest/0G submission links into public materials.")
    parser.add_argument("--config", default="", help="Optional JSON file relative to the repository root.")
    for field in LinkSet.__dataclass_fields__:
        parser.add_argument(f"--{field.replace('_', '-')}", default="")
    parser.add_argument("--apply", action="store_true", help="Write updates. Without this flag, only print a dry-run report.")
    args = parser.parse_args()

    links = build_links(args)
    if not links.any_value:
        print("No submission links provided. Pass CLI flags or --config.")
        print_missing(links)
        return 1
    errors = validate_links(links)
    if errors:
        print("Invalid submission links:")
        for error in errors:
            print(f"- {error}")
        return 2

    changes = apply_updates(links) if args.apply else planned_updates(links)
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"PrivyGate submission link update: {mode}")
    print("=" * 39)
    print_missing(links)
    if changes:
        print("Files to update:" if not args.apply else "Files updated:")
        for relative, line_count in changes:
            print(f"- {relative}: {line_count} changed lines")
    else:
        print("No file changes needed.")

    if not args.apply:
        print()
        print("Re-run with --apply after reviewing the planned updates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
