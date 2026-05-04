# PrivyGate Demo Voiceover Script

Last updated: 2026-05-04

Purpose: final English narration for a sub-3-minute 0G APAC Hackathon demo video. This script is designed to be read at a steady pace while showing the README, CLI demo, static web demo, contract code, 0G Explorer evidence, and the 0G Storage audit manifest.

## Recording Pace

- Target duration: 2:45 to 2:55.
- Target speaking pace: about 130 to 145 words per minute.
- Tone: calm, technical, judge-facing.
- Do not say: production-ready, fully anonymous, full on-chain cryptographic verification, real university integration.
- Must say: research prototype, symbolic backend, 0G Chain registry, 0G Storage audit manifest.

## Final Narration

### 0:00-0:12 Opening

PrivyGate is a privacy-preserving multi-authority attribute authorization prototype for autonomous agents on 0G.

It is built for cases where an agent needs access to private data or protected tools, but the user should not reveal their full identity or every credential they own.

### 0:12-0:33 Problem

Wallet ownership is not enough for real access control.

A private research dataset may require someone to be both a university student and a lab researcher. Those attributes are issued by different authorities, and showing full identity documents would leak unnecessary personal information.

PrivyGate turns this into a policy proof instead of an identity disclosure.

### 0:33-0:55 Architecture

The system has three layers.

Independent authorities issue attributes, such as university status or lab role.

The requester creates an authorization signature for a specific tool call and policy.

0G Chain acts as the auditable registry for authority key hashes, policy hashes, revocation state, and verification events.

0G Storage is used for a redacted audit manifest that captures the policy-bound authorization decision.

The heavy cryptographic workflow stays off-chain, while public audit evidence stays on-chain.

### 0:55-1:24 Alice Success

Here Alice has both required attributes: `University:role:student` and `Lab:role:researcher`.

Her agent requests access to `private-dataset.read`.

PrivyGate verifies that the policy is satisfied and returns accept. The verifier learns that Alice meets the policy, but does not need her real-world identity or her full credential set.

### 1:24-1:48 Bob Failure

Now Bob tries the same request.

Bob only has the university student attribute. He does not have the lab researcher credential, so the policy cannot be satisfied.

The request is rejected. Missing attributes cannot be fabricated or borrowed from another user.

### 1:48-2:10 Revocation

Next, Alice's lab researcher credential is revoked.

After revocation, her old authorization no longer verifies.

This matters for agent access control because permissions must be removable when a role changes, a credential expires, or an authority withdraws trust.

### 2:10-2:36 0G Integration

This contract is the 0G registry layer.

It records demo authorities, policy hashes, revocation state, and verification events. The final submission includes the deployed 0G contract address and Explorer activity so judges can inspect the public audit trail.

This manifest is the 0G Storage audit package. It stores redacted policy metadata, decision hashes, chain evidence, and redaction fields for persistent review.

Sensitive identity and credential data stay off-chain.

### 2:36-2:52 Boundary

This hackathon version uses a symbolic field backend.

It validates the workflow, CLI demo, service interfaces, tests, and thesis experiments, but it is not production cryptography yet.

The next step is replacing it with a real pairing backend.

### 2:52-3:00 Closing

PrivyGate demonstrates multi-authority, revocable, policy-based private authorization for autonomous agents, with Chain and Storage audit evidence on 0G.

## Ultra-Short Backup Version

PrivyGate is a privacy-preserving authorization gateway for autonomous agents on 0G.

Instead of treating wallet ownership as the only access signal, it lets a requester prove that multiple independent authorities issued the required attributes for a tool call.

In the demo, Alice has both student and researcher attributes, so her agent can access `private-dataset.read`. Bob has only the student attribute, so he is rejected. After Alice's researcher credential is revoked, her old authorization fails.

The cryptographic workflow runs off-chain. 0G Chain provides the public registry for authority keys, policy hashes, revocations, and verification events.

This is a research prototype using a symbolic backend, not production cryptography yet. The next step is a real pairing backend and full 0G deployment evidence.
