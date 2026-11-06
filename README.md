# Agent Coding Lifecycle

> **MVP v0.2：Skill 與指令入口已建立，待 Codex / Claude Code 實機驗證。** 本 Repo 是跨專案的工程流程、研究與模板來源；不是特定產品 Repo，也不代表任何重大架構決策已核准。

讓 Codex 與 Claude Code 依據版本化的 GitHub Issue、OpenSpec、ADR、測試與 PR 記錄接續工作，不必依賴對話歷史。

## 快速開始

### 方式 A：只安裝主 Skill（Codex + Claude Code）

在**目標產品 Repository** 根目錄執行（需具備 Node.js / npx）：

```bash
npx skills add appletiger0704/agent-coding-lifecycle --skill agent-coding-lifecycle -a codex -a claude-code
```

這個方式安裝主 Skill；**不包含** Claude Code 的冒號命名空間命令檔。

### 方式 B：完整安裝（推薦給需要冒號指令的人）

```bash
git clone https://github.com/appletiger0704/agent-coding-lifecycle.git
bash agent-coding-lifecycle/scripts/install.sh /path/to/your-product-repo
```

透過 [安裝腳本](scripts/install.sh) 複製：

- Codex：`.agents/skills/agent-coding-lifecycle/`
- Claude Code：`.claude/skills/agent-coding-lifecycle/`
- Claude Code 命名空間命令：`.claude/commands/agent-coding-lifecycle/`
- 唯讀 Preflight：各 Skill 目錄下的 `scripts/preflight.sh`

腳本預設**不覆寫**已存在檔案；核對差異後可在最後加 `--force`。適用 Bash 環境（macOS、Linux、WSL 或 Git Bash）；安裝後可重新啟動 Agent 讓指令被辨識。以上仍待使用者的實際 Agent 版本驗證。

## 指令總覽

| 指令 | 說明 | 何時使用 |
|---|---|---|
| `help` | 查看功能與標準流程 | 第一次使用 |
| `status` | **唯讀**查看目前進度與阻礙 | 接手或恢復工作 |
| `issue` | 讀取、整理或建立 Issue | 明確定義需求 |
| `openspec` | 使用專案既有的 OpenSpec 流程 | 撰寫規格／設計 |
| `adr` | 檢查已核准決策，必要時提出 ADR | 重大架構選擇前 |
| `implement` | 依規格實作並測試 | 規格與必要決策確認後 |
| `pr` | 檢查變更並準備／建立 PR | 程式碼與測試完成後 |
| `close` | 確認 PR 已合併，才歸檔並結案 | 合併後 |
| `run` | 自動選出**下一個未完成階段** | 想接續目前工作 |

### 建議執行順序

```text
第一次使用：
  help → status

新功能（標準流程）：
  issue → openspec → adr（檢查關卡）→ implement → pr → close
                    │
                    └─ 若需新增重大決策：Proposed ADR → 人工核准
                       若決策改變設計：回 openspec 更新 Design / Tasks

接續既有任務：
  status → run（一次只處理下一個未完成階段）

小型 bugfix：
  issue / 既有任務 → implement → pr → close
```

**重要區別：** 每次涉及架構的開發應讀取相關 *Accepted ADR*；但**不是每次都要新增 ADR**。`help`、`status`、`run` 是輔助入口，不是必須依序執行的另外三個開發階段。 `run` 不表示已授權自動合併、部署或跳過人工核准。

### 呼叫範例

**Codex**

```text
$agent-coding-lifecycle help
$agent-coding-lifecycle status
$agent-coding-lifecycle openspec issue-123
$agent-coding-lifecycle run 請接續 Issue #123
```

**Claude Code（完整安裝後）**

```text
/agent-coding-lifecycle:help
/agent-coding-lifecycle:status
/agent-coding-lifecycle:openspec issue-123
/agent-coding-lifecycle:adr 評估是否需要使用 Kafka
/agent-coding-lifecycle:run 請接續 Issue #123
```

只安裝主 Skill 時，也可嘗試 `/agent-coding-lifecycle help` 等參數形式；**冒號命令需要額外的 `.claude/commands/` 檔案**。

## Routing Gate：何時執行、何時跳過？

Skill 在進入各階段之前先判斷**使用者要求、既有進度及專案配置**，避免每次完整掃描或建立無用文件。

| 情況 | MVP 行為 |
|---|---|
| `help` | 直接顯示指令，**不讀 Repo、不呼叫外部工具** |
| `status` | 唯讀檢查 Git、OpenSpec / ADR 位置，必要時查 Issue / PR |
| `run` | 僅執行**下一個未完成階段**，不是一口氣跑到合併 |
| 例行 bugfix、遵循現有設計 | 可略過新 OpenSpec 變更與新 ADR |
| 沒有 `openspec/` 或未安裝 OpenSpec | 自動流程跳過 OpenSpec；若明確指定 `openspec`，回報安裝前提 |
| 沒有 ADR 目錄 | 跳過不存在的既有紀錄；如涉及重大**新**架構選擇，仍須提出 Proposed ADR |
| 與既有 Accepted ADR 衝突 | 停止受影響的實作，提出取代方案並等待人工核准 |

判定需要規格的典型情況：**新增／改變使用者可觀察行為、公開 API 或資料契約、需多步任務且有驗收條件的新功能**。判定需要新 ADR 的情況：**長期架構、資安邊界、資料契約、核心依賴、跨元件模式或難以逆轉的技術決策**。

### 可執行的唯讀環境檢查

完成**完整安裝**後，在產品 Repo 根目錄執行：

```bash
bash .agents/skills/agent-coding-lifecycle/scripts/preflight.sh .
```

這會輸出分支、工作區變動數、最近 5 筆 commit、`gh` / `openspec` CLI 是否存在、OpenSpec change 目錄，以及可能為 Accepted 的 ADR 檔案。它**不會**連線查詢 GitHub Issue / PR，也**不會修改文件**；ADR 清單僅供候選篩選，仍須閱讀確認適用性。

需要查 GitHub 遠端狀態時，應另外確認權限後執行 `gh issue view <number> --json number,title,state,url` 或 `gh pr view <number> --json number,state,mergedAt,url`，或使用已授權的 GitHub 工具。

在中央 Repo 執行離線 smoke test：

```bash
bash -n skills/agent-coding-lifecycle/scripts/preflight.sh
bash -n scripts/test-preflight.sh
bash scripts/test-preflight.sh
```

目前離線煙霧測試已通過（無 OpenSpec/ADR、存在 Accepted 與 Superseded ADR、缺少 Repo）；**Codex / Claude Code 實機載入與端到端工作流仍待測試**。

## MVP 範圍與限制

此專案目前只有**一個 Orchestrator Skill**，根據子命令按需載入規則，**不會替代** GitHub、OpenSpec 或 ADR 的專門工具。

- 已提供：[`SKILL.md`](skills/agent-coding-lifecycle/SKILL.md)、[各命令規則](skills/agent-coding-lifecycle/references/commands.md)、[9 個 Claude Code 命令](.claude/commands/agent-coding-lifecycle)、[安裝腳本](scripts/install.sh)。
- 未涵蓋：自動安裝 OpenSpec、ADR Tools、GitHub Projects、強制性的 CI / Branch Rules、MCP、部署自動化。
- 安全邊界：**重大 ADR 需人員核准**；不得自行核准、合併或部署；沒有執行的測試不得宣稱通過。
- 技術現況：GitHub 文件、唯讀檢查腳本與命令檔已提交，離線 smoke test 已通過；**仍需在本機 Codex / Claude Code 驗證指令與完整流程**。

詳細說明及手動測試案例請見 [MVP 指南](docs/mvp.md)。

## 文件與規劃

| 文件 | 內容 |
|---|---|
| [生命週期設計](docs/architecture/lifecycle.md) | 各階段職責、決策關卡 |
| [OpenSpec 研究](docs/research/openspec.md) | Spec、Design、Tasks 與 Issue 的分工 |
| [ADR 工具比較](docs/research/adr-skills.md) | ADR Skills、MADR、ADR Tools |
| [GitHub 整合](docs/research/github-integration.md) | Projects、Actions、PR 規劃 |
| [ADR 模板](templates/adr-template.md) | 擬定決策用的 Proposed ADR |
| [Codex 規範範本](templates/AGENTS.md) | 可複製到產品 Repo |
| [Claude Code 規範範本](templates/CLAUDE.md) | 可複製到產品 Repo |

中央 Repo 保存**共用方法、模板和研究**；每個產品 Repo 保留**自己的程式碼、OpenSpec、實際 ADR 與 PR**。

進度：[總體提案 #1](https://github.com/appletiger0704/agent-coding-lifecycle/issues/1) · [MVP #6](https://github.com/appletiger0704/agent-coding-lifecycle/issues/6) · [子命令擴充 #7](https://github.com/appletiger0704/agent-coding-lifecycle/issues/7) · [條件式流程與 Preflight #8](https://github.com/appletiger0704/agent-coding-lifecycle/issues/8)

更新日期：2026-11-06
