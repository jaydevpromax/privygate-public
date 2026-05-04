from __future__ import annotations

import argparse
import json
from typing import Any

from privygate import (
    Attribute,
    InMemoryRegistry,
    authority_setup,
    encode_policy,
    issue_credential,
    register_authority,
    revoke_credential,
    setup,
    sign,
    user_setup,
    verify,
)
from privygate.core import SigningError


def build_demo(agent: str, tool: str, message: str) -> dict[str, Any]:
    params = setup(epoch=1)
    registry = InMemoryRegistry()

    university_sk, university_pk = authority_setup(params, "University")
    lab_sk, lab_pk = authority_setup(params, "Lab")
    dao_sk, dao_pk = authority_setup(params, "DAO")
    for pk in (university_pk, lab_pk, dao_pk):
        register_authority(pk, registry)

    student = Attribute("University", "role", "student")
    researcher = Attribute("Lab", "role", "researcher")
    policy = encode_policy(
        "University:role:student AND Lab:role:researcher",
        [student, researcher],
        threshold=2,
    )
    registry.register_policy(policy)

    alice_secret, alice_commitment = user_setup(params, "alice")
    bob_secret, bob_commitment = user_setup(params, "bob")

    alice_student = issue_credential(params, university_sk, university_pk, alice_commitment, student, params.epoch)
    alice_researcher = issue_credential(params, lab_sk, lab_pk, alice_commitment, researcher, params.epoch)
    bob_student = issue_credential(params, university_sk, university_pk, bob_commitment, student, params.epoch)

    authority_pks = {"University": university_pk, "Lab": lab_pk, "DAO": dao_pk}
    message_bytes = message.encode("utf-8")

    alice_signature = sign(params, alice_secret, [alice_student, alice_researcher], policy, message_bytes)
    alice_result = verify(params, authority_pks, policy, message_bytes, alice_signature)

    try:
        sign(params, bob_secret, [bob_student], policy, message_bytes)
        bob_result = {"accepted": True, "reason": "unexpectedly signed"}
    except SigningError as exc:
        bob_result = {"accepted": False, "reason": str(exc)}

    revoke_credential(alice_researcher.credential_id, registry)
    revoked_result = verify(
        params,
        authority_pks,
        policy,
        message_bytes,
        alice_signature,
        revocation_registry=registry.revoked_credentials,
    )

    return {
        "project": "PrivyGate",
        "backend": params.backend,
        "scenario": {
            "agent": agent,
            "tool": tool,
            "message": message,
            "policy": policy.expression,
        },
        "authorities": [
            {"authority_id": pk.authority_id, "public_key_hash": pk.public_key_hash}
            for pk in (university_pk, lab_pk, dao_pk)
        ],
        "credentials": {
            "alice": [alice_student.attribute.namespace, alice_researcher.attribute.namespace],
            "bob": [bob_student.attribute.namespace],
        },
        "alice_verification": {
            "accepted": alice_result.accepted,
            "reason": alice_result.reason,
            "matched_attributes": alice_result.matched_attributes,
            "audit_hash": alice_result.audit_hash,
            "signature_id": alice_signature.signature_id,
        },
        "bob_attempt": bob_result,
        "revocation": {
            "credential_id": alice_researcher.credential_id,
            "accepted_after_revocation": revoked_result.accepted,
            "reason": revoked_result.reason,
            "audit_hash": revoked_result.audit_hash,
        },
        "og_chain_evidence_plan": [
            "registerAuthority(University)",
            "registerAuthority(Lab)",
            "registerPolicy(ResearchPolicy)",
            "recordVerification(success)",
            "setRevoked(Alice researcher credential)",
            "recordVerification(after revocation)",
        ],
        "note": "Research prototype using symbolic field arithmetic; not production cryptography.",
    }


def print_human(result: dict[str, Any]) -> None:
    scenario = result["scenario"]
    print("PrivyGate Demo")
    print("=" * 14)
    print(f"Backend: {result['backend']}")
    print(f"Agent:   {scenario['agent']}")
    print(f"Tool:    {scenario['tool']}")
    print(f"Message: {scenario['message']}")
    print(f"Policy:  {scenario['policy']}")
    print()

    print("1. Authorities")
    for authority in result["authorities"]:
        print(f"   - {authority['authority_id']} registered, key hash {authority['public_key_hash'][:16]}...")
    print()

    print("2. Credentials")
    print(f"   - Alice: {', '.join(result['credentials']['alice'])}")
    print(f"   - Bob:   {', '.join(result['credentials']['bob'])}")
    print()

    alice = result["alice_verification"]
    print("3. Alice requests the protected tool")
    print(f"   Result: {'ACCEPT' if alice['accepted'] else 'REJECT'}")
    print(f"   Reason: {alice['reason']}")
    print(f"   Matched attributes: {', '.join(alice['matched_attributes'])}")
    print(f"   Audit hash: {alice['audit_hash']}")
    print()

    bob = result["bob_attempt"]
    print("4. Bob requests the same tool")
    print(f"   Result: {'ACCEPT' if bob['accepted'] else 'REJECT'}")
    print(f"   Reason: {bob['reason']}")
    print()

    revocation = result["revocation"]
    print("5. Alice's researcher credential is revoked")
    print(f"   Revoked credential id: {revocation['credential_id']}")
    print(f"   Old signature after revocation: {'ACCEPT' if revocation['accepted_after_revocation'] else 'REJECT'}")
    print(f"   Reason: {revocation['reason']}")
    print()

    print("6. 0G chain evidence to record after deployment")
    for item in result["og_chain_evidence_plan"]:
        print(f"   - {item}")
    print()
    print(result["note"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the PrivyGate agent authorization demo.")
    parser.add_argument("--agent", default="ResearchAgent", help="Agent name shown in the demo.")
    parser.add_argument("--tool", default="private-dataset.read", help="Protected tool name.")
    parser.add_argument(
        "--message",
        default="invoke private-dataset.read for lab dataset summary",
        help="Message bound to the attribute signature.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    args = parser.parse_args()

    result = build_demo(agent=args.agent, tool=args.tool, message=args.message)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)


if __name__ == "__main__":
    main()
