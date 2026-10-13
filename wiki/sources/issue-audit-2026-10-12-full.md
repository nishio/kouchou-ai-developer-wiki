---
type: source
summary: "広聴AI open Issue 全105件のうち今回95件を 2026-10-12 に 10シャード並列で current main@c297bc97 へコード照合した全棚卸しの一次記録。観測日時・基準commit・実行検証・未確認範囲。判定一覧と次の一手は [[issue-backlog-audit-2026-10-12]]。"
last_checked: 2026-10-12 JST
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues
  - source-code.md
  - issue-audit-2026-10-11-batch1.md
  - issue-backlog-audit-2026-10-11.md
---

## What it is

digitaldemocracy2030/kouchou-ai の open Issue 全棚卸し（2026-10-12）の根拠 source。open Issue 総数は **105 件**。このうち **95 件**を今回 10 シャードの read-only 並列調査で現行 main に要件別照合した。残る 10 件（[#11](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11) [#44](https://github.com/digitaldemocracy2030/kouchou-ai/issues/44) [#52](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52) [#55](https://github.com/digitaldemocracy2030/kouchou-ai/issues/55) [#56](https://github.com/digitaldemocracy2030/kouchou-ai/issues/56) [#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60) [#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79) [#104](https://github.com/digitaldemocracy2030/kouchou-ai/issues/104) [#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121) [#143](https://github.com/digitaldemocracy2030/kouchou-ai/issues/143)）は 2026-10-11 調査済みで [[issue-audit-2026-10-11-batch1]] / [[issue-backlog-audit-2026-10-11]] を再利用する。判定一覧・集計・次の一手は [[issue-backlog-audit-2026-10-12]]。

## Freshness marker

- 基準コード: `work/kouchou-ai` の current main `c297bc97bb2bbce42964a90d7501c2d3592aeaf0`（観測日 2026-10-12）。commit 固定のコードリンクは `https://github.com/digitaldemocracy2030/kouchou-ai/blob/c297bc97bb2bbce42964a90d7501c2d3592aeaf0/<path>#L<line>` で解決する。
- 公開 GitHub: 各 Issue の本文・コメント・担当・ラベル・関連 PR を観測。今回分の生データ（Issue 1 件 = 1 JSON、シャード毎の判定 = `results.json`）は `raw/issue-audit/2026-10-12-full/shard-0 … shard-9/` に固定（`raw/` は gitignored なので local/private な一次置き場）。
- 対象 95 件の Issue 番号: 170, 172, 173, 176, 186, 190, 211, 213, 221, 227, 236, 250, 255, 266, 280, 285, 289, 292, 293, 295, 306, 308, 310, 323, 324, 337, 339, 342, 345, 346, 364, 366, 370, 374, 395, 417, 445, 450, 454, 464, 470, 471, 474, 493, 496, 503, 507, 513, 515, 516, 517, 518, 519, 529, 537, 542, 546, 547, 548, 556, 558, 564, 573, 576, 577, 586, 592, 638, 641, 643, 648, 669, 679, 809, 869, 871, 876, 879, 880, 881, 882, 885, 898, 912, 913, 921, 949, 953, 954, 956, 960, 962, 964, 971, 972。
- 再利用 10 件: [#11](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11) [#44](https://github.com/digitaldemocracy2030/kouchou-ai/issues/44) [#52](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52) [#55](https://github.com/digitaldemocracy2030/kouchou-ai/issues/55) [#56](https://github.com/digitaldemocracy2030/kouchou-ai/issues/56) [#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60) [#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79) [#104](https://github.com/digitaldemocracy2030/kouchou-ai/issues/104) [#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121) [#143](https://github.com/digitaldemocracy2030/kouchou-ai/issues/143)（2026-10-11 観測、同一 main）。

## 実行した検証

- 各 Issue について、公開 Issue 本文・全コメント・担当・関連 PR を読み、依頼された要件を分解。
- 現行 main のコードに対し、要件ごとに `grep` / ファイル読解で実装の有無を file:line で確認（例: [#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176) は `grep 'analysis_mode'` が apps/admin・apps/api/src で 0 件、engine 側 `steps/llm_grouping.py` は実装・テスト済）。
- 判定は 5 区分: 未解決 / 一部解決 / 要件再確認 / 解決済(close候補) / 不明。各判定に confidence（high/medium/low）を付与。
- close 検証: 解決済み/不明と判定した件を再確認し、main の file:line 完了条件を満たし人手の確認が不要なもののみ close 対象とした。**今回の close 対象は 0 件**（verdict 上書きなし）。

## 未確認範囲

- 実 LLM / 実 API 課金を伴う挙動（[#912](https://github.com/digitaldemocracy2030/kouchou-ai/issues/912) GPT-5.6 実 API 検証、[#573](https://github.com/digitaldemocracy2030/kouchou-ai/issues/573) GPU/大規模再評価 など）は未実施。
- アプリ起動による視覚再現（[#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121) 縦長散布図の歪み重症度、[#227](https://github.com/digitaldemocracy2030/kouchou-ai/issues/227) 濃いグループ設定ダイアログの実表示、[#898](https://github.com/digitaldemocracy2030/kouchou-ai/issues/898) Apple Silicon 実機クラッシュ再現）は未実施。
- 外部 repo で進む実験（[#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324) masatosasano2、[#346](https://github.com/digitaldemocracy2030/kouchou-ai/issues/346) nasuka、[#370](https://github.com/digitaldemocracy2030/kouchou-ai/issues/370) nishio 等）の現況・結論は本体 repo から検証不能。担当への確認が必要。
- repo 外成果の公開状況（[#519](https://github.com/digitaldemocracy2030/kouchou-ai/issues/519) エネルギー庁パブコメ分析レポート）は検証不能。
- 関連 PR 番号は本調査で照合しきれていない件がある（「本調査では未特定」と明記した件）。

## 関連

- 判定一覧・集計・重要な判断・Open Questions: [[issue-backlog-audit-2026-10-12]]
- 前回 10 件の根拠: [[issue-audit-2026-10-11-batch1]] / [[issue-backlog-audit-2026-10-11]]
- 2026-09-09 の GitHub 反映を伴う棚卸し: [[issue-backlog-audit-2026-09-09]]
