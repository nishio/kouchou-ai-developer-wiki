---
name: source-code
summary: "kouchou-ai リポジトリのソースコード本体 — docs だけでは見えない実装ギャップを取るための一次参照"
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

## このソースで判明した重要事実（2026-05-24 snapshot, main tip `e5ed743`）

- **パイプライン本体は既に `packages/analysis-core/` に移動済み**。`apps/api/broadlistening/pipeline/` に旧 Python 実装は残っておらず、`configs/` / `inputs/` が runtime data として残る
- **`PluginRegistry` という名前のクラスが 2 つ存在** — `apps/api/src/plugins/registry.py` (input) と `packages/analysis-core/src/analysis_core/plugin/registry.py` (analysis)。互換性なし
- **CLI は `kouchou-analyze` ／ `python -m analysis_core`**（[[cli]] 参照）。API サーバは subprocess でこれを呼ぶ
- **`PipelineOrchestrator.run_default()` が canonical** — current `main` では `run_default()` が `run_workflow()` を呼び、`run()` は deprecated direct-step fallback
- **`--skip-interaction` はなお argparse 上で False に戻せない**。一方 `--without-html` は `PR #825` で default `False` へ修正済み
- **PR #825 は main に merge 済み**。ただし得られる `report.html` は CLI 向け観察用HTMLであり、Web の主経路は依然 `hierarchical_result.json` + `public-viewer`
- **source tree 上の refactoring phase docs は整理済み** — `docs/refactoring/phase0_investigation.md` / `phase2_5_plan.md` / `phase3_plan.md` は current tree から除去され、履歴は wiki 側で管理する前提になった
- **`embeddings.pkl` は元の埋め込みベクトルを保存**。UMAP による 2D 化は `hierarchical_clustering` ステップ側で行う

詳細は [[refactoring-status]]。

## 読むべき key ファイル

- `packages/analysis-core/pyproject.toml` — パッケージ定義、entry point
- `packages/analysis-core/src/analysis_core/__main__.py` — CLI
- `packages/analysis-core/src/analysis_core/orchestrator.py` — `run_default()` / `run()` / `run_workflow()`
- `packages/analysis-core/src/analysis_core/plugin/{interface,registry,decorator,loader}.py` — analysis plugin 機構
- `packages/analysis-core/src/analysis_core/plugins/builtin/` — 8 つの builtin plugin
- `apps/api/src/plugins/{base,registry,youtube}.py` — input plugin 機構（別系統）
- `apps/api/src/services/report_launcher.py` — subprocess で CLI を呼ぶ層
- `docs/refactoring/naming_convention.md` — source tree に残る refactoring 由来ドキュメント

## `#221` 系で読んだ current facts (2026-05-29, main tip `0c294da`)

- `apps/admin/app/create/page.tsx` は CSV / spreadsheet / plugin 入力を送信前に `comments` へ組み立て、`comments.length < clusterLv2` の時だけ `window.confirm` で続行確認している
- `apps/admin/app/create/components/EnvironmentCheckDialog/` と `apps/api/src/routers/admin_report.py` の `/admin/environment/verify` で API 接続チェックは実装済み。OpenAI / Gemini などに軽い chat request を投げ、認証エラー、残高不足、rate limit を分類する
- `apps/admin/app/create/parseCsv.ts` は `chardet` / `iconv-lite` / `papaparse` を使い、`apps/admin/app/create/utils/columnScorer.ts` はコメント列を推定する
- `apps/admin/app/create/hooks/useClusterSettings.ts` はコメント数から推奨クラスタ数を自動設定する
- `apps/api/src/services/llm_pricing.py` と ReportCard 側の `TokenUsage` は実行後の token usage / estimated cost 表示を支えているが、作成前見積もりにはまだ使われていない
- `apps/admin/app/_components/ReportCard/DuplicateReportDialog/`、`apps/admin/app/reuse/[slug]/page.tsx`、`apps/api/src/services/report_duplicate.py`、`docs/user-guide/reuse-report.md` により、レポート再利用と中間成果物 reuse は current main に入っている

## ラベル入力 sampling / UI 表示の current facts (2026-05-30, main tip `0c294da`)

- 管理画面/API 経由の通常レポート作成では、`apps/api/src/services/report_launcher.py` が `hierarchical_initial_labelling.sampling_num = 30` と `hierarchical_merge_labelling.sampling_num = 30` を設定する
- analysis-core の config 変換 / builtin plugin default では、initial / merge とも `sampling_num` default は `10`
- 実際の抽出方法は、initial が `cluster_data.sample(n=sampling_num)`、merge が `current_cluster_data.sample(n=sampling_num)` で、どちらも seed なしの Polars random sample。最大被覆 / FPS / k-medoids / label coverage ではない
- `hierarchical_aggregation` は `hierarchical_result.json` に全 arguments をそのまま入れる。ここで representative arguments は選んでいない
- public-viewer の `HierarchyListChart` は deepest-level cluster だけ `argumentList.filter(arg.cluster_ids.includes(cluster.id))` で argument を持たせ、展開時に `maxDisplay=10` の default で `argumentsList.slice(0, maxDisplay)` を表示する。順序は `hierarchical_result.json` の `arguments` 配列順で、ラベル適合度やクラスタ中心性による代表例選定ではない

## hierarchical_clustering の current baseline (2026-06-30, main tip `d5c9ece6e3b3`)

`packages/analysis-core/src/analysis_core/steps/hierarchical_clustering.py` では、`embeddings.pkl` から元 embedding を読み、`UMAP(n_components=2, n_neighbors=n_neighbors)` で 2D 座標 `umap_embeds` を作る。その `umap_embeds` を `hierarchical_clustering_embeddings()` に渡し、最大 cluster 数で `sklearn.cluster.KMeans` を fit する。

階層化は、KMeans の `cluster_centers_` を `scipy.cluster.hierarchy.linkage(..., method="ward")` に掛け、`fcluster(..., criterion="maxclust")` で粗い level の label へ merge する。つまり current main の baseline は、**元 embedding → 2D UMAP → sklearn KMeans → ward merge** である。

この事実は、Spherical K-means / Faiss K-means / 15D〜25D UMAP などの実験を設計する時の baseline として使う。詳細な実験候補は [[spherical-kmeans-experiment-scope-2026-06-30]]。

## Updates

- 2026-06-30: `work/kouchou-ai/main@d5c9ece6e3b3` を確認し、`hierarchical_clustering.py` の current baseline が「元 embedding → 2D UMAP → sklearn KMeans → ward merge」であることを追記
- 2026-06-02: `work/kouchou-ai/main@3c5d1f026757` を再確認し、ラベル付け sampling の前提が残っていることを確認。API 経由は `apps/api/src/services/report_launcher.py` で initial / merge とも `sampling_num=30`、analysis-core built-in plugin と compat config は default `10`。`apps/public-viewer/components/charts/HierarchyListChart.tsx` の個別データ表示も `maxDisplay=10` の配列先頭表示で、representative selection ではない
- 2026-05-30: `work/kouchou-ai/main@0c294da` を確認し、ラベル付け時の sampling が API 経由では最大 30 件、CLI/default では 10 件で、選択は seed なし random sample であること、UI の「個別データ」表示は representative selection ではなく deepest-level cluster の配列先頭 10 件であることを追記
- 2026-05-29: `work/kouchou-ai/main@0c294da` を確認し、`#221` 系の current facts として、作成画面の送信前 `window.confirm`、API 接続チェック、CSV parse / column scoring、推奨クラスタ数、実行後 token/cost 表示、再利用機能の実装状況を追記
- 2026-05-24: `work/kouchou-ai/main@e5ed743` を確認し、legacy pipeline Python 実装と source tree 上の phase docs が除去された current state へ更新
- 2026-05-17: 初回 ingest（リファクタ／plugin／CLI／pip 化のコードリーディング）
- 2026-05-17: AI コーディングエージェント向けの作業用 clone 置き場を `work/kouchou-ai/` に統一
- 2026-05-17: `work/kouchou-ai/` を `git fetch origin` で確認。`main` / tip `3809a7a` は origin と一致
- 2026-05-17: local clone を一次参照、DeepWiki を補助ソースとする refresh protocol を追記
- 2026-05-17: `embeddings.pkl` は元 embedding 保存、UMAP 2D 化は後段というコード上の事実を追記
- 2026-05-20: `work/kouchou-ai/main@b4d4bcf` と open PR `#840` を見比べ、Phase 3b は main では dormant だが branch 上では blocker 解消が進行中と追記
