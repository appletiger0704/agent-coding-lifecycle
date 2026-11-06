# OpenSpec — 研究與導入策略

> 狀態：Research；關聯 [Issue #2](https://github.com/appletiger0704/agent-coding-lifecycle/issues/2)、[總體 Issue #1](https://github.com/appletiger0704/agent-coding-lifecycle/issues/1)。

## 定位

OpenSpec 是需求與變更規格層，讓 Coding Agent 在實作前能取得可版本化的需求、設計及 tasks。

建議典型專案結構（實際以工具生成與既有專案慣例為準）：

```text
product-repo/
└── openspec/
    ├── specs/       # 現行系統規格
    └── changes/     # 單次變更及其 proposal、specs、design、tasks
```

## 如何整合 GitHub

| 資料 | 建議位置 |
|---|---|
| 需求背景與優先級 | GitHub Issue |
| 驗收行為 | OpenSpec specs |
| 技術設計 | OpenSpec design |
| 工作拆解 | OpenSpec tasks |
| 重要跨功能選型的理由 | ADR |
| 實作與證據 | PR、測試結果 |

每次變更建議在 Issue 補上 OpenSpec change ID，PR 同時連結 Issue、OpenSpec 路徑、適用 ADR。

## PoC 待驗證

- [ ] 依官方最新版本驗證安裝與初始化指令。
- [ ] 確認 change 的建立、實作與 archive 行為。
- [ ] 判斷何種小型修正可免用完整 spec 流程。
- [ ] 確認 `design.md` 與 ADR 不會重複產出。
- [ ] 用 Codex 起草、Claude Code 接手驗證交接品質。

## 風險

- 若每個小修正都強制建立大量設計檔，維護成本可能超過收益。
- Agent 只讀最新對話卻未讀 Repository 文件，仍可能產生架構漂移。
- OpenSpec 的具體檔案名稱與 CLI 步驟需以安裝時版本為準。

參考：https://github.com/Fission-AI/OpenSpec

更新：2026-11-06
