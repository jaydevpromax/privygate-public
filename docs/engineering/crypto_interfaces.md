# 算法接口与实验指标文档

最后更新：2026-05-01

## 1. 设计原则

第一版接口服务两个目标：

1. 论文可写：函数名、输入输出、安全目标能直接对应论文第 4 章。
2. 工程可跑：可以快速实现命令行、API、实验脚本和 Demo。

第一版不追求生产级密码库，重点是结构正确、流程完整、实验可复现。若底层 pairing 库受限，可以先抽象群运算接口，但论文和 README 必须清楚标注实现边界。

## 2. 核心实体

| 实体 | 说明 |
|---|---|
| `SystemParams` | 系统公共参数 |
| `Authority` | 属性机构，拥有机构主密钥和公钥 |
| `User` | 用户或 Agent 操作者，拥有隐藏身份因子 |
| `Attribute` | 由某个机构签发的属性 |
| `Credential` | 属性私钥或属性凭证 |
| `Policy` | 访问策略 |
| `Signature` | 属性签名 |
| `VerificationResult` | 验证结果和审计信息 |

## 3. 数据结构草案

### 3.1 SystemParams

```python
@dataclass
class SystemParams:
    curve: str
    group_order: int
    g1: Any
    g2: Any
    gt: Any
    hash_to_scalar_id: str
    hash_to_group_id: str
    epoch: int
```

### 3.2 Authority

```python
@dataclass
class AuthoritySecretKey:
    authority_id: str
    alpha: int

@dataclass
class AuthorityPublicKey:
    authority_id: str
    public_key: Any
    public_key_hash: str
    registered_at_epoch: int
```

### 3.3 Attribute 与 Credential

```python
@dataclass(frozen=True)
class Attribute:
    authority_id: str
    name: str
    value: str

    @property
    def namespace(self) -> str:
        return f"{self.authority_id}:{self.name}:{self.value}"

@dataclass
class Credential:
    credential_id: str
    user_binding_commitment: str
    attribute: Attribute
    secret_component: Any
    issuer_public_key_hash: str
    epoch: int
    revoked: bool = False
```

### 3.4 Policy

```python
@dataclass
class Policy:
    policy_id: str
    expression: str
    required_attributes: list[Attribute]
    threshold: int
    policy_hash: str
```

第一版用阈值结构统一表示：

- AND：`threshold = n`
- OR：`threshold = 1`
- k-of-n：`threshold = k`

### 3.5 Signature

```python
@dataclass
class AttributeSignature:
    signature_id: str
    message_hash: str
    policy_hash: str
    epoch: int
    sigma_components: dict[str, Any]
    proof_commitments: dict[str, Any]
    challenge: int
```

## 4. 核心算法接口

### 4.1 Setup

```python
def setup(security_param: int = 128, epoch: int = 1) -> SystemParams:
    ...
```

输入：

- 安全参数。
- 当前 epoch。

输出：

- 系统公共参数。

论文对应：系统初始化算法。

### 4.2 AuthoritySetup

```python
def authority_setup(params: SystemParams, authority_id: str) -> tuple[AuthoritySecretKey, AuthorityPublicKey]:
    ...
```

输入：

- 系统公共参数。
- 机构标识。

输出：

- 机构主密钥。
- 机构公钥。

论文对应：机构初始化算法。

### 4.3 RegisterAuthority

```python
def register_authority(public_key: AuthorityPublicKey) -> str:
    ...
```

输入：

- 机构公钥。

输出：

- 链上交易哈希或本地登记 ID。

工程说明：

- 本地版写入 registry。
- 链上版调用 `AuthorityRegistry` 合约。

### 4.4 UserSetup

```python
def user_setup(user_label: str | None = None) -> tuple[int, str]:
    ...
```

输入：

- 可选用户标签，仅用于 Demo。

输出：

- 用户隐藏身份因子。
- 用户承诺。

安全作用：

- 绑定属性私钥，防止不同用户拼接属性合谋。

### 4.5 KeyGen / IssueCredential

```python
def issue_credential(
    params: SystemParams,
    authority_sk: AuthoritySecretKey,
    authority_pk: AuthorityPublicKey,
    user_commitment: str,
    attribute: Attribute,
    epoch: int,
) -> Credential:
    ...
```

输入：

- 系统参数。
- 机构密钥。
- 用户隐藏身份承诺。
- 属性。
- epoch。

输出：

- 属性凭证。

论文对应：属性密钥生成算法。

### 4.6 PolicyEncode

```python
def encode_policy(expression: str, attributes: list[Attribute], threshold: int) -> Policy:
    ...
```

输入：

- 策略表达式。
- 策略涉及的属性。
- 阈值。

输出：

- 可验证策略结构。

### 4.7 Sign

```python
def sign(
    params: SystemParams,
    user_secret: int,
    credentials: list[Credential],
    policy: Policy,
    message: bytes,
) -> AttributeSignature:
    ...
```

输入：

- 系统参数。
- 用户隐藏身份因子。
- 用户凭证集合。
- 访问策略。
- 待签名消息。

输出：

- 属性签名。

失败条件：

- 属性不足。
- 属性已撤销。
- 凭证 epoch 不匹配。
- 凭证绑定因子不一致。

### 4.8 Verify

```python
def verify(
    params: SystemParams,
    authority_pks: dict[str, AuthorityPublicKey],
    policy: Policy,
    message: bytes,
    signature: AttributeSignature,
    revocation_registry: set[str] | None = None,
) -> VerificationResult:
    ...
```

输入：

- 系统参数。
- 机构公钥集合。
- 策略。
- 消息。
- 属性签名。
- 撤销集合。

输出：

- 是否验证通过。
- 失败原因。
- 审计哈希。

### 4.9 RevokeCredential

```python
def revoke_credential(credential_id: str) -> str:
    ...
```

输入：

- 凭证 ID。

输出：

- 本地登记 ID 或链上交易哈希。

工程说明：

- 本地版写入撤销集合。
- 链上版调用合约更新撤销状态。

## 5. 合约接口草案

### 5.1 AuthorityRegistry

```solidity
function registerAuthority(bytes32 authorityId, bytes32 publicKeyHash) external;
function isAuthorityRegistered(bytes32 authorityId) external view returns (bool);
function getAuthorityKeyHash(bytes32 authorityId) external view returns (bytes32);
```

### 5.2 PolicyRegistry

```solidity
function registerPolicy(bytes32 policyId, bytes32 policyHash) external;
function getPolicyHash(bytes32 policyId) external view returns (bytes32);
```

### 5.3 RevocationRegistry

```solidity
function setRevoked(bytes32 credentialHash, bool revoked) external;
function isRevoked(bytes32 credentialHash) external view returns (bool);
```

### 5.4 VerificationLog

```solidity
event VerificationRecorded(bytes32 indexed policyId, bytes32 proofHash, bool result);

function recordVerification(bytes32 policyId, bytes32 proofHash, bool result) external;
```

## 6. API 接口草案

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/setup` | 初始化系统参数 |
| `POST` | `/authorities/register` | 注册属性机构 |
| `POST` | `/users/create` | 创建 Demo 用户 |
| `POST` | `/attributes/issue` | 签发属性凭证 |
| `POST` | `/policies/create` | 创建访问策略 |
| `POST` | `/signatures/sign` | 生成属性签名 |
| `POST` | `/signatures/verify` | 验证属性签名 |
| `POST` | `/credentials/revoke` | 撤销凭证 |
| `GET` | `/audit/{id}` | 查看审计记录 |

## 7. 实验指标

### 7.1 算法性能

| 指标 | 说明 |
|---|---|
| `setup_time_ms` | 系统初始化耗时 |
| `authority_setup_time_ms` | 单个机构初始化耗时 |
| `keygen_time_ms` | 属性凭证签发耗时 |
| `sign_time_ms` | 签名生成耗时 |
| `verify_time_ms` | 签名验证耗时 |
| `signature_size_bytes` | 签名序列化长度 |
| `credential_size_bytes` | 单个凭证序列化长度 |

### 7.2 链上辅助成本

| 指标 | 说明 |
|---|---|
| `authority_register_gas` | 机构注册 gas |
| `policy_register_gas` | 策略登记 gas |
| `revoke_gas` | 撤销状态更新 gas |
| `verification_log_gas` | 验证事件记录 gas |

## 8. 实验场景

| 场景 | 参数设置 | 观察指标 |
|---|---|---|
| 属性数量变化 | 5、10、20、40 | 签名时间、验证时间、签名长度 |
| 机构数量变化 | 2、4、8、16 | KeyGen、Sign、Verify |
| 策略复杂度变化 | AND、OR、k-of-n | 签名长度、验证时间 |
| 方案对比 | 普通签名、单机构 ABS、本文方案 | 开销与功能差异 |

## 9. 第一版测试用例

1. Alice 同时拥有 `University:student` 和 `Lab:researcher`，满足策略，验证通过。
2. Bob 只有 `University:student`，不满足策略，验证失败。
3. Alice 的 `Lab:researcher` 被撤销后，再次验证失败。
4. Alice 与 Bob 拼接属性，因用户绑定因子不同，验证失败。
5. 使用错误机构公钥验证，验证失败。
6. 消息被篡改，验证失败。

## 10. 后端边界

当前工程实现使用 `symbolic-field-v1` 研究后端，用字段元素模拟双线性映射构造中的指数关系。该后端用于验证系统流程、接口、策略、撤销和实验流水线，不是生产级密码实现。

真实 pairing 后端迁移计划见：

`docs/engineering/pairing_backend_evaluation.md`

