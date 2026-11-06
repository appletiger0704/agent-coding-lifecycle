# AGENTS.md — Agent Coding Lifecycle 範本（Codex）

> 本檔是**複用模板**，不表示已套用到任何產品 Repo。複製到專案根目錄後，請填入該專案實際命令與路徑。

## Source of Truth

1. GitHub Issue：業務目標、優先級與驗收標準。
2. OpenSpec：現行 specs、個別 change 的 proposal / design / tasks。
3. `docs/adr/`：已接受的重要架構決策與限制。
4. 既有程式碼與測試：實作行為的證據，但不可取代需求與 ADR。

## Before Coding

- 閱讀關聯 GitHub Issue 和 OpenSpec change。
- 搜尋並閱讀相關 **Accepted ADR**，遵守已核准限制。
- 如有重大、跨元件、難以逆轉或與既有 ADR 衝突的選擇，**先提出 Proposed ADR** 並請求人工核准。
- 除非已明確授權，不得自行將 ADR 改為 Accepted，不得繞過審核。
- 小型 bugfix 與在既有模式內的調整不需建立新 ADR。

## During Coding

- 按 OpenSpec tasks 逐項實作與測試。
- 避免擴增沒有規格依據的功能。
- 若需求或 ADR 互相矛盾，明確回報衝突，不得自行假設可以推翻已核准架構。
- 使用適當的測試與靜態檢查；實際執行指令由各專案指定。

## Before Pull Request

- 提供 Issue / OpenSpec / ADR 的連結（若無 ADR 請標示 N/A）。
- 提供測試命令與結果，說明未完成的測試與風險。
- 更新必要文件及規格，不將聊天紀錄當作唯一決策來源。
- 等待 PR 審核，避免假設 CI 自動代表架構核准。

## Repository-Specific Overrides

請在各產品 Repo 補充實際環境、建置命令、測試命令、部署政策與敏感資訊處理方式。

參考中央規劃：https://github.com/appletiger0704/agent-coding-lifecycle
