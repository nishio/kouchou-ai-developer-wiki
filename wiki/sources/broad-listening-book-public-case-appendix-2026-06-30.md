---
type: source
summary: "Web 公開版「選挙を変えたブロードリスニング」の公開事例一覧を、広聴AI / Talk to the City / その他 broad listening 事例の追加候補カタログとして要約"
last_checked: 2026-06-30
coverage: "public web search; book appendix, web book top page, and supporting public search hits"
sources:
  - https://github.com/digitaldemocracy2030/broad-listening-book/blob/main/99_%E4%BB%98%E9%8C%B2_%E5%85%AC%E9%96%8B%E4%BA%8B%E4%BE%8B%E4%B8%80%E8%A6%A7.md
  - https://broadlisteningbook.com/ja/
  - https://www.docswell.com/s/tokoroten/ZL1M88-2025-06-14-014546
  - https://note.com/kosonippon/n/n67fe713c2811
  - https://www.jmooc.jp/images/upload/2026/06/JMOOCWS_20260325_Tanenobu_1780904234037.pdf
  - https://www.pref.osaka.lg.jp/o060020/senryaku_kikaku/broad_listening.html
  - https://policy.team-mir.ai/policies/digital-democracy
  - https://takahiroanno.com/directvote
  - https://cybozu.co.jp/not-shirokuro/
  - https://www.altius-link.com/news/detail20260511.html
  - https://www.town.yosano.lg.jp/assets/yosanomiraikaigi_teian.pdf
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - broad-listening-book-source.md
---

## What it is

2026-06-30 17:05 JST の追加 public web search で確認した、Web 公開版「選挙を変えたブロードリスニング」と GitHub 上の `99_付録_公開事例一覧.md` の要約。既存の [[public-web-broadlistening-japan-use-cases-2026-06-30]] は public web search で direct に開いた事例を中心に整理していたが、この付録は広聴AI / Talk to the City / その他 broad listening の日本国内事例をまとめた public catalog として使える。

ただし、この source は「各事例の primary page をすべて再確認した」という意味ではない。外部向け公開事例ページへ載せる前には、付録内の URL を個別に開き、自治体公式・政党公式・public viewer・技術記事・書籍カタログ由来を分けて source strength を付ける必要がある。

2026-06-30 17:30 JST の direct verification で、大阪府、チームみらい、DirectVote、サイボウズ、アルティウスリンク、与謝野町は primary / organization page を個別確認した。確認結果は [[public-web-broadlistening-japan-use-cases-2026-06-30]] に反映済み。ただし、確認できたという事実は「全部が広聴AI confirmed case」という意味ではなく、自治体 broad listening、政党・政策形成、企業 VOC、TTTC lineage、AI 支援住民対話 adjacent に分ける必要がある。

## Findings

Web book / GitHub 付録は、既存 map の確認済み事例に加えて、次の候補群を public catalog として示している。

- 自治体 / 公共 sector: 大阪府は府公式 broad listening 実証ページまで確認できた。与謝野町は official proposal PDF まで確認したが、広聴AI confirmed ではなく AI 支援住民対話 adjacent として扱う。東大阪市、太田市は引き続き primary confirmation queue に残す。渋谷区、奈良市、岩手県、広島県、宇多津町、舞鶴2040、八代市、東京都 2050 など既存 map に入っている事例と合わせて、自治体公式・地域 project・public viewer を分ける必要がある。[[broad-listening-book-public-case-appendix-2026-06-30]]より
- 政党 / 国会 / 選挙: チームみらい official policy page と DirectVote campaign official page を確認できた。公明党は引き続き primary confirmation queue に残す。国民民主党、日本維新の会、日本テレビ衆院選報道、東京都知事選 2024 TTTC と並べる時は、広聴AI利用実績と broad listening 実践を混ぜない分類が必要である。[[broad-listening-book-public-case-appendix-2026-06-30]]より
- 企業 / メディア / civic tech: アルティウスリンクは official press release、サイボウズは official project / report page まで確認できた。JINS、GMO Developers、M-1 2024 は引き続き TTTC / broad listening adjacent として扱う。企業・メディア系は自治体公式 proof ではなく、応用領域・技術・VOC分析の public example として分ける。[[broad-listening-book-public-case-appendix-2026-06-30]]より

Docswell の広聴AI技術解説は、Talk to the City から広聴AIへ至る技術系譜と、現時点の広聴AIがどういう pipeline で読まれるかの公開説明として使える。JMOOC PDF や東大阪市の note は、広聴AIそのものの導入実績として断定するより、ブロードリスニング / AI ファシリテーション / 自治の自己理解設計の周辺事例として読む方が安全である。

## Implication

#564 の公開事例ページや 8/2 event material では、この付録を「事例数を増やす根拠」に使うだけでは危ない。むしろ、次の 4 分類を public page schema に入れる根拠として使う。

| category | examples | handling |
|---|---|---|
| 広聴AI confirmed / official | 渋谷区、宇多津町、奈良市 official PDF、岩手県など | primary URL を直接確認し、自治体公式 source として載せる |
| public viewer / regional project | 奈良 #全員市長、舞鶴2040、北見、八代市など | viewer demo としては有用だが、政治文脈・実施主体・許諾を別途確認する |
| broad listening / TTTC lineage | 東京都 2050、大阪府、東京都知事選 2024、DirectVote、M-1、JINS、GMO など | 広聴AIそのものではなく、系譜・技術・応用例として説明する |
| enterprise / VOC / civic discussion | サイボウズ、アルティウスリンクなど | 広聴AI confirmed artifact でも、自治体向け first demo とは分け、応用領域として説明する |
| book appendix candidate | 東大阪市、太田市、公明党など | 付録 URL だけで confirmed 扱いにせず、次の direct verification queue に置く |

8/2 の first demo は、引き続き primary URL と表示状態を direct に確認済みの viewer / official document から選ぶのがよい。付録は「日本でも多領域に広がっている」ことを示す breadth slide や、次に検証する candidate list に使う。

## Open Questions

- 付録由来の候補のうち、次に direct verification する 3 件はどれか。自治体 official を増やすなら東大阪市 / 太田市、政党文脈を増やすなら公明党、企業文脈を増やすならサイボウズ / アルティウスリンク以外の primary page が候補。
- Web book / GitHub 付録を #564 の外部公開ページで source として出すか、内部の candidate intake に留めるか。
- Docswell の技術解説を 8/2 の「技術 / ツール」入口に使う場合、広聴AI本体 docs、dd2030.org、broadlisteningbook.com のどこを canonical にするか。
- 大阪府のような広義 broad listening / Liqlid 系の自治体公式 case を、広聴AIページに置くか、ブロードリスニング全体のページに分けるか。

## Updates

- 2026-06-30: 17:30 JST の direct verification で、大阪府、チームみらい、DirectVote、サイボウズ、アルティウスリンク、与謝野町を `book appendix candidate` から source strength 付きの分類へ進めた。
- 2026-06-30: 初回作成。公開Web検索で、Web book 付録を国内 broad listening 活用事例の追加候補カタログとして固定した。
