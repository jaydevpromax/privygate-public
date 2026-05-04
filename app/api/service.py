"""Stateful API service for the PrivyGate prototype.

The service intentionally avoids framework dependencies so it can be tested
without FastAPI. The optional FastAPI routes in main.py delegate to this class.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from privygate import (
    Attribute,
    AttributeSignature,
    AuthorityPublicKey,
    AuthoritySecretKey,
    Credential,
    InMemoryRegistry,
    Policy,
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


class ServiceError(ValueError):
    """Raised when API service input or state is invalid."""


@dataclass
class UserRecord:
    user_id: str
    secret: int
    commitment: str


@dataclass
class PrivyGateService:
    params_epoch: int = 1
    registry: InMemoryRegistry = field(default_factory=InMemoryRegistry)

    def __post_init__(self) -> None:
        self.params = setup(epoch=self.params_epoch)
        self.authority_sks: dict[str, AuthoritySecretKey] = {}
        self.authority_pks: dict[str, AuthorityPublicKey] = {}
        self.users: dict[str, UserRecord] = {}
        self.credentials: dict[str, Credential] = {}
        self.credentials_by_user: dict[str, list[str]] = {}
        self.policies: dict[str, Policy] = {}
        self.signatures: dict[str, AttributeSignature] = {}

    def reset(self) -> None:
        self.registry = InMemoryRegistry()
        self.__post_init__()

    def register_authority(self, authority_id: str) -> dict[str, str]:
        self._ensure_new(authority_id, self.authority_pks, "authority")
        sk, pk = authority_setup(self.params, authority_id)
        tx = register_authority(pk, self.registry)
        self.authority_sks[authority_id] = sk
        self.authority_pks[authority_id] = pk
        return {
            "authority_id": authority_id,
            "public_key_hash": pk.public_key_hash,
            "registry_tx": tx,
        }

    def create_user(self, user_id: str) -> dict[str, str]:
        self._ensure_new(user_id, self.users, "user")
        secret, commitment = user_setup(self.params, user_id)
        self.users[user_id] = UserRecord(user_id=user_id, secret=secret, commitment=commitment)
        self.credentials_by_user[user_id] = []
        return {"user_id": user_id, "user_commitment": commitment}

    def issue_attribute(self, authority_id: str, user_id: str, name: str, value: str) -> dict[str, str]:
        sk = self.authority_sks.get(authority_id)
        pk = self.authority_pks.get(authority_id)
        if sk is None or pk is None:
            raise ServiceError(f"unknown authority: {authority_id}")
        user = self.users.get(user_id)
        if user is None:
            raise ServiceError(f"unknown user: {user_id}")

        attribute = Attribute(authority_id=authority_id, name=name, value=value)
        credential = issue_credential(self.params, sk, pk, user.commitment, attribute, self.params.epoch)
        self.credentials[credential.credential_id] = credential
        self.credentials_by_user[user_id].append(credential.credential_id)
        return {
            "credential_id": credential.credential_id,
            "attribute_namespace": attribute.namespace,
            "user_commitment": user.commitment,
        }

    def create_policy(self, expression: str, required_attributes: list[str], threshold: int) -> dict[str, object]:
        attributes = [parse_attribute_namespace(namespace) for namespace in required_attributes]
        policy = encode_policy(expression, attributes, threshold)
        self.policies[policy.policy_id] = policy
        self.registry.register_policy(policy)
        return {
            "policy_id": policy.policy_id,
            "policy_hash": policy.policy_hash,
            "expression": policy.expression,
            "threshold": policy.threshold,
        }

    def sign_message(self, user_id: str, policy_id: str, message: str) -> dict[str, object]:
        user = self.users.get(user_id)
        if user is None:
            raise ServiceError(f"unknown user: {user_id}")
        policy = self.policies.get(policy_id)
        if policy is None:
            raise ServiceError(f"unknown policy: {policy_id}")

        credentials = [self.credentials[credential_id] for credential_id in self.credentials_by_user[user_id]]
        try:
            signature = sign(
                self.params,
                user.secret,
                credentials,
                policy,
                message.encode("utf-8"),
                revoked_credentials=self.registry.revoked_credentials,
            )
        except SigningError as exc:
            raise ServiceError(str(exc)) from exc
        self.signatures[signature.signature_id] = signature
        return {
            "signature_id": signature.signature_id,
            "policy_hash": signature.policy_hash,
            "selected_attributes": list(signature.selected_attributes),
        }

    def verify_signature(self, policy_id: str, signature_id: str, message: str) -> dict[str, object]:
        policy = self.policies.get(policy_id)
        if policy is None:
            raise ServiceError(f"unknown policy: {policy_id}")
        signature = self.signatures.get(signature_id)
        if signature is None:
            raise ServiceError(f"unknown signature: {signature_id}")

        result = verify(
            self.params,
            self.authority_pks,
            policy,
            message.encode("utf-8"),
            signature,
            revocation_registry=self.registry.revoked_credentials,
        )
        self.registry.record_verification(policy_id, result.audit_hash, result.accepted)
        return {
            "accepted": result.accepted,
            "reason": result.reason,
            "audit_hash": result.audit_hash,
            "matched_attributes": list(result.matched_attributes),
        }

    def revoke(self, credential_id: str) -> dict[str, str]:
        if credential_id not in self.credentials:
            raise ServiceError(f"unknown credential: {credential_id}")
        tx = revoke_credential(credential_id, self.registry)
        return {"credential_id": credential_id, "registry_tx": tx}

    def demo_state(self) -> dict[str, object]:
        return {
            "backend": self.params.backend,
            "authorities": sorted(self.authority_pks),
            "users": sorted(self.users),
            "policies": sorted(self.policies),
            "credentials": len(self.credentials),
            "signatures": len(self.signatures),
            "revoked_credentials": len(self.registry.revoked_credentials),
        }

    def seed_demo(self) -> dict[str, object]:
        self.reset()
        self.register_authority("University")
        self.register_authority("Lab")
        self.register_authority("DAO")
        self.create_user("alice")
        self.create_user("bob")
        alice_student = self.issue_attribute("University", "alice", "role", "student")
        alice_researcher = self.issue_attribute("Lab", "alice", "role", "researcher")
        self.issue_attribute("University", "bob", "role", "student")
        policy = self.create_policy(
            "University:student AND Lab:researcher",
            [alice_student["attribute_namespace"], alice_researcher["attribute_namespace"]],
            threshold=2,
        )
        return {"state": self.demo_state(), "policy": policy}

    @staticmethod
    def _ensure_new(key: str, mapping: dict[str, object], label: str) -> None:
        if not key:
            raise ServiceError(f"{label} id must not be empty")
        if key in mapping:
            raise ServiceError(f"{label} already exists: {key}")


def parse_attribute_namespace(namespace: str) -> Attribute:
    parts = namespace.split(":")
    if len(parts) != 3 or any(not part for part in parts):
        raise ServiceError(f"invalid attribute namespace: {namespace}")
    return Attribute(authority_id=parts[0], name=parts[1], value=parts[2])

