# PrivyGate X/Twitter 公开发布草稿

最后更新：2026-05-03

用途：0G APAC Hackathon 公开发布。正式上线前必须替换本文末尾列出的 GitHub、Demo、0G Explorer 占位符。

## 中文版本

我们正在构建 PrivyGate：一个面向 AI agent 私有数据和工具访问控制的去中心化多机构属性签名原型。

它解决的问题很直接：钱包地址只能证明地址所有权，却不能表达“我同时被大学、实验室、DAO 等多个机构确认具备某些资格”。在 agent 调用私有数据集或敏感工具时，用户也不应该暴露完整身份和全部凭证。

PrivyGate 让多个独立机构签发属性，用户或 agent 操作者只证明自己满足策略，例如：

`University:role:student AND Lab:role:researcher`

当前版本包含：

- Python 符号域属性签名原型
- 可录制的 CLI demo：`scripts/privygate_cli.py`
- 0G Chain registry 合约：`contracts/contracts/PrivyGateRegistry.sol`
- 论文初稿：去中心化的多机构属性签名算法设计与实现

0G 在这里作为可审计登记层，用于记录 authority、公钥哈希、policy hash、撤销状态和验证事件。

GitHub: https://github.com/jaydevpromax/privygate-public
Demo: <DEMO_VIDEO_URL>
0G Explorer: https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0

## English Version

We are building PrivyGate: a decentralized multi-authority attribute-signature prototype for private data and tool access control in AI agent workflows.

The problem is simple: wallet ownership is too coarse for real authorization. An agent may need to prove that its operator is both a university student and a lab researcher, without revealing their full identity or every credential they hold.

PrivyGate lets independent authorities issue attributes, while the requester only proves that a policy is satisfied, for example:

`University:role:student AND Lab:role:researcher`

Current hackathon build:

- Python symbolic-field attribute-signature prototype
- Recording-friendly CLI demo: `scripts/privygate_cli.py`
- 0G Chain registry contract: `contracts/contracts/PrivyGateRegistry.sol`
- Research draft on decentralized multi-authority attribute signatures

0G is used as the auditable registry layer for authorities, public-key hashes, policy hashes, revocations, and verification events.

GitHub: https://github.com/jaydevpromax/privygate-public
Demo: <DEMO_VIDEO_URL>
0G Explorer: https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0

## 短版

PrivyGate is a privacy-preserving multi-authority attribute authorization prototype for AI agents on 0G.

Instead of revealing full identity data, a requester proves it satisfies a policy like:

`University:role:student AND Lab:role:researcher`

Built with a Python symbolic prototype, CLI demo, and 0G mainnet registry contract.

GitHub: https://github.com/jaydevpromax/privygate-public
Demo: <DEMO_VIDEO_URL>
0G Explorer: https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0

## 带标签版

PrivyGate brings privacy-preserving, multi-authority attribute authorization to AI agent workflows.

Users or agent operators can prove they satisfy policies like:

`University:role:student AND Lab:role:researcher`

without exposing full identity or all credentials.

Built for the 0G APAC Hackathon:

- Python symbolic-field prototype
- CLI demo
- `PrivyGateRegistry` contract on 0G mainnet
- 0G auditable registry design

GitHub: https://github.com/jaydevpromax/privygate-public
Demo: <DEMO_VIDEO_URL>
0G Explorer: https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0

#0GHackathon #BuildOn0G #AIagents #Privacy #Web3 #AccessControl

## 上线后必须替换的占位符

| 占位符 | 替换为 |
|---|---|
| `<DEMO_VIDEO_URL>` | 3 分钟以内 Demo 视频链接 |
| `0G mainnet contract address` | `0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| `0G Explorer activity link` | `https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |

## 发布前检查

- 如果 0G mainnet 尚未部署，不要发布“deployed on 0G mainnet”。
- 如果只有合约脚手架，不要把未替换的 0G Explorer 占位符留在公开帖子中。
- 如要 tag 官方账号，发布前确认 0G 当前官方 X 账号拼写。
- 附图建议优先使用：`docs/hackathon/assets/privygate-share-card.png`；移动端或短视频封面可用 `docs/hackathon/assets/privygate-mobile-story.png`。
- 如果 0G 已部署，可再追加 0G Explorer 页面截图或 CLI 成功/失败输出截图。
- 不要声称当前版本是生产级密码学；可描述为 symbolic prototype / research prototype。
