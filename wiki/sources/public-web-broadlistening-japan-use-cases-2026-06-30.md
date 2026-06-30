---
type: source
summary: "2026-06-30 に公開Web検索で確認した、日本国内の広聴AI / Talk to the City / ブロードリスニング活用事例の棚卸し"
last_checked: 2026-06-30
coverage: "public web search; official pages, public viewers, organization announcements, and candidates that still need primary confirmation"
sources:
  - https://dd2030.org/kouchou-ai/case
  - https://www.town.utazu.lg.jp/page/4114.html
  - https://www.city.shibuya.tokyo.jp/kusei/kocho/questionnaire/kuminishikichosa_ai.html
  - https://files.city.shibuya.tokyo.jp/assets/12995aba8b194961be709ba879857f70/38d509b421d049c4ad53536fc88ae4ca/kuminishikichosa_ai.pdf
  - https://www.pref.hiroshima.lg.jp/site/hiroshima-dx-torikumi/hiroshimanomirai.html
  - https://maizuru2040.jp/wordpress/
  - https://maizuru2040.jp/kouchou-ai-reports/
  - https://maizuru2040.jp/kouchou-ai-reports/faq/
  - https://www.city.maizuru.kyoto.jp/shisei/0000014341.html
  - https://everyonemayor.github.io/kouchou-ai/2025-7-13/
  - https://democracy-x.org/news/yatsushiro-kouchouai-202508/
  - https://democracy-x.github.io/kouchou-ai-yatsushiro/47ae7bf4-e5de-4dbd-82ab-520160f373d6/
  - https://new-kokumin.jp/news/diet/20250307_2
  - https://dd2030.org/broad-listening/
  - public-broadlistening-artifacts-2026-06-30.md
  - slack-case-introduction-channel-2026-03-04.md
---

## What it is

広聴AI、Talk to the City、その他のブロードリスニング系実践について、2026-06-30 に公開Web検索で確認した日本国内の活用事例メモ。Slack / Drive / 非公開議事録ではなく、外部にそのまま出典として示せる public page / public viewer / 公式発表を優先した。

この source は公開事例の最終採用リストではない。検索結果には、ページが 404 になっているもの、検索 snippet では見えるが一次ページを読めていないもの、広聴AIではなく広義のブロードリスニングだけを示すものが混ざる。そのため、事例は `confirmed` / `candidate` / `secondary context` に分ける。

## Freshness marker

2026-06-30 15:22 JST 時点の public web search pass。`dd2030.org/kouchou-ai/case`、宇多津町、渋谷区、広島県、舞鶴2040、奈良 #全員市長、八代市、国民民主党の公開ページを確認した。[[public-broadlistening-artifacts-2026-06-30]]より

広聴AI本体の public viewer は HTML に大きな JSON が埋め込まれているため、URL、title / description、reporter、comment count など公開 HTML 上で読める範囲を確認した。検索 snippet だけの事例はこのページでは confirmed に昇格しない。

## Confirmed public cases

| case | source strength | what was confirmed | notes |
|---|---|---|---|
| DD2030 official case page | DD2030 official | 広聴AIの活用事例として、選挙報道、東京都 2050 戦略案、宇多津町の 3 類型が紹介されている。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | 事例名の入口として使えるが、個別の詳しい根拠は各 primary page を併読する。 |
| 宇多津町 | municipality official | 第2次宇多津町総合計画の町民アンケート自由記述 396 件を、広聴AIで整理するブロードリスニング trial として公開。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | 自治体公式かつ件数・用途が明確。#564 の public case schema に最も載せやすい。 |
| 渋谷区 | municipality official | 令和6年度区民意識調査の自由回答 6,037 件を対象に、デジタル民主主義2030の広聴AIでブロードリスニング trial を実施。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | 既存の 8/2 棚卸しにも入っている trust context。PDF は HTTP 200 を確認。 |
| 広島県 | prefecture official | 「デジタル化で描く未来の広島」で、意見をブロードリスニング（AI技術）で整理・見える化・公表し、デジタル民主主義2030の協力を得て実施すると公開。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | ページ上では `広聴AI` の語は確認できないため、広義の broad listening / DD2030 cooperation として扱う。 |
| 舞鶴2040 | public viewer + FAQ + city project page | `#みんなでつくる舞鶴2040` の特設サイト / レポート一覧 public viewer があり、FAQ で広聴AIは DD2030 の OSS 成果物と説明されている。舞鶴市公式ページでは、意見募集と特設サイトでの公表、総合計画への参考利用が確認できる。[[slack-case-introduction-channel-2026-03-04]]より | 8/2 の viewer demo 候補に追加できる。市公式ページと特設サイト / viewer を分けて引用する。 |
| 奈良 #全員市長 | public viewer | `2025年7月13日のレポート - 全員市長` public viewer が公開され、公開 HTML 上で comment count 1022 と読める。[[public-broadlistening-artifacts-2026-06-30]]より | 既存の primary viewer demo 候補。政治・選挙文脈の説明が必要。 |
| 八代市 Democracy-X | public article + viewer | Democracy-X 記事で、八代市長と連携し、広聴AIを用いて市民の声を可視化したブロードリスニングとして説明されている。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | Deep case 候補。ただし政治・政策文脈の言い方に注意する。 |
| 国民民主党 / 伊藤孝恵議員 | party official | 就職氷河期世代の声を、電話、Googleフォーム、SNS、YouTube live などから集め、AIで収集・分析し政策ニーズを可視化したブロードリスニング結果として国会質疑に用いた。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より | 広聴AI利用とは断定しない。AI broad listening の政治・国会利用例として扱う。 |

## Talk to the City / adjacent context

DD2030 のブロードリスニング説明ページは、2024〜2025 年に日本でも実践事例が急速に増えたと説明し、広聴AIを DD2030 が開発しているブロードリスニング支援 OSS の一つとして位置づけている。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より

Talk to the City は広聴AIの系譜理解には重要だが、公開事例マップでは `Talk to the City そのものを使った事例` と `Talk to the City を参考にした広聴AI事例` を混ぜない。八代市 public viewer の footer でも、広聴AIが AI Objectives Institute の Talk to the City を参考に開発されていると説明されている。[[public-web-broadlistening-japan-use-cases-2026-06-30]]より

## Candidate leads not yet confirmed enough

- 日本維新の会: Web 検索では `政策AI活用プロジェクト` や public viewer らしき結果が見えるが、今回確認した GitHub Pages URL は 404 だった。公式発表と現在有効な viewer URL を再確認するまで candidate に留める。
- 岩手県: Web 検索では `広聴AI` / `BOOTS` / 幸福ワークショップ関連の PDF が見えるが、今回の直接 URL 確認では PDF が 404 だった。現行 URL を確認してから昇格する。
- 奈良市 official PDF: Web 検索では `広聴AI` / 1361 ideas / `こんなまちになったらいいな` が見えるが、既知 PDF URL は 404 だった。public viewer は confirmed、official PDF は candidate。
- アルティウスリンク、朝日新聞 M研、日本テレビ、GMO、JINS: 検索や既存書籍 source では関連例として見えるが、今回の public web pass では primary page を十分に確認できていない。外部資料へ載せるなら個別確認が必要。
- Slack `#1_事例紹介_全体` の lead: [[slack-case-introduction-channel-2026-03-04]] に固定した通り、Slack lead は candidate intake として有用だが、外部公開では primary public URL へ昇格したものだけを実績扱いにする。

## Open Questions

- 8/2 の public viewer demo は、奈良、八代、舞鶴2040のどれを第一候補にするか。
- #564 の外部公開ページに載せる case は、自治体公式 source に限るか、政党・国会・選挙報道・viewer-only case も含めるか。
- Talk to the City 由来の日本事例は、広聴AIページに入れるか、ブロードリスニングの歴史 / 系譜ページへ分けるか。
- 404 になっている viewer / PDF は、単なる URL 移動か、公開停止か。

## Updates

- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、舞鶴2040を Slack lead から official project page / special site / public viewer 確認済み case として補強した。
- 2026-06-30: 初回作成。公開Web検索で、日本国内の広聴AI / Talk to the City / ブロードリスニング活用事例を confirmed / candidate / secondary context に分けた。
