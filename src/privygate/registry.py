"""Small in-memory registry used by demos and tests."""

from __future__ import annotations

from dataclasses import dataclass, field

from .hashing import digest_hex
from .models import AuthorityPublicKey, Policy


@dataclass
class InMemoryRegistry:
    authorities: dict[str, AuthorityPublicKey] = field(default_factory=dict)
    policies: dict[str, Policy] = field(default_factory=dict)
    revoked_credentials: set[str] = field(default_factory=set)
    verification_events: list[dict[str, object]] = field(default_factory=list)

    def register_authority(self, public_key: AuthorityPublicKey) -> str:
        self.authorities[public_key.authority_id] = public_key
        return digest_hex("register-authority", public_key.authority_id, public_key.public_key_hash)

    def register_policy(self, policy: Policy) -> str:
        self.policies[policy.policy_id] = policy
        return digest_hex("register-policy", policy.policy_id, policy.policy_hash)

    def revoke_credential(self, credential_id: str) -> str:
        self.revoked_credentials.add(credential_id)
        return digest_hex("revoke-credential", credential_id)

    def record_verification(self, policy_id: str, proof_hash: str, result: bool) -> str:
        event = {
            "policy_id": policy_id,
            "proof_hash": proof_hash,
            "result": result,
        }
        self.verification_events.append(event)
        return digest_hex("verification-event", len(self.verification_events), event)

