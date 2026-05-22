---
name: windows-distribution-gpt-brainstorm-2026-05-22
type: source
summary: "nishio と外部 GPT の対話メモ。Windows ユーザー向け配布形態を `exe` 単体化か Docker Compose ランチャーか、また正規入口を Docker Desktop と WSL2 のどちらに据えるか、という 2 つの論点を整理したブレスト"
sources:
  - windows-distribution-gpt-brainstorm-2026-05-22.txt
---

## 何のソースか

`raw/windows-distribution-gpt-brainstorm-2026-05-22.txt` は、[[nishio]] が外部の GPT に対して「kouchou-ai を Windows 用の exe にできるか」「Docker Desktop と WSL2 のどちらを正規入口にするか」を尋ね、GPT が回答した対話の生ログ。kouchou-ai 開発者の中での合意でも、議事録でもなく、**外部 LLM のブレスト出力**。判断材料にはなるが、無批判に採用しない（`CLAUDE.md` の運用方針）。

## 論点 1: Windows 用 exe の現実的な段階

GPT は kouchou-ai の現状（`api` FastAPI / `public-viewer` `admin` Next.js / Docker Compose 前提）を踏まえ、Windows exe 化を 3 段階に分けて提案している。

1. **ランチャー exe (推奨)**
   - `kouchou-ai.exe` を起動 → Docker Desktop 起動確認 → `.env` 未生成なら API key 入力 → `docker compose up` 相当 → ブラウザで `localhost:4000` を開く → 終了時に `docker compose down`
   - 実装候補: Go / Tauri / Electron / .NET。GPT は Go か Tauri を推している
   - 「中身は今の Docker 構成のまま、Windows ユーザーにコマンドを打たせない」方式
2. **デスクトップアプリ化 (Tauri / Electron)**
   - 管理画面を WebView で包む。ただし裏側で結局 FastAPI / Next.js / Docker / `.env` / API key / 生成物保存先を管理する必要があり、UI 体験は改善するが配布難度は上がる
3. **完全な単体 exe (PyInstaller / Nuitka + Next.js 静的ビルド)**
   - Docker 不要にする方式。kouchou-ai は Python 分析依存・ファイル入出力・長時間実行・場合により Ollama / GPU まで絡むので、署名・ウイルス対策誤検知・自動更新まで含めると保守コストが高い

GPT の結論は「**完全単体 exe ではなく、Docker Compose を操作する Windows ランチャー exe**」。最小仕様は

```text
kouchou-ai-launcher.exe
  - 初回起動時に OpenAI API key を入力
  - .env を生成
  - Docker Desktop の起動確認
  - docker compose pull / up -d
  - 管理画面を開く
  - ログ表示
  - 停止ボタン
```

## 論点 2: Docker Desktop か WSL2 か

GPT の結論は「**正規入口は Docker Desktop (WSL2 backend)**」。ドキュメント上は「Docker Desktop を入れる。内部では WSL2 を使う」と説明する。

理由として GPT が挙げているのは:

- kouchou-ai は Docker Compose 前提の Web アプリ構成で、README も Docker 前提
- Docker 公式が Windows での標準導線として Docker Desktop (WSL2 backend) を案内している
- WSL2 を正規入口にするとユーザーが distro / shell / WSL integration の概念に触れる必要があり、非開発者には説明コストが高い

GPT は「Docker Desktop vs WSL2 は対立ではない」と注意している。Docker Desktop は内部で WSL2 を使う構成が標準で、WSL integration を有効化すれば WSL distro 内から `docker` CLI を直接使える。したがってドキュメント構成は

```text
Windowsで使う
  1. 一般ユーザー向け: Docker Desktop で起動する
  2. 開発者向け: WSL2 Ubuntu で開発する
  3. トラブルシュート: Docker Desktop / WSL2 / ポート / メモリ
```

と二本立てにし、一般ユーザーには WSL2 を主役にしない、というのが提案。

注意点として GPT は、Docker Desktop のライセンス条件（大企業・政府機関では有料サブスク必要）と、厳格な隔離が要る環境では Hyper-V / Enhanced Container Isolation も選択肢に残ることを挙げている。

## kouchou-ai での現状との照合

- [[usage-modes]] は既に「非専門家向けには `Zip + setup.bat + Web UI` に近い入口」「研究者向けは `Mac/Linux + CLI` 正規入口で、Windows 研究者は `WSL2/Docker` 寄せでよい」という二系統の整理に到達している。GPT の提案する「ランチャー exe / Docker Desktop 正規入口」は **非専門家向けレーンの強化案** として既存方針と方向性は揃っている
- [[local-dev-setup]] の「Windows ユーザ向けの落とし穴」節は、Docker Desktop の 4GB RAM デフォルトでパイプラインが死ぬ、`entrypoint.sh` の CRLF 改行で起動失敗、利用専用ユーザは Git すら入っていない、といった実地観測を記録している。ランチャー exe / `setup_win.*` 整備が必要な動機の一次根拠になる
- 2026-05-22 の log では `Issue #731` の Windows setup 文字化け対応が `PR #863` で進行中。`setup_win.bat` を ASCII ランチャー化し、`setup_win.ps1` を日本語案内本体に分離する方針に切り替えた。これは GPT の言うランチャー方式の **`.bat` / `.ps1` 版** に相当する段階で、Tauri / Go のような言語ランタイム同梱までは踏み込んでいない

## 鵜呑みにできない部分

- GPT は外部参照（Docker 公式 docs / Microsoft Learn）を引いているが、本ソースを引用すること自体が kouchou-ai プロジェクトの公式判断ではない
- 「Tauri / Go がよさそう」「Electron は重い」のような技術選定の好みは、kouchou-ai の運用体制・既存 OSS スタック（Python / Node / Docker）と合わせて検討すべきで、GPT の判断は出発点に留める
- ライセンス（Docker Desktop の商用条件）の扱いは、自治体・行政・大企業展開時の検討事項として残るが、本ソース内では一般論のみ
- 現在 main に入っているのは `setup_win.bat` / `setup_win.ps1` 系のスクリプト方式で、GPT が言うような独立した exe ランチャーは未実装

## Updates

- 2026-05-22: 初回作成。GPT ブレストの内容を kouchou-ai 側の `usage-modes` / `local-dev-setup` / 進行中の `setup_win.*` 作業と突き合わせて記録
