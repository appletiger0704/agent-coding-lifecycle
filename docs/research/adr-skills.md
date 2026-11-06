# ADR Skills、MADR、ADR Tools — 比較與研究

> 狀態：Research；關聯 [Issue #3](https://github.com/appletiger0704/agent-coding-lifecycle/issues/3)、[總體 Issue #1](https://github.com/appletiger0704/agent-coding-lifecycle/issues/1)。此表是適用性判斷，**不是使用人數排行，也不代表工具已導入**。

## 候選比較

| 工具／資源 | 主要用途 | 初期建議 |
|---|---|---|
| [Architecture Decision Record Skill](https://github.com/architecture-decision-record/architecture-decision-record/tree/main/skills/architecture-decision-record-skill) | ADR 建立、選擇模板、檔案命名與取代 | 參考 |
| [Documentation and ADRs](https://github.com/addyosmani/agent-skills/tree/main/skills/documentation-and-adrs) | ADR 與 API / README 等文件慣例 | 優先試用 |
| [Jvdbreemen ADR Skill](https://github.com/Jvdbreemen/adr-skill) | 防止 Agent 略過 ADR、完整性／證據／清晰度／一致性檢查 | 進階治理參考 |
| [AgDR](https://github.com/me2resh/agent-decision-record) | Agent 決策歷程與模型、觸發、時間的中繼資料 | 暫緩 |
| [Vercel ADR Skill](https://github.com/vercel/ai/blob/main/skills/adr-skill/SKILL.md) | 強化 ADR 可供 Coding Agent 執行的限制與驗證 | 設計參考；檔案標示 internal |
| [MADR](https://github.com/adr/madr) | Markdown 決策記錄模板與格式 | 優先使用最小模板 |
| [ADR Tools](https://github.com/npryce/adr-tools) | CLI 編號、建立與取代 ADR | 初期不需要 |

## 技術注意事項（已核對程式碼）

1. `adr-tools` 的 `adr new` 使用 `Accepted` 作為預設狀態。若要求人工核准，須調整模板／後處理，並在審核前維持 Proposed。
2. `adr new -s` 依賴 `## Status` 區段加入取代連結；直接放入不同結構的 MADR 模板不一定正常。
3. `adr-tools` 支援使用自訂模板，例如 `docs/adr/templates/template.md`（以實際初始化路徑為準）。
4. Agent Skill 僅提供行為指引，不能替代 CI、PR Review、branch protection 或人工核准。
5. 避免把 ADR 裡所有實作細節又複製到 OpenSpec Design；可透過相互連結保留單一資訊來源。

## 推薦導入順序

**Phase 1：** OpenSpec + Documentation and ADRs Skill + MADR 最小模板 + GitHub Issues/PR。

**Phase 2：** 若有可量化管理痛點，再加入 ADR Tools、CI 文件驗證與架構合規檢查。

## 評估準則

- 能否先掃描已有 ADR，避免違反已核准決策？
- 是否只在重大架構變更時提出新 ADR？
- 是否保留候選方案、決策原因、負面影響、驗證方式？
- 是否能把 Proposed 與 Accepted 明確分開？
- Codex 與 Claude Code 交接後是否能重現相同選型約束？
- 會否在無人工核准的情況下自行修改已接受決策？

## 待驗證

- [ ] 確認 `npx skills add addyosmani/agent-skills --skill documentation-and-adrs` 在目標工具版本的實際安裝流程。
- [ ] 測試兩個 Agent 對 ADR 例外情境的一致性。
- [ ] 評估 MADR 模板是否需增加 Verification、Issue、OpenSpec 路徑。
- [ ] ADR 數量增加後再評估 CLI 管理價值。

更新：2026-11-06
