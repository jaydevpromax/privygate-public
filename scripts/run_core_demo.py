from __future__ import annotations

import json

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


def main() -> None:
    params = setup(epoch=1)
    registry = InMemoryRegistry()

    university_sk, university_pk = authority_setup(params, "University")
    lab_sk, lab_pk = authority_setup(params, "Lab")
    dao_sk, dao_pk = authority_setup(params, "DAO")
    for pk in (university_pk, lab_pk, dao_pk):
        register_authority(pk, registry)

    student = Attribute("University", "role", "student")
    researcher = Attribute("Lab", "role", "researcher")
    policy = encode_policy("University:student AND Lab:researcher", [student, researcher], threshold=2)
    registry.register_policy(policy)

    alice_secret, alice_commitment = user_setup(params, "alice")
    bob_secret, bob_commitment = user_setup(params, "bob")
    alice_student = issue_credential(params, university_sk, university_pk, alice_commitment, student, params.epoch)
    alice_researcher = issue_credential(params, lab_sk, lab_pk, alice_commitment, researcher, params.epoch)
    bob_student = issue_credential(params, university_sk, university_pk, bob_commitment, student, params.epoch)

    authority_pks = {"University": university_pk, "Lab": lab_pk, "DAO": dao_pk}
    message = b"invoke protected AI agent tool: release lab dataset summary"
    alice_signature = sign(params, alice_secret, [alice_student, alice_researcher], policy, message)
    alice_result = verify(params, authority_pks, policy, message, alice_signature)

    try:
        sign(params, bob_secret, [bob_student], policy, message)
        bob_result = "unexpectedly signed"
    except SigningError as exc:
        bob_result = str(exc)

    revoke_credential(alice_researcher.credential_id, registry)
    revoked_result = verify(
        params,
        authority_pks,
        policy,
        message,
        alice_signature,
        revocation_registry=registry.revoked_credentials,
    )

    output = {
        "project": "PrivyGate",
        "backend": params.backend,
        "policy": policy.expression,
        "authorities": sorted(registry.authorities),
        "alice_verification": {
            "accepted": alice_result.accepted,
            "matched_attributes": alice_result.matched_attributes,
            "audit_hash": alice_result.audit_hash,
        },
        "bob_signing": bob_result,
        "after_revocation": {
            "accepted": revoked_result.accepted,
            "reason": revoked_result.reason,
        },
        "note": "Research prototype using symbolic field arithmetic; not production cryptography.",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

