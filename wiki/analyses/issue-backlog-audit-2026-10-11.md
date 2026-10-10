---
type: analysis
summary: "古い順 open Issue 先頭10件を current main@c297bc97 に照合した棚卸し。未解決5 (#11/#44/#60/#79/#121)、一部解決3 (#52/#55/#143)、要件再確認1 (#104)。#52 は階層図連動が PR #927 で main 反映済み、#55 は viewer 読込済みだが admin 編集 UI 欠落、#11/#79 は作成前確認パネルに費用/時間欄枠はあるが『目安なし』固定"
sources:
  - issue-audit-2026-10-11-batch1.md
  - issue-backlog-audit-2026-09-09.md
  - current-open-issue-triage-2026-06-01.md
  - issue-884-pre-create-review-contract-2026-06-30.md
  - analysis-stance.md
  - serverless-product-direction-2026-09-08.md
---

## 観測範囲

2026-10-11 00:30 JST。`kouchou-issue-audit-queue` 経由の依頼 I1「古い未解決 Issue の先頭 10 件を調査し developer-wiki に記録」に基づく。目的は Issue を減らすことではなく、**現行実装で満たした要件と残件を区別し、次に利用者の問題を解決する一手を明確化する**こと。

対象は open Issue を `createdAt` 昇順に並べた先頭 10 件: #11, #44, #52, #55, #56, #60, #79, #104, #121, #143。本体は `work/kouchou-ai` の current main `c297bc97bb2bbce42964a90d7501c2d3592aeaf0`（00:30 JST に fetch / pull --ff-only）を一次根拠に、公開 Issue 本文・全コメント・関連 PR・現行コードまで確認した。要件別の file:line 根拠と freshness marker は [[issue-audit-2026-10-11-batch1]]。

この 10 件の多くは [[issue-backlog-audit-2026-09-09]] が 2026-09-08〜09 に本文へ「現状と残作業」を追記済み。本棚卸しは、その後 merge された PR（特に #52 の #927）を反映しつつ current main を確認し直したもの。過去 note を証拠にせず、コードで判定した。全件の動作確認（アプリ起動・実 LLM・実 API 課金）はしていない。上流 Issue の更新・コメント・close・assign・実装・merge はこの調査の範囲外。

## 判定一覧

| # | 題名 | 担当 | 判定 | 満たした範囲 | 残件 | 関連PR | 次の一手 | 確度 |
|---|---|---|---|---|---|---|---|---|
| 11 | レポート出力時間の目安 | nishio | 未解決 | 作成前確認パネルに「時間」表示枠 (#922); per-step duration は status.json に記録 | 入力件数/モデルからの時間推定と表示 (現在 `時間：目安なし` 固定) | #922(merged), #884 umbrella | 推定関数→`CreateReportConfirmation.tsx:143` に接続。粗い帯でよい | 高 |
| 44 | クラスタ固有タイトル | - | 未解決 | なし (抽象語回避を促す弱い prompt nudge のみ) | 近傍クラスタの contrast 情報を label prompt に注入 / タイトル重複検出 | - | initial/merge labelling に近傍 sample を追加する実験 | 高 |
| 52 | チャート連動文章 | - | 一部解決 | 階層図(treemap)連動を実装・テスト済 (PR #927 merged): 現在位置/戻る/属性絞込件数/0件表示 | 散布図のクラスタ選択連動は未実装; 散布図リストは属性絞込件数未反映 | #927(merged, #528経由) | ClientContainer に選択 state を追加し ScatterChart click と連動 | 高 |
| 55 | 濃いクラスタ閾値のレポート別デフォルト | nishio | 一部解決 | viewer 読込済; schema+API は保存可能 | admin 編集 UI (閾値入力欄) が欠落 | #946(open, 未反映) | dialog に maxDensity/minValue 入力追加 (API/viewer は既に E2E 対応) | 高 |
| 56 | 元コメント表示 | -(※) | 未解決 | 下地のみ: comment_id リンク, 死蔵 `_build_comments_value`(権限フィルタ付), pubcom CSV(admin専用) | 公開 JSON に comments 未出力(コメントアウト); viewer UI 無; per-comment 再頒布可否フラグ無 | - | 権限フラグ設計→`_build_comments_value` 有効化→viewer opt-in toggle | 中〜高 |
| 60 | 階層図最下層を濃いクラスタに絞る | - | 未解決 | `getDenseClusters` は散布図 density mode のみ | treemap には未適用、default-on toggle も無 (R1/R2/R3 未達) | #961 は別機能 | ClientContainer に default-on toggle、treemap に `getDenseClusters` 適用 | 高 |
| 79 | CSVコスト表示 | - | 未解決 | 作成前確認パネルに「費用」枠+文章警告 (#922); 価格 infra と単価 fetch は済(事後計算のみ) | 処理前コスト推定(トークン量×単価→帯)と表示 (現在 `費用：目安なし` 固定) | #922/#926(merged), #884 umbrella | 推定 helper→`CreateReportConfirmation.tsx:142`。埋め込み分は別扱い | 高 |
| 104 | 利用状況把握 | - | 要件再確認が必要 | GA4 は per-deployment(各運用者の ID)で導入済 | プロジェクト横断の集約 visibility 無; report-gen イベント無; opt-out/consent 無; 方針未合意 | - | まず収集項目/opt-in 既定/説明を人間が決定。実装は方針合意後 | 高 |
| 121 | 縦長画面の散布図[BUG] | - | 未解決 | ≤600px でデフォルト表示を hierarchyList に切替(回避) | アスペクト比 1:1 lock 無 (scaleanchor 無); 縦長時の散布図対応無 | - | yaxis に scaleanchor/scaleratio (縦長で余白/可読性 tradeoff)。要 runtime 確認 | 中 |
| 143 | クラスタ品質自動評価 | - | 一部解決 | 独立評価スクリプト `experiments/evaluation_report/` あり (silhouette + LLM-judge rubric, CSV/HTML) | 同梱データセット/harness 無; 検証結果未コミット; プロダクト統合無(意図的に後段) | - | `experiments/evaluation_report/inputs/` に例データ+結果ノートをコミットし再現可能に | 中〜高 |

※ #56 は assignee 欄は空だが ei-blue が 2025-03-25 に `/assign`（#105 と共に）宣言。GitHub 欄には未反映で、進行中作業は観測されない。

集計: 未解決 5（#11 / #44 / #60 / #79 / #121）、一部解決 3（#52 / #55 / #143）、要件再確認が必要 1（#104）。「不明」はなし。重複・統合の新規特定はなし（#56 は #250、#11/#79 は #884 と既存の束ね関係を継承）。

## 重要な判断

### 「似た機能がある」と「要件が満たされた」を混同しない
- **#55**: viewer が閾値を読むこと（閲覧側）と、出力者が閾値を保存できること（管理側編集）は別経路。viewer 読込が動いても #55 の主眼（出力者が結果を見てデフォルトを設定）は満たされない。admin dialog に入力欄が無いため「一部解決」に留める。schema/API は対応済みなので残作業は UI 接続に閉じる。
- **#60**: 散布図の濃いクラスタ filter があることは、階層図最下層を絞る要件を満たさない。density gate が `scatterDensity` 限定である点がコード上明確。
- **#52**: 階層図の連動（issue が難所と指摘した plotly 内部 logic 側）は PR #927 で解決。散布図側のクラスタ選択連動は別経路として未達。
- **#79 / #11**: 作成前確認パネルが merge されたこと（PR #922）＝費用/時間の目安が出ること、ではない。両欄とも `目安なし` の固定文字列で、推定ロジックは存在しない。

### チャット/埋め込み・公開/再分析など、違う利用経路を分ける
- **#79**: モデル選択（チャット）とコスト見積もりは接続可能だが、埋め込みモデルは独立選択 UI が無く（サーバ内処理 on/off のみ）、埋め込み費用は別扱い。
- **#56**: 公開 viewer JSON への原文自動追加は現状していない。pubcom 向け admin CSV（`is_pubcom`）と公開出力は別契約。per-comment 再頒布可否フラグが schema に無いことが設計上の起点。[[analysis-stance]]（構造把握の道具であり件数=世論ではない）に照らしても、原文表示は「要約から元の声へ戻る」契約として設計する。

### 方針未決を既決としない
- **#104**: GA4 は各運用者のデプロイ単位で動くだけで、プロジェクト横断の利用把握という issue の主眼は満たさない。Slack 議論でオプトアウト・同意・自治体温度感が未決のため「要件再確認が必要」とし、実装は方針合意後とする。
- **#143**: 評価スクリプトは存在するが、プロダクト統合は issue 自身が後段としており、既決の実装方針にしない。まず再現可能な検証（データセット同梱）を揃える段階。

## 次に前進させる利用者の行動

[[issue-backlog-audit-2026-09-09]] / [[serverless-product-direction-2026-09-08]] の重点（導入経路・費用時間・元の声への参照）を current main で裏取りした結果、近い一手は次。

1. **分析を始める判断ができる — #79 / #11**。価格 infra・単価 fetch・per-step duration は既に揃っているので、[[issue-884-pre-create-review-contract-2026-06-30]] の first PR scope で「粗い費用帯 / 時間帯」を `CreateReportConfirmation.tsx` の既存枠に入れる。精密 ETA・精密請求額は後続 slice。
2. **閲覧の操作が破綻しない — #52 散布図連動 / #55 admin 閾値 / #60 treemap 絞り込み / #121 縦長**。いずれも残作業が public-viewer / admin の局所修正に閉じており、schema/API 側の前提は揃っている。#121 は視覚再現での重症度確認を先に。
3. **元の声を確かめて対話へ渡す — #56**。per-comment 再頒布可否フラグの設計（公開用と再分析用の分離）が先で、その後 `_build_comments_value` 有効化と viewer opt-in。

## Open Questions

- #11 / #79 の「粗い帯」を #884 first PR に含めるか、後続 slice にするか（[[issue-884-pre-create-review-contract-2026-06-30]] は first PR scope 外に置いていた）。
- #104 の収集項目・opt-out 既定・説明文を、どの利用観測で決めるか（人間判断）。
- #56 の per-comment 再頒布可否フラグを入力 schema に持たせるか。
- #121 の 1:1 lock と縦長の余白/可読性 tradeoff をどう両立するか。
- 次 batch 候補（古い順の続き）: #170, #172, #173, #176, #186。本依頼は自動着手しない。

## Updates

- 2026-10-11 00:55 JST: 初版。5 つの read-only subagent で 10 件をコード照合し、分類に効く主張（費用/時間 placeholder、`comments: {}` のコメントアウト、散布図の scaleanchor 不在）を spot-grep で再確認。snapshot は `raw/issue-audit/2026-10-11-batch1/` と private キュー `drafts/issue-audit/2026-10-11-batch1/`。日本語 Issue 更新案と checkpoint も同キューに保存。
