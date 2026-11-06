# Agent Coding Lifecycle

> **Status: Proposal / Research** · 研究 Codex、Claude Code 與可追溯的軟體開發流程。**尚未宣告任何架構已核准。**

## MVP — 單一 Orchestrator Skill（已建立，待實測）

- [Skill 原始碼：`skills/agent-coding-lifecycle/SKILL.md`](skills/agent-coding-lifecycle/SKILL.md)
- [MVP 安裝與手動驗收說明](docs/mvp.md)
- [Issue #6：MVP 試跑](https://github.com/appletiger0704/agent-coding-lifecycle/issues/6) · [Issue #7：子命令擴充](https://github.com/appletiger0704/agent-coding-lifecycle/issues/7)

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

## 指令式工作流（MVP v0.2）

這仍是**一個 Skill**；以子命令路由到需要的功能，不會每次強迫讀取所有 OpenSpec / ADR 文件。主 Skill 請見 [`SKILL.md`](skills/agent-coding-lifecycle/SKILL.md)，各命令細節見 [`references/commands.md`](skills/agent-coding-lifecycle/references/commands.md)。

| 子命令 | 作用 |
|---|---|
| `help` | 顯示 Skill 目標、命令與建議流程 |
| `status` | 只讀目前工作階段與阻礙 |
| `issue` | 整理 GitHub Issue |
| `openspec` | 呼叫專案已安裝的 OpenSpec |
| `adr` | 檢查 / 提出架構決策（人工核准） |
| `implement` | 實作與測試 |
| `pr` | 審查並準備 PR |
| `close` | 合併後歸檔並更新追蹤狀態 |
| `run` | 判斷下一個尚未完成的階段 |

### 建議執行順序（從新需求開始）

**不需要每次都執行 9 個指令。** `help` 是使用說明、`status` 是只讀進度盤點，`run` 是「繼續下一個未完成階段」的快捷入口；真正的開發階段是以下六步：

| 順序 | 指令 | 完成條件 |
|---|---|---|
| 1 | `issue` | 已有清楚的需求、範圍與驗收條件（可沿用既有 Issue） |
| 2 | `openspec` | 有足以評估架構的 Proposal / Specs / 初步 Design / Tasks（依變更規模調整） |
| 3 | `adr` | 檢查相關 Accepted ADR；如需重大新決策，先提出 Proposed、等待人工核准 |
| 4 | `implement` | 依核准設計實作並執行適當測試 |
| 5 | `pr` | 提交變更與測試證據，接受審查 |
| 6 | `close` | **確認 PR 已合併**，才歸檔 OpenSpec 並更新 Issue / Project |

- **先看有什麼：** `help`（不用讀專案）→ `status`（只讀）→ 選上述六步的下一步。
- **想省操作：** `status` → `run`。每次 `run` 只選下一個未完成階段；不是無條件自動執行到合併或部署。
- **ADR 無重大新決策：** 檢查完成就繼續，**不用建立 ADR 文件**。
- **ADR 改變既有設計：** 先回到 `openspec` 更新 Design / Tasks，再進入 `implement`。
- **小型 bugfix：** 可以採 Issue → Implement → PR 的精簡路徑，不強制新增 OpenSpec／ADR。

OpenSpec 的底層操作由已安裝的 OpenSpec Skills 負責，通常可對應 `explore`（可選）、`propose`、`apply`、`archive`；本 Skill 不重造它們的指令或自動跳過人工審核。

**Codex** 使用 Skill 名稱加參數，例如：

```text
$agent-coding-lifecycle help
$agent-coding-lifecycle openspec issue-123
$agent-coding-lifecycle adr 評估是否需要採用 Kafka
```

**Claude Code** 可使用參數形式 `/agent-coding-lifecycle help`，或安裝 **額外命名空間命令**後使用：

```text
/agent-coding-lifecycle:help
/agent-coding-lifecycle:status
/agent-coding-lifecycle:openspec issue-123
/agent-coding-lifecycle:adr 評估是否需要採用 Kafka
```

> **重要：** `npx skills add` 僅安裝主 Skill，**不會自動安裝**本 Repo 的 `.claude/commands/`。若要使用冒號形式，請採下方完整安裝方式。

### 完整安裝（含 Claude Code 冒號命令）

在工作機器執行，將 `<product-repo>` 換成要使用 Skill 的專案路徑：

```bash
git clone https://github.com/appletiger0704/agent-coding-lifecycle.git
bash agent-coding-lifecycle/scripts/install.sh /path/to/product-repo
```

此安裝腳本會**複製**主 Skill 到 `.agents/skills/` 與 `.claude/skills/`，並將 9 個 Claude Code 命名空間命令安裝於 `.claude/commands/agent-coding-lifecycle/`。遇到已存在的檔案預設跳過；更新時可先檢查差異，再用 `--force` 覆寫這些受管理檔案。

請確認目標專案的變更後再提交 Git。腳本不會安裝 OpenSpec、ADR Tools，亦不會建立 GitHub Issues/PR。**Claude Code / Codex 的實際呼叫尚待使用者環境驗證。**

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
- [#6 MVP Orchestrator Skill](https://github.com/appletiger0704/agent-coding-lifecycle/issues/6)
- [#7 子命令擴充](https://github.com/appletiger0704/agent-coding-lifecycle/issues/7)

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
