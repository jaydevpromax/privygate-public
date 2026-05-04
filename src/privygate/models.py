"""Data models for the PrivyGate research prototype."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SystemParams:
    curve: str
    group_order: int
    g1: int
    g2: int
    gt: int
    hash_to_scalar_id: str
    hash_to_group_id: str
    epoch: int
    security_param: int = 128
    backend: str = "symbolic-field-v1"


@dataclass(frozen=True)
class AuthoritySecretKey:
    authority_id: str
    alpha: int


@dataclass(frozen=True)
class AuthorityPublicKey:
    authority_id: str
    public_key: int
    public_key_hash: str
    registered_at_epoch: int


@dataclass(frozen=True)
class Attribute:
    authority_id: str
    name: str
    value: str

    @property
    def namespace(self) -> str:
        return f"{self.authority_id}:{self.name}:{self.value}"


@dataclass(frozen=True)
class Credential:
    credential_id: str
    user_binding_commitment: str
    attribute: Attribute
    secret_component: int
    issuer_public_key_hash: str
    epoch: int
    revoked: bool = False


@dataclass(frozen=True)
class Policy:
    policy_id: str
    expression: str
    required_attributes: tuple[Attribute, ...]
    threshold: int
    policy_hash: str


@dataclass(frozen=True)
class AttributeSignature:
    signature_id: str
    message_hash: str
    policy_hash: str
    epoch: int
    user_binding_commitment: str
    sigma_components: dict[str, int]
    proof_commitments: dict[str, str]
    challenge: int
    selected_attributes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class VerificationResult:
    accepted: bool
    reason: str
    audit_hash: str
    matched_attributes: tuple[str, ...] = field(default_factory=tuple)

