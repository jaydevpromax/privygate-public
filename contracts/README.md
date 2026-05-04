# PrivyGate Contracts

This folder contains the minimal on-chain registry layer for PrivyGate.

## Contract

- `contracts/PrivyGateRegistry.sol`

## Responsibilities

The contract records:

- authority public key hashes;
- policy hashes;
- credential revocation status;
- verification events.

It does not run full attribute-signature verification on-chain. Heavy cryptographic operations stay off-chain in the Python prototype/API layer, while the chain provides auditability and tamper-evident registration.

## 0G APAC Usage

For the 0G APAC submission, deploy `PrivyGateRegistry` to 0G Chain, then include:

- contract address;
- explorer link;
- sample transactions for authority registration, policy registration, revocation, and verification event logging.

## Next Step

Install dependencies and run local tests:

```powershell
cd contracts
npm install
npm test
```

Deploy to 0G mainnet after filling `.env` or your shell environment. The template uses Chain ID `16661`, RPC `https://evmrpc.0g.ai`, and Explorer `https://chainscan.0g.ai`.

```powershell
copy .env.example .env
# Fill OG_PRIVATE_KEY. Keep OG_RPC_URL, OG_CHAIN_ID, and OG_EXPLORER_URL unless 0G updates them.
npm run check:og
npm run deploy:og
```

Record sample audit events after deployment:

```powershell
$env:PRIVYGATE_REGISTRY_ADDRESS='<deployed-address>'
npm run record:demo:og
```

For a Galileo testnet rehearsal, fill the `OG_GALILEO_*` variables and run:

```powershell
npm run check:og:galileo
npm run deploy:og:galileo
npm run record:demo:og:galileo
```

Do not commit `.env` or private keys.
