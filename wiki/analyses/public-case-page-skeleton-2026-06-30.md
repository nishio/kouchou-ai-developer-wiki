---
type: analysis
summary: "Issue #564 の活用事例公開を、導入検討者向けの公開ページへ落とすためのページ構成案"
sources:
  - github-issues-564-696-542-trust-layer-live-2026-06-30.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - japan-broadlistening-use-case-map-2026-06-30.md
  - report-reading-guide-minimum-wording-2026-06-30.md
  - slack-case-introduction-channel-2026-03-04.md
  - event-2026-08-02-public-example-inventory-2026-06-30.md
---

## Conclusion

Issue #564 の公開事例ページは、単なる「使われました」一覧ではなく、導入検討者が次に質問する内容へ先回りするページにする必要がある。#564 のコメントでは、自治体側の関心が、意見収集方法、X からの収集、費用、手書き意見 / OCR、使える話題、体制づくり、実施内容、結果まで広がっていた。[[github-issues-564-696-542-trust-layer-live-2026-06-30]]より

したがって、最小公開ページは **事例リスト + レポートの読み方 + 何を保証しないか** の 3 点セットにする。これは #696 の誤読防止と #542 の責任所在を外すと、事例が「広聴AIが正しい民意を保証した」ように読まれかねないためである。[[issue-564-public-case-trust-layer-scope-2026-06-30]]より

## Page skeleton

### 1. 最初に見る 3 事例

1 ページ目の最初は、件数を多く見せるより `source strength` の異なる 3 類型を出す。

| role | candidate | reason |
|---|---|---|
| 自治体公式 proof | 宇多津町または渋谷区 | 自治体公式ページ上で、広聴AI / ブロードリスニング trial と件数・用途が確認できる。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より |
| viewer demo | 舞鶴2040または奈良 #全員市長 | public viewer の読み方を実際に見せられる。舞鶴2040は政治色を下げたい場合の代替候補。[[japan-broadlistening-use-case-map-2026-06-30]]より |
| deep case | 八代市 Democracy-X | 記事と viewer があり、実践 lane と技術 lane をつなぎやすい。ただし政治・政策文脈の説明が必要。[[event-2026-08-02-public-example-inventory-2026-06-30]]より |

### 2. 事例一覧

一覧は、組織名だけでなく「何を根拠に確認したか」を見せる。導入検討者には実績の広がりを示しつつ、内部資料や Slack-only anecdote に依存しない。

| field | description |
|---|---|
| 事例名 | 自治体 / 政党 / 団体 / viewer 名 |
| 分類 | 自治体公式 / public viewer / 政党・国会 / メディア / 企業 / candidate |
| source strength | official page / public viewer / organization article / secondary article / search snippet |
| tool lineage | 広聴AI / Talk to the City / 広義の broad listening / AI analysis |
| public artifact | official page / PDF / viewer / article の URL |
| 何を見られるか | 意見収集、分析結果、viewer 操作、政策利用、発表資料など |
| 注意 | 代表性、責任所在、政治・選挙文脈、権利確認、個人情報、誤読可能性 |

Slack `#1_事例紹介_全体` のような channel は、一覧に入れる候補を拾う lead intake として扱い、外部公開の evidence にはしない。Slack lead には広聴AI case、広義の broad listening 言及、AI assistant、いどばた関連、内部リンクが混ざるため、primary URL が確認できるまで `candidate` に留める。[[slack-case-introduction-channel-2026-03-04]]より

### 3. 事例詳細テンプレート

1 事例を深く紹介する時は、#564 のコメントにある自治体側の質問へ答える順序にする。

| section | question it answers |
|---|---|
| 背景と目的 | 何を知りたくて始めたのか |
| 体制 | 誰が主催し、誰が分析・支援したのか |
| 意見の集め方 | アンケート、SNS、電話、対面、既存 public comment、手書き / OCR など |
| 対象データ | 件数、対象期間、自由記述か、投稿か、公開できる範囲 |
| 分析・可視化 | 広聴AI / Talk to the City / broad listening のどれか、何を見せたか |
| レポートの読み方 | クラスタ、点、ラベル、要約、個別意見への戻り方 |
| 分かったこと | 「民意を証明した」ではなく、見つかった論点・次に深掘りする問い |
| 限界と注意 | 代表性、LLM の限界、責任所在、政策反映を保証しないこと |
| 次の展開 | 実施後に何を変えたか、または次に何を検討するか |

### 4. レポートの読み方

事例ページには、public viewer や PDF を見る前に読む短い guide を置く。

- 点は意見・コメントを表す。人の数や投票数をそのまま表すとは限らない。
- クラスタの大きさや位置は、社会全体の多数派を保証しない。
- LLM によるラベルや要約は、論点把握を助ける説明であり、最終判断ではない。
- 重要な意思決定では、元データ、収集方法、対象者、公開条件、人間の検証と合わせて読む。
- レポート内容に関する責任主体を明示し、DD2030 / 広聴AI OSS が各レポート内容を保証しているように見せない。

この section は #696 / #542 の最小版であり、事例ページと別に実装するとリンク切れや説明抜けが起きやすい。[[github-issues-564-696-542-trust-layer-live-2026-06-30]]より

実際に外へ出す文言 draft は [[report-reading-guide-minimum-wording-2026-06-30]] に固定した。事例ページ上部は短い説明、viewer footer / dialog は常設注意、README / docs は OSS と個別レポートの責任境界、metadata は発行主体表示という役割分担にする。

## First slice

外部公開へ移す前の first slice は、DD2030 website の `kouchou-ai/case` を拡張する想定で、次の範囲に絞るのが衝突しにくい。

1. 現在確認済みの public source だけを載せる。
2. 事例一覧には `classification` / `source_strength` / `tool_lineage` を入れる。
3. 詳細ページ化は宇多津町または渋谷区の 1 件に絞る。
4. レポートの読み方と免責を同じ PR / 同じページに含める。
5. candidate は「確認中」として、公開 URL が有効になるまで本文の実績には混ぜない。

## Do not include

- Slack-only / Drive-only の事例、許諾未確認のスクリーンショット、内部説明資料の中身。
- Azure デモ環境の URL、resource 名、revision、run log、secret / access 周辺。
- 「広聴AIが民意を証明した」「多数派がこの政策を望んでいる」のような断定。
- 広聴AIではない broad listening 事例を、広聴AI利用実績として扱う表現。

## Open Questions

- 外部正本は DD2030 website の `kouchou-ai/case` でよいか、kouchou-ai docs 側にも mirror を置くか。
- 最初の詳細事例は宇多津町、渋谷区、舞鶴2040、八代市のどれにするか。
- #696 / #542 の wording を誰が承認するか。技術・法務・渉外の責任境界が要る。
- 公開事例の候補管理を GitHub issue、Drive、website repo、developer wiki のどこで canonical にするか。

## Updates

- 2026-06-30: [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、公開事例ページに置く「レポートの読み方」の実文言 draft へ接続。
- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、Slack case channel は lead intake、外部ページは primary URL 確認済み case list として分ける方針を追記。
- 2026-06-30: 初回作成。#564 の issue コメント、公開Web検索、#696 / #542 の trust layer をもとに、公開事例ページの構成案を固定した。
