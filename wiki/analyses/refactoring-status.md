---
name: refactoring-status
summary: v5 リファクタの実装状況 — Phase 0〜3a は概ね着地、Phase 3b は dormant、Phase 8 (旧コード削除) は未完
type: analysis
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - source-code.md
  - pr-825-standalone-html-observation-2026-05-19.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
---

[[meeting-minutes]] では「v5.0 plugin 化は別リポジトリで開発」「2026-06 リリース目標」と語られていたが、実コードを読むと **既に大部分が main にマージされている**。docs と実装の乖離を整理する。

2026-05-20 時点では、[[usage-modes]] に合わせて次の 3 軸でも読む。

- **Web UI** — `admin` / `api` / `public-viewer` / 配信・共有の改善
- **CLI / analysis-core** — `analysis-core` / PyPI / 中間成果物 / sidecar HTML の改善
- **共通基盤** — 両モードで共有するパイプライン、plugin 基盤、provider、旧コード削除

## 出典

- `docs/refactoring/phase0_investigation.md`
- `docs/refactoring/phase2_5_plan.md`
- `docs/refactoring/phase3_plan.md`
- `docs/refactoring/naming_convention.md`
- 実コード（main, tip `b4d4bcf`、2026-05-20 12:02 JST 時点）— [[source-code]]

## Phase 別の状況

### 読み方

- **Phase 1 / 2 / 3a / 3b / 8** は主に **共通基盤** の話
- **Phase 2.5** は主に **CLI / analysis-core** の話
- `packages/ui-shared/` や frontend plugin のような周辺論点は **Web UI** に寄る

### Phase 1 — ディレクトリ再構成 ✅ 完了

`server/`, `client/`, `client-admin/`, `client-static-build/` → `apps/api/`, `apps/public-viewer/`, `apps/admin/`, `apps/static-site-builder/` への移行は **済**。`naming_convention.md` 末尾 `2026-01-19` に「Migration: 完了」とある。

### Phase 2 — パイプラインを `packages/analysis-core` に移動 ✅ 完了

8 ステップすべてが `packages/analysis-core/src/analysis_core/steps/` に存在。`apps/api/broadlistening/pipeline/steps/` にも同名ファイルが残っているが、これらは **deprecated layer**。

### Phase 2.5 — PyPI パッケージ化 ✅ ほぼ完了

利用モード: **CLI / analysis-core**

- `kouchou-ai-analysis-core` (version `0.1.2`) として PyPI 公開
- `[project.scripts] kouchou-analyze = "analysis_core.__main__:main"` で CLI 配信
- API サーバはこの CLI を **subprocess** で呼ぶ ([[cli]])
- `analysis-core-v*` tag push 起点の `.github/workflows/publish-analysis-core.yml` があり、`ruff` / `pytest` / `build` 通過後に PyPI publish する自動 release 経路も入った

**未完**：

- Task 2.5.6（torch / sklearn を `[clustering]`, `[embeddings]` extras に分割）→ 全部 `dependencies` のまま
- Web/API 経路は current `apps/api/src/services/report_launcher.py` で `python -m analysis_core ... --without-html` を固定しており、CLI 既定の self-contained `report.html` を活かしていない

### Phase 3a — plugin インフラ ✅ 完了

利用モード: **共通基盤**

`packages/analysis-core/src/analysis_core/plugin/` に：

- `interface.py`（`AnalysisStepPlugin` ABC、`PluginMetadata`）
- `registry.py`（`PluginRegistry`）
- `decorator.py`（`@step_plugin`）
- `loader.py`（YAML manifest ベースの外部ロード）

`packages/analysis-core/src/analysis_core/plugins/builtin/` に 8 つの builtin plugin が居り、既存ステップ関数を薄くラップしている。

### Phase 3b — workflow engine ⚠️ 実装あるが dormant

利用モード: **共通基盤**

- `orchestrator.run_workflow()` は実装済み（plugin dispatch 経由）
- `WorkflowEngine` / `workflows/hierarchical_default.py` / `tests/test_workflow_engine.py` まで揃っている
- ただし [[cli|CLI]] (`analysis_core.__main__`) と API サーバ (`report_launcher.py`) はどちらも `.run()`（レガシーの `run_step` ループ）を呼ぶ
- `packages/analysis-core/README.md` や integration tests は branch 上で workflow default path に追随し始めたが、e2e tests や一部 docs にはなお legacy mode 前提が残る
- current tree では、初期 `comments` artifact の注入、status 永続化、`without_html`/`without-html` 正規化、visualization artifact 契約に未吸収の差があり、default 化 blocker は [[workflow-defaultization-blockers]] に整理した
- → **plugin システムは production パスに乗っていない**

ただし open PR `#840` はこの dormant 状態を崩しに行く実装として進んでおり、2026-05-20 時点で少なくとも次が branch 上にある。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

- 初期 `comments` artifact 注入
- workflow path での `hierarchical_status.json` 永続化
- `from_dict()` からの `previous` / rerun plan 読み込み
- 既存成果物 (`args.csv`, `embeddings.pkl`, `hierarchical_result.json`, `report.html`) の artifact 再利用
- `analysis_core.__main__` からの default 実行経路を `run_workflow()` 側へ寄せる変更
- `apps/api/src/services/report_launcher.py` の command 共通化

= **main ではなお dormant / open PR では CLI default path まで workflow 側へ寄せつつある** と書くのが current state に近い。

### Phase 8 — 旧コード削除 ⚠️ 部分的

利用モード: **共通基盤**

`apps/api/broadlistening/pipeline/hierarchical_main.py` 冒頭：

```python
warnings.warn("hierarchical_main.py is deprecated. "
              "Use 'python -m analysis_core' instead.",
              DeprecationWarning, stacklevel=2)
```

= **DeprecationWarning は出すが動く**。同様に `hierarchical_utils.py` も shim 化。

ただし `steps/` 配下の旧コード約 1600 LOC は残存していて、`hierarchical_main.py` 経由で実行すれば旧パスが動く。誰かが古い手順書で `python hierarchical_main.py` すると **黙ってステイル版が動く**。さらに current `apps/api/broadlistening/README.md` もなお「FastAPI サーバーは `hierarchical_main.py` を起点に実行する」と説明しており、docs drift が残っている。

## docs / 議事メモにあるが実装に存在しないもの

### Web UI 寄り

- `packages/ui-shared/` — Phase 0 投資計画と naming convention に記載があるが未作成
- 可視化 plugin の **Python 系統** — `why-plugin-system.md` で 3 軸目として言及されるがバックエンド側に実装なし。代わりに `apps/public-viewer/components/charts/plugins/` の **TypeScript 側 registry/types/validation と built-in plugin** は既に存在する

### CLI / analysis-core 寄り

- 外部 `plugins/analysis/` ディレクトリ — `loader.discover_plugin_directories()` は `Path.cwd()/plugins/analysis` を探すが、リポジトリにこのパスは無く、外部 analysis plugin の同梱もゼロ
- `CHANGELOG.md` — リポジトリルートに無し（履歴は git log のみ）
- YAML ベース workflow 定義 — loader は YAML manifest を読むが、実態は Python の `workflows/hierarchical_default.py` のみ
- `apps/api` からの subprocess 起動は current でも `--without-html` を固定しており、CLI 既定の `report.html` 出力と挙動が分かれている

## PR #825「Python 直接 静的 HTML 出力」(議事メモ 2026-05-18 見出し)

利用モード: **CLI / analysis-core**（ただし Web UI との境界論点を持つ）

2026-05-19 時点では `PR #825` は merge 済みで、`analysis-core` CLI は自己完結型 `report.html` を既定生成できる。  
ただしこれは **CLI / coding agent 向け sidecar 出力** であり、Web プロダクトの主経路を置き換えたわけではない。current `public-viewer` はなお `/reports/{slug}` から `hierarchical_result.json` を fetch して描画し、`report_sync.py` も `report.html` を保持対象に含めない。したがって「静的 HTML 出力の実装」は入ったが、「プロダクトの配信経路として採用された」とまでは言えない。

## 「別リポジトリでリファクタする」の方針との整合

[[meeting-minutes]] 2025-10-08 では「今のコードがあちこち動かなくなるので、リポジトリ自体を複製して開発する」と [[nishio]] が言っていた。実際には **main ブランチ上で Phase 単位の段階移行** を行い、旧コードに DeprecationWarning を貼って共存させる方式が採られている。別リポジトリ手法は採用されなかった。

## 含意

- **「v5 はまだ別世界」というメンタルモデルは正しくない**。`packages/analysis-core/` のコードは既に canonical。新規 PR は基本こちらに投げる
- 一方、**plugin 化は dormant** — 既存ステップを書き換える時、plugin wrapper も同時に直すべきか、wrapper は最終的に削除される予定なのか、要確認
- `analysis-core` 自体の配布はほぼ着地したが、**CLI の canonical 挙動** と **Web/API が固定している挙動** はまだ揃っていない
- 旧 `apps/api/broadlistening/pipeline/` には触らない（deprecated）。バグ報告で旧パスのトレースを見たら「`hierarchical_main.py` で実行している」を疑う

利用モードの観点で言い換えると：

- **Web UI の変更** か **CLI / analysis-core の変更** かを先に切り分けた方が、PR や docs の読み違いが減る
- その上で、plugin 基盤・workflow engine・旧コード削除のような話を **共通基盤** として追うと、`open-decisions` や `gotchas` と対応が取りやすい

## Open Questions

- Phase 3b (`run_workflow()`) を default にする計画／タイミング（具体的 blocker は [[workflow-defaultization-blockers]]）
- 旧 `apps/api/broadlistening/pipeline/steps/` 完全削除のタイミング
- Web/API でも `report.html` を生成・保存対象に寄せるのか、それとも CLI sidecar に留めるのか
- `--skip-interaction` の argparse バグ修正 ([[cli]])
- 依存分割（Task 2.5.6）

これらを含む全プロジェクトの未着地論点は [[open-decisions]] に分類整理。

## Updates

- 2026-05-17: 初回作成（コードリーディング結果から）
- 2026-05-17: `main@3809a7a` を再確認し、可視化 plugin は「フロント側は実装済み、Python 側は未実装」と表現を精密化
- 2026-05-20: [[usage-modes]] に合わせ、各 Phase / 周辺論点 / `PR #825` を Web UI / CLI / 共通基盤のどこに効く話か読めるよう補助線を追加
- 2026-05-20: `main@b4d4bcf` を再確認し、Phase 2.5 の自動 PyPI release 導入済み、Phase 3b の dormant 継続、Phase 8 の docs drift、`apps/api` の `--without-html` 固定を反映
- 2026-05-20: open PR [[pr-840-workflow-defaultization-observation-2026-05-20]] を反映し、Phase 3b は main では dormant だが PR 上では初期 artifact / status / rerun 再利用まで前進していると追記
- 2026-05-20: 同 PR の追加 commit を反映し、branch 上では CLI default path 切替と API launcher command 共通化まで進んだと追記
