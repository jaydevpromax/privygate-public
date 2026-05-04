# HackQuest 提交字段草稿

最后更新：2026-05-04

用途：提交 0G APAC Hackathon 前，把常见表单字段、公开说明和链接占位集中到一个文件中。正式提交前必须把所有 `TODO` 链接替换为真实公开地址。

官方要求来源：`https://www.hackquest.io/en/hackathons/0G-APAC-Hackathon`

## 基础字段

| 字段 | 推荐填写 |
|---|---|
| Project name | PrivyGate |
| Tagline | Privacy-preserving multi-authority attribute authorization for autonomous agents on 0G. |
| 30-word description | PrivyGate is a privacy-preserving authorization gateway that lets autonomous agents prove multi-authority attributes for tool access on 0G without exposing raw identity data. |
| Primary track | Agentic Infrastructure & OpenClaw Lab |
| Secondary track | Privacy & Sovereign Infrastructure |
| Project stage | Research prototype / hackathon MVP |
| Repository | [Repository](https://github.com/jaydevpromax/privygate-public) |
| Demo video | TODO: demo video URL, under 3 minutes |
| 0G contract address | `0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| 0G explorer link | `https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| 0G Storage audit manifest | `docs/hackathon/privygate_0g_storage_audit_manifest.json` |
| 0G Storage manifest hash | `e760bad9008f6beea01e9d005209db8bcec83953ac38ed96cc3fa11df39aa64f` |
| 0G Storage root hash | `0xe8cc7ce846e8952caa41f491041dbd424d89dd762f55b9e7482f36295d252e8f` |
| 0G Storage tx | `https://chainscan.0g.ai/tx/0xdc192a3713bb96baad3880c1dce0c1a089d3b9b02c6783d1d4afa990960ac66f` |
| X public post | TODO: X post URL |

Recommended preview image: `docs/hackathon/assets/privygate-share-card.png`

## English Project Summary

PrivyGate is a privacy-preserving authorization gateway for autonomous agents and Web3 applications. Instead of treating a wallet address as the only access signal, PrivyGate lets a requester prove that they satisfy a policy over attributes issued by multiple independent authorities, such as `University:role:student AND Lab:role:researcher`.

The prototype demonstrates a decentralized multi-authority attribute-signature workflow: authorities issue attribute credentials, a user or agent operator generates a policy-bound authorization signature, and the verifier checks whether the requested tool call is allowed. The 0G integration uses 0G Chain as an auditable registry layer for authority key hashes, policy hashes, revocation state, and verification events. It also generates a redacted 0G Storage audit manifest for the agent authorization decision.

For the demo, a `ResearchAgent` tries to call `private-dataset.read`. Alice has both required attributes and is accepted. Bob lacks one required attribute and is rejected. After Alice's researcher credential is revoked, her old authorization no longer verifies. This shows how PrivyGate can protect sensitive agent tools while reducing identity disclosure.

## 中文项目摘要

PrivyGate 是一个面向自治 Agent 和 Web3 应用的隐私授权网关。它不把钱包地址作为唯一访问依据，而是让请求方基于多个独立机构签发的属性凭证，证明自己满足访问策略，例如 `University:role:student AND Lab:role:researcher`，同时避免暴露真实身份和完整凭证集合。

当前原型实现了去中心化多机构属性签名的核心流程：机构签发属性凭证，用户或 Agent 操作者为特定工具调用生成策略绑定签名，验证方检查签名是否满足访问策略。0G 集成使用 0G Chain 作为可审计登记层，记录机构公钥哈希、策略哈希、撤销状态和验证事件；同时生成可上传到 0G Storage 的脱敏授权审计 manifest。

Demo 场景中，`ResearchAgent` 申请调用 `private-dataset.read`。Alice 同时具备学生和研究员属性，因此授权通过；Bob 缺少研究员属性，因此被拒绝；当 Alice 的研究员凭证被撤销后，旧签名也会验证失败。该流程展示了 PrivyGate 如何在 Agent 工具调用前提供可审计、可撤销、少披露的访问控制。

## Why 0G

0G is a good fit because PrivyGate separates privacy-preserving authorization from public auditability. The attribute-signature workflow stays off-chain, while 0G Chain stores tamper-evident state and events that judges can inspect:

- authority registration;
- policy hash registration;
- credential revocation state;
- successful verification events;
- failed verification events after revocation.

0G Storage complements this by persisting a redacted authorization audit manifest containing public policy metadata, decision hashes, chain evidence, and explicit redaction fields. This gives the project a Chain + Storage integration path while keeping sensitive identity and credential details off-chain.

## Technical Highlights

- Decentralized multi-authority model: no single issuer controls all user attributes.
- Policy-bound authorization: signatures are tied to a resource policy and message.
- Agent access-control scenario: demo protects `ResearchAgent` access to `private-dataset.read`.
- Revocation-aware verification: stale credentials stop working after revocation.
- Auditable registry contract: 0G Chain records public state, hashes, and events.
- Storage audit package: generated manifest can be uploaded to 0G Storage for persistent review.
- Honest cryptographic boundary: current backend is `symbolic-field-v1`, designed for workflow validation, testing, thesis experiments, and hackathon demonstration rather than production cryptography.

## Demo Flow

1. Show the README and project positioning.
2. Open `app/web/index.html` or run `scripts/privygate_cli.py`.
3. Show Alice accepted for `private-dataset.read`.
4. Show Bob rejected because he lacks the researcher attribute.
5. Show Alice rejected after credential revocation.
6. Show the 0G contract address and explorer events.
7. Show the 0G Storage audit manifest hash and upload helper.

Recommended local command:

```powershell
$env:PYTHONPATH='src'
python .\scripts\privygate_cli.py
```

## Link Placeholders

正式提交前逐项替换：

| Item | Placeholder |
|---|---|
| GitHub repo | `https://github.com/jaydevpromax/privygate-public` |
| Demo video | `TODO_DEMO_VIDEO_URL` |
| X post | `TODO_X_POST_URL` |
| 0G contract | `0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| 0G explorer contract | `https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| Deploy transaction | `https://chainscan.0g.ai/tx/0xa28e74c61c34c8652a07845d5fca6f443d816487ca85e7576c44839576259251` |
| Authority registration transaction | `https://chainscan.0g.ai/tx/0x64c8563ca32e96f8949aad0b348abc354adedb38fed103b5deae5af7b7748d5f` |
| Policy registration transaction | `https://chainscan.0g.ai/tx/0x4846aa7e3a522281666ab181cdb66c7ae787c59ad0d557bf29718decd8906c21` |
| Verification success transaction | `https://chainscan.0g.ai/tx/0x5fdfeb82d5fcd30863fb245a0ce2c7e0922f6aea2a7b68989beac976b7159ab0` |
| Revocation transaction | `https://chainscan.0g.ai/tx/0xcf406dfbc72c86abe86c380eb341077523e07a6a6925b1bce0cecb78427abd55` |
| Verification failure transaction | `https://chainscan.0g.ai/tx/0x2f26b9630ecc42c1fdfef41e2d3af1e1c0611d6028406d30d271adbd1fa1dfcf` |
| 0G Storage audit manifest hash | `e760bad9008f6beea01e9d005209db8bcec83953ac38ed96cc3fa11df39aa64f` |
| 0G Storage root hash | `0xe8cc7ce846e8952caa41f491041dbd424d89dd762f55b9e7482f36295d252e8f` |
| 0G Storage transaction hash | `0xdc192a3713bb96baad3880c1dce0c1a089d3b9b02c6783d1d4afa990960ac66f` |

## Judge-Facing Short Pitch

PrivyGate protects autonomous-agent tool calls with privacy-preserving attribute authorization. A requester proves that multiple institutions issued the required attributes, but does not reveal full identity data. 0G Chain provides the public registry and audit trail, while 0G Storage persists a redacted audit manifest for the authorization decision.

## Submission Risk Notes

- Do not claim production cryptographic security; describe the backend as a symbolic pairing-style prototype.
- Do not claim full on-chain signature verification; the intended 0G use is registry and audit evidence.
- Do not claim real university or lab integration; current authorities are demo authorities.
- Do not submit before replacing the 0G contract address and explorer links with real mainnet evidence.

## Final Form Checklist

| Status | Check |
|---|---|
| TODO | GitHub repository is public and contains the latest commit. |
| DONE | Root `README.md` contains real 0G evidence links. |
| DONE | `docs/hackathon/0g_deployment_notes.md` contains deployed contract and transaction URLs. |
| DONE | 0G Storage audit manifest is generated and referenced by hash. |
| DONE | 0G Storage root and transaction hash are recorded after upload. |
| TODO | Demo video is under 3 minutes and shows local CLI plus 0G explorer evidence. |
| TODO | X post is public and points to the project or demo. |
| TODO | HackQuest form links are tested in a private browser window. |
| TODO | Submission screenshot or confirmation ID is saved locally. |
