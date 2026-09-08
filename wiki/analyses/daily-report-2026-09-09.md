---
title: "開発日報 — 2026年9月8日〜9日未明"
type: analysis
summary: "9月8日から9日未明の開発日報。追記を含め本体20 PRをmerge、両版の入力・閲覧改善、Issue整理と利用者の行動を起点にした方針の見直しを記録"
sources:
  - issues-response-plan-2026-09-07.md
  - other-issue-candidates-2026-09-07.md
  - issue-backlog-audit-2026-09-09.md
  - serverless-product-direction-2026-09-08.md
  - serverless-relationship-2026-09-08.md
  - wiki-driven-workflow.md
  - recent-slack-issues-2026-09-07.md
---

## 今日進んだこと

> **9月9日02:21追記**：CI待ちだった本体#927〜#933もすべてmergeし、この日報の対象期間でmain反映は累計20 PRとなった。以下の表と本文は初稿時点の記録を保持している。追加の検証と最終状態は末尾のUpdatesを参照。

分析の失敗を成功に見せないこと、利用者が設定や結果を読み違えないことを中心に、実装・検証・Issue整理を進めた。同時にdd2030-wikiを参照し、開発の目的を「初めての人が使い始め、集まった声を確かめ、対話・判断・応答へつなげられること」として捉え直した。Serverlessとの関係も、その仕事にどの版が適するかを検証する課題として整理した。[[issues-response-plan-2026-09-07]] / [[other-issue-candidates-2026-09-07]] / [[serverless-product-direction-2026-09-08]]より。

日付をまたいだ一連の作業として、**2026年9月8日から9日未明（JST）**を対象にする。9月7日のSlack調査・最初の修正・Wikiリンク確認は前段として扱う。以下は作業時の記録とWikiのコミット `a083426` までをまとめた日報で、執筆時にGitHubや実モデルを再検証したものではない。

| 区分 | 到達点 | 集計の意味 |
| --- | --- | --- |
| 本体mainへの反映 | 13 PRをmerge | 9月8日02:36の3件と23:21の10件。以前からあったPRも含む |
| 本体の進行中実装 | PR #927〜#933の7件 | 階層図の連動と、その後に選んだ10 Issueの実装。9月9日01:00の観測でCI成功・未merge |
| Serverlessへの対応 | PR #22〜#26の5件 | 元コメント参照・入力・読み方・階層図・診断と閲覧。未merge、Actions承認待ち |
| 過去Issueの整理 | 8件close、18件更新 | 最後の棚卸しでopen 119→111。完了5件と重複統合3件を区別 |

集計根拠は [[issues-response-plan-2026-09-07]] / [[other-issue-candidates-2026-09-07]] / [[issue-backlog-audit-2026-09-09]]。未mergeの実装をmain反映済みには数えていない。

## 出発点は、声の欠落と設定の食い違い

前日のSlack・Issue調査では、同じ入力でも抽出0件になる回答が増える報告と、ラベル生成エラー、Azureで選択したモデルが実際には使われない問題が見つかっていた。抽出数だけでモデル品質を比較する前に、失敗による欠落を正常0件と区別する必要があった。報告された欠落の根本原因は確定しておらず、並列数を下げれば常に解決すると判断したわけではない。[[recent-slack-issues-2026-09-07]]より。

モデル管理では、西尾の判断をIssueコメントへ残してから実装した。モデルが選択可能かどうかと、動作を確認したかどうかを分離し、未検証のモデルも状態を表示して一覧に出す。料金不明を無料に見せず、提供終了モデルを無言で置き換えない。実モデルによる確認は#912 / #913へ分離し、人間が担当することになった。[[issues-response-plan-2026-09-07]]より。

## mainに反映した改善

9月8日は、早朝と夜の二回、ユーザーのmerge指示を受けてCI成功を確認したPRをmainへ反映した。抽出・ラベル段階の失敗検知から、作成前の入力確認、設定と接続先の一致、結果の読み方までをつないだ。

| 利用者・開発者にとっての変化 | 本体PR（merge済み） |
| --- | --- |
| 抽出のAPI例外・timeout・形式不正を正常0件と分け、失敗時は後段へ進めない | [#910](https://github.com/digitaldemocracy2030/kouchou-ai/pull/910) |
| Azureの固定モデルを正しく示し、モデル一覧・説明・価格・検証状態をカタログに集約 | [#911](https://github.com/digitaldemocracy2030/kouchou-ai/pull/911)、[#914](https://github.com/digitaldemocracy2030/kouchou-ai/pull/914) |
| 空のタイトル・概要をCSV名から補完し、入力済みの内容は保持 | [#918](https://github.com/digitaldemocracy2030/kouchou-ai/pull/918) |
| ラベル生成失敗で後続を止め、失敗時の費用・token集計が不完全であることを示す | [#919](https://github.com/digitaldemocracy2030/kouchou-ai/pull/919) |
| タイムアウト設定が実行処理まで届き、作成前に入力・設定・API状態を確認できる | [#920](https://github.com/digitaldemocracy2030/kouchou-ai/pull/920)、[#922](https://github.com/digitaldemocracy2030/kouchou-ai/pull/922) |
| 不正CSVの原因と修正方法を表示し、失敗後に古い入力を残さない | [#923](https://github.com/digitaldemocracy2030/kouchou-ai/pull/923) |
| 件数と支持率の違い、収集の偏り、原文照合などの読み方を閲覧画面・HTMLへ追加 | [#924](https://github.com/digitaldemocracy2030/kouchou-ai/pull/924) |
| コントリビュータが読む順番と、Issue着手からPR提出までの導線を集約 | [#925](https://github.com/digitaldemocracy2030/kouchou-ai/pull/925) |
| 選択したprovider・モデル・ローカル接続先でチャット接続を確認 | [#926](https://github.com/digitaldemocracy2030/kouchou-ai/pull/926) |
| Node runtime依存の棚卸し文書、dummy-serverの依存更新を取り込み | [#903](https://github.com/digitaldemocracy2030/kouchou-ai/pull/903)、[#904](https://github.com/digitaldemocracy2030/kouchou-ai/pull/904) |

[[issues-response-plan-2026-09-07]] / [[other-issue-candidates-2026-09-07]]より。#905のラベル段階などの残件は#915へ移してから追跡し、PR #919で対応した。#925の文書ナビゲーション競合は双方の導線を残して解消し、再build・CI確認後にmergeした。最後のmainは `2dd5adc`。費用・時間の数値見積もりや全pipelineの実モデル動作まで完了したという意味ではない。

## Serverlessとの関係を考え直し、共通の確認例で実装した

dd2030-wikiを読んだ最初の整理では、ブラウザ版を初回利用の候補、既存版を継続的な組織運用の候補、analysis-coreを分析手法の交換・比較の候補とした。「本流」という語は、利用入口・開発の重点・所有やrepo移管の三つに分けた。元コメントを含むかどうかなど、両版の結果JSONにも差があり、表示・根拠確認・再分析・公開を別々に確かめる必要が分かった。[[serverless-relationship-2026-09-08]]より。

その後「次は抽出部分失敗を直す」と提案したところ、西尾から「広い視野で考えて」と指摘された。実装できる不具合を選ぶだけでは、今それが利用者の最大の障害かは分からない。そこで、具体的な実践の収集→分析→議論→応答をたどり、価値の大きい障害を特定することへ次goal案を修正した。各版の役割分担も、利用場面で確かめる仮説として扱う。[[serverless-product-direction-2026-09-08]]より。

保守として進められる部分は、その議論と並行して両版へ実装した。

| Serverless PR（すべて未merge） | 実装・確認した内容 |
| --- | --- |
| [#22](https://github.com/tokoroten/kouchou-ai-serverless/pull/22) | 数値変換で元コメントIDの先頭ゼロや整数精度が失われる問題を修正。保存・読込・再分析用復元の参照を確認 |
| [#23](https://github.com/tokoroten/kouchou-ai-serverless/pull/23) | 本体#923と同じCSV入力例・判定・案内を使い、不正入力後の復帰を確認 |
| [#24](https://github.com/tokoroten/kouchou-ai-serverless/pull/24) | 本体#924と読み方の説明を揃え、アプリ内と持ち出す単一HTMLで確認 |
| [#25](https://github.com/tokoroten/kouchou-ai-serverless/pull/25) | 本体#927と階層図・説明・件数・割合・戻る操作を同期。同じ属性条件で両版を比較 |
| [#26](https://github.com/tokoroten/kouchou-ai-serverless/pull/26) | 抽出失敗の診断、日本語折り返し、スマホ初期表示、状態カタログを揃え、旧空キャッシュも再検証 |

[[other-issue-candidates-2026-09-07]] / [[serverless-product-direction-2026-09-08]]より。コードの形を一律にするのでなく、同じ入力で期待する挙動と復帰操作を確認した。本体の静的出力はHTTPで配信し、Serverlessの単一HTMLは直接開けるという配布上の違いを保った。原文付き診断は公開レポートに自動追加しない。

## 夜から未明に、次の10件を実装してPRへ

階層図と説明の現在位置を揃える [本体PR #927](https://github.com/digitaldemocracy2030/kouchou-ai/pull/927) の後、未担当のIssueから次の10件を選び、担当を設定して着手した。以下は**実装済み・未merge**の作業である。[[other-issue-candidates-2026-09-07]]より。

| 対象Issue | 提出したPRと範囲 |
| --- | --- |
| #318 | [#928](https://github.com/digitaldemocracy2030/kouchou-ai/pull/928)：回答ID・原文・エラー種別を公開出力とは別の診断へ保存 |
| #877 | [#929](https://github.com/digitaldemocracy2030/kouchou-ai/pull/929)：Windows導入の適用条件・キー要件・確認・失敗時の分岐を整理 |
| #367 | [#930](https://github.com/digitaldemocracy2030/kouchou-ai/pull/930)：入力特性に合わせた抽出プロンプトの比較手順。例は動作未検証と明記 |
| #838 | [#931](https://github.com/digitaldemocracy2030/kouchou-ai/pull/931)：完成JSONのID・親参照・循環・階層パス・数値を調べる任意の検査CLI |
| #690 | [#932](https://github.com/digitaldemocracy2030/kouchou-ai/pull/932)：開発実行をtsxへ移し、起動・再読込を修正 |
| #478 / #283 / #253 / #872 / #566 | [#933](https://github.com/digitaldemocracy2030/kouchou-ai/pull/933)：日本語表示・全画面の重なり・静的出力の案内・スマホ表示・状態別UI確認環境 |

スマホの初期表示は600px以下でリストとし、本体に明示設定があれば優先する。画面幅が変わっても利用者が選んだ表示を上書きしない。状態カタログには共通の合成12意見を使い、本番では利用できないことも確認した。#927 / #933とServerless #25 / #26は、それぞれ競合なく統合できることを事前に確認したが、実際のmergeはしていない。[[other-issue-candidates-2026-09-07]]より。

## CIを待つ間に、過去Issueの意味を整理した

open 119件の一覧・本文・コメントを取得し、現行実装と関係するものを重点的に照合した。全119件の動作確認をしたわけではない。実装済みの#514 / #305 / #391 / #223 / #379を完了として閉じ、重複する#294を#266へ、#287 / #254を#877中心の窓口へ統合した。さらに18件の本文へ現状と残作業を追記し、反映後のGitHub状態を再取得して確認した。[[issue-backlog-audit-2026-09-09]]より。

ここで重要だったのは、閉じなかったIssueの判断である。#513の古い「seed設定済み」というコメントは、現行mainでは固定seedが意図的に外されているため完了根拠にならなかった。#79 / #11は作成前確認があっても数値見積もりが残り、#56は抽出意見を読めても元コメントの公開可否や参照の問題が残る。Issue本文の履歴を消さず、何が済み何が必要かを更新した。[[issue-backlog-audit-2026-09-09]]より。

## 確認できたことと、まだ確認していないこと

検証は変更ごとに行った。ラベル失敗対応ではcore全体231テスト、10件の後半実装では本体viewer102テストとブラウザ回帰4件、Serverlessの最終追加修正では204テストと型検査が成功した。階層図・属性絞り込み・0件からの復帰、スマホ表示、単一HTMLの操作もブラウザで確認した。Issue #514は処理を意図的に逆順で完了させ、出力が入力順に戻ることを確認した。これらの件数は時点・branchごとに重複するため、合算した「総テスト数」は出さない。[[other-issue-candidates-2026-09-07]] / [[issue-backlog-audit-2026-09-09]]より。

9月9日01:00の観測では本体PR #927〜#933の登録済みCIは全成功、未merge。Serverless #22〜#26はローカル検証済みだが外部forkのActions承認待ちで、現在の作業アカウントにmerge権限はなかった。CodeRabbitが利用制限でレビューできなかったPRもあり、CI成功とレビュー完了は区別する。実LLM API、新モデルの一連の動作、Windows実機の追加確認、初見利用者による現場評価は行っていない。実モデル確認#912 / #913は人間担当のままである。[[other-issue-candidates-2026-09-07]] / [[issues-response-plan-2026-09-07]] / [[issue-backlog-audit-2026-09-09]]より。

## Wikiに残した学びと次の行動

今回の実装・調査・CI結果は都度Wikiと定例報告下書きへ記録した。最後のfile backでは、現行mainで完了を判断すること、確認した範囲を広い保証へ膨らませないこと、両版を同じ入力・期待する挙動・復帰操作で照合することを [[wiki-driven-workflow]] に整理し、Issueの更新前後の照合を `CLAUDE.md` に反映した。

次の候補は、利用者の流れに沿って三つにまとめた。[[issue-backlog-audit-2026-09-09]] / [[serverless-product-direction-2026-09-08]]より。

1. **自分に合う入口を選ぶ**：#876 / #877 / #496。閲覧・CSV分析・組織運用・開発・分析実験を分け、制約に合う経路へ案内する。
2. **分析を始める判断ができる**：#79 / #11。費用・時間について推定・不明・実測を区別し、両版で比較できる条件を残す。
3. **元の声を確かめ、次の対話へ渡す**：#56 / #250 / #564 / #130。原文の公開範囲を守り、事例には問い・収集の偏り・根拠照合・その後の行動・失敗も残す。

## Open Questions

- #921の利用入口・開発重点・所有/移管は、それぞれどの利用観測を根拠に決めるか。今回の実装は正式な製品方針の決定ではない。
- 費用・時間見積もりと元コメント参照は、両版のどこまで共通の振る舞いを約束するか。
- 具体的な利用場面で、収集から対話・判断・応答までの最大の障害はどこか。初見利用の成功や現場価値はまだ実証していない。

## Updates

- 2026-09-09: ユーザーの依頼で、9月8日から9日未明までの活動を日報として編集。前日のSlack調査・Wikiリンク確認は [[recent-slack-issues-2026-09-07]] / [[wiki-driven-workflow]] を参照。main反映済み・未merge・未検証を分け、詳細な実装記録への入口とした。

### 2026-09-09 02:21 CI通過後の7 PRを追加merge

日報作成後、ユーザーのmerge指示を受けてGitHubを再確認し、本体#927〜#933をすべてmainへ反映した。#930 / #933は文書メニューの競合を解消し、変更後のHEADでGitHub Actions成功を待ってmergeした。#933は総合E2E・本番buildも成功。必須レビュー設定による制限には、前回同様に明示指示に基づく管理者mergeを使用した。merge直前のCodeRabbitは進行中であり、レビュー完了とCI成功は区別する。[[other-issue-candidates-2026-09-07]]より。

最終mainは `775e0f5`。統合後のviewer109テスト、抽出診断・成果物検査21テストと、競合解消後の厳密docs buildが成功し、最終mainと検証したtreeの一致も確認した。11 Issueがmergeによりclosedとなり、openは100件。本体のopen PRはdraft #917 / #891の2件のみ。冒頭で進行中としていた本体7 PRはこの追記でmain反映済みとなる。

Serverlessはread権限のみのため未mergeで、#22〜#26のActionsは承認待ち。実モデル確認#912 / #913は人間担当のまま。この追記はGitHub・コード統合の再確認であり、実モデルや現場利用の追加検証ではない。

### 2026-09-09 02:57 残る2 PRはdraftのまま維持する

西尾が内容を確認し、「それは残そう」と判断したため、[#917](https://github.com/digitaldemocracy2030/kouchou-ai/pull/917) と [#891](https://github.com/digitaldemocracy2030/kouchou-ai/pull/891) は当面draftのまま残す。

- **#917：OpenAI Flex対応**。tokoroten / Copilotが担当するAPI費用削減の変更。02:31の観測ではCodeQL成功のみで、通常テスト・buildの成功確認は揃っていない。
- **#891：Windowsスタンドアロン版**。tokoroten作のPython・API・閲覧／管理画面を同梱する試作。6月1日から同じHEADのままで、02:31の観測ではmainと競合。作成フロー全体の検証とインストーラーが残り、Serverlessとの役割も検討事項となる。

技術的な状態は [[other-issue-candidates-2026-09-07]] / [[github-pr-891-live-2026-06-30]] の02:31の確認に基づく。今回はdraftを維持するユーザー判断を記録したもので、追加のPR操作や動作検証は行っていない。
