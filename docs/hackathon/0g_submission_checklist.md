# 0G APAC Hackathon 提交清单

最后更新：2026-05-04

官方页面：https://www.hackquest.io/hackathons/0G-APAC-Hackathon

## 关键信息

- 模式：Online。
- 截止：2026-05-16 23:59 UTC+8。
- 总奖池：150,000 USD。
- 奖项：1st $45,000、2nd $35,000、3rd $20,000、10 个 $3,700 Excellence Awards、10 个 $1,300 Community Awards。
- 项目必须实际集成至少一个 0G 组件，否则可能无效。

## 推荐提交定位

项目名：`PrivyGate`

一句话描述：

> Privacy-preserving multi-authority attribute authorization for autonomous agents on 0G.

目标赛道：

1. Track 1: Agentic Infrastructure & OpenClaw Lab。
2. Track 5: Privacy & Sovereign Infrastructure。

## 必须提交材料

| 状态 | 材料 | 说明 |
|---|---|---|
| DRAFT | 项目名 | PrivyGate |
| DRAFT | 30 词内一句话描述 | 已写入 `project_readme_draft.md` |
| DRAFT | 项目摘要 | 已写入 `project_readme_draft.md`，部署后需补 0G 证据 |
| READY | GitHub 仓库 | 公开或对评委可见，必须有实质提交 |
| DONE | 0G mainnet contract address | `0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| DONE | 0G Explorer link | `https://chainscan.0g.ai/address/0x1b55C901A69fE53a70F0011579d3576684FAAdc0` |
| DONE | 0G 集成证明 | 0G Chain 合约和 6 笔主网事件已完成；0G Storage audit manifest 已生成 |
| DONE | 0G Storage audit manifest | root `0xe8cc7ce846e8952caa41f491041dbd424d89dd762f55b9e7482f36295d252e8f`，tx `0xdc192a3713bb96baad3880c1dce0c1a089d3b9b02c6783d1d4afa990960ac66f` |
| DRAFT | 3 分钟内 Demo 视频 | 脚本已写入 `demo_script.md`，录制方案已写入 `video_recording_plan.md`，仍需录制 |
| READY | README | 英文公开版已合并到根目录 `README.md`，部署后需补 0G 证据 |
| DRAFT | X 公开帖子 | 草稿已写入 `x_post_draft.md`，发布前需替换 GitHub、Demo 和 0G Explorer 链接 |

## 推荐 0G 集成路径

第一优先级：0G Chain

- 部署 `AuthorityRegistry` 合约。
- 记录机构公钥哈希、策略哈希、撤销状态、验证事件。
- 提供 Explorer 链接作为集成证明。

第二优先级：0G Storage

- 生成脱敏 Agent 授权审计 manifest。
- 上传 manifest 后将 root hash / tx hash 写入 README。

第三优先级：Agent ID / Privacy

- 将 Agent 绑定到属性策略。
- 用属性签名决定 Agent 是否能调用受保护工具。

## Demo 视频结构

总时长控制在 180 秒以内：

1. 0-20 秒：问题与一句话定位。
2. 20-50 秒：系统架构，说明多机构属性签名和 0G 组件位置。
3. 50-110 秒：演示成功授权流程。
4. 110-145 秒：演示属性不足或撤销后的失败流程。
5. 145-170 秒：展示 0G Explorer / Storage / Chain 集成证据。
6. 170-180 秒：总结价值和后续计划。

## 最小可赢版本

如果时间紧，必须优先完成：

1. 可运行算法闭环。
2. 0G Chain 合约部署和 Explorer 链接。
3. 一个 Agent 工具调用授权 Demo。
4. README + 架构图 + 3 分钟视频。

## 禁止承诺

- 不说已经生产可用。
- 不说链上完成完整属性签名验证。
- 不说支持所有属性策略类型。
- 不把模拟机构接入描述成真实机构接入。
