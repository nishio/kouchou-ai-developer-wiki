---
title: "CLI(kouchou-analyze / analysis_core)"
name: cli
summary: "kouchou-analyze CLI と python -m analysis_core — pip install で使える"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - pr-825-standalone-html-observation-2026-05-19.md
  - report-html-non-web-canonical-decision-2026-05-23.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
  - source-code.md
---

## エントリポイント

`packages/analysis-core/pyproject.toml`:

```toml
[project.scripts]
kouchou-analyze = "analysis_core.__main__:main"
```

つまり：

- `pip install kouchou-ai-analysis-core` すると **`kouchou-analyze` コマンド** が PATH に入る
- 等価に `python -m analysis_core` でも起動可能（API サーバはこちらを使う）

PyPI 上の **パッケージ名は `kouchou-ai-analysis-core`（ハイフン）**、import 時の **モジュール名は `analysis_core`（アンダースコア）**。新規利用者が混乱しやすい。

### PyPI 版は main より遅れる

2026-10-21 時点で PyPI の最新は 0.1.3（2026-10-12 公開。タグ `analysis-core-v0.1.3` = `055b8824`）。それより後に main に入った機能と修正は PyPI 版に無い。たとえば UMAP 平面の使い回し `reuse_umap_model`（PR [#988](https://github.com/digitaldemocracy2030/kouchou-ai/issues/988)）、意見ラベル付与の `opinion_classification`（PR [#975](https://github.com/digitaldemocracy2030/kouchou-ai/issues/975)）、指定カテゴリ分類の `predefined_groups`（PR [#996](https://github.com/digitaldemocracy2030/kouchou-ai/issues/996)、[[llm-grouping-supervised-classification]]）と、analysis-core の修正（PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)、[#1015](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1015)、[#1016](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1016)、[#1022](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1022)、[#1029](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1029)〜[#1033](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1033)、[#1037](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1037) など。集計結果のデータ欠落を直した [#1032](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1032) を含む）。PyPI 版に上の機能の設定を渡すと、config の検証で `Unknown field ...` / `Unknown option ...` として止まる。

main の version 表記も 0.1.3 のままなので、`kouchou-analyze --version` では PyPI 版か main 版かを区別できない。新しい機能を使うときは本体を clone し、`packages/analysis-core` で `pip install -e ".[embeddings,clustering]"` を実行する（extras は PyPI 版の推奨と同じ。Gemini を使うなら `gemini`、テストも回すなら `dev` を足す。`packages/analysis-core/README.md` の「開発」節も参照）。PyPI への公開は `analysis-core-v*` タグの push で起き、merge だけでは起きない（[[pypi-release-trigger]]）。

## フラグ

`packages/analysis-core/src/analysis_core/__main__.py`:

| フラグ | 意味 |
|---|---|
| `--config / -c PATH` | 設定 JSON（必須） |
| `--force / -f` | 完了済みステップも強制再実行。`--only` と一緒に使うと、そのステップだけを再実行する |
| `--only / -o STEP` | 特定ステップのみ実行。値は `analysis_mode` ごとの spec のステップ名（hierarchical なら 9 個。例: `hierarchical_clustering`、`hierarchical_aggregation`）で、workflow 側の短い名前（`clustering` など）は使えない。存在しない名前や、実行されないステップ（無効にした `opinion_classification`、`--without-html` のときの `hierarchical_visualization`）を指定すると exit 1 |
| `--output-dir PATH` | 出力ベースディレクトリ（既定 `outputs`） |
| `--input-dir PATH` | 入力ベースディレクトリ（既定 `inputs`） |
| `--reuse-from SRC` | 別ジョブの出力（パス、または `--output-dir` の下のジョブ名）から、完了済みステップの中間成果物をコピーし、その段を skip できるようにする。`hierarchical_aggregation` / `hierarchical_visualization` は再利用せず毎回やり直す。出力先に `hierarchical_status.json` が既にあればコピーしない（別の複製元を指定していれば警告を出す）。config JSON の `reuse_from` でも指定できる |
| `--dry-run` | 軽い事前検証（config と入力 CSV。API キーは見ない）の後、実行計画を表示して終了。status の書き込み、出力ディレクトリの作成、`--reuse-from` のコピーはしない |
| `--validate-config` | config の構造と `--only` の値を検証して終了（API キーと入力 CSV は見ない） |
| `--validate-input` | config の検証に加えて、入力 CSV があるかと必須列（`comment-id`, `comment-body`。`extraction.properties` で指定した列も）を検証して終了。実行計画が入力を必要としない場合は CSV を見ない |
| `--version / -v` | バージョン表示 |
| `--skip-interaction` | 対話プロンプトをスキップ（既定 True） |
| `--without-html` | HTML 生成をスキップ（既定 False） |

`--reuse-from` は PR [#867](https://github.com/digitaldemocracy2030/kouchou-ai/issues/867)、`--validate-config` / `--validate-input`（と `--dry-run` の事前検証）は PR [#844](https://github.com/digitaldemocracy2030/kouchou-ai/issues/844) で入った。`--only` の検証と `--force` との併用時の挙動は PR [#1033](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1033)（2026-10-19 merge）以降のもので、それより前は `--force` を付けると `--only` が無視されて全段が再実行された。`analysis_mode=llm_grouping` で `llm_grouping` 段を `--reuse-from` で再利用すると集計が失敗する不具合があったが、PR [#1043](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1043)（2026-10-21 merge）で直った。`--reuse-from` が PR だった時点の観測は [[open-pr-pipeline-step-observation-2026-05-28]]。

## ハマりどころ：`--skip-interaction` は CLI から無効化できない

current `main` では `--without-html` は `default=False` へ直っており、CLI 既定で自己完結型 `report.html` が出る。これは `PR #825` で入った変更。[[pr-825-standalone-html-observation-2026-05-19]]より

一方、`--skip-interaction` はなお `action="store_true"` + `default=True` で定義されている：

```python
parser.add_argument("--skip-interaction", action="store_true", default=True,
                    help="Skip interactive prompts (default: True)")
```

= **コマンドラインから False に戻せない**。対話確認を明示的に有効化したい用途にはまだ向かない。[[gotchas]] にも記載。

## ライブラリとしての利用

```python
from analysis_core import PipelineOrchestrator
orchestrator = PipelineOrchestrator.from_config(config_path=Path("config.json"))
result = orchestrator.run_default()
```

公開 export（`analysis_core/__init__.py`）：

- `PipelineOrchestrator` — CLI の中身
- `PipelineConfig`, `PipelineResult`, `StepResult`
- `__version__`

実行モードは 2 系統（[[pipeline]] 参照）：

- `orchestrator.run_default()` → `run_workflow()` — canonical な実行経路。CLI（`__main__.py`）はこれを呼ぶ（[[plugin-system]] 経由の workflow 実行）
- `orchestrator.run()` — レガシーの `run_step` ループ。`DeprecationWarning` つきの互換用で、新規は `run_default()` を使う

ただし 2026-05-20 時点の open PR `#840` では、`run_workflow()` 側に初期 `comments` artifact、status 永続化、rerun artifact 再利用まで段階的に持ち込み中であり、CLI default 化に向けた地ならしは進んでいる。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

## API サーバとの境界

`apps/api/src/services/report_launcher.py` は **subprocess** で CLI を起動する。コマンドは `_build_analysis_core_command(config_path, only=None)` が組み立てる：

```python
cmd = [sys.executable, "-m", "analysis_core",
       "--config", str(config_path),
       "--output-dir", str(settings.REPORT_DIR),
       "--input-dir", str(settings.INPUT_DIR),
       "--skip-interaction", "--without-html"]
# only を渡すと ["--only", only] を足す
```

- 起動は `_launch_analysis_process` の `subprocess.Popen(cmd, env=env, stdout=<analysis.log>, stderr=subprocess.STDOUT)`
- 呼び出し元は `launch_report_generation` と `launch_report_generation_from_config`（どちらも `--only` なし）、ラベル編集後の再集計 `execute_aggregation`（`only="hierarchical_aggregation"`）
- インタプリタに `sys.executable`（API を動かしているのと同じ Python）を使うのは、PATH 上の別の `python`（analysis_core の入っていない Python など）を拾わないため。Issue [#992](https://github.com/digitaldemocracy2030/kouchou-ai/issues/992) を PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)（2026-10-13 merge）で直した。教訓は [[gotchas]]

パイプラインの実行はこの subprocess を境界にしている。依存は API→core の一方向で、analysis-core 側は API を import しない。ただし次の 2 か所では、API が `analysis_core.services.llm` を関数内で直接 import する。

- 接続確認 `GET /admin/environment/verify`: `request_to_chat_ai`（`apps/api/src/routers/admin_report.py`）
- ローカル LLM のモデル一覧 `GET /admin/models`（provider が local のとき）: `resolve_local_llm_base_url`（`apps/api/src/services/llm_models.py`。PR [#1038](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1038) 以降）

この 2 関数の名前・引数・戻り値の形（接続確認は `response[0]` を応答文として読む）・投げる例外の型とメッセージ（接続確認のエラー分類に使う）を変えると、API 側も壊れる。API のテストは `request_to_chat_ai` を mock して使うので、引数・戻り値・例外の変化は API の CI では捕まらない。変えるときは `apps/api` も grep すること。import は関数内なので analysis-core が無くても API 自体は起動するが、これらのエンドポイントは 500 になり、レポート生成の subprocess も `No module named analysis_core` で失敗する。したがって API の実行環境（ネイティブ起動や API の pytest を含む）には analysis-core のインストールが必要（Docker イメージと CI では同梱・インストール済み。手順は [[local-dev-setup]] / [[testing]]）。[[source-code]]より

なお CLI 既定で出る `report.html` は **CLI / 手動実行向けの観察用HTML** であり、Web の主経路を置き換えるものではない。current `apps/api/src/routers/report.py` は `hierarchical_result.json` を返し、`apps/public-viewer` はその JSON を fetch して描画する。`apps/api/src/services/report_launcher.py` が subprocess 起動時に `--without-html` を付けているのも、現行 Web 経路では HTML が配信対象ではないから、と読むのが自然。[[pr-825-standalone-html-observation-2026-05-19]]より

2026-05-23 の maintainer 判断でも、この `report.html` は Web canonical にしない。したがって CLI の観察用HTMLと Web の JSON viewer は、「あとで統一されるはずの半端状態」ではなく、現在の artifact 契約として分けて読む。[[report-html-non-web-canonical-decision-2026-05-23]]より

新しい読者向けには、ここを **「CLI 既定と API 挙動が食い違っている未解決問題」ではなく、「利用モードごとに artifact 契約を分けている」** と明記しておく方が混乱が少ない。CLI は手元で完結して読める `report.html` を重視し、Web は `hierarchical_result.json` + `public-viewer` を canonical path としている。判断の全体像は [[analysis-core-and-web-ui]]。[[usage-modes]]より

## 関連ドキュメント

- `docs/user-guide/cli-quickstart.md` — 公式 quickstart。`config.json` 例とトラブルシューティング（`Job already running` → `rm -rf outputs/config`）
- なお `pyproject.toml` の `Documentation` URL は古い `docs/CLI_QUICKSTART.md` を指していて壊れている（実体は `docs/user-guide/cli-quickstart.md`）

## クラスタ数デフォルト

2026-05-18 の `Issue #830` / `PR #832` では、CLI / `analysis-core` の `hierarchical_clustering.cluster_nums` を **省略可能** にし、未指定時は extraction 後の `argument` 数から cube-root rule で推奨値を自動計算する方向が整理された。  
背景には、quickstart の `[3, 6]` 例が AI コーディングエージェントにそのまま転用され、300 件規模でも粗いまとめを生みやすかったという実務上の問題がある。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

ただし source repo 全体では、README や `docs/getting-started/quickstart.md`（現 `docs/self-hosting/quickstart.md`）が「コメント数ベース」の説明を残している一方、`analysis-core` 実装は「`argument` 数ベース」に寄っている。2026-05-18 時点では、**Web docs の語り口と CLI 実装の基準はまだ完全一致していない**。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

## "vive 広聴AI" 用途

[[meeting-minutes]] 2025-07-09 で命名された「AI コーディングエージェントから叩く CLI 利用パターン」のメイン経路。議事メモ 2026-05-18 見出しの [[nishio]] の社内 300 件分析でも、`Claude Code` がこの CLI を直接叩いている。

## Open Questions

- `--skip-interaction` を CLI から False に戻せない問題の解決

## Updates

- 2026-10-21: main `b71e0b79` と照合。フラグ表に `--reuse-from`・`--validate-config`・`--validate-input` を足し、`--only` / `--force` / `--dry-run` の説明を PR [#1033](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1033) 後の挙動に合わせた。API 起動のコード例を `sys.executable` に直し（PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)）、「API は `analysis_core` を import しない」を訂正（接続確認とローカル LLM のモデル一覧では直接 import する）。PyPI 0.1.3 が main より遅れている点を追記。PR [#1043](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1043) が 2026-10-21 に merge されたことを反映
- 2026-10-18: docs の rename（`docs/getting-started/` → `docs/self-hosting/`）を注記
- 2026-05-17: 初回作成（コードリーディング結果から）
- 2026-05-18: `Issue #830` / `PR #832` により、`cluster_nums` 省略時は cube-root rule で推奨値を自動算出する方向が具体化したことを追記
- 2026-05-19: `PR #825` merge 後の current `main` に合わせ、`--without-html` は既定 False へ直ったが、これは CLI 向け観察用HTMLの話であり Web の主経路は JSON + `public-viewer` のままだと補正
- 2026-05-20: open PR `#840` により、`run_workflow()` default 化へ向けた下回り実装が branch 上で進んでいることを追記
- 2026-05-23: maintainer 判断 [[report-html-non-web-canonical-decision-2026-05-23]] を反映し、`report.html` は Web canonical にしないと明記
- 2026-10-07: lint 注記。本文の「open PR `#840`」は 2026-05-21 に merge 済み。current main `a12d68e` では CLI が `run_default()` → `run_workflow()` を呼ぶ（[[refactoring-status]]）
- 2026-10-07: main `a12d68e` で、既定の CLI 実行（HTML あり）が可視化の段階で `report_dir` 未定義により失敗することを確認（[#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) / PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955)）。クイックスタートが案内する `report_url_pattern` も効かない（[#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954)）。経緯は [[gotchas]] の「CLI の `report.html` 経路は Web UI の実行では通らない」
- 2026-10-12: 本文のライブラリ利用例（L63）と実行モード説明を current main に合わせて訂正（`run()` → `run_default()`→`run_workflow()` が canonical、`run()` は `DeprecationWarning` つき deprecated）。2026-10-07 の lint 注記は履歴として残置。`kouchou-analyze` の PyPI 公開＋GHA 自動リリースは完了済みのため Open Questions から除去（[[refactoring-status]] Phase 2.5。残件 Trusted Publishing / release gate hardening は [[open-decisions]] follow-up）。[[wiki-self-audit-2026-10-12]]
