---
name: refactoring-status
summary: v5 リファクタの実装状況 — Phase 0〜3a 着地、Phase 3b は dormant、Phase 8 (旧コード削除) は未完
type: analysis
sources:
  - github-dev-docs.md
  - meeting-minutes.md
---

[[meeting-minutes]] では「v5.0 plugin 化は別リポジトリで開発」「2026-06 リリース目標」と語られていたが、実コードを読むと **既に大部分が main にマージされている**。docs と実装の乖離を整理する。

## 出典

- `docs/refactoring/phase0_investigation.md`
- `docs/refactoring/phase2_5_plan.md`
- `docs/refactoring/phase3_plan.md`
- `docs/refactoring/naming_convention.md`
- 実コード（main, tip `3809a7a`、2026-05 時点）— [[source-code]]

## Phase 別の状況

### Phase 1 — ディレクトリ再構成 ✅ 完了

`server/`, `client/`, `client-admin/`, `client-static-build/` → `apps/api/`, `apps/public-viewer/`, `apps/admin/`, `apps/static-site-builder/` への移行は **済**。`naming_convention.md` 末尾 `2026-01-19` に「Migration: 完了」とある。

### Phase 2 — パイプラインを `packages/analysis-core` に移動 ✅ 完了

8 ステップすべてが `packages/analysis-core/src/analysis_core/steps/` に存在。`apps/api/broadlistening/pipeline/steps/` にも同名ファイルが残っているが、これらは **deprecated layer**。

### Phase 2.5 — PyPI パッケージ化 ✅ ほぼ完了

- `kouchou-ai-analysis-core` (version `0.1.0`) として PyPI 公開
- `[project.scripts] kouchou-analyze = "analysis_core.__main__:main"` で CLI 配信
- API サーバはこの CLI を **subprocess** で呼ぶ ([[cli]])

**未完**：

- Task 2.5.6（torch / sklearn を `[clustering]`, `[embeddings]` extras に分割）→ 全部 `dependencies` のまま
- 自動 PyPI リリース GitHub Action → workflow ファイル無し、手動リリース運用

### Phase 3a — plugin インフラ ✅ 完了

`packages/analysis-core/src/analysis_core/plugin/` に：

- `interface.py`（`AnalysisStepPlugin` ABC、`PluginMetadata`）
- `registry.py`（`PluginRegistry`）
- `decorator.py`（`@step_plugin`）
- `loader.py`（YAML manifest ベースの外部ロード）

`packages/analysis-core/src/analysis_core/plugins/builtin/` に 8 つの builtin plugin が居り、既存ステップ関数を薄くラップしている。

### Phase 3b — workflow engine ⚠️ 実装あるが dormant

- `orchestrator.run_workflow()` は実装済み（plugin dispatch 経由）
- ただし [[cli|CLI]] と API サーバはどちらも `.run()`（レガシーの `run_step` ループ）を呼ぶ
- → **plugin システムは production パスに乗っていない**

### Phase 8 — 旧コード削除 ⚠️ 部分的

`apps/api/broadlistening/pipeline/hierarchical_main.py` 冒頭：

```python
warnings.warn("hierarchical_main.py is deprecated. "
              "Use 'python -m analysis_core' instead.",
              DeprecationWarning, stacklevel=2)
```

= **DeprecationWarning は出すが動く**。同様に `hierarchical_utils.py` も shim 化。

ただし `steps/` 配下の旧コード約 1600 LOC は残存していて、`hierarchical_main.py` 経由で実行すれば旧パスが動く。誰かが古い手順書で `python hierarchical_main.py` すると **黙ってステイル版が動く**。

## docs / 議事メモにあるが実装に存在しないもの

- 外部 `plugins/analysis/` ディレクトリ — `loader.discover_plugin_directories()` は `Path.cwd()/plugins/analysis` を探すが、リポジトリにこのパスは無く、外部 analysis plugin の同梱もゼロ
- `packages/ui-shared/` — Phase 0 投資計画と naming convention に記載があるが未作成
- `CHANGELOG.md` — リポジトリルートに無し（履歴は git log のみ）
- YAML ベース workflow 定義 — loader は YAML manifest を読むが、実態は Python の `workflows/hierarchical_default.py` のみ
- 可視化 plugin の **Python 系統** — `why-plugin-system.md` で 3 軸目として言及されるがバックエンド側に実装なし。代わりに `apps/public-viewer/components/charts/plugins/` の **TypeScript 側 registry/types/validation と built-in plugin** は既に存在する

## PR #825「Python 直接 静的 HTML 出力」(議事メモ 2026-05-18 見出し)

[[meeting-minutes]] では着地したかのように語られているが、**main の tip は #821**（2026-05 中旬時点）。`82d870f test: 静的HTML出力（GitHub Pages等）のE2Eテスト` は別件（static-site-builder の E2E テスト）。PR #825 は未マージ／別ブランチの可能性。

## 「別リポジトリでリファクタする」の方針との整合

[[meeting-minutes]] 2025-10-08 では「今のコードがあちこち動かなくなるので、リポジトリ自体を複製して開発する」と [[nishio]] が言っていた。実際には **main ブランチ上で Phase 単位の段階移行** を行い、旧コードに DeprecationWarning を貼って共存させる方式が採られている。別リポジトリ手法は採用されなかった。

## 含意

- **「v5 はまだ別世界」というメンタルモデルは正しくない**。`packages/analysis-core/` のコードは既に canonical。新規 PR は基本こちらに投げる
- 一方、**plugin 化は dormant** — 既存ステップを書き換える時、plugin wrapper も同時に直すべきか、wrapper は最終的に削除される予定なのか、要確認
- 旧 `apps/api/broadlistening/pipeline/` には触らない（deprecated）。バグ報告で旧パスのトレースを見たら「`hierarchical_main.py` で実行している」を疑う

## Open Questions

- Phase 3b (`run_workflow()`) を default にする計画／タイミング
- 旧 `apps/api/broadlistening/pipeline/steps/` 完全削除のタイミング
- `--without-html` / `--skip-interaction` の argparse バグ修正 ([[cli]])
- 依存分割（Task 2.5.6）と自動 PyPI リリース

これらを含む全プロジェクトの未着地論点は [[open-decisions]] に分類整理。

## Updates

- 2026-05-17: 初回作成（コードリーディング結果から）
- 2026-05-17: `main@3809a7a` を再確認し、可視化 plugin は「フロント側は実装済み、Python 側は未実装」と表現を精密化
