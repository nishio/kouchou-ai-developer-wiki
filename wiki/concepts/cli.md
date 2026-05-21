---
name: cli
summary: "kouchou-analyze CLI と python -m analysis_core — pip install で使える"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - pr-825-standalone-html-observation-2026-05-19.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
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

## フラグ

`packages/analysis-core/src/analysis_core/__main__.py`:

| フラグ | 意味 |
|---|---|
| `--config / -c PATH` | 設定 JSON（必須） |
| `--force / -f` | 完了済みステップも強制再実行 |
| `--only / -o STEP` | 特定ステップのみ |
| `--output-dir PATH` | 出力ベースディレクトリ |
| `--input-dir PATH` | 入力ベースディレクトリ |
| `--dry-run` | 実行計画のみ表示 |
| `--version / -v` | バージョン表示 |
| `--skip-interaction` | 対話プロンプトをスキップ（既定 True） |
| `--without-html` | HTML 生成をスキップ（既定 False） |

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
result = orchestrator.run()
```

公開 export（`analysis_core/__init__.py`）：

- `PipelineOrchestrator` — CLI の中身
- `PipelineConfig`, `PipelineResult`, `StepResult`
- `__version__`

実行モードは 2 系統（[[pipeline]] 参照）：

- `orchestrator.run()` — 既定。レガシーの `run_step` ループ
- `orchestrator.run_workflow()` — [[plugin-system]] 経由の workflow 実行。**実装はあるが CLI からは呼ばれない**

ただし 2026-05-20 時点の open PR `#840` では、`run_workflow()` 側に初期 `comments` artifact、status 永続化、rerun artifact 再利用まで段階的に持ち込み中であり、CLI default 化に向けた地ならしは進んでいる。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

## API サーバとの境界

`apps/api/src/services/report_launcher.py` は **subprocess** で CLI を起動する：

```python
subprocess.Popen(["python", "-m", "analysis_core",
                  "--config", str(config_path),
                  "--output-dir", str(settings.REPORT_DIR), ...])
```

API は `analysis_core` を import しない。**`python -m analysis_core` が canonical な境界面**。これにより `apps/api/` と `packages/analysis-core/` は依存方向が一方向（API→core）に整理されている。

ただしこれは **CLI / 手動実行向けの sidecar 成果物** の話であり、Web の主経路を置き換えるものではない。current `apps/api/src/routers/report.py` は `hierarchical_result.json` を返し、`apps/public-viewer` はその JSON を fetch して描画する。`apps/api/src/services/report_launcher.py` が subprocess 起動時に `--without-html` を付けているのも、現行 Web 経路では HTML が配信対象ではないから、と読むのが自然。[[pr-825-standalone-html-observation-2026-05-19]]より

新しい読者向けには、ここを **「CLI 既定と API 挙動が食い違っている未解決問題」ではなく、「利用モードごとに artifact 契約を分けている」** と明記しておく方が混乱が少ない。CLI は手元で完結して読める `report.html` を重視し、Web は `hierarchical_result.json` + `public-viewer` を canonical path としている。[[usage-modes]]より

## 関連ドキュメント

- `docs/user-guide/cli-quickstart.md` — 公式 quickstart。`config.json` 例とトラブルシューティング（`Job already running` → `rm -rf outputs/config`）
- なお `pyproject.toml` の `Documentation` URL は古い `docs/CLI_QUICKSTART.md` を指していて壊れている（実体は `docs/user-guide/cli-quickstart.md`）

## クラスタ数デフォルト

2026-05-18 の `Issue #830` / `PR #832` では、CLI / `analysis-core` の `hierarchical_clustering.cluster_nums` を **省略可能** にし、未指定時は extraction 後の `argument` 数から cube-root rule で推奨値を自動計算する方向が整理された。  
背景には、quickstart の `[3, 6]` 例が AI コーディングエージェントにそのまま転用され、300 件規模でも粗いまとめを生みやすかったという実務上の問題がある。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

ただし source repo 全体では、README や `docs/getting-started/quickstart.md` が「コメント数ベース」の説明を残している一方、`analysis-core` 実装は「`argument` 数ベース」に寄っている。2026-05-18 時点では、**Web docs の語り口と CLI 実装の基準はまだ完全一致していない**。[[issue-830-pr-832-auto-cluster-defaults-2026-05-18]]より

## "vive 広聴AI" 用途

[[meeting-minutes]] 2025-07-09 で命名された「AI コーディングエージェントから叩く CLI 利用パターン」のメイン経路。議事メモ 2026-05-18 見出しの [[nishio]] の社内 300 件分析でも、`Claude Code` がこの CLI を直接叩いている。

## Open Questions

- `--skip-interaction` を CLI から False に戻せない問題の解決
- standalone `report.html` を保存・配信対象にしたいユースケースがあるか
- `kouchou-analyze` PyPI 公開と GitHub Actions 自動リリース（[[refactoring-status]] 参照）

## Updates

- 2026-05-17: 初回作成（コードリーディング結果から）
- 2026-05-18: `Issue #830` / `PR #832` により、`cluster_nums` 省略時は cube-root rule で推奨値を自動算出する方向が具体化したことを追記
- 2026-05-19: `PR #825` merge 後の current `main` に合わせ、`--without-html` は既定 False へ直ったが、これは CLI 側 sidecar HTML の話であり Web の主経路は JSON + `public-viewer` のままだと補正
- 2026-05-20: open PR `#840` により、`run_workflow()` default 化へ向けた下回り実装が branch 上で進んでいることを追記
