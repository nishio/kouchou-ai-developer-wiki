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
  - slack-pr-channel-website-faq-case-map-2026-03-04.md
  - event-2026-08-02-public-example-inventory-2026-06-30.md
  - meeting-municipality-user-research-scope-2026-06-30.md
  - broad-listening-book-public-case-appendix-2026-06-30.md
  - meeting-cartographer-idobata-boundary-2026-06-30.md
  - public-tool-catalog-draft-2026-06-30.md
  - website-kouchou-ai-case-live-2026-06-30.md
---

## Conclusion

Issue #564 の公開事例ページは、単なる「使われました」一覧ではなく、導入検討者が次に質問する内容へ先回りするページにする必要がある。#564 のコメントでは、自治体側の関心が、意見収集方法、X からの収集、費用、手書き意見 / OCR、使える話題、体制づくり、実施内容、結果まで広がっていた。[[github-issues-564-696-542-trust-layer-live-2026-06-30]]より

さらに #564 では、`広聴AIって何？` / `何ができる？` / `どう使える？` / `使うにはどうしたらいい？` という初回説明を、毎回個別対応しなくてよい形にしたいという要求も出ている。したがって外部ページは、事例 detail だけでなく、**初回説明 FAQ / 一枚絵 / 説明資料導線** を持つべきである。[[github-issues-564-696-542-trust-layer-live-2026-06-30]]より

したがって、最小公開ページは **事例リスト + レポートの読み方 + 何を保証しないか** の 3 点セットにする。これは #696 の誤読防止と #542 の責任所在を外すと、事例が「広聴AIが正しい民意を保証した」ように読まれかねないためである。[[issue-564-public-case-trust-layer-scope-2026-06-30]]より

## Page skeleton

### 0. 最初に渡す説明 block

事例一覧の前に、導入検討者が個別相談で最初に聞く質問へ短く答える block を置く。これは営業資料ではなく、問い合わせ前の認識合わせである。

| question | short answer needed |
|---|---|
| 広聴AIとは何か | 自由記述の意見を LLM とクラスタリングで整理し、論点を見つけやすくする OSS |
| 何ができるか | 収集済みの自由記述を整理し、公開 viewer / report で論点把握を助ける |
| 何ができないか | 母集団代表性、政策決定、正しい民意、多数派証明を自動保証しない |
| どう使えるか | アンケート、SNS、対面記録、パブコメなどの自由記述を、目的と公開条件に合わせて扱う |
| 使うには何が必要か | データ収集設計、公開範囲、分析担当、発行主体、LLM/API 費用、個人情報・権利確認 |
| まず何を見るか | 公式事例 1 件、viewer demo 1 件、レポートの読み方 |

この block には、利用状況一覧の一枚絵や、自治体向け説明資料 / 動画へのリンクを置ける。ただし、Drive 内資料や未許諾動画をそのまま公開リンクにしない。公開可能になったものだけを載せる。

FAQ は読者別に分ける。Slack `#2_広報_pr` の 2026-03/04 議論では、メンバー向け QA と外向け QA が混ざる問題、参加検討者と既存参加者では読む FAQ が違う問題が出ていた。website PR #192 は 2026-06-19 に merge 済みだが、カテゴリ分けは別途考える扱いになった。#564 の公開事例ページでは、少なくとも `導入検討者向け` / `レポート閲覧者向け` / `既に関わっている人向け` を混ぜない方がよい。[[slack-pr-channel-website-faq-case-map-2026-03-04]]より

この block には、広聴AI / いどばた / Cartographer / Jigsaw Sensemaker / tttc-light-js を混同しないための短い tool catalog も入れる。`collect / deepen / analyze / show / classify / read-and-act` を分け、広聴AI本体の promise は収集済み自由記述の分析・可視化に置く。[[public-tool-catalog-draft-2026-06-30]]より

### 1. 最初に見る 3 事例

1 ページ目の最初は、件数を多く見せるより `source strength` の異なる 3 類型を出す。

| role | candidate | reason |
|---|---|---|
| 自治体公式 proof | 宇多津町、渋谷区、奈良市、岩手県のいずれか | 自治体公式ページ / PDF 上で、広聴AI / ブロードリスニング trial と件数・用途が確認できる。大阪府も府公式 broad listening case として補助線になるが、広聴AI confirmed ではなく広義 broad listening と明示する。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より |
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

`tool lineage` は、少なくとも `kouchou-ai`、`Talk to the City lineage`、`broad listening adjacent`、`idobata / dialogue`、`enterprise / VOC`、`candidate` を分ける。外向けに細かすぎる場合でも、内部整理ではこの分類を持っておくと、広義 broad listening や enterprise VOC を広聴AI confirmed case と誤って載せるリスクを下げられる。[[public-tool-catalog-draft-2026-06-30]]より

一覧とは別に、SNS 発信や初回説明に使う `利用状況の一枚絵` を作る場合は、同じ分類を使う。つまり、プロダクト x 政党・行政・議員・その他組織の grid にしても、`実績` / `予定` / `候補` / `adjacent` を混ぜない。

Slack `#1_事例紹介_全体` のような channel は、一覧に入れる候補を拾う lead intake として扱い、外部公開の evidence にはしない。Slack lead には広聴AI case、広義の broad listening 言及、AI assistant、いどばた関連、内部リンクが混ざるため、primary URL が確認できるまで `candidate` に留める。[[slack-case-introduction-channel-2026-03-04]]より

公開ページには、確認済み事例一覧とは別に `掲載候補を教えてください` 導線を置く余地がある。`#2_広報_pr` では、DD2030 から見えないところで進む活用に気づく方法、HP の導入事例マップ、掲載 OK 確認、事例を集めたいことを伝える必要が議論されていた。したがって public page は `実績を見せる場所` と `候補を受け取る場所` を分けるのがよい。[[slack-pr-channel-website-faq-case-map-2026-03-04]]より

ただし、case intake と自治体 user research は分ける。case intake は public artifact / 掲載許諾 / source strength を確認する導線で、自治体 user research は広聴活動一般の課題や広聴AIが活きるケースを探索する導線である。両者を同じフォームにすると、事例候補収集と product discovery が混ざる。[[meeting-municipality-user-research-scope-2026-06-30]]より

2026-06-30 17:30 JST の direct verification で、Web book 付録由来の大阪府、チームみらい、DirectVote、サイボウズ、アルティウスリンク、与謝野町は primary / organization page まで確認できた。公開ページへ移す時は、これらを `広聴AI導入実績` に一括投入せず、`広義 broad listening`、`政党・政策形成`、`TTTC lineage`、`企業 / VOC`、`AI 支援住民対話 adjacent` に分ける。[[broad-listening-book-public-case-appendix-2026-06-30]]より

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

1. 初回説明 block を置き、`広聴AIとは何か / 何ができるか / どう使えるか / 使うには何が必要か` に短く答える。
2. 現在確認済みの public source だけを載せる。
3. 事例一覧には `classification` / `source_strength` / `tool_lineage` を入れる。
4. 詳細ページ化は宇多津町、渋谷区、奈良市、岩手県のような自治体公式 source が強い 1 件に絞る。
5. レポートの読み方と免責を同じ PR / 同じページに含める。
6. candidate は「確認中」として、公開 URL が有効になるまで本文の実績には混ぜない。
7. `掲載候補を教えてください` 導線を置くなら、候補投稿は public case list へ直結させず、primary URL / 実施主体 / 掲載可否 / source strength の確認 queue に入れる。
8. サイボウズ / アルティウスリンクのような企業・VOC case を載せるなら、自治体向け first slice の後段に `応用領域` として置く。自治体の導入検討者が最初に見る 3 事例とは混ぜない。

## Website current state

2026-06-30 17:59 JST に `digitaldemocracy2030/website` を確認したところ、`src/kouchou-ai/case.vto` が広聴AI活用事例ページの直接更新先で、現行掲載は選挙報道、東京都 2050 戦略案、宇多津町の 3 件だった。選挙報道と東京都は説明文のみでリンクがなく、宇多津町だけ official page へのリンクがある。[[website-kouchou-ai-case-live-2026-06-30]]より

website 側には #208 `広聴AIの利用事例を更新する`、#216 `Slackに投稿された事例をもとにウェブサイト更新PRを作成する`、#125 `[活用事例]リンク追加/UI改善` が open で存在する。#125 には「広聴AIの活用事例ではないかも？」という候補分類の不安が明記されているため、developer wiki 側の `tool_lineage` / `source_strength` は、そのまま website PR 前の guardrail として使える。[[website-kouchou-ai-case-live-2026-06-30]]より

一方で、#123 `プロダクト別の事例ページから、プロダクト横断のニュース一覧に変える` も open のままで、長期的には product-specific `case.vto` 直書きではなく、tagged / cross-product case-news list へ移る可能性がある。したがって first slice は `src/kouchou-ai/case.vto` に載せる最小改修、長期情報設計は #123 側、と分けた方がよい。

## Do not include

- Slack-only / Drive-only の事例、許諾未確認のスクリーンショット、内部説明資料の中身。
- Azure デモ環境の URL、resource 名、revision、run log、secret / access 周辺。
- 「広聴AIが民意を証明した」「多数派がこの政策を望んでいる」のような断定。
- 広聴AIではない broad listening 事例を、広聴AI利用実績として扱う表現。

## Open Questions

- 外部正本は DD2030 website の `kouchou-ai/case` でよいか、kouchou-ai docs 側にも mirror を置くか。
- 最初の詳細事例は宇多津町、渋谷区、舞鶴2040、八代市のどれにするか。
- 奈良市 official document case と奈良 #全員市長 viewer demo は、同じ地域名で混同されやすいので、公開ページ上でどう分けるか。
- 大阪府のような広義 broad listening 公式 case、サイボウズ / アルティウスリンクのような企業・VOC case を、DD2030 website の `kouchou-ai/case` に入れるか、ブロードリスニング全体 / 応用領域の別 section に分けるか。
- 初回説明 block は DD2030 website に置くか、自治体向け説明資料 / 動画を別 artifact として置くか。
- #696 / #542 の wording を誰が承認するか。技術・法務・渉外の責任境界が要る。
- 公開事例の候補管理を GitHub issue、Drive、website repo、developer wiki のどこで canonical にするか。
- 事例掲載 intake を外部ページに置く場合、問い合わせ先・確認担当・掲載可否の判断基準をどこで管理するか。
- 自治体 user research を public case page の case intake と同居させるか、別 instrument として設計するか。

## Updates

- 2026-06-30: 17:30 JST の direct verification を反映し、大阪府、チームみらい、DirectVote、サイボウズ、アルティウスリンク、与謝野町を公開ページへ載せる場合は source strength と tool lineage で分けると追記。
- 2026-06-30: [[website-kouchou-ai-case-live-2026-06-30]] を追加し、DD2030 website の現行 `src/kouchou-ai/case.vto`、#208/#216/#125/#123 を確認。first slice は `case.vto` 直更新、長期は横断 case-news list と分ける方針を追記。
- 2026-06-30: [[public-tool-catalog-draft-2026-06-30]] を追加し、事例ページ冒頭に tool catalog を置き、`tool_lineage` を `kouchou-ai` / `TTTC lineage` / `broad listening adjacent` / `idobata` / `enterprise` / `candidate` で分ける方針を追記。
- 2026-06-30: [[meeting-municipality-user-research-scope-2026-06-30]] を追加し、case intake と自治体 user research は目的が違うため、同じフォームに混ぜない方がよいと追記。
- 2026-06-30: 16:48 JST 追加Web検索を反映し、自治体公式 proof に奈良市 official PDF 群を追加し、奈良市 document case と奈良 #全員市長 viewer demo を分ける必要を Open Questions に追記。
- 2026-06-30: [[slack-pr-channel-website-faq-case-map-2026-03-04]] を追加し、FAQ の読者分離と case intake 導線を public case page skeleton に反映。
- 2026-06-30: #564 を再読し、公開事例ページに初回説明 FAQ / 一枚絵 / 説明資料導線を置く必要を追記。
- 2026-06-30: [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、公開事例ページに置く「レポートの読み方」の実文言 draft へ接続。
- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、Slack case channel は lead intake、外部ページは primary URL 確認済み case list として分ける方針を追記。
- 2026-06-30: 初回作成。#564 の issue コメント、公開Web検索、#696 / #542 の trust layer をもとに、公開事例ページの構成案を固定した。
