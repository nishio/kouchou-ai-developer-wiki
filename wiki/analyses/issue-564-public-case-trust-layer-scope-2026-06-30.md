---
type: analysis
summary: "Issue #564 活用事例公開を、8/2 イベント・公開事例棚卸し・#696 誤読防止・#542 責任所在と接続した次 scope"
sources:
  - github-issues-564-696-542-trust-layer-live-2026-06-30.md
  - event-2026-08-02-public-example-inventory-2026-06-30.md
  - public-broadlistening-artifacts-2026-06-30.md
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - japan-broadlistening-use-case-map-2026-06-30.md
  - public-case-page-skeleton-2026-06-30.md
  - report-reading-guide-minimum-wording-2026-06-30.md
  - slack-case-introduction-channel-2026-03-04.md
  - azure-demo-public-visibility-proposal-2026-06-04.md
  - azure-demo-visibility-thread-resolution-2026-06-05.md
  - kouchou-ai-docs-entry-restructure-2026-06-03.md
  - issue-876-developer-docs-gap-audit-2026-06-30.md
  - current-open-issue-triage-2026-06-01.md
  - remaining-issue-priority-2026-05-29.md
  - source-code.md
---

## Conclusion

Issue #564 は「事例を並べる」だけでは閉じない。自治体や導入検討者が知りたいのは、成果物の URL だけでなく、導入検討、体制づくり、テーマ決定、実施内容、やってみた結果、公開 report までの流れである。[[github-issues-564-696-542-trust-layer-live-2026-06-30]]より

同時に、#696 の誤読防止と #542 の責任所在を外すと、公開事例は「広聴AIが正しい民意を保証した」ように読まれかねない。したがって、8/2 イベントや public docs に移す最小単位は **公開事例リスト + レポートの読み方 + 何を保証しないか** の 3 点セットである。[[current-open-issue-triage-2026-06-01]]より

2026-06-30 16:12 JST に #564 を再読すると、要求は事例 detail だけではなく、初回説明の反復コスト削減にも向いている。`広聴AIって何？` / `何ができる？` / `どう使える？` / `使うにはどうしたらいい？` へ事前に答える説明 block、一枚絵、自治体向け説明資料 / 動画への導線も #564 の scope に入る。[[github-issues-564-696-542-trust-layer-live-2026-06-30]]より

公開Web検索で確認できた事例は、自治体公式 trial、public viewer、政党・国会での broad listening 利用、Talk to the City の系譜、検索 snippet だけの候補に分かれる。#564 のページ設計では、事例数を増やす前に `classification` / `source_strength` / `tool lineage` を明示する必要がある。[[japan-broadlistening-use-case-map-2026-06-30]]より

## Why this matters for 8/2

前回の棚卸しで、8/2 の public artifact 候補は、渋谷区 official page / PDF、奈良 #全員市長 public viewer、八代市 Democracy-X public article / viewer、synthetic sample fallback に分けられた。[[event-2026-08-02-public-example-inventory-2026-06-30]]より

これをそのままスライドに貼るだけだと、「どの事例が何を証明しているのか」が曖昧になる。8/2 での扱いは次のように分けるのがよい。

- **渋谷区**: 自治体公式 artifact があることを示す trust context。
- **奈良 #全員市長**: public-viewer の読み方を見せる demo artifact。
- **八代市**: 実践 lane と技術 lane をつなぐ deep case。ただし政策・選挙文脈があるため、「そのニーズが見つかった」に表現を寄せる。
- **synthetic sample**: 操作説明・fallback。実事例の代替にはしない。

この分担なら、#564 の「導入ハードルを下げる」と、#696 / #542 の「誤読させない」を同時に満たしやすい。[[public-broadlistening-artifacts-2026-06-30]]より

## Minimum Public Case Schema

公開事例ページまたは 8/2 用スライドに落とす場合、1 事例を次の項目で揃えると、#564 のコメントに出ている自治体側の疑問に答えやすい。

| field | purpose |
|---|---|
| 公開 artifact | official page / viewer / PDF / article の URL。Slack-only / Drive-only は載せない |
| だれが使ったか | 自治体 / 政党 / 議員 / メディア / 企業など、公開可能な範囲 |
| 何を知りたかったか | テーマ設定。広聴AIが何に使われたか |
| どう意見を集めたか | アンケート、SNS、対面、既存 public comment など。未公開なら空欄にする |
| どの artifact を見るべきか | viewer / PDF / 記事 / 発表資料のうち、導入検討者に見せる入口 |
| 何が分かったか | 「民意を証明した」ではなく、発見された論点・次に調べるべき問い |
| 注意 | 代表性、責任所在、政治・選挙文脈、権利確認、個人情報の扱い |
| 分類 | 自治体公式 / public viewer / 政党・国会 / メディア / 企業 / candidate |
| source strength | official page / public viewer / organization article / secondary article / search snippet |
| tool lineage | 広聴AI / Talk to the City / 広義の broad listening / AI analysis |

この schema とは別に、ページ冒頭には `basic explainer` が要る。これは「個別事例の説明」ではなく、問い合わせ前に共通認識を作るための入口である。

| explainer item | role |
|---|---|
| 広聴AIとは何か | ツールの最短説明 |
| 何ができる / できない | 期待値調整と誤読防止 |
| どう使える | アンケート / SNS / 対面記録 / パブコメなどの入力例 |
| 使うには何が必要 | データ、体制、公開範囲、費用、責任主体 |
| まず見る事例 | official context / viewer demo / deep case の 3 種 |

## Placement Recommendation

短期の wiki / docs-safe action としては、developer wiki にこの scope を残すだけで十分に価値がある。外部公開へ移す場合は、1 PR / 1 page で全部を解こうとせず、次の順序に分ける。

1. **dd2030 website / event page**: 事例を見せる外部向け正本。#564 の本来の出口に近い。
2. **kouchou-ai docs**: 「レポートを見る」「public-viewer を読む」「自分のデータを準備する」ための技術寄り導線。current docs は setup-first なので、事例リンク集を入口に置くなら docs spine 変更と一緒に扱う。[[kouchou-ai-docs-entry-restructure-2026-06-03]]より
3. **kouchou-ai README / footer / public-viewer**: #696 / #542 の注意書き・責任所在を支える場所。事例ページと同時に最低限の reading guide へリンクする。

Azure デモ環境は「自分のデータを投入する場所」ではなく「使い方や準備データを理解する参照環境」と再フレームされているため、公開事例 / sample report / sample CSV の導線は、専用試用環境より先に整える価値が高い。[[azure-demo-visibility-thread-resolution-2026-06-05]]より

公開ページへ落とす具体 skeleton は [[public-case-page-skeleton-2026-06-30]] に固定した。最初に見る 3 事例、事例一覧の分類軸、詳細テンプレート、レポートの読み方、first slice、載せない情報を分け、DD2030 website の `kouchou-ai/case` 拡張を想定した。

#696 / #542 の最小文言は [[report-reading-guide-minimum-wording-2026-06-30]] に固定した。current main の public-viewer footer には責任所在の短い文言が既にあるため、次の実装は footer 単純追加ではなく、README / docs / viewer dialog / 公開事例ページで「読み方」「保証しない範囲」「個別レポート発行主体」を揃える scope として切るのがよい。[[source-code]]より

Slack `#1_事例紹介_全体` は candidate intake として有用だが、public case list とは分ける。舞鶴2040のように Slack lead から primary public URL へ昇格できるものもある一方、AI assistant、いどばた、broad listening の意向表明、内部リンクも混ざるためである。[[slack-case-introduction-channel-2026-03-04]]より

## What Not To Do

- #564 のために、Slack / Drive の非公開情報をそのまま公開 wiki や public docs に転記しない。
- 事例公開だけを先に出して、#696 / #542 の「どう読むべきか」「誰が責任を持つか」を後回しにしない。
- 8/2 の技術資料に、#876 developer quickstart、#877 Windows setup、#885 Node runtime 排除を混ぜない。これらは裏側の docs / packaging 整備で、導入検討者に見せる public case layer とは別の読者である。[[issue-876-developer-docs-gap-audit-2026-06-30]]より
- AI agent が独断で GitHub issue の assign、review request、close、website 公開をしない。

## Next Wiki-Safe Actions

- `#564/#696/#542` を合わせた public case page の skeleton を developer wiki に置く。
- #564 の public page first slice には、事例一覧の前に basic explainer / FAQ を置く。
- 8/2 用に、奈良 / 渋谷区 / 八代市 / 舞鶴2040 / 宇多津町のどれを first demo / official context にするかを人間が選べる判断表へ落とす。
- 事例ごとの公開可能 / 要許諾 / 不使用を `public-broadlistening-artifacts` の freshness marker で管理する。
- `#1_事例紹介_全体` の lead を、confirmed / broad listening mention / adjacent civic AI / internal pointer に triage する表へ落とす。
- 本体 docs に移すなら、#876 の developer quickstart とは別に、docs spine first slice として「事例を見る / レポートを読む」入口を切る。

## Open Questions

- #564 の正本は dd2030 website か、kouchou-ai docs か、8/2 event material か。
- #696 / #542 の minimum wording は誰が承認するか。技術的正確性だけでなく、法務・運営・渉外の判断が要る。
- 事例 schema の field を全部埋められない public artifact を、事例として出すか、リンク集に留めるか。
- #1_事例紹介_全体 channel や Drive にある素材を、誰が公開可否で scrub するか。

## Updates

- 2026-06-30: #564 を再読し、公開事例ページは事例 detail だけでなく basic explainer / FAQ / 一枚絵の入口も必要だと追記。
- 2026-06-30: [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、#696 / #542 の最小文言と placement を #564 trust layer の実装前 draft として接続。
- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、Slack 事例紹介 channel は lead intake として扱い、public case list には primary URL 確認済み case だけを載せると整理。
- 2026-06-30: [[public-case-page-skeleton-2026-06-30]] を追加し、#564 の公開事例ページを「最初に見る 3 事例 / 事例一覧 / 詳細テンプレート / レポートの読み方 / first slice」に分解した。
- 2026-06-30: [[public-web-broadlistening-japan-use-cases-2026-06-30]] / [[japan-broadlistening-use-case-map-2026-06-30]] を追加し、#564 の事例 schema に classification / source strength / tool lineage を加える必要があると整理。
- 2026-06-30: 初回作成。Issue #564 を 8/2 公開事例棚卸しと接続し、#696 / #542 を含む trust layer として次 scope を整理した。
