# GitHub Issues / Projects / Actions — 整合提案

> 狀態：Research；關聯 [Issue #5](https://github.com/appletiger0704/agent-coding-lifecycle/issues/5)、[總體 Issue #1](https://github.com/appletiger0704/agent-coding-lifecycle/issues/1)。

## 職責

- **Issues**：需求、研究方向、技術問題、工作追蹤及驗收條件。
- **Projects**：跨 Issue / PR 的視覺化進度與 Timeline（尚未建立）。
- **Pull Requests**：變更、審查、測試證據與決策連結。
- **Actions**：第二階段導入文件與程式驗證（目前未配置）。
- **Rulesets / Branch protection**：對必要審核及 CI 結果設定合併閘門；必須另行啟用。

## 建議狀態（Projects）

`Research → Proposed → Approved → Implementing → In Review → Done`

這是建議的管理欄位，不代表目前已有 GitHub Project。

## Issue 最少欄位

背景／目標、範圍、驗收標準、相關 OpenSpec change、適用 ADR、優先級。

## PR 最少欄位

- 關聯 Issue
- OpenSpec change 路徑
- 適用 ADR（若無請說明）
- 程式改動摘要與測試結果
- 相容性／部署／資安風險
- 文件是否同步

## 第一階段

只使用 Issues、Markdown、PR 的人工檢查，先觀察是否能完整追溯。

## 第二階段

- [ ] 測試與 lint
- [ ] Markdown / 連結檢查
- [ ] 提醒審核有關 ADR 的改動
- [ ] 在具體風險評估後增加 PR / Branch rules
- [ ] 確認哪些檢查可強制、哪些需要人工判斷

**重要限制：** CI 無法可靠地僅靠文字判斷所有架構設計是否合理；人工負責重大設計決策的最終核准。

更新：2026-11-06
