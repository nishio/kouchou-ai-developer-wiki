---
type: source
summary: "Issue #564 / #696 / #542 の live state。活用事例公開は、誤読防止とレポート責任所在を含む trust layer として扱う必要がある"
last_checked: 2026-06-30
coverage: "2026-06-30 16:19 JST に GitHub issue #564, #696, #542 と #542 の参照元 #539 を gh issue view で確認。#564/#696/#542 は open / unassigned"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/564
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/696
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/542
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/539
  - source-code.md
  - slack-logs-repository.md
  - slack-case-introduction-channel-2026-03-04.md
---

## What it is

広聴AIの公開事例・導入説明・レポートの読み方に関係する GitHub issue の live state。

2026-06-30 に `gh issue view -R digitaldemocracy2030/kouchou-ai` で確認した。16:12 JST に #564、16:19 JST に #696 / #542 / #539 を再確認したが、state / assignee / comments は変わっていない。GitHub への comment / assign / close は行っていない。

## Freshness marker

- `#564` は open / high priority / unassigned。last update は 2025-09-28 で、担当者が活動困難のため assign を外したコメントが最後。
- `#696` は open / unassigned。2025-08-21 作成で、広聴AIレポートを誤って解釈しないための説明・プロダクト組み込み・website 掲載を論点にしている。
- `#542` は open / unassigned。2025-05-19 作成で、レポートに関する責任の所在を README / footer などに明記する提案。参照元 `#539` は closed で、利用規約はレポート出力者側が書くもの、判断結果の責任所在は免責事項に書くもの、という切り分けがある。

`#564` 本文・コメントには Slack 由来の事例紹介 channel や Google Drive へのポインタがある。ただし Drive 内の非公開資料や Slack-only anecdote は、この source では公開 wiki に転記しない。`work/slack-logs` の `#1_事例紹介_全体` (`C08LJ9T5MLY`) raw / mirror は存在するが、2026-06-30 確認時点の local snapshot では 2025-05 / 2025-06 の該当メッセージ本文は入っていなかった。[[slack-logs-repository]]より

その後 `#1_事例紹介_全体` の 2026-03/04 raw を確認し、北見、舞鶴2040、相模原、宮崎、和歌山など少数の事例 lead があることを [[slack-case-introduction-channel-2026-03-04]] に固定した。これは public case list の一次根拠ではなく、primary URL 確認へ進める lead intake として扱う。

## Issue #564: 活用事例を集めて公開する

目的は、広聴AIを利用しようとするユーザーにとって、様々な活用事例があると導入ハードルが下がるため、事例を集めて公開すること。

コメント上の重要点:

- 自治体側は、他自治体の事例に強い関心を示している。
- 質問は「意見を集める具体的方法」「X からの収集方法」「費用」「手書き意見 / OCR」「どんな話題に使えるか」「どう使うとよいか」まで広い。
- 事例公開で公開されがちなのは成果物・発表だが、自治体が本当に知りたいのは、導入検討、体制づくり、テーマ決定、実施内容、やってみた結果、成果 / report までの連なり。
- dd2030 website に、利用検討者向けの説明資料や活用事例を公開できる形にしておく案が出ている。
- `広聴AIって何？` / `何ができる？` / `どう使える？` / `使うにはどうしたらいい？` という最初の説明を、毎回個別対応しなくてよい形でまとめたいというコメントがある。
- 利用状況一覧の一枚絵、プロダクト x 政党・行政・議員・その他組織のグリッド、有賀さんの自治体向け説明資料 / 動画の再利用など、事例 detail とは別の「最初に渡す武器」も求められている。
- 既にコンタクトのあった国政政党・政治団体は引き継ぎ待ちという運用メモがある。公開ページは渉外情報そのものではなく、公開可能な説明・事例・導入 FAQ に絞る必要がある。

## Issue #696: 誤読防止

背景は、広聴AIレポートが「なんとなく説得力を産むツール」として誤読されるリスク。issue 本文では、ブロードリスニングは質的調査・定性分析に近く、一般に広がる過程で暗黙の前提知識が失われることを問題にしている。

論点:

- 広聴AIは課題発見ツールとして説明した方がよい可能性がある。
- 画像・可視化は説得力を持ってしまうので、良い分析であることや代表性を自動保証するように見せない。
- 有権者へのアピールと内部利用の分析は方針を分ける必要がある。
- 入れる場所は README、プロダクト、website、解説記事、書籍など複数候補。
- 背景 thread では、広聴AIの性質、データの読み方、何が得られるか、追加調査の考え方を整理する必要があるとされている。
- `課題発見ツール` と言い切る案が出ている。これは、見栄えのよい可視化が「良い分析」や「多数派の証明」に見えてしまうことへの対策である。
- 注意書きは、単なる footer 免責ではなく、プロダクト内・website・README/docs・解説記事など複数 surface にまたがる。

## Issue #542: レポート責任所在

問題は、レポートの footer には dd2030 の免責事項があるが、レポートに関する責任の所在が明記されていないこと。

提案は、README / footer の免責事項に、レポートに関する責任の所在を明記すること。これは #696 の「誤読防止」と #564 の「事例公開」を支える trust layer として読むべきである。

参照元 #539 では、footer の利用規約リンクは、広聴AI側の規約ではなく「広聴AIを使ってレポートを出力した人・組織」が記載するものだと確認されている。悪用禁止、二次利用、サービス変更・停止はユーザー側が各自で設定すべきものとされ、広聴AI側の免責事項に入れるべきものとして「サービスを利用して判断した結果の責任の所在」が issue 化された。したがって #542 は、`termsLink` の有無ではなく、レポート発行主体と OSS / DD2030 の責任境界を読者に誤解させない問題として読む。

## Current code cross-check

2026-06-30 に `work/kouchou-ai/main@d5c9ece6e3b3` を確認したところ、public-viewer footer には既にレポーター帰属と発行責任者への問い合わせ文言が入っている。一方 README / docs index の免責は LLM バイアスと保証なしが中心で、個別レポートの発行主体と OSS / DD2030 の責任境界は揃っていない。[[source-code]]より

したがって #542 は、current main では「footer 文言が完全に欠けている」というより、README / docs / public-viewer / 事例ページの文言統一問題として読む方がよい。最小文言案は [[report-reading-guide-minimum-wording-2026-06-30]] に固定した。

## Open Questions

- #564 の正本は kouchou-ai issue のままでよいか、それとも website repo / dd2030 website 側へ移管するか。
- 事例ページの minimum schema は、公開 artifact だけでよいか、導入検討 / 体制 / テーマ決定 / 実施内容 / 結果まで含めるか。
- #696 / #542 の注意書きは、公開事例ページ、public-viewer footer、本体 docs、README のどれを canonical にするか。
- Slack / Drive にある事例情報を、どの owner が公開可能 / 非公開に scrub するか。

## Updates

- 2026-06-30: 16:19 JST に #696 / #542 / #539 を再読し、内部分析と対外アピールの混同、課題発見ツールとしての説明、termsLink はレポート出力者側のものという責任境界を追記。
- 2026-06-30: 16:12 JST に #564 を再読し、活用事例公開は事例 detail だけでなく、初回説明 FAQ / 一枚絵 / 説明資料導線も求められていると追記。
- 2026-06-30: [[source-code]] と [[report-reading-guide-minimum-wording-2026-06-30]] を追加し、#542 は current main では footer 単純追加ではなく、README / docs / viewer / 事例ページの責任境界統一として読むと補正。
- 2026-06-30: [[slack-case-introduction-channel-2026-03-04]] を追加し、`#1_事例紹介_全体` は lead intake として使い、外部公開では primary URL 確認済み case だけを載せる方針を追記。
- 2026-06-30: 初回作成。Issue #564 / #696 / #542 を live state として確認し、活用事例公開を trust layer として扱う必要を固定した。
