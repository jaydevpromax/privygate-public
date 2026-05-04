from __future__ import annotations

import unittest

from scripts.generate_storage_audit_manifest import build_manifest


class DummyArgs:
    agent = "ResearchAgent"
    tool = "private-dataset.read"
    message = "invoke private-dataset.read for lab dataset summary"
    generated_at_utc = "2026-05-04T00:00:00Z"
    storage_root_hash = ""
    storage_tx_hash = ""
    storage_indexer_rpc = "https://indexer-storage-turbo.0g.ai"


class StorageAuditManifestTest(unittest.TestCase):
    def test_manifest_contains_decision_and_public_evidence(self) -> None:
        manifest = build_manifest(DummyArgs())

        self.assertEqual(manifest["schema"], "privygate.storage-audit.v1")
        self.assertEqual(manifest["storage_upload"]["status"], "upload-ready")
        self.assertTrue(manifest["authorization_decision"]["alice"]["accepted"])
        self.assertFalse(manifest["authorization_decision"]["bob"]["accepted"])
        self.assertEqual(manifest["chain_evidence"]["chain_id"], 16661)
        self.assertIn("manifest_sha256_without_this_field", manifest)

    def test_manifest_redacts_secret_material(self) -> None:
        manifest = build_manifest(DummyArgs())
        redaction = manifest["redaction"]

        self.assertFalse(redaction["contains_private_key"])
        self.assertFalse(redaction["contains_seed_phrase"])
        self.assertFalse(redaction["contains_raw_identity_document"])
        self.assertFalse(redaction["contains_raw_attribute_secret_component"])


if __name__ == "__main__":
    unittest.main()
