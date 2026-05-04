# 0G APAC Hackathon 提交材料补齐计划

最后更新：2026-05-02

## 目标

在 2026-05-16 23:59 UTC+8 前完成一个有效且有竞争力的 0G APAC Hackathon 提交。当前策略不是把论文原型包装成概念项目，而是把 PrivyGate 定位为：

> Privacy-preserving multi-authority attribute authorization for autonomous agents on 0G.

核心目标分两层：

1. 有效提交：必须有公开 GitHub、可运行代码、0G mainnet 合约地址、Explorer 链上活动、3 分钟内 Demo 视频、README、X 公开帖子。
2. 冲奖提交：在有效提交基础上，突出 Agent 授权场景、隐私授权价值、可审计链上证据和可复用 SDK/API 形态。

## 官方要求核查

来源：`https://www.hackquest.io/hackathons/0G-APAC-Hackathon`

当前已核查到的硬性要求：

| 要求 | 状态 | 对 PrivyGate 的处理 |
|---|---|---|
| Online hackathon | 已确认 | 远程提交，优先准备视频和公开材料 |
| Submission deadline: 2026-05-16 23:59 UTC+8 | 已确认 | 内部冻结时间设为 2026-05-15 23:00 UTC+8 |
| GitHub repository required | 已推送，待确认公开访问 | 本地 `main` 已跟踪 `origin/main`，提交前需做匿名访问检查 |
| 0G mainnet contract address required | 已完成 | `0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| Explorer link with on-chain activity required | 已完成 | 已提交机构登记、策略登记、验证事件和撤销事件 |
| README required | 已完成 | 根目录 `README.md` 已是英文参赛版 |
| Demo video under 3 minutes required | 脚本完成 | 录制本地 Demo + Explorer 证据 |
| X public post required | 待完成 | 提交前发布项目视频或截图帖 |
| Project must integrate at least one 0G component | 已完成 | 0G Chain 主网合约和事件审计 |

## 当前资产

| 资产 | 文件 | 可用程度 |
|---|---|---|
| Python 核心算法原型 | `src/privygate/` | 可运行，已测试 |
| 单元测试 | `tests/` | Python 测试通过 |
| Demo 脚本 | `scripts/run_core_demo.py` | 可展示 Alice 成功、Bob 失败、撤销后失败 |
| API 服务层 | `app/api/` | 业务层可测试，HTTP 服务依赖 FastAPI 环境 |
| Solidity 合约 | `contracts/contracts/PrivyGateRegistry.sol` | 已通过本地 Hardhat 编译和 6 个合约测试 |
| 架构说明 | `docs/hackathon/architecture.md` | 可复用到 README 和视频 |
| 0G 部署说明 | `docs/hackathon/0g_deployment_notes.md` | 已填主网地址和交易 |
| 英文 README 草稿 | `docs/hackathon/project_readme_draft.md` | 需改成公开仓库首页 |
| Demo 视频脚本 | `docs/hackathon/demo_script.md` | 需按真实部署证据更新 |
| 论文材料 | `deliverables/论文初稿.docx` | 可作为项目研究深度背书，不作为黑客松主提交材料 |

## 奖金最大化判断

优先冲两个方向：

1. Track 1: Agentic Infrastructure & OpenClaw Lab  
   包装重点：AI Agent 调用敏感工具前，先用 PrivyGate 验证多机构属性签名，避免暴露真实身份或完整属性。

2. Track 5: Privacy & Sovereign Infrastructure  
   包装重点：多机构、去中心化机构密钥、用户承诺绑定、撤销检查、链上审计，不依赖单一身份授权中心。

不推荐把项目主叙事放在“纯密码学算法”或“纯论文系统”上。评委更容易理解的表达是：

- PrivyGate is a privacy authorization gateway for autonomous agents.
- It lets agents prove policy satisfaction without exposing raw identity data.
- 0G Chain stores tamper-evident authorization state and audit events.

## 时间计划

### 2026-05-01 至 2026-05-02：有效提交基础

必须完成：

1. 创建 GitHub 仓库并推送本地提交。（已完成推送，提交前还需确认公开访问）
2. 把公开 README 改成英文参赛版。（已完成）
3. 初始化 Hardhat 工程。（已完成）
4. 为 `PrivyGateRegistry.sol` 添加本地合约测试。（已完成，6 个测试通过）
5. 准备 `.env.example`，列出 `OG_RPC_URL`、`OG_PRIVATE_KEY`、`OG_CHAIN_ID`。（已完成）

验收标准：

- GitHub 仓库能公开访问。
- `README.md` 让评委 60 秒内看懂项目、0G 集成和运行方式。
- 合约至少能在本地 Hardhat 网络通过测试。

### 2026-05-03 至 2026-05-05：0G 链上证据

必须完成：

1. 获取 0G Chain RPC、Chain ID、测试资金和 Explorer 地址。
2. 部署 `PrivyGateRegistry.sol`。
3. 记录合约地址和部署交易。
4. 执行至少 4 类链上操作：
   - registerAuthority
   - registerPolicy
   - recordVerification(success)
   - setRevoked
5. 把交易哈希和 Explorer 链接写入 `0g_deployment_notes.md`。

验收标准：

- README 中有真实 0G mainnet contract address。
- README 中有 Explorer 链接，能看到链上活动。
- Demo 视频能展示链上证据。

### 2026-05-06 至 2026-05-08：Agent 授权 Demo

必须完成：

1. 增加命令行演示包装 `scripts/privygate_cli.py`。
2. 输出评委易懂的步骤：
   - seed demo authorities
   - create users
   - issue credentials
   - create policy
   - sign tool call
   - verify
   - revoke credential
   - verify again
3. 给 Demo 增加一个 Agent 场景名称，例如 `ResearchAgent` 调用 `private-dataset.read`。
4. 输出 JSON 或清晰终端日志，方便录屏。

验收标准：

- 评委不读论文也能看懂：Alice 的 Agent 满足策略，可以调用工具；Bob 的 Agent 不满足策略，被拒绝；撤销后 Alice 的旧签名失效。

### 2026-05-09 至 2026-05-11：提交材料包装

必须完成：

1. 生成公开 README 最终版。
2. 更新 `docs/hackathon/demo_script.md`，加入真实合约地址和 Explorer 链接。
3. 准备 30 词以内项目描述。
4. 准备 1 段项目摘要。
5. 准备架构图截图或 Mermaid 渲染图。
6. 准备 X 帖文案。

推荐文案：

```text
PrivyGate is a privacy authorization gateway for autonomous agents on 0G. It lets users prove multi-institution attributes for tool access without exposing raw identity data.
```

### 2026-05-12 至 2026-05-14：视频录制与回归

必须完成：

1. 录制 3 分钟以内 Demo 视频。
2. 重新运行测试。
3. 重新运行 Demo。
4. 检查 README 中所有链接。
5. 检查提交表单所需字段是否完整。

视频结构：

| 时间 | 内容 |
|---|---|
| 0-20 秒 | 问题：Agent 需要私有授权，但不能暴露完整身份 |
| 20-50 秒 | 架构：多机构属性签名 + 0G Chain 审计 |
| 50-105 秒 | Alice 成功调用受保护工具 |
| 105-135 秒 | Bob 属性不足被拒绝 |
| 135-160 秒 | 撤销后旧签名失效 |
| 160-175 秒 | 展示 0G Explorer 链接和交易 |
| 175-180 秒 | 总结：privacy authorization gateway for agents |

### 2026-05-15：内部冻结

必须完成：

1. 最终提交表单预填。
2. README、视频、GitHub、Explorer、X 帖链接互相可达。
3. 保留一份提交截图和所有链接快照。
4. 不再做大规模功能改动，只修提交阻塞问题。

### 2026-05-16：提交日

只做：

1. 最终检查。
2. 发布 X 帖。
3. 提交 HackQuest 表单。
4. 记录提交编号、提交时间和最终链接。

## 证据清单

| 证据 | 文件或位置 | 状态 |
|---|---|---|
| GitHub repo URL | `README.md` / HackQuest 表单 | [GitHub repo](https://github.com/jaydevpromax/privygate-public) |
| 0G contract address | `docs/hackathon/0g_deployment_notes.md` | READY |
| Explorer deploy tx | `docs/hackathon/0g_deployment_notes.md` | READY |
| Authority registration tx | `docs/hackathon/0g_deployment_notes.md` | READY |
| Policy registration tx | `docs/hackathon/0g_deployment_notes.md` | READY |
| Verification event tx | `docs/hackathon/0g_deployment_notes.md` | READY |
| Revocation tx | `docs/hackathon/0g_deployment_notes.md` | READY |
| Demo video URL | HackQuest 表单 / README | TBD |
| X post URL | HackQuest 表单 | TBD |
| Test command output | README / local terminal | READY |

## 降级方案

### 如果 0G Chain 部署受阻

处理顺序：

1. 优先解决 RPC、钱包、资金、Chain ID 和 Explorer 问题。
2. 若合约部署失败，先部署最小合约，只保留机构登记和事件记录。
3. 若 Solidity 测试通过但 0G 部署不可用，补充 0G Storage 或官方文档允许的其他 0G 组件。
4. 若仍无法获得真实 0G 证据，提交胜率会显著下降，不建议把该版本作为主力提交。

### 如果 Demo 视频时间不足

保留以下最小片段：

1. 项目一句话定位。
2. 本地 Demo：Alice 成功，Bob 失败，撤销后失败。
3. 0G Explorer：合约地址和事件交易。

删掉：

- 论文背景长解释。
- 密码学公式细节。
- 过长代码 walkthrough。

### 如果公开 README 太长

保留以下结构：

1. One-line pitch。
2. Problem。
3. Solution。
4. Why 0G。
5. Demo flow。
6. Run locally。
7. 0G evidence。
8. Limitations。

## 下一步执行队列

1. 生成干净公开导出包并确认 GitHub 仓库可匿名访问。
2. 录制 3 分钟以内 Demo 视频。
3. 发布 X 公开帖。
4. 填入 GitHub、Demo 视频和 X 帖最终链接。
5. 运行 `scripts/hackathon_readiness_check.py --strict`，确认所有提交占位符已替换且没有阻塞项。
6. 提交 HackQuest 表单并保存提交截图。
