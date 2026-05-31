---
name: windows-distribution-options
type: analysis
summary: "非専門家 Windows ユーザー向けの kouchou-ai 配布形態を、`setup_win.*` スクリプト / ランチャー exe / デスクトップアプリ / 完全単体 exe の 4 段階で整理。2026-05-31 時点で、完全単体 exe の前提 refactor として Node runtime を build-time assets に閉じ込める route が `#885` として追加された"
sources:
  - windows-distribution-gpt-brainstorm-2026-05-22.md
  - meeting-minutes.md
  - source-code.md
  - windows-powershell-default-installation.md
  - windows-setup-encoding-decision.md
  - docker-engine-wsl2-alternative-2026-05-23.md
  - slack-windows-single-exe-2026-05-31.md
  - node-runtime-free-windows-exe-2026-05-31.md
---

## 問い

[[kouchou-ai|広聴 AI]] を **Windows の非専門家にも届ける** ときに、どの粒度の「配布物」を正規入口にすべきか。`setup_win.bat` のような shell script レベルで止めるのか、独立した `kouchou-ai-launcher.exe` を作るのか、最終的に Docker 不要の単体 exe まで持っていくのか、という選択肢の差を整理する。

`usage-modes` の 2 軸（非専門家向け Web UI / 研究者・データサイエンティスト向け CLI）のうち、本 analysis は **非専門家向け Web UI モードの配布** に絞る。研究者向けは [[usage-modes]] が示すとおり `Mac/Linux + CLI`、Windows 研究者は `WSL2/Docker` 寄せで割り切れる。

## 4 段階の配布形態

[[windows-distribution-gpt-brainstorm-2026-05-22]] の GPT 整理に、kouchou-ai 側の現状作業を 1 段階追加して 4 段階に並べると次のようになる。

### 段階 1: `setup_win.*` スクリプト方式 (現状進行中)

- `setup_win.bat` を ASCII ランチャー、`setup_win.ps1` を日本語案内本体として分離する方針が `PR #863` で進行中（`Issue #731`）。`wiki/log.md` 2026-05-22 23:27 entry より
- この分離判断の理由は [[windows-setup-encoding-decision]] に整理した。要点は「文字化け」ではなく `cmd.exe` による日本語行のパース破綻を避けることにある
- この方針で依存する `powershell.exe` は、Microsoft Learn ベースでは Windows client 10 以降の既定インストール範囲に入る。したがって `Windows 10/11` 対象の配布導線としては比較的置きやすい前提である。一方で `pwsh` は標準前提にできない。[[windows-powershell-default-installation]]より
- 配布物は zip 展開で済む shell script。Docker Desktop と Git の前提は残る
- 過去の Windows 落とし穴（CRLF 改行・Docker Desktop の 4GB RAM デフォルト・Git 未導入）と直接対応する救済策。[[local-dev-setup]]より
- 利点: kouchou-ai 本体に対する変更が最小。実装・配布・保守コストが軽い
- 限界: ユーザーは依然として「.bat / .ps1 を二重クリックで実行」「Docker Desktop を別途インストール」「日本語コンソールエンコーディング」のような Windows 固有の地雷に触れる

### 段階 2: ランチャー exe (Docker Compose ラッパー)

- `kouchou-ai-launcher.exe` を起動 → Docker Desktop 起動確認 → `.env` 未生成なら API key 入力 → `docker compose up -d` 相当 → `localhost:4000` をブラウザで開く → 停止ボタンで `docker compose down`。[[windows-distribution-gpt-brainstorm-2026-05-22]]より
- 実装候補: Go / Tauri / Electron / .NET / Rust。Go か Tauri が候補に挙がっている
- 利点: Windows ユーザーはコマンドを 1 度も打たない。`.bat` / `.ps1` の文字化け・改行コード問題が消える
- 限界: 新たに言語スタック (Go / Rust / Node + Electron など) を kouchou-ai リポジトリに持ち込むことになる。配布バイナリの署名・更新も必要
- 現状: 着手なし。明示的な意思決定もまだない

### 段階 3: デスクトップアプリ化 (Tauri / Electron)

- 管理画面を WebView で包んで、見た目を「普通のデスクトップアプリ」にする
- 裏側ではなお FastAPI / `public-viewer` / Docker / `.env` / API key / 生成物保存先を管理する必要があるので、UX 改善はあるが配布難度は上がる
- 利点: 「ブラウザを使う」工程が消え、ユーザーから見るとアプリ起動 1 アクションで完結
- 限界: 段階 2 のすべてを抱えたまま、さらに UI 層が増える

### 段階 4: 完全な単体 exe (Docker 不要)

- Python API を PyInstaller / Nuitka で固め、Next.js を静的ビルドし、必要なランタイムを全部同梱
- kouchou-ai は分析系 Python 依存・ファイル入出力・長時間実行・場合により Ollama / GPU 利用も絡むので、署名・ウイルス対策誤検知・自動更新まで含めると保守コストが大きい。[[windows-distribution-gpt-brainstorm-2026-05-22]]より
- 利点: ユーザーは Docker Desktop すら不要
- 限界: kouchou-ai 本体を「ローカル単体実行しやすい構造」に再構築する必要があり、規模としては別プロジェクトになる
- 現状: 着手意図なし

### 段階 4a: Node runtime を消す前提 refactor

2026-05-31 に tokoroten / nishio の Slack 断片から、段階 4 を「Python と Node を両方同梱する」問題としてではなく、**Node を build-time に閉じ込め、frontend を SPA/static assets として Python/FastAPI から配信する**問題として再評価する案が出た。[[slack-windows-single-exe-2026-05-31]]より

current main の確認では、`apps/admin` の Node runtime 責務は server-side fetch、server actions、route handlers、CSP headers に寄っており、多くは既存 FastAPI endpoint への薄い wrapper と読める。`apps/static-site-builder` も Express で `pnpm run build:static` と zip を実行するだけなので、API そのものは Python に寄せられる。したがって、完全単体 exe の前提として **runtime Node なしで Web UI を動かす** issue `#885` を起票した。[[node-runtime-free-windows-exe-2026-05-31]]より

ただしこれは段階 4 の難しさを消すものではない。`apps/public-viewer` の revalidate / OGP / live viewer、on-demand static zip 出力、`analysis-core` の `torch` / `numba` / `scipy` / `umap-learn` などを含む Python packaging は残る。MVP も外部 API route だけでなく、軽量モデルを同梱して **API 契約不要で local 完結**する offline bundled-model route を比較すべき、という整理に更新した。[[node-runtime-free-windows-exe-2026-05-31]]より

## 正規入口を Docker Desktop に置く前提

段階 2-3 の路線は、いずれも **Docker Desktop (WSL2 backend) を正規入口にする** ことを暗黙の前提にしている。ここを変えると段階の意味付けも変わる。

- [[usage-modes]] と [[local-dev-setup]] の現状は Docker Compose 前提
- [[windows-distribution-gpt-brainstorm-2026-05-22]] も「Docker Desktop を入れる。内部では WSL2 を使う」というドキュメントの書き方を推奨している
- WSL2 を正規入口にするのは開発者向けに留め、非専門家には WSL2 という用語を主役化しない、というのが妥当
- Docker Desktop のライセンス（大企業 / 政府機関では有料サブスク）はドキュメントに残しておくべき注意点。自治体・行政展開時にここが障害になる可能性がある

## ランタイム基盤の選択軸: Docker Desktop / Docker Engine in WSL2

「段階 1〜4」とは別の軸として、**Docker 実行基盤として何を入れるか** という選択がある。これは 4 段階のどこにいても直交する軸であり、[[docker-engine-wsl2-alternative-2026-05-23]] で GPT が示した「Docker Desktop を使わない経路」を整理すると次のようになる。

### ルート A: Docker Desktop (WSL2 backend)

- 現状の `docs/getting-started/windows-setup.md` と段階 1 の `setup_win.*` 系が前提にしているルート
- 利点: GUI / daemon 起動 / port forwarding / メモリ管理 / WSL integration を Docker Desktop が肩代わりするので、非専門家でも比較的成功率が高い
- 限界: 大企業・政府機関・特定規模以上の組織では有料サブスクリプションが必要になる場合がある。Docker Desktop のインストール自体が組織端末管理ポリシーで弾かれることもある

### ルート B: WSL2 Ubuntu に Docker Engine + Compose plugin

- Docker Desktop を経由せず、WSL2 Ubuntu の中に `docker-ce` / `docker-ce-cli` / `containerd.io` / `docker-compose-plugin` を apt で直接入れて `docker compose up` する構成。[[docker-engine-wsl2-alternative-2026-05-23]]より
- 利点: Docker Desktop ライセンスの制約を避けられる。Docker Engine 側は OSS 配布条件のまま
- 限界: WSL2 / Ubuntu 導入、systemd 有効化、Docker daemon 起動、`docker` group 設定、Windows / WSL のパス混乱、port forwarding、メモリ診断、組織 PC の VPN / セキュリティソフト制限まで、利用者が自力で扱う必要が出る。「支払いは避けられるが、サポートコストは上がる」。[[docker-engine-wsl2-alternative-2026-05-23]]より
- 現状: kouchou-ai 側の正規 docs / setup script は未対応。`setup_win.bat` / `setup_win.ps1` でも対象外

GPT は「迷ったら Docker Desktop、組織 PC・行政・大企業・ライセンス確認が必要なら WSL2 + Docker Engine」という入口分岐を提案している。これは現状 main の docs 構成（Windows ネイティブ + Docker Desktop 一本）からは一歩踏み込む変更で、kouchou-ai 側の意思決定はまだない。

### 段階軸とランタイム軸の関係

段階 1〜4 とランタイム A / B は組み合わせ可能だが、現実的に意味のある組み合わせは限られる。

- 段階 1 (`setup_win.*`) × ルート A: 現状進行中の本線
- 段階 1 × ルート B: 「WSL2 Ubuntu 上で `docker compose up` する手順」を docs として正規化する案。setup script というより docs / playbook で支援する形になる
- 段階 2 (ランチャー exe) 以降 × ルート A: GPT が推した「ランチャー exe で Docker Desktop を操作する」案
- 段階 2 以降 × ルート B: ランチャー exe が WSL2 内 Docker Engine を扱う案。Windows ネイティブ exe から WSL2 内のプロセスを起動する形になり、設計難度が一段上がる

kouchou-ai の主要利用者層（自治体・政党・運用担当者）の中で「Docker Desktop の制約に直撃する側」がどれだけ多いかで、ルート B を **補助ルート** に留めるか **主要ルート** へ昇格させるかが変わる。

## 現状の作業との対応関係

- main で進んでいる作業は **段階 1**（`setup_win.bat` / `setup_win.ps1`）まで
- 段階 2 のランチャー exe は GPT のブレスト以外に明示提案が見当たらない（[[meeting-minutes]] でも個別議論には到達していない）
- 段階 3-4 は現状の体制 / 工数では現実的でない

つまり「Windows ユーザー向け体験」をどこまでやるかは、コードレベルでは段階 1 で進行中、戦略レベルでは段階 2 以降は **未着手・未決の open question** として残っている。

## 判断材料

段階 2 以降に進むべきかは、次のような判断軸で考えると整理しやすい。

1. **対象ユーザーの広さ**: 「Windows でも CLI を打てる人」が大半なら段階 1 で十分。「ダブルクリックで動かしたい層」を取りに行くなら段階 2 が要る
2. **配布側コスト**: 段階 2 以降は新スタック導入・コード署名・ウイルス対策誤検知対応・自動更新が必要。OSS 体制のキャパシティに見合うか
3. **Docker Desktop 依存の許容度**: 行政・大企業展開を意識するなら、Docker Desktop ライセンスの説明が必要。段階 4 はその回避策にもなり得る
4. **既存路線との整合**: 現在の `Zip + setup_win.* + Web UI` の延長で困っているのか、別レーンとして exe を作るのか。[[usage-modes]] の「`Zip + setup.bat + browser open` をどこまで正式サポートするか」の Open Question と連動する

## Open Questions

- 非専門家向け Windows 体験のゴールを `setup_win.*` 系で打ち止めるか、段階 2 (ランチャー exe) へ進むかを正式に意思決定するタイミング
- `#885` の Node runtime 排除 route を段階 4 の前提 refactor として進めるか、それとも段階 2 の Docker Desktop launcher route を優先するか
- 段階 2 に進む場合の言語スタック (Go / Tauri / Electron / .NET) の選定。kouchou-ai 本体の保守者層と乖離しすぎないこと
- Docker Desktop ライセンス前提のままで自治体・行政展開を続けられる範囲。回避策が必要になる場面の見極め
- ルート B（WSL2 Ubuntu + Docker Engine）を「上級者向け補助ルート」に留めるか、主要利用者層のライセンス事情を踏まえて「主要ルート」へ昇格させるか
- Mac の非専門家向け配布をどう扱うか。Windows と同等の `setup_mac.*` 整備、または別物として扱うか

## Updates

- 2026-05-31: tokoroten / nishio の Slack 議論を受け、完全単体 exe の前提 refactor として Node runtime を build-time assets に閉じ込める route を追加。`#885` を起票し、詳細は [[node-runtime-free-windows-exe-2026-05-31]] に分離
- 2026-05-31: `#885` の MVP を external API route / offline bundled-model route の 2 本比較に修正。単一バイナリの価値は Docker なしだけでなく API 契約不要にもある
- 2026-05-22: 初回作成。`setup_win.*` 進行と GPT ブレストを突き合わせ、段階 1〜4 の整理と現状判断材料をまとめた
- 2026-05-23: ランタイム基盤の選択軸（Docker Desktop / Docker Engine in WSL2）を段階軸とは直交する第 2 軸として追記し、ルート B を主要ルートに昇格させるかを Open Question に追加
