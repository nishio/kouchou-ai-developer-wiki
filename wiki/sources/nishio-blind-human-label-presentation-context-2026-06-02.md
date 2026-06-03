---
type: source
summary: "2026-06-02 に nishio が、人間への A/B ラベル評価ではどのアルゴリズム由来かを隠して聞くべきであり、困難な full UI 評価をラベル単体・隣接ラベル集合・ラベルと代表例の分解テストとして扱う必要があると指摘したメモ"
sources:
  - user-message-2026-06-02
---

## What it is

2026-06-02 の nishio からの追加メモを source 化したもの。

要点は 2 つある。第一に、人間に A/B preference を聞く時は、どちらがどの algorithm / process 由来かを隠すべきである。第二に、full UI context での評価は困難なので、まず label 単体、隣接している label 集合、label と代表例という 3 つの提示文脈に分解して評価する。

## Extracted Points

- A/B の候補は `A` / `B` として提示し、`current main`、`setwise`、`LLM grouping`、`hierarchical` などの由来名を人間に見せない。
- 表示順も固定しない。A/B の左右や上下は randomize / counterbalance し、位置バイアスを減らす。
- label 単体の評価は、heading として自立しているかを見る。
- 隣接 / sibling label 集合の評価は、隣と区別できるか、label set として読みやすいかを見る。
- label と代表例の評価は、label が実際の意見に支えられているか、重要な軸を落としていないかを見る。
- full UI context の A/B は複合要因が多く困難なので、最初の clean experiment にはしない。前 3 つの分解テストを先に行い、UI 全体は後段の統合確認として扱う。

## Related Pages

- [[human-pairwise-label-preference-experiment-2026-06-02]]
- [[one-factor-experiment-principle-2026-06-02]]
- [[clustering-labeling-comparison-corpus-2026-06-02]]
- [[cli-pipeline-experiment-roadmap-2026-06-02]]

## Open Questions

- 最初の blind A/B は `label_only`、`sibling_label_set`、`label_with_representatives` のどれから始めるか。
- 同じ label pair を 3 つの presentation context すべてで評価するか、まず 1 つに絞るか。
- full UI の統合確認は、分解テストで勝った候補だけを public-viewer に近い mock へ載せる形で足りるか。

## Updates

- 2026-06-02: nishio の「full_ui_context は困難なので前 3 つに分解した」という補足を受け、full UI は同列の A/B 条件ではなく、分解テスト後の統合確認として扱う方針に補正した。
- 2026-06-02: 初版作成。
