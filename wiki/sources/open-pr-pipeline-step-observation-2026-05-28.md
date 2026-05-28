---
type: source
summary: "2026-05-28 時点の open PR 観測。pipeline step 追加判断に直接関係するのは `#866` LLM grouping、`#874` semantic island layout、補助的に `#867` reuse-from で、`#874` は named layout artifact として筋がある一方 CI は未通過"
sources:
  - github-dev-docs.md
  - source-code.md
---

## What it is

2026-05-28 00:08 JST に `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` と `gh pr view` / `gh run view` で確認した open PR の観測。  
直近の「pipeline に step を追加するべきか」論点に関係する PR だけを抜き出す。

## Open PR Summary

2026-05-28 00:08 JST 時点で open PR は 6 本。

| PR | title | relevance |
| --- | --- | --- |
| `#874` | `[codex] semantic island layout 生成を追加` | pipeline step 追加の具体例。`hierarchical_layout_generation` を aggregation と visualization の間に追加 |
| `#873` | `[codex] Azure deploy を直列化して更新競合を避ける` | deploy reliability。step 追加論点とは直接関係しない |
| `#868` | `[codex] 実行時ユーザーAPIキーの受け渡しを直す` | runtime credential plumbing。step 追加論点とは直接関係しない |
| `#867` | `[codex] 既存出力を再利用して再実行できるようにする` | step が増える時の rerun / skip 複雑性を下げる補助 PR |
| `#866` | `[codex] LLM grouping 分析モードを追加` | `analysis_mode=llm_grouping` と workflow branch の具体化 |
| `#863` | `[codex] Windows setup の日本語案内を PowerShell に分離` | Windows setup。step 追加論点とは直接関係しない |

## PR #866: LLM grouping

`#866` は `analysis_mode=llm_grouping` を追加し、`analysis.llm_grouping` plugin / step / spec / workflow を追加する。出力は既存 viewer 互換の `hierarchical_clusters.csv` と `hierarchical_merge_labels.csv`。PR 本文では、散布図互換を保ったまま raw argument を LLM で top-level group に割り当てる **実験用の入口** と明記され、label refinement は含めていない。[[github-dev-docs]]より

観測:

- changed files は `llm_grouping.py`、`llm_grouping_specs.json`、`llm_grouping_compatible.py`、prompt / config / tests など
- checks は Ruff / Pytest / Server Tests / CodeQL / CodeRabbit すべて success
- mergeable だが review required

設計上は、これは「既存 step へ押し込む」のではなく、別 `analysis_mode` / workflow として切る方向であり、[[strategic-development-order-2026-05-23]] の短期互換案と一致する。

## PR #867: reuse-from

`#867` は CLI に `--reuse-from` を追加し、既存 output から中間成果物を seed して、対応する step を `nothing changed` として skip できるようにする。スコープは reuse-from のみで、LLM grouping と label refinement は含めていない。[[github-dev-docs]]より

観測:

- changed files は CLI entry、orchestration、orchestrator、CLI / orchestration tests
- checks は Ruff / Pytest / Server Tests / CodeQL / CodeRabbit すべて success
- mergeable だが review required

設計上は、step 数が増える時の実務的複雑性（rerun / skip / status）を下げる基盤である。`label_refinement` や `layout_generation` のような downstream 実験を安全に回すには、この PR の価値が高い。

## PR #874: semantic island layout generation

`#874` は aggregation と visualization の間に `hierarchical_layout_generation` step を追加する。PR 本文によると、`arguments[].x/y` は既存 embedding 由来座標のまま残し、`hierarchical_result.json.layouts` に名前付き layout を追加する。全 run で `embedding_umap` を生成し、`llm_grouping` 出力では既定で `semantic_island_map` も生成する。[[github-dev-docs]]より

観測:

- changed files は `hierarchical_layout_generation.py`、plugin registration、`hierarchical_specs.json`、`hierarchical_default.py`、`hierarchical_visualization.py`、tests
- workflow では `layout_generation` が `aggregation` と `embedding` に依存し、`visualization` は `aggregation` ではなく `layout_generation` に依存する
- specs では `hierarchical_visualization` の dependency も `hierarchical_layout_generation` へ変わる
- `hierarchical_layout_generation.py` は `result["layouts"]` に `embedding_umap` と必要に応じて `semantic_island_map` を追加し、`default_layout_id` を設定する
- mergeable だが review required

checks:

- CodeQL / Server Tests / CodeRabbit は success
- Ruff は failure。`hierarchical_layout_generation.py` の import formatting と、関数 annotation で `np.ndarray` を使っているが module scope に `np` がない `F821` が原因
- Pytest は failure。`tests/test_orchestration.py` などに `len(specs) == 8` / `len(plan) == 8` / `len(orchestrator.steps) == 8` の固定期待が残り、新 step 追加で 9 になったため落ちている

設計上の評価:

- `arguments[].x/y` を置き換えず、named layout artifact を足すのは後方互換性を守る設計でよい
- これは「分析 artifact」ではなく「表示 artifact」の first-class 化であり、昨日の整理でいう責務分離に当たる
- 一方で default workflow に常時 step を足すため、step 数増加の複雑性は実際に発生している。CI の 8 step 固定失敗はその兆候
- `embedding_umap` を全 run で作る価値と、`semantic_island_map` を `llm_grouping` に限定して作る価値は分けて評価すべき

### 2026-05-28 source code re-check

2026-05-28 に `work/kouchou-ai-mst-visualization-prototype` の PR head `27b3be6` と base `e5ed743` を直接確認した。[[source-code]]より

source code 上も、`#874` は「実験用 layout を任意に有効化する」実装ではなく、「標準パイプラインに step を追加する」実装である。

- `workflows/hierarchical_default.py` は `layout_generation` を常に `steps` に追加し、`visualization` は `layout_generation` に依存する。`include_visualization=False` でも `layout_generation` 自体は残る。[[source-code]]より
- `specs/hierarchical_specs.json` も `hierarchical_layout_generation` を標準 step として追加し、`hierarchical_visualization` の dependency を `hierarchical_aggregation` から `hierarchical_layout_generation` に変更している。[[source-code]]より
- `orchestrator.py` の `DEFAULT_STEPS` に `hierarchical_layout_generation` が入り、workflow step mapping / status mapping にも追加されている。[[source-code]]より
- `compat/config_converter.py` は通常 config に `layout_generation.semantic_island_map` default を追加し、builtin plugin registration も標準 plugin 群に入れている。[[source-code]]より
- tests も `len(plan) == 9`、`len(steps) == 9`、`without_html=True` の rerun plan でも `hierarchical_layout_generation` が run される、という期待に書き換えている。[[source-code]]より

つまり、PR 本文の「追加 layout 層」という説明より、実装は強い。表示用の派生成果物を標準 pipeline contract に昇格させる変更になっている。

手元では次を実行し、PR 内で書き換えられた 9 step 前提の局所テストは通ることを確認した。[[source-code]]より

```console
PYTHONPATH=packages/analysis-core/src .venv-analysis312/bin/pytest \
  packages/analysis-core/tests/test_hierarchical_layout_generation.py \
  packages/analysis-core/tests/test_integration.py::TestPipelineIntegration::test_full_plan_execution \
  packages/analysis-core/tests/test_pipeline_paths_integration.py::TestOrchestratorPathsIntegration::test_from_config_duplicate_style_rerun_only_restarts_missing_downstream_steps \
  -q
```

結果は `4 passed`。これは「9 step 前提にテストを書き換えれば整合する」確認であり、「標準パイプラインを 9 step にしてよい」根拠ではない。なお、手元 venv には `ruff` が入っておらず Ruff は再現できなかったが、GitHub 上の PR checks は引き続き Ruff / Pytest failure を示している。[[github-dev-docs]]より

## Implication

open PR を踏まえると、昨日の結論は少し具体化できる。

- `#866` は、new analysis mode を既存 hierarchical step に押し込まず workflow として切る方向なので妥当
- `#867` は、step 追加による運用複雑性を下げる基盤なので先に入る価値が高い
- `#874` は、named layout artifact を first-class にする意味では筋があるが、source code 上は標準 workflow / specs / orchestrator / tests を 9 step 前提に変えている。現時点では、default workflow に常時 step を足す形ではなく、明示有効化される実験用経路へ戻す方が筋である

## Updates

- 2026-05-28: 初回作成。open PR 6 本のうち、step 追加判断に関係する `#866` / `#867` / `#874` を観測し、特に `#874` の named layout artifact と CI failure を整理した。
- 2026-05-28: PR head `27b3be6` の source code を直接確認し、`#874` が optional 実験ではなく標準 workflow / specs / orchestrator / tests を 9 step 前提へ変える実装であることを追記した。
