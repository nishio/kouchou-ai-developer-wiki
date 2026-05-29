---
type: source
summary: "2026-05-29 時点の Docker 公式文書確認。Docker Desktop は大規模 enterprise の商用利用や政府系 entity では paid subscription が必要になり得るため、自治体・大企業向け Windows 導線ではライセンス確認を前提にする必要がある"
sources:
  - https://docs.docker.com/subscription/desktop-license/
  - https://docs.docker.com/get-started/get-docker/
  - https://www.docker.com/legal/docker-subscription-service-agreement/
---

## 何のソースか

2026-05-29 に Docker 公式の `Docker Desktop license agreement`、`Get Docker`、`Docker Subscription Service Agreement` を確認し、Windows セットアップガイドで Docker Desktop を前提にする時のライセンス注意点を整理した source。[[issue-877-windows-setup-guide-scope-2026-05-29]] のコメントで出た「自治体・大企業では Docker Desktop を入れられない / 有償になり得る」という懸念を、公式文書に照らして扱うために追加する。

## 確認したこと

Docker 公式の Get Docker は、Docker Desktop の商用利用について、大規模 enterprise では paid subscription が必要だと明記している。閾値は「従業員 250 人超」または「年商 1,000 万 USD 超」と説明されている。[Get Docker](https://docs.docker.com/get-started/get-docker/) より

Docker Desktop license agreement は、Docker Desktop が無料で使える範囲を小規模企業、個人利用、教育、非商用 OSS に限定し、paid subscription が必要な例として larger organization の professional use、government entities、free tier を超える commercial use を挙げている。[Docker Desktop license agreement](https://docs.docker.com/subscription/desktop-license/) より

Docker Subscription Service Agreement は `Government Entity` を広く定義している。[Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement/) より

したがって、kouchou-ai の Windows ユーザー向け docs で Docker Desktop を標準入口にする場合、「個人利用や小規模組織なら楽な標準手順」とだけ書くのは不十分である。自治体・行政・大企業・組織管理端末では、Docker Desktop の利用可否と契約条件を所属組織で確認する必要がある。

## kouchou-ai への含意

`docs/getting-started/windows-setup.md` の Docker Desktop 前提は、個人や小規模組織の初回体験としては現実的だが、kouchou-ai の想定利用者に自治体・行政・大企業が含まれるなら、ライセンスと端末管理ポリシーを単なるトラブルシュートではなく、事前条件として扱う必要がある。

Docker Desktop を避ける構成としては、[[docker-engine-wsl2-alternative-2026-05-23]] が WSL2 Ubuntu 内に Docker Engine + Compose plugin を入れるルートを整理している。ただしこれは Docker Desktop より UX コストが高く、現状の `setup_win.bat` / `setup_win.ps1` ではカバーしていない。したがって beginners guide に混ぜるより、組織管理者・技術者向けの別ルートとして扱う方が安全である。[[docker-engine-wsl2-alternative-2026-05-23]]より

## Open Questions

- 日本国内の自治体・行政機関が Docker の `Government Entity` 定義にどう該当するかは、Docker 公式条文だけでなく各組織の調達・法務判断に依存する。
- kouchou-ai として Docker Desktop 回避ルートを公式サポートする場合、WSL2 Ubuntu + Docker Engine の実機検証を誰がどこまで担うか。
- Windows 初心者向けガイドにライセンス注意をどの粒度で載せるか。詳しすぎると離脱点になるが、隠すと自治体・大企業で詰まる。

## Updates

- 2026-05-29: 初回作成。Docker Desktop の paid subscription 条件と government entity 注意を、公式文書ベースで整理した。
