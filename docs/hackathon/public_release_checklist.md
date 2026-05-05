# Public Release Checklist

最后更新：2026-05-04

用途：创建公开 GitHub 仓库、发布 Demo 视频、发布 X 帖和填写 HackQuest 表单前，按本清单逐项检查，避免泄露本地文件、私钥或提交未替换占位符。

## 1. 公开仓库应包含

这些内容可以公开，且应该出现在 GitHub 仓库中：

| 路径 | 是否公开 | 说明 |
|---|---|---|
| `README.md` | 是 | 评委入口，必须包含项目定位、运行方式、0G 证据和密码学边界。 |
| `src/privygate/` | 是 | Python 核心算法原型。 |
| `tests/` | 是 | Python 单元测试，证明核心流程可运行。 |
| `scripts/privygate_cli.py` | 是 | 录屏和评委复现实验的最短入口。 |
| `scripts/generate_storage_audit_manifest.py` | 是 | 生成 0G Storage 脱敏审计包。 |
| `scripts/hackathon_readiness_check.py` | 是 | 提交前自检。 |
| `scripts/update_submission_links.py` | 是 | 最终链接批量替换。 |
| `app/web/` | 是 | 免构建静态 Demo。 |
| `contracts/` | 是 | Solidity 登记合约、Hardhat 配置、测试和部署脚本。 |
| `storage/` | 是 | 可选 0G Storage 上传 helper，不包含私钥。 |
| `docs/hackathon/` | 是 | 提交清单、架构说明、视频计划、X 草稿和媒体资产。 |
| `docs/engineering/` | 可公开 | 说明系统设计和当前边界。 |
| `docs/thesis/` | 可选择 | 如果担心论文查重或学校流程，公开仓库可不主动展示论文草稿入口。 |

## 2. 公开仓库不应包含

这些内容不得提交或不得在公开视频中展示：

| 路径或内容 | 原因 |
|---|---|
| `contracts/.env` | 可能包含 RPC、私钥或部署配置。 |
| 任意私钥、助记词、钱包导出文件 | 严重资产风险。 |
| `node_modules/` | 依赖缓存，体积大且不应提交。 |
| `contracts/artifacts/`、`contracts/cache/` | Hardhat 生成物，不需要进入源码仓库。 |
| `storage/node_modules/` | 0G Storage 上传 helper 的依赖缓存，不提交。 |
| `docs/hackathon/submission_links.local.json` | 本地链接配置，可能包含未公开信息。 |
| 学校、老师、本人隐私信息 | 公开仓库和黑客松材料中只保留必要项目身份。 |
| 未确认可公开的论文完整 DOCX | 可能影响学校提交、查重或后续修改流程。 |

## 3. GitHub 上线顺序

强烈建议：不要直接把当前 private 主仓库改成 Public。当前仓库历史中包含论文、答辩和内部项目控制材料。公开参赛版应使用干净导出包、新公开仓库或 orphan public branch。

生成干净公开导出包：

```powershell
python .\scripts\prepare_public_release.py --force
```

默认输出目录：

```text
data/generated/public_release/
```

如果该目录已经存在，脚本会自动生成新的非破坏式目录，例如 `data/generated/public_release_1/`。

公开导出包会包含代码、Demo、合约、工程说明和黑客松材料，并排除 `deliverables/`、`docs/thesis/`、`docs/project/`、`references/` 和本地生成物。

如果 npm/Hardhat 或 0G 部署还没完成，先按 `docs/hackathon/external_setup_guide.md` 修复外部依赖。

1. 确认本地工作区干净：

```powershell
git status --short
```

2. 创建 GitHub public repository。
3. 添加远程仓库并推送：

```powershell
git remote add origin <GITHUB_REPO_URL>
git push -u origin main
```

4. 用匿名浏览器窗口检查：

- README 图片能显示；
- `app/web/`、`src/`、`contracts/`、`docs/hackathon/` 能访问；
- README 中没有 `TODO`、`TBD`、`<...>` 占位符；
- README 没有声称生产级密码系统；
- README 没有泄露本地绝对路径、私钥或钱包信息。

本地也要运行自检脚本。脚本会扫描公开材料中的本机绝对路径、明显私钥/token 模式、`.env`、本地链接配置和依赖生成目录：

```powershell
python .\scripts\hackathon_readiness_check.py
```

## 4. Demo 视频上线顺序

优先录制顺序：

1. 打开 README，说明项目一句话定位。
2. 运行 CLI Demo，展示 Alice 通过、Bob 失败、撤销后失败。
3. 打开 `app/web/index.html`，展示可视化 Demo。
4. 打开 0G Explorer，展示 contract address 和关键交易。
5. 打开 0G Storage audit manifest，展示 manifest hash 和 upload helper。
6. 最后回到 README 的 0G Evidence 区域，说明所有链接已写入。

公开视频验收：

- 时长小于 3 分钟；
- 不展示 `.env`、私钥、钱包助记词或完整 RPC 密钥；
- 不说“生产级密码安全”；
- 明确说当前是 research prototype / hackathon MVP；
- 匿名浏览器窗口能打开视频链接。

## 5. X 帖发布顺序

1. 使用 `docs/hackathon/x_post_draft.md` 的英文短版或带标签版。
2. 附图使用 `docs/hackathon/assets/privygate-share-card.png`。
3. 发布前替换：

| 占位 | 替换为 |
|---|---|
| `TODO_GITHUB_REPO_URL` | 公开 GitHub 仓库 |
| `TODO_DEMO_VIDEO_URL` | 公开视频 |
| `TODO_0G_EXPLORER_CONTRACT_URL` | 0G Explorer 合约页 |

4. 发布后把 X 帖链接写入 `docs/hackathon/submission_links.local.json`。

## 6. 最终链接填充

复制模板：

```powershell
copy docs\hackathon\submission_links.template.json docs\hackathon\submission_links.local.json
```

填好链接后先 dry-run：

```powershell
python .\scripts\update_submission_links.py --config docs\hackathon\submission_links.local.json
```

确认无误后应用：

```powershell
python .\scripts\update_submission_links.py --config docs\hackathon\submission_links.local.json --apply
```

如果 URL 或合约地址格式不正确，脚本会直接报错并停止，不会写入公开材料。

然后运行严格检查：

```powershell
python .\scripts\hackathon_readiness_check.py --strict
```

只有 `FAIL=0` 且 `BLOCKED=0` 时才提交 HackQuest 表单。

## 7. 提交后归档

提交完成后在本地记录：

| 项目 | 记录 |
|---|---|
| HackQuest 提交时间 | 2026-05-05 |
| HackQuest 项目页或提交编号 | https://www.hackquest.io/projects/PrivyGate |
| GitHub commit hash | See latest public repository `main` branch |
| Demo video URL | https://youtu.be/P52F4F0H-QI |
| X post URL | https://x.com/Jaydevpromax/status/2051522134015685119?s=20 |
| 0G contract address | 0x1b55C901A69fE53a70F0011579d3576684FAAdc0 |
| 0G deploy transaction | https://chainscan.0g.ai/tx/0xa28e74c61c34c8652a07845d5fca6f443d816487ca85e7576c44839576259251 |
| 0G Storage manifest hash | 待填写 |
| 0G Storage root/tx | root `0xe8cc7ce846e8952caa41f491041dbd424d89dd762f55b9e7482f36295d252e8f`，tx `0xdc192a3713bb96baad3880c1dce0c1a089d3b9b02c6783d1d4afa990960ac66f` |

建议把提交确认截图保存在本地非公开目录，不提交到仓库。
