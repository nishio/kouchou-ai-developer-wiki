---
title: "スプリント第 1 群 4 件の実装 PR と判断点 2026-10-29"
type: analysis
summary: "10-28 棚卸しの第 1 群 5 件のうち 4 件（#79 費用概算、#292 課金と 429 の docs、#493 散布図ホイール、#1130 接続チェックのエラー詳細）を PR #1161〜#1164 にした。#1128 は別作業の #1154 で本体修正済み。各 PR で AI が置いた仮定と、人間に確かめてほしい点を記録する"
sources:
  - issue-audit-2026-10-28-sprint.md
---

[[issue-backlog-audit-2026-10-28]] で「先にやる」とした第 1 群 5 件に、2026-10-29 に着手した。nishio の指示は「第 1 群の 5 件から着手して PR を作る」。着手前に 4 件を nishio の assignee にし、issue ごとに `work/kouchou-ai-issue-<n>` の worktree で並行実装した。GitHub への書き込みは assign と PR 作成のみで、Issue のコメント・close・label・reviewer 指定はしていない。

## 結果

| Issue | PR | 種別 | Issue との関係 | CI（作成時） |
|---|---|---|---|---|
| [#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292) 課金と 429 の docs | [#1161](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1161) | docs のみ（11 ファイル） | Refs（画面からの docs 導線 1 項目が残る） | green。CodeRabbit 指摘 5 件は 2 commit 目で反映 |
| [#493](https://github.com/digitaldemocracy2030/kouchou-ai/issues/493) 散布図ホイール誤操作 | [#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162) | public-viewer（5 ファイル） | Refs（操作感は人間がデモ環境で判断） | green |
| [#1130](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1130) 接続チェックのエラー詳細 | [#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163) | api + admin（7 ファイル） | Closes | green |
| [#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79) 作成前の費用概算 | [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) | admin + カタログ（10 ファイル） | Refs（係数の較正が要る） | e2e が旧文言「費用：目安なし」を期待して失敗 → 期待値を更新して再実行 |
| [#1128](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1128) 再試行のトークン数 | [#1154](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1154)（merge 済み） | 別セッションが 10-29 朝に対応 | 「関連して残っている点」2 つは未着手 | — |

**merge 順の注意**: [#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163) と [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) は `CreateReportConfirmation.tsx` とそのテストを両方とも触る（前者はエラー表示、後者は費用欄）。どちらも main には merge 可能だが、片方を merge した後にもう片方は rebase が要る。

## 各 PR で置いた仮定と、人間に確かめてほしい点

### [#1161](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1161) 課金と 429（docs）

- 置き場は `docs/self-hosting/api-billing-and-rate-limits.md` の独立ページ。FAQ の 1 項目には長すぎた（課金／429 の 2 種類／自動調整／Tier）。入口がセットアップガイドの「APIキーの準備」なので self-hosting 側に置いた。user-guide が良ければ nav とリンク 7 箇所の置換で移せる
- [#1152](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1152) の自動調整は、`insufficient_quota` を対象外にしている（`rate_limit.py` の非一時的コード）ことをコードで確認して書いた。v4.2.0 以前のリリースには自動調整が入っていないと注記したので、次のリリース後に「vX.Y.Z 以降」へ書き換えが要る
- CodeRabbit の指摘 5 件はすべて妥当で、2 commit 目で反映した。埋め込み要求は自動調整の対象外（`request_to_embed` は `call_with_rate_limit` を通らず、OpenAI SDK の短い再試行のみ）、並列数は失敗した工程の `workers`（抽出・意見分類・初期ラベル・統合ラベル・LLM grouping の 5 つ。管理画面の「並列実行数」はまとめて適用）を下げる、プリペイド課金は新規アカウントの通常形で月次請求や無料クレジットの例外がある、`insufficient_quota` は usage limit 到達でも出るので残高と上限の両方を確認、と書き分けた
- docs は日本語版のみで運用されているので新ページも日本語のみ。README の英語・韓国語版には既存の慣例どおり「(Japanese)」目印つきでリンクした
- 残件は「作成前確認・接続確認のメッセージから docs へリンク」の 1 項目。[#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163) と同じコンポーネントなので、merge 後の後続 PR にした

### [#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162) 散布図のホイール誤操作

- 仕様は Issue の最終合意（dentaro 案、UtkNggc 承認 2025-06-13）どおり。白いオーバーレイ、フェード 500ms、ホイール停止から 600ms で解除、カーソル切替、click-to-enable は不採用（[[chart-scroll-ux-decision]]）
- 実装は Plotly の `scrollZoom` を切り替えて再描画する方式ではなく、ラッパー要素の capture 段階で wheel の伝播を止める方式。Plotly 4.1.1 は内部の dragger 要素で wheel を受けて `preventDefault()` するので、手前で止めればページは通常どおりスクロールする
- AI が独自に足した判断: ctrl キー付き wheel（トラックパッドのピンチ）はロック中でも通す。不要なら 1 行で戻せる。全画面では常に有効。タッチ操作は変更なし
- 案内文「スクロール中は拡大・縮小しません（止めると有効になります）」と `not-allowed` カーソルはデザイン側の確認が要る。既存のヒント tooltip（[#986](https://github.com/digitaldemocracy2030/kouchou-ai/pull/986)）にも一言足した
- 実ブラウザでは未確認。PR 本文に 10 項目の確認手順を書いた。ページがスクロールして図がカーソルの下から外れた時の再ロックは、ブラウザがスクロール後に mouseleave を発火することに依存している

### [#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163) 接続チェックのエラー詳細

- 詳細を付けるのは `unknown_error` の時だけ。認証・残高・レート制限の分類済みエラーは「挙動を変えない」完了条件を優先し `error_detail` を `null` にした。分類済みにも詳細を添えるかはレビューの論点
- 詳細の材料は SDK 例外の文字列ではなく、応答本文の `code` / `message` と HTTP status のみ。OpenAI SDK の `APIStatusError`（OpenAI / Azure / OpenRouter / local）と google-genai の `APIError`（Gemini）に対応。応答のない失敗（接続エラー・timeout）は接続先アドレスを含みうるので従来どおり詳細なし。`redact_secrets` を通し 300 文字で切る
- Azure の応答メッセージにはデプロイ名が含まれることがある。管理画面専用なので許容したが、レビューで判断してもらう
- テストは pinned SDK（openai 1.77.0 / google-genai 1.62.0）の実例外クラスを組み立てて行った（[[source-review-findings-2026-10-16]] で mock の形が実 SDK と違って Gemini 埋め込みの全断を見逃した教訓どおり）

### [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) 作成前の費用概算

- 表示は「円の帯（100 円未満 / 100〜1,000 円 / 1,000 円以上）」と内訳の一行（チャット $x〜$y、埋め込み $z または単価不明・課金なし）と「目安であり実料金の保証ではない」の注記。チャット単価が不明なら帯を出さない（0 円にしない）。埋め込みだけ不明なら帯はチャット分で決め、不明がある目印を立てる
- 係数は analysis-core の実装と aipubcom の実データから置いた。1 文字 0.7〜1.5 トークン、抽出出力はコメント文字数の 0.3 倍 + 40、意見 1 件 50 文字、ラベル生成サンプル 30 件／クラスタなど。帯は幅の high 側を 1 ドル 150 円で換算して決める（安く見せない）
- 桁の確認: aipubcom 実測 $0.87 に対し本実装 $0.71〜$1.46。Serverless の `estimate.ts` は $1.18 で桁は一致（Serverless は長文で抽出出力と埋め込みを約 2 倍多く見積もる）
- カタログ `model_catalog.json` に `text-embedding-3-small` / `-large` の単価を足した（無いと埋め込みは常に単価不明になる）。Gemini 埋め込みと OpenRouter の未登録モデルは単価不明のまま
- e2e（`create-report.spec.ts`）が旧プレースホルダ「費用：目安なし」を期待して落ちた。実装は仕様どおりなので e2e の期待値を「100円未満の見込み」と内訳・注記の表示に更新した。ダミーサーバーは本体の `model_catalog.json` をそのまま返すので、fixture 3 件では 100 円未満の帯が出る
- 人間に較正してほしい点: 1 ドル 150 円の固定換算、high 側で帯を決める方針、抽出出力係数（パブコメ型の長文が根拠で短い自由記述では未検証）、手元の実レポートの `estimated_cost` と幅の桁が合うか、`embedding_model` 未指定時の表示名

### [#1128](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1128) は着手しなかった

別セッションが 10-29 朝に [#1154](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1154) で本体（OpenAI・Azure の parse 経路で弾かれた応答の usage 集計）を merge 済みだった。Issue に残る「JSON の形で返る拒否の扱い」「finish_reason を専用の例外にする」は別の改善なので、重複を避けて今回は触っていない。

## Open Questions

- [#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163) と [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) のどちらを先に merge するか（後の方を rebase する）
- [#1162](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1162) の操作感（600ms、文言、カーソル）をデモ環境で誰が確認するか。UtkNggc のデザイン確認を頼むか
- [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) の係数を実レポートで較正する手順。CLI で数件回して `estimated_cost` と比べるのが早い
- [#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292) の残件（画面から docs へのリンク）をいつ出すか。[#1163](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1163) の merge 後

## Updates

- 2026-10-29: 初版。4 PR 作成直後の状態
- 2026-10-29: [#1161](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1161) の CodeRabbit 指摘 5 件を反映、[#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) の e2e 失敗（旧文言の期待値）を修正。並行 agent が scratchpad の同名ファイル `pr-body.md` を上書きし、[#1161](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1161) の本文が一時的に [#1164](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1164) の本文になる事故があった（直後に復旧）。並行 PR 作成では PR 番号入りの一意なファイル名を使う
