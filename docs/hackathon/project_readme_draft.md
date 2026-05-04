# PrivyGate

Privacy-preserving multi-authority attribute authorization for autonomous agents on 0G.

## Problem

AI agents and Web3 applications increasingly need to decide whether a user or agent is allowed to call a sensitive tool, access a dataset, or enter a workflow. A wallet address alone is not enough, and exposing full identity documents or all user attributes is too invasive.

Many real permissions come from different institutions:

- a university confirms student status;
- a lab confirms researcher status;
- a DAO confirms membership;
- a compliance provider confirms KYC status.

PrivyGate lets a requester prove that they satisfy a multi-institution policy without revealing their real identity or full attribute set.

## Solution

PrivyGate is a privacy authorization gateway built around decentralized multi-authority attribute signatures.

The prototype supports this flow:

1. Multiple authorities register public key hashes.
2. Authorities issue attribute credentials to a user or agent operator.
3. A resource owner defines an access policy, such as `University:student AND Lab:researcher`.
4. The requester generates an attribute signature for a specific message or tool call.
5. The gateway verifies that the signature satisfies the policy.
6. The chain records authority registration, policy hashes, revocation status, and verification events.

## Why 0G

PrivyGate fits 0G as an authorization layer for autonomous agents:

- 0G Chain can provide the registry and audit trail for authorities, policies, revocations, and verification events.
- 0G Storage can store policy metadata, encrypted authorization logs, or agent access manifests.
- Agent workflows can call PrivyGate before invoking protected tools.

For the first 0G submission, the planned integration path is:

1. deploy `PrivyGateRegistry` on 0G Chain;
2. register demo authorities and policy hashes;
3. record a successful verification event and a revoked/failed verification event;
4. include the contract address and explorer links in the final submission.

## Current Prototype

The current repository includes:

- Python core prototype: `src/privygate/`;
- unit tests: `tests/test_core_flow.py`;
- demo script: `scripts/run_core_demo.py`;
- recording-friendly CLI demo: `scripts/privygate_cli.py`;
- benchmark script: `experiments/benchmark_core.py`;
- Solidity registry contract: `contracts/contracts/PrivyGateRegistry.sol`.

The current cryptographic backend is `symbolic-field-v1`. It is a research prototype for validating the thesis workflow, API boundaries, demo flow, and benchmark pipeline. It is not production cryptography yet.

## Run Locally

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -v
```

```powershell
$env:PYTHONPATH='src'
python .\scripts\run_core_demo.py
```

```powershell
$env:PYTHONPATH='src'
python .\scripts\privygate_cli.py
```

```powershell
$env:PYTHONPATH='src'
python .\experiments\benchmark_core.py
```

## Demo Scenario

Authorities:

- `University`
- `Lab`
- `DAO`

Policy:

```text
University:role:student AND Lab:role:researcher
```

Expected results:

- Alice has both attributes and passes verification.
- Bob has only the student attribute and cannot sign.
- Alice's researcher credential is revoked, and her previous signature fails verification after revocation.

## Roadmap

- Add FastAPI verification gateway.
- Deploy `PrivyGateRegistry` to 0G Chain.
- Add 0G Storage proof for policy metadata.
- Add an agent tool-call demo.
- Evaluate a real pairing backend for stronger cryptographic implementation.
