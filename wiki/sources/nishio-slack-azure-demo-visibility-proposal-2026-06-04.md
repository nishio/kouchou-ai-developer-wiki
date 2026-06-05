---
name: nishio-slack-azure-demo-visibility-proposal-2026-06-04
type: source
summary: 2026-06-04 22:00 / 22:29 nishio の dd2030 Slack 投稿。docs entry 3 段階 spine の改訂版と、Azure デモサイトを docs から動線化する具体案 4 問を Ohki さんに投げかけている
sources:
  - dd2030-slack-2026-06-04
---

## 文脈

[[kouchou-ai-docs-entry-restructure-2026-06-03]] と [[nishio-docs-entry-restructure-discussion-2026-06-03]] で出た「セットアップが docs の入口になっているのを改める」議論の翌日、nishio が dd2030 Slack で同テーマをさらに明確化した投稿を 2 本出した。前段は spine の refinement、後段は Azure デモサイトの動線について Ohki さんに 4 問の具体質問を投げている。

last_read: 2026-06-04
coverage: 2026-06-04 22:00 と 22:29 の 2 投稿のみ

## 22:00 投稿: docs spine の refinement

[抜粋 verbatim]

> ドキュメントのあるべき形を考えていたんですけど、現状getting-startedで広聴AIを手元のマシンにセットアップする方法の話がされる構成ですが、これがソフトウェアエンジニア視点に狭まっているのがよくないのではないかという気持ちになりました。
>
> 改めて考えたらこういう構造になるのが適切かなと思います。
>
> 1: 広聴AIに興味がある人
> - まず公開されているデモサービスのビューワーでレポートを見てみよう(Webレポートの使い方解説)
> - dd2030以外のレポートを公開しているサイト・自治体へのリンク集
>
> 2: 自分も自分の持ってるデータでこのレポートを作ってみたい、となった人
> - 選択肢1: 誰かが建ててくれたサーバを使う(dd2030がサービス提供するならここ)
> - 選択肢2: サーバを立ててくれる人を探す(引き受ける気がある人がいればここに連絡先リストを置くとかする)
> - 選択肢3: 自分でサーバを建てる(技術力と適切な計算環境が必要)
>
> 3: 自分でサーバを建てたい人
> - ここで従来のgetting-startedになる

### 既存 analysis との差分

[[kouchou-ai-docs-entry-restructure-2026-06-03]] にあった spine は tier 2 が「(a) managed / (b) self-host」の 2 択だったが、本投稿では **「(b') サーバを立ててくれる人を探す」が間の選択肢として追加** されている。仲介者・代行者・組織内エンジニアに頼む経路を明示する。これは [[broadlistening-tool-ecosystem-vision]] の「組織内デモ役」と「WebUI 開発者」の境目に当たる読者像。

## 22:29 投稿: Azure デモサイトを docs から動線化する 4 問

[抜粋 verbatim]

> @Shingo OHKI 現状のAzureのデモサイトってドキュメントからはっきりと動線がない状態だと思うんですけど、ドキュメントからリンクをすることについてどう思いますか？(ふわっとした質問)
>
> ふわっとしてない方が良い場合ように噛み砕いてみました:
>
> Q1: ビューワーを公開してサンプルのレポートを見せるのは問題がないのでは
> Q2: admin画面を公開することに関して、ユーザがAPIキーを入力して使うコードがもうmainに入っているのでコスト的な問題はないはず。「共用環境であり全ての人に強要されるから秘密情報を入れないでね」と明示すればOKではないか？
> Q3: 「共用環境であり全ての人に強要されるから秘密情報を入れないでね」ではお試しできないよ！という自治体さんに対して、大木さん他Github adminがワンクリックしたら1ヶ月間の専用試用環境が立ち上がるような構成にするという案はどうか？
> Q4: 試用期間を超えて365日稼働を保証するSaaSは目下のところ大木さんとしてはやる気はないという理解であっているか？

注: 22:29 投稿の「強要されるから」は文脈上「共有されるから」の typo と読める。本 source では原文を verbatim 保持し、派生 analysis 側では「共有される」の意で扱う。

### 関連事実

- Q2 の「ユーザが API キーを入力するコードが main に入っている」は既存実装と整合する。Issue #660 (2025-07-30 merge) で admin form 入力経路、PR #868 (2026-05-29 までに merge) で `USER_API_KEY` plumbing が main に入っている。[[llm-providers]] / [[meeting-report-2026-05-25]] より
- Q3 の「1 ヶ月専用試用環境」は、[[open-decisions]] A2 で「やるならユーザごとに現 Azure デモ環境相当を丸ごと複製する方向」と書かれていたものを、Github admin による on-demand provisioning として具体化している。誰が provisioning をトリガーするかを Github admin (大木さん他) と名指ししている点が新しい
- Q4 は確認質問。365 日稼働 SaaS は dd2030 体制不足で先送り中（[[deployment]] / [[open-decisions]] A2）という現状認識を、Ohki さんから明示確認したい意図と読める

## 関連

- [[kouchou-ai-docs-entry-restructure-2026-06-03]]
- [[nishio-docs-entry-restructure-discussion-2026-06-03]]
- [[azure-demo-public-visibility-proposal-2026-06-04]] (本投稿に基づく分析)
- [[open-decisions]] A2
- [[deployment]]
- [[broadlistening-tool-ecosystem-vision]]
