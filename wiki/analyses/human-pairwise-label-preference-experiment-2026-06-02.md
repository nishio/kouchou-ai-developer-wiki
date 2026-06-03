---
type: analysis
summary: "ラベル品質実験では、人間に単独ラベルを批判させるのではなく、同じ tree / evidence から生成した複数ラベル案を algorithm 由来を隠した blind A/B で比較してもらう。困難な full UI 評価は label 単体・隣接ラベル集合・label と代表例に分解し、その pairwise preference を judge 較正データにする"
sources:
  - nishio-blind-human-label-presentation-context-2026-06-02.md
  - nishio-human-pairwise-label-preference-before-judge-2026-06-02.md
  - one-factor-experiment-principle-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - cli-pipeline-experiment-roadmap-2026-06-02.md
  - label-quality-rubric-evaluation-2026-05-29.md
  - label-quality-redesign-reset-2026-05-30.md
---

## 結論

ラベル品質実験の人間評価は、単独 label の批評から始めない。まず同じ tree / evidence / 表示文脈から複数の label 案を作り、人間には **A と B のどちらがよいか** を聞く。人間の役割は詳細な rubric judge になることではなく、比較可能な候補の中から選好を返すことである。[[nishio-human-pairwise-label-preference-before-judge-2026-06-02]]より

この時、人間には A/B がどの algorithm / process 由来かを見せない。`current main`、`setwise`、`LLM grouping`、`hierarchical` のような名前が見えると、実際の label quality ではなく先入観で選びやすい。A/B の表示順も randomize / counterbalance し、位置バイアスを記録する。[[nishio-blind-human-label-presentation-context-2026-06-02]]より

これにより、judge 改善の目標も変わる。最初の judge v1 は「単独 label の欠点を言語化できるか」ではなく、「人間の pairwise preference を再現できるか」を見る。

## なぜ A/B が先か

単独 label を見て、人間がすぐに「coverage が弱い」「sibling distinction が弱い」「unsupported axis がある」と言語化できるとは限らない。だが、同じ cluster に対する 2 つの label を並べれば、「こっちの方が中身に近い」「こっちは隣と紛らわしい」「短いが情報が落ちている」は判断しやすくなる。

したがって human observation は、まず自由記述の批評ではなく、次のような preference record として保存する。

```json
{
  "preference_id": "pref-001",
  "comparison_id": "cmp-hierarchical-8-40-label-process-001",
  "tree_run_id": "hierarchical_8_40",
  "cluster_id": "level1:3",
  "candidate_a_labelling_run_id": "baseline_merge",
  "candidate_b_labelling_run_id": "sibling_aware_setwise",
  "algorithm_origin_visible": false,
  "candidate_a_display_position": "left",
  "candidate_b_display_position": "right",
  "presentation_context": "label_with_representatives",
  "ui_surface": "cluster_detail_panel",
  "factor_under_test": "labelling_process",
  "fixed_inputs": ["dataset", "extracted_arguments", "embeddings", "tree_run", "evidence_policy"],
  "winner": "b",
  "confidence": 2,
  "reason_tags": ["covers_more", "distinguishes_siblings"],
  "free_text": null
}
```

自由記述は optional にする。人間に必須で求めるのは、`A / B / tie / unsure` と軽い confidence、必要なら理由タグまででよい。

## Presentation Context

人間に何を一緒に見せるかも、preference の一部として記録する。label は現実 UI で単独に存在するとは限らないため、presentation context を分けないと、どの場面でよい label なのかが分からない。[[nishio-blind-human-label-presentation-context-2026-06-02]]より

| presentation_context | 見せるもの | 主に分かること |
|---|---|---|
| `label_only` | label text だけ | heading として自立しているか、短く読めるか |
| `sibling_label_set` | 同じ親の隣接 / sibling labels 一式 | 隣と区別できるか、label set として読みやすいか |
| `label_with_representatives` | label + representative arguments | label が実例に支えられているか、重要な軸を落としていないか |

`presentation_context` を変える実験と、`labelling_process` を変える実験は分ける。algorithm / labelling process を比較する時は presentation context を固定する。逆に presentation context を比較したい時は、候補 label を固定して、表示文脈だけを変える。

`full_ui_context` は、最初の clean A/B 実験の presentation context にはしない。現実 UI では cluster size、description、代表例、隣接 label、階層、layout、interaction などが同時に効き、どれが preference を動かしたか解釈しにくい。だからこそ `label_only`、`sibling_label_set`、`label_with_representatives` の 3 つに分解している。full UI は、分解テストで候補を絞った後の統合確認として扱う。[[nishio-blind-human-label-presentation-context-2026-06-02]]より

## 1 要素原則との関係

「色々なパラメータ違いの label を作る」と「1 要素ずつ変える」は矛盾しない。1 つの比較 block では、変える軸を 1 つに絞る。

- labelling process 比較: tree、evidence、model を固定し、prompt / process だけを複数案にする
- evidence policy 比較: tree、prompt、model を固定し、見せる材料だけを複数案にする
- tree 比較: labelling process、evidence、model を固定し、tree generation だけを複数案にする
- presentation context 比較: 候補 label と tree を固定し、`label_only` / `sibling_label_set` / `label_with_representatives` だけを変える

複数軸を同じ A/B に混ぜると、人間が B を選んでも、prompt が効いたのか evidence が効いたのか分からない。[[one-factor-experiment-principle-2026-06-02]]より

## 最初にやる実験

最初の実験は、judge rubric ではなく **label variant の A/B preference collection** にする。

固定するもの:

- dataset: LLM grouping 400 件 corpus
- tree: `hierarchical_8_40`
- evidence policy: まず既存 evidence または同一 representative artifact
- model: 同じ model
- 表示文脈: cluster size、sibling labels、代表 argument の見せ方
- blind 条件: algorithm / process 名は人間に見せない。A/B の表示位置は randomize / counterbalance する

変えるもの:

- labelling process / prompt だけ

人間に聞くこと:

- A と B どちらがよいか
- tie / unsure か
- confidence は低 / 中 / 高のどれか
- 理由タグを選ぶなら、`covers_more`、`distinguishes_siblings`、`more_concise`、`less_unsupported`、`better_heading` 程度

最初は `sibling_label_set` または `label_with_representatives` で始めるのが現実的である。`label_only` は heading としての読みやすさを見る診断にはよい。full UI での確認は、A/B clean experiment ではなく、これらの分解テストで候補を絞った後に行う。

この preference dataset ができてから、judge に同じ A/B を見せる。judge の評価は、人間の winner / tie / reason_tags をどれだけ再現できるかで見る。

## 実験順序の補正

補正後の順序は次の通り。

1. tree / labelling run を蓄積する comparison corpus を作る。
2. 同じ tree / evidence で、パラメータ違いの label variants を作る。
3. algorithm / process 由来を隠し、presentation context を固定して、人間に blind A/B preference を聞く。
4. judge を、その preference を再現するものとして較正する。
5. judge が一定程度合ったら、より広い parameter sweep や view prototype の評価補助に使う。

これなら、人間に過剰な言語化を求めず、judge も人間判断と接続した形で育てられる。

## Open Questions

- A/B は cluster label 単位で始めるか、同じ top-level label set 全体で始めるか。
- 最初の presentation context は `sibling_label_set` と `label_with_representatives` のどちらがよいか。
- full UI の統合確認は、どの分解テストを通過した後に行うか。
- reason tag は最初から必須にするか、winner / tie だけで始めるか。
- 何件の pairwise preference があれば judge v1 の calibration と呼べるか。
- 人間 evaluator が複数いる場合、disagreement を label ambiguity として扱うか、rubric 不足として扱うか。

## Updates

- 2026-06-02: nishio の「full_ui_context は困難なので前 3 つに分解した」という補足を受け、`full_ui_context` を同列の presentation context から外し、分解テスト後の統合確認として扱う方針に補正した。
- 2026-06-02: [[nishio-blind-human-label-presentation-context-2026-06-02]] を追加。人間には algorithm / process 由来を隠して A/B を提示し、`presentation_context` として label 単体、隣接 label 集合、label + representative arguments を分けて記録する方針を追記した。
- 2026-06-02: 初版作成。nishio の「人間は単独のラベルだけ見て批判しにくいので、先にパラメータ違いのラベルを作って、どっちがよいかを聞くべき」という指摘を、pairwise preference 実験として整理した。
