---
type: source
summary: "2026-09-07確認のSlackとIssue。回答欠落、モデル選択・管理、serverless移管と戦略会議の論点"
sources:
  - slack-logs-repository.md
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/905
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/909
---

## Freshness marker

- 最終読解日: 2026-09-07 JST。Slack clone は `4032946660b8207714c9532ac28c07077621bb32` まで更新。
- `mirror/sync.json`: 同期 2026-09-07 04:08:54 UTC（13:08 JST）、window は 2026-06-24〜09-07、**75日**、59 channels。以前の14日という説明は今回のsnapshotに適用しない。
- 精読: `C08F7JZPD63`（広聴AI開発）、`C08PX74S5T4`（アルゴリズム開発）の8月〜9月7日。7月のserverless共有も文脈として確認。直近約14日は全channelの広聴AI関連語も検索。
- 固定snapshot: `raw/recent-2026-09-07/` に上記2channel・sync metadata・Issue #884 / #905〜#909 の本文とコメント・open PR一覧を保存。8月の開発channelはcanonical rawも確認。
- GitHubは9月7日に更新順Issue一覧と上記6件の本文・コメント、open PR全件を取得。実装コード・戦略会議のリンク先文書・モデル提供元の仕様は今回未検証。以下は投稿・Issueの報告内容。

## SlackとIssueの接続

[9月6日の報告](https://dd2030.slack.com/archives/C08F7JZPD63/p1788647591961169) と [追試](https://dd2030.slack.com/archives/C08F7JZPD63/p1788648652444879)、[Issue #905](https://github.com/digitaldemocracy2030/kouchou-ai/issues/905) より、同じ194回答・同じプロンプトで次の結果が報告された。

| 条件 | 抽出意見数 | 抽出0件の元回答数 |
|---|---:|---:|
| GPT-4o / workers=30 | 482 | 49 |
| GPT-4o / workers=5 | 666 | 0 |
| GPT-4o-mini / workers=30 | 681 | 0 |

原因APIエラーのログは未確認。並列数を下げた追試で改善したが、rate limit等を確定原因とはしない。追試でも詳細クラスタのラベル生成エラー2件が残ったというSlack報告がある。4o-miniのラベルが読みやすいという印象は今回のデータに限られた主観評価。

9月7日確認時点で以下はすべてopen・assigneeなし・コメントなし。

- [#905](https://github.com/digitaldemocracy2030/kouchou-ai/issues/905): 部分失敗と正常な抽出0件を区別し、失敗件数を利用者に知らせる。retry / backoffも検討。
- [#906](https://github.com/digitaldemocracy2030/kouchou-ai/issues/906) / [#907](https://github.com/digitaldemocracy2030/kouchou-ai/issues/907): OpenAI / Geminiモデル追加要望。列挙されたモデル名・提供状況・互換性はIssueの主張として扱い、実装前に提供元確認が必要。
- [#908](https://github.com/digitaldemocracy2030/kouchou-ai/issues/908): Azure OpenAIでUI上のモデル選択と実際の呼び出し先が対応しないとの報告。公開可能な設計課題は、選択可能にするか、固定した実際の選択を明示するか。
- [#909](https://github.com/digitaldemocracy2030/kouchou-ai/issues/909): モデル一覧・料金・説明・利用可否・必要機能の対応を管理しやすくする。動的取得の全モデルと動作確認済みモデルの扱いが未決。
- [#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884): 作成前の入力・コスト・API状態確認。実行中の部分失敗検知とは別の段階を担う。

## その他の最近の動き

- 8月14〜18日の開発channelでは、9月以降の戦略会議と、いどばた・広聴AI・自然言語データ収集を横断する議論への接続が共有された。日程や結論はこの読解では確認していない。
- 7月にアルゴリズムchannelでブラウザ完結版の共有があり、8月21日はDD2030移管と別repo / 本体配下の選択肢に言及。決定済みとは読まない。
- 9月1日の開発channelではデモ環境のコスト削減・構成簡素化への協力募集と、Issue滞留を整理する必要が挙がった。環境詳細は公開wikiに転記しない。
- open PRは #904（依存更新）、#903（Node runtime依存の文書化）、#891（Windows配布、draft）の3件。#905〜#909の対応PRはこのopen一覧では確認できない。依存更新の安全性評価は今回行っていない。

## Open Questions

- #905の失敗原因と、警告付き完了・中断・再実行の境界はどう定義するか。
- serverless版の移管と戦略会議の方針は、その後確定したか。

## Updates

- 2026-09-07: 最新snapshotとGitHub live stateから初回整理。解釈は [[recent-slack-issues-2026-09-07]] へ。
