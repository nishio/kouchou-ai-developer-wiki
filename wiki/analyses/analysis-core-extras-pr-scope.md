---
type: analysis
summary: "`analysis-core` の extras 分割は独立 PR で切り出せるが、依存定義だけでなく eager import・CI・インストール導線を同時に整える必要がある"
sources:
  - source-code.md
  - github-dev-docs.md
---

# Task 2.5.6 は独立 PR にできるか

結論から言うと、**できる**。ただし「`pyproject.toml` で `torch` / `scikit-learn` を optional-dependencies に移すだけ」の小修正ではなく、`analysis-core` package の import 契約と install 導線まで含めた **独立した package 整備 PR** として切るのが妥当である。`packages/analysis-core` が主対象で、Phase 3b や Phase 8 と実装的に強く結合していない。[[source-code]]より

## なぜ独立 PR にできるか

- Task 2.5.6 の未完箇所は `packages/analysis-core/pyproject.toml` とその周辺 docs / CI に局在している。workflow engine や API rerun semantics のような大きい論点とは別軸。[[source-code]]より
- `apps/api` は `analysis-core` を subprocess で呼ぶが、依存分割そのものは package 配布境界の話であり、API 側の機能改修と一緒にしなくてよい。必要なのは install profile の明示である。[[source-code]]より
- `docs/refactoring/phase2_5_plan.md` でも extras 分割は Task 2.5.6 として単独項目で切られている。[[github-dev-docs]]より

## 独立 PR にする時の最小スコープ

1. `packages/analysis-core/pyproject.toml` で `embeddings` / `clustering` extras を導入する
2. base install で壊れないよう、optional dependency を要求する import を lazy 化する
3. `README` / quickstart / release docs の install コマンドを extras 前提へ更新する
4. `requirements.lock` / `requirements-dev.lock` と package CI を新しい依存構成に合わせる

## ここを直さないと壊れる

### 1. `steps/__init__.py` が clustering 依存を eager import している

`analysis_core.steps.__init__` は import 時に `hierarchical_clustering` を無条件 import している。現状の `hierarchical_clustering.py` は module load 時点で `scipy` と `sklearn` を import するため、extras 化して base install から外すと **`from analysis_core.steps import extraction` だけでも失敗しうる**。[[source-code]]より

### 2. test suite が「全部入っている」前提

`packages/analysis-core/tests/test_imports.py` は全 step import 成功を前提にしている。extras 導入後もこのままなら、base profile と full profile のどちらを保証したいのかが曖昧になる。`base install では optional step は helpful error を返す` か、`CI は full extras 前提で回す` かを決めてテストを分ける必要がある。[[source-code]]より

### 3. install 導線が素の `pip install kouchou-ai-analysis-core`

`packages/analysis-core/README.md`、`docs/user-guide/cli-quickstart.md`、`docs/user-guide/import-quickstart.md` などは、現在は extras なし install を案内している。extras 化後にそのままだと、CLI 利用者が clustering/embedding 実行時に初めて落ちる。少なくとも「標準利用は `full`」なのか「軽量 install を正規化する」のかを docs で明示する必要がある。[[source-code]]より [[github-dev-docs]]より

## 実務上の推奨PR形

- PR タイトル例: `Split analysis-core optional dependencies into extras`
- 対象はまず `packages/analysis-core/` とその package docs / workflow に限定する
- `apps/api` 側は、必要なら install comment や Docker build 手順の明文化だけに留める
- 動作保証は `base import`, `full install`, `embedding step`, `clustering step` の 4 点を見る

## 依存関係

この PR は **独立して出せるが、完全に孤立ではない**。意味的には [[refactoring-status]] の「Phase 2.5 残課題」を 1 つ減らす PR であり、PyPI 配布導線との関係は [[pypi-auto-release-requirements]] と合わせて見るとよい。[[source-code]]より

## Open Questions

- `openai` も extras に分けるか、それとも current path どおり base dependency に残すか
- `full` を README の既定 install にするか、軽量 base install を前面に出すか
- optional dependency 不足時の UX を `ImportError` のままにするか、step 実行時に説明的なエラーへ包むか

## Updates

- 2026-05-21: `main@0e1552d` を確認し、Task 2.5.6 は独立 PR で切れるが eager import / CI / docs 更新を同梱すべきと整理
