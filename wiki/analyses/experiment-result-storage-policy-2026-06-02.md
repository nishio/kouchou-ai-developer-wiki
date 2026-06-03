---
type: analysis
summary: "実験結果の保存先を 3 層に分ける方針。`work/kouchou-ai/.../outputs/` は一時実行物、`raw/experiments/<experiment_id>/` は gitignored な一次 artifact snapshot、公開 wiki は manifest / summary / 判断だけを持つ。採用判断用実験では `factor_under_test` も記録する"
sources:
  - nishio-blind-human-label-presentation-context-2026-06-02.md
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - nishio-human-pairwise-label-preference-before-judge-2026-06-02.md
  - one-factor-experiment-principle-2026-06-02.md
  - nishio-one-factor-experiment-principle-2026-06-02.md
  - codex-log-experiment-archive-cli-2026-06-02.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
  - nishio-experiment-result-storage-question-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - cli-pipeline-experiment-roadmap-2026-06-02.md
  - remaining-experiment-artifacts-snapshot-2026-05-29.md
  - weekly-log-2026-05-20.md
  - source-code.md
---

## 結論

実験結果の蓄積先は、**一時実行物 / 一次 artifact snapshot / 公開 wiki** の 3 層に分ける。

| 層 | 置き場所 | 役割 | git |
|---|---|---|---|
| scratch output | `work/kouchou-ai*/packages/analysis-core/outputs/` | CLI 実行直後の生成物。再実行・目視・デバッグ用 | gitignored、長期保存扱いしない |
| raw experiment snapshot | `raw/experiments/<experiment_id>/` | 後で比較・再評価するための一次 artifact 固定場所 | gitignored、immutable 扱い |
| public wiki index / interpretation | `wiki/sources/` / `wiki/analyses/` | 人間と AI が辿る manifest、要約、設計判断 | git tracked |

これで、`work/` に残った出力を「保存したつもり」になる事故を避けつつ、公開 wiki に巨大な raw output やユーザ由来データを載せないで済む。[[nishio-experiment-result-storage-question-2026-06-02]]より

## なぜ 3 層に分けるか

`work/kouchou-ai/.../outputs/` は、実験の実行場所としては自然だが、長期保存場所ではない。branch / worktree を切り替えたり、別の実験を走らせたり、cleanup したりすると失われる。実際、過去の remaining experiment artifacts は branch snapshot に退避したが、長期保存するなら `raw/` または別 repo / release artifact へ切り出すべきという open question が残っていた。[[remaining-experiment-artifacts-snapshot-2026-05-29]]より

2026-05-26 の `#2_開発_広聴ai_アルゴリズム開発` でも、生成されたデータを永続化して後から確認できるようにするには、実験を本体 output だけでなく別 repo / 別保存場所で扱う必要がある、という気づきが出ていた。[[weekly-log-2026-05-20]]より

一方、公開 wiki はナレッジベースであり、raw output storage ではない。`hierarchical_result.json`、embeddings、全コメント、judge の full response をそのまま入れると、量も秘匿境界も破綻する。公開 wiki に置くのは、artifact の manifest、軽量 summary、比較表、判断だけにする。

したがって、実験 artifact の一次保管は `raw/experiments/` に寄せる。`raw/` はこの repo の schema 上も生ソース置き場であり、gitignored なので、重い output や公開境界が怪しいものを置きやすい。ただし gitignored なので、共有が必要な artifact は別途 Google Drive / release artifact / 別 repo を検討し、wiki には pointer と hash だけを置く。

## Directory Convention

実験ごとに `experiment_id` を付け、`raw/experiments/<experiment_id>/` を作る。

命名例:

```text
raw/experiments/
  2026-06-02-llm-grouping-400-tree-label-corpus/
    README.md
    manifest.json
    datasets.jsonl
    tree_runs.jsonl
    labelling_runs.jsonl
    human_preferences.jsonl
    human_observations.jsonl
    judge_runs.jsonl
    artifacts/
      tree_hierarchical_8_40/
      labels_hierarchical_8_40_refine_none/
      labels_hierarchical_8_40_refine_balanced/
    bundles/
      tree_label_matrix.md
      tree_label_matrix.html
```

`README.md` は local raw artifact の入口で、公開 wiki に載せる前の詳細メモを置いてよい。`manifest.json` は機械可読な索引で、最低限次を持つ。

```json
{
  "experiment_id": "2026-06-02-llm-grouping-400-tree-label-corpus",
  "created_at": "2026-06-02T20:02:00+09:00",
  "source_repo": "digitaldemocracy2030/kouchou-ai",
  "source_commit": "3c5d1f026757",
  "dataset_ids": ["llm_grouping_sample_comments_400"],
  "public_summary": "wiki/sources/llm-grouping-400-tree-label-corpus-2026-06-02.md",
  "artifact_policy": "raw-local-gitignored",
  "contains_user_data": false,
  "share_location": null
}
```

採用判断に使う experiment では、保存先だけでなく実験設計も manifest に残す。複数要素を変えた探索 run なのか、current `main` baseline から 1 要素だけ変えた clean experiment なのかを後から読めるようにする。[[one-factor-experiment-principle-2026-06-02]]より

```json
{
  "experiment_class": "clean",
  "baseline_experiment_id": "main-2026-06-02-hierarchical-8-40",
  "factor_under_test": "labelling_process",
  "fixed_inputs": ["dataset", "extracted_arguments", "embeddings", "tree_run", "model", "evidence_policy"],
  "changed_inputs": ["labelling_prompt"],
  "comparison_question": "同じ tree と evidence で label quality が改善するか",
  "adoption_decision_allowed": true
}
```

## What Goes Where

### `work/`: 実行直後の output

ここにはその場で出た output を置く。消えてもよいものとして扱う。

- `outputs/<run_id>/hierarchical_clusters.csv`
- `outputs/<run_id>/hierarchical_merge_labels.csv`
- `outputs/<run_id>/hierarchical_result.json`
- `outputs/<run_id>/label_quality_*.json`
- temporary HTML / report

保存したいと判断したら、必要な artifact だけ `raw/experiments/<experiment_id>/artifacts/` へコピーし、manifest に `source_output_path` と hash を残す。

### `raw/experiments/`: 一次 artifact snapshot

ここには「後で比較に使うもの」を固定する。

- tree run artifact
- labelling run artifact
- judge run artifact
- generated comparison bundle
- human preference の blind A/B winner / tie / confidence / reason tags / presentation context
- human observation の元メモ
- prompt / config / model / commit / token / cost metadata

原則 immutable とし、修正したくなったら `experiment_id` を分けるか、`manifest.json` に `supersedes` / `superseded_by` を書く。

### `wiki/sources/`: 公開可能な source summary

ここには raw artifact の full dump ではなく、公開可能な要約を置く。

- experiment_id
- 何を比較したか
- 参照 commit / dataset / run id
- raw artifact が local `raw/experiments/...` にあること
- 主要な結果表
- 公開してよい代表 label / cluster summary
- 注意点、未解決論点

ユーザ由来データ、secret、実環境 URL、巨大 JSON、embeddings は載せない。

### `wiki/analyses/`: 判断と次の一手

ここには「その結果から何を判断したか」を置く。

- どの tree / labelling process がどの用途に向くか
- judge が拾えなかった人間 observation
- 次の PR / issue slice
- Web UI に昇格するか、CLI 実験に留めるか

## Public Boundary

公開 wiki に載せてよいのは、設計判断と公開可能な軽量 summary までである。

- OK: cluster 数、tree shape summary、label text、比較表、hash、run id、公開可能な代表例
- 原則 NG: raw comments 全件、embeddings、full `hierarchical_result.json`、ユーザデータ、secret、実環境 URL、resource 名・サイズ、deploy logs
- 要判断: prompt full text、judge full response、representative arguments

代表例を載せる場合は、公開サンプルデータか、公開許諾済み / 既に公開されている dataset に限定する。実データを含む experiment は `wiki/sources/` には抽象 summary だけを置き、artifact は gitignored raw または権限付き storage に置く。

## First Slice

`#881` 系の最初の実装は、judge 改善ではなく storage convention を具体化するのがよい。

1. `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に既存 LLM grouping 400 件実験の比較 artifact を集める
2. `manifest.json`、`tree_runs.jsonl`、`labelling_runs.jsonl` を手で最小作成する
3. `bundles/tree_label_matrix.md` を作り、人間 preference / observation を書ける欄を置く
4. `wiki/sources/llm-grouping-400-tree-label-corpus-2026-06-02.md` に公開 summary を作る
5. そのうえで judge v1 が human preference を再現できるかを見る

この順にすると、「どこに保存したか」「何を比較したか」「judge が何を見ているか」が同時に固定される。

2026-06-02 の first implementation では、手作業 convention を一歩進め、`analysis-core` CLI に `--experiment-root` / `--experiment-id` を追加する topic branch `codex/experiment-storage` を作成した。1 回の pipeline output から `manifest.json`、`datasets.jsonl`、`tree_runs.jsonl`、`labelling_runs.jsonl`、空の `human_observations.jsonl` / `judge_runs.jsonl`、および `artifacts/` / `bundles/` のコピーを作る。[[codex-log-experiment-archive-cli-2026-06-02]]より

同日、既存 LLM grouping 400 件実験 artifact も `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に台帳化した。これは 1 dataset、5 tree run、10 labelling run、4 human observation、5 judge run を持つ first corpus で、`bundles/tree_label_matrix.md` / `.html` も生成した。[[llm-grouping-400-tree-label-corpus-2026-06-02]]より

## Open Questions

- `raw/experiments/` は local gitignored なので、複数人共有には弱い。共有 artifact は Google Drive / GitHub release artifact / 別 repo のどれに置くか。
- `manifest.json` / `*.jsonl` の schema をどこまで厳密にするか。最初は手書きでよいが、後で script 化する必要がある。
- 公開可能な sample dataset だけは、軽量 artifact を git tracked にするべきか。
- `raw/experiments/` の容量管理をどうするか。古い full artifact をいつ外部 storage へ退避するか。

## Updates

- 2026-06-02: [[nishio-blind-human-label-presentation-context-2026-06-02]] を追加し、`human_preferences.jsonl` には algorithm / process origin を人間に隠したか、A/B 表示順、`presentation_context` も保存する方針を追記した。
- 2026-06-02: [[human-pairwise-label-preference-experiment-2026-06-02]] を追加し、ラベル品質評価では `human_preferences.jsonl` に A/B winner / tie / confidence / reason tags を保存し、judge はその preference を再現できるかで較正する方針を追記した。
- 2026-06-02: [[one-factor-experiment-principle-2026-06-02]] を追加し、採用判断用の clean experiment では `experiment_class` / `baseline_experiment_id` / `factor_under_test` / `fixed_inputs` / `changed_inputs` を manifest に残す方針を追記した。
- 2026-06-02: [[llm-grouping-400-tree-label-corpus-2026-06-02]] を追加。既存 LLM grouping 400 件実験を `raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` に保存し、first corpus と tree-label matrix bundle を作成した。
- 2026-06-02: [[codex-log-experiment-archive-cli-2026-06-02]] を追加。`work/kouchou-ai-experiment-storage` の topic branch `codex/experiment-storage` で、`analysis-core` CLI から `raw/experiments/<experiment_id>/` 形式の最小 archive を生成する first slice を実装した。
- 2026-06-02: 初版作成。nishio の「実験結果をどこにどのように蓄積するかが宙に浮いている」という指摘を受け、`work/` は scratch、`raw/experiments/` は gitignored raw snapshot、`wiki/` は public manifest / summary / analysis という 3 層保存方針を整理した。
- 2026-06-02: `oss_weekly_reporter` の 2026-05-20_to_2026-05-27 週次 dump を確認し、2026-05-26 Slack 上の実験 artifact 永続化の気づきを前段 source として追加
