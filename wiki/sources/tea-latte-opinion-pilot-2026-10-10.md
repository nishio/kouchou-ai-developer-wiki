---
type: source
summary: 午後の紅茶TEA LATTE二商品の公開検索投稿を195件保存し、比較・両方への評価49件を試験データにした2026-10-10の収集記録
sources:
  - https://www.kirinholdings.com/jp/newsroom/release/2026/0910_02.html
  - https://search.yahoo.co.jp/realtime/
---

# 午後の紅茶 TEA LATTE 意見収集 pilot

## 出典と鮮度

- [キリン公式発表](https://www.kirinholdings.com/jp/newsroom/release/2026/0910_02.html)より、2026-10-06発売の「TEA LATTE with ESPRESSO」「TEA LATTE CREAM & MILK」。2026-10-10確認。
- 2026-10-10 14:26 JSTにYahoo!リアルタイム検索の公開HTMLを6クエリの先頭ページだけ取得。X投稿の検索表示を読んだ観測で、X本体の全件・原文保証ではない。
- 検索語は `午後の紅茶` と `ティーラテ` / `エスプレッソ` / `クリーム` / `"TEA LATTE"` / `どっち` / `飲み比べ`。期間固定はしていない。

## 保存内容

local/private snapshot: `raw/experiments/2026-10-10-tea-latte-opinion-pilot/`。

取得表示236件を投稿IDで重複排除して195件を `posts.jsonl` に保存。本文を読んで二商品の比較・両方への評価がある49件（49著者）を `comparisons.jsonl` に選定。選定分はUTCで10月5〜10日の投稿で、発売日前日も含む。

分析用 `analysis_input.jsonl` は表示本文とIDだけ、暫定解釈は `annotations.jsonl` に分離。残り146件は `review_queue.jsonl` とし、単品の味の意見も含むため一括除外しない。HTML、検索条件、時刻、投稿URL、取得スクリプト、manifestをsnapshotに保存。pipeline実行・人間評価は未実施。

| ファイル | SHA-256 |
| --- | --- |
| posts.jsonl | `75c8c06865558521df9cbbf51b0cfcd20a8c3a0ffcf6586ae3a0a5ff4bc9251c` |
| analysis_input.jsonl | `6453fbbc12919e29256d01628b4d4cfafb1f9d047686570e7dff45326643479e` |

原文・投稿URL・HTMLは公開Wikiへ転記しない。[[tea-latte-opinion-dataset-feasibility-2026-10-10]]に利用上の判断を記載。

## Open Questions

- 検索表示の省略・引用依存。画像と引用先本文は未確認。
- 拡張時の期間統一、検索漏れ、投稿単位以外の重複処理。
- 公開デモ向けの原文利用・再配布条件と匿名化。今回はローカルの試験保存まで。

## Updates

- 2026-10-10: 初回収集。grasp書き込み未導入のためMarkdownで記録。
