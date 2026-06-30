---
type: source
summary: "2026-06-30 に GitHub live state と PR head ref で確認した PR #891。Windows standalone draft は embeddable Python + FastAPI + static viewer/admin を試すが、draft / dirty / stale で readiness risk が残る"
sources:
  - github-dev-docs.md
  - source-code.md
  - windows-distribution-options.md
  - node-runtime-free-windows-exe-2026-05-31.md
---

## Freshness

2026-06-30 14:33 JST に `gh pr view 891`、`gh pr diff 891 --name-only`、`git fetch origin pull/891/head:refs/remotes/origin/pr-891`、`git show origin/pr-891:<path>` で確認した。`work/kouchou-ai/` の作業 tree は `main@d5c9ece6e3b3` のまま checkout していない。[[github-dev-docs]]より [[source-code]]より

## GitHub State

PR #891 (`feat(packaging): Windows スタンドアロン（embeddable Python + 静的 viewer）`) は open / draft / review required / merge state dirty。author は `tokoroten`、head branch は `feat/windows-standalone-embeddable`、head commit は `2a27d572bb270ba7d5933b8a707ab77645c64ad8`。CodeRabbit は draft のため review を skip している。[[github-dev-docs]]より

2026-06-30 時点の open PR は #903 と #891 の 2 本だけで、#891 は #903 より古い 2026-06-01 の draft のまま更新が止まっている。`main...origin/pr-891` を見ると、PR branch 側の 6 commit に対し、main 側には public-viewer build/serve 分離、setup_win PowerShell 分離、security / dependency / CodeQL / aarch64 Numba など複数 commit が進んでいる。したがって、PR #891 は内容評価の前に rebase / conflict 解消が必要な stale branch と読むべきである。[[source-code]]より

## PR Scope

PR body は、広聴AIを Windows standalone として動かすため、embeddable Python に FastAPI backend + analysis pipeline を同梱し、public-viewer を静的 SPA として FastAPI から配信する土台と説明している。LM Studio の OpenAI-compatible local LLM と組み合わせ、torch を入れずに API コストなしで試す用途を狙う。[[github-dev-docs]]より

PR body の初期説明には `apps/admin` はまだ含めないとあるが、PR head の `packaging/windows-standalone/README.md` と後続 commits では admin static SPA も `/admin-ui` で同梱する形に進んでいる。したがって、PR body は一部 stale で、実際の head state は「viewer + admin を static assets として FastAPI 配信する draft prototype」である。[[github-dev-docs]]より

PR diff の merge-base からの差分は 47 files / 1861 insertions / 28 deletions。主な追加は `packaging/windows-standalone/`、public-viewer の standalone SPA ルート、admin の standalone build switch、PoC findings / verification scripts / screenshots である。[[source-code]]より

## Packaging Files

`packaging/windows-standalone/build.ps1` は Python 3.12 embeddable を download / extract し、`python312._pth` を編集して `Lib\site-packages` と `import site` を有効化し、pip / hatchling / `analysis-core[clustering,gemini]` / API runtime dependencies を入れる。torch は意図的に除外し、local embeddings は LM Studio など OpenAI-compatible endpoint に委譲する前提である。[[source-code]]より

同 script は `apps/api/src`、`broadlistening`、`public` を `dist/app` へコピーしつつ、pipeline configs / inputs / outputs と `data/report_status.json` を空にして、開発者ローカルのレポートデータや巨大 artifact を bundle に入れない。これは privacy と size の両方に効く設計判断である。[[source-code]]より

frontend bundle では public-viewer を `NEXT_PUBLIC_OUTPUT_MODE=export` / `NEXT_PUBLIC_STANDALONE=1` / `NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH=/viewer` で build し、admin を `NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH=/admin-ui` で build する。出力は `dist/viewer` と `dist/admin-ui` にコピーされ、`run-server.py` が FastAPI `StaticFiles` として mount する。[[source-code]]より

`run-server.py` は `start.bat` から `runtime\python.exe -X utf8 run-server.py` として起動される前提で、Japanese Windows の cp932 default による UTF-8 JSON decode crash を避けるため `-X utf8` を必須としている。bundle root の `.env` を先に `override=True` で読み、`ENV_FILE` を絶対 path にしてから `app/` へ chdir する。`/` は static UI がある場合 `/admin-ui/` または `/viewer/` へ redirect し、API の `/admin/*` route と衝突しないよう admin UI は `/admin-ui` に mount する。[[source-code]]より

## Standalone Viewer And Admin

public-viewer は `NEXT_PUBLIC_STANDALONE=1` を `isStandaloneBuild()` として `isStaticExportBuild()` から分ける。standalone は output としては static export だが、static-site-builder のように report slug を build 時に焼き込むのではなく、`/report?slug=...` の client page が runtime に API から取得して描画する。これは #885 の「runtime Node なし」と相性がよい一方、既存 static-site-builder の frozen HTML export とは別物である。[[source-code]]より

admin は hosted app の Server Actions / SSR root / route handlers / middleware を直接書き換えず、`apps/admin/scripts/standalone-prep.mjs` が standalone build の直前だけ `"use server"` を strip し、`ADMIN_API_KEY` 参照を `NEXT_PUBLIC_ADMIN_API_KEY` に向け、`app/page.tsx` と Footer を standalone client variants に差し替え、`app/api` / `middleware.ts` / `app/reuse` を一時的に退避する。build 後に restore するため、hosted build は untouched という建て付けである。[[source-code]]より

`env.sample` は `ADMIN_API_KEY` と `PUBLIC_API_KEY` が build 時に static UI へ bake されることを明示している。`dist/.env` だけを後から変えると UI 側の request key と API 側の key がずれて 401 になるため、変更するなら bundle rebuild が必要である。[[source-code]]より

## Findings And Known Limits

`tmp-embeddable-poc/FINDINGS.md` は、embeddable Python 方針自体は成立し、numba / UMAP / scipy / sklearn、analysis-core CLI import、FastAPI + uvicorn、StaticFiles 配信が動いたと記録する。配布サイズは runtime 約 664MB、torch を除外できたことが size の主要な勝ち筋。初回 cold import と UMAP JIT は重いので、起動 UX は別途考える必要がある。[[source-code]]より

同 findings は、current code の `apps/api/src/services/report_launcher.py` が analysis-core subprocess を `"python"` で起動する点を残タスクとして挙げている。2026-06-30 の current main / PR head でも `_build_analysis_core_command()` は `["python", "-m", "analysis_core", ...]` のままで、embeddable bundle の同梱 interpreter を確実に使うには `sys.executable` などへの変更が必要に見える。[[source-code]]より

PR head の README は、known limitations として admin の publish static site build button (`/api/download`) と `/reuse/[slug]` duplicate flow を standalone admin から除外し、full report creation は LM Studio または cloud key を動かした状態では未実行と書く。installer / Start Menu shortcut / windowless launcher は未実装で、React hydration warning と Next RSC prefetch 404 も非致命の既知事項として残る。[[source-code]]より

## Open Questions

- PR #891 は #885 の prototype / child issue として再位置づけるべきか、探索的 draft のまま扱うべきか。
- `standalone-prep.mjs` の build-time source mutation は prototype としては速いが、main に入れる運用として許容できるか。
- `ADMIN_API_KEY` / `PUBLIC_API_KEY` の static UI bake は local desktop threat model として許容するか、runtime config injection が必要か。
- `report_launcher.py` の subprocess interpreter は standalone merge 前に `sys.executable` へ変えるべきか。
- PR branch の stale / dirty 状態を解消する時、main 側の Windows setup / public-viewer build/serve / security fixes とどう統合するか。

## Updates

- 2026-06-30: 初回作成。PR #891 の live state、head ref、packaging files、standalone viewer/admin design、PoC findings、known limitations、main との stale 差分を固定した。
