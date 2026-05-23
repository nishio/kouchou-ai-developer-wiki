---
name: refactoring-status
summary: "v5 リファクタの実装状況 — Phase 0〜8 の主要移行は main で完了し、残るのは package 配布・status semantics・周辺 docs の follow-up"
type: analysis
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - source-code.md
  - pr-825-standalone-html-observation-2026-05-19.md
  - report-html-non-web-canonical-decision-2026-05-23.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
---

[[meeting-minutes]] では「v5.0 plugin 化は別リポジトリで開発」「2026-06 リリース目標」と語られていたが、実コードを読むと **既に大部分が main にマージされている**。docs と実装の乖離を整理する。

2026-05-24 時点では、[[usage-modes]] に合わせて次の 3 軸でも読む。

- **Web UI** — `admin` / `api` / `public-viewer` / 配信・共有の改善
- **CLI / analysis-core** — `analysis-core` / PyPI / 中間成果物 / 観察用HTML の改善
- **共通基盤** — 両モードで共有するパイプライン、plugin 基盤、provider、旧コード削除

## 出典

- `docs/refactoring/naming_convention.md`
- 実コード（main, tip `e5ed743`、2026-05-24 確認）— [[source-code]]
- workflow default 化直前の branch 観測 — [[pr-840-workflow-defaultization-observation-2026-05-20]]

## Phase 別の状況

### 読み方

- **Phase 1 / 2 / 3a / 3b / 8** は主に **共通基盤** の話
- **Phase 2.5** は主に **CLI / analysis-core** の話
- `packages/ui-shared/` や frontend plugin のような周辺論点は **Web UI** に寄る

### Phase 1 — ディレクトリ再構成 ✅ 完了

`server/`, `client/`, `client-admin/`, `client-static-build/` → `apps/api/`, `apps/public-viewer/`, `apps/admin/`, `apps/static-site-builder/` への移行は **済**。`naming_convention.md` 末尾 `2026-01-19` に「Migration: 完了」とある。

### Phase 2 — パイプラインを `packages/analysis-core` に移動 ✅ 完了

8 ステップすべてが `packages/analysis-core/src/analysis_core/steps/` に存在する。2026-05-23 の legacy cleanup merge 後、`apps/api/broadlistening/pipeline/` には Python 実装は残っておらず、`configs/` と `inputs/` の runtime data だけが残る。つまり **コードとしての canonical path 移行は完了** と読んでよい。[[source-code]]より

### Phase 2.5 — PyPI パッケージ化 ✅ ほぼ完了

利用モード: **CLI / analysis-core**

- `kouchou-ai-analysis-core` (version `0.1.2`) として PyPI 公開
- `[project.scripts] kouchou-analyze = "analysis_core.__main__:main"` で CLI 配信
- API サーバはこの CLI を **subprocess** で呼ぶ ([[cli]])
- `analysis-core-v*` tag push 起点の `.github/workflows/publish-analysis-core.yml` があり、`ruff` / `pytest` / `build` 通過後に PyPI publish する自動 release 経路も入った
- `main@5d591ef` では filesystem-based usage の quickstart 整備と `--validate-config` / `--validate-input` / `--dry-run` preflight が入り、CLI 初回利用時の fail-fast も main に反映済み

**未完**：

- Web/API 経路は current `apps/api/src/services/report_launcher.py` で `python -m analysis_core ... --without-html` を固定している。ただしこれは「CLI 既定に未追随な半端状態」というより、**Web は JSON + `public-viewer`、CLI は self-contained `report.html` を観察用に持つ** という artifact 契約の意図的分岐と読んだ方が正確である（[[usage-modes]], [[cli]], [[analysis-core-and-web-ui]]）
- release hardening は別途残る。Trusted Publishing、`apps/api` 互換を含む release gate、package metadata の詰めは [[open-decisions]] の follow-up として読む方が近い

### Phase 3a — plugin インフラ ✅ 完了

利用モード: **共通基盤**

`packages/analysis-core/src/analysis_core/plugin/` に：

- `interface.py`（`AnalysisStepPlugin` ABC、`PluginMetadata`）
- `registry.py`（`PluginRegistry`）
- `decorator.py`（`@step_plugin`）
- `loader.py`（YAML manifest ベースの外部ロード）

`packages/analysis-core/src/analysis_core/plugins/builtin/` に 8 つの builtin plugin が居り、既存ステップ関数を薄くラップしている。

### Phase 3b — workflow engine ✅ 完了

利用モード: **共通基盤**

- `PipelineOrchestrator.run_default()` は current `main` で `run_workflow()` を呼ぶ。つまり CLI / API の canonical path は workflow 側に寄った
- `WorkflowEngine` / `workflows/hierarchical_default.py` / `tests/test_workflow_engine.py` に加え、CLI `main()` の rerun plan / status carry-forward、API `report_launcher` の full generation / config rerun / aggregation rerun / duplicate reuse 経路まで service-level test が main に入った
- duplicate/reuse 相当の実ファイル群を置いた状態から `from_config()` が missing downstream artifact だけ rerun する integration test、real workflow rerun e2e、workflow failure step status API も main に存在する
- `packages/analysis-core/README.md` と `apps/api/broadlistening/README.md` も canonical path を `run_default()` → `run_workflow()` 前提へ更新済み
- したがって workflow engine は「実装があるだけ」の段階を抜け、**CLI / API の production 入口として実用互換に達した** と読んでよい

残る論点は、[[hierarchical-status-semantics]] で整理した `duration` / `estimated_cost` / progress semantics のような許容差分と、plugin wrapper の整理、release hardening である。Phase 3b 完了条件の整理は [[phase3b-exit-criteria]] を参照。

### Phase 8 — 旧コード削除 ✅ 完了

利用モード: **共通基盤**

- `apps/api/broadlistening/pipeline/steps/`
- `apps/api/broadlistening/pipeline/hierarchical_main.py`
- `apps/api/broadlistening/pipeline/hierarchical_utils.py`
- 旧 `services/` と、それに紐づく source tree 上の stale refactoring phase docs

は current `main@e5ed743` で source tree から除去された。これにより、以前の未完根拠だった **「古い手順書どおり `python hierarchical_main.py` すると黙って旧パスが動く」** 状態は current tree から消えた。runtime data としての `configs/` / `inputs/`、後方互換としての `analysis_core.compat.*` は残るが、これは legacy 実行経路の存続とは別である。[[source-code]]より

## docs / 議事メモにあるが実装に存在しないもの

### Web UI 寄り

- `packages/ui-shared/` — Phase 0 投資計画と naming convention に記載があるが未作成
- 可視化 plugin の **Python 系統** — `why-plugin-system.md` で 3 軸目として言及されるがバックエンド側に実装なし。代わりに `apps/public-viewer/components/charts/plugins/` の **TypeScript 側 registry/types/validation と built-in plugin** は既に存在する

### CLI / analysis-core 寄り

- 外部 `plugins/analysis/` ディレクトリ — `loader.discover_plugin_directories()` は `Path.cwd()/plugins/analysis` を探すが、リポジトリにこのパスは無く、外部 analysis plugin の同梱もゼロ
- `CHANGELOG.md` — リポジトリルートに無し（履歴は git log のみ）
- YAML ベース workflow 定義 — loader は YAML manifest を読むが、実態は Python の `workflows/hierarchical_default.py` のみ
- `docs/refactoring/phase0_investigation.md` / `phase2_5_plan.md` / `phase3_plan.md` — current source tree には存在しない。履歴として読むなら wiki 側の観測ページや本ページの `## Updates` を参照
- `apps/api` からの subprocess 起動は current `main` でも `--without-html` を固定しており、CLI の `report.html` 既定出力とは役割分担が分かれている。この差分は現状では docs で明示して読ませるべきで、直ちに統一すべき未整合とは限らない

## PR #825「Python 直接 静的 HTML 出力」(議事メモ 2026-05-18 見出し)

利用モード: **CLI / analysis-core**（ただし Web UI との境界論点を持つ）

2026-05-19 時点では `PR #825` は merge 済みで、`analysis-core` CLI は自己完結型 `report.html` を既定生成できる。  
ただしこれは **CLI / coding agent 向け観察用HTML出力** であり、Web プロダクトの主経路を置き換えたわけではない。current `public-viewer` はなお `/reports/{slug}` から `hierarchical_result.json` を fetch して描画し、`report_sync.py` も `report.html` を保持対象に含めない。したがって「静的 HTML 出力の実装」は入ったが、「プロダクトの配信経路として採用された」とまでは言えない。
2026-05-23 の maintainer 判断でも、この分離は維持される。`report.html` を Web canonical に昇格させる前提ではなく、CLI 向け観察用HTMLとして扱う方針で読む。[[report-html-non-web-canonical-decision-2026-05-23]]より

## 完了判定

2026-05-24 の current judgment では、**refactoring は done と言ってよい**。

ここでいう done は、

- canonical path が `analysis-core` / workflow 側へ移った
- API がその core を subprocess で呼ぶ形に揃った
- 旧 `apps/api/broadlistening/pipeline/` 実装が source tree から除去された

までを含む。逆に、以下は残っていても refactoring 未完の根拠とはしない。

- `hierarchical_status.json` の semantics 調整
- package metadata / release hardening
- 外部 plugin 利用例や YAML workflow のような拡張余地

## 「別リポジトリでリファクタする」の方針との整合

[[meeting-minutes]] 2025-10-08 では「今のコードがあちこち動かなくなるので、リポジトリ自体を複製して開発する」と [[nishio]] が言っていた。実際には **main ブランチ上で Phase 単位の段階移行** を行い、旧コードに DeprecationWarning を貼って共存させる方式が採られていたが、その legacy 共存期間も current `main` では終わった。別リポジトリ手法は採用されなかった。

## 含意

- **「v5 はまだ別世界」というメンタルモデルは正しくない**。`packages/analysis-core/` のコードは既に canonical。新規 PR は基本こちらに投げる
- 一方、plugin wrapper の多くはなお legacy step の薄いラッパーであり、どこまで workflow-native 実装へ寄せるかは別論点として残る
- `analysis-core` 自体の配布はほぼ着地したが、**CLI** と **Web/API** は同じコアを使いながら、生成・保持・配信する artifact 契約を意図的に分けている。新しい読者が「なぜ API は `--without-html` 固定なのか」で迷わないよう、docs 側で明示しておく価値が高い
- current tree では旧 Python 実装自体が無い。古い runbook やブログ記事に `hierarchical_main.py` が出てきたら、**2026-05-23 以前の履歴** とみなして読む方が安全

利用モードの観点で言い換えると：

- **Web UI の変更** か **CLI / analysis-core の変更** かを先に切り分けた方が、PR や docs の読み違いが減る
- その上で、plugin 基盤・workflow engine・旧コード削除のような話を **共通基盤** として追うと、`open-decisions` や `gotchas` と対応が取りやすい

## Open Questions

- `hierarchical_status.json` のどこまでを legacy 完全互換に寄せるべきか（現状整理は [[hierarchical-status-semantics]]）
- `--skip-interaction` の argparse バグ修正 ([[cli]])

workflow default 化を止めていた実装差分と、その後どこまで解消されたかの履歴は [[workflow-defaultization-blockers]] を参照。

これらを含む全プロジェクトの未着地論点は [[open-decisions]] に分類整理。

## Updates

- 2026-05-24: `work/kouchou-ai/main@e5ed743` を確認し、legacy cleanup merge 後の current state に合わせて Phase 8 を「完了」へ更新。source tree から旧 pipeline 実装と refactoring phase docs が除去されたため、refactoring 全体も done 判定へ補正
- 2026-05-17: 初回作成（コードリーディング結果から）
- 2026-05-23: maintainer 判断 [[report-html-non-web-canonical-decision-2026-05-23]] を反映し、`report.html` の Web canonical 化を Open Questions から外した
- 2026-05-17: `main@3809a7a` を再確認し、可視化 plugin は「フロント側は実装済み、Python 側は未実装」と表現を精密化
- 2026-05-20: [[usage-modes]] に合わせ、各 Phase / 周辺論点 / `PR #825` を Web UI / CLI / 共通基盤のどこに効く話か読めるよう補助線を追加
- 2026-05-20: `main@b4d4bcf` を再確認し、Phase 2.5 の自動 PyPI release 導入済み、Phase 3b の dormant 継続、Phase 8 の docs drift、`apps/api` の `--without-html` 固定を反映
- 2026-05-20: open PR [[pr-840-workflow-defaultization-observation-2026-05-20]] を反映し、Phase 3b は main では dormant だが PR 上では初期 artifact / status / rerun 再利用まで前進していると追記
- 2026-05-20: 同 PR の追加 commit を反映し、branch 上では CLI default path 切替と API launcher command 共通化まで進んだと追記
- 2026-05-20: さらに CLI rerun plan test、API `report_launcher` の full generation / aggregation rerun service-level test まで進んだことを反映し、Phase 3b の説明を current state に合わせて更新
- 2026-05-20: さらに failure semantics、config rerun、duplicate/reuse 経路、`from_config()` rerun plan integration の確認まで進んだことを反映し、残課題を docs と実データ寄り e2e 中心に寄せて更新
- 2026-05-21: real workflow rerun e2e と workflow failure step status API の確認まで反映し、Phase 3b の remaining work を「実データバリエーションの厚み」と docs 側にさらに絞って更新
- 2026-05-21: 「branch 上では実装的にかなり切り替わっているが、main の canonical state と運用宣言はまだ別」という読み分けを追記
- 2026-05-21: `hierarchical_status.json` の項目別 semantics 棚卸しページ [[hierarchical-status-semantics]] への導線を追加
- 2026-05-21: Phase 3b の完了条件を議論しやすくするため、[[phase3b-exit-criteria]] への導線を追加
- 2026-05-21: `main@0e1552d` を再確認し、PR #840 相当が merged された前提で Phase 3b を「完了」へ更新。残課題を Phase 8 / extras 分割 / status semantics 許容差分へ寄せ直した
- 2026-05-21: CLI の `report.html` 既定出力と API の `--without-html` 固定は「未整合」より「利用モード別の意図的分岐」と読めるよう表現を補正し、[[usage-modes]] / [[cli]] への導線を強めた
- 2026-05-21: `main@42d2afb` で PR #843 merge を確認し、Task 2.5.6（extras 分割）を未完リストから除外
- 2026-05-21: `main@5d591ef` で PR #844 merge を確認し、Phase 2.5 に CLI preflight / filesystem-based quickstart が main へ入ったことを追記
