# Agent Coding Lifecycle Skill — MVP（v0.1 基礎流程 + v0.2 子命令）

> **狀態：MVP 已建立、待 Codex / Claude Code 實測**；追蹤：[Issue #6](https://github.com/appletiger0704/agent-coding-lifecycle/issues/6)。不代表 OpenSpec 或 ADR 已正式選型通過。

## MVP 範圍

一個 `agent-coding-lifecycle` 協調 Skill，根據 Repository 現況決定下一個動作：Issue → OpenSpec → ADR Gate → Coding + Tests → PR → Merge 後歸檔。

- **不取代**原生 OpenSpec Skills 或 GitHub。
- **不自動核准 ADR**；若是重大架構決策，只提出 Proposed，等待人工核准。
- **不自動合併／部署**；不安裝全套管理工具。
- **支援接續進行中的工作**，不要求每次從零建立 Issue。
- 細微修改可採輕量流程，不必硬建所有文件。

## v0.2：依需求呼叫子命令

主 Skill 維持單一入口：`skills/agent-coding-lifecycle/SKILL.md`。細節保留在 `skills/agent-coding-lifecycle/references/commands.md`，讓使用者只載入選取的命令。

| 功能 | Codex | Claude Code（安裝額外 wrapper 後） |
|---|---|---|
| 使用說明 | `$agent-coding-lifecycle help` | `/agent-coding-lifecycle:help` |
| 工作進度 | `$agent-coding-lifecycle status` | `/agent-coding-lifecycle:status` |
| GitHub Issue | `$agent-coding-lifecycle issue` | `/agent-coding-lifecycle:issue` |
| OpenSpec | `$agent-coding-lifecycle openspec` | `/agent-coding-lifecycle:openspec` |
| ADR | `$agent-coding-lifecycle adr` | `/agent-coding-lifecycle:adr` |
| Coding | `$agent-coding-lifecycle implement` | `/agent-coding-lifecycle:implement` |
| PR | `$agent-coding-lifecycle pr` | `/agent-coding-lifecycle:pr` |
| 完成 | `$agent-coding-lifecycle close` | `/agent-coding-lifecycle:close` |
| 自動接續 | `$agent-coding-lifecycle run` | `/agent-coding-lifecycle:run` |

原本的 Claude Code `/agent-coding-lifecycle <子命令>` 呼叫方式仍可使用，但冒號形式**不是單靠安裝 SKILL.md 就會出現**。

## 完整命名空間安裝

從本 Repo clone 的來源目錄執行以下指令，將主 Skill 與 Claude Code 的 9 個命令檔複製到產品專案：

```bash
bash scripts/install.sh /path/to/product-repo
```

預設會跳過已存在檔案。核對更新內容後，可加 `--force` 覆寫受管理檔案。

注意：`npx skills add` 僅安裝 Skill，不包含本 Repo `.claude/commands/` 的命令檔。若不需要冒號形式，沿用原本的 `npx skills add` 即可。

## 正常執行順序

首次使用：`help`（說明）→ `status`（只讀進度），之後選擇六階段：

1. `issue`：確認目標與驗收條件
2. `openspec`：整理提案／規格／設計／Tasks
3. `adr`：讀取相關 Accepted ADR，必要時提 Proposed 並由人員批准
4. `implement`：開發與測試
5. `pr`：提交 PR 與驗證證據，等待審查
6. `close`：確認合併後歸檔、更新追蹤

接續工作：`status` → `run`（僅下一個未完成階段）。`adr` 並非每次都建立新紀錄；如 ADR 影響設計，回到 `openspec` 修正後再實作。日常小修可略過不必要的 OpenSpec 或新 ADR。

## Skill 原始碼

[`skills/agent-coding-lifecycle/SKILL.md`](../skills/agent-coding-lifecycle/SKILL.md)

這是中央 Repository 的**單一維護來源**，不是每個產品 Repo 直接自動發現的路徑。

## 安裝到產品 Repository（手動、可重現）

在自己的工作環境中執行以下範例，請依實際路徑調整：

```bash
git clone https://github.com/appletiger0704/agent-coding-lifecycle.git
cd /path/to/your-product-repo
mkdir -p .agents/skills .claude/skills
cp -R /path/to/agent-coding-lifecycle/skills/agent-coding-lifecycle .agents/skills/
cp -R /path/to/agent-coding-lifecycle/skills/agent-coding-lifecycle .claude/skills/
```

- Codex：`.agents/skills/agent-coding-lifecycle/SKILL.md`
- Claude Code：`.claude/skills/agent-coding-lifecycle/SKILL.md`
- 建議將選定版本提交到產品 Repo，讓跨 Agent 協作使用相同規則。更新時明確同步並接受 code review。
- 若已在產品 Repo 安裝 OpenSpec，保留 OpenSpec 本身產生的 skills/commands；本 Skill 只負責協調。
- 若未安裝 OpenSpec，Skill 不能代替安裝與初始化。

## 典型呼叫（安裝完成後）

Codex：`$agent-coding-lifecycle 請從 Issue #123 開始，先確認目前階段與相關 ADR`

Claude Code：`/agent-coding-lifecycle 請接續 Issue #123，確認規格與測試狀態`

上述只是**預期用法**，仍須在實際 Codex / Claude Code 版本中確認能被載入。完成安裝但未出現時，請參考各 Agent 官方的 Skill discovery 說明。

## 手動試跑清單

**案例 A：既有模式下的小型功能**

- [ ] Agent 能讀取指定 Issue 並判斷已有工作，不重複開單。
- [ ] 不涉及重大選型時，不強制建立 ADR。
- [ ] 按 spec/tasks 或 Issue 驗收條件執行實作與測試。
- [ ] 在 PR 描述明列 Issue、Spec/ADR（可 N/A）、測試結果。

**案例 B：重大架構決策**

- [ ] Agent 先閱讀 Accepted ADR。
- [ ] 假設需要更換資料儲存、核心推論框架或認證模式，只建立 Proposed ADR。
- [ ] 未獲人工批准時暫停相關架構變更。
- [ ] 已核准後按決策實作，PR 可追溯到 ADR。

**案例 C：Agent 交接**

- [ ] Codex 開始後讓 Claude Code 接續（或反過來）。
- [ ] 第二個 Agent 能透過 GitHub / OpenSpec / ADR 恢復進度，而不是仰賴前次對話。
- [ ] 兩個 Agent 的下一步與禁止事項一致。

## 後續迭代，暫不實作

1. 整理試跑阻礙及 Skill 觸發問題。
2. 必要時再拆分 `adr-review`、`pr-review`。
3. 最後再評估 GitHub Actions / Rulesets、ADR Tools、Projects。
