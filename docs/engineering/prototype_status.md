# Python 原型实现状态

最后更新：2026-05-02

## 当前状态

已完成 PrivyGate 第一版 Python 核心闭环：

```text
setup -> authority_setup -> register_authority -> user_setup
-> issue_credential -> encode_policy -> sign -> verify -> revoke
```

当前后端为 `symbolic-field-v1`。它用符号化字段元素模拟双线性映射构造中的指数关系，用于验证多机构属性签名的工程流程、接口、策略、撤销和测试逻辑。该实现不是生产级密码实现，不能在论文或比赛材料中描述为已达到真实密码库安全级别。

## 已实现文件

| 文件 | 说明 |
|---|---|
| `src/privygate/core.py` | 核心算法原型 |
| `src/privygate/models.py` | 数据结构 |
| `src/privygate/hashing.py` | 哈希工具 |
| `src/privygate/registry.py` | 本地登记器 |
| `tests/test_core_flow.py` | 单元测试 |
| `scripts/run_core_demo.py` | 演示脚本 |
| `experiments/benchmark_core.py` | 基准脚本 |
| `contracts/contracts/PrivyGateRegistry.sol` | 链上辅助登记合约 |
| `contracts/hardhat.config.js` | Hardhat 3 合约工程配置 |
| `contracts/test/PrivyGateRegistry.test.js` | 合约本地测试 |
| `contracts/scripts/deploy.js` | 0G 部署脚本 |
| `contracts/scripts/record-demo-events.js` | 0G Demo 事件记录脚本 |
| `app/api/service.py` | API 服务层 |
| `app/api/main.py` | 可选 FastAPI 路由入口 |
| `tests/test_api_service.py` | API 服务层测试 |

## 测试结果

命令：

```powershell
$env:PYTHONPATH='src'
& 'C:\Users\86152\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
```

结果：

- Python 单元测试全部通过。
- Hardhat 合约测试 6 个用例全部通过。
- 覆盖成功签名验证、属性不足、撤销、混合用户凭证、错误机构公钥、消息篡改。
- API 服务层覆盖 seed demo、签名验证、属性不足和撤销。

## Demo 结果

命令：

```powershell
$env:PYTHONPATH='src'
& 'C:\Users\86152\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' '.\scripts\run_core_demo.py'
```

验证结果：

- Alice 同时拥有 `University:role:student` 和 `Lab:role:researcher`，满足策略并验证通过。
- Bob 只有学生属性，签名失败。
- Alice 的研究员属性被撤销后，原签名验证失败。

## 实验结果

命令：

```powershell
$env:PYTHONPATH='src'
& 'C:\Users\86152\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' '.\experiments\benchmark_core.py'
```

输出：

`experiments/results/core_benchmark.csv`

该结果文件为生成数据，不进入版本控制。

## 后续工程任务

1. 增加真实 pairing 后端可行性评估。（已完成文档，见 `pairing_backend_evaluation.md`）
2. 安装 FastAPI/uvicorn 后启动 HTTP 服务。
3. 获取 0G RPC、钱包和测试资金后部署 `PrivyGateRegistry`。
4. 将 Demo 流程接入 0G APAC 参赛叙事。

说明：第 2 项的可选路由入口已完成，但当前环境未安装 FastAPI/uvicorn。合约工程已经完成本地依赖安装、编译和测试，下一步阻塞点转为 0G RPC、钱包和测试资金。

## 后端迁移判断

当前建议继续保留 `symbolic-field-v1`，并将 `py_ecc` 作为第一真实 pairing 后端候选。论文和比赛材料必须明确：当前实现用于研究原型和流程验证，不是生产密码库。详细评估见：

`docs/engineering/pairing_backend_evaluation.md`
