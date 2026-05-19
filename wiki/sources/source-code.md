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

この配置は単なる便宜ではなく、**Wiki repo で文脈整理しながら本体 repo の local clone を一次参照する** 運用を前提にしている。全体像は [[wiki-driven-workflow]] を参照。

## Refresh protocol

コード由来のページを更新する前に、まず `work/kouchou-ai/` で `git fetch origin && git pull --ff-only` を実行し、参照した commit を `log.md` または当該ページの `## Updates` に残す。[[deepwiki-kouchou-ai]] や `docs/` は読み筋の補助には使えるが、**実装断定の根拠は local clone** とする。

## このソースで判明した重要事実（2026-05 snapshot, tip `55e93e1`）

- **パイプライン本体は既に `packages/analysis-core/` に移動済み**。`apps/api/broadlistening/pipeline/hierarchical_main.py` は `DeprecationWarning` を出す shim
- **`PluginRegistry` という名前のクラスが 2 つ存在** — `apps/api/src/plugins/registry.py` (input) と `packages/analysis-core/src/analysis_core/plugin/registry.py` (analysis)。互換性なし
- **CLI は `kouchou-analyze` ／ `python -m analysis_core`**（[[cli]] 参照）。API サーバは subprocess でこれを呼ぶ
- **Plugin dispatch は実装済みだが production パスで未使用** — `orchestrator.run_workflow()` は dormant、`orchestrator.run()` がレガシーループを直接実行
- **`--skip-interaction` はなお argparse 上で False に戻せない**。一方 `--without-html` は `PR #825` で default `False` へ修正済み
- **PR #825 は main に merge 済み**。ただし得られる `report.html` は CLI sidecar であり、Web の主経路は依然 `hierarchical_result.json` + `public-viewer`
- **`embeddings.pkl` は元の埋め込みベクトルを保存**。UMAP による 2D 化は `hierarchical_clustering` ステップ側で行う

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
- 2026-05-17: `work/kouchou-ai/` を `git fetch origin` で確認。`main` / tip `3809a7a` は origin と一致
- 2026-05-17: local clone を一次参照、DeepWiki を補助ソースとする refresh protocol を追記
- 2026-05-17: `embeddings.pkl` は元 embedding 保存、UMAP 2D 化は後段というコード上の事実を追記
