from __future__ import annotations

import unittest

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


class PrivyGateCoreFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.params = setup(epoch=1)
        self.registry = InMemoryRegistry()

        self.university_sk, self.university_pk = authority_setup(self.params, "University")
        self.lab_sk, self.lab_pk = authority_setup(self.params, "Lab")
        self.dao_sk, self.dao_pk = authority_setup(self.params, "DAO")
        for public_key in (self.university_pk, self.lab_pk, self.dao_pk):
            register_authority(public_key, self.registry)

        self.student = Attribute("University", "role", "student")
        self.researcher = Attribute("Lab", "role", "researcher")
        self.member = Attribute("DAO", "role", "member")
        self.policy = encode_policy(
            "University:student AND Lab:researcher",
            [self.student, self.researcher],
            threshold=2,
        )
        self.registry.register_policy(self.policy)

        self.alice_secret, self.alice_commitment = user_setup(self.params, "alice")
        self.bob_secret, self.bob_commitment = user_setup(self.params, "bob")
        self.alice_student = issue_credential(
            self.params,
            self.university_sk,
            self.university_pk,
            self.alice_commitment,
            self.student,
            self.params.epoch,
        )
        self.alice_researcher = issue_credential(
            self.params,
            self.lab_sk,
            self.lab_pk,
            self.alice_commitment,
            self.researcher,
            self.params.epoch,
        )
        self.bob_student = issue_credential(
            self.params,
            self.university_sk,
            self.university_pk,
            self.bob_commitment,
            self.student,
            self.params.epoch,
        )
        self.bob_researcher = issue_credential(
            self.params,
            self.lab_sk,
            self.lab_pk,
            self.bob_commitment,
            self.researcher,
            self.params.epoch,
        )
        self.authority_pks = {
            "University": self.university_pk,
            "Lab": self.lab_pk,
            "DAO": self.dao_pk,
        }

    def test_alice_can_sign_and_verify_policy(self) -> None:
        message = b"access protected agent tool"
        signature = sign(self.params, self.alice_secret, [self.alice_student, self.alice_researcher], self.policy, message)

        result = verify(self.params, self.authority_pks, self.policy, message, signature)

        self.assertTrue(result.accepted)
        self.assertEqual(result.reason, "accepted")
        self.assertEqual(set(result.matched_attributes), {self.student.namespace, self.researcher.namespace})

    def test_bob_with_missing_attribute_cannot_sign(self) -> None:
        with self.assertRaises(SigningError):
            sign(self.params, self.bob_secret, [self.bob_student], self.policy, b"access protected agent tool")

    def test_revoked_credential_invalidates_existing_signature(self) -> None:
        message = b"access protected agent tool"
        signature = sign(self.params, self.alice_secret, [self.alice_student, self.alice_researcher], self.policy, message)
        revoke_credential(self.alice_researcher.credential_id, self.registry)

        result = verify(
            self.params,
            self.authority_pks,
            self.policy,
            message,
            signature,
            revocation_registry=self.registry.revoked_credentials,
        )

        self.assertFalse(result.accepted)
        self.assertIn("credential revoked", result.reason)

    def test_mixed_user_credentials_are_rejected_before_signing(self) -> None:
        with self.assertRaises(SigningError):
            sign(
                self.params,
                self.alice_secret,
                [self.alice_student, self.bob_researcher],
                self.policy,
                b"access protected agent tool",
            )

    def test_wrong_authority_public_key_rejects_signature(self) -> None:
        message = b"access protected agent tool"
        signature = sign(self.params, self.alice_secret, [self.alice_student, self.alice_researcher], self.policy, message)
        _, fake_lab_pk = authority_setup(self.params, "Lab")
        wrong_keys = dict(self.authority_pks)
        wrong_keys["Lab"] = fake_lab_pk

        result = verify(self.params, wrong_keys, self.policy, message, signature)

        self.assertFalse(result.accepted)
        self.assertIn("invalid component", result.reason)

    def test_tampered_message_rejects_signature(self) -> None:
        signature = sign(
            self.params,
            self.alice_secret,
            [self.alice_student, self.alice_researcher],
            self.policy,
            b"access protected agent tool",
        )

        result = verify(self.params, self.authority_pks, self.policy, b"tampered request", signature)

        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "message hash mismatch")


if __name__ == "__main__":
    unittest.main()

