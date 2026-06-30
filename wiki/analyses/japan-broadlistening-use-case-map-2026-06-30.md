---
type: analysis
summary: "公開Web検索で確認した日本国内の広聴AI / Talk to the City / ブロードリスニング活用事例を、8/2 イベントと #564 公開事例整備へ接続する地図"
sources:
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - slack-case-introduction-channel-2026-03-04.md
  - public-broadlistening-artifacts-2026-06-30.md
  - event-2026-08-02-public-example-inventory-2026-06-30.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
  - slack-pr-channel-website-faq-case-map-2026-03-04.md
  - current-status-2026-06-30.md
  - broad-listening-book-public-case-appendix-2026-06-30.md
---

## Conclusion

2026-06-30 の公開Web検索で、8/2 と #564 に使える公開事例は既存の 3 件より広がった。ただし、すべてを同列の「広聴AI活用事例」と呼ぶと、公式自治体 trial、public viewer、政党・国会利用、Talk to the City の系譜、検索 snippet だけの候補が混ざる。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より

短期の使い分けは次が安全である。

- **公式性を示す事例**: 宇多津町、渋谷区、奈良市総合計画関連資料、広島県、岩手県、東京都 2050 戦略案、大阪府、DD2030 official case page。自治体・公共 sector の trust context として使う。ただし大阪府は広聴AI confirmed ではなく、広義 broad listening case として分ける。
- **viewer demo に向く事例**: 奈良 #全員市長、八代市、舞鶴2040、北見。広聴AI viewer の読み方を見せる素材として使う。
- **政治・国会文脈の事例**: 国民民主党 / 伊藤孝恵議員、日本維新の会、チームみらい、八代市、奈良 #全員市長。文脈説明と誤読防止が必須。
- **政党 AI / broad listening adjacent**: 公明党 We Connect。公式 source はあるが、広聴AI confirmed ではなく、党組織・Google Form・AI 分析を組み合わせた政策立案 process として扱う。
- **系譜・歴史文脈**: Talk to the City、東京都知事選 2024、東京都 2050 戦略案、DirectVote、日本テレビ衆院選報道、M-1 2024。広聴AIそのものの導入実績ではなく、ブロードリスニングの発展として分ける。
- **実装支援者 / platform integration**: Code for Japan / 加古川市・品川区 Decidim、株式会社ブーツ、Democracy X 八代市。実装支援者側の public source と自治体公式 proof を分ける。
- **収集・熟議 platform**: 東京都AI戦略いどばた会議、すぎなみブロードリスニング、中央区みんなでアップデート会議。いどばた / broad listening の public practice として有用だが、広聴AIの分析・可視化実績ではない。
- **企業 / VOC / civic discussion / adjacent AI**: サイボウズ、アルティウスリンク、JINS、GMO、litela Recogra、富士通パブリックコメント AI。サイボウズとアルティウスリンクは direct public source ありへ進められるが、自治体向け first demo ではなく応用領域として扱う。litela と富士通は広聴AI confirmed ではなく、それぞれ対面議論支援と LLM直接分類 adjacent として扱う。
- **候補 / adjacent**: 中野駅新北口、与謝野町、東大阪市、太田市、田原本町、富岡市、長崎県知事選、相模原市の意見募集結果 PDF など。与謝野町は official PDF があるが、広聴AI confirmed ではなく AI 支援住民対話 adjacent として扱う。相模原市は公式 PDF 内の市民提案・市回答であり、実施済み case ではなく municipality demand signal。東大阪市 / 太田市 / 田原本町 / 富岡市 / 長崎県知事選は primary URL 追加確認待ち。[[broad-listening-book-public-case-appendix-2026-06-30]]より

Slack `#1_事例紹介_全体` は、事例 candidate の lead intake として有用だが、public case list の一次根拠にはしない。2026-03/04 raw には北見の広聴AI・いどばた lead、舞鶴2040、相模原市 AI avatar、宮崎県の broad listening 言及、和歌山県いどばたへの内部リンクなどが混ざっており、`広聴AI confirmed case` / `broad listening mention` / `adjacent civic AI` / `internal pointer` に分ける必要がある。[[slack-case-introduction-channel-2026-03-04]]より

## Implication for 8/2

既存の [[event-2026-08-02-public-example-inventory-2026-06-30]] は、渋谷区 official page / PDF、奈良 public viewer、八代市 deep case、synthetic fallback の順序にしていた。今回の検索後も、default order は大きく変えなくてよい。むしろ、最初の trust context を渋谷区だけに背負わせず、宇多津町、奈良市 official PDF 群、岩手県、DD2030 official case page、広島県、東京都 2050、大阪府の official page を補助線として持てるようになった。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より

奈良市 official PDF 群は、`奈良 #全員市長` public viewer と混ぜない方がよい。前者は自治体公式 document case として「広聴AIが公共計画資料に入った」ことを示す素材、後者は viewer 操作と政治・選挙文脈を扱う素材で、source strength と public risk が違う。

viewer demo は、奈良と八代に加えて舞鶴2040と北見が候補になる。舞鶴2040は public viewer と FAQ が確認でき、タイトルも地域の未来づくりに寄っているため、政治・選挙色を下げたい場合の代替候補になり得る。北見は public portal / viewer として読みやすいが、自治体公式 source ではなく地域 project として source strength を下げる。ただし実施主体、公開許諾、イベントでのスクリーンショット利用可否は別途確認する。

東京都AI戦略いどばた会議、すぎなみブロードリスニング、中央区みんなでアップデート会議は、8/2 の first demo を置き換える素材ではなく、`collect / deepen / deliberate` 側の public practice として tool ecosystem slide に置くのが自然である。広聴AIの viewer 操作を見せる素材にすると、分析・可視化 tool と収集・熟議 platform の役割が混ざる。

## Implication for #564

#564 の public case page は、単なるリンク集ではなく、事例の source strength を明示するべきである。最小 schema は [[issue-564-public-case-trust-layer-scope-2026-06-30]] にある通りだが、今回の検索で `source_strength` と `classification` を追加した方がよいと分かった。

| field | why it matters |
|---|---|
| classification | municipality official / public viewer / party official / media / company / candidate を分ける |
| source_strength | official page, public viewer, organization article, secondary article, search snippet を分ける |
| tool lineage | 広聴AIそのものか、Talk to the City か、広義の broad listening / AI analysis かを分ける |
| public risk | 政治・選挙文脈、代表性、権利、個人情報、誤読可能性を分ける |

この分類を入れないと、「広聴AIが民意を保証した」「同じ技術で全事例が作られた」と誤読される。#696 / #542 と接続した trust layer は、事例数が増えるほど重要になる。

事例管理の運用では、`lead intake` と `public page` を分ける。Slack / Drive / issue comment は lead の発見に使い、外部ページは primary URL と許諾・文脈確認を通ったものだけを載せる。[[slack-case-introduction-channel-2026-03-04]]より

`lead intake` は、単に内部で候補を拾うだけでは足りない。Slack `#2_広報_pr` の 2026-04 議論では、DD2030 から見えない活用に気づくには、HP 上で導入事例マップや掲載希望の受け皿を見せる必要がある、という発想が出ていた。#564 の public page は、確認済み事例一覧と候補 intake を明確に分けたうえで、外部から候補が入る導線を持つ方が自然である。[[slack-pr-channel-website-faq-case-map-2026-03-04]]より

## Recommended next page shape

外部公開へ移す前の developer wiki 正本としては、`公開事例マップ` を次の章立てにするのがよい。

1. まず見るべき 3 事例: 宇多津町・渋谷区・奈良市 official PDF のいずれか、舞鶴2040または奈良 viewer、八代市。
2. 自治体 / 公共 sector の事例: 宇多津町、渋谷区、奈良市、岩手県、広島県、東京都 2050 戦略案、大阪府。大阪府は広聴AI confirmed ではなく広義 broad listening と明示する。
3. 政治・国会・選挙報道の事例: 国民民主党、日本維新の会、チームみらい、奈良、八代、日本テレビ衆院選報道。
4. Talk to the City と広聴AIの関係: 直接利用、派生利用、広義の broad listening を分ける。東京都知事選 2024 / DirectVote / M-1 / JINS / GMO はここに入れる。
5. 収集・熟議 platform: 東京都AI戦略いどばた会議、すぎなみブロードリスニング、中央区みんなでアップデート会議。広聴AI事例ではなく、いどばた / broad listening platform の実践として分ける。
6. 実装支援者 / platform integration: Code for Japan / 加古川市・品川区 Decidim、株式会社ブーツ、Democracy X 八代市。自治体公式 proof と実装支援者 source を分ける。
7. 企業 / VOC / civic discussion / adjacent AI: サイボウズ、アルティウスリンク、litela Recogra、富士通パブリックコメント AI。自治体向け first demo とは分け、応用領域として出す。
8. 候補と追加確認リスト: 北見、中野駅新北口、与謝野町、東大阪市、太田市、田原本町、富岡市、長崎県知事選、相模原市の需要シグナル、企業・メディア系。与謝野町は AI 支援住民対話 adjacent、相模原市は公式 PDF 上の提案・回答であり実施済み case ではない。他は primary confirmation queue。

## Open Questions

- 8/2 で政治色を下げるなら、奈良の代わりに舞鶴2040を viewer demo 第一候補にするか。
- 奈良市 official document case と `奈良 #全員市長` viewer demo を、8/2 や #564 で同じ「奈良」枠にまとめるか、source strength が違う別事例として出すか。
- DD2030 website の `kouchou-ai/case` は外部正本として十分か、それとも #564 の schema に沿って拡張する必要があるか。
- 広島県のように `広聴AI` と明記しない broad listening / DD2030 cooperation 事例を、広聴AI事例ページに載せるか、別カテゴリに分けるか。
- 検索で見えたが 404 だった viewer / PDF の現行 URL を誰が確認するか。
- Web book 付録由来の候補は、どの順で primary URL direct verification するか。
- JINS や M-1 のような TTTC / broad listening adjacent cases を #564 の公開事例ページに載せるか、技術・歴史 reference に分けるか。
- サイボウズ / アルティウスリンクのような企業・VOC case を、DD2030 website の公開事例ページに入れるか、自治体向けページとは別の応用領域 section に分けるか。
- Code for Japan / 加古川市・品川区、litela Recogra、富士通パブリックコメント AI のような public source あり adjacent case を、公開事例ページではどこまで載せるか。
- Democracy X / 長崎県知事選は、どの public report URL を source of truth として確認するか。
- 東京都AI戦略いどばた会議、すぎなみブロードリスニング、中央区みんなでアップデート会議は、広聴AI case page に adjacent section として載せるか、tool catalog / broad listening history 側へ分けるか。
- 外部からの事例候補 intake を public page に置く場合、source strength / tool lineage / 掲載許諾を誰が判定するか。

## Updates

- 2026-06-30: 18:46 JST の追加検索を反映し、東京都AI戦略いどばた会議 / すぎなみブロードリスニング / 中央区みんなでアップデート会議を `collect / deepen / deliberate` 側に分類し、相模原市 official PDF は実施済み事例ではなく demand signal として扱う方針にした。
- 2026-06-30: 18:13 JST に `work/broad-listening-book/main@9c22db6` の Code for Japan / Democracy X / litela / 公明党 / 富士通章を確認し、Code for Japan / 加古川市・品川区、公明党 We Connect、litela Recogra、富士通パブリックコメント AI を source strength 付き分類へ進めた。長崎県知事選は public report URL 未確認なので candidate のまま。
- 2026-06-30: 18:05 JST の追加Web検索を反映し、Code for Japan / 加古川市、Democracy X / 長崎県知事選、litela / 田原本町・富岡市、富士通パブリックコメント AI を primary confirmation queue に追加した。
- 2026-06-30: 17:30 JST の direct verification を反映し、大阪府、チームみらい、DirectVote、サイボウズ、アルティウスリンク、与謝野町を `book appendix candidate` から source strength 付き分類へ進めた。
- 2026-06-30: [[broad-listening-book-public-case-appendix-2026-06-30]] を追加し、Web book 付録由来の追加候補は `book appendix candidate` として primary URL direct verification queue に置くと整理した。
- 2026-06-30: 16:48 JST の追加Web検索を反映し、奈良市 official PDF 群を自治体公式 document case へ昇格、東京都知事選 2024 TTTC / GMO / 中野駅新北口を adjacent practice として分類した。
- 2026-06-30: [[slack-pr-channel-website-faq-case-map-2026-03-04]] を追加し、公開事例ページには確認済み事例一覧だけでなく事例候補 intake 導線も必要だと追記。
- 2026-06-30: 16:05 JST の追加Web検索を反映し、岩手県・日本維新の会を candidate から昇格、東京都 / GovTech東京・北見・日本テレビ衆院選・M-1・JINS を分類へ追加。
- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、Slack 事例紹介 channel は lead intake であり public case list とは分ける必要があると追記。
- 2026-06-30: 初回作成。公開Web検索をもとに、8/2 と #564 へ接続する日本国内 broad listening use case map を作成した。
