---
title: "Open Japan PoliTech Platform(OJPP)"
name: ojpp
summary: "Open Japan PoliTech Platform（ochyai）。DD2030 を参照しつつ『エージェントファースト設計を追加』を掲げる外部の政治テック基盤。BroadListening を再実装"
type: entity
sources:
  - ojpp-repo-source-2026-10-13.md
---

## What

**Open Japan PoliTech Platform (OJPP)** は GitHub `ochyai/open-japan-politech-platform` の OSS。「AIエージェント時代の政治インフラ」を掲げる Next.js 15 monorepo で、Portal + 7 アプリ（BroadListening β / MoneyGlass / PolicyDiff / ParliScope / SeatMap / CultureScope / SocialGuard）を持つ。[[ojpp-repo-source-2026-10-13]]より。

**[[dd2030]] 配下ではなく外部プロジェクト**である点に注意。関連プロジェクト表で DD2030 を「方向性は近い」とし、自らを「**エージェントファースト設計を追加**」した版と位置づけている。

## なぜ kouchou-ai 開発者に関係するか

- **BroadListening を再実装**している。ただし Argument Mining + デジタルフェロモン(Stigmergy) + 適応度/Shannon 多様性という独自モデルで、[[kouchou-ai]] の抽出→埋め込み→階層クラスタリングとはパイプラインが異なる（[[broadlistening]] の広義/狭義の揺れの一例）。コード単位の突き合わせ評価は [[ojpp-vs-kouchou-ai-broadlistening-model-2026-10-13]]（結論: 埋め込み・空間可視化は実装破綻、argument mining / 生態系ダイナミクスは着想価値あり）
- **MoneyGlass** は政治資金可視化で [[polimoney]] と機能が重なる
- 開発プロセスが Claude Code / Entire 前提で、`agent/` ラベルの AI PR を歓迎。AI コーディング運用の比較対象になる（[[coding-agents]]）
- 「**エージェントファースト設計**」という語の中身と、kouchou-ai/DD2030 への射程は [[ojpp-agent-first-design-read-2026-10-13]] で批判的に整理した

## 鮮度・素性

- repo は 2026-02 作成・**2026-03-22 を最後に dormant**（HEAD `d1a9c2b`）。`v0.2`（エージェント認証 / MCP / 監査ログ）は未着手のまま
- GitHub アカウント `ochyai` は一般に落合陽一のアカウントとして知られるが、本 wiki では一次確認していない（下記 Open Questions）

## Open Questions

- `ochyai` = 落合陽一 本人かは一次未確認。素性より「公開 repo が何を主張し何を実装したか」を一次とする
- OJPP は demo 寄りの完成度か、継続開発される基盤か（2026-03 以降停止しているため現状は前者寄り）

## Updates

- 2026-10-13: 初回作成（[[nishio]] から repo 参照依頼。「エージェントファースト設計」の意味を問うクエリから）
