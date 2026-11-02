---
title: "open PR 8 本の状態と merge 前の残作業 2026-11-02"
type: analysis
summary: "2026-11-02 時点の kouchou-ai の open PR 8 本（#1161〜#1167、#1174）を GitHub の live state で確認した。全件 CI green・人間コメントなし。wiki の 10-29 記録との差は、#1165 に CodeRabbit の Minor 5 件が未対応で残っていることと、#1162 が #1155 の merge で衝突していることの 2 点"
sources:
  - source-code.md
---

nishio の「現状の PR はどうなってる？」に答えるため、2026-11-02 15:10（JST）に GitHub の open PR・CI・レビュースレッド・main との差分を観測した。観測時の main は `d2702d48`（10-30 の事例 docs [#1175](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1175) まで）。open PR は 8 本で、すべて 10-28〜10-29 に AI が nishio 名義で作ったもの（[[sprint-group1-prs-2026-10-29]]、[[post-review-direction-issues-2026-10-29]]）。他の人の PR と Dependabot の PR は無い。

## 結果

| PR | 内容（Issue） | CI | merge 可否 | 残作業 |
|---|---|---|---|---|
| [#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) | 賛否・新規性スコアの属性ステップ（[#1158](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1158)） | green | 可 | CodeRabbit の Minor 5 件が未対応 |
| [#1166](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1166) | 階層リストの詳細モード化（[#1159](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1159)） | green | 可 | なし |
| [#1167](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1167) | ビューの選び方ギャラリー docs（[#1160](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1160)） | green | 可 | なし |
| [#1174](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1174) | 関連研究の紹介 docs（[#1173](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1173)） | green | 可 | tokoroten さんへの確認（人間） |
| [#1161](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1161) | OpenAI の課金と 429 の docs（[#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292)） | green | 可 | なし（指摘 5 件は 10-29 に対応済み） |
| [#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162) | 散布図の上でのスクロール拡縮を止める（[#493](https://github.com/digitaldemocracy2030/kouchou-ai/issues/493)） | green | **衝突** | main への rebase |
| [#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163) | API 接続チェックのエラー詳細（[#1130](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1130)） | green | 可 | なし |
| [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) | 作成前確認に API 利用料の目安（[#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79)） | green | 可 | なし |

- 8 本とも branch protection でレビュー必須（`REVIEW_REQUIRED`）のため、これまでと同じく nishio の手元での admin merge が要る。Claude Code からの admin merge は権限判定で止まる（10-29 の [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155) と同じ）
- 人間のコメント・レビューは 8 本とも付いていない。付いているのは CodeRabbit の要約と、CI の how-to-use リマインダー（[#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163)・[#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164)。利用ガイド未更新の注意で、merge は止めない）だけ
- main からの遅れは 1〜5 commit。衝突しているのは [#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162) だけで、ほかは GitHub 上で merge 可能と判定されている

## wiki の 10-29 記録と違う点

### [#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) は「merge 待ち」のまま止まり、その後に指摘が付いた

10-29 15:10 の記録は「rebase と CodeQL 修正を push、CI green で nishio の merge 待ち」で終わっている。その push（`d86f56da`、06:46 UTC）の 12 分後に CodeRabbit が Minor 5 件をレビュースレッドとして付けていて、11-02 時点で 5 件とも未解決・未対応のまま。内訳は次のとおり。

1. **docs の項目説明の誤り**（`docs/development/plugin-output-data-structures.md`）: 賛否と新規性の summary ファイルの両方に「分布」と「計算方法」があると書いているが、実際は賛否側に `distribution` だけ、新規性側に `method` と `raw_value` だけ。docs 側を直す。軽い
2. **score ステップを無効化して再実行したとき集計が再実行されない**（`core/orchestration.py`）: 一度有効で走らせた後に無効にして `-f` なしで再実行すると、集計がスキップされ、`hierarchical_result.json` に古い `stance_score` / `novelty_score` 属性が残り、ビューアのフィルタにも出続ける。planner が「無効化された opt-in 依存に過去の完了がある」場合は集計を再実行する必要がある。CodeRabbit 自身が「heavy lift」と分類
3. **入力属性が生成 score で上書きされる**（`steps/hierarchical_aggregation.py`）: 入力 CSV に `attribute_stance_score` 列があると `stance_score` キーに入るが、ステップを有効にすると生成 score が同じキーに書き込まれて入力値が消える（新規性も同じ）。キー名を変える／既存キーがあれば merge しない／エラーにする、のどれにするかは「フィルタに出すべきは生成値か入力値か」の設計判断。CodeRabbit も修正案を出していない
4. **新規性の `k` / `seed` の変換前に古い出力を消す**（`steps/opinion_novelty.py`）: 非数値を渡すと変換で落ち、古い `opinion_novelty.csv` が残る。その後 `run: false` で新規性を飛ばしつつ enabled のままにすると古い CSV が集計に混ざる。削除処理を変換より前に動かす。軽い
5. **賛否の target 検証前に古い出力を消す**（`steps/opinion_stance.py`）: `target` と `question` が両方空だと検証で落ちて古い `opinion_stances.csv` が残り、集計だけの再実行で混ざる。4 と同じ形。軽い

1・4・5 は小さい修正で済む。2 は planner の変更、3 は設計判断が要る。2 と 3 は「既定無効の任意ステップ」の初版としては後追いでもよいが、merge 前に直すなら 2 が一番重い。

### [#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162) は [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155) の merge で衝突した

衝突しているのは public-viewer の翻訳ファイル `apps/public-viewer/lib/i18n/messages.ts` の 1 本だけ。[#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155)（元コメント表示）と [#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162)（スクロール時のオーバーレイ文言）がどちらも文言を足したため。散布図の実装側（`ScatterChart.tsx` と plugin）と利用ガイドは自動 merge できている。rebase は両方の文言を残すだけで済む見込み。

## 注意点

- [#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163) と [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) は同じ作成前確認コンポーネント（`CreateReportConfirmation`）を触る。片方を merge したらもう片方は rebase が要る（10-29 の記録どおり）
- [#1167](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1167) のギャラリーに属性つきの例を足す作業は [#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) の merge 後に行う予定で、merge 順は [#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) → [#1166](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1166) → [#1167](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1167) のまま
- [#1174](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1174) は tokoroten さんへの説明と位置づけの確認が先で、AI 側の残作業は無い（[[open-decisions]] A14）

## 次に見るもの

- nishio が決める: [#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) の指摘 5 件を直してから merge するか、先に merge して後追いにするか。直すなら 1・4・5 はすぐ、2 は planner の変更、3 は設計判断つき
- AI 側で進められる: [#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162) の rebase、[#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) の軽い 3 件の修正
- 人間判断が先: [#1174](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1174) の tokoroten さん確認、[#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162) の操作感と [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) の費用係数の較正（[[sprint-group1-prs-2026-10-29]]）

## Open Questions

- [#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) の指摘 3（入力属性と生成 score の衝突）は、属性フィルタに出すべきは入力値か生成値か。生成値を優先するなら入力値を別キーで残すのが自然だが、入力に同名列を持ち込む運用が実際にあるかは未確認
- [#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) の指摘 2（無効化後の再実行で古い属性が残る）は、既存の「opt-in ステップを後から無効にする」一般的な問題として planner 側で扱うのか、score ステップだけの個別対応にするのか

## Updates

- 2026-11-02: 初版。GitHub の live state を 15:10（JST）に観測
