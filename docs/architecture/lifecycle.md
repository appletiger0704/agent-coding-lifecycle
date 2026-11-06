# Agent Coding Lifecycle — 流程與治理（Proposal）

> 狀態：Proposed（尚未核准）。關聯 Issue：[總體規劃 #1](../../issues/1)。

## 1. 目標

讓 Codex / Claude Code 在不同回合、不同開發者或不同模型間，都能依據版本化文件繼續開發，而非依靠對話記憶。

## 2. 各元件的資料責任

| 問題 | 單一主要來源 | 輔助連結 |
|---|---|---|
| 為何需要／何時做 | GitHub Issue | Project、PR |
| 功能應有何行為 | OpenSpec specs | 測試 |
| 此次如何拆解實作 | OpenSpec proposal / design / tasks | Issue |
| 為何做出長期架構選擇 | ADR | OpenSpec Design、PR |
| 實際程式變更與審核 | Git Commit / PR | 測試、Issue |
| 執行狀態與排程 | GitHub Projects | Issue、PR |

## 3. 建議流程

1. **Intake — Issue**：描述問題、範圍、驗收標準、優先級。建立對應工作項目。
2. **Specification — OpenSpec**：整理 proposal/specs/design/tasks；每項 task 可追溯到 Issue。
3. **Decision Gate — ADR**：
   - Agent 先閱讀既有 Accepted ADR，避免重新選型或違反限制。
   - 若變更引入重大新架構、跨元件影響、不可逆選型或顯著技術取捨，提出 **Proposed** ADR。
   - 人員審閱並批准後才可標記 Accepted；未批准則暫停受決策約束的實作。
4. **Implementation**：Agent 遵守 Spec + Accepted ADR；依 tasks 撰寫程式碼與測試。
5. **Review — PR**：檢查需求符合性、測試結果、架構決策一致性、資安風險與文件。
6. **Closure**：完成合併、同步需求文件、歸檔變更、結束 Issue／更新 Project 狀態。

## 4. 何時需要 ADR？

**建議建立**：改變持久性資料模型、選用核心推論框架、跨系統 API 契約、認證與資料安全策略、部署或事件架構等。

**不建議建立**：一般錯字修復、局部 bugfix、遵循已核准樣式的小型功能、一般 refactor。

ADR 記錄「重要決策的原因與取捨」，不是複製整份 OpenSpec Design。

## 5. 決策狀態與權責

- `Proposed`：討論中，不能當成已核准開發約束。
- `Accepted`：經指定人員批准，Agent 實作時須遵循。
- `Superseded`：被新 ADR 取代，保留原文件與連結。
- `Deprecated`：此決策不再適用，但保留歷史。
- **Agent**：提案、蒐證、檢查、修訂，不能自行升級為 Accepted。
- **人員**：對重大決策與 PR 進行核准。

## 6. 中央 Repo 與產品 Repo

中央 Repo：方法、範本、研究、跨專案共用原則。

產品 Repo：程式碼、專屬 ADR、OpenSpec、測試與特定版本的工程規範。複用中央規範應透過明確版本／複製策略，避免未審核的集中變更直接改變各產品行為。

## 7. 最小試辦驗證

- [ ] 用一個小型功能從 Issue 走到 PR。
- [ ] 在 Codex 起草規格後，讓 Claude Code 依同一份規格接手。
- [ ] 遇到重要架構變更，確認會提出 Proposed ADR 而非先實作。
- [ ] 人工核准後，驗證兩個 Agent 都遵循 Accepted ADR。
- [ ] 測試結果、Issue、Spec、ADR 與 PR 能相互追溯。

更新：2026-11-06
