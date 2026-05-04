from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/hackathon/privygate_0g_storage_audit_manifest.json"

sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from privygate.hashing import canonical_json, digest_hex  # noqa: E402
from privygate_cli import build_demo  # noqa: E402


MAINNET_EVIDENCE = {
    "network": "0G Mainnet",
    "chain_id": 16661,
    "registry_contract": "0x1b55C901A69fE53a70F0011579d3576684FAAdc0",
    "explorer_contract": "https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0",
    "deploy_tx": "https://chainscan.0g.ai/tx/0xa28e74c61c34c8652a07845d5fca6f443d816487ca85e7576c44839576259251",
    "authority_university_tx": "https://chainscan.0g.ai/tx/0x64c8563ca32e96f8949aad0b348abc354adedb38fed103b5deae5af7b7748d5f",
    "authority_lab_tx": "https://chainscan.0g.ai/tx/0x361e66b3e21f2eb9740c5ff3dc5db42c5dd08e994c1919de8c75523f994065aa",
    "policy_tx": "https://chainscan.0g.ai/tx/0x4846aa7e3a522281666ab181cdb66c7ae787c59ad0d557bf29718decd8906c21",
    "verification_success_tx": "https://chainscan.0g.ai/tx/0x5fdfeb82d5fcd30863fb245a0ce2c7e0922f6aea2a7b68989beac976b7159ab0",
    "revocation_tx": "https://chainscan.0g.ai/tx/0xcf406dfbc72c86abe86c380eb341077523e07a6a6925b1bce0cecb78427abd55",
    "verification_after_revocation_tx": "https://chainscan.0g.ai/tx/0x2f26b9630ecc42c1fdfef41e2d3af1e1c0611d6028406d30d271adbd1fa1dfcf",
}


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    demo = build_demo(agent=args.agent, tool=args.tool, message=args.message)
    manifest: dict[str, Any] = {
        "schema": "privygate.storage-audit.v1",
        "project": "PrivyGate",
        "generated_at_utc": args.generated_at_utc,
        "purpose": "Upload-ready 0G Storage audit manifest for an agent authorization decision.",
        "prototype_boundary": {
            "backend": demo["backend"],
            "cryptography": "symbolic research backend; not production cryptography",
            "verification_location": "off-chain Python prototype/API layer",
            "chain_role": "0G Chain registry and public audit trail",
            "storage_role": "0G Storage audit manifest persistence",
        },
        "authorization_decision": {
            "agent": demo["scenario"]["agent"],
            "tool": demo["scenario"]["tool"],
            "message_hash": digest_hex("agent-tool-message", demo["scenario"]["message"]),
            "policy": demo["scenario"]["policy"],
            "alice": {
                "accepted": demo["alice_verification"]["accepted"],
                "reason": demo["alice_verification"]["reason"],
                "matched_attributes": list(demo["alice_verification"]["matched_attributes"]),
                "audit_hash": demo["alice_verification"]["audit_hash"],
                "signature_id": demo["alice_verification"]["signature_id"],
            },
            "bob": demo["bob_attempt"],
            "revocation": demo["revocation"],
        },
        "authorities": demo["authorities"],
        "chain_evidence": MAINNET_EVIDENCE,
        "storage_upload": {
            "status": "upload-ready",
            "root_hash": None,
            "tx_hash": None,
            "indexer_rpc": args.storage_indexer_rpc,
            "network_note": "Upload this manifest with storage/upload-audit.mjs. Record the returned root/tx outside this manifest so the content-addressed root remains valid.",
        },
        "redaction": {
            "contains_private_key": False,
            "contains_seed_phrase": False,
            "contains_raw_identity_document": False,
            "contains_raw_attribute_secret_component": False,
        },
    }
    manifest["manifest_sha256_without_this_field"] = digest_hex("storage-audit-manifest", canonical_json(manifest))
    return manifest


def write_manifest(manifest: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a 0G Storage audit manifest for the PrivyGate demo.")
    parser.add_argument("--agent", default="ResearchAgent")
    parser.add_argument("--tool", default="private-dataset.read")
    parser.add_argument("--message", default="invoke private-dataset.read for lab dataset summary")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--generated-at-utc", default="2026-05-04T00:00:00Z")
    parser.add_argument("--storage-root-hash", default="", help="Optional display-only value; not written into the manifest.")
    parser.add_argument("--storage-tx-hash", default="", help="Optional display-only value; not written into the manifest.")
    parser.add_argument("--storage-indexer-rpc", default="https://indexer-storage-turbo.0g.ai")
    args = parser.parse_args()

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    manifest = build_manifest(args)
    write_manifest(manifest, output)
    print(f"Storage audit manifest written: {output}")
    print(f"Manifest hash: {manifest['manifest_sha256_without_this_field']}")
    print("0G Storage upload status: upload-ready")
    if args.storage_root_hash or args.storage_tx_hash:
        print("Note: supplied root/tx values were not written into the manifest, so the uploaded content hash remains stable.")
        if args.storage_root_hash:
            print(f"0G Storage root: {args.storage_root_hash}")
        if args.storage_tx_hash:
            print(f"0G Storage tx: {args.storage_tx_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
