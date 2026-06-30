---
type: analysis
summary: "広聴AI / いどばた / Cartographer / Jigsaw Sensemaker / tttc-light-js を外向けに混同なく説明するための tool catalog draft。#564 公開事例ページと 8/2 技術・ツール資料へ転用する"
sources:
  - meeting-cartographer-idobata-boundary-2026-06-30.md
  - public-case-page-skeleton-2026-06-30.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
  - event-2026-08-02-tech-tool-brief-draft-2026-06-30.md
  - report-reading-guide-minimum-wording-2026-06-30.md
  - github-issues-564-696-542-trust-layer-live-2026-06-30.md
  - broadlistening.md
  - idobata.md
  - jigsaw-sensemaker.md
  - talk-to-the-city.md
  - website-kouchou-ai-case-live-2026-06-30.md
---

## Conclusion

#564 の公開事例ページや 8/2 の技術・ツール資料では、`ブロードリスニング` を一語で説明しきろうとせず、**collect / deepen / analyze / show / classify / read-and-act** の 6 層に分けるのが安全である。議事録上でも、広聴AI、いどばた、Cartographer、Jigsaw Sensemaker、tttc-light-js は同じ ecosystem に見えるが、主入力・成果物・読者の期待が違う。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

外向けの最短説明は、広聴AIを「集まった自由記述を整理し、論点を見つけやすくする OSS」と置き、いどばた / Cartographer は収集・深掘り側、Jigsaw Sensemaker / tttc-light-js は LLM 直接分類や TTTC lineage の別 route として添える形がよい。これにより、広聴AIが収集・対話・対立調停・政策判断まで全て自動で行うような誤読を避けられる。[[report-reading-guide-minimum-wording-2026-06-30]]より

## Public Tool Catalog Draft

| layer | reader question | primary tool / route | say this | avoid saying |
|---|---|---|---|---|
| collect | どう声を集めるか | アンケート、SNS、対面記録、パブコメ、既存データ、必要に応じた入力プラグイン | 広聴AIは、集まった自由記述を扱いやすい形に取り込んで分析する | 広聴AIだけで意見収集の全設計が完了する |
| deepen | どう深く聴くか | [[idobata]] / Cartographer | いどばた系は、1-on-1 dialogue や追加質問で意見を深掘る側の道具 | いどばた / Cartographer が広聴AIの標準機能である |
| analyze | どう全体構造を見るか | [[kouchou-ai]] | 広聴AIは、収集済み自由記述を抽出・クラスタリング・ラベリングし、論点を見つけやすくする | 多数派証明、統計的世論、政策判断の正しさを保証する |
| show | どう共有・検証するか | public viewer / report / individual opinions | 全体図から個別意見へ戻れるようにし、AIのまとめを人間が検証できる | 図の見栄えがそのまま分析品質や代表性を示す |
| classify | どう別の構造で分類するか | LLM grouping、[[jigsaw-sensemaker]]、[[talk-to-the-city|tttc-light-js]] | LLM 直接分類や tree-native route は、scatter とは別の分析様式として検討されている | Jigsaw や tttc-light-js を広聴AI current UI と同一視する |
| read-and-act | どう判断につなげるか | 人間の読み解き、追加調査、政策・運用判断 | レポートは課題発見・論点把握の補助資料で、次に何を調べるかを決める材料 | AIが民意・結論・合意形成を単独で確定する |

## Drop-in Copy

### Short public copy

広聴AIは、集まった自由記述の意見を LLM とクラスタリングで整理し、論点や課題を見つけやすくする OSS です。アンケート、パブコメ、SNS、対面記録などから得られた声を、全体像から個別意見まで行き来しながら読むために使います。

ただし、広聴AIは統計的な世論調査や政策判断を自動化するものではありません。結果は対象データと集め方に依存するため、重要な判断では収集方法、元データ、文脈、人間による確認とあわせて読む必要があります。[[report-reading-guide-minimum-wording-2026-06-30]]より

### Ecosystem copy

声を集めたり深掘りしたりする段階では、アンケート設計、対面記録、いどばたのような対話型ツール、Cartographer のような追加質問・理解補助が関係します。広聴AIはその後段で、集まった自由記述を分析・可視化し、公開 viewer や report として読みやすくする役割を担います。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

Jigsaw Sensemaker や tttc-light-js のような LLM 直接分類 / TTTC 系の route は、散布図中心の広聴AIとは別の分析様式として参考になります。特に対立軸発見や tree-native な整理は重要な next theme だが、現行広聴AIの default capability として約束しない。[[jigsaw-sensemaker]]より [[talk-to-the-city]]より

## Placement

| surface | recommended role | note |
|---|---|---|
| DD2030 website / #564 public case page | 外向け canonical。事例一覧の前に tool catalog と reading guide を置く | #564 の「広聴AIって何？ / 何ができる？」への初回回答に使う |
| 8/2 event material | 1 枚の tool ecosystem 図。collect / deepen / analyze / show / classify / read-and-act を分ける | 技術・ツール lane と実践 lane の橋渡しに使う |
| kouchou-ai docs | 「レポートを見る」「データを準備する」「読み方」の技術寄り補足 | developer quickstart や Windows setup とは読者を分ける |
| public-viewer / README | 誤読防止、責任所在、図とラベルの読み方 | #696 / #542 の trust layer として扱う |

DD2030 website は外向け canonical として自然だが、2026-06-30 時点では `src/kouchou-ai/case.vto` への直書き page で、事例 schema や `tool_lineage` field はない。website issue #208 / #216 / #125 は case 更新の受け皿であり、#123 は将来の cross-product case-news list 化を示している。したがって、短期は `case.vto` first slice、長期は tagged list / CMS 可能性、と分けて考える。[[website-kouchou-ai-case-live-2026-06-30]]より

## How this changes #564

#564 の first slice では、事例数を増やす前に、事例ページ冒頭へこの tool catalog を短く入れる。導入検討者は「どんな事例があるか」だけでなく、「自分たちが必要としているのは収集なのか、深掘りなのか、分析・可視化なのか、公開 viewer なのか」を知りたいからである。[[public-case-page-skeleton-2026-06-30]]より

事例一覧の `tool_lineage` は、少なくとも次の値を分ける。

- `kouchou-ai`: 広聴AI confirmed / public artifact あり
- `Talk to the City lineage`: TTTC / tttc-light-js / TTTC 由来
- `broad listening adjacent`: 広義の broad listening / AI 支援住民対話
- `idobata / dialogue`: 収集・深掘り・提案生成側
- `enterprise / VOC`: 企業・顧客の声分析
- `candidate`: primary public source / 掲載許諾 / tool lineage が未確認

この分類がないと、大阪府のような広義 broad listening official case、チームみらいのような複数 tool の政策形成 case、DirectVote のような TTTC lineage、サイボウズ / アルティウスリンクのような enterprise / VOC case が、すべて「広聴AI導入実績」として誤読される。[[public-case-page-skeleton-2026-06-30]]より

## What Not To Do

- 広聴AIを「ブロードリスニング全体の総称」として使わない。
- いどばた / Cartographer / Jigsaw Sensemaker / tttc-light-js を、広聴AIの current product capability として列挙しない。
- 対立軸発見を、現行広聴AIの default output として約束しない。
- 公開事例ページで、広義 broad listening / TTTC lineage / enterprise VOC / candidate を `広聴AI利用実績` と一括表示しない。
- Slack-only / Drive-only の事例や、許諾未確認のスクリーンショットを public page の根拠にしない。

## Open Questions

- この tool catalog の正本は DD2030 website か、kouchou-ai docs か、8/2 event material か。
- Cartographer を外向け資料で固有名詞として出すか、`追加質問・理解補助のプロトタイプ` と一般化するか。
- `tool_lineage` の値は public case page の field として固定するか、内部整理だけに留めるか。
- 対立軸発見を LLM grouping の future capability として説明する場合、どの程度まで公開 roadmap に出すか。

## Updates

- 2026-06-30: 初回作成。[[meeting-cartographer-idobata-boundary-2026-06-30]] を #564 公開事例ページと 8/2 技術・ツール資料に転用するため、外向け tool catalog draft と drop-in copy に落とした。
- 2026-06-30: [[website-kouchou-ai-case-live-2026-06-30]] を反映し、DD2030 website は短期 canonical 候補だが、現状は `case.vto` 直書きで、長期は #123 の横断 case-news list と分けると追記。
