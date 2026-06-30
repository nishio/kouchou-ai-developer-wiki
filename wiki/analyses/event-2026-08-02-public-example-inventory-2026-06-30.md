---
type: analysis
summary: "8/2 イベントで使う公開可能事例・デモ素材を、public-ready / 確認待ち / fallback / 使用不可に分けた棚卸し"
sources:
  - event-2026-08-02-broadlistening-readiness-2026-06-30.md
  - event-2026-08-02-tech-tool-brief-draft-2026-06-30.md
  - public-broadlistening-artifacts-2026-06-30.md
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - japan-broadlistening-use-case-map-2026-06-30.md
  - azure-demo-public-visibility-proposal-2026-06-04.md
  - azure-demo-visibility-thread-resolution-2026-06-05.md
  - broad-listening-book-source.md
  - broad-listening-book-extractions.md
  - meeting-minutes.md
  - source-code.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
---

## Conclusion

8/2 イベントで衝突なく使いやすい demo stack は、(1) 渋谷区 official page / PDF で自治体公式の public artifact があることを示す、(2) 奈良 #全員市長の public viewer で広聴AIの読み方を見せる、(3) 八代市は深い実践事例として扱えるが、政治・政策文脈の表現に注意する、という順序が安全である。[[public-broadlistening-artifacts-2026-06-30]]より

公開Web検索で、宇多津町、広島県、舞鶴2040、国民民主党などの public source も確認できた。ただし 8/2 の default demo order は大きく変えず、公式性を補強する source と viewer demo の代替候補として使うのがよい。[[japan-broadlistening-use-case-map-2026-06-30]]より

Azure デモ環境は、現時点では「自分のデータを投入する場所」より「使い方や準備データを理解する参照環境」として位置づけ直されている。したがって 8/2 では、専用環境を主役にするより、公開事例 / サンプルレポート / サンプル CSV の導線を前面に出す方がよい。[[azure-demo-public-visibility-proposal-2026-06-04]]より [[azure-demo-visibility-thread-resolution-2026-06-05]]より

## Candidate Inventory

| candidate | public artifact | why useful | risk / required check | 8/2 use |
|---|---|---|---|---|
| 奈良 #全員市長 | public viewer: https://everyonemayor.github.io/kouchou-ai/2025-7-13/ | 1,000 件規模の public viewer として、全体図 / 濃いクラスタ / 階層図 / 個別意見へ戻る流れを見せやすい。[[public-broadlistening-artifacts-2026-06-30]]より | local politics / campaign context の説明が必要。イベント直前に URL と表示状態を再確認する。 | primary viewer demo 候補 |
| 渋谷区 official trial | official page / PDF | 自治体公式ページとして、広聴AIが公共 sector で試されている証拠を示せる。[[public-broadlistening-artifacts-2026-06-30]]より | viewer 実演というより official proof。スクリーンショット利用や PDF 図表利用は要確認。 | trust / context 用 |
| 八代市 Democracy-X | public article + result viewer | 実践 lane と技術 lane をつなぐ深いケース。政策課題の発見と viewer を接続できる。[[public-broadlistening-artifacts-2026-06-30]]より | 選挙・政策文脈を含む。「みんなが一番望んでいる」ではなく「そのニーズが見つかった」と説明する。[[meeting-minutes]]より | speaker が文脈を扱える場合の deep case |
| 舞鶴2040 | public viewer + FAQ | 地域の未来像づくりに寄った public viewer で、広聴AI OSS 成果物の活用が FAQ で確認できる。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | 実施主体・許諾・スクリーンショット利用可否を確認する。 | 政治色を下げたい場合の viewer demo 代替候補 |
| 宇多津町 | municipality official page | 第2次総合計画の町民アンケート自由記述 396 件を広聴AIで整理した自治体公式 case。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | viewer demo ではなく official proof。 | trust / context 用 |
| 広島県 | prefecture official page | 意見をブロードリスニング（AI技術）で整理・見える化・公表し、DD2030 協力で実施すると公式ページにある。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | `広聴AI` の語はページ上で確認できないため、広義の broad listening / DD2030 cooperation として説明する。 | official context 用 |
| 国民民主党 / 伊藤孝恵議員 | party official page | AI で政策ニーズを可視化したブロードリスニング結果を国会質疑に用いた public case。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | 広聴AI利用とは断定しない。政治・国会文脈の説明が必要。 | broad listening の活用幅を示す補助例 |
| 朝日新聞 | book case | ラベル抽象化、SNS キーワード設計、外れ値除外要望など、技術説明の lesson が多い。[[broad-listening-book-extractions]]より | 図表・紙面・引用・画像は権利確認が必要。 | lesson 用。viewer demo にはしない |
| サイボウズ / 富士通 / 企業・NPO系 | book / meeting references | 公共 sector 以外の利用可能性を示せる。[[broad-listening-book-source]]より | 権利者、顔出し、公開範囲の確認が必要。 | owner confirmation 後 |
| 岩手県 / 郡山 / kuu village | meeting references | pipeline of prospects として、広聴AIが複数現場で話題化していることを示せる。[[meeting-minutes]]より | 公開 artifact が未確認。Slack / 議事録だけで外部説明しない。 | background only |
| synthetic sample CSV | 自前で作るサンプル | 権利・個人情報リスクが低く、admin upload の操作説明に使える。 | 現実の説得力は弱い。サンプル設計が必要。 | fallback / technical dry-run |

## Recommended 8/2 Demo Order

1. 渋谷区 official page / PDF を冒頭に置き、自治体公式の public artifact があることを示す。
2. 奈良 #全員市長 public viewer で、全体図、濃いクラスタ、階層図、クラスタ説明、個別意見への戻り方を見せる。
3. 八代市は、政治・政策文脈を説明できる speaker がいる場合だけ deep case として扱う。表現は「そのニーズが見つかった」に寄せる。
4. live viewer が落ちた場合、または政治文脈を避けたい場合に備えて、synthetic sample CSV / static screenshot / recorded flow の fallback を用意する。

政治色を下げたい場合は、奈良 viewer の代替として舞鶴2040 viewer を第一候補にできる可能性がある。舞鶴2040は public viewer と FAQ が確認できたため、次に見るべきは表示安定性ではなく、イベントでの見せ方・許諾・実施主体の説明である。[[japan-broadlistening-use-case-map-2026-06-30]]より

この順序なら、技術・ツール lane だけで閉じず、実践 lane と接続しながらも、未確認の deployment detail や private data に触れずに説明できる。[[event-2026-08-02-tech-tool-brief-draft-2026-06-30]]より

## Do Not Use Without Confirmation

- Azure デモ環境の admin URL、resource 名、revision、run log、secret / access 周辺の詳細。
- 書籍・取材・議事録に出てくるが、公開 artifact や許諾が未確認のスクリーンショット、図表、発言、内部 report。
- Slack だけにある anecdote。公開 artifact や issue / PR / docs に落ちていないものは、イベントの外部説明では使わない。
- Dependabot alerts や security details。公開 wiki には対応 issue / PR / 優先度判断までに留める。

## Docs Implication

本体 docs / 公開ページに移すなら、最初の landing は「自分で環境を立てる」ではなく、公開事例と viewer の読み方に置く方が自然である。current docs は OS 別 setup と user guide に寄っており、8/2 の短い説明には「事例を見る → viewer を読む → 自分のデータを準備する → 必要なら setup へ進む」という導線が不足している。[[source-code]]より

ただし、公開事例は単独で出さず、#696 の誤読防止と #542 の責任所在を含む trust layer として扱う。最小単位は「公開事例リスト + レポートの読み方 + 何を保証しないか」であり、詳細 scope は [[issue-564-public-case-trust-layer-scope-2026-06-30]] に固定した。

## Open Questions

- 8/2 の第一候補 viewer は奈良 #全員市長でよいか。それとも八代市、舞鶴2040、synthetic sample、別自治体を主役にするか。
- 渋谷区 PDF / 八代市 viewer / 奈良 viewer のスクリーンショットをスライドに載せてよいか。
- sample CSV を public repo / docs 側に置くなら、どの repository のどの path を canonical にするか。
- 広島県の公開中間結果など、追加で候補へ昇格できる artifact を誰が確認するか。

## Updates

- 2026-06-30: [[public-web-broadlistening-japan-use-cases-2026-06-30]] / [[japan-broadlistening-use-case-map-2026-06-30]] を追加し、宇多津町 / 舞鶴2040 / 広島県 / 国民民主党などを official context / viewer demo / political context に分類して追記。
- 2026-06-30: [[issue-564-public-case-trust-layer-scope-2026-06-30]] を追加し、公開事例 demo は #696 誤読防止 / #542 責任所在とセットで出す必要があると追記。
- 2026-06-30: 初回作成。公開 artifact として奈良 #全員市長 / 渋谷区 / 八代市を primary 候補に置き、広島県・朝日新聞・企業系は確認待ち、synthetic sample は fallback として整理した。
