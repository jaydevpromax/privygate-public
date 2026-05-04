# PrivyGate API

The API layer is split into two parts:

- `service.py`: framework-independent stateful service, covered by unit tests.
- `main.py`: optional FastAPI routes that delegate to the service.

## Current Runtime Status

The bundled Python runtime currently has Pydantic but does not have FastAPI or uvicorn installed. The service layer is runnable and tested now; the FastAPI entrypoint will run after installing:

```powershell
pip install fastapi uvicorn
```

Network access is restricted in the current environment, so installation is intentionally not attempted yet.

## Planned Routes

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/demo/seed` | Reset and seed the standard demo |
| `GET` | `/state` | Inspect demo state |
| `POST` | `/authorities/register` | Register an attribute authority |
| `POST` | `/users/create` | Create a demo user |
| `POST` | `/attributes/issue` | Issue an attribute credential |
| `POST` | `/policies/create` | Create a policy |
| `POST` | `/signatures/sign` | Generate an attribute signature |
| `POST` | `/signatures/verify` | Verify an attribute signature |
| `POST` | `/credentials/revoke` | Revoke a credential |

## Future Run Command

```powershell
$env:PYTHONPATH='src;.'
uvicorn app.api.main:app --reload
```

