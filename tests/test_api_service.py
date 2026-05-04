from __future__ import annotations

import unittest

from app.api.service import PrivyGateService, ServiceError


class PrivyGateApiServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.service = PrivyGateService()
        seeded = self.service.seed_demo()
        self.policy_id = seeded["policy"]["policy_id"]
        self.message = "invoke protected AI agent tool"

    def test_seed_demo_state(self) -> None:
        state = self.service.demo_state()

        self.assertEqual(state["backend"], "symbolic-field-v1")
        self.assertEqual(state["authorities"], ["DAO", "Lab", "University"])
        self.assertEqual(state["users"], ["alice", "bob"])
        self.assertEqual(state["credentials"], 3)

    def test_sign_and_verify_from_service(self) -> None:
        signature = self.service.sign_message("alice", self.policy_id, self.message)
        result = self.service.verify_signature(self.policy_id, signature["signature_id"], self.message)

        self.assertTrue(result["accepted"])
        self.assertEqual(result["reason"], "accepted")
        self.assertEqual(set(result["matched_attributes"]), {"University:role:student", "Lab:role:researcher"})

    def test_missing_attribute_returns_service_error(self) -> None:
        with self.assertRaises(ServiceError):
            self.service.sign_message("bob", self.policy_id, self.message)

    def test_revoke_invalidates_signature(self) -> None:
        signature = self.service.sign_message("alice", self.policy_id, self.message)
        alice_researcher_id = next(
            credential_id
            for credential_id in self.service.credentials_by_user["alice"]
            if self.service.credentials[credential_id].attribute.namespace == "Lab:role:researcher"
        )
        self.service.revoke(alice_researcher_id)

        result = self.service.verify_signature(self.policy_id, signature["signature_id"], self.message)

        self.assertFalse(result["accepted"])
        self.assertIn("credential revoked", result["reason"])


if __name__ == "__main__":
    unittest.main()

