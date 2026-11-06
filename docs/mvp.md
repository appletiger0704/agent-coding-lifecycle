# MVP 指南 — Agent Coding Lifecycle

> 版本：v0.2（單一 Skill + 子命令）。**命令檔已在 GitHub；Codex / Claude Code 實機驗證待完成。**  
> 追蹤：[Issue #6](https://github.com/appletiger0704/agent-coding-lifecycle/issues/6) / [Issue #7](https://github.com/appletiger0704/agent-coding-lifecycle/issues/7)

## 目標

透過一個 `agent-coding-lifecycle` Skill，協調 GitHub Issue → OpenSpec → ADR（必要時）→ Implementation / Tests → PR → Merge 後歸檔。

重點是讓 Codex / Claude Code **從文件恢復開發進度**，不靠對話歷史。這是協調 Skill，不會自行安裝 OpenSpec、操作未授權的遠端資源或取代人員的架構審核。

## 安裝

### 使用 Skills CLI（主 Skill）

於產品 Repo 根目錄：

```bash
npx skills add appletiger0704/agent-coding-lifecycle --skill agent-coding-lifecycle -a codex -a claude-code
```

### 完整安裝（含 Claude Code 的冒號指令）

```bash
git clone https://github.com/appletiger0704/agent-coding-lifecycle.git
bash agent-coding-lifecycle/scripts/install.sh /path/to/your-product-repo
```

腳本複製 Skill 與其 `references/` 到：

- `.agents/skills/agent-coding-lifecycle/`（Codex）
- `.claude/skills/agent-coding-lifecycle/`（Claude Code）
- `.claude/commands/agent-coding-lifecycle/`（Claude Code 的 9 個冒號命令）

腳本預設保留既有檔案，確認更新內容後才使用 `--force`。直接用 Skills CLI 安裝不會順帶提供命名空間命令。

## 指令與正確順序

| 階段 | 子命令 | 判斷與輸出 |
|---|---|---|
| 使用前 | `help` | 查詢有哪些命令，不掃描專案 |
| 接續前 | `status` | 唯讀查詢完成度與下一步 |
| 1 | `issue` | 需求與驗收條件明確 |
| 2 | `openspec` | 規格、初步設計、工作拆分 |
| 3 | `adr` | 檢查 Accepted ADR；重大新決策須 Proposed → 人工核准 |
| 4 | `implement` | 依已核准規格實作與測試 |
| 5 | `pr` | 準備提交審核與測試紀錄 |
| 6 | `close` | **確認 PR 合併**後才歸檔／結案 |
| 快捷 | `run` | 從現況選**下一個未完成階段**，不是全流程自動執行 |

新需求：`issue → openspec → adr gate → implement → pr → close`。  
接續工作：`status → run`。  
小型 bugfix：可走簡化 Issue → Implement → PR → Close，不必強制建立 OpenSpec 變更或新 ADR。

若 ADR 核准結果改變技術設計，先回到 OpenSpec 修正 Design / Tasks。沒有重要新決策時，`adr` 只讀既有紀錄，不建立新 ADR。

## v0.2 的 Routing Gate 與實際操作

此版本的主 Skill 先判斷當前命令，再決定哪些工具、文件需要讀取：

- `help`：不進行任何 Repo/CLI 掃描。
- `status`：只讀調查工作進度。
- `run`：從現況選擇**下一個未完成階段**；不自動執行所有階段。
- **Routine fix**：不強制建立 OpenSpec／ADR。
- **無 OpenSpec**：自動流程跳過；若使用者明確要求 `openspec`，則說明缺少安裝/初始化。
- **無 ADR 目錄**：不查不存在的檔案；但真正重大新架構決策仍須提出 Proposed ADR。
- **ADR 核准修改設計**：先回 OpenSpec 更新 Design / Tasks，再實作。

### 唯讀 Preflight

完整安裝之後，於**產品 Repo** 根目錄執行：

```bash
bash .agents/skills/agent-coding-lifecycle/scripts/preflight.sh .
```

掃描 Git 分支、變更檔案數、最近 commit、`gh` / `openspec` 可用性、OpenSpec changes，以及可能 Accepted 的 ADR；**不會查遠端 Issue/PR、修改 Repo 或自動讀取全部 ADR**。候選 ADR 需再確認狀態與實際關聯性。

### CLI 與 OpenSpec 的區別

- GitHub CLI（可用且有權限）：`gh issue view 123 --json number,title,state,url`
- OpenSpec CLI（已安裝並初始化）：`openspec status --change <change-name> --json`
- Claude Code 的 `/opsx:propose`、`/opsx:apply`、`/opsx:archive` 是 **Agent 聊天指令**，不是 shell 命令；Codex 的具體 Skill 名稱以安裝結果為準。

### 離線 Smoke Test

中央 Repo 內可執行：

```bash
bash -n skills/agent-coding-lifecycle/scripts/preflight.sh
bash -n scripts/test-preflight.sh
bash scripts/test-preflight.sh
```

**已測：** 無配置的暫存 Git Repo、存在 OpenSpec change、Accepted 與 Superseded ADR 篩選、無 Repo 時正確報錯。  
**未測：** 真實 Codex／Claude Code 命令是否可被發現、是否遵循路由、是否完成跨 Agent Issue→PR 交接。

此改善由 [Issue #8](https://github.com/appletiger0704/agent-coding-lifecycle/issues/8) 追蹤。

## 指令範例

```text
# Codex
$agent-coding-lifecycle help
$agent-coding-lifecycle status
$agent-coding-lifecycle run 請接續 Issue #123

# Claude Code（完整安裝後）
/agent-coding-lifecycle:help
/agent-coding-lifecycle:openspec issue-123
/agent-coding-lifecycle:adr 針對資料庫選型產生 Proposed ADR
/agent-coding-lifecycle:run 請接續 Issue #123
```

## 手動驗收（尚待實測）

**案例 A：一般功能**

- [ ] Agent 可從 Issue 找到需求及既有 OpenSpec，避免重複產生。
- [ ] 若沒有重大架構變更，不建立新 ADR。
- [ ] 實作與測試結果可回連 PR。

**案例 B：重要架構變更**

- [ ] Agent 先讀相關 Accepted ADR。
- [ ] 提出 Proposed ADR，未批准前不繼續受影響的實作。
- [ ] 核准後若影響設計，先回 OpenSpec 更新，再實作。

**案例 C：跨 Agent 接續**

- [ ] Codex 和 Claude Code 均可載入對應指令（尚待本機驗證）。
- [ ] 第二個 Agent 能從 Repo 文件判斷下一個未完成階段。
- [ ] 不會自行核准 ADR、合併或部署。

## 後續（本期不做）

GitHub Projects 自動化、ADR Tools、CI / Rulesets、獨立 Review Skills、MCP Server、部署自動化。先完成真實使用測試，再依 Issue 逐項改善。

相關檔案：[`SKILL.md`](../skills/agent-coding-lifecycle/SKILL.md) · [命令行為](../skills/agent-coding-lifecycle/references/commands.md) · [README](../README.md)
