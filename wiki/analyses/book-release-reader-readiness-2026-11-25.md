---
title: 書籍の発売までに整えたい広聴AIの読者体験 2026-11-25
type: analysis
summary: 書籍を読んだ人が設定なしで意見と根拠をたどれる入口を提案。v5の公開判断は発売日と独立させ、CSVの実地検証、組織の導入案内、利用者からのフィードバックを整える
sources:
  - broad-listening-book-source.md
  - meeting-minutes.md
  - source-code.md
  - slack-logs-repository.md
---

## 発売時に目指す状態

書籍で興味を持った人が、スマホで公開レポートを開き、論点を一つ見つけ、根拠の意見までたどれる。さらに試したい人には、自分のCSVで分析する道と、組織で導入を検討する道が見える。書籍に操作手順を載せないという既存の前提に沿い、操作案内は更新できるWeb側に置く。DD2030公式の[広聴AIページ](https://dd2030.org/kouchou-ai/)には事例とドキュメントへの入口があるので、ここを起点にできる。[[book-release-development-plan-2026-09]]より

1. **設定なしで結果を読む。** 最初に案内するレポートを一つ選び、収集時の問い、誰からどのように集めた声か、図から根拠の意見にたどる一例を添える。公開許諾された原文につなぎ、集めた声の論点や見落としに気づくための図であることを説明する。発売前には初見の3〜5人に、説明を受けずにスマホで公式ページから進み、5分で論点一つと根拠の意見一件を見つけられるか試す。[[issue-564-public-case-trust-layer-scope-2026-06-30]]より
2. **自分のCSVで試す。** ブラウザ版はサンプルCSVと手元のCSVの入口を案内し、推奨する実AI構成一つで、設定から分析、結果表示、書き出しまで通す。外部AIを選ぶ場合は、入力がどこへ送られるかを実行前に分かるようにする。検証が発売に間に合わなければ、公開レポートと既存の導入ガイドを案内する。自治体・企業向けには、サーバー版の構成の目安、費用とデータの扱いを一箇所からたどれるようにする。CLIは再現や自動化をしたい人に案内する。[[serverless-onboarding-2026-11-25]]より [[long-term-strategy-2026-11-02]]より
3. **安定版の準備を並走させる。** v5候補は、既存レポートの閲覧、新規レポートの作成、公開範囲、書き出しの回帰を確認し、利用者への変更点と更新手順を揃えてから出す。書籍の発売時はその時点で検証済みの安定版を案内する。公開用データに非公開の素材が混ざらないことや、同じ意見集合の件数が表示間で一致することを優先する。レビュー待ちのPRは、この読者経路と既存利用に影響するものから選ぶ。[[long-term-strategy-2026-11-02]]より [[verification-opportunities-2026-11-25]]より

発売後の反応を次の改善に使えるよう、事例報告やつまずきを返せる窓口を一つ案内する。初回にどこで止まったか、どんな問いやデータで使いたかったか、導入の条件は何かが分かると次の優先度をつけやすい。

## 2026-11-25 の観測

- [DD2030公式の書籍案内](https://dd2030.org/broad-listening/)はインプレスから発売予定と記載し、具体日は掲載していない。開発議事メモのtxtを同日に再取得し、先頭見出しは2026-07-27だった。Slackのリポジトリで、11月25日07:13 JST同期のmirror（2026-09-11〜11-25 JST、59チャンネル、更新されるmirror）を発売・刊行の語で確認した範囲では、確定日を確認できなかった。[[meeting-minutes]]より [[slack-logs-repository]]より
- 本体は同期済みのmain `03d07295` を参照。GitHubの最新安定版は[v4.2.0](https://github.com/digitaldemocracy2030/kouchou-ai/releases/tag/v4.2.0)、[M5](https://github.com/digitaldemocracy2030/kouchou-ai/milestone/1)のopenは貢献者一覧の[#1199](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1199)。公開用JSONとビューアの切替は[#1187](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1187)でmainに入っている。[[long-term-strategy-2026-11-02]]より
- ブラウザ版の初回案内は[ドラフトPR #13](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/13)、本体docsから組織版への案内更新は[PR #1245](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1245)で進行中。初回案内は狭い画面と模擬AIで操作確認済み。初見の読者と実AIでの完走が次の確認になる。[[serverless-onboarding-2026-11-25]]より

## Open Questions

- 最初のレポートをどれにするか。元の問いと収集範囲を公開情報から説明でき、読者が根拠の意見までたどれるものを選ぶ。
- 読者からの問い合わせや事例を既存のどの窓口で受けるか。

## Updates

- 2026-11-25。書籍からの現行導線を確認。[書籍Web版の「この本について」](https://broadlisteningbook.com/ja/about)からは DD2030 のトップにリンクする。[DD2030 のブロードリスニング総合ページ](https://dd2030.org/broad-listening/)からは書籍Web版と[広聴AI公式ページ](https://dd2030.org/kouchou-ai/)の両方へ進める。広聴AI公式ページは[活用事例](https://dd2030.org/kouchou-ai/case)・使い方・ドキュメントを案内しており、このページを前段の提案で想定していた。2026-05-04の議事メモには書籍Web版と公式サイトの相互リンク案がある。公開原稿のmain（[`52c9cac`](https://github.com/digitaldemocracy2030/broad-listening-book/commit/52c9cace24f69de370e753be9118bb76a012c2a5)）と公開ページからは、商業版の紙面に載るURLやQRコードの行き先は確認できていない。[[meeting-minutes]]より

### 日本語Web版トップからの導線案

- 2026-11-25。[日本語トップ](https://broadlisteningbook.com/ja/)と書籍サイトのmain `04054a2` を照合した。[web_build.py の render_index](https://github.com/lukec/broad-listening-book-site/blob/04054a2c453a39295cc7e9e72801cd5db6de254b/src/broad_listening_book_site/web_build.py#L2794-L2808) は書名・読書ボタン・区切り線・目次の順。幅390pxと1280pxで読書リンクの並びを確認した。日本語トップに限り、読書ボタンの下、目次の手前に「広聴AIで実際の意見を読む」と小さな案内を置く案。説明は「似た意見がどうまとまるか、公開レポートで確かめられます」程度にする。静的なリンク一つから始められる。[[broad-listening-book]]より
- 最初のリンクはレポート一件へ直接つなぐ。第一候補は [舞鶴2040「未来の舞鶴は、どんなまちになっていてほしいですか？」](https://maizuru2040.jp/kouchou-ai-reports/c479cdba-f3da-44d8-b096-08bdd335170f/)。[舞鶴市の取組案内](https://www.city.maizuru.kyoto.jp/shisei/0000013931.html)で背景を説明でき、公開ビューアはスマホ幅で開ける。短いお題は「リストで気になる話題を開き、意見を一つ読んでみる」。初見の利用者が自力でそこまで進めるかを掲載前に確かめる。組織での利用やCSV分析はその後の導入ガイドで案内する案。
- 書籍サイトにはすでに、本文の一節を選んで匿名で「視点を寄せる」機能がある。[本書の読みかたの「Web版の機能」](https://broadlisteningbook.com/ja/00_%E6%9C%AC%E6%9B%B8%E3%81%AE%E8%AA%AD%E3%81%BF%E3%81%8B%E3%81%9F.html#web-book-features) をスマホ幅で確認した。参加したい人はこの案内から本文へ戻れる。集まった声は [既存仕様](https://github.com/lukec/broad-listening-book-site/blob/main/spec/LISTEN-PLAN.md) の同意範囲で非公開分析し、書籍チームへの振り返りに役立てる案。公開体験は公開用レポートで提供する。
