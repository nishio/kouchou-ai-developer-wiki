---
type: source
summary: "Issue #564 / #696 / #542 の live state。活用事例公開は、誤読防止とレポート責任所在を含む trust layer として扱う必要がある"
last_checked: 2026-06-30
coverage: "GitHub issue #564, #696, #542 を gh issue view で確認。いずれも open / unassigned"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/564
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/696
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/542
  - source-code.md
  - slack-logs-repository.md
  - slack-case-introduction-channel-2026-03-04.md
---

## What it is

広聴AIの公開事例・導入説明・レポートの読み方に関係する GitHub issue の live state。

2026-06-30 に `gh issue view -R digitaldemocracy2030/kouchou-ai` で確認した。GitHub への comment / assign / close は行っていない。

## Freshness marker

- `#564` は open / high priority / unassigned。last update は 2025-09-28 で、担当者が活動困難のため assign を外したコメントが最後。
- `#696` は open / unassigned。2025-08-21 作成で、広聴AIレポートを誤って解釈しないための説明・プロダクト組み込み・website 掲載を論点にしている。
- `#542` は open / unassigned。2025-05-19 作成で、レポートに関する責任の所在を README / footer などに明記する提案。

`#564` 本文・コメントには Slack 由来の事例紹介 channel や Google Drive へのポインタがある。ただし Drive 内の非公開資料や Slack-only anecdote は、この source では公開 wiki に転記しない。`work/slack-logs` の `#1_事例紹介_全体` (`C08LJ9T5MLY`) raw / mirror は存在するが、2026-06-30 確認時点の local snapshot では 2025-05 / 2025-06 の該当メッセージ本文は入っていなかった。[[slack-logs-repository]]より

その後 `#1_事例紹介_全体` の 2026-03/04 raw を確認し、北見、舞鶴2040、相模原、宮崎、和歌山など少数の事例 lead があることを [[slack-case-introduction-channel-2026-03-04]] に固定した。これは public case list の一次根拠ではなく、primary URL 確認へ進める lead intake として扱う。

## Issue #564: 活用事例を集めて公開する

目的は、広聴AIを利用しようとするユーザーにとって、様々な活用事例があると導入ハードルが下がるため、事例を集めて公開すること。

コメント上の重要点:

- 自治体側は、他自治体の事例に強い関心を示している。
- 質問は「意見を集める具体的方法」「X からの収集方法」「費用」「手書き意見 / OCR」「どんな話題に使えるか」「どう使うとよいか」まで広い。
- 事例公開で公開されがちなのは成果物・発表だが、自治体が本当に知りたいのは、導入検討、体制づくり、テーマ決定、実施内容、やってみた結果、成果 / report までの連なり。
- dd2030 website に、利用検討者向けの説明資料や活用事例を公開できる形にしておく案が出ている。

## Issue #696: 誤読防止

背景は、広聴AIレポートが「なんとなく説得力を産むツール」として誤読されるリスク。issue 本文では、ブロードリスニングは質的調査・定性分析に近く、一般に広がる過程で暗黙の前提知識が失われることを問題にしている。

論点:

- 広聴AIは課題発見ツールとして説明した方がよい可能性がある。
- 画像・可視化は説得力を持ってしまうので、良い分析であることや代表性を自動保証するように見せない。
- 有権者へのアピールと内部利用の分析は方針を分ける必要がある。
- 入れる場所は README、プロダクト、website、解説記事、書籍など複数候補。

## Issue #542: レポート責任所在

問題は、レポートの footer には dd2030 の免責事項があるが、レポートに関する責任の所在が明記されていないこと。

提案は、README / footer の免責事項に、レポートに関する責任の所在を明記すること。これは #696 の「誤読防止」と #564 の「事例公開」を支える trust layer として読むべきである。

## Current code cross-check

2026-06-30 に `work/kouchou-ai/main@d5c9ece6e3b3` を確認したところ、public-viewer footer には既にレポーター帰属と発行責任者への問い合わせ文言が入っている。一方 README / docs index の免責は LLM バイアスと保証なしが中心で、個別レポートの発行主体と OSS / DD2030 の責任境界は揃っていない。[[source-code]]より

したがって #542 は、current main では「footer 文言が完全に欠けている」というより、README / docs / public-viewer / 事例ページの文言統一問題として読む方がよい。最小文言案は [[report-reading-guide-minimum-wording-2026-06-30]] に固定した。

## Open Questions

- #564 の正本は kouchou-ai issue のままでよいか、それとも website repo / dd2030 website 側へ移管するか。
- 事例ページの minimum schema は、公開 artifact だけでよいか、導入検討 / 体制 / テーマ決定 / 実施内容 / 結果まで含めるか。
- #696 / #542 の注意書きは、公開事例ページ、public-viewer footer、本体 docs、README のどれを canonical にするか。
- Slack / Drive にある事例情報を、どの owner が公開可能 / 非公開に scrub するか。

## Updates

- 2026-06-30: [[source-code]] と [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、#542 は current main では footer 単純追加ではなく、README / docs / viewer / 事例ページの責任境界統一として読むと補正。
- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、`#1_事例紹介_全体` は lead intake として使い、外部公開では primary URL 確認済み case だけを載せる方針を追記。
- 2026-06-30: 初回作成。Issue #564 / #696 / #542 を live state として確認し、活用事例公開を trust layer として扱う必要を固定した。
