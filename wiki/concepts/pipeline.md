---
name: pipeline
summary: 解析パイプライン — extraction → embedding → 階層クラスタリング → ラベリング → 可視化
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - slack-dev-kouchouai-2026-q1.md
---

## 配置（重要：canonical な場所は移動済み）

**2026 時点での canonical 実装は `packages/analysis-core/src/analysis_core/steps/`**。8 ステップすべてここ。

旧 `apps/api/broadlistening/pipeline/` は **deprecation shim**。`hierarchical_main.py` は冒頭で `DeprecationWarning` を出して旧 `steps/` を import する旧パスを残しているが、新規開発は触らない。詳細は [[refactoring-status]]。

- エントリポイント（推奨）: `python -m analysis_core` または `kouchou-analyze`（[[cli]]）
- 旧エントリ: `apps/api/broadlistening/pipeline/hierarchical_main.py`（動くが deprecated）

## ステップ列

1. `extraction` — 生コメントから「意見」を LLM で抽出（コスト最大）
2. `embedding` — 各意見を埋め込みベクトル化
3. `hierarchical_clustering` — 階層クラスタリング（一層目／二層目）
4. `hierarchical_initial_labelling` — 各クラスタに初期ラベル
5. `hierarchical_merge_labelling` — 上位ラベル統合
6. `hierarchical_overview` — 全体サマリ
7. `hierarchical_aggregation` — 集約レポート生成
8. `hierarchical_visualization` — 散布図・ツリーマップ・dense-scatter 出力

## 実行モード

`analysis_core.PipelineOrchestrator` に **2 系統** ある：

- `run()` — 既定。レガシーの `run_step` ループで 8 ステップを順番に呼ぶ。**CLI と API サーバはこれを呼ぶ**
- `run_workflow()` — [[plugin-system]] dispatch 経由。実装済みだが production パスでは未使用（[[refactoring-status]]）

## Jigsaw 系 LLM 分類をどう差し込む想定だったか

[[slack-dev-kouchouai-2026-q1]] 2026-02-11 週では、近い将来の案として **`extraction, embedding` の後に LLM ベースのクラスタリングへ分岐する枝** が語られている。これは理論上の最適形ではなく、まずは **既存のパイプラインや可視化と両立する形で分析切り替え部分を検証する** ための互換性優先案。

同 source 2026-02-25 週では、embedding 後に分岐するのは「実装の楽さ」「後での可視化」のためであり、論理的に embedding が必須なわけではないとも整理されている。  
要するに、**近い枝は `embedding` を足場に使うが、長期的には分類基準そのものを距離空間から分類ツリーへ移す余地がある**。

## 出力物の場所とスキーマ

`{output_base_dir}/{report_id}/` 配下（CLI の `--output-dir` で指定。API サーバは `settings.REPORT_DIR`）：

- `args.csv` — 抽出された意見一覧（kebab-case 列：`arg-id`, `comment-id` 等）
- `embeddings.pkl` — **元の埋め込みベクトル**（UMAP 後 2D ではない）
- `hierarchical_clusters.csv` — クラスタ階層
- `hierarchical_result.json` — viewer が読む統合結果
- `final_result_with_comments.csv` — `config.is_pubcom=true` のとき出力。**この CSV だけ snake_case** (`arg_id`, `category_id`) — 他は kebab-case ([[gotchas]])

詳細スキーマは `docs/development/plugin-output-data-structures.md`。

## 主要な hidden assumption と落とし穴

- **Slack では `embeddings.pkl` が UMAP 後 2D と誤認された形跡がある** ([[slack-dev-kouchouai-2025-q4]]) が、`main@3809a7a` のコードでは `embedding` ステップが元の埋め込みベクトルを `embeddings.pkl` に保存し、`hierarchical_clustering` ステップがそれを読んでから UMAP で 2D に落としている（[[source-code]]）
- **`comment-id` の自動採番が経路依存**: Web CSV アップロードとスプレッドシート取り込みは自動生成するが、CLI／プラグイン／直接 CSV ではプラグイン側で `comment-id` を出す責任がある
- **`propertyMap`** (`hierarchical_result.json`): `args.csv` に対応する列がないと `hierarchical_aggregation` が落ちる
- **CSV 列名の case 不一致**: `is_pubcom=true` 経路だけ snake_case
- **E2E パイプラインテストは課金**: gpt-4o-mini で約 $0.01/run。`pyproject.toml` の `norecursedirs = ["tests/e2e"]` で既定 `pytest` から除外、CI でも実行されない

## クラスタ数のデフォルト問題

[[meeting-minutes]] 2026-05-18 見出しで再浮上：`docs/user-guide/cli-quickstart.md` の例が `[3, 6]`。これを Claude Code がそのまま使い、300 件規模のデータでも `3 → 6 → 12 → 24` のような粗いまとめになる。提案された方向は「クラスタ数を optional にし、データ件数からおすすめ値を自動算出」(cube-root rule の言及あり)。

過去にも [[other-contributors|kitaro]] が silhouette-score ベースの自動選択を PR #567 で実装したが embedding エラーの誘発で #579 で revert。**未解決**。

## なぜ UMAP→クラスタリングなのか（既知の理論的弱点）

[[meeting-minutes]] 2025-10-08: 研究的には HDBSCAN を高次元で直接掛けるほうが精度が高いと知られているが、人間が高次元を見られない以上、散布図の可読性とのトレードオフで現状の構成を維持。代替を試したい場合は [[plugin-system|解析 plugin]] として実装する方針。

## 軽量化と CLI 静的出力（2026-05）

[[meeting-minutes]] 2026-05-18 見出し / PR #825：

- 従来は「サーバを立てて `npm run build`」する必要があったが、AI コーディングエージェントは「サーバ無しで HTML を出して静的ホスト」したい
- Python から直接静的 HTML を吐く実装を追加。デフォルトをこちらにする方針
- 旧サーバ経路との見た目は 100% 同一ではない — 「実験的ビューを試しやすい」副産物がある

## Open Questions

- `extraction.skip: true` オプションの実装（複数回希望されているが未着地、議事メモ 2026-05-18 見出し時点）
- レポート再利用（Issue #19）は 2026-02 に「実装し終わった」報告あり、現状確認が必要
- 散布図の維持／削除：「散布図を見て満足する時代ではない」(ken-san, 2025-10-01) vs 「見た目のインパクトを求める顧客がいる」(nishio)。未決
- Jigsaw 系 LLM 分類を `embedding` 後の互換枝として入れるのか、`embedding` 自体を省く独立 workflow にするのか

## Updates

- 2026-05-17: 初回作成
- 2026-05-17: `#2_開発_広聴ai` ログ由来の Jigsaw 系 LLM 分類導入意図を追記
- 2026-05-17: `embeddings.pkl` を UMAP 後 2D とする記述を撤回し、Slack 発言と `main@3809a7a` のコード実装を分離
