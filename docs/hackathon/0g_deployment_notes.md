# 0G Deployment Notes

最后更新：2026-05-04

## Purpose

This document tracks 0G Chain and 0G Storage evidence for the 0G APAC submission.

## Current Status

Done:

- Minimal registry contract written: `contracts/contracts/PrivyGateRegistry.sol`.
- Contract scope defined: authority registration, policy hashes, revocation status, verification logs.
- README draft and demo script mention where the 0G evidence will appear.
- Hardhat project scaffold added under `contracts/`.
- Local contract tests written in `contracts/test/PrivyGateRegistry.test.js`.
- Deployment script added in `contracts/scripts/deploy.js`.
- Demo event recording script added in `contracts/scripts/record-demo-events.js`.
- Environment template added in `contracts/.env.example`.
- Hardhat local compile and 6 contract tests passed.
- Deployment scripts now print contract address, transaction hash, and Explorer URLs.
- 0G mainnet registry deployment and demo events are complete.
- Redacted 0G Storage audit manifest generated at `docs/hackathon/privygate_0g_storage_audit_manifest.json`.
- Optional 0G Storage upload helper added under `storage/`.
- 0G Storage audit manifest uploaded and root/transaction evidence recorded.

Pending:

- No 0G integration blocker remains. Before final submission, record the final demo video URL and public X post URL.

## Official Network Defaults

| Network | Chain ID | RPC | Explorer | Use |
|---|---:|---|---|---|
| 0G Mainnet | `16661` | `https://evmrpc.0g.ai` | `https://chainscan.0g.ai` | Final hackathon evidence |
| 0G Galileo Testnet | `16602` | `https://evmrpc-testnet.0g.ai` | `https://chainscan-galileo.0g.ai` | Rehearsal only |

Source: official 0G docs mainnet and testnet pages.

## Required Environment Variables

Use placeholders until official 0G network details and wallet are ready:

```text
OG_RPC_URL=https://evmrpc.0g.ai
OG_PRIVATE_KEY=
OG_CHAIN_ID=16661
OG_EXPLORER_URL=https://chainscan.0g.ai
PRIVYGATE_REGISTRY_ADDRESS=
```

Do not commit `.env` files.

## Local Tooling Status

Node/npm are available, Hardhat dependencies are installed, and local tests pass. Re-run this before deployment:

```powershell
cd contracts
npm install
npm test
```

## Planned Deployment Steps

1. Install Hardhat dependencies. Done.
2. Compile `PrivyGateRegistry.sol`. Done.
3. Run local tests for:
   - `registerAuthority`
   - `registerPolicy`
   - `setRevoked`
   - `recordVerification`
4. Copy `.env.example` to `.env`, fill `OG_PRIVATE_KEY`, and keep mainnet defaults unless 0G updates them.
5. Run `npm run check:og` to verify chain ID, signer address, and balance.
6. Deploy to 0G Chain with `npm run deploy:og`.
7. Record:
   - contract address;
   - explorer URL;
   - authority registration transaction;
   - policy registration transaction;
   - revocation transaction;
   - verification event transaction.
8. Update:
   - `docs/hackathon/0g_submission_checklist.md`
   - `docs/hackathon/project_readme_draft.md`
   - final public README
   - demo video script

## 0G Storage Audit Manifest

The storage audit manifest is generated locally from the same demo flow as the CLI. It contains the policy, public authority key hashes, Alice/Bob/revocation decision records, public 0G Chain evidence, and explicit redaction fields.

Generate:

```powershell
$env:PYTHONPATH='src'
python .\scripts\generate_storage_audit_manifest.py
```

Upload helper:

```powershell
cd storage
npm.cmd install
$env:OG_PRIVATE_KEY='0x...'
npm.cmd run upload:audit
```

The helper uses `OG_RPC_URL` when provided, defaults to `https://evmrpc.0g.ai`, and uses `OG_STORAGE_INDEXER_RPC` when provided, defaults to `https://indexer-storage-turbo.0g.ai`.

## Evidence Table

### 0G Galileo Testnet Rehearsal

| Evidence | Status | Value |
|---|---|---|
| Network | DONE | 0G Galileo Testnet, Chain ID `16602` |
| Registry contract address | READY | `0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| Explorer contract link | DONE | `https://chainscan-galileo.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| Deployment tx | DONE | `https://chainscan-galileo.0g.ai/tx/0x2bf6b4211b749b6480ee90883bdd53e2765f4be476c54427acfbddf20658ff25` |
| Authority registration tx: University | DONE | `https://chainscan-galileo.0g.ai/tx/0xd7f4f3c518622cf84624eb3963e3e1f6b88a8f67f3c4489bb93f2d3ec8a95966` |
| Authority registration tx: Lab | DONE | `https://chainscan-galileo.0g.ai/tx/0x59aea3b20bbdd2c001ec3df9bbb7ff48273bbf99fa1ebbda5d383d0b4aa601a9` |
| Policy registration tx | READY | [policy tx](https://chainscan.0g.ai/tx/0x4846aa7e3a522281666ab181cdb66c7ae787c59ad0d557bf29718decd8906c21) |
| Verification success tx | READY | [verification success](https://chainscan.0g.ai/tx/0x5fdfeb82d5fcd30863fb245a0ce2c7e0922f6aea2a7b68989beac976b7159ab0) |
| Revocation tx | READY | [revocation](https://chainscan.0g.ai/tx/0xcf406dfbc72c86abe86c380eb341077523e07a6a6925b1bce0cecb78427abd55) |
| Verification after revocation tx | DONE | `https://chainscan-galileo.0g.ai/tx/0xe55a6fd080df42a15d55dd9f956e86ce84b85f926e78d01962a531bd77304814` |

This rehearsal proves that the deployment scripts, registry contract, and event-recording flow work end to end on 0G Galileo. It does not replace the required 0G mainnet final evidence.

### 0G Mainnet Final Evidence

| Evidence | Status | Value |
|---|---|---|
| Network | DONE | 0G Mainnet, Chain ID `16661` |
| Registry contract address | READY | `0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| Explorer contract link | DONE | `https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| Deployment tx | DONE | `https://chainscan.0g.ai/tx/0xa28e74c61c34c8652a07845d5fca6f443d816487ca85e7576c44839576259251` |
| Authority registration tx: University | DONE | `https://chainscan.0g.ai/tx/0x64c8563ca32e96f8949aad0b348abc354adedb38fed103b5deae5af7b7748d5f` |
| Authority registration tx: Lab | DONE | `https://chainscan.0g.ai/tx/0x361e66b3e21f2eb9740c5ff3dc5db42c5dd08e994c1919de8c75523f994065aa` |
| Policy registration tx | READY | [policy tx](https://chainscan.0g.ai/tx/0x4846aa7e3a522281666ab181cdb66c7ae787c59ad0d557bf29718decd8906c21) |
| Verification success tx | READY | [verification success](https://chainscan.0g.ai/tx/0x5fdfeb82d5fcd30863fb245a0ce2c7e0922f6aea2a7b68989beac976b7159ab0) |
| Revocation tx | READY | [revocation](https://chainscan.0g.ai/tx/0xcf406dfbc72c86abe86c380eb341077523e07a6a6925b1bce0cecb78427abd55) |
| Verification after revocation tx | DONE | `https://chainscan.0g.ai/tx/0x2f26b9630ecc42c1fdfef41e2d3af1e1c0611d6028406d30d271adbd1fa1dfcf` |

### 0G Storage Evidence

| Evidence | Status | Value |
|---|---|---|
| Audit manifest path | DONE | `docs/hackathon/privygate_0g_storage_audit_manifest.json` |
| Audit manifest hash | DONE | `e760bad9008f6beea01e9d005209db8bcec83953ac38ed96cc3fa11df39aa64f` |
| Upload helper | DONE | `storage/upload-audit.mjs` |
| 0G Storage root hash | DONE | `0xe8cc7ce846e8952caa41f491041dbd424d89dd762f55b9e7482f36295d252e8f` |
| 0G Storage transaction hash | DONE | `0xdc192a3713bb96baad3880c1dce0c1a089d3b9b02c6783d1d4afa990960ac66f` |
| 0G Storage transaction link | DONE | `https://chainscan.0g.ai/tx/0xdc192a3713bb96baad3880c1dce0c1a089d3b9b02c6783d1d4afa990960ac66f` |

## Submission Language

Use this wording before deployment:

> PrivyGate includes a minimal registry contract designed for 0G Chain integration. Deployment evidence will be added before final submission.

Use this wording only after deployment:

> PrivyGate uses 0G Chain as the tamper-evident registry for authority public key hashes, policy hashes, credential revocation state, and verification event logs.

Use this wording after storage manifest generation:

> PrivyGate also generates a redacted 0G Storage audit manifest for the policy-bound agent authorization decision. The manifest can be uploaded to 0G Storage and referenced by root hash for persistent review.

## Risk

If the 0G Storage upload is blocked, fall back to:

1. keep the 0G Chain mainnet evidence as the mandatory integration proof;
2. submit the generated audit manifest and upload helper as the storage integration path;
3. clearly describe the storage upload as pending rather than completed.
