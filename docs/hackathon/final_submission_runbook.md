# Final Submission Runbook

最后更新：2026-05-04

用途：在 0G APAC Hackathon 最终提交前，按固定顺序完成公开仓库、0G Chain 证据、0G Storage 审计包、Demo 视频、X 帖和 HackQuest 表单，避免最后一天手工漏项。

## 0. 当前前提

已完成：

- Python 原型、CLI Demo、静态 Web Demo。
- Solidity registry 合约、Hardhat 配置、部署脚本、事件记录脚本和本地合约测试。
- README、提交字段、X 草稿、视频脚本和分享图。
- 自检脚本：`scripts/hackathon_readiness_check.py`。
- 链接填充脚本：`scripts/update_submission_links.py`。
- 0G Chain 主网合约和示例事件证据。
- 0G Storage audit manifest 生成器和上传 helper。

仍待完成：

- GitHub 仓库已创建并推送，提交前还需确认是否公开可匿名访问。
- Demo 视频和 X 公开帖尚未发布。

## 1. 工具链准备

目标：让 `contracts/` 下的 Hardhat 工程可运行。

需要完成：

1. 确认 Node.js 发行版可用，使 `node` 和 `npm` 都可用。
2. 进入合约目录：

```powershell
cd contracts
npm install
npm test
```

验收：

- `npm test` 通过；当前已通过 6 个 Hardhat 合约测试。
- 不提交 `node_modules/`、`cache/`、`artifacts/` 或 `.env`。

## 2. GitHub 公开仓库

目标：让评委能直接访问代码、README、Demo 说明和媒体资产。

需要完成：

1. 在 GitHub 创建公开仓库。
2. 推送本地 `main` 分支。
3. 打开仓库页面，检查 README 图片、表格和链接显示正常。
4. 记录仓库 URL 到 `docs/hackathon/submission_links.template.json` 的 `github_url`。

验收：

- GitHub 页面可匿名访问。
- 最新 commit 包含 README、`src/`、`contracts/`、`app/web/`、`scripts/` 和 `docs/hackathon/`。

## 3. 0G Chain 部署

目标：获得真实 0G mainnet contract address 和 Explorer activity。

准备 `.env`：

```powershell
cd contracts
copy .env.example .env
```

填写：

```text
OG_RPC_URL=https://evmrpc.0g.ai
OG_PRIVATE_KEY=
OG_CHAIN_ID=16661
OG_EXPLORER_URL=https://chainscan.0g.ai
```

0G Galileo testnet 彩排可使用 `OG_GALILEO_RPC_URL=https://evmrpc-testnet.0g.ai`、`OG_GALILEO_CHAIN_ID=16602` 和 `OG_GALILEO_EXPLORER_URL=https://chainscan-galileo.0g.ai`。最终提交优先使用 0G mainnet。

部署：

```powershell
npm run check:og
npm run deploy:og
```

记录 Demo 事件：

```powershell
$env:PRIVYGATE_REGISTRY_ADDRESS='<deployed-address>'
npm run record:demo:og
```

至少记录这些证据：

- deployed contract address；
- deploy transaction；
- authority registration transaction；
- policy registration transaction；
- verification success transaction；
- revocation transaction；
- verification failure transaction。

把证据写入 `docs/hackathon/submission_links.template.json` 对应字段。

安全要求：

- 不把 `.env`、私钥、助记词、钱包截图提交到仓库。
- 视频录制时不要展示私钥、完整 `.env` 或钱包敏感信息。

## 4. 0G Storage Audit Manifest

目标：把 Agent 授权决策整理为可上传到 0G Storage 的脱敏审计包。

生成：

```powershell
$env:PYTHONPATH='src'
python .\scripts\generate_storage_audit_manifest.py
```

上传：

```powershell
cd storage
npm.cmd install
$env:OG_PRIVATE_KEY='0x...'
npm.cmd run upload:audit
```

上传后记录：

- 0G Storage root hash；
- 0G Storage transaction hash；
- 如有 StorageScan 或 indexer 查询链接，也记录链接。

回填规则：

- 把 root hash 和 transaction hash 写入 README、部署记录和 HackQuest 字段。
- 不要写回已上传的 manifest 文件本身，因为写回会改变文件内容，使 Storage root 不再对应该文件。

安全要求：

- 不把私钥写入文件。
- 不在视频中展示私钥、钱包导出或 shell 历史中的私钥。
- 只公开脱敏 audit manifest。

## 5. Demo 视频

目标：录制 180 秒以内的公开视频。

使用材料：

- 视频方案：`docs/hackathon/video_recording_plan.md`
- 静态 Demo：`app/web/index.html`
- CLI Demo：`scripts/privygate_cli.py`
- 分享图：`docs/hackathon/assets/privygate-share-card.png`
- 0G Explorer 页面
- 0G Storage audit manifest

录制后：

1. 上传视频到公开视频平台。
2. 确认匿名浏览器可打开。
3. 把视频 URL 写入 `demo_video_url`。

## 6. X 公开帖

目标：满足公开传播材料要求。

使用：

- 草稿：`docs/hackathon/x_post_draft.md`
- 附图：`docs/hackathon/assets/privygate-share-card.png`

发布前必须替换：

- GitHub URL；
- Demo video URL；
- 0G Explorer URL。

发布后把帖子 URL 写入 `x_post_url`。

## 7. 批量写入最终链接

先复制模板，保留模板不动：

```powershell
copy docs\hackathon\submission_links.template.json docs\hackathon\submission_links.local.json
```

填写 `submission_links.local.json` 后，先 dry-run：

```powershell
python .\scripts\update_submission_links.py --config docs\hackathon\submission_links.local.json
```

确认变更范围合理后执行：

```powershell
python .\scripts\update_submission_links.py --config docs\hackathon\submission_links.local.json --apply
```

脚本会先校验 URL 字段必须以 `http://` 或 `https://` 开头、不得包含空白字符，并校验 `contract_address` 为 `0x` 加 40 位十六进制字符的 EVM 地址格式。校验失败时不会写入文件。

脚本会更新：

- `README.md`
- `docs/hackathon/0g_deployment_notes.md`
- `docs/hackathon/hackquest_submission_fields.md`
- `docs/hackathon/x_post_draft.md`
- `docs/hackathon/video_recording_plan.md`
- `docs/hackathon/0g_submission_checklist.md`
- `docs/hackathon/submission_workplan.md`

## 8. 最终自检

执行：

```powershell
python .\scripts\hackathon_readiness_check.py --strict
```

验收：

- `FAIL=0`
- `BLOCKED=0`
- `WARN=0` 或只剩可解释的非提交风险项
- `git status --short` 为空

如果 `--strict` 仍然失败，不提交 HackQuest 表单，先修阻塞项。

## 9. HackQuest 表单

按 `docs/hackathon/hackquest_submission_fields.md` 填表。

提交前检查：

- GitHub URL 能匿名访问。
- Demo 视频少于 3 分钟。
- 0G contract address 和 Explorer link 是真实主网证据。
- 0G Storage audit manifest hash、root hash 和 transaction hash 已写入。
- X 帖公开可访问。
- README 中不再显示 `TBD` 或未替换链接占位符。
- 项目没有声称生产级密码学、链上完整验证属性签名或真实机构接入。

提交后记录：

- 提交时间。
- 提交确认页截图。
- HackQuest 项目页或提交编号。
- 最终 Git commit hash。
