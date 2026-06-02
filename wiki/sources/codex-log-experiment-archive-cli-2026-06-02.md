---
type: source
summary: "Codex が analysis-core CLI に実験結果アーカイブの first slice を実装した作業ログ。`--experiment-root` / `--experiment-id` で 1 回の pipeline output を `raw/experiments/<experiment_id>/` 形式へ保存する"
sources:
  - source-code.md
  - experiment-result-storage-policy-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
---

## Context

2026-06-02、nishio の「やってみよう、まず何をする？」を受け、judge / view / label 改善ではなく、まず既存 CLI 実行の結果を比較可能な実験台帳へ保存する first slice に着手した。

この作業は [[experiment-result-storage-policy-2026-06-02]] と [[clustering-labeling-comparison-corpus-2026-06-02]] の実装着手である。

実装対象は `work/kouchou-ai-experiment-storage` の topic branch `codex/experiment-storage`。base は `digitaldemocracy2030/kouchou-ai` の `main@3c5d1f0267571edbe045d36775ab2461a0989581`。`work/kouchou-ai/` 本体は main のまま維持した。

## Implemented

- `packages/analysis-core/src/analysis_core/__main__.py` に `--experiment-root`、`--experiment-id`、`--experiment-overwrite` を追加
- `packages/analysis-core/src/analysis_core/experiment_archive.py` を新規追加し、1 回の pipeline output から `manifest.json`、`datasets.jsonl`、`tree_runs.jsonl`、`labelling_runs.jsonl`、空の `human_observations.jsonl` / `judge_runs.jsonl` を生成
- 既存 output の `args.csv`、`relations.csv`、`hierarchical_clusters.csv`、`hierarchical_initial_labels.csv`、`hierarchical_merge_labels.csv`、`hierarchical_result.json`、`hierarchical_status.json` などを `artifacts/` へコピー
- `report.html`、`metadata.json`、`icon.png` など表示 bundle 由来のファイルがあれば `bundles/` へコピー
- `packages/analysis-core/README.md` に `raw/experiments/<experiment-id>/` への保存例を追記

この first slice で保存できるのは、dataset / tree / labelling の最低限の比較索引である。人間 observation と judge run は、同じ実験 ID に後段で追記する前提の空 JSONL として作る。

## Validation

`packages/analysis-core` で以下を実行した。

```bash
PYTHONPATH=src pytest tests/test_experiment_archive.py tests/test_cli.py -q
ruff check src/analysis_core/experiment_archive.py src/analysis_core/__main__.py tests/test_experiment_archive.py tests/test_cli.py
git diff --check
```

結果:

- `13 passed in 7.43s`
- `ruff`: All checks passed
- `git diff --check`: no output

## Open Questions

- この branch を PR 化する時、CLI option 名を `--experiment-root` のままにするか、`--archive-root` / `--experiment-archive-root` のようにするか。
- `human_observations.jsonl` と `judge_runs.jsonl` への追記コマンドを同じ CLI に足すか、別 script にするか。
- 既存 LLM grouping 400 件実験の過去 artifact を、この schema に手動移行するか、まずは新規実行だけを対象にするか。
