---
type: analysis
summary: "pipeline 実験は探索 corpus と採用判断用の clean experiment を分け、採用判断では current main baseline から `factor_under_test` を 1 つだけ変えるべきという実験設計原則。ラベル品質は単独批評ではなく A/B preference で人間評価し、複数要素変更 run は単独で winner 判定しない"
sources:
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - nishio-human-pairwise-label-preference-before-judge-2026-06-02.md
  - nishio-one-factor-experiment-principle-2026-06-02.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - experiment-result-storage-policy-2026-06-02.md
  - cli-pipeline-experiment-roadmap-2026-06-02.md
  - label-quality-redesign-reset-2026-05-30.md
  - label-quality-rubric-evaluation-2026-05-29.md
---

## 結論

CLI / `analysis-core` で pipeline を試す時は、**探索 corpus** と **採用判断用の clean experiment** を分ける。やってみることは重要だが、current `main` から clustering、tree、labelling、evidence、judge を一度に変えると、結果が良くても悪くても原因が読めない。[[nishio-one-factor-experiment-principle-2026-06-02]]より

したがって、採用判断に使う実験では、baseline を current `main` の run に置き、`factor_under_test` を 1 つだけ明示する。複数要素を同時に変えた run は `exploratory` として扱い、仮説生成、failure mode 発見、judge calibration に使うが、単独で winner 判定しない。

ただしラベル品質では、人間に単独 label の絶対評価や詳細批評を求める前提も危うい。人間評価は、同じ tree / evidence から生成した複数 label 案の A/B preference として集め、その preference を judge が再現できるかを見る順序にする。[[human-pairwise-label-preference-experiment-2026-06-02]]より

## 2 種類の実験

### 探索 corpus

探索 corpus は、既存 artifact や複数 variant を集めて、何を見るべきかを発見するためのもの。

- tree shape、label set、judge result、人間 observation を横並びにする
- 失敗モードや評価軸を洗い出す
- judge が再現すべき human preference / observation を作る
- 次に切る clean experiment の候補を作る

2026-06-02 の `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` はこの位置づけである。5 tree run / 10 labelling run / 5 judge run / 4 observation を保存したので、比較の材料としては有用だが、複数要素が混ざった retrospective corpus であり、採用判断の causal evidence ではない。[[llm-grouping-400-tree-label-corpus-2026-06-02]]より

### Clean Experiment

clean experiment は、採用判断や実装変更の根拠にするためのもの。

- baseline: current `main` の run
- factor_under_test: 1 つだけ
- fixed_inputs: dataset、extracted arguments、embeddings、tree、model、prompt、evidence など固定したものを明示
- changed_inputs: 実際に変えたものを明示
- comparison_question: 何を見れば勝ち負けが分かるかを事前に書く

この区別をしないと、「LLM grouping が良い」「hierarchical が良い」「balanced が良い」のような粗い winner に戻り、どの実装要素を変えるべきかが曖昧になる。[[clustering-labeling-comparison-corpus-2026-06-02]]より

## Ledger に追加する項目

`raw/experiments/<experiment_id>/manifest.json` には、保存場所だけでなく実験設計も残す。

```json
{
  "experiment_class": "exploratory",
  "baseline_experiment_id": null,
  "factor_under_test": null,
  "fixed_inputs": [],
  "changed_inputs": [],
  "comparison_question": null,
  "adoption_decision_allowed": false
}
```

採用判断に使う clean experiment なら、たとえば次のようにする。

```json
{
  "experiment_class": "clean",
  "baseline_experiment_id": "main-2026-06-02-hierarchical-8-40",
  "factor_under_test": "labelling_process",
  "fixed_inputs": ["dataset", "extracted_arguments", "embeddings", "tree_run", "model", "evidence_policy"],
  "changed_inputs": ["labelling_prompt"],
  "comparison_question": "同じ tree と evidence で、sibling distinction と coverage が改善するか",
  "adoption_decision_allowed": true
}
```

## 1 要素ずつ変える例

| 見たいこと | 固定するもの | 変えるもの |
|---|---|---|
| labelling process | dataset、extracted args、embeddings、tree、model、evidence policy | labelling prompt / process だけ |
| evidence policy | dataset、tree、labelling prompt、model | random / all args / representative artifact の 1 軸だけ |
| judge rubric | comparison bundle、human observations、judge model | rubric / prompt だけ |
| judge model | comparison bundle、human observations、rubric | judge model だけ |
| clustering method | dataset、extracted args、embeddings、labelling process、evidence policy | tree generation method / params だけ |

clustering method 比較では、tree が変わるため label output も従属的に変わる。この場合の `factor_under_test` は tree generation であり、labelling process と evidence policy を固定して、tree 差が label set にどう伝播するかを見る。

## Human Preference を先に集める

人間評価は、まず pairwise preference にする。単独 label を見て「どこが悪いか」を言語化してもらうのではなく、同じ cluster / 同じ label set に対する候補 A/B を blind に出し、`A / B / tie / unsure` を選んでもらう。理由は optional なタグでよい。[[nishio-human-pairwise-label-preference-before-judge-2026-06-02]]より

この時も 1 要素原則は維持する。たとえば label prompt を比べる block では tree と evidence を固定し、evidence policy を比べる block では prompt と tree を固定する。複数 parameter variants を作ることはよいが、1 つの A/B 比較で変わっている軸を混ぜない。

## 次にやる clean experiment

最初の clean experiment は、既存 corpus から仮説を選んで 1 要素に切り直す。

1. `hierarchical_8_40` の tree と evidence を固定し、labelling process だけを変えた label variants を作る。
2. その variants を人間に blind A/B で見せ、preference を集める。
3. judge rubric / prompt は、その preference を再現できるかで較正する。
4. 次に、prompt を固定して evidence policy だけを `random sample` から `representative artifact` に変える。

この順にすると、judge 改善、label 改善、view prototype が「なんとなく良い」ではなく、どの要素が効いたかを説明できる。

## Open Questions

- clean experiment の `baseline_experiment_id` は current `main` commit ごとに作るか、dataset ごとに固定 baseline を持つか。
- 1 つの PR に exploratory corpus 作成と clean experiment を同居させてよいか。レビュー上は分ける方が読みやすい可能性が高い。
- `factor_under_test` の語彙を自由記述にするか、`tree_generation` / `labelling_process` / `evidence_policy` / `judge_rubric` / `view_layout` などに enum 化するか。
- pairwise preference の比較単位は cluster label 単位か、label set 全体か。

## Updates

- 2026-06-02: [[human-pairwise-label-preference-experiment-2026-06-02]] を追加。ラベル品質の人間評価は単独批評ではなく、同じ tree / evidence から作った label variants の A/B preference として集める方針に補正した。
- 2026-06-02: 初版作成。nishio の「やってみるのは大事だが、main から一度にいろいろ変えると解釈が難しい。1 要素ずつ変えた実験にすべき」という指摘を、探索 corpus と clean experiment の区別として整理した。
