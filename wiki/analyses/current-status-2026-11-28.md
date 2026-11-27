---
title: 広聴AIの開発状況 2026-11-28
type: analysis
summary: 11月27日に本体のPR4本（意見検索、輪郭の分割、PowerPoint書き出し、意見の切り直しと共有）がマージされた。残るPRは5本で、全件が承認待ちで競合はない。研究会の運営者がワークショップ由来のIssueに回答した。Dependabotの未対応アラートは11月17日以降に30件まで増え、対応するIssue・PRはまだない。
sources:
  - source-code.md
  - slack-logs-repository.md
  - meeting-minutes.md
---

11月28日03時台（JST）に本体の main と GitHub を照合した。前回（[[current-status-2026-11-26]]）からの変化は次のとおり。

- 11月27日に、承認待ちだった4本が main に入った。最新の安定版は引き続き10月26日公開の v4.2.0。[[source-code]]より。[確認した本体コミット](https://github.com/digitaldemocracy2030/kouchou-ai/commit/77cb3f82b84067c2568f48ea51ce7d85adc81a04)・[最新安定版](https://github.com/digitaldemocracy2030/kouchou-ai/releases/tag/v4.2.0)
- 研究会の運営者が、ワークショップ由来の Issue への質問に答えた。
- Dependabot の未対応アラートが大きく増えている。

## main に入ったもの

| 変更 | PR | 元の Issue |
| --- | --- | --- |
| 公開レポートから意見を直接検索し、所属グループを開く | [#1270](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1270) | [#1205](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1205) |
| 散布図でクラスタの輪郭が重なる部分を分割する | [#1271](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1271) | [#1259](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1259) |
| サーバ版のレポートを、編集できる PowerPoint に書き出す | [#1268](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1268) | [#1264](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1264) |
| 公開ビューアで意見を対話的に切り直して共有する | [#1267](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1267) | [#1263](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1263) |

輪郭については、初期表示で隠す案（[#1260](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1260)）が11月26日に閉じられ、表示したまま重なりを分割する #1271 に一本化された。ただしブラウザ版では、隠す案の [PR #14](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/pull/14) が開いたまま残っている。#1259 も、ブラウザ版の扱いを追うために open のまま。[[scatter-cluster-contours-2026-11-25]]より

merge 後の main では、テスト・ビルド・CodeQL・docs の配信がすべて通った。途中の commit で取り消された実行が 2 件あるが、どちらも直後の commit で走り直している。

## 本体の未マージPR

開いている本体 PR は5本、open の Issue は63件。5本とも承認待ちで、競合はなく、報告された CI チェックに失敗はない。[本体のPR一覧](https://github.com/digitaldemocracy2030/kouchou-ai/pulls)

| マージ前の状態 | PR |
| --- | --- |
| 承認待ち | [ポンチ絵の出力 #1266](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1266)、[既存レポートのプロンプトを新規作成で読み込む #1272](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1272)、[散布図で選んだグループの意見をリストで開く #1273](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1273) |
| ドラフト | [狭い画面での散布図 #1252](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1252)、[Polisの取り込み #1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248) |

前回は競合があった #1266・#1252・#1248 も、main を取り込んで競合が解けた。

- #1272 は、プロンプトだけを読み込む作りになっている。分析方法・モデル・クラスタ数のような AI 設定も合わせて読み込むかは、PR 本文で判断を求めている。
- #1273 で、[#1207](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1207) の「点をクリック → 説明のボタン → リスト」の流れについて、起票者から「ひとまずはこれで事足りそう」と回答があった。輪郭（区画）をクリックして開く対応は、今は必要ない。

## 研究会の運営者からの回答

自治体の研究会のワークショップで出た要望について、運営者（Shingo OHKI）が11月26〜27日に各 Issue で質問に答えた。[[municipal-workshop-issues-triage-2026-11-24]]より

- **使われ方**：参加者が手元の PC でレポートを見たのではない。1人が操作する画面を大きなモニタに映し、皆で見ていた（[#1211](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1211)・[#1212](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1212)）。「レポートの読み方」の折りたたみはあったが、参加者が気づいたかは分からない。開発に関わる人がその場にいると、説明は読まずにその人に聞く、という指摘もあった。
- **検索**：フィルタのアイコンから検索できることには、運営者自身も気づけなかった（[#1205](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1205)）。図の上から直接検索できる #1270 は、この課題への対応にあたる。
- **プロンプトの再利用**：[#1203](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1203) は「既存のレポートからプロンプトを読み込む」案で足りる、との回答。#1272 はこの案で作られている。
- **音声からの作成**：ワークショップでは、30分ほどの会議を Windows の録音アプリで録り、外部の文字起こしサービスで広聴AI用の CSV に変換していた（[#1204](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1204)）。手間取ったのは、文字起こしサービス側の NG ワード（防災・医療で普通に使う語）の扱いで、広聴AI側の課題ではない。
- **会議の分析の線引き**：[#1226](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1226) の既定の案（本体の外で試作する）に賛成。そのうえで、職員が自分たちで録音からレポートを作り、議論していた点が面白かったとして、現場で試す時は職員自身が使える形を考えたい、という意見があった。期限案は12月8日。
- **上位グループの妥当性**：[#1208](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1208) は、公開できるデータがあるかを確認中。

## ブラウザ版

org 版の main は前回と同じ `ec0c88a` で、新しい PR はない。開いているのは上の輪郭の PR #14 だけ。

11月26日の Slack で、西尾が両版の関係を「ブラウザ版で作ったもののうち experimental 以外は、サーバ版で読める」という約束に絞る案を出した（[[serverless-read-compatibility-contract-2026-11-26]]）。続くやり取りで、「experimental な機能はブランチで試すのとどう違うか」という質問が出た。答えは、ブランチだと自動でデプロイされないので、利用者に試してもらえない、というもの。リポジトリは main の1本で進める。[[slack-logs-repository]]より

## 依存関係の脆弱性アラート

Dependabot の未対応アラートは30件。11月8日に対応を済ませた時点では、修正版の出ていない1件だけだった。その後、11月17日から20日に28件、11月27日に2件が新しく出ている。すべて npm の依存で、対応する Issue・PR はまだない。main の「Dependabot Updates」は11月27日の実行でも失敗しており、自動の更新 PR は出ていない。脆弱性の内容は公開境界により書かない。[[security-maintenance]]より

## 観測範囲

- 本体は main `77cb3f82`、ブラウザ版は org 版 main `ec0c88a`。PR・Issue・CI・Dependabot の状態は、11月28日03:54〜03:56 JST に GitHub で確認した。Dependabot の open は30件。[[source-code]]より
- Slack は11月27日16:53 JST 同期のミラーで、11月26日06:00 JST 以降の全チャンネルを11月28日に読んだ。[[slack-logs-repository]]より
- 議事録は11月28日03:55 JST に txt を取り直した。前回の取得分と同じで、先頭は引き続き7月27日だった。[[meeting-minutes]]より

## Open Questions

- Dependabot の30件を、どの順に、誰が塞ぐか。11月8日に範囲指定に揃えた override の後も「Dependabot Updates」が失敗する理由は、まだ確かめていない
- ブラウザ版の輪郭の既定表示を、本体の分割案に揃えるか（PR #14 を閉じて分割を移植するか）
- #1272 で、プロンプト以外の AI 設定も読み込むか
