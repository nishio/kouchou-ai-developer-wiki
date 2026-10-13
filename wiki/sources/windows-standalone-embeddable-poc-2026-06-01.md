---
type: source
summary: "PR #891（tokoroten, Draft）の検証記録 tmp-embeddable-poc/FINDINGS.md の要約。広聴AI を Windows スタンドアロン化する embeddable Python 方針が成立すると実証（numba/UMAP/FastAPI が単一 embeddable Python 上で完走、torch は LM Studio 委譲で回避し ~650MB）。同時に、現 main にも残る2つの移植性バグ（report_launcher の python ハードコード=#992、open/json.load の encoding 未指定による cp932 クラッシュ=#993）と、admin が Server Actions のため純静的化できないという設計分岐を発掘した"
sources:
  - "github PR #891 (feat/windows-standalone-embeddable, tmp-embeddable-poc/FINDINGS.md)"
---

## 何のソースか

kouchou-ai の PR **[#891](https://github.com/digitaldemocracy2030/kouchou-ai/issues/891)**（作者 tokoroten・**Draft**・2026-06-01 作成、以降停滞）に含まれる検証記録 `tmp-embeddable-poc/FINDINGS.md` の要約。広聴AI を **Windows スタンドアロン**（システム Python 不要、embeddable CPython に FastAPI バックエンド + 分析パイプライン + 静的 viewer を同梱）で動かす PoC の結果をまとめたもの。PR 本体のマージ可否とは独立に、知見と発掘されたバグを救出するために記録する。最終読解日 2026-10-13（`work/kouchou-ai` の `origin/feat/windows-standalone-embeddable` から読解）。

## 結論：embeddable Python 方針は成立する

最大リスクだった **numba/UMAP の JIT・パイプラインの subprocess 起動・FastAPI+uvicorn の Web 配信が、すべて単一の embeddable Python 上で動いた**。

- Python 3.12 embeddable (amd64) を `runtime/` に展開、`python312._pth` に `Lib\site-packages` 追加＋`import site` 有効化、`get-pip.py` で pip ブートストラップ。
- `analysis-core[clustering,gemini]`（**torch を含む `embeddings` extra は入れない**）＋ `uvicorn[standard] fastapi pydantic-settings orjson structlog` を導入。
- **torch を LM Studio（OpenAI 互換のローカル LLM・embedding）に委譲して回避** → バンドル **~650MB**（torch 同梱なら +2.5GB 超）。圧縮インストーラ化で ~250–300MB 見込み。
- スモーク全 PASS（numba `@njit`、UMAP `fit_transform`、polars/scipy/sklearn import、`python -m analysis_core --help`、uvicorn で FastAPI 起動＋`/health`、`StaticFiles` 配信）。実データでの `hierarchical_clustering`（UMAP→KMeans→ward→fcluster→CSV）も完走。
- 起動コスト: 初回 cold import ~20 秒、初回 UMAP fit ~8.6 秒（numba JIT）。2 回目以降は JIT キャッシュで短縮。初回だけスプラッシュで吸収する想定。

## 発掘された、現 main にも残るバグ（PR と独立に価値）

2026-10-13 時点の main で残存を確認し、issue 化のうえ **PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995) で両方を修正・main へ merge 済み**（merge commit `a570d689`、[#992](https://github.com/digitaldemocracy2030/kouchou-ai/issues/992)/[#993](https://github.com/digitaldemocracy2030/kouchou-ai/issues/993) とも自動 close、API 318 / analysis-core 321 tests pass・ruff clean）：

- **`report_launcher.py:92` が `"python"` をハードコード** → PATH 上の別 Python を拾う。`sys.executable` にすべき。analysis-core は Docker/推奨ローカル開発で API と同一環境に入る（`apps/api/pyproject.toml` のコメント）ため `sys.executable` が正しい。→ **issue [#992](https://github.com/digitaldemocracy2030/kouchou-ai/issues/992) / PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)**。
- **`open()`/`json.load` の多くが `encoding` 未指定** → 日本語 Windows の既定 cp932 で UTF-8 JSON を読み `UnicodeDecodeError` でクラッシュ（Linux/Docker は UTF-8 既定で顕在化しない）。`report_status.py` / `meta.py` / `admin_report.py` 等の API 起動・実行時読み取り経路が該当。PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995) は `apps/api` と `analysis-core` の読み書き両方に `encoding="utf-8"` を明示（起動時 `PYTHONUTF8=1` でも一括回避可）。→ **issue [#993](https://github.com/digitaldemocracy2030/kouchou-ai/issues/993) / PR [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)**。

## 設計分岐：admin は純静的化できない

| アプリ | 設定 | 静的化 | スタンドアロンでの扱い |
|---|---|---|---|
| **public-viewer** | `NEXT_PUBLIC_OUTPUT_MODE=export` で `output:"export"` | 可能 | 静的ファイルを FastAPI `StaticFiles` で配信 |
| **admin** | `output:"standalone"` ＋ **Server Actions 使用** | **不可** | **Node.js ランタイム必須**（同梱 or Server Actions を FastAPI 呼び出しへ書き換え） |

「単一 Python ランタイムで完結」を阻む最大の分岐点がこれ。Windows 配布を本気で検討するなら最初に決めるべき判断。

## 再利用可能な実装（PR ブランチ内）

- **public-viewer の SPA 化パターン**（`isStandaloneBuild()` = `NEXT_PUBLIC_STANDALONE=1` で分岐、`ReportView` のクライアント版・`/report?slug=` universal ページ・`ReporterClient`）。static export は「ビルド時のレポートを焼き込む」方式で実行時作成レポートを表示できないため、**実行時に API から取得して描画**する方式にしたもの。ホスト版(SSR)と static-site-builder の挙動は不変。
- `packaging/windows-standalone/build.ps1`（embeddable 構築の動く参照実装）。

## embeddable 特有のハマりどころ（FINDINGS より）

- `pip install ./packages/analysis-core` がビルド分離で `hatchling.build` を import できず失敗（embeddable の `_pth` がサブプロセスの sys.path を絞るため）。回避＝先に `pip install hatchling` ＋ `--no-build-isolation`、本番では **wheel 事前ビルド**して embeddable に入れる。
- フロント静的化の footgun: React **[#482](https://github.com/digitaldemocracy2030/kouchou-ai/issues/482)**（async サーバコンポーネント `Reporter` をクライアントツリーで描画すると落ちる→`ReporterClient` 差し替え）／ [#418](https://github.com/digitaldemocracy2030/kouchou-ai/issues/418) ハイドレーション警告（`dynamic(ssr:false)` で実害回避）／ `output:export` の動的ルートは空 `generateStaticParams` がエラー（sentinel 1 件返しで回避）／ `apps/public-viewer/.env.local` が `NEXT_PUBLIC_API_BASEPATH` を上書きし別ポートを叩いて CORS 失敗。
- ビルドスクリプトの footgun: PowerShell 5.1 は `next build` の stderr 警告が `$ErrorActionPreference=Stop` で致命化（当該区間だけ `Continue`＋`$LASTEXITCODE` 判定）／ `Copy-Item -Recurse` が既存同名ディレクトリへネスト（コピー前に削除）／ git-bash の MSYS パス変換で `/viewer` が化ける（`MSYS_NO_PATHCONV=1`、build.ps1=PowerShell では非発生）。

## 残タスク / 要判断（FINDINGS より）

- **admin をどうするか**（Node 同梱 vs Server Actions 書き換え）が最大の分岐点。
- ランチャー exe（`PYTHONUTF8=1` 設定＋API 起動＋ブラウザ自動オープン）＋ Inno Setup 化。
- 本番ビルドは analysis-core を wheel 事前ビルドして同梱。
- 実 LLM での真の end-to-end は LM Studio を GUI 起動した状態でユーザー自身が要実施（PoC では headless 起動できず未実施。LLM 経路は OpenAI 互換 HTTP で embeddable 固有リスクは無い）。

## Open Questions

- PR [#891](https://github.com/digitaldemocracy2030/kouchou-ai/issues/891) 自体は 130 commits 遅れ・現 main と 4 競合（`EnvironmentCheckDialog.tsx` / public-viewer `[slug]/page.tsx` / `page.tsx` / `ReportView.tsx`）・CLA 未同意・CI は 2026-06 の古い結果のみ・`tmp-embeddable-poc/` を同梱したまま。作者の継続意思を確認して rebase 再挑戦するか、一旦 close して知見だけ本ページに残すかは要判断（人間 attention 領域）。
- Windows スタンドアロン需要と、既存の Windows 対応施策（[[gotchas]] の「Windows インストール地獄」、[#524](https://github.com/digitaldemocracy2030/kouchou-ai/issues/524) ネイティブ環境等）との優先度関係。
