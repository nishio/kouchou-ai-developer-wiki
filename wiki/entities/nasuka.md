---
name: nasuka
summary: "Nasuka Sumino (角野) — 抽出プロンプト・limited-publish・クラスタタイトル手動編集等を実装したコントリビュータ"
type: entity
sources:
  - meeting-minutes.md
---

## Who

**nasuka (Nasuka Sumino, 角野)**。2025-06-04 の定例で、本人が「（開発とは関係ないトピックですが）チームみらいの次回参院選の公認候補予定者になりました」と共有している（[[meeting-minutes]] 2025/06/04 見出しより）。

[[kouchou-ai]] の中核コントリビュータの一人。詳細は [[meeting-minutes]] 各所に散在。

## kouchou-ai での主な貢献

- **抽出プロンプトの書き換え**、**structured output 化**
- **limited-publish (YouTube unlisted 風 限定公開)** — PR #500 / Issue #341
- **クラスタタイトル手動編集** — PR #545 / Issue #310（DB 導入を退け、ファイルストレージで実装）
- **team-mirai/kouchou-ai フォーク運用**（2025-05-28）— 「公開で fork して実装すれば dd2030 の人もチームみらいがどういう変更をしているか見える」という方針
- **PR #582** — team-mirai 固有の修正（cluster→issue link、Azure バグ修正）を upstream 戻し
- **`nasuka/flexible-text-analyzer`** — 埋め込みを使わない LLM だけのクラスタリング前身プロトタイプ

## Related Analyses

- [[nasuka-statements-retrospective-2026-05-25]] — 過去発言を、運用基盤・実利用・分析品質・governance の観点で振り返る考察

## 名前表記

`nasuka`, `Nasuka Sumino`, `角野` — 同一人物として参照。`sumino` 単体表記も同一人物のことがある（要文脈確認）

## Updates

- 2026-05-17: 初回作成
- 2026-05-25: 過去発言の振り返り [[nasuka-statements-retrospective-2026-05-25]] への導線を追加
- 2026-10-07: lint。初回作成時の「週次会議の元ファシリテーター」は議事録・oss_weekly_reporter に出典が見つからず削除。「2025-12 以降はチームみらい 2026 衆院選候補」は、議事録 2025/06/04 の本人発言「チームみらいの次回参院選の公認候補予定者」と時期・選挙の種類が食い違っていたため、原文どおりに訂正。PR #500 / #545 / #582 の author が nasuka であることは GitHub で確認済み
