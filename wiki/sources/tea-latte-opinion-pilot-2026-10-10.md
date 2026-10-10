---
type: source
summary: 午後の紅茶TEA LATTE二商品の公開投稿を195件から1485件へ拡張し、比較・両方への評価98件を整理した2026-10-10の収集記録
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

### 2026-10-10 14:39 — 追加収集

14:37〜14:38 JSTに「午後ティー」などの表記揺れと追加読み込みを使って拡張。14検索・159ページから検索別1,994件を取得し、前回分との投稿ID重複排除後は **1,485件（新規1,290件）**。全検索で10月5日00:00 JST以前の投稿に到達して停止。網羅性を保証するものではない。

拡張snapshotは `raw/experiments/2026-10-10-tea-latte-opinion-expanded/`。前回snapshotは維持。rawのうち期間内1,421件、商品語候補1,216件、意見語候補550件、意見語と比較語の候補145件。後三者は機械判定であり、有効な意見として確認済みの件数とは区別する。

新規比較候補95件の本文をCodexが読み、二商品の比較・両方への評価49件を追加。前回49件と合わせて **98件（98著者）** を `analysis_input.jsonl` に整理した。単品・他商品との比較36件、期待5件、告知3件、別対象への「両方」1件、家族の好みの伝聞1件は今回の比較セットから外した。暫定タグ・選定理由は別ファイルに保持し、人間による正解評価ではない。

| 拡張版ファイル | SHA-256 |
| --- | --- |
| posts.jsonl | `8f287e062aa400b7ff6fb689491210135e32e3fcced372b2dc975dbd20f04403` |
| analysis_input.jsonl | `68265b0c626ccacedef6b316e9770b0e8a746192d060e8736ae870882b8ce532` |

公開検索のページ番号指定では同じ結果が返ることを確認し、「もっと見る」のカーソルで遡った。raw内の同一本文17グループは記録のみで削除していない。検索語依存・画像未確認・引用先未確認という限界と、原文を公開しない方針は継続。

### 2026-10-10 15:06 — 公開デモ分析へ

味の語候補550件を起点とする分析を実行し、原文照合後の377意見で公開用デモを作成した。初回・拡張収集時点の「pipeline未実施」は当時の記録として維持し、現在の結果・公開範囲は [[tea-latte-public-demo-analysis-2026-10-10]] を参照する。
