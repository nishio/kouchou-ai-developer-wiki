---
name: docker-engine-wsl2-alternative-2026-05-23
type: source
summary: "nishio と外部 GPT の対話。Docker Desktop を避ける選択肢として、WSL2 Ubuntu の中に Docker Engine + Docker Compose plugin を直接入れる構成と、その UX コストおよび 2 本立て docs 案を整理したブレスト"
sources:
  - docker-engine-wsl2-alternative-2026-05-23.txt
---

## 何のソースか

`raw/docker-engine-wsl2-alternative-2026-05-23.txt` は、[[nishio]] が外部 GPT に「Docker Desktop を使わずに済む選択肢はあるか」を尋ねた対話の生ログ。前日 [[windows-distribution-gpt-brainstorm-2026-05-22]] の続きで、Docker Desktop ライセンス問題が自治体・大企業展開で障害になり得るという論点をさらに掘ったもの。kouchou-ai 開発者の合意でも議事録でもなく、外部 LLM のブレスト出力なので、無批判には採用しない（`CLAUDE.md` の運用方針）。

## 論点: Docker Desktop を使わない経路

GPT は「Docker Desktop を避ける選択肢として、**WSL2 Ubuntu 内に Docker Engine + Docker Compose plugin を直接入れる**」構成を成立する選択肢として挙げている。

構成イメージは

```text
Windows
  └─ WSL2 Ubuntu
       ├─ Docker Engine
       ├─ Docker CLI
       ├─ Docker Compose plugin
       └─ kouchou-ai repo
```

で、起動は

```bash
cd ~/kouchou-ai
cp .env.example .env
docker compose up
```

GPT が根拠として挙げているのは Docker 公式 docs:

- Docker Desktop のライセンスは商用 / 大規模組織で有料だが、Docker Engine 側の OSS 配布条件は別枠
- Ubuntu 向け Docker Engine は apt repository から `docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin` を入れる手順がある
- Compose plugin にも Linux CLI 向けの個別インストール手順がある

## UX コスト

GPT は同時に「**一般ユーザー向け正規入口にするには弱い**」と注意している。Docker Desktop が肩代わりしていたものを自分で扱う必要が出るため、詰まりやすい場所として:

```text
- WSL2 / Ubuntu の導入
- systemd 有効化の有無
- Docker daemon の起動確認
- sudo なしで docker を使うための docker group 設定
- Windows 側ファイルパスと WSL 側ファイルパスの混乱
- ポート公開 localhost:3000 / 4000 / 8000 の確認
- メモリ不足時の診断
- VPN / セキュリティソフト / 組織PC制限
```

を列挙している。要するに「支払いは避けられるが、サポートコストは上がる」。

## GPT が示した docs 方針

GPT の推奨は **2 本立て**:

```text
標準入口:
  Docker Desktop を使う
  対象: 個人・小規模組織・Docker Desktop 利用が許可されている組織

組織向け / Docker Desktop 非利用入口:
  WSL2 Ubuntu に Docker Engine を直接入れる
  対象: 自治体・大企業・Docker Desktop ライセンスや端末管理ポリシーに引っかかる利用者
```

Windows ガイドにはこのように書く案を提示している:

```text
A. Docker Desktopを使う方法
  最も簡単。個人・教育・非商用OSS・小規模組織で推奨
  ただし所属組織の規模や利用目的によっては有料ライセンスが必要

B. Docker Desktopを使わず、WSL2 UbuntuにDocker Engineを入れる方法
  Docker Desktop が難しい組織向け
  手順はやや複雑だが Docker Engine と Compose plugin で起動できる
```

GPT の判断は「Docker Desktop 回避ルートを **上級者・組織管理者向けの正規サポート手順** として置く」。「迷ったら Docker Desktop、組織 PC・行政・大企業・ライセンス確認が必要なら WSL2 + Docker Engine」という入口分岐を提案している。

## kouchou-ai での現状との照合

- [[local-dev-setup]] / [[windows-distribution-options]] の前提は「Docker Desktop (WSL2 backend) を正規入口にする」だった。GPT のこの提案は **Docker Desktop 非利用ルートを正規サポート手順として用意する** という拡張に相当する
- 現状 main の docs (`docs/getting-started/windows-setup.md`) も、Windows ネイティブ + Docker Desktop 前提で書かれている。Docker Engine in WSL2 ルートを正規手順に追加する動きはまだない
- 直近の [[windows-real-machine-e2e-lessons]] では Docker Desktop の image build / runtime build を Windows 実機 E2E で検証する path に踏み込んでいる。これは Docker Desktop ルートを正規入口に据える方向の補強であり、Docker Engine in WSL2 を E2E でカバーする話とは別レーン

## 鵜呑みにできない部分

- GPT は Docker Desktop ライセンス条件を「個人・教育・非商用 OSS・小規模組織は無料、それ以外は有料」と粗く要約しているが、実際の閾値・対象組織種別・契約条件は Docker 公式の最新条文を都度確認する必要がある
- Docker Engine in WSL2 構成は「OSS 配布条件は変わらない」とあるが、Docker / Mirantis の商標・配布ポリシー、`docker-ce` の license 詳細までは GPT は深掘りしていない
- 「一般ユーザーには Docker Desktop」「組織管理者には Docker Engine in WSL2」という分け方は妥当に見えるが、kouchou-ai の主要利用者層（自治体・政党・運用担当者）は **Docker Desktop の制約に直撃する側** である可能性もあり、「上級者向け補助ルート」ではなく「主要ターゲット向け本線」の可能性まで含めて検討する必要がある
- WSL2 内の Docker Engine 構成はセットアップ品質の検証がまだ無く、kouchou-ai が想定する `setup_win.bat` / `setup_win.ps1` 系のスクリプトでは現状カバーされない

## Updates

- 2026-05-23: 初回作成。Docker Desktop 回避策として Docker Engine in WSL2 ルートを GPT が提案した内容を、kouchou-ai 側の現状 docs / E2E 整備状況と突き合わせて記録
