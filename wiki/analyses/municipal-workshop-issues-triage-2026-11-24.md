---
title: 自治体の研究会で出た要望 14 件の振り分け 2026-11-24
type: analysis
summary: "大木さんが自治体の研究会から起こした Issue #1203〜#1216 を、2026-11-24 の main と照らし合わせて振り分けた。閲覧画面の 4 件（一括展開・検索で一致した枝を開く・件数の単位・散布図の見方）は PR #1221〜#1224 に。管理画面の「再利用」は入力データも引き継ぐため新しいデータにプロンプトを当てる手段は無い、意見ごとのラベル付けは決められた 2 種類だけで利用者定義のラベルが無い、という 2 つの穴が見つかった。会議の分析の 5 件は本体の外の試作を先にする案"
sources:
  - slack-municipal-workshop-issues-2026-11-18.md
  - source-code.md
---

# 自治体の研究会で出た要望 14 件の振り分け 2026-11-24

対象: kouchou-ai main `2a924af6`（2026-11-24、[#1220](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1220) merge 後）。Issue の経緯は [[slack-municipal-workshop-issues-2026-11-18]]より。どの Issue も本文に「最新の実装と照合する」と書かれていたので、本体のコードを読んで、すでにある機能・足りない機能・すぐ直せる範囲を分けた。各 Issue には 11-24 にコメントとラベルを付けた。

## 振り分けの結果

| Issue | main の状況 | 扱い |
|---|---|---|
| [#1206](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1206) リストを一括展開 | 階層リストはグループを 1 つずつ開く操作だけ | PR [#1221](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1221)「すべて開く／すべて閉じる」 |
| [#1205](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1205) 意見を検索して該当箇所へ | テキスト検索（[#560](https://github.com/digitaldemocracy2030/kouchou-ai/issues/560)）はフィルタのダイアログの中。リストでは自分で開かないと意見に届かず、一致した意見が 11 件目以降だと「さらに表示」の奥 | PR [#1222](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1222)：検索中は一致した枝を最下層まで開き、一致した意見を先頭に。検索欄を表に出すかは残件 |
| [#1211](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1211) 意見数と回答者数の違い | 冒頭にコメント数と抽出した意見数、読み方ガイドに注意書きはあるが、グループの件数は「3件」だけ。「子要素を表示 (3件)」の 3 は子グループの数 | PR [#1223](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1223)：「意見 3件」「(3グループ)」、ツールチップに人数と一致しない旨。回答者数は [#1156](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1156) と関わるので残件 |
| [#1212](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1212) 散布図の読み方 | 散布図の「?」は操作方法だけ | PR [#1224](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1224)：「散布図の見方」（点＝意見 1 件、軸そのものに意味はない、点の多さは重要度ではない、輪郭の重なり）。11-10 の Slack の輪郭の重なりもここで扱った。説明に気づけるかは残件 |
| [#1207](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1207) グループから個別の意見へ | 散布図の点クリックは下の説明文へ連動（[#52](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52)）するが、意見の一覧へは移れない | [#1221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1221) の後に「このグループの意見をリストで見る」を作る案。どの画面の話かを大木さんに確認中 |
| [#1203](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1203) プロンプトの保存と再利用 | 下の「見つかった穴」1 | (a) 新規作成で既存レポートのプロンプトを読み込む、(b) 名前つきで保存、の 2 案を提示 |
| [#1210](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1210) 課題と解決策を分ける | 指定カテゴリ分類（[#994](https://github.com/digitaldemocracy2030/kouchou-ai/issues/994)、CLI）で「課題」「解決策」を枠にできる。ただし通常の分析の代わりになる | 設定例を返した。残件は下の「見つかった穴」2 |
| [#1213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1213) 件数の少ない大事な意見 | 新規性スコア（[#1158](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1158)、CLI、LLM 不要）を属性フィルタで絞れる | 設定例を返した。残件は「見つかった穴」2 |
| [#1204](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1204) 音声から作る | 文字起こし機能は無い | まず文字起こし済みテキストを入力 CSV にする手順を docs に、次にローカルの文字起こしを CLI の前処理に（国内完結の [#1190](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1190) と合う） |
| [#1208](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1208)・[#1209](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1209) 会議データの分け方・抽出 | 抽出のプロンプトは変えられる。話者の列を属性にすれば見るときに絞れる | 公開できる会議データが要る。大木さんにサンプルの有無を確認中。ラベル側は [#882](https://github.com/digitaldemocracy2030/kouchou-ai/issues/882) と同じ比べ方 |
| [#1214](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1214)〜[#1216](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1216) 会議の時系列・横断・評価 | 時系列は本体の外で試作済み（11-19） | 本体の外の試作を先にし、[#1215](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1215)・[#1216](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1216) はその上に載せる順番の案 |

## 見つかった穴

1. **新しいデータに調整済みのプロンプトを当てる手段が無い。** 管理画面の「再利用」（[#19](https://github.com/digitaldemocracy2030/kouchou-ai/issues/19)）はプロンプトを含む設定を引き継ぐが、入力データも再利用元のものを使う（`apps/admin/app/reuse/[slug]/page.tsx`、画面に「入力データは再利用元から引き継がれます」）。同じデータを設定を変えて作り直すための機能で、[#1203](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1203) の要望（新しいデータで再利用）には当たらない。最初は「再利用で足りるのでは」と書きかけ、コードを読み直して取り消した
2. **意見ごとのラベルを利用者が定義できない。** `opinion_classification`（[#971](https://github.com/digitaldemocracy2030/kouchou-ai/issues/971)）は `labels` で選べるのが既定の 2 種類（侮辱・ヘイト表現／政策提案）の ID だけ（`steps/opinion_classification.py` の `DEFAULT_LABEL_IDS`）。「安全上の指摘か」（[#1213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1213)）、「課題か・解決策か」（[#1210](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1210)）を、通常の分析を残したまま属性フィルタで見るには、利用者がラベルと定義を渡せるようにする必要がある。指定カテゴリ分類は分析の方式そのものを置き換えるので、別レポートになる

## 4 本の PR の関係

- [#1221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1221) と [#1222](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1222) は `HierarchyListChart.tsx` の同じあたり（import 行・補助関数の位置）を触るので、どちらかが先に入ったらもう一方を rebase する。[#1223](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1223)・[#1224](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1224) は他の 3 本と衝突しない（docs の追記位置をずらして確認済み）
- 開発用の確認画面（`apps/public-viewer` の `/dev/viewer-states`）を headless Chromium で開き、[#1221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1221)・[#1222](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1222)・[#1224](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1224) の画面を確認した。[#1223](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1223) は文言だけなので jest の期待値で確認

## 作業上の注意

- worktree を `git -C work/kouchou-ai worktree add <相対パス>` で作ると、相対パスが本体の clone の中に解釈される。`work/` 直下に置くには `../kouchou-ai-<topic>` と書くか、作った後に `git worktree move` する
- Next.js 16.4.2 の `next dev` は、worktree ごとの初回起動で `AGENTS.md` を生成し `next-env.d.ts` を書き換え、アップグレードの案内を出して止まる。2 回目の起動で動く。生成物は commit しない

## Open Questions

- 会議の分析（[#1208](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1208)〜[#1210](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1210)、[#1214](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1214)〜[#1216](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1216)）を本体でどこまで受けるか。今回のコメントは「既存の機能で試せる範囲は本体、新しい見せ方は本体の外で試作」という案で書いた。nishio の判断はまだ
- 利用者定義のラベル（穴 2）を Issue として起こすか。[#1210](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1210)・[#1213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1213) の両方に効き、CLI の任意ステップとして小さく作れる
- 大木さんへの確認待ち：ワークショップで使った版、[#1207](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1207) の画面、[#1205](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1205)・[#1212](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1212) の説明に気づけたか、会議データのサンプル、[#1203](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1203) の (a)(b)

## Updates
- 2026-11-24: nishio の判断で、[#1221](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1221)・[#1223](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1223)・[#1224](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1224) を main に入れた（nishio が手元で admin merge、`f6df8b53`・`d9920fc6`・`ef8a16c4`。[#1206](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1206) は自動で閉じた）。[#1222](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1222) は #1221 と衝突したので main に rebase し（補助関数を 2 つとも残す）、jest 338 件・tsc・biome が通ることを確認した（rebase 後の CI も e2e を含め全件 pass）。[#1205](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1205)・[#1211](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1211)・[#1212](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1212) は残件があるので open のまま
- 2026-11-24: Open Questions の 2 つを Issue にした。利用者定義のラベルは [#1225](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1225)（CLI 先行。今の設定はそのまま動く形、設定の検証・プロンプトの組み立て・集計・ビューアでの表示名・docs）。会議の分析の線引きは [#1226](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1226)（既定の案＝閲覧画面の改善と入力手順は本体、時系列・横断・評価は本体の外で試作、#1208・#1209 はデータが揃ってから実験。期限案 2026-12-08）。関連する Issue からリンクした
