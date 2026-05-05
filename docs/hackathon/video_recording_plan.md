# PrivyGate 3 分钟 Demo 视频录制方案

最后更新：2026-05-04

目标：录制一条 180 秒以内的 0G APAC Hackathon Demo 视频，清楚展示 PrivyGate 的问题、方案、可运行原型、0G Chain 链上证据、0G Storage 审计包，以及当前原型边界。

项目定位：

> PrivyGate 是面向 AI agent 私有数据和工具访问控制的去中心化多机构属性签名原型。用户或 agent 操作者可以证明自己满足多机构属性策略，例如 `University:role:student AND Lab:role:researcher`，而不需要暴露真实身份或完整凭证集合。

## 录制前准备

- 屏幕分辨率建议：1920x1080，浏览器缩放 100%，终端字体 16-18px。
- 关闭无关通知、浏览器书签栏、含私钥或账号信息的窗口。
- 提前打开：
  - README：`README.md`
  - 静态 Web Demo：`app/web/index.html`
  - 视频封面图：`docs/hackathon/assets/privygate-share-card.png`
  - CLI demo：`scripts/privygate_cli.py`
  - 0G Storage audit manifest：`docs/hackathon/privygate_0g_storage_audit_manifest.json`
  - 合约：`contracts/contracts/PrivyGateRegistry.sol`
  - 0G Explorer 合约页面或交易页面
  - 论文初稿位置：`deliverables/论文初稿.docx`
- 终端准备命令：

```powershell
$env:PYTHONPATH='src'
python .\scripts\privygate_cli.py
```

如本机 Python 路径需要固定，可改用当前环境中可运行的 Python 解释器，但视频里只需要让观众看到命令和输出，不需要展示本地绝对路径。

## 镜头顺序

| 时间 | 镜头 | 屏幕内容 | 旁白要点 | 必须展示的证据 |
|---|---|---|---|---|
| 0:00-0:12 | 开场定位 | README 标题 `PrivyGate` 和一句话描述 | PrivyGate 是面向 autonomous agents 的隐私保护多机构属性授权层，部署证据落在 0G。 | 项目名、README、一句话描述 |
| 0:12-0:32 | 问题场景 | README 的 Problem 段或简短架构图 | 钱包地址只能证明“谁持有地址”，不能表达“是否由大学、实验室、DAO 等多方确认过资格”；AI agent 调用私有工具时也不应暴露完整身份资料。 | AI agent access control 场景、隐私授权问题 |
| 0:32-0:55 | 系统架构 | `docs/hackathon/architecture.md` 或 README Solution 流程 | University、Lab、DAO 等机构独立签发属性；PrivyGate 根据策略验证属性签名；链上只记录 authority、policy、revocation、verification event 等可审计状态。 | 多机构、策略、撤销、0G registry 的关系 |
| 0:55-1:25 | 成功授权 Demo | 静态 Web Demo 中选择 Alice，或终端运行 `python .\scripts\privygate_cli.py` 并停在 Alice 成功部分 | Alice 同时拥有 `University:role:student` 和 `Lab:role:researcher`，因此可以为 `private-dataset.read` 生成满足策略的签名。验证方知道策略被满足，但不需要看到 Alice 的完整身份。 | `ACCEPT` 或 `Result: ACCEPT`；策略文本；Alice 的属性 |
| 1:25-1:48 | 失败授权 Demo | 静态 Web Demo 中选择 Bob，或同一终端输出中 Bob 失败部分 | Bob 只有 student 属性，缺少 Lab researcher，无法组合缺失属性绕过策略。 | Bob 失败输出；`insufficient non-revoked credentials for policy` 或等价错误 |
| 1:48-2:08 | 撤销 Demo | 静态 Web Demo 中选择 Alice after revocation，或同一终端输出中撤销后验证失败部分 | 当 Alice 的 Lab researcher 凭证被撤销，旧签名不再可用。撤销状态进入 registry 后，过期凭证不能继续访问私有工具。 | 撤销动作；`credential revoked` 或等价失败输出 |
| 2:08-2:38 | 0G 证据 | `contracts/contracts/PrivyGateRegistry.sol`、0G Explorer、Storage audit manifest | 当前密码学验证在链下完成，0G Chain 用作可审计登记层，0G Storage 保存脱敏授权审计 manifest。 | 合约名；0G mainnet contract address；Explorer activity link；Storage manifest hash |
| 2:38-2:52 | 原型边界 | README 的 Current Cryptographic Boundary 段 | 当前版本是 `symbolic-field-v1`，用于验证算法流程、接口、测试和论文实验；不是生产密码学实现。下一步会替换为真实 pairing backend。 | `symbolic-field-v1` 边界说明，避免误导 |
| 2:52-3:00 | 收尾 | README 或提交页草稿 | PrivyGate demonstrates policy-based, revocable, multi-authority private authorization for AI agents, with audit evidence on 0G. | GitHub、Demo、0G Explorer 三个链接占位已准备 |

## 旁白稿

### 0:00-0:12 开场

PrivyGate is a privacy-preserving multi-authority attribute authorization prototype for autonomous agents on 0G. It is designed for cases where an AI agent needs access to private data or protected tools, but the user should not reveal their full identity.

### 0:12-0:32 问题

Wallet ownership is not enough for real access control. A private dataset may require someone to be both a university student and a lab researcher. Those attributes come from different authorities, and exposing all credentials would leak unnecessary personal information.

### 0:32-0:55 架构

PrivyGate uses decentralized multi-authority attribute signatures. Independent authorities issue attributes, the requester signs a tool call against a policy, and the verifier checks whether the policy is satisfied. 0G Chain provides the audit layer for authority registration, policy hashes, revocation state, and verification events.

### 0:55-1:25 成功授权

Here Alice has both required attributes: `University:role:student` and `Lab:role:researcher`. Her agent requests `private-dataset.read`, and PrivyGate returns accept. The verifier sees that the policy is satisfied, without needing Alice's real-world identity or every credential she owns.

### 1:25-1:48 失败授权

Bob only has the university student attribute. Because he does not have the lab researcher credential, the policy cannot be satisfied and the request is rejected. Missing attributes cannot be fabricated or combined from another user.

### 1:48-2:08 撤销

Now Alice's lab researcher credential is revoked. The old signature fails after revocation, which is important for agent access control because permissions must be removable after a role changes.

### 2:08-2:38 0G 集成

The cryptographic workflow runs off-chain, and 0G Chain is used as the tamper-evident registry. This contract records authority keys, policy hashes, revocations, and verification events. PrivyGate also generates a redacted 0G Storage audit manifest for the authorization decision.

### 2:38-2:52 原型边界

This hackathon version uses a symbolic field backend to validate the attribute-signature workflow, CLI demo, service interfaces, tests, and thesis experiments. It is a research prototype, not production cryptography yet.

### 2:52-3:00 收尾

PrivyGate brings multi-authority, revocable, policy-based private authorization to AI agent workflows, with auditable evidence on 0G.

## 必须展示的证据清单

视频中至少停留到观众能看清以下内容：

- GitHub 仓库页面或本地 README，显示项目名 `PrivyGate`。
- 静态 Web Demo 页面：`app/web/index.html`。
- CLI demo 命令：`python .\scripts\privygate_cli.py`。
- 成功授权：Alice 满足 `University:role:student AND Lab:role:researcher`，输出 `ACCEPT`。
- 失败授权：Bob 缺少 `Lab:role:researcher`，输出拒绝原因。
- 撤销后失败：旧签名因撤销不再通过。
- 合约文件：`contracts/contracts/PrivyGateRegistry.sol`。
- 0G mainnet contract address：`0x1b55C901A69fE53a70F0011579d3576684FAAdc0`。
- 0G Explorer activity link：`https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0`。
- 0G Storage audit manifest：`docs/hackathon/privygate_0g_storage_audit_manifest.json`。
- 0G Storage audit manifest hash：`e760bad9008f6beea01e9d005209db8bcec83953ac38ed96cc3fa11df39aa64f`。
- 0G Storage root hash：`0xe8cc7ce846e8952caa41f491041dbd424d89dd762f55b9e7482f36295d252e8f`。
- 0G Storage tx：`0xdc192a3713bb96baad3880c1dce0c1a089d3b9b02c6783d1d4afa990960ac66f`。
- README 中的原型边界：`symbolic-field-v1`，链下符号域原型，非生产密码学。

## 正式链上证据版

如果 0G 部署已完成，2:08-2:38 镜头按以下顺序录：

1. 打开 `contracts/contracts/PrivyGateRegistry.sol`，展示合约名和事件字段。
2. 切到 0G Explorer 合约页面，展示合约地址。
3. 切到 activity 或 transaction 页面，展示至少一条真实交易。
4. 展示 0G Storage audit manifest 文件和 manifest hash。
5. 口播说明每类交易代表的含义：
   - authority registered；
   - policy hash registered；
   - verification success event；
   - credential revocation event；
   - verification failure after revocation。

录制后替换以下占位符：

- `0x1b55C901A69fE53a70F0011579d3576684FAAdc0`
- `https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0`
- `https://chainscan.0g.ai/tx/0x64c8563ca32e96f8949aad0b348abc354adedb38fed103b5deae5af7b7748d5f`
- `https://chainscan.0g.ai/tx/0x4846aa7e3a522281666ab181cdb66c7ae787c59ad0d557bf29718decd8906c21`
- `https://chainscan.0g.ai/tx/0x5fdfeb82d5fcd30863fb245a0ce2c7e0922f6aea2a7b68989beac976b7159ab0`
- `https://chainscan.0g.ai/tx/0xcf406dfbc72c86abe86c380eb341077523e07a6a6925b1bce0cecb78427abd55`
- `https://chainscan.0g.ai/tx/0x2f26b9630ecc42c1fdfef41e2d3af1e1c0611d6028406d30d271adbd1fa1dfcf`

## 链上部署暂未完成时的降级版本

如果需要备用剪辑，仍可保留“可运行原型 + 合约脚手架”的降级版，但正式提交视频应使用已完成的 0G mainnet Explorer 证据。

2:08-2:38 镜头改为：

1. 展示 `contracts/contracts/PrivyGateRegistry.sol`。
2. 展示 README 的 Contract Workflow 和 0G Evidence 表格。
3. 说明合约脚手架和主网部署证据已经准备好。
4. 如已有本地 Hardhat 测试结果，可展示 `npm test` 通过结果；如没有，不要口播“测试已通过”。

降级版旁白：

> The current recording shows the working symbolic prototype and the 0G registry contract. The final hackathon submission should use the real 0G mainnet contract address and Explorer activity link.

降级版必须避免的说法：

- 可以说“deployed on 0G mainnet”，但不要说链上完成完整属性签名验证。
- 不说“chain verifies the full attribute signature cryptography”。
- 不说“production-ready privacy system”。
- 不把模拟机构说成真实大学、真实实验室或真实 DAO。

## 最终提交前检查

- 视频时长小于 180 秒。
- README 中 0G Evidence 已替换真实地址和链接。
- X/Twitter 帖子中的 GitHub、Demo、0G Explorer 占位符已替换。
- 录屏中没有私钥、`.env`、助记词、钱包余额敏感信息。
- 对 `symbolic-field-v1` 的边界说明保留在视频中。
- 如果采用降级版，提交前需补录或剪入真实 0G Explorer 证据。
