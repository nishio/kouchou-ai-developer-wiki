---
type: source
summary: "DD2030 website 側の広聴AI活用事例ページ live state。`src/kouchou-ai/case.vto` が直接更新先で、#208/#216/#125/#123 が #564 の外部正本候補と分類リスクに関係する"
last_checked: 2026-06-30
coverage: "2026-06-30 18:37 JST に digitaldemocracy2030/website の GitHub issue / PR と work/website/main@2d28aad を再確認。コード変更は行っていない"
sources:
  - https://github.com/digitaldemocracy2030/website
  - https://github.com/digitaldemocracy2030/website/issues/208
  - https://github.com/digitaldemocracy2030/website/issues/216
  - https://github.com/digitaldemocracy2030/website/issues/125
  - https://github.com/digitaldemocracy2030/website/issues/123
  - https://github.com/digitaldemocracy2030/website/issues/126
  - https://github.com/digitaldemocracy2030/website/issues/40
  - https://github.com/digitaldemocracy2030/website/issues/135
  - public-case-page-skeleton-2026-06-30.md
  - public-tool-catalog-draft-2026-06-30.md
  - github-issues-564-696-542-trust-layer-live-2026-06-30.md
---

## Freshness

2026-06-30 17:59 JST に `digitaldemocracy2030/website` を `work/website/` へ clone し、`main@2d28aad` を確認した。18:37 JST に re-pull しても `main@2d28aad` のままで、open PR は #217 `Add English landing page` と #211 `Week51 Summary Update` の 2 本、広聴AI case page そのものを触る open PR は見当たらなかった。GitHub への comment / assign / close は行っていない。

open issue では、#208 `広聴AIの利用事例を更新する`、#216 `Slackに投稿された事例をもとにウェブサイト更新PRを作成する`、#125 `[活用事例]リンク追加/UI改善`、#123 `プロダクト別の事例ページから、プロダクト横断のニュース一覧に変える` が #564 の外部正本候補に直接関係する。

## Current Website Shape

website repo には、product 別の case page がある。

- `src/kouchou-ai/case.vto`
- `src/idobata/case.vto`
- `src/polimoney/case.vto`

`src/kouchou-ai/index.vto` は `活用事例を見る` ボタンで `./case` へ遷移する。したがって、現行 website の外部公開面では `dd2030.org/kouchou-ai/case` が広聴AI活用事例の自然な置き場である。[[public-case-page-skeleton-2026-06-30]]より

ただし、`src/kouchou-ai/case.vto` は structured data や Markdown list ではなく VTO への直書きで、2026-06-30 時点では次の 3 件だけが載っている。

| page item | current state | implication |
|---|---|---|
| 選挙報道 | 説明文のみ。リンクなし | TTTC / AI analysis / media case なのか、広聴AI confirmed case なのかが読者に分かりにくい |
| 東京都の長期戦略「2050東京戦略（案）」 | 説明文のみ。リンクなし | #125 でも「広聴AIの活用事例ではないかも？」という分類不安が出ている |
| 宇多津町のブロードリスニング | official page へのリンクあり | 自治体公式 source strength が強い case として first slice 候補にしやすい |

## Related Website Issues

### #208 広聴AIの利用事例を更新する

#208 は、ブロードリスニング本の公開事例一覧を website に掲載できるとよさそう、という issue。コメントでは、最終的には `src/kouchou-ai/case.vto` を更新することになるが、まずは Web 検索で見つかる広聴AI / ブロードリスニング事例を整理するだけでもよい、という進め方が示されている。

この issue は、[[broad-listening-book-public-case-appendix-2026-06-30]] と [[public-web-broadlistening-japan-use-cases-2026-06-30]] の成果を website に移す自然な受け口である。ただし、book appendix には広聴AI以外も含まれるため、精査が必要と明示されている。

### #216 Slackに投稿された事例をもとにウェブサイト更新PRを作成する

#216 は、Slack `#1_事例紹介_全体` などに流れる広聴AI・いどばた等の活用事例投稿をもとに、AI が website の適切な反映先を提案し、PR を作る workflow の issue。反映先候補として、広聴AI / いどばた / Polimoney / topics などを AI が提案し、人間が確認してから merge する想定である。

これは [[slack-case-introduction-channel-2026-03-04]] の `lead intake` 方針と一致する。Slack 投稿をそのまま public case list に入れるのではなく、candidate として拾い、公開可能 source、tool lineage、掲載先を人間が確認する workflow が必要である。

### #125 活用事例リンク追加 / UI改善

#125 には、選挙報道や東京都 2050 戦略案が「広聴AIの活用事例ではないかも？」という注記つきで候補に挙がっている。これは、現行 `case.vto` へ候補を直接追加すると、広聴AI confirmed case、TTTC lineage、広義 broad listening、media / adjacent case が混ざりやすいことを示す。

#125 のコメントにはチームみらい関連の hosted viewer URL も候補として出ているが、公開 wiki では実環境 URL を転記しない。website へ載せる場合も、その URL 自体ではなく、canonical な public artifact、発行主体、source strength、tool lineage を確認してから扱う必要がある。

このため、[[public-tool-catalog-draft-2026-06-30]] の `tool_lineage` 分類は、単なる内部整理ではなく website issue #125 の分類不安に対する直接の guardrail になる。

### #123 プロダクト別の事例ページから横断ニュース一覧へ

#123 は、プロダクト別 case page だけでなく、事例、ニュース、リリース情報、ユーザーインタビューなどをタグ付けし、プロダクト別にも絞れる横断的な一覧へ変える案である。コメントでは CMS を入れて、非エンジニアや SNS 担当者が更新・管理できるとよい、という方向も出ている。

したがって、短期 first slice は `src/kouchou-ai/case.vto` 更新でよいが、長期 canonical は product-specific case page に固定されていない。#564 の正本を website に置く場合でも、将来は `case.vto` 直書きから tagged content / CMS / cross-product activity list へ移る可能性を残す。

### #126 / #40 / #135

#126 は、各 product detail page から活用事例ページに飛べるようにする issue で、closed。現行 `src/kouchou-ai/index.vto` には case へのボタンがあるので、導線自体は存在する。

#40 は、活用事例ページを Markdown 管理できるようにする案だったが closed。したがって 2026-06-30 時点で case page は Markdown 管理へ移っていない。

#135 は、広聴AI技術解説への動線を website に貼りたい open issue。これは tool catalog / #564 case page と近いが、公開事例そのものではなく技術解説導線である。

## Implications

- DD2030 website は #564 の外部正本として自然だが、現状は `case.vto` 直書きであり、事例 schema / source strength / tool lineage を持つ構造にはなっていない。
- #208 と #216 は、developer wiki で整理した public case candidates を website PR へ移す受け皿になる。
- #125 の分類不安を踏まえると、website へ追加する前に `kouchou-ai confirmed`、`TTTC lineage`、`broad listening adjacent`、`idobata / dialogue`、`enterprise / VOC`、`candidate` を分ける必要がある。
- GitHub issue や Slack に貼られた hosted viewer URL は、そのまま website の公開実績リンクにしない。canonical public source と掲載許諾が確認できるまで candidate として扱う。
- #123 が open のため、長期的な canonical は product-specific page ではなく、tagged / cross-product case-news list になる可能性がある。短期 PR と長期情報設計を混ぜない方がよい。

## Open Questions

- #564 の first slice は website repo #208 / #216 / #125 のどれに接続して進めるべきか。
- `tool_lineage` / `source_strength` は website の visible field にするか、PR 作成前の internal checklist に留めるか。
- #123 の横断 news / case list を待つか、まず `src/kouchou-ai/case.vto` へ verified cases と reading guide を足すか。
- website に載せる reading guide / trust layer は、kouchou-ai docs / public-viewer の文言とどこを canonical にするか。

## Updates

- 2026-06-30: 18:37 JST に website repo / issue / PR を再確認し、`work/website/main@2d28aad` から変化なし、case page 直接更新 PR なしと補正。#125 の hosted viewer 候補は公開 wiki に URL 転記せず、canonical public artifact 確認待ちの candidate として扱う方針を追記。
- 2026-06-30: 初回作成。website repo の case page 構造、関連 issue (#208/#216/#125/#123/#126/#40/#135)、open PR を確認し、#564 の外部正本候補としての DD2030 website の現在地を固定した。
