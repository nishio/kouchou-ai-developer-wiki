---
type: source
summary: "議事録から見た Brand Compass / 情報発信 / stable v4 / 利用者課題調査の接続。Brand Compass 本体ではなく、議事録上の判断フィルタを要約する"
last_checked: 2026-06-30
coverage: "raw/meeting_minutes.txt; 2026-06-22 priority list plus older meeting snippets on M2, external messaging, user discovery, and A/B/C/D distribution"
sources:
  - meeting-minutes.md
  - meeting-2026-06-22-event-priority.md
  - kouchou-ai.md
  - usage-modes.md
---

## What it is

2026-06-30 17:15 JST に `raw/meeting_minutes.txt` を読み、Brand Compass / 情報発信 / stable v4 / 利用者課題調査 / 配布形態 A/B/C/D のつながりを整理した source。

注意: この source は Brand Compass 本体の内容を読んだものではない。議事録内で `Brand Compass に沿った開発` がどういう判断フィルタとして現れているかを要約する。

## Freshness marker

議事録 source は [[meeting-minutes]] の freshness marker に従う。2026-06-30 16:33 JST に Google Doc export を再取得済みで、先頭見出しは `2026/06/22`、`2026/06/29` 見出しは未検出、txt は 7702 行。[[meeting-minutes]]より

## Observations

2026-06-22 の「今後追求する事」は、Brand Compass に沿った開発、high priority issues、情報発信と事例の積み上げ、運用ポリシーの改善の 4 本で始まる。これは 8/2 イベントだけでなく、直近定例で繰り返される優先軸として読める。[[meeting-2026-06-22-event-priority]]より

過去の M2 / stable v4 文脈では、ブロードリスニング本発売に合わせて、バグフィクス、ドキュメント、わかりにくい UI の改善、v4 挙動との食い違い検証が優先として出ている。一方、新しい view / 解析手法の追加や pipeline customization は「余裕があれば」であり、Web UI 上の大きな新機能より、JSON / YAML 設定や plugin 的な別軸で扱う方がよい、という読みが出ている。[[meeting-minutes]]より

書籍・外部発信文脈では、ブロードリスニングを「発信に偏った民主主義へ、聞く能力を与える」方向の物語として打ち出す流れがある。これは事例数を増やすだけではなく、広聴AIを democracy / broad listening の循環にどう位置づけるかの説明責務である。[[meeting-minutes]]より

利用者課題調査の文脈では、DD2030 が接触できている自治体関係者は、広聴AIを入口に接点ができた広報・広聴課やデジタル推進部署に偏っている可能性が示されている。そのため「自治体の広聴活動における課題」を分かったつもりにならず、広聴AIが活きそうなケースと、広聴活動一般の課題を分けて聞く必要がある。[[meeting-minutes]]より

配布形態 A/B/C/D は、単なる実装構成ではなく、対外説明の切り口でもある。研究者向け ipynb、エンジニア向け pip、デプロイできる組織向け Web UI、エンジニアがいない組織向け hosted trial を分けることで、誰に何を提供しているのかを説明しやすくなる。[[kouchou-ai]]より [[usage-modes]]より

## Reading

Brand Compass に沿った開発は、個別 issue の優先順位表をそのまま消化する話ではなく、次の 4 つを合わせる判断フィルタとして読むのが安全である。

1. stable v4 / M2 に向けた現行価値の安定化。
2. 情報発信と事例の積み上げによる trust layer の整備。
3. 「聞く能力」を民主主義の物語として説明できる外部発信。
4. 実利用者の課題を、既存接点の偏りを意識して取りに行くこと。

この読み方だと、短期の docs / wiki 作業は単なる周辺作業ではない。8/2 や #564 に向けて、公開事例、レポートの読み方、利用モード、何を保証しないかを揃えることが、Brand Compass / 情報発信 / stable v4 の共通土台になる。

## Open Questions

- Brand Compass 本体のどの項目が、現行の docs / public case / stable v4 整理と直接対応しているか。
- M2 / stable v4 の「バグフィクス・ドキュメント・わかりにくい UI 改善」は、現在の open issue / PR 群のどれを first slice にするのがよいか。
- 自治体向け利用者課題調査は、広聴AIが活きそうなケースに絞るのか、広聴活動一般の課題探索として広く聞くのか。
- A/B/C/D の配布形態を、dd2030.org / kouchou-ai docs / broadlisteningbook.com のどこで説明するか。

## Updates

- 2026-06-30: 初回作成。議事録から、Brand Compass / 情報発信 / stable v4 / 外部発信 / 利用者課題調査の接続を固定した。
