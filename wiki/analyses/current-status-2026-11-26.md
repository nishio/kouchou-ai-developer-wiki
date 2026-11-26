---
title: 広聴AIの開発状況 2026-11-26
type: analysis
summary: 11月25日に本体の19本のPRがマージされた。残る8本は全件承認待ちで4本に競合がある。ブラウザ版の初回ガイドと原文表示は反映済み。v5の公開仕様告知と貢献者一覧は準備中。
sources:
  - source-code.md
  - slack-logs-repository.md
  - meeting-minutes.md
---

11月26日16時台（JST）に本体の main と GitHub を照合した。11月25日に19本のPRが main に入り、LLM 直接グルーピングの件数指定・全件一括、階層リストからの元コメント表示、事前計算済みの対立軸を読むビューが加わった。最新の安定版は10月26日公開の v4.2.0。[[source-code]]より。[確認した本体コミット](https://github.com/digitaldemocracy2030/kouchou-ai/commit/efbd0f285cbc92e72c7c3f8d88924841d8ec5e1b)・[最新安定版](https://github.com/digitaldemocracy2030/kouchou-ai/releases/tag/v4.2.0)

## 初めて使う人の入口

書籍の読者向けガイドからブラウザ版を案内するようになった。ブラウザ版では設定なしでサンプルを開き、検索した意見から公開された元の回答までたどれる。初見の利用者がスマホでこの操作を完了できるか、自分のCSVで実際のAIに接続して分析を終えられるかは、今後の確認項目。11月25日のSlackでもDD2030のブラウザ版をお試しの入口とする方向に元作者が賛同している。[[serverless-onboarding-2026-11-25]]、[[slack-logs-repository]]より。[書籍を読んだ方へ](https://digitaldemocracy2030.github.io/kouchou-ai/book)・[ブラウザ版の初回ガイド](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/13)・[元の回答を開く変更](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/16)

## 本体の未マージPR

GitHubで開いている本体PRは8本、Issueは65件。8本とも承認が必要で、報告されたCIチェックに失敗・実行中はなかった。[[source-code]]より。[本体のPR一覧](https://github.com/digitaldemocracy2030/kouchou-ai/pulls)

| マージ前の状態 | PR |
| --- | --- |
| 競合なし、承認待ち | [意見検索から所属グループを開く #1270](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1270)、[散布図の輪郭の重なりを分割 #1271](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1271)、[編集可能なPowerPoint出力 #1268](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1268)、[論点を切り直して共有 #1267](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1267) |
| 競合あり | [ポンチ絵の出力 #1266](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1266)、[輪郭を初期表示で隠す #1260](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1260) |
| ドラフト、競合あり | [狭い画面での散布図 #1252](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1252)、[Polisの取り込み #1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248) |

研究会で「見たい意見が見つからない」と挙がった課題に直接対応するのが #1270。散布図では #1260 と #1271 が同じ課題に異なる方法で対応している。後から出た #1271 は輪郭を表示して重なりを分ける案で、モバイル実機での性能確認が残る。ブラウザ版で唯一開いているPRは、輪郭を初期表示で隠す方の案。[[scatter-cluster-contours-2026-11-25]]より。[研究会の要望 #1205](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1205)・[輪郭の設計課題 #1259](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1259)・[ブラウザ版 #14](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/14)

## v5の準備

M5に属する2件が個別のIssueでopenだった。公開用JSONの出力とAPIは実装済みで、#1178には v5.0 のリリースノートで利用者に公開仕様を告知する作業が残る。#1199 はコード以外の貢献も含めた貢献者一覧の準備。[[source-code]]より。[公開仕様の告知 #1178](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1178)・[貢献者一覧 #1199](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1199)

## 観測範囲

- 本体は main `efbd0f28`、ブラウザ版は main `ec0c88a`。PRの状態は11月26日にGitHubで確認した。[[source-code]]より。
- Slackは11月26日06:29 JST同期のミラーで、11月19日以降の開発・アルゴリズム開発チャンネルを同日に読んだ。議事録は11月26日16:10 JSTにtxtを再取得し、先頭は引き続き7月27日だった。[[slack-logs-repository]]、[[meeting-minutes]]より。

## Open Questions

- 通常レポートの輪郭の既定表示を本体とブラウザ版でどうそろえるか。モバイル実機で分割の負荷が許容できるか。
