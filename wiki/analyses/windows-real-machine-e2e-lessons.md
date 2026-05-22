---
type: analysis
summary: "Issue #860 / PR #862 の Windows 実機 E2E 構築で分かった self-hosted runner と Docker Desktop の落とし穴"
sources:
  - source-code.md
  - github-dev-docs.md
  - gotchas.md
  - coding-agents.md
  - testing.md
---

# Windows 実機 E2E 構築の学び

## Summary

Issue #860 では、Windows 実機で `setup_win.bat` と Docker Desktop を検証する手順を docs に書くだけでなく、PR #862 として self-hosted Windows runner 上の E2E workflow まで作った。結果として、単なるドキュメント確認では見落としやすい Docker image の欠落、runner service の PATH 差分、PowerShell HTTP client の挙動差分を検出できた。[[source-code]]より [[github-dev-docs]]より

個人情報を残さないため、このページではローカルユーザー名、メールアドレス、端末固有名、絶対パスは扱わない。公開されている Issue / PR 番号、branch / commit、workflow 上の一般化できる症状だけを記録する。

## What Happened

最初の実機 E2E workflow は、`setup_win.bat` を非対話で実行し、その後 `localhost:4000` / `localhost:3000` / `localhost:8000/docs` を待つ構成にした。Hosted `windows-latest` では Docker Desktop 実機検証はできないため、軽量な `.bat` 回帰 CI と self-hosted runner の実機 E2E を分けた。[[source-code]]より

runner を動かすと、まず workflow 環境の前提差分が順に出た。self-hosted Windows runner には `pwsh` が無く、PowerShell execution policy が `.ps1` 実行を拒み、runner service の PATH には Docker CLI が入っていなかった。そこで workflow は Windows PowerShell に寄せ、`-ExecutionPolicy Bypass` を明示し、Docker CLI は絶対パスと一時 PATH 追加で扱うようにした。[[source-code]]より

任意の PR から self-hosted runner が動くのは危険なので、PR 起動時は PR author が `nishio` の場合だけ実行する条件を入れた。これは secrets を使わない E2E でも、実機 runner が任意コードを実行する以上、攻撃面を広げるためである。[[coding-agents]]より

同じ PR へ連続 push すると古い E2E run が単一 runner を占有し、新しい run が queued のままになった。`concurrency` と `cancel-in-progress` を入れることで、同じ PR の古い実機 E2E をキャンセルし、最新 head を優先できるようにした。[[github-dev-docs]]より

実機 E2E が初めて app stack まで進むと、`public-viewer` の runtime build が `Cannot find module '../shared/csp'` で落ちた。原因は `apps/public-viewer` と `apps/static-site-builder` の Docker image runtime stage に `apps/shared` が入っていないことだった。Docker Desktop 実機で image build を再現し、両 Dockerfile に `apps/shared` の copy を追加して解消した。[[source-code]]より

最後に、container は起動し `curl.exe -I` では各 URL が 200 を返すのに、workflow の `Invoke-WebRequest` は同じ URL で timeout した。E2E の readiness check は本文を読む必要がないため、PowerShell HTTP client ではなく `curl.exe --fail --head --silent --show-error --max-time 5` に寄せた。これで PR #862 の checks は、実機 E2E を含めて success になった。[[source-code]]より [[github-dev-docs]]より

## Why Existing Success Did Not Catch It

今回の重要な教訓は、GitHub Actions 上の `success` が「何を観測した success か」を分けて読む必要があること。`Deploy Documentation` の success は docs build / GitHub Pages deploy の成功であり、production app の Docker runtime build 成功を意味しない。`client build` は checkout された repo 全体で `pnpm --filter @kouchou-ai/public-viewer build` を実行するため、`apps/shared` は普通に見える。どちらも、Docker image の runner stage に `apps/shared` が copy されているかまでは保証しない。[[testing]]より [[source-code]]より

Azure deployment workflow は `apps/public-viewer/Dockerfile` と `apps/static-site-builder/Dockerfile` を build / push し、Container Apps 更新後に HTTP status を見る構成を持つ。ただし今回 PR 上で見えていた success 群をそのまま「この PR head の production runtime が完全に検査された」と読むのは危険だった。少なくとも PR #862 の失敗時点で問題になったのは、`public-viewer` container の起動後に `entrypoint.sh` が実行する runtime `pnpm run build` であり、そこでは Dockerfile runner stage に明示 copy されたファイルだけが存在する。[[source-code]]より [[github-dev-docs]]より

つまり、同じ `public-viewer build` でも観測面が違う。repo checkout 上の build は「source tree 全体がある状態で Next.js build が通るか」を見る。Docker build は「image を作れるか」を見る。container 起動後の runtime build は「runner stage に入れたファイルだけで build / start できるか」を見る。実機 E2E は最後の層まで踏んだため、`apps/shared/csp` 欠落を検出できた。[[source-code]]より

## Lessons

- Windows 実機 E2E は「setup 手順が正しいか」だけでなく、Docker image の runtime stage に必要ファイルが本当に入っているかも検出する。今回の `apps/shared/csp` 欠落は、docs だけでは見つけにくい種類の問題だった。
- CI / deploy の `success` は、それがどの層を検査した成功かまで読む。docs deploy success、repo checkout 上の client build success、Docker image build success、container 起動後 runtime build success は別物である。
- self-hosted runner は、手元の対話 shell と同じ環境だと思わない。`pwsh`、execution policy、PATH、Docker Desktop への到達性は、runner service 上で別物として確認する。
- Windows workflow では、Docker CLI の場所を明示した方が安定する。特に Docker Desktop を後から入れた環境では、service が見る PATH に反映されていないことがある。
- self-hosted runner は任意 PR で動かさない。PR author 制限、手動 dispatch、nightly など、実行入口を意識的に絞る。
- 単一 runner では、同じ PR の古い run が残るだけで最新検証が止まる。PR 番号単位の `concurrency` は実機 E2E と相性がよい。
- readiness check は「ページ本文を全部取る」より「HTTP status が返る」ことを検査する方が堅い。Windows PowerShell の `Invoke-WebRequest` が timeout する場面でも、`curl.exe --head --fail` は期待通り機能した。
- E2E failure を runner 設定の問題と app の問題に切り分けるには、GitHub Actions の状態、runner process、Docker containers、container logs、host からの HTTP probe を順に見ると迷いにくい。

## Operational Pattern

Windows 実機 E2E を増やす時は、まず hosted Windows で検出できる軽量 CI と、self-hosted runner でしか検出できない実機 CI を分ける。前者は `.bat` の文字コード、非対話 mode、失敗 path、`.env` 生成のような安い確認に向いている。後者は Docker Desktop、port forwarding、実 app stack、runtime image の欠落確認に向いている。[[testing]]より [[source-code]]より

self-hosted runner の workflow は、初期状態から「人間が今見ている shell」と違う前提で書く。`shell`、`PATH`、実行 policy、Docker CLI path、cleanup の失敗許容、古い run の cancellation までを workflow に閉じ込めると、再起動後や別ユーザー session でも再現しやすい。[[gotchas]]より

E2E が失敗した時は、すぐに workflow を直すより、まず「runner が job を拾ったか」「container が起動したか」「container 内アプリが Ready か」「host から port が見えるか」を分けて見る。今回も、runner pickup の問題、Dockerfile の `apps/shared` 欠落、PowerShell readiness check の timeout は別々の層だった。[[source-code]]より

## Open Questions

- self-hosted runner の実行条件は PR author 固定で十分か、将来は label / environment approval / protected runner group に寄せるべきか。
- Windows 実機 E2E は nightly と手動 dispatch を中心にし、PR ごとは opt-in にする方が runner 負荷と安全性のバランスがよいか。
- readiness check は `curl.exe` のままでよいか、将来は専用の health endpoint を用意して body / static generation に依存しない検査へ寄せるべきか。

## Updates

- 2026-05-22: 初回作成。Issue #860 / PR #862 の Windows 実機 E2E 構築で得た runner、Docker Desktop、readiness check の学びを整理。
- 2026-05-22: production / docs / client build の success と、実機 E2E が検出した runtime Docker image 欠落の観測面の違いを追記。
