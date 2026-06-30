---
type: analysis
summary: "公開Web検索で確認した日本国内の広聴AI / Talk to the City / ブロードリスニング活用事例を、8/2 イベントと #564 公開事例整備へ接続する地図"
sources:
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - slack-case-introduction-channel-2026-04.md
  - public-broadlistening-artifacts-2026-06-30.md
  - event-2026-08-02-public-example-inventory-2026-06-30.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
  - current-status-2026-06-30.md
---

## Conclusion

2026-06-30 の公開Web検索で、8/2 と #564 に使える公開事例は既存の 3 件より広がった。ただし、すべてを同列の「広聴AI活用事例」と呼ぶと、公式自治体 trial、public viewer、政党・国会利用、Talk to the City の系譜、検索 snippet だけの候補が混ざる。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より

短期の使い分けは次が安全である。

- **公式性を示す事例**: 宇多津町、渋谷区、広島県、DD2030 official case page。自治体・公共 sector の trust context として使う。
- **viewer demo に向く事例**: 奈良 #全員市長、八代市、舞鶴2040。広聴AI viewer の読み方を見せる素材として使う。
- **政治・国会文脈の事例**: 国民民主党 / 伊藤孝恵議員、八代市、奈良 #全員市長。文脈説明と誤読防止が必須。
- **系譜・歴史文脈**: Talk to the City、東京都 2050 戦略案、選挙報道。広聴AIそのものの導入実績ではなく、ブロードリスニングの発展として分ける。
- **候補**: 日本維新の会、岩手県、奈良市 official PDF、企業・メディア系。現行 primary URL を確認するまで公開資料では補助線に留める。

Slack `#1_事例紹介_全体` は、事例 candidate の lead intake として有用だが、public case list の一次根拠にはしない。2026-04 raw には舞鶴2040、相模原市 AI avatar、宮崎県の broad listening 言及、和歌山県いどばたへの内部リンクなどが混ざっており、`広聴AI confirmed case` / `broad listening mention` / `adjacent civic AI` / `internal pointer` に分ける必要がある。[[slack-case-introduction-channel-2026-04]]より

## Implication for 8/2

既存の [[event-2026-08-02-public-example-inventory-2026-06-30]] は、渋谷区 official page / PDF、奈良 public viewer、八代市 deep case、synthetic fallback の順序にしていた。今回の検索後も、default order は大きく変えなくてよい。むしろ、最初の trust context を渋谷区だけに背負わせず、宇多津町、DD2030 official case page、広島県の official page を補助線として持てるようになった。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より

viewer demo は、奈良と八代に加えて舞鶴2040が候補になる。舞鶴2040は public viewer と FAQ が確認でき、タイトルも地域の未来づくりに寄っているため、政治・選挙色を下げたい場合の代替候補になり得る。ただし実施主体、公開許諾、イベントでのスクリーンショット利用可否は別途確認する。

## Implication for #564

#564 の public case page は、単なるリンク集ではなく、事例の source strength を明示するべきである。最小 schema は [[issue-564-public-case-trust-layer-scope-2026-06-30]] にある通りだが、今回の検索で `source_strength` と `classification` を追加した方がよいと分かった。

| field | why it matters |
|---|---|
| classification | municipality official / public viewer / party official / media / company / candidate を分ける |
| source_strength | official page, public viewer, organization article, secondary article, search snippet を分ける |
| tool lineage | 広聴AIそのものか、Talk to the City か、広義の broad listening / AI analysis かを分ける |
| public risk | 政治・選挙文脈、代表性、権利、個人情報、誤読可能性を分ける |

この分類を入れないと、「広聴AIが民意を保証した」「同じ技術で全事例が作られた」と誤読される。#696 / #542 と接続した trust layer は、事例数が増えるほど重要になる。

事例管理の運用では、`lead intake` と `public page` を分ける。Slack / Drive / issue comment は lead の発見に使い、外部ページは primary URL と許諾・文脈確認を通ったものだけを載せる。[[slack-case-introduction-channel-2026-04]]より

## Recommended next page shape

外部公開へ移す前の developer wiki 正本としては、`公開事例マップ` を次の章立てにするのがよい。

1. まず見るべき 3 事例: 宇多津町または渋谷区、舞鶴2040または奈良 viewer、八代市。
2. 自治体 / 公共 sector の事例: 宇多津町、渋谷区、広島県、東京都 2050 戦略案。
3. 政治・国会・選挙報道の事例: 国民民主党、奈良、八代、選挙報道。
4. Talk to the City と広聴AIの関係: 直接利用と派生利用を分ける。
5. 候補と追加確認リスト: 岩手県、日本維新の会、企業・メディア系。

## Open Questions

- 8/2 で政治色を下げるなら、奈良の代わりに舞鶴2040を viewer demo 第一候補にするか。
- DD2030 website の `kouchou-ai/case` は外部正本として十分か、それとも #564 の schema に沿って拡張する必要があるか。
- 広島県のように `広聴AI` と明記しない broad listening / DD2030 cooperation 事例を、広聴AI事例ページに載せるか、別カテゴリに分けるか。
- 検索で見えたが 404 だった viewer / PDF の現行 URL を誰が確認するか。

## Updates

- 2026-06-30: [[slack-case-introduction-channel-2026-04]] を追加し、Slack 事例紹介 channel は lead intake であり public case list とは分ける必要があると追記。
- 2026-06-30: 初回作成。公開Web検索をもとに、8/2 と #564 へ接続する日本国内 broad listening use case map を作成した。
