---
type: analysis
summary: "CLI を pipeline 実験の場として使い、まず clustering tree と labelling output の比較コーパスを作り、label variants の A/B human preference を集めてから judge / evidence artifact / ラベル改善 / マンダラート・付箋ビューを順に育てるロードマップ。Web UI は simple に保ち、CLI で比較可能な artifact を貯めてから昇格判断する"
sources:
  - codex-log-label-preference-bundle-2026-06-03.md
  - label-quality-human-preference-improvement-plan-2026-06-03.md
  - nishio-label-evaluation-improvement-plan-request-2026-06-03.md
  - nishio-blind-human-label-presentation-context-2026-06-02.md
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - nishio-human-pairwise-label-preference-before-judge-2026-06-02.md
  - one-factor-experiment-principle-2026-06-02.md
  - nishio-one-factor-experiment-principle-2026-06-02.md
  - codex-log-experiment-archive-cli-2026-06-02.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
  - nishio-cli-pipeline-ideas-2026-06-02.md
  - nishio-clustering-labeling-comparison-corpus-2026-06-02.md
  - nishio-experiment-result-storage-question-2026-06-02.md
  - broadlistening-tool-ecosystem-vision.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - experiment-result-storage-policy-2026-06-02.md
  - label-quality-redesign-reset-2026-05-30.md
  - label-quality-rubric-evaluation-2026-05-29.md
  - label-coverage-policy-2026-05-29.md
  - pipeline-step-addition-framing-2026-05-27.md
  - current-open-issue-triage-2026-06-01.md
  - thinking-targets.md
  - source-code.md
---

## 結論

CLI / `analysis-core` は、Web UI に複雑さを載せずに **pipeline を試行錯誤して発展させる実験場** として位置づけるのがよい。Web UI は全体傾向把握ユースケースの simple な default に保ち、CLI 側で judge、label、view prototype、比較 artifact を回してから、価値が見えたものだけ product へ昇格させる。[[broadlistening-tool-ecosystem-vision]]より

2026-06-02 の追加メモで、さらに 1 段手前の前提が明確になった。品質 judge を改善するにも、現状は比較対象が曖昧すぎる。まず各種 clustering method が作る tree と、その tree を入力にした各種 summarization / labelling process の label output を蓄積し、比較できるようにする必要がある。[[nishio-clustering-labeling-comparison-corpus-2026-06-02]]より

さらに、その実験結果をどこに蓄積するかも未決のままだった。保存先は 3 層に分け、`work/kouchou-ai/.../outputs/` は scratch、`raw/experiments/<experiment_id>/` は gitignored な一次 artifact snapshot、`wiki/` は public manifest / summary / analysis とする。[[experiment-result-storage-policy-2026-06-02]]より

また、実験を実際にやってみることは大事だが、current `main` から一度に複数要素を変えると結果の解釈が難しくなる。既存 artifact から作る corpus は exploratory として使い、採用判断用の clean experiment では `factor_under_test` を 1 つだけ変える。[[one-factor-experiment-principle-2026-06-02]]より

さらに、人間評価は単独 label の絶対批評から始めない。先に同じ tree / evidence から複数の label variants を作り、人間には A/B でどちらがよいかを聞く。その preference を judge 較正の教師信号にする。A/B では algorithm / process 由来を隠し、困難な full UI 評価は label 単体、隣接 label 集合、label + 代表例の分解テストとして扱う。[[human-pairwise-label-preference-experiment-2026-06-02]]より [[nishio-blind-human-label-presentation-context-2026-06-02]]より

したがって今回の並びは、次の順に補正する。

0. **比較コーパス / 実験台帳を作る**。
1. **実験ごとに 1 つの `factor_under_test` を決める**。
2. **同じ tree / evidence で label variants を作る**。
3. **人間に blind A/B preference を聞く**。
4. **その preference を再現するように judge を較正する**。
5. **ラベル生成入力と代表例 artifact を固定する**。
6. **その上でラベル生成 / refinement を改善する**。
7. **マンダラート / 付箋ビューを CLI 由来の display artifact として試す**。
8. **比較結果を残し、Web UI へ入れるかを別判断にする**。

ポイントは、ラベル品質改善を急いで winner を決めないこと。現状の rubric judge v0 は過去出力のズレを十分に検出できておらず、judge が見る evidence も representative artifact として固定されていない。さらに、人間も単独 label だけでは十分に批判しにくい。したがって、まず比較可能な label variants を作り、pairwise preference を集め、その preference を judge が再現できるようにしてから、採用判断に進む。[[label-quality-redesign-reset-2026-05-30]]より [[label-quality-rubric-evaluation-2026-05-29]]より [[clustering-labeling-comparison-corpus-2026-06-02]]より

## CLI 実験場としての意味

CLI は「上級者向けの同じ product」ではなく、分析者 / 研究者が次のような実験を回す場所である。[[broadlistening-tool-ecosystem-vision]]より

- `sampling_num`、全件入力、代表例選定、prompt variant を固定条件で比較する
- `human_preferences.jsonl` や `label_quality_rubric.jsonl` のような evaluation artifact を保存し、後で人間判断と judge を照合する
- `mandalart.html`、`sticky_board.html`、`cards.json` のような view prototype を既存 output から作る
- 同じ入力・同じ hierarchy に対して、label / judge / view だけを差し替えて差分を見る
- 成功した実験だけを issue / PR に切り出し、Web UI には簡単な表示として入れる

この方向は、pipeline step 追加を「step 数」ではなく「新しい成果物責務があるか」で判断する方針と整合する。prompt variant や copy 改善は step にしない。一方、judge 結果、代表例、カード一覧、named layout のように後続 consumer が読むものは artifact として残す。[[pipeline-step-addition-framing-2026-05-27]]より

採用判断に使う実験では、`main` baseline から変える要素を 1 つに絞る。複数要素を同時に変える run は禁止ではないが、`experiment_class=exploratory` として、仮説生成や judge calibration のための材料に留める。[[nishio-one-factor-experiment-principle-2026-06-02]]より

## 順序

### 0. 比較コーパス / 実験台帳

最初に必要なのは、judge ではなく比較台帳である。各種 clustering method でどのような tree ができたのか、その tree を入力にして各種 labelling process がどのような label を出したのかを、dataset / tree / labelling / human observation / judge run に分けて蓄積する。詳細は [[clustering-labeling-comparison-corpus-2026-06-02]]。

最小 slice:

- 既存 LLM grouping 400 件実験の `LLM grouping K=8`、`hierarchical K=8`、`K=20`、`[8,40]`、refinement variants を `tree_run` / `labelling_run` に分けて登録する
- 登録先は `raw/experiments/<experiment_id>/` とし、公開 wiki には manifest と summary だけを置く
- top-level tree と label set を横並びにした Markdown / HTML bundle を作る
- 人間が A/B preference と「この tree はこう見える」「この label はここが変」という observation を書ける場所を作る
- judge はその preference / observation を拾えるかで較正する

### 1. Label variants と human preference

最初に直すべきは、label prompt でも judge rubric でもなく、人間が比較しやすい評価セットを作ることである。単独 label の批評を求めず、同じ tree / evidence / display context から作った label variants を blind A/B で見せる。[[human-pairwise-label-preference-experiment-2026-06-02]]より

最小 slice:

- `hierarchical_8_40` tree を固定する
- evidence policy と model を固定する
- current label process と sibling-aware / setwise などの label variants を作る
- 人間には algorithm / process 名を見せず、`A / B / tie / unsure` と confidence を選んでもらう
- `presentation_context` は `label_only` / `sibling_label_set` / `label_with_representatives` のどれかを固定して保存する
- optional に `covers_more` / `distinguishes_siblings` / `more_concise` / `less_unsupported` などの理由タグを保存する

### 2. 品質 judge / evidence contract

次に直すべきは、judge が見る材料と失敗定義である。現状は、ラベル生成側も judge 側も sampling / evidence が揃っておらず、rubric judge v0 もほぼ満点を返してしまった。[[label-quality-rubric-evaluation-2026-05-29]]より

最小 slice:

- judge 入力を `label / description / size / representative arguments / sibling labels` に固定する
- representative arguments は配列先頭ではなく、`典型例 + 幅` を明示した artifact にする
- rubric は `coverage` と `sibling distinction` を重くし、`材料にない主張` と `見えている重要軸の欠落` を fatal 寄りに扱う
- `[8,40]` 既存 bundle 由来の A/B preference で、人間の winner / tie / reason tags を judge が再現できるか確認する

これは「judge を標準 pipeline に常時入れる」という意味ではない。まずは CLI / offline evaluation artifact として始め、1 の preference bundle に対する人間判断と照合する。[[label-quality-rubric-evaluation-2026-05-29]]より

### 3. ラベル生成入力

次に、LLM に何を見せてラベルを作るかを固定する。current main では、API 経由は initial / merge とも最大 30 件、analysis-core の built-in plugin / compat config default は 10 件の seed なし random sample でラベル付けしている。大きな cluster では、ラベルが cluster 全体ではなく「当たった標本」を説明している可能性がある。[[source-code]]より [[label-coverage-policy-2026-05-29]]より

最小 slice:

- 同じ hierarchy で `random 10 / random 30 / all args / representative artifact` を比較する
- token / latency / cost を cluster size 別に残す
- judge は 0 の固定 evidence contract を使う
- 改善判定は総合点だけでなく、`MISSING_VISIBLE_AXIS` や `UNSUPPORTED_AXIS` の減少を見る

### 4. ラベル生成 / refinement

ラベル改善は、現行 `hierarchical_label_refinement` の polish-only をそのまま育てるのではなく、元 arguments または設計された representative artifact を見て label / description を再生成できる責務として再検討する。現行 refinement は rep args を入力に取らないため、上流ラベルが誤っている場合に中身と照らして直せない。[[label-quality-redesign-reset-2026-05-30]]より

実験としては、次を分ける。

- label を短く読みやすくする UI heading 改善
- cluster の上位 2-3 軸を落とさない coverage 改善
- sibling と区別できる label set 改善
- description に boundary を補わせる説明改善

この 4 つは同じ「ラベル品質」でも、失敗モードと judge criteria が違う。

### 5. マンダラート view

マンダラートは、`[8,64]` のような階層と相性がよい。中心に全体 summary、周囲 8 マスに top-level cluster、各 top-level cluster をさらに 8 下位要素へ展開する view として試せる。`#880` も、主要 8 観点と 64 下位要素を探索する view として mock / prototype で読みやすさを確認するのが次の一手と整理されている。[[current-open-issue-triage-2026-06-01]]より

ただしこれは、最初から標準 pipeline の新 step にする必要はない。まずは CLI output の `hierarchical_result.json` から `mandalart.html` を生成する display prototype で十分である。必要になってから、layout metadata や `analysis_capabilities` に載せるかを判断する。

### 6. 付箋ビュー

付箋ビューは、KJ 法的にカードを眺める / 並べ替える / 人間が意味づけるための view 候補である。今回の nishio メモでは、マンダラートと並ぶ view 案として出た。[[nishio-cli-pipeline-ideas-2026-06-02]]より

最初の実験では、編集 UI まで作らず、次のような `cards.json` と standalone HTML でよい。

```json
{
  "card_id": "arg-123",
  "text": "...",
  "cluster_id": "cluster-level-2:17",
  "top_cluster_id": "cluster-level-1:3",
  "label": "...",
  "representative_role": "typical",
  "flags": ["boundary_candidate"]
}
```

この view は「全体傾向把握ユースケース」の Web default とは別に、CLI 分析者が構造を読み、仮説を作るための道具として始めるのが安全である。広聴AI 本体で KJ 原則のすべてを担わず、別ツール / CLI 実験として育てる方針とも整合する。[[thinking-targets]]より

## Issue / PR に切るなら

最初の PR は view 追加でも judge 改善でもなく、比較可能性を作る方がよい。

1. **experiment storage convention**: `work/` scratch、`raw/experiments/` raw snapshot、`wiki/` public summary の 3 層を固定する
2. **comparison corpus ledger**: dataset / tree_run / labelling_run / human_observation / judge_run を分けて保存する
3. **tree-label comparison bundle**: 既存 LLM grouping 400 件実験から、tree と label set を横並びにする Markdown / HTML を作る
4. **label variant A/B bundle**: 同じ tree / evidence で複数 label 案を作り、blind comparison UI / JSONL を作る
5. **human preference collection**: algorithm / process 由来を隠し、`presentation_context`、`A / B / tie / unsure`、confidence、reason tags を保存する
6. **judge evidence artifact**: representative arguments を固定し、judge と human review が同じ材料を見る
7. **rubric judge v1**: pairwise preference に合わせて criteria を締める
8. **label input sweep**: random / all args / representative artifact を同一 hierarchy で比較する
9. **Mandalart mock**: `[8,64]` の `hierarchical_result.json` から standalone HTML を生成する
10. **Sticky board mock**: `cards.json` と standalone HTML を生成し、典型例 / 幅 / 境界候補を目視できるようにする

この順にすると、マンダラートや付箋ビューが「見た目の新機能」で終わらず、ラベル品質と evidence 設計の改善 loop に接続できる。

2026-06-02 時点で 1 の first slice は `codex/experiment-storage` として実装中である。`analysis-core` CLI に `--experiment-root` / `--experiment-id` を足し、1 回の pipeline output を `raw/experiments/<experiment_id>/` 形式の `manifest.json`、dataset / tree / labelling JSONL、artifact copy に変換する。[[codex-log-experiment-archive-cli-2026-06-02]]より

同日、2 と 3 の初回版として、既存 LLM grouping 400 件実験を `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に登録し、`bundles/tree_label_matrix.md` / `.html` を作った。これで次の issue / PR slice は、judge / evidence contract の較正へ進める。具体的には、この corpus の 4 human observations を judge v1 が拾えるかを見る。[[llm-grouping-400-tree-label-corpus-2026-06-02]]より

ただしこの corpus は retrospective / exploratory であり、そのまま方式採用の根拠にはしない。次の clean slice は、`manifest.json` に `experiment_class`、`baseline_experiment_id`、`factor_under_test`、`fixed_inputs`、`changed_inputs` を入れ、`hierarchical_8_40` tree / evidence 固定で labelling process だけを変えた label variants を作る。judge rubric はその後、人間の A/B preference を再現できるかで較正する。[[one-factor-experiment-principle-2026-06-02]]より [[human-pairwise-label-preference-experiment-2026-06-02]]より

2026-06-03 時点では、この次の実務計画を [[label-quality-human-preference-improvement-plan-2026-06-03]] に切り出した。さらに first implementation slice として、既存 corpus の `hierarchical_8_40` を使い、algorithm / process 由来を隠した A/B bundle と `human_preferences` 系 JSONL / schema を生成した。[[codex-log-label-preference-bundle-2026-06-03]]より

## Open Questions

- comparison corpus は既存 LLM grouping 400 件実験だけで始めて足りるか。別 dataset も同時に入れるべきか。
- `raw/experiments/` は gitignored local snapshot なので、共有 artifact をどこへ置くか。
- A/B preference collection は、まず `[8,40]` bundle の top-level 8 cluster だけで足りるか。
- 品質 judge v1 は winner / tie 予測から始めるか、reason tags まで予測対象に含めるか。
- 最初の presentation context は label 単体ではなく、現実 UI の分解テストとして `sibling_label_set` または `label_with_representatives` から始めるべきか。
- full UI 統合確認は、分解テストで候補を絞った後に別途行うだけで足りるか。
- representative artifact は `hierarchical_result.json` 内に入れるか、別 `representative_arguments.json` として保存するか。
- マンダラートは `[8,64]` 専用でよいか、任意 cluster 数を 8 枠へ折りたたむルールが必要か。
- 付箋ビューは read-only から始めるか、人間の並べ替え結果を保存するところまで含めるか。
- Web UI に昇格させる基準は、構造把握スタンスの `解説素材性 / 突合素材性` で十分か、それとも mobile / print / workshop 利用の別基準が要るか。
- `#881` 系の次 PR は judge v1 へ進む前に、`factor_under_test` metadata を experiment archive に入れるべきか。

## Updates

- 2026-06-03: [[codex-log-label-preference-bundle-2026-06-03]] を追加。`scripts/build_label_preference_bundle.py` で 24 件の blind A/B questions と Markdown / HTML bundle を生成したことを反映した。
- 2026-06-03: [[label-quality-human-preference-improvement-plan-2026-06-03]] を追加。次の implementation slice を、`hierarchical_8_40` 固定の blind A/B bundle と `human_preferences.jsonl` schema 作成として明確化した。
- 2026-06-02: [[nishio-blind-human-label-presentation-context-2026-06-02]] を追加。A/B evaluation では algorithm / process 由来を人間に隠し、提示文脈を label 単体 / 隣接 label 集合 / label + 代表例に分ける方針を追記した。
- 2026-06-02: nishio の補足を受け、full UI context を同列の A/B 条件から外し、label 単体 / 隣接 label 集合 / label + 代表例への分解テストとして扱う方針に補正した。
- 2026-06-02: [[human-pairwise-label-preference-experiment-2026-06-02]] を追加。judge 改善の前に、同じ tree / evidence から作った label variants を人間に blind A/B 比較してもらい、その preference を judge 較正データにする順序へ補正した。
- 2026-06-02: [[one-factor-experiment-principle-2026-06-02]] を追加。既存 corpus は exploratory、採用判断用の clean experiment は `factor_under_test` を 1 つに絞る方針をロードマップに反映した。
- 2026-06-02: [[llm-grouping-400-tree-label-corpus-2026-06-02]] を追加。既存 LLM grouping 400 件実験の comparison corpus と tree-label matrix bundle ができたため、次の slice を judge / evidence contract 較正へ進める状態に更新した。
- 2026-06-02: [[codex-log-experiment-archive-cli-2026-06-02]] を追加。最初の issue / PR slice である experiment storage convention を `analysis-core` CLI の `--experiment-root` / `--experiment-id` 実装として進め、次は comparison corpus ledger と tree-label comparison bundle に進む流れへ更新した。
- 2026-06-02: 実験結果の保存先問題が未解決だったため、[[experiment-result-storage-policy-2026-06-02]] を追加し、`work/` scratch、`raw/experiments/` raw snapshot、`wiki/` public summary の 3 層方針を接続した
- 2026-06-02: nishio の追加メモを受け、judge / evidence contract の前に「clustering tree と labelling output の比較コーパス / 実験台帳」を置くよう順序を補正。詳細を [[clustering-labeling-comparison-corpus-2026-06-02]] に切り出した
- 2026-06-02: 初版作成。nishio の「CLI で pipeline を試行錯誤して発展させる」「マンダラート / 付箋ビュー」「ラベル品質改善の前に品質 judge 改善」というメモを、CLI 実験 lane の順序として整理した。`work/kouchou-ai/` は `main@3c5d1f026757` まで fast-forward 済み。
