"""PrivyGate research prototype.

This package implements the first runnable loop for the thesis project:
setup -> authority setup -> credential issuing -> policy encoding -> sign -> verify.

The current backend is a symbolic finite-field prototype. It is suitable for
workflow validation, API development, demos, and repeatable experiments. It is
not a production cryptographic implementation.
"""

from .core import (
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

__all__ = [
    "Attribute",
    "AttributeSignature",
    "AuthorityPublicKey",
    "AuthoritySecretKey",
    "Credential",
    "InMemoryRegistry",
    "Policy",
    "SystemParams",
    "VerificationResult",
    "authority_setup",
    "encode_policy",
    "issue_credential",
    "register_authority",
    "revoke_credential",
    "setup",
    "sign",
    "user_setup",
    "verify",
]

