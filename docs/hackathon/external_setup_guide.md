# External Setup Guide

最后更新：2026-05-02

用途：完成 GitHub 推送、npm/Hardhat、0G 部署和最终公开提交前，用这份清单修复本机外部依赖。

## 当前判断

本地代码、论文、PPT、Demo、合约测试和公开材料已经通过预检。当前真正阻塞黑客松最终提交的是 0G 主网部署证据：

- GitHub private 主仓库已可推送，最终公开仓库仍需匿名访问检查。
- Node/npm/npx 已可用，Hardhat 依赖已安装，合约本地测试已通过。
- `contracts/.env` 尚未创建，0G 钱包私钥尚未填写。
- 还需要确认部署钱包有足够 0G 主网 Gas。

## 1. 推送 private 主仓库最新提交

在 CMD 中执行：

```cmd
cd /d "<PROJECT_ROOT>"
git push -u origin main
```

推送成功后，本地 `main` 会追踪 `origin/main`。

## 2. 安装正常 Node.js LTS

最推荐安装官方 Node.js LTS。安装完成后，重新打开 CMD 或 PowerShell，检查：

```cmd
node --version
npm --version
npx --version
```

期望：

- 三条命令都能输出版本号。
- `where node` 不应只指向 Codex app 内部路径。

如果仍然指向 Codex app 内部路径，重启终端或调整系统 PATH，让 Node.js LTS 安装目录排在前面。

## 3. 安装合约依赖并测试

```cmd
cd /d "<PROJECT_ROOT>\contracts"
npm install
npm test
```

验收：

- `npm test` 通过。
- 不提交 `node_modules/`、`cache/`、`artifacts/`、`.env`。

## 4. 准备 0G 部署环境

```cmd
cd /d "<PROJECT_ROOT>\contracts"
copy .env.example .env
```

填写：

```text
OG_RPC_URL=https://evmrpc.0g.ai
OG_PRIVATE_KEY=
OG_CHAIN_ID=16661
OG_EXPLORER_URL=https://chainscan.0g.ai
```

当前官方默认值：

| 网络 | Chain ID | RPC | Explorer |
|---|---:|---|---|
| 0G Mainnet | `16661` | `https://evmrpc.0g.ai` | `https://chainscan.0g.ai` |
| 0G Galileo Testnet | `16602` | `https://evmrpc-testnet.0g.ai` | `https://chainscan-galileo.0g.ai` |

黑客松最终证据优先使用 0G Mainnet；Galileo 只用于部署彩排。

安全要求：

- `.env` 不要提交。
- 不要截图展示私钥。
- 视频录制时不要打开 `.env`。

## 5. 运行外部依赖检查

回到项目根目录：

```cmd
cd /d "<PROJECT_ROOT>"
python .\scripts\external_dependency_check.py
```

目标：

- `git origin` 为 `https://github.com/jaydevpromax/privygate.git`
- `git upstream` 为 `origin/main`
- `node`、`npm`、`npx` 全部 OK
- `contracts/node_modules` installed
- `contracts/.env` required deployment keys are present
- `hardhat tests` OK

## 6. 部署 0G 合约

```cmd
cd /d "<PROJECT_ROOT>\contracts"
npm run check:og
npm run deploy:og
```

部署后记录：

- contract address
- deploy transaction
- Explorer contract link

如果主网 Gas 还没准备好，可以先用 Galileo 彩排：

```cmd
npm run check:og:galileo
npm run deploy:og:galileo
```

## 7. 记录 Demo 事件

```cmd
set PRIVYGATE_REGISTRY_ADDRESS=<deployed-address>
npm run record:demo:og
```

至少保存：

- authority registration tx
- policy registration tx
- verification success tx
- revocation tx
- verification failure tx

## 8. 回填最终链接

```cmd
cd /d "<PROJECT_ROOT>"
copy docs\hackathon\submission_links.template.json docs\hackathon\submission_links.local.json
```

填好 `submission_links.local.json` 后：

```cmd
python .\scripts\update_submission_links.py --config docs\hackathon\submission_links.local.json
python .\scripts\update_submission_links.py --config docs\hackathon\submission_links.local.json --apply
python .\scripts\hackathon_readiness_check.py --strict
```

## 9. 公开参赛仓库

不要直接公开 private 主仓库历史。

生成干净公开包：

```cmd
python .\scripts\prepare_public_release.py --force
```

把生成的 `data/generated/public_release_*` 推送到新的 public 仓库，或推到 orphan public branch。
