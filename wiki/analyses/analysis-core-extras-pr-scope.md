---
title: "analysis-core extras 分割PRの範囲"
type: analysis
summary: "`analysis-core` の extras 分割（Task 2.5.6）を独立 PR で切るための事前検討。依存定義だけでなく eager import・テスト・インストール導線を同時に整える必要があるとし、2026-05-21 merge の PR #843 で extras 導入・遅延 import・docs 更新として実装された"
sources:
  - source-code.md
  - github-dev-docs.md
---

# Task 2.5.6 は独立 PR にできるか

> この検討は 2026-05-21 merge の PR [#843](https://github.com/digitaldemocracy2030/kouchou-ai/issues/843)「analysis-core の optional dependency を extras に分離」で実装済み。「依存関係」節までは実装前（`main@0e1552d`）の検討で、実装後のことは下の「実装後の状態」節を参照。

結論から言うと、**できる**。ただし「`pyproject.toml` で `torch` / `scikit-learn` を optional-dependencies に移すだけ」の小修正ではなく、`analysis-core` package の import 契約と install 導線まで含めた **独立した package 整備 PR** として切るのが妥当である。`packages/analysis-core` が主対象で、Phase 3b や Phase 8 と実装的に強く結合していない。[[source-code]]より

## なぜ独立 PR にできるか

- Task 2.5.6 の未完箇所は `packages/analysis-core/pyproject.toml` とその周辺 docs / CI に局在していた。workflow engine や API rerun semantics のような大きい論点とは別軸。[[source-code]]より
- `apps/api` は `analysis-core` を subprocess で呼ぶが、依存分割そのものは package 配布境界の話であり、API 側の機能改修と一緒にしなくてよい。必要なのは install profile の明示である。[[source-code]]より
- `docs/refactoring/phase2_5_plan.md` でも extras 分割は Task 2.5.6 として単独項目で切られていた（このファイルは PR [#865](https://github.com/digitaldemocracy2030/kouchou-ai/issues/865) で削除済み）。[[github-dev-docs]]より

## 独立 PR にする時の最小スコープ

1. `packages/analysis-core/pyproject.toml` で `embeddings` / `clustering` extras を導入する
2. base install で壊れないよう、optional dependency を要求する import を lazy 化する
3. `README` / quickstart / release docs の install コマンドを extras 前提へ更新する
4. `requirements.lock` / `requirements-dev.lock` と package CI を新しい依存構成に合わせる

## ここを直さないと壊れる（実装前の状態）

### 1. `steps/__init__.py` が clustering 依存を eager import していた

`analysis_core.steps.__init__` は import 時に `hierarchical_clustering` を無条件 import していた。当時の `hierarchical_clustering.py` は module load 時点で `scipy` と `sklearn` を import するため、extras 化して base install から外すと **`from analysis_core.steps import extraction` だけでも失敗しうる** 状態だった。[[source-code]]より

### 2. test suite が「全部入っている」前提だった

`packages/analysis-core/tests/test_imports.py` は全 step import 成功を前提にしていた。extras 導入後もこのままなら、base profile と full profile のどちらを保証したいのかが曖昧になる。`base install では optional step は helpful error を返す` か、`CI は full extras 前提で回す` かを決めてテストを分ける必要があった。[[source-code]]より

### 3. install 導線が素の `pip install kouchou-ai-analysis-core` だった

`packages/analysis-core/README.md`、`docs/user-guide/cli-quickstart.md`、`docs/user-guide/import-quickstart.md` などは、当時は extras なし install を案内していた。extras 化後にそのままだと、CLI 利用者が clustering/embedding 実行時に初めて落ちる。少なくとも「標準利用は `full`」なのか「軽量 install を正規化する」のかを docs で明示する必要があった。[[source-code]]より [[github-dev-docs]]より

## 実務上の推奨PR形

- PR タイトル例: `Split analysis-core optional dependencies into extras`
- 対象はまず `packages/analysis-core/` とその package docs / workflow に限定する
- `apps/api` 側は、必要なら install comment や Docker build 手順の明文化だけに留める
- 動作保証は `base import`, `full install`, `embedding step`, `clustering step` の 4 点を見る

## 依存関係

この PR は **独立して出せるが、完全に孤立ではない**。意味的には [[refactoring-status]] の「Phase 2.5 残課題」を 1 つ減らす PR であり、PyPI 配布導線との関係は [[pypi-auto-release-requirements]] と合わせて見るとよい。[[source-code]]より

## 実装後の状態

PR [#843](https://github.com/digitaldemocracy2030/kouchou-ai/issues/843) は 2026-05-21 に merge された。中身は次のとおり。[[github-dev-docs]]より [[source-code]]より

- **extras**: `embeddings`（`sentence-transformers` / `torch`）、`clustering`（`scikit-learn` / `scipy` / `umap-learn` / `numba`）、`full`（`gemini` + `embeddings` + `clustering`）を追加し、これらを base 依存から外した。`gemini` extra はそれ以前からある。`openai` は base 依存に残した
- **遅延 import**: `analysis_core.steps` は `__getattr__` で、`PipelineOrchestrator` は step を解決する時点で、step module を初めて使うときに import する。clustering の依存（`_load_clustering_dependencies()`）と local embedding の `sentence_transformers` も使う時点で読み込み、無ければ install コマンドつきの `RuntimeError` を出す
- **install 導線**: README・cli-quickstart・import-quickstart は `pip install 'kouchou-ai-analysis-core[embeddings,clustering]'` を標準にし、Gemini を使う場合は `[gemini,embeddings,clustering]` を案内する。extras なしの base install でも `import analysis_core` や dry-run はできる、と明記した
- **テスト**: lock を作り直し、`test_imports.py` に「`analysis_core.steps` の import や `PipelineOrchestrator` の生成だけでは clustering の module を import しない」ことを確かめるテストを足した

「ここを直さないと壊れる」のうち、1（eager import）と 3（install 導線）は解消した。2（テスト）は次の形に落ち着いた。

- analysis-core の CI（`.github/workflows/analysis-core-ci.yml`。[#843](https://github.com/digitaldemocracy2030/kouchou-ai/issues/843) では変更していない）は `requirements-dev.lock`（all-features）を入れ、full 構成のまま回る
- base install で import できることは、`sys.modules` を見る上記のテストで守る。base install だけで回す CI ジョブは無い

一方、[#843](https://github.com/digitaldemocracy2030/kouchou-ai/issues/843) は API の Dockerfile を変えておらず、API イメージは analysis-core を extras なしで入れていた。CI は all-features の lock で回るので気づかれず、2026-06-05 にレポート生成が clustering 依存の不足で失敗する報告（Issue [#894](https://github.com/digitaldemocracy2030/kouchou-ai/issues/894)）が出た。同日の PR [#895](https://github.com/digitaldemocracy2030/kouchou-ai/issues/895) で Dockerfile を `[full]` に直し、PR [#896](https://github.com/digitaldemocracy2030/kouchou-ai/issues/896) で Dockerfile が `[full]` を入れることのテストと、イメージ内で import を確かめる smoke CI を足した。上の推奨 PR 形は `apps/api` 側を「install comment や Docker build 手順の明文化」に留めるとしていたが、実際には API イメージの install 行も extras 化の影響範囲だった。[[github-dev-docs]]より

## Open Questions

- `openai` も extras に分けるか、それとも current path どおり base dependency に残すか → [#843](https://github.com/digitaldemocracy2030/kouchou-ai/issues/843) では base 依存に残した
- `full` を README の既定 install にするか、軽量 base install を前面に出すか → README の標準は `[embeddings,clustering]`。`full` は API の Docker イメージが使う
- optional dependency 不足時の UX を `ImportError` のままにするか、step 実行時に説明的なエラーへ包むか → install コマンドつきの `RuntimeError` に包んだ
- base install（extras なし）で import と dry-run が通ることを、単体テストだけでなく CI のジョブとしても確かめるか（2026-10-21 時点では `sys.modules` を見る単体テストだけ）

## Updates

- 2026-05-21: `main@0e1552d` を確認し、Task 2.5.6 は独立 PR で切れるが eager import / CI / docs 更新を同梱すべきと整理
- 2026-10-21: main と照合し、PR [#843](https://github.com/digitaldemocracy2030/kouchou-ai/issues/843) で実装された内容と、その後の API Docker の修正（[#894](https://github.com/digitaldemocracy2030/kouchou-ai/issues/894) / [#895](https://github.com/digitaldemocracy2030/kouchou-ai/issues/895) / [#896](https://github.com/digitaldemocracy2030/kouchou-ai/issues/896)）を追記。実装前の状態を述べた箇所を過去形にし、Open Questions の決着と削除済みの phase2_5_plan.md を注記
