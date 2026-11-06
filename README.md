# Agent Coding Lifecycle

> **Status: Proposal / Research** · 研究 Codex、Claude Code 與可追溯的軟體開發流程。**尚未宣告任何架構已核准。**

## MVP v0.1 — 單一 Orchestrator Skill（已建立，待實測）

- [Skill 原始碼：`skills/agent-coding-lifecycle/SKILL.md`](skills/agent-coding-lifecycle/SKILL.md)
- [MVP 安裝與手動驗收說明](docs/mvp.md)
- [Issue #6：MVP 試跑與後續迭代](https://github.com/appletiger0704/agent-coding-lifecycle/issues/6)

**第一階段僅提供一個 Workflow Skill**，協調 GitHub Issue → OpenSpec → ADR Gate → Coding / Tests → PR。Skill 已提交，但**尚未在使用者環境實際安裝或測試**；OpenSpec / ADR Tools / GitHub Actions 也尚未在產品專案中導入。決策需人工核准，合併／部署亦不能由 Agent 擅自執行。

## Skill 安裝方式（Codex / Claude Code）

> 需求：Node.js 22.20+、npm / npx。以下請在**要開發的產品 Repository 根目錄**執行；預設安裝於目前專案，不是全域安裝。

### 1. 推薦：使用 Skills CLI

先確認此 Repo 提供的 Skill：

```bash
npx skills add appletiger0704/agent-coding-lifecycle --list
```

同時安裝給 Codex 與 Claude Code：

```bash
npx skills add appletiger0704/agent-coding-lifecycle --skill agent-coding-lifecycle -a codex -a claude-code
```

安裝時確認選擇 **Project** scope；如需將檔案獨立複製到 Agent 目錄，可加 `--copy`。預期可由 `.agents/skills/`、`.claude/skills/` 存取該 Skill，具體形式可能是目錄或符號連結。

### 2. 驗證與更新

```bash
npx skills list
npx skills check
npx skills update agent-coding-lifecycle
```

也可以在安裝完成後，於 Codex 呼叫 `$agent-coding-lifecycle`，或在 Claude Code 呼叫 `/agent-coding-lifecycle`，確認 Skill 能被載入。**目前尚未在使用者的本機實測這些命令。**

### 3. 手動安裝（不使用 Skills CLI）

可依 [MVP 文件的手動複製步驟](docs/mvp.md#安裝到產品-repository手動可重現)，將 `skills/agent-coding-lifecycle/` 複製到產品 Repo 的 `.agents/skills/` 與 `.claude/skills/`。

> 此 Skill **只協調流程**，不會自動安裝 OpenSpec、建立 ADR Tools、合併 PR 或部署程式。正式使用前，請先檢視 [SKILL.md](skills/agent-coding-lifecycle/SKILL.md) 內容及所需權限。

CLI 參考：[vercel-labs/skills 安裝文件](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)。

## 目的

打造能在不同 AI Coding Agents 間交接的工程流程，從需求、規格、架構決策、實作、測試到審查都有版本控制與可回溯證據。此 Repository 是**共用方法、研究與模板的中央知識庫**，不是單一產品的程式碼 Repository。

## 最小可行架構（待驗證）

| 元件 | 角色 | 第一階段 |
|---|---|---|
| GitHub Issues / PRs | 需求、進度、審查與連結 | 採用 |
| OpenSpec | Proposal / Specs / Design / Tasks | 評估導入 |
| ADR（MADR 格式） | 重大架構決策的原因、限制、取捨 | 評估導入 |
| Documentation and ADRs Skill | 引導 Codex / Claude Code 管理文件及 ADR | 優先評估 |
| GitHub Projects | 視覺化追蹤 | 視需要啟用 |
| ADR Tools | ADR CLI 編號和 supersede | 暫緩 |
| GitHub Actions / Rulesets | 自動驗證、強制審核 | 第二階段 |

## 建議流程

```text
GitHub Issue
  → OpenSpec (Proposal / Specs / Design / Tasks)
  → 檢查既有 Accepted ADR；重大架構變更提出 Proposed ADR
  → 人工核准（若需要 ADR）
  → Codex / Claude Code 實作
  → Pull Request + Tests + Review
  → Merge + OpenSpec Archive + Issue / Projects 更新
```

**原則**：AI 可以起草重大架構決策，**不可以自行批准**；一般 bugfix、既有模式內的小修改不需另建 ADR。

## 文件導覽

- [整體開發生命週期與治理邊界](docs/architecture/lifecycle.md)
- [OpenSpec 研究與導入問題](docs/research/openspec.md)
- [ADR Skills / MADR / ADR Tools 比較](docs/research/adr-skills.md)
- [GitHub 整合與分階段導入](docs/research/github-integration.md)
- [ADR 目錄說明](docs/adr/README.md)
- [MADR 簡化模板](templates/adr-template.md)
- [Codex AGENTS.md 範本](templates/AGENTS.md)
- [Claude Code CLAUDE.md 範本](templates/CLAUDE.md)

## 待辦 Issues

- [#1 總體規劃](https://github.com/appletiger0704/agent-coding-lifecycle/issues/1)
- [#2 OpenSpec](https://github.com/appletiger0704/agent-coding-lifecycle/issues/2)
- [#3 ADR Skills / MADR / ADR Tools](https://github.com/appletiger0704/agent-coding-lifecycle/issues/3)
- [#4 Codex / Claude Code 共用規範](https://github.com/appletiger0704/agent-coding-lifecycle/issues/4)
- [#5 GitHub Projects / Actions](https://github.com/appletiger0704/agent-coding-lifecycle/issues/5)

## 中央與各專案的權責

- **本 Repo**：共用工作流程、研究結果、範本、可複用的 Skills 政策與示例。
- **每個實際專案 Repo**：其 `openspec/`、真正的 `docs/adr/`、程式碼、CI 設定及 PR 歷程。
- 不把本 Repo 的研究提案誤用成所有產品都已接受的技術決策。

## 參考資源

- [OpenSpec](https://github.com/Fission-AI/OpenSpec)
- [Documentation and ADRs Skill](https://github.com/addyosmani/agent-skills/tree/main/skills/documentation-and-adrs)
- [MADR](https://github.com/adr/madr)
- [ADR Tools](https://github.com/npryce/adr-tools)

最後更新：2026-11-06
