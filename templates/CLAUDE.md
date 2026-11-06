# CLAUDE.md — Agent Coding Lifecycle 範本（Claude Code）

> 本檔為**共用規範模板**，應在各產品 Repo 根目錄複用，並與該 Repo 的 `AGENTS.md` 內容保持一致；不是獨立的一套決策政策。

## Workflow

1. 開始修改前，先閱讀 GitHub Issue、OpenSpec specs 和相關 change 文件。
2. 搜尋 `docs/adr/` 的 **Accepted ADR**，不得違反既有架構限制。
3. 只有重大、長期影響、跨元件或難以逆轉的決策才新增 **Proposed ADR**。
4. 任何 Proposed → Accepted 或取代已核准 ADR 的變更均須由人員核准；AI 不得自行批准。
5. 按 OpenSpec tasks 實作，執行專案指定的測試／檢查。
6. PR 應連結 Issue、OpenSpec、相關 ADR，並摘要測試結果、部署與相容性風險。
7. 合併後依專案流程更新規格與任務狀態。

## Conflict Handling

- 當 Issue、OpenSpec、Accepted ADR 相互矛盾時，先回報差異與影響；不可靜默覆蓋既有決策。
- 不以 Chat History 取代版控文件。
- 不把每個 bugfix 或日常 refactor 都當成需要 ADR。

## Project Configuration

請在產品 Repo 中補入實際 build/test 指令、依賴、部署目標與資料保護規則。

參考中央規劃：https://github.com/appletiger0704/agent-coding-lifecycle
