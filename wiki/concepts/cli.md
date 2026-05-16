---
name: cli
summary: kouchou-analyze CLI と python -m analysis_core — pip install で使える
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
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
| `--without-html` | HTML 生成をスキップ（既定 True） |

## ハマりどころ：`--without-html` / `--skip-interaction` が無効化できない

両者は `action="store_true"` + `default=True` で定義されている：

```python
parser.add_argument("--without-html", action="store_true", default=True,
                    help="Skip HTML visualization generation (default: True)")
```

= **コマンドラインから False に戻せない**。HTML を出したい場合はライブラリ API (`PipelineOrchestrator`) を直接叩く必要がある。[[gotchas]] にも記載。

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

## API サーバとの境界

`apps/api/src/services/report_launcher.py` は **subprocess** で CLI を起動する：

```python
subprocess.Popen(["python", "-m", "analysis_core",
                  "--config", str(config_path),
                  "--output-dir", str(settings.REPORT_DIR), ...])
```

API は `analysis_core` を import しない。**`python -m analysis_core` が canonical な境界面**。これにより `apps/api/` と `packages/analysis-core/` は依存方向が一方向（API→core）に整理されている。

## 関連ドキュメント

- `docs/user-guide/cli-quickstart.md` — 公式 quickstart。`config.json` 例とトラブルシューティング（`Job already running` → `rm -rf outputs/config`）
- なお `pyproject.toml` の `Documentation` URL は古い `docs/CLI_QUICKSTART.md` を指していて壊れている（実体は `docs/user-guide/cli-quickstart.md`）

## "vive 広聴AI" 用途

[[meeting-minutes]] 2025-07-09 で命名された「AI コーディングエージェントから叩く CLI 利用パターン」のメイン経路。議事メモ 2026-05-18 見出しの [[nishio]] の社内 300 件分析でも、`Claude Code` がこの CLI を直接叩いている。

## Open Questions

- `--without-html` を CLI から有効化できない問題の解決（`store_false` への変更、default 反転、別フラグ名）
- `kouchou-analyze` PyPI 公開と GitHub Actions 自動リリース（[[refactoring-status]] 参照）

## Updates

- 2026-05-17: 初回作成（コードリーディング結果から）
