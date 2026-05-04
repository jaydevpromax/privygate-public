# PrivyGate Demo Script

最后更新：2026-05-01

目标：录制 0G APAC Hackathon 3 分钟以内 Demo 视频。

## 视频结构

### 0:00-0:20 问题

画面：标题页或终端/架构图。

旁白：

> AI agents and Web3 apps need authorization that is more expressive than wallet ownership, but users should not reveal their full identity or all credentials. PrivyGate solves this with decentralized multi-authority attribute signatures.

中文要点：

- 钱包地址不能表达复杂资格。
- 暴露完整身份资料会损害隐私。
- 多机构属性授权更符合真实场景。

### 0:20-0:45 架构

画面：展示系统架构。

要点：

- University、Lab、DAO 作为独立属性机构。
- 用户拿到多个属性凭证。
- PrivyGate Gateway 验证属性签名。
- 0G Chain 记录机构、公钥哈希、策略哈希、撤销状态和验证事件。

### 0:45-1:25 成功授权

画面：运行 Demo 或前端成功页。

命令：

```powershell
$env:PYTHONPATH='src'
python .\scripts\privygate_cli.py
```

展示：

- Alice 拥有 `University:role:student`。
- Alice 拥有 `Lab:role:researcher`。
- 策略为 `University:role:student AND Lab:role:researcher`。
- 终端输出 `Result: ACCEPT`。

旁白：

> Alice proves that she satisfies the policy, but the verifier does not need to see her real identity.

### 1:25-1:55 失败授权

画面：同一 Demo 输出中的 Bob 失败。

展示：

- Bob 只有 student 属性。
- Bob 无法生成满足策略的签名。
- 输出 `insufficient non-revoked credentials for policy`。

旁白：

> Bob cannot combine missing attributes or bypass the policy.

### 1:55-2:20 撤销

画面：展示撤销后的验证失败。

展示：

- 撤销 Alice 的 Lab researcher 凭证。
- 原签名再次验证失败。
- 输出 `credential revoked`。

旁白：

> Revocation is checked through the registry, so stale credentials stop working.

### 2:20-2:45 0G 集成

画面：展示合约代码、部署地址或 Explorer 页面。

要点：

- `PrivyGateRegistry` 负责 authority、policy、revocation、verification events。
- 0G Chain 提供可审计登记层。

正式提交前需替换：

- 合约地址。
- 0G Explorer 链接。
- 真实交易哈希。

### 2:45-3:00 总结

旁白：

> PrivyGate is a privacy authorization layer for autonomous agents: multi-authority, policy-based, revocable, and auditable on 0G.

## 拍摄前检查

- 单元测试通过。
- CLI Demo 命令输出稳定。
- README 写明 symbolic prototype 边界。
- 0G 合约地址和 Explorer 链接已替换。
- 视频控制在 180 秒以内。
