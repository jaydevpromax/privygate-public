"""Optional FastAPI entrypoint for PrivyGate.

FastAPI is not bundled in the current local runtime. This module is written so
the route contract is ready; installing fastapi + uvicorn will make it runnable.
"""

from __future__ import annotations

from .schemas import (
    AttributeIssueRequest,
    AttributeIssueResponse,
    AuthorityRegisterRequest,
    AuthorityRegisterResponse,
    DemoStateResponse,
    PolicyCreateRequest,
    PolicyCreateResponse,
    RevokeRequest,
    RevokeResponse,
    SignRequest,
    SignResponse,
    UserCreateRequest,
    UserCreateResponse,
    VerifyRequest,
    VerifyResponse,
)
from .service import PrivyGateService, ServiceError

try:
    from fastapi import FastAPI, HTTPException
except ModuleNotFoundError:  # pragma: no cover - exercised only without FastAPI installed.
    FastAPI = None  # type: ignore[assignment]
    HTTPException = None  # type: ignore[assignment]


service = PrivyGateService()
app = FastAPI(title="PrivyGate API", version="0.1.0") if FastAPI else None


def _http_error(exc: ServiceError):
    if HTTPException is None:
        raise exc
    raise HTTPException(status_code=400, detail=str(exc))


if app is not None:

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "backend": service.params.backend}

    @app.post("/demo/seed", response_model=DemoStateResponse)
    def seed_demo() -> dict[str, object]:
        return service.seed_demo()["state"]

    @app.get("/state", response_model=DemoStateResponse)
    def state() -> dict[str, object]:
        return service.demo_state()

    @app.post("/authorities/register", response_model=AuthorityRegisterResponse)
    def register_authority_route(request: AuthorityRegisterRequest) -> dict[str, str]:
        try:
            return service.register_authority(request.authority_id)
        except ServiceError as exc:
            _http_error(exc)

    @app.post("/users/create", response_model=UserCreateResponse)
    def create_user_route(request: UserCreateRequest) -> dict[str, str]:
        try:
            return service.create_user(request.user_id)
        except ServiceError as exc:
            _http_error(exc)

    @app.post("/attributes/issue", response_model=AttributeIssueResponse)
    def issue_attribute_route(request: AttributeIssueRequest) -> dict[str, str]:
        try:
            return service.issue_attribute(request.authority_id, request.user_id, request.name, request.value)
        except ServiceError as exc:
            _http_error(exc)

    @app.post("/policies/create", response_model=PolicyCreateResponse)
    def create_policy_route(request: PolicyCreateRequest) -> dict[str, object]:
        try:
            return service.create_policy(request.expression, request.required_attributes, request.threshold)
        except ServiceError as exc:
            _http_error(exc)

    @app.post("/signatures/sign", response_model=SignResponse)
    def sign_route(request: SignRequest) -> dict[str, object]:
        try:
            return service.sign_message(request.user_id, request.policy_id, request.message)
        except ServiceError as exc:
            _http_error(exc)

    @app.post("/signatures/verify", response_model=VerifyResponse)
    def verify_route(request: VerifyRequest) -> dict[str, object]:
        try:
            return service.verify_signature(request.policy_id, request.signature_id, request.message)
        except ServiceError as exc:
            _http_error(exc)

    @app.post("/credentials/revoke", response_model=RevokeResponse)
    def revoke_route(request: RevokeRequest) -> dict[str, str]:
        try:
            return service.revoke(request.credential_id)
        except ServiceError as exc:
            _http_error(exc)

