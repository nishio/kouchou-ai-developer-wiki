---
type: source
summary: "議事録から見た自治体利用者課題調査の scope。広聴活動一般の探索と、広聴AIが活きるケースの探索を分ける必要がある"
last_checked: 2026-06-30
coverage: "raw/meeting_minutes.txt; 2025-11 discussion around municipality survey, user bias, department targeting, and Cartographer feedback"
sources:
  - meeting-minutes.md
  - meeting-brand-compass-information-strategy-2026-06-30.md
  - public-case-page-skeleton-2026-06-30.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
---

## What it is

2026-06-30 17:20 JST に `raw/meeting_minutes.txt` を読み、自治体向けアンケート / 利用者課題調査の scope を整理した source。議事録上では、Ohki が「広聴AIユーザー、特に自治体がどんな課題を抱えているか」を知るためのアンケート案を共有し、nishio が対象部署や役割の明確化、既存接点の偏りを指摘している。[[meeting-minutes]]より

この source はアンケート本文の転載ではなく、今後の product / docs / public case page 判断に使える論点だけを残す。

## Freshness marker

議事録 source は [[meeting-minutes]] の freshness marker に従う。2026-06-30 16:33 JST に Google Doc export を再取得済みで、先頭見出しは `2026/06/22`、`2026/06/29` 見出しは未検出、txt は 7702 行。[[meeting-minutes]]より

## Observations

議事録には、自治体の「広聴活動」全般の課題を広く集める案と、現状の広聴AIが活きそうなケースに限定して課題を集める案の揺れがある。前者は広い探索には向くが、広聴AI開発に直結しない課題も拾いやすい。後者は開発判断に効きやすいが、既存の想定ユースケースに調査を閉じすぎる危険がある。[[meeting-minutes]]より

Cartographer にアンケート案を入れた結果、対象者の部署・役割・人数規模を明確にする必要が示された。議事録では、広聴活動に間接的に関わる人も対象にしたい一方、100 件程度という期待値には強い根拠がないことも明示されている。[[meeting-minutes]]より

DD2030 が現時点で接点を持てている自治体関係者は、広聴AIを入口に関係が始まった広報・広聴課やデジタル推進部署に偏っている可能性がある。そのため「自治体の広聴活動における課題」を知っていると見なすのは危険である。[[meeting-brand-compass-information-strategy-2026-06-30]]より

同じ議事録には、自治体・候補者 / 政治家・企業用途・コールセンターなど、ユースケース候補の幅も出ている。これらを 1 つのアンケートに混ぜると、誰の課題を聞いているのかが曖昧になる。[[meeting-minutes]]より

## Reading

自治体利用者課題調査は、#564 の公開事例ページとは目的が違う。

- #564 / public case page は、導入検討者の既存質問に先回りして答え、実績・読み方・責任境界を示す入口である。[[public-case-page-skeleton-2026-06-30]]より
- 自治体利用者課題調査は、広聴AIのロードマップが既存接点や既存想定に偏っていないかを確かめる探索である。

したがって、調査を設計する時は、少なくとも次の 2 層を分けるのがよい。

| layer | purpose | sample questions |
|---|---|---|
| 広聴活動一般の探索 | 自治体が現在どのように声を集め、処理し、意思決定へ渡しているかを知る | どの部署が、どんなチャネルで、どの頻度で、どの規模の自由記述を扱っているか |
| 広聴AI適合ケースの探索 | 広聴AIがすぐ効きそうな入力・運用・公開条件を見つける | 自由記述がどの形式で残っているか、公開 viewer が必要か、分析担当と発行主体は誰か |

この分離をしないと、広聴AIが解くべきでない収集・合意形成・組織調整の課題を product backlog に入れてしまうか、逆に現行広聴AIに合うケースだけを聞いて broader need を見落とす。

## Implication

公開事例ページには `掲載候補を教えてください` の case intake を置けるが、それは利用者課題調査とは別である。case intake は確認済み public URL や掲載許諾を集める導線で、user research は未顕在の課題や部署横断の運用を知る導線である。[[issue-564-public-case-trust-layer-scope-2026-06-30]]より

8/2 や Brand Compass 文脈で人間が決めるべきことは、アンケートを「広聴活動一般の実態調査」として出すのか、「広聴AIが活きるケースの発見」に寄せるのか、あるいは 2 つの instrument に分けるのかである。

## Open Questions

- 調査対象は、広報・広聴課、デジタル推進、企画、各事業部門、首長 / 議員周辺のどこまで含めるか。
- 100 件程度という期待値に対し、どの sampling route を使うか。既存接点だけで集めると偏りが残る。
- 「広聴AIが活きるケース」を聞く前に、自治体側の現在の広聴 workflow をどの粒度で聞くか。
- Cartographer / いどばた / 広聴AI / Talk to the City のどれに解くべき課題かを、調査票内でどう切り分けるか。
- 調査結果を product issue、public docs、case page、Brand Compass のどこへ還流するか。

## Updates

- 2026-06-30: 初回作成。議事録から、自治体利用者課題調査は public case page / case intake と分け、広聴活動一般の探索と広聴AI適合ケースの探索を切り分ける必要があると整理した。
