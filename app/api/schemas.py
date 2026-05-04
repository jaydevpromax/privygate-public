"""Pydantic schemas for the optional FastAPI layer."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AuthorityRegisterRequest(BaseModel):
    authority_id: str = Field(min_length=1)


class AuthorityRegisterResponse(BaseModel):
    authority_id: str
    public_key_hash: str
    registry_tx: str


class UserCreateRequest(BaseModel):
    user_id: str = Field(min_length=1)


class UserCreateResponse(BaseModel):
    user_id: str
    user_commitment: str


class AttributeIssueRequest(BaseModel):
    authority_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    value: str = Field(min_length=1)


class AttributeIssueResponse(BaseModel):
    credential_id: str
    attribute_namespace: str
    user_commitment: str


class PolicyCreateRequest(BaseModel):
    expression: str = Field(min_length=1)
    required_attributes: list[str] = Field(min_length=1)
    threshold: int = Field(ge=1)


class PolicyCreateResponse(BaseModel):
    policy_id: str
    policy_hash: str
    expression: str
    threshold: int


class SignRequest(BaseModel):
    user_id: str = Field(min_length=1)
    policy_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class SignResponse(BaseModel):
    signature_id: str
    policy_hash: str
    selected_attributes: list[str]


class VerifyRequest(BaseModel):
    policy_id: str = Field(min_length=1)
    signature_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class VerifyResponse(BaseModel):
    accepted: bool
    reason: str
    audit_hash: str
    matched_attributes: list[str]


class RevokeRequest(BaseModel):
    credential_id: str = Field(min_length=1)


class RevokeResponse(BaseModel):
    credential_id: str
    registry_tx: str


class DemoStateResponse(BaseModel):
    backend: str
    authorities: list[str]
    users: list[str]
    policies: list[str]
    credentials: int
    signatures: int
    revoked_credentials: int

