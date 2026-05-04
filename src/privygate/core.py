"""Core PrivyGate research prototype.

The implementation uses a symbolic exponent-field backend. Public keys and
credential components are represented as field elements that behave like
exponents in a bilinear-map construction. This lets the project validate the
multi-authority ABS workflow before introducing a real pairing library.
"""

from __future__ import annotations

import secrets
from typing import Iterable

from .hashing import digest_hex, hash_bytes, hash_scalar
from .models import (
    Attribute,
    AttributeSignature,
    AuthorityPublicKey,
    AuthoritySecretKey,
    Credential,
    Policy,
    SystemParams,
    VerificationResult,
)
from .registry import InMemoryRegistry


DEFAULT_GROUP_ORDER = 2**255 - 19


class SigningError(ValueError):
    """Raised when a signer cannot produce a valid attribute signature."""


def setup(security_param: int = 128, epoch: int = 1) -> SystemParams:
    return SystemParams(
        curve="symbolic-bn254-like",
        group_order=DEFAULT_GROUP_ORDER,
        g1=1,
        g2=2,
        gt=3,
        hash_to_scalar_id="sha256-to-field",
        hash_to_group_id="sha256-to-symbolic-group",
        epoch=epoch,
        security_param=security_param,
    )


def authority_setup(params: SystemParams, authority_id: str) -> tuple[AuthoritySecretKey, AuthorityPublicKey]:
    alpha = secrets.randbelow(params.group_order - 1) + 1
    secret_key = AuthoritySecretKey(authority_id=authority_id, alpha=alpha)
    public_key_value = alpha
    public_key_hash = digest_hex("authority-public-key", authority_id, public_key_value, params.epoch)
    public_key = AuthorityPublicKey(
        authority_id=authority_id,
        public_key=public_key_value,
        public_key_hash=public_key_hash,
        registered_at_epoch=params.epoch,
    )
    return secret_key, public_key


def register_authority(public_key: AuthorityPublicKey, registry: InMemoryRegistry | None = None) -> str:
    if registry is None:
        return digest_hex("register-authority", public_key.authority_id, public_key.public_key_hash)
    return registry.register_authority(public_key)


def user_setup(params: SystemParams, user_label: str | None = None) -> tuple[int, str]:
    if user_label is None:
        user_secret = secrets.randbelow(params.group_order - 1) + 1
    else:
        user_secret = hash_scalar(params.group_order, "demo-user", user_label)
    user_commitment = digest_hex("user-binding", user_secret)
    return user_secret, user_commitment


def issue_credential(
    params: SystemParams,
    authority_sk: AuthoritySecretKey,
    authority_pk: AuthorityPublicKey,
    user_commitment: str,
    attribute: Attribute,
    epoch: int,
) -> Credential:
    if authority_sk.authority_id != authority_pk.authority_id:
        raise ValueError("authority secret key and public key belong to different authorities")
    if attribute.authority_id != authority_sk.authority_id:
        raise ValueError("attribute authority does not match issuer")

    base = _credential_base(params, attribute, user_commitment, epoch)
    secret_component = (base * authority_sk.alpha) % params.group_order
    credential_id = digest_hex(
        "credential",
        attribute.namespace,
        user_commitment,
        authority_pk.public_key_hash,
        epoch,
        secret_component,
    )
    return Credential(
        credential_id=credential_id,
        user_binding_commitment=user_commitment,
        attribute=attribute,
        secret_component=secret_component,
        issuer_public_key_hash=authority_pk.public_key_hash,
        epoch=epoch,
    )


def encode_policy(expression: str, attributes: list[Attribute], threshold: int) -> Policy:
    if not attributes:
        raise ValueError("policy must contain at least one attribute")
    if threshold < 1 or threshold > len(attributes):
        raise ValueError("threshold must be between 1 and the number of attributes")

    namespaces = [attribute.namespace for attribute in attributes]
    policy_hash = digest_hex("policy", expression, namespaces, threshold)
    policy_id = digest_hex("policy-id", policy_hash)[:16]
    return Policy(
        policy_id=policy_id,
        expression=expression,
        required_attributes=tuple(attributes),
        threshold=threshold,
        policy_hash=policy_hash,
    )


def sign(
    params: SystemParams,
    user_secret: int,
    credentials: list[Credential],
    policy: Policy,
    message: bytes,
    revoked_credentials: set[str] | None = None,
) -> AttributeSignature:
    revoked_credentials = revoked_credentials or set()
    expected_commitment = digest_hex("user-binding", user_secret)
    selected = _select_credentials(params, credentials, policy, expected_commitment, revoked_credentials)
    if len(selected) < policy.threshold:
        raise SigningError("insufficient non-revoked credentials for policy")

    selected = selected[: policy.threshold]
    message_hash = hash_bytes(message)
    selected_namespaces = tuple(credential.attribute.namespace for credential in selected)
    sigma_components = {
        credential.attribute.namespace: credential.secret_component
        for credential in selected
    }
    challenge = _challenge(params, message_hash, policy.policy_hash, expected_commitment, selected_namespaces)
    proof_commitments = {
        namespace: digest_hex("proof", namespace, component, challenge, message_hash, policy.policy_hash)
        for namespace, component in sigma_components.items()
    }
    signature_id = digest_hex(
        "attribute-signature",
        message_hash,
        policy.policy_hash,
        params.epoch,
        expected_commitment,
        selected_namespaces,
        proof_commitments,
    )
    return AttributeSignature(
        signature_id=signature_id,
        message_hash=message_hash,
        policy_hash=policy.policy_hash,
        epoch=params.epoch,
        user_binding_commitment=expected_commitment,
        sigma_components=sigma_components,
        proof_commitments=proof_commitments,
        challenge=challenge,
        selected_attributes=selected_namespaces,
    )


def verify(
    params: SystemParams,
    authority_pks: dict[str, AuthorityPublicKey],
    policy: Policy,
    message: bytes,
    signature: AttributeSignature,
    revocation_registry: set[str] | None = None,
) -> VerificationResult:
    revocation_registry = revocation_registry or set()
    message_hash = hash_bytes(message)
    if signature.message_hash != message_hash:
        return _reject("message hash mismatch", policy, signature)
    if signature.policy_hash != policy.policy_hash:
        return _reject("policy hash mismatch", policy, signature)
    if signature.epoch != params.epoch:
        return _reject("epoch mismatch", policy, signature)

    allowed = {attribute.namespace: attribute for attribute in policy.required_attributes}
    matched: list[str] = []
    for namespace in signature.selected_attributes:
        attribute = allowed.get(namespace)
        if attribute is None:
            return _reject(f"attribute {namespace} is not in policy", policy, signature)
        authority_pk = authority_pks.get(attribute.authority_id)
        if authority_pk is None:
            return _reject(f"missing authority public key: {attribute.authority_id}", policy, signature)
        component = signature.sigma_components.get(namespace)
        if component is None:
            return _reject(f"missing signature component: {namespace}", policy, signature)
        if not _component_matches(params, attribute, signature.user_binding_commitment, component, authority_pk):
            return _reject(f"invalid component for {namespace}", policy, signature)
        credential_id = _credential_id_from_public_data(
            attribute,
            signature.user_binding_commitment,
            authority_pk.public_key_hash,
            signature.epoch,
            component,
        )
        if credential_id in revocation_registry:
            return _reject(f"credential revoked: {namespace}", policy, signature)
        proof = digest_hex("proof", namespace, component, signature.challenge, message_hash, policy.policy_hash)
        if signature.proof_commitments.get(namespace) != proof:
            return _reject(f"proof commitment mismatch: {namespace}", policy, signature)
        matched.append(namespace)

    if len(set(matched)) < policy.threshold:
        return _reject("matched attributes do not satisfy threshold", policy, signature)

    expected_challenge = _challenge(
        params,
        message_hash,
        policy.policy_hash,
        signature.user_binding_commitment,
        tuple(signature.selected_attributes),
    )
    if signature.challenge != expected_challenge:
        return _reject("challenge mismatch", policy, signature)

    audit_hash = digest_hex("verification", policy.policy_id, signature.signature_id, matched, True)
    return VerificationResult(
        accepted=True,
        reason="accepted",
        audit_hash=audit_hash,
        matched_attributes=tuple(matched),
    )


def revoke_credential(credential_id: str, registry: InMemoryRegistry | None = None) -> str:
    if registry is None:
        return digest_hex("revoke-credential", credential_id)
    return registry.revoke_credential(credential_id)


def _credential_base(params: SystemParams, attribute: Attribute, user_commitment: str, epoch: int) -> int:
    return hash_scalar(params.group_order, "credential-base", attribute.namespace, user_commitment, epoch)


def _credential_id_from_public_data(
    attribute: Attribute,
    user_commitment: str,
    issuer_public_key_hash: str,
    epoch: int,
    secret_component: int,
) -> str:
    return digest_hex(
        "credential",
        attribute.namespace,
        user_commitment,
        issuer_public_key_hash,
        epoch,
        secret_component,
    )


def _select_credentials(
    params: SystemParams,
    credentials: Iterable[Credential],
    policy: Policy,
    expected_commitment: str,
    revoked_credentials: set[str],
) -> list[Credential]:
    required = {attribute.namespace for attribute in policy.required_attributes}
    selected: list[Credential] = []
    seen: set[str] = set()
    for credential in credentials:
        namespace = credential.attribute.namespace
        if namespace not in required or namespace in seen:
            continue
        if credential.user_binding_commitment != expected_commitment:
            raise SigningError("credential is bound to a different user")
        if credential.epoch != params.epoch:
            continue
        if credential.revoked or credential.credential_id in revoked_credentials:
            continue
        selected.append(credential)
        seen.add(namespace)
    return selected


def _component_matches(
    params: SystemParams,
    attribute: Attribute,
    user_commitment: str,
    component: int,
    authority_pk: AuthorityPublicKey,
) -> bool:
    base = _credential_base(params, attribute, user_commitment, params.epoch)
    expected = (base * authority_pk.public_key) % params.group_order
    return component == expected


def _challenge(
    params: SystemParams,
    message_hash: str,
    policy_hash: str,
    user_commitment: str,
    selected_attributes: tuple[str, ...],
) -> int:
    return hash_scalar(
        params.group_order,
        "fiat-shamir-challenge",
        params.backend,
        params.epoch,
        message_hash,
        policy_hash,
        user_commitment,
        selected_attributes,
    )


def _reject(reason: str, policy: Policy, signature: AttributeSignature) -> VerificationResult:
    audit_hash = digest_hex("verification", policy.policy_id, signature.signature_id, reason, False)
    return VerificationResult(accepted=False, reason=reason, audit_hash=audit_hash)

