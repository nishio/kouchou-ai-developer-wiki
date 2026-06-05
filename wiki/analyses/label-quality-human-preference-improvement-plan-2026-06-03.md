---
type: analysis
summary: "ラベル品質改善の次の実務計画。既存 LLM grouping 400 件 corpus を探索材料に、`hierarchical_8_40` tree などを固定して label variants を作り、algorithm 由来を隠した A/B bundle で human preference を集め、その preference を再現する judge を較正してから evidence / labelling / tree の clean experiment へ進む。2026-06-03 に 7 件回した時点で、prompt few-shot 由来のテンプレ冗長度が confound と判明し、prompt 修正からやり直しに reset"
sources:
  - labelling-prompt-few-shot-template-confound-2026-06-03.md
  - codex-log-label-preference-bundle-2026-06-03.md
  - nishio-label-evaluation-improvement-plan-request-2026-06-03.md
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - nishio-blind-human-label-presentation-context-2026-06-02.md
  - one-factor-experiment-principle-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - experiment-result-storage-policy-2026-06-02.md
  - cli-pipeline-experiment-roadmap-2026-06-02.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
  - label-quality-redesign-reset-2026-05-30.md
  - label-quality-rubric-evaluation-2026-05-29.md
---

> **Status (2026-06-03)**: この実験は仕切り直し。label_only 7 件を回した時点で、勝因が `labelling_process` ではなく labelling prompt few-shot 由来のテンプレ冗長度差だと判明した。詳細と次の方針は [[labelling-prompt-few-shot-template-confound-2026-06-03]] を参照。本ページの Plan セクションはアーカイブとして残す

## 結論

ラベル品質改善の次の計画は、**judge 改善でも prompt 改善でもなく、blind A/B preference を集める評価セット作り**から始める。既存 LLM grouping 400 件 corpus は exploratory material として使い、採用判断用の clean experiment では `factor_under_test` を 1 つに絞る。[[human-pairwise-label-preference-experiment-2026-06-02]]より [[one-factor-experiment-principle-2026-06-02]]より

最初の実装目標は、`raw/experiments/.../` に保存された tree / label artifacts から、algorithm / process 由来を隠した A/B comparison bundle と `human_preferences.jsonl` を作れる状態にすることである。

## 原則

- 人間には algorithm / process 由来を見せない。A/B の表示順も randomize / counterbalance する。
- 人間には単独 label の批評を書かせず、`A / B / tie / unsure`、confidence、任意の reason tags を返してもらう。
- full UI context は困難なので、まず `label_only` / `sibling_label_set` / `label_with_representatives` に分解する。
- algorithm / labelling process を比較する時は presentation context を固定する。
- presentation context を比較する時は label candidates を固定する。
- public wiki には summary / 判断だけを置き、raw artifact と preference records は `raw/experiments/<experiment_id>/` に置く。

## Plan

### 0. Baseline と corpus を固定する

最初は新しい dataset を増やさず、既存の `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` を使う。これは retrospective corpus なので採用根拠にはしないが、label variants と A/B bundle を作る材料としては十分である。[[llm-grouping-400-tree-label-corpus-2026-06-02]]より

固定するもの:

- dataset: LLM grouping 400 件 corpus
- tree: まず `hierarchical_8_40`
- comparison unit: まず top-level 8 cluster または sibling label set
- presentation context: 最初は `sibling_label_set` か `label_with_representatives`

### 1. Label variants を作る

`factor_under_test=labelling_process` として、同じ tree / evidence / model から複数 label 案を作る。

候補:

- baseline: current merge / existing label
- sibling-aware / setwise label
- coverage-focused label
- concise-heading label

この段階では winner を決めない。目的は、人間が比較できる候補を作ることである。

### 2. Blind A/B bundle を作る

人間に見せる bundle は、内部 metadata と表示を分ける。

表示:

- candidate A
- candidate B
- presentation context に応じた追加情報
- `A / B / tie / unsure`
- confidence
- optional reason tags

隠すもの:

- algorithm / process 名
- run id
- prompt 名
- `current main` かどうか

保存するもの:

- `comparison_id`
- `tree_run_id`
- candidate A/B の `labelling_run_id`
- `algorithm_origin_visible=false`
- A/B 表示位置
- `presentation_context`
- `factor_under_test`
- `fixed_inputs`
- `winner`
- `confidence`
- `reason_tags`

### 3. Human preference を集める

最初は大規模にしない。top-level 8 cluster に対して、1-2 presentation contexts だけでよい。

最初の収集単位:

- `sibling_label_set`: sibling と区別できるか、label set として読めるか
- `label_with_representatives`: label が代表例に支えられているか、重要な軸を落としていないか

`label_only` は heading としての診断には使えるが、最初の採用判断は上の 2 つを優先する。

### 4. Judge を preference に合わせる

judge v1 は、単独 label を採点するのではなく、同じ A/B bundle を見て人間の winner / tie / reason tags を再現できるかで見る。

最初の合格条件:

- 人間が明確に A/B を選んだ比較で、judge も同じ winner を選ぶ比率を見る
- tie / unsure を過剰に片方勝ちへ倒さない
- reason tags のうち `distinguishes_siblings` と `covers_more` を大きく外さない

この合格条件を満たすまでは、judge を使って label prompt の winner を決めない。

### 5. Clean experiment へ進む

preference collection と judge calibration ができてから、次の clean experiment を切る。

- evidence policy: prompt / tree を固定し、random sample と representative artifact を比較する
- labelling process: tree / evidence を固定し、prompt / process を比較する
- tree generation: labelling process / evidence を固定し、tree generation だけを比較する

full UI は最後に統合確認として扱う。最初の clean A/B には入れない。

## First Implementation Slice

最初の implementation slice は、次に絞る。

1. `human_preferences.jsonl` schema を決める。
2. 既存 corpus から `hierarchical_8_40` の top-level labels を取り出す。
3. 2 つ以上の `labelling_run_id` を A/B 候補にする。
4. algorithm / process 名を隠した `bundles/label_preference_ab.md` または `.html` を生成する。
5. bundle から `A / B / tie / unsure`、confidence、reason tags を JSONL に保存できる形式にする。

これは Web UI 機能ではなく、CLI / raw experiment artifact の改善である。

2026-06-03 に、この first slice を実行した。`scripts/build_label_preference_bundle.py` を追加し、既存 corpus の `hierarchical_8_40` tree を固定して、`none` vs `setwise` の label variants から 24 件の blind A/B questions を作った。生成物は `human_preference_questions.jsonl`、空の `human_preferences.jsonl`、`human_preferences.schema.json`、`bundles/label_preference_ab.md` / `.html` である。HTML には winner / confidence / reason tags / free text の入力フォームを追加し、完成済み回答だけを JSONL textarea に出す形にした。[[codex-log-label-preference-bundle-2026-06-03]]より

## Acceptance Criteria

- A/B 表示に algorithm / process 名が出ない。
- A/B の表示順が comparison ごとに記録されている。
- 各 comparison に `presentation_context`、`factor_under_test`、`fixed_inputs` が入っている。
- `label_only` / `sibling_label_set` / `label_with_representatives` のどれで評価したかが分かる。
- `human_preferences.jsonl` を後から judge calibration に使える。
- public wiki には raw preference 全件を載せず、summary と判断だけを載せる。

## Open Questions

- HTML bundle は小さな回答フォーム付きになったが、複数 evaluator の回答をどの粒度で分けて merge するか。
- 最初の comparison unit は top-level 8 cluster で生成済みだが、次は sibling label set 全体の 1 question 形式も必要か。
- reason tags は固定選択にするか、まず winner / confidence だけにするか。
- `#881` tracking issue にこの plan を first slice として接続するか、新しい issue に切るか。
- `label_with_representatives` は現時点では cluster CSV の先頭 3 件なので、representative artifact 作成後に再生成するか。

## Updates

- 2026-06-03: **実験仕切り直しを決定**。nishio が label_only 7 件 (cluster 1_1〜1_7) を回した結果、7/7 で「短い候補」が winner となり、勝因は `labelling_process` ではなく labelling prompt few-shot 由来のテンプレ冗長度差だと判明。3 文脈すべてに同じ confound があるため、残り 17 件は回さず prompt 修正から再出発する。詳細は [[labelling-prompt-few-shot-template-confound-2026-06-03]]
- 2026-06-03: 信頼度ラジオの "1 / 2 / 3" が意味不明だったため、HTML / md に `1 低 / 2 中 / 3 高` ラベルを追加し bundle を再生成
- 2026-06-03: [[codex-log-label-preference-bundle-2026-06-03]] を追加。first implementation slice として、`hierarchical_8_40` 固定の blind A/B bundle と `human_preferences` 系 JSONL / schema を生成したことを反映した。
- 2026-06-03: `label_preference_ab.html` に回答フォームと JSONL output textarea を追加したことを反映した。
- 2026-06-03: 初版作成。nishio の「改善計画を Wiki に書く？」という確認を受け、blind A/B preference collection から judge calibration へ進む実務計画として整理した。
