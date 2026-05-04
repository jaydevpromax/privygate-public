# 黑客松与奖金策略

最后更新：2026-05-01

## 总策略

用同一个技术内核，包装成不同比赛可理解的项目：

- 对 AI x Web3 比赛：强调 Agent 权限、Agent ID、私有记忆访问授权。
- 对隐私/安全比赛：强调匿名认证、多机构属性证明、抗合谋。
- 对基础设施比赛：强调可复用 SDK、策略验证 API、链上登记合约。
- 对应用型比赛：强调高校、DAO、企业协作或 API 准入场景。

## 近期优先比赛

### 1. 0G APAC Hackathon

状态：优先冲刺。

已核查信息：

- 模式：Online。
- 奖池：150,000 USD。
- 截止：2026-05-16 23:59 UTC+8。
- 适配方向：AI x Web3、autonomous agents、privacy、sovereign infrastructure。
- 必要材料：项目名、简介、GitHub、0G 集成证明、3 分钟内 Demo 视频、README、公开 X 帖。
- 必要集成：至少一个 0G 组件，例如 0G Chain、0G Storage、0G Compute、Agent ID 或隐私/安全执行特性。

官方来源：

- https://www.hackquest.io/hackathons/0G-APAC-Hackathon

推荐包装：

> PrivyGate: privacy-preserving multi-authority attribute authorization for autonomous agents on 0G.

优先 track：

- Track 1: Agentic Infrastructure & OpenClaw Lab。
- Track 5: Privacy & Sovereign Infrastructure。

### 2. ETHGlobal Open Agents

状态：只适合作为快速试投或观察，不作为主战场。

已核查信息：

- 提交截止：2026-05-03 12:00 EDT。
- 奖项包括 0G $15,000、Uniswap Foundation $5,000、Gensyn $5,000、ENS $5,000、KeeperHub $5,000。
- 截止时间非常近，除非已有账号和基础代码，否则不建议把它作为主投入。

官方来源：

- https://ethglobal.com/events/openagents/info/start
- https://ethglobal.com/events/openagents/prizes

### 3. Agents Assemble Healthcare AI

状态：短期复投目标。

已核查信息：

- 截止：2026-05-11 23:00 EDT。
- 主题：Healthcare AI，要求在 Prompt Opinion 平台上以 MCP Server 或 A2A Agent 形式集成。
- 奖项：1st $7,500、2nd $5,000、3rd $2,500、10 个 $1,000 Honorable Mentions。
- 强制要求：必须发布到 Prompt Opinion Marketplace，可被平台发现和调用；必须使用合成或去标识化数据，不能包含真实 PHI。

官方来源：

- https://agents-assemble.devpost.com/rules

推荐包装：

> PrivyGate Health: privacy-preserving multi-institution authorization for healthcare agents.

### 4. Google Cloud Rapid Agent Hackathon

状态：5 月下旬到 6 月主力复投目标。

已核查信息：

- 时间：2026-05-05 到 2026-06-11。
- 模式：Online。
- 奖池：60,000 USD。
- 要求：使用 Gemini 和 Google Cloud Agent Builder，并通过 MCP 集成至少一个合作伙伴能力。
- 提交材料：Hosted Project、公开开源仓库、约 3 分钟 Demo 视频、Devpost 表单。

官方来源：

- https://rapid-agent.devpost.com/

推荐包装：

> PrivyGate MCP: a privacy authorization gateway that lets agents call tools only when multi-authority attributes satisfy policy.

### 5. ETHOnline 2026

状态：中期复投目标。

已核查信息：

- ETHGlobal 事件页显示 ETHOnline 2026 为 2026-09-04 到 2026-09-16 的 Async Hackathon。

官方来源：

- https://ethglobal.com/events

## 奖金最大化原则

1. 优先选择奖金池大、主题匹配、线上、允许原型继续开发的比赛。
2. 每次提交尽量覆盖多个 bounty，但不要为了 bounty 牺牲主线完整性。
3. 参赛材料模块化：README、架构图、Demo 视频、部署说明可复用。
4. 强调真实集成证据：合约地址、Explorer 链接、存储交易、API 调用记录。
5. 不把项目描述成单纯论文算法，而描述成“隐私授权基础设施”。

## 0G 提交清单

- 项目名称。
- 30 词以内一句话描述。
- 3 分钟以内 Demo 视频。
- 公开 GitHub 仓库。
- 架构图。
- 0G 集成说明。
- 合约地址或 Explorer 链接。
- 本地运行步骤。
- 测试账户或演示数据。
- X 公共帖子链接。

## 近期行动

1. 先完成 0G 版项目叙事和 README。
2. 做最小链上集成，确保不是概念提交。
3. 把算法 Demo 和 Agent 授权场景连起来。
4. 录制一次完整用户流程。
