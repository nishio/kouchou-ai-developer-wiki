---
title: "open Issue 全件のコード照合 2026-10-28（スプリント開始）"
type: source
summary: "2026-10-28 スプリント開始時に open Issue 全89件を古い順 12 シャードで current main@1028da9c へ照合し、close/実装/統合と判定した38件を別 agent が懐疑検証した一次記録。観測日時・基準 commit・方法・未確認範囲。判定一覧とスプリント提案は issue-backlog-audit-2026-10-28"
last_checked: 2026-10-28 JST
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues
  - source-code.md
  - issue-audit-2026-10-12-full.md
---

## What it is

digitaldemocracy2030/kouchou-ai の open Issue 全件（**89 件**、open PR 0 件）を 2026-10-28 に現行 main へ照合した根拠 source。前回 [[issue-audit-2026-10-12-full]]（105 件、main `c297bc97`）以降に main に入った 167 commit を踏まえ、各 issue の「満たした要件 / 残件 / 10-12 以降の変化 / 対応方針」を判定した。判定の正本と、今スプリントで着手する候補の順序は [[issue-backlog-audit-2026-10-28]]。

## Freshness marker

- 基準コード: `work/kouchou-ai` の current main `1028da9c63b94850baa36fe24911ce62544b52cb`（2026-10-27 の [#1152](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1152) まで。観測日 2026-10-28）
- 公開 GitHub: 各 issue の本文・全コメント・assignee・ラベル、関連 PR、Dependabot alerts（件数のみ転記）を観測。生データ（issue 1 件 = 1 JSON、前回判定の索引、10-12 以降の commit 一覧、workflow の返り値、統合後の `results.json`）は `raw/issue-audit/2026-10-28-sprint/` に固定（`raw/` は gitignored）
- 対象 89 件: 11, 44, 56, 60, 79, 121, 170, 172, 173, 186, 190, 213, 221, 227, 236, 250, 255, 266, 280, 285, 289, 292, 293, 308, 310, 323, 324, 337, 339, 342, 345, 346, 364, 366, 370, 374, 395, 445, 454, 464, 470, 471, 493, 496, 503, 507, 513, 516, 517, 518, 529, 546, 547, 548, 556, 558, 564, 576, 586, 592, 638, 641, 643, 648, 669, 679, 809, 869, 879, 880, 881, 882, 885, 898, 913, 921, 949, 954, 973, 974, 989, 991, 994, 997, 1012, 1042, 1128, 1130, 1131
- 前回棚卸しに無い新規 11 件: 973, 974, 989, 991, 994, 997, 1012, 1042, 1128, 1130, 1131

## 方法

- dynamic workflow（agent 23、実行約 3 時間、subagent 約 237 万 token）。古い順 8 件ずつ 12 シャードの照合 agent が、issue JSON・前回判定・commit 一覧・現行 main のコード（読み取り専用、checkout しない）・`gh` の読み取りを使い、verdict（解決済 / 一部解決 / 未解決 / 要件再確認 / 前提消失）と action（close / implement_now / merge_into / keep_backlog / needs_human）、size、user_value、assignee の扱い、根拠、次の一手を構造化出力した
- close / implement_now / merge_into と判定された 38 件は、シャードごとに別の懐疑検証 agent が「反証できなければ維持、曖昧なら保守側」で再判定。11 件を人間判断・保留へ修正した（内訳は analysis の「懐疑検証で修正した 11 件」）
- 途中で Claude の 5 時間枠の上限に当たり、3 agent がリセット後に再実行された。失敗シャードは 0
- GitHub への書き込み（close・assign・コメント・ラベル）は行っていない。close 候補 4 件も人間の操作待ち

## 未確認範囲

- アプリ起動・実ブラウザでの視覚確認はしていない（[#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121) [#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60) [#213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/213) [#227](https://github.com/digitaldemocracy2030/kouchou-ai/issues/227) [#266](https://github.com/digitaldemocracy2030/kouchou-ai/issues/266) [#493](https://github.com/digitaldemocracy2030/kouchou-ai/issues/493) などはコード読解のみ）
- 実 LLM / 実 API を使う検証はしていない（[#913](https://github.com/digitaldemocracy2030/kouchou-ai/issues/913) [#991](https://github.com/digitaldemocracy2030/kouchou-ai/issues/991) [#994](https://github.com/digitaldemocracy2030/kouchou-ai/issues/994) [#1131](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1131)）。OpenAI の利用明細・アカウント設定は参照できない
- 外部 repo で進む実験（[#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324) [#346](https://github.com/digitaldemocracy2030/kouchou-ai/issues/346) [#370](https://github.com/digitaldemocracy2030/kouchou-ai/issues/370) [#516](https://github.com/digitaldemocracy2030/kouchou-ai/issues/516)）の現在の中身、Google Slides / Drive の資料（[#517](https://github.com/digitaldemocracy2030/kouchou-ai/issues/517) [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564)）は未確認
- Apple Silicon の Docker（[#898](https://github.com/digitaldemocracy2030/kouchou-ai/issues/898)）、Windows + WSL2 / Podman（[#496](https://github.com/digitaldemocracy2030/kouchou-ai/issues/496)）の実機は無い。GitHub Actions の実行ログ（[#643](https://github.com/digitaldemocracy2030/kouchou-ai/issues/643) [#973](https://github.com/digitaldemocracy2030/kouchou-ai/issues/973) [#974](https://github.com/digitaldemocracy2030/kouchou-ai/issues/974)）と GitHub Project の field（[#454](https://github.com/digitaldemocracy2030/kouchou-ai/issues/454)、token に read:project が無い）も未調査
- `gh pr list --search <番号>` は全文検索で雑音が多く、issue に紐づく未 merge PR が無いことは「open PR 0 件」の前提と合わせた判断
- umap-learn の「random_state=None なら並列」は公式ドキュメントの記述に依拠し、実パッケージでは未確認（[#809](https://github.com/digitaldemocracy2030/kouchou-ai/issues/809)）

## 関連

- [[issue-backlog-audit-2026-10-28]] — 判定一覧とスプリント提案
- [[issue-backlog-audit-2026-10-12]] — 前回の全件棚卸し（superseded）
- [[meeting-report-draft]] — 定例向けの要点
