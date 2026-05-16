---
name: source-code
summary: kouchou-ai リポジトリのソースコード本体 — docs だけでは見えない実装ギャップを取るための一次参照
type: source
url: https://github.com/digitaldemocracy2030/kouchou-ai
sources:
  - init.txt
---

## What it is

[[github-dev-docs]] が指すのと同じリポジトリだが、こちらは **コード本体** を一次ソースとして扱う宣言ページ。docs と meeting minutes が「こうなる予定」と語ることと、main の実装の間には継続的なギャップがあり、コードを読まないと判別できないことが多い。

snapshot は `raw/kouchou-ai-snapshot/` に保存（gitignored）。作業用 clone の正位置は `work/kouchou-ai/`。一時的な検証 clone は `/tmp/kouchou-ai/` に置くこともある。

## このソースで判明した重要事実（2026-05 snapshot, tip `3809a7a`）

- **パイプライン本体は既に `packages/analysis-core/` に移動済み**。`apps/api/broadlistening/pipeline/hierarchical_main.py` は `DeprecationWarning` を出す shim
- **`PluginRegistry` という名前のクラスが 2 つ存在** — `apps/api/src/plugins/registry.py` (input) と `packages/analysis-core/src/analysis_core/plugin/registry.py` (analysis)。互換性なし
- **CLI は `kouchou-analyze` ／ `python -m analysis_core`**（[[cli]] 参照）。API サーバは subprocess でこれを呼ぶ
- **Plugin dispatch は実装済みだが production パスで未使用** — `orchestrator.run_workflow()` は dormant、`orchestrator.run()` がレガシーループを直接実行
- **`--without-html`, `--skip-interaction` フラグに argparse バグ**（`store_true` + `default=True` で False に戻せない）
- **PR #825 は main 未マージ**（tip は #821）

詳細は [[refactoring-status]]。

## 読むべき key ファイル

- `packages/analysis-core/pyproject.toml` — パッケージ定義、entry point
- `packages/analysis-core/src/analysis_core/__main__.py` — CLI
- `packages/analysis-core/src/analysis_core/orchestrator.py` — `run()` / `run_workflow()`
- `packages/analysis-core/src/analysis_core/plugin/{interface,registry,decorator,loader}.py` — analysis plugin 機構
- `packages/analysis-core/src/analysis_core/plugins/builtin/` — 8 つの builtin plugin
- `apps/api/src/plugins/{base,registry,youtube}.py` — input plugin 機構（別系統）
- `apps/api/src/services/report_launcher.py` — subprocess で CLI を呼ぶ層
- `docs/refactoring/{phase0_investigation,phase2_5_plan,phase3_plan,naming_convention}.md` — リファクタの計画と現状

## Updates

- 2026-05-17: 初回 ingest（リファクタ／plugin／CLI／pip 化のコードリーディング）
- 2026-05-17: AI コーディングエージェント向けの作業用 clone 置き場を `work/kouchou-ai/` に統一
