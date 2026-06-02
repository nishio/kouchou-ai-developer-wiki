---
type: analysis
summary: "品質 judge を改善する前に、dataset × clustering tree × labelling process × label output を蓄積する比較コーパスを作るべきという整理。採用判断に使う実験は 1 要素ずつ変え、judge はこの corpus 上で人間が見た失敗を検出できるかを較正する"
sources:
  - one-factor-experiment-principle-2026-06-02.md
  - nishio-one-factor-experiment-principle-2026-06-02.md
  - codex-log-experiment-archive-cli-2026-06-02.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
  - nishio-clustering-labeling-comparison-corpus-2026-06-02.md
  - nishio-experiment-result-storage-question-2026-06-02.md
  - experiment-result-storage-policy-2026-06-02.md
  - cli-pipeline-experiment-roadmap-2026-06-02.md
  - llm-grouping-experiment-output-2026-05-25.md
  - llm-grouping-experiment.md
  - label-quality-redesign-reset-2026-05-30.md
  - label-quality-rubric-evaluation-2026-05-29.md
  - label-refinement-judge-bundle-2026-05-25.md
  - pipeline-step-addition-framing-2026-05-27.md
---

## 結論

品質 judge 改善の前に、まず **clustering tree と labelling output の比較コーパス** を作るべきである。今のまま judge criteria を詰めても、何を入力 tree として見ているのか、どの labelling process が出した label なのか、どの失敗を人間が本当に問題視しているのかが曖昧すぎる。[[nishio-clustering-labeling-comparison-corpus-2026-06-02]]より

したがって、前回の [[cli-pipeline-experiment-roadmap-2026-06-02]] の順序は、次のように 0 番を追加して補正する。

0. **比較コーパス / 実験台帳を作る**: dataset、clustering tree、labelling process、label output、人間メモを蓄積する
1. **その corpus 上で judge / evidence contract を較正する**
2. **tree を固定して labelling process を比較する**
3. **labelling process を固定して clustering method / params を比較する**
4. **価値が見えた view / artifact だけを Web UI へ昇格判断する**

ここで重要なのは、`clustering method` と `labelling process` を混ぜて winner を決めないこと。LLM grouping 実験でも、geometry と label semantics は別軸で評価すべきだと分かっており、cluster 平均 judge と label set direct judge も winner が割れていた。[[llm-grouping-experiment-output-2026-05-25]]より

2026-06-02 の追加整理で、さらに実験の読み方も分ける必要があると分かった。既存 artifact から作る comparison corpus は探索には有用だが、current `main` から一度に多くの要素を変えている場合、採用判断の因果根拠にはならない。採用判断に使う clean experiment は、baseline から `factor_under_test` を 1 つだけ変える。[[one-factor-experiment-principle-2026-06-02]]より

## なぜ judge 先行では足りないか

現状の judge 改善は、評価対象が曖昧なままになりやすい。

- tree が違う: `K=8`、`K=20`、`[8,40]`、LLM grouping では、同じ dataset でも親子構造と cluster size が違う
- label process が違う: merge label、setwise refinement、contrast、balanced、KJ prompt などが混在する
- evidence が違う: random sample、all args、representative args、children label だけ、などが混在する
- judge 粒度が違う: cluster 単位平均と label set 全体比較で判断が割れる

この状態で rubric を細かくしても、「judge が何を見て何に勝たせたのか」が不明なままになる。rubric は単体の採点表としてではなく、比較コーパス上で **人間が見た失敗を検出できるか** を試す道具として育てるべきである。[[label-quality-rubric-evaluation-2026-05-29]]より

## 保存する単位

比較可能にするには、最低限 4 層を分けて保存する。

保存場所そのものは [[experiment-result-storage-policy-2026-06-02]] に従う。つまり `work/kouchou-ai/.../outputs/` は一時実行物、`raw/experiments/<experiment_id>/` は gitignored な一次 artifact snapshot、公開 wiki は manifest / summary / 判断のみを持つ。比較コーパスの `datasets.jsonl` / `tree_runs.jsonl` / `labelling_runs.jsonl` / `human_observations.jsonl` / `judge_runs.jsonl` は、まず `raw/experiments/<experiment_id>/` 側に置く。公開 wiki には、その中から公開可能な要約だけを source / analysis として filing back する。[[experiment-result-storage-policy-2026-06-02]]より

### 1. Dataset Run

同じ入力かどうかを固定する層。

- `dataset_id`
- raw comments / extracted arguments の hash
- argument count
- extraction prompt / model / provider
- embeddings hash
- upstream reuse source

### 2. Tree Run

clustering method が作った tree を固定する層。

- `tree_run_id`
- clustering method: `hierarchical_default`, `llm_grouping`, `pairwise_spectral`, `bertopic_like` など
- params: `cluster_nums`, `K`, seed, UMAP params, affinity params
- tree artifact: normalized tree JSON or `hierarchical_clusters.csv`
- assignment artifact
- tree summary: top-level count、leaf count、cluster size distribution、singleton count、max depth
- visualization compatibility: scatter / hierarchy / treemap / mandalart など

ここでは label の良し悪しを混ぜない。まず「この method はどんな tree を作ったか」だけを見る。

### 3. Labelling Run

tree を入力として label / description を作る層。

- `labelling_run_id`
- `tree_run_id`
- process: `merge_labelling`, `all_args_labelling`, `representative_args_labelling`, `setwise_refine`, `contrast`, `balanced`, `kj_prompt` など
- model / provider / prompt version
- evidence policy: random 10 / random 30 / all args / representative artifact / children labels only
- output labels: cluster label / description / label set
- token / latency / cost

ここでは tree を固定できるので、「同じ tree で label process だけを変える」比較ができる。

### 4. Human Observation / Judge Run

評価はさらに後段に分ける。

- `human_observation_id`: 人間が見た違和感、良い点、落ちた軸、重複 pair
- `judge_run_id`: judge prompt / rubric version / evidence input / score
- judge が human observation を拾えたか
- judge が過剰に問題視した false positive

judge 改善の主タスクは、score を上げることではなく、human observation と judge result のズレを減らすことになる。

## 比較の切り方

最初の比較は、変数を 1 つだけ動かす。これは「実験を小さくする」ためだけではなく、結果の解釈を守るためである。複数要素を同時に変えた run は exploratory として残してよいが、採用判断には使わない。[[nishio-one-factor-experiment-principle-2026-06-02]]より

| 比較 | 固定するもの | 動かすもの | 見ること |
|---|---|---|---|
| labelling process 比較 | dataset + tree | labelling process | 同じ tree で label がどう変わるか |
| clustering tree 比較 | dataset + labelling process | clustering method / params | tree 構造の違いが label set にどう出るか |
| evidence policy 比較 | dataset + tree + label prompt | random / all / representative | 欠落や unsupported axis が減るか |
| judge 較正 | comparison bundle | rubric / judge model | 人間が見た失敗を拾えるか |

この分解により、`LLM grouping が良い`、`hierarchical が良い`、`balanced が良い` のような粗い結論ではなく、「粗い俯瞰 tree では読みやすいが、細粒度 tree では sibling distinction が落ちる」のような実装に戻せる判断になる。

### 探索 corpus と clean experiment

comparison corpus は、次の clean experiment を設計するための探索 material でもある。既存 artifact を集めた retrospective corpus では、tree、labelling、evidence、judge が同時に変わっていることがある。その場合は、`experiment_class=exploratory` として、failure mode と評価軸を見つける用途に限定する。採用判断へ進む時は、`factor_under_test`、`fixed_inputs`、`changed_inputs` を明示し、1 要素だけを変えた run を作る。[[one-factor-experiment-principle-2026-06-02]]より

## 既存実験からの移行

既存の [[llm-grouping-experiment-output-2026-05-25]] は、この比較コーパスの原型として使える。2026-06-02 には、実際に以下を `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` へ移行した。[[llm-grouping-400-tree-label-corpus-2026-06-02]]より

- `LLM grouping K=8`
- `hierarchical K=8`
- `hierarchical K=20`
- `hierarchical [8,40]`
- `[8,40] refine_none / setwise / short / contrast / balanced`

ただしこの corpus は retrospective / exploratory として読む。複数要素が混ざっているため、「どの方式を採用するか」の直接根拠ではなく、次に `tree_run` 固定の labelling process 比較、または label output 固定の judge rubric 比較へ切り直すための材料である。[[one-factor-experiment-principle-2026-06-02]]より

[[label-refinement-judge-bundle-2026-05-25]] も、judge bundle としては有用だが、今後は `tree_run_id` / `labelling_run_id` / `evidence_policy` を明示して、どの条件の label set なのかを追える形にする必要がある。

## CLI 実装に落とすなら

最初は pipeline 本体に入れず、CLI / experiments の周辺 script でよい。

```text
raw/experiments/<experiment_id>/
  manifest.json
  datasets.jsonl
  tree_runs.jsonl
  labelling_runs.jsonl
  human_observations.jsonl
  judge_runs.jsonl
  artifacts/
  bundles/
    llm_grouping_400_tree_label_matrix.md
    llm_grouping_400_tree_label_matrix.html
```

CLI の first slice は次の 3 つに絞る。

1. 既存 outputs から `tree_run` / `labelling_run` metadata を抽出する
2. top-level tree + labels を横並びにした Markdown / HTML bundle を生成する
3. 人間が bundle に観察メモを追記できる形式を作る

これで、judge 改善は「bundle 上の人間観察をどれだけ拾えるか」という具体的な仕事になる。

2026-06-02 の `codex/experiment-storage` first slice では、このうち 1 を CLI option として実装した。`--experiment-root` / `--experiment-id` を指定すると、既存 output から `datasets.jsonl`、`tree_runs.jsonl`、`labelling_runs.jsonl` と artifact copy を作る。2 の tree-label comparison bundle と 3 の human observation 追記は次の slice として残る。[[codex-log-experiment-archive-cli-2026-06-02]]より

続けて、既存 LLM grouping 400 件実験を `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` へ移し、5 tree run / 10 labelling run / 5 judge run / 4 observation を 1 corpus にまとめた。`bundles/tree_label_matrix.md` / `.html` には、run summary、top-level labels、`[8,40]` refinement matrix、judge summary、human observation slots を入れた。[[llm-grouping-400-tree-label-corpus-2026-06-02]]より

## Open Questions

- normalized tree artifact は既存 CSV から都度生成するだけでよいか、保存すべきか。
- tree の違いをどう表現するか。cluster size distribution / parent-child structure / representative examples / label set のどれを first view に置くか。
- human observation は Markdown comment で十分か、JSONL として structured に残すべきか。
- comparison corpus は [[experiment-result-storage-policy-2026-06-02]] の 3 層方針で始めるとして、複数人共有が必要になった時に Google Drive / GitHub release artifact / 別 repo のどれへ移すか。
- `#881` ラベル品質 tracking issue は、この comparison corpus 作成を first slice に差し替えるべきか。
- `factor_under_test` の語彙は自由記述で始めるか、`tree_generation` / `labelling_process` / `evidence_policy` / `judge_rubric` などに固定するか。

## Updates

- 2026-06-02: [[one-factor-experiment-principle-2026-06-02]] を追加。既存 corpus は exploratory として扱い、採用判断用の clean experiment では `factor_under_test` を 1 つだけ変える原則を追記した。
- 2026-06-02: [[llm-grouping-400-tree-label-corpus-2026-06-02]] を追加。既存 LLM grouping 400 件実験を 1 dataset / 5 tree run / 10 labelling run / 5 judge run / 4 observation の比較コーパスへ移し、tree-label matrix bundle を作成した。
- 2026-06-02: [[codex-log-experiment-archive-cli-2026-06-02]] を追加。比較コーパスの first slice として、`analysis-core` CLI から dataset / tree / labelling JSONL と artifact copy を生成できる topic branch `codex/experiment-storage` を作成した。
- 2026-06-02: [[experiment-result-storage-policy-2026-06-02]] を追加し、比較コーパスの保存先を `raw/experiments/<experiment_id>/` に寄せ、公開 wiki には manifest / summary / 判断だけを置く方針へ補正した。
- 2026-06-02: 初版作成。nishio の「各種 clustering method の tree と、その tree を入力にした各種 labelling process の label を蓄積・比較する方が先。judge 改善には現状が曖昧すぎる」という指摘を受け、[[cli-pipeline-experiment-roadmap-2026-06-02]] の前段として比較コーパス / 実験台帳を置く方針に補正した。
