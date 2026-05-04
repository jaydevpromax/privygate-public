# 工程与 Demo 蓝图

最后更新：2026-05-01

## 项目名

暂定：`PrivyGate`

## 产品定位

一个面向 Web3、AI Agent 和多机构协作场景的隐私属性授权层。用户或 Agent 可以证明自己满足多个机构共同定义的属性策略，而无需公开真实身份或完整属性集合。

## 最小可行 Demo

核心流程：

1. 多个机构注册并发布公钥。
2. 用户从不同机构获得属性私钥。
3. 服务方定义访问策略，例如：
   - `University:Student AND Lab:Researcher`
   - `DAO:Member AND Compliance:KYC-Passed`
   - `Agent:Registered AND Org:Approved`
4. 用户生成属性签名。
5. 验证方验证签名满足策略。
6. 链上记录机构状态、策略哈希和验证事件。

## 模块架构

| 模块 | 目录 | 说明 |
|---|---|---|
| 密码学核心 | `src/` | Setup、KeyGen、Sign、Verify |
| API 服务 | `app/` | FastAPI 或 Node API |
| 辅助合约 | `contracts/` | AuthorityRegistry、PolicyRegistry、VerificationLog |
| 实验脚本 | `experiments/` | 性能测试与图表 |
| 数据 | `data/` | 实验配置和输出 |
| 文档 | `docs/` | 论文、工程、比赛材料 |

## 推荐技术栈

- 算法原型：Python。
- pairing 库优先级：Charm-Crypto、petlib、py_ecc、或可控的模拟群实现。
- API：FastAPI。
- 前端：Vite + React。
- 合约：Solidity + Hardhat。
- 图表：Python matplotlib / pandas。

## 真实实现与模拟边界

必须真实实现：

- 算法核心流程。
- 签名验证逻辑。
- 性能测试脚本。
- 链上注册与事件记录。

允许模拟：

- 真实高校/机构账户后台。
- 大规模用户系统。
- 生产级 DID 钱包。
- 真实隐私计算硬件。

模拟部分必须在 README 和论文中写清楚，避免把工程演示说成生产系统。

## API 草案

- `POST /authorities/register`
- `POST /users/issue-attribute`
- `POST /policies/create`
- `POST /signatures/sign`
- `POST /signatures/verify`
- `GET /experiments/run`

## 演示页面

建议 4 个页面即可：

1. 机构面板：注册机构、发布属性。
2. 用户面板：领取属性、生成签名。
3. 验证方面板：创建策略、验证签名。
4. 审计面板：查看链上登记与验证记录。

## 第一阶段代码目标

先完成命令行闭环，再做 API 和前端：

```text
setup -> authority setup -> issue attributes -> sign -> verify -> benchmark
```

