# Pairing 后端评估与迁移方案

最后更新：2026-05-01

## 结论

当前最优策略：

1. 短期继续保留 `symbolic-field-v1` 作为论文接口、Demo、API 和实验流水线后端。
2. 中期优先评估 `py_ecc` 作为真实 pairing 后端候选。
3. 如果学校或指导老师更认可密码学教学/研究工具，再评估 Charm-Crypto，但不要把它作为 Windows 本地短期交付的唯一依赖。
4. 比赛提交和论文实现章节必须明确标注当前后端边界，避免把符号化原型描述成生产级密码实现。

## 当前本地环境

已检查：

| 依赖 | 当前状态 |
|---|---|
| `py_ecc` | 未安装 |
| `fastapi` | 未安装 |
| `uvicorn` | 未安装 |
| `pydantic` | 已安装 |
| Node/NPM | 当前命令不可用或无权限 |

因此当前环境不适合立即引入需要联网安装或编译的密码学库。先完成可测、可演示、可写论文的抽象层是更稳的路线。

## 候选方案对比

| 方案 | 优点 | 风险 | 推荐度 |
|---|---|---|---|
| `symbolic-field-v1` | 无外部依赖，稳定可测，能支撑接口、Demo、实验流水线 | 不是真实 pairing 实现，不能作为安全实现宣称 | 当前保留 |
| `py_ecc` | Python 生态，Ethereum 相关，支持 BN128/BLS12-381 基础运算，Windows 安装风险相对较低 | API 偏底层，需自己封装群元素序列化、哈希到群和 pairing 检查；性能不一定理想 | 第一候选 |
| Charm-Crypto | 学术 ABS/ABE 原型常用，`PairingGroup` 抽象适合论文算法 | Windows 安装和编译风险较高，环境可复现性可能差 | 第二候选 |
| `petlib` / `bplib` | 有椭圆曲线/双线性相关能力 | 原生依赖多，Windows 风险高，维护和安装不确定 | 不作为短期主线 |
| 自己实现 pairing | 理论可控 | 风险极高，容易引入错误，不适合毕业和比赛周期 | 不推荐 |

## 推荐迁移路径

### 阶段 1：保持当前后端，完成产品闭环

目标：

- API、合约、Demo、实验、论文接口全部稳定。
- 继续用当前 10 个单元测试保护行为。

状态：进行中，核心闭环已完成。

### 阶段 2：抽象后端接口

新增接口建议：

```python
class PairingBackend(Protocol):
    name: str
    group_order: int

    def random_scalar(self) -> int: ...
    def hash_to_scalar(self, *parts: object) -> int: ...
    def scalar_mul(self, base: object, scalar: int) -> object: ...
    def pair(self, left: object, right: object) -> object: ...
    def serialize(self, value: object) -> str: ...
```

当前 `symbolic-field-v1` 实现这个接口，未来 `py_ecc` 也实现同一接口。上层 `setup`、`authority_setup`、`issue_credential`、`sign`、`verify` 不直接依赖具体库。

### 阶段 3：验证 `py_ecc`

最低验证项：

1. 能在当前机器或 WSL 中安装。
2. 能完成 BN128 或 BLS12-381 基础群运算。
3. 能完成 pairing 等式验证。
4. 能序列化公钥、凭证、签名组件。
5. 能跑通当前 10 个测试，允许测试阈值耗时变慢。

如果 `py_ecc` 成功：

- 增加 `py-ecc-v1` 后端。
- 保留 `symbolic-field-v1` 作为快速测试后端。
- 论文实验分两类：流程实验使用 symbolic，密码运算实验使用 py_ecc。

如果 `py_ecc` 失败：

- 保持 symbolic 后端。
- 在论文中写明工程原型验证算法流程，真实密码库适配作为后续工作。
- 比赛材料继续强调“research prototype”，避免安全过度承诺。

## 对论文的表述建议

可以写：

> 本文实现的原型系统采用模块化后端设计。为保证实验可复现性，第一版工程实现使用符号化有限域后端模拟双线性映射构造中的指数关系，用于验证多机构属性签名的系统流程、策略验证、撤销机制和性能变化趋势。该后端不作为生产密码库使用。系统保留真实 pairing 后端适配接口，后续可接入 py_ecc 或 Charm-Crypto 完成真实群运算验证。

不要写：

> 本系统已经实现生产级安全的双线性映射属性签名库。

不要写：

> 当前性能结果等价于真实 pairing 密码库的性能。

## 对黑客松的表述建议

可以写：

> PrivyGate currently uses a symbolic-field research backend to demonstrate the multi-authority attribute-signature workflow. The architecture is designed so the backend can be replaced by a real pairing library while preserving the API, registry, and agent authorization flow.

不要写：

> Production-ready cryptographic authorization.

## 对实验的影响

当前 `experiments/benchmark_core.py` 结果只能说明：

- 随机构数量、属性数量和阈值变化，系统流程开销如何变化。
- 签名组件数量和序列化长度如何随策略规模变化。
- API、撤销、验证日志链路是否可用。

不能说明：

- 真实 pairing 计算耗时。
- 真实群元素序列化大小。
- 真实密码学安全强度。

正式论文中应把实验分为：

1. 原型流程实验。
2. 理论复杂度分析。
3. 如能接入真实库，再增加真实 pairing 后端性能实验。

## 资料来源

- py_ecc project page: https://github.com/ethereum/py_ecc
- Charm-Crypto project page: https://github.com/JHUISI/charm
- Charm-Crypto documentation: https://jhuisi.github.io/charm/

