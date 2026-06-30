---
type: source
summary: "Issue #221 / #884 と下位 issue の 2026-06-30 live state。試行錯誤負担削減は #884 の作成前確認パネル first slice に具体化されているが、current main ではまだ window.confirm と手動 API check が分離している"
last_checked: 2026-06-30 19:15 JST
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/221
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/884
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/11
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/79
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/292
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/391
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/97
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/877
  - source-code.md
  - trial-and-error-burden-reduction-2026-05-29.md
  - issue-884-pre-create-review-contract-2026-06-30.md
---

## What it is

2026-06-30 16:54 JST に GitHub issue live state と `work/kouchou-ai` current main (`d5c9ece`) を再確認したメモ。目的は、`#221` 試行錯誤負担削減がまだ抽象 umbrella なのか、実装可能な first slice に落ちているのかを確認すること。

2026-06-30 19:15 JST に #884 / #221 の live state と `work/kouchou-ai/main@d5c9ece` を再確認し、state は変わっていないことを確認した。追加で、first PR の実装契約は [[issue-884-pre-create-review-contract-2026-06-30]] に切り出し済みである。

## Freshness marker

- `work/kouchou-ai`: `main@d5c9ece`, 19:15 JST に `git fetch origin && git pull --ff-only` 済み。
- high priority open issue: `#884`, `#564`, `#221` の 3 件（19:15 JST 確認）。
- `gh issue view` で `#221`, `#884`, `#11`, `#79`, `#292`, `#391`, `#97`, `#877` を確認（#221 / #884 は 19:15 JST に再確認）。

## Live issue state

| issue | state | assignee | role |
|---|---|---|---|
| #221 `(情報整理)試行錯誤の負担を減らす` | open / high priority | none | umbrella。2026-05-29 コメントで #884 を concrete tracking issue として接続済み |
| #884 `レポート作成前に入力・コスト・API状態を確認できるパネルを追加する` | open / high priority | none | first implementation slice。CSV / Spreadsheet / plugin を同じ作成前確認パネルへ通す |
| #11 `レポート出力にかかる時間の目安` | open | nishio | #884 child。最初は粗い時間帯、精密 ETA は後続 |
| #79 `CSVアップロード時のコスト表示` | open | none | #884 child。精密な金額ではなく粗い費用帯が first slice |
| #292 `OpenAI APIの課金設定に関する混乱` | open | none | docs issue だが、アプリ側では API / billing / quota 状態と docs 導線を #884 へ接続 |
| #391 `APIが正常でない場合にわかりやすいエラー` | open | none | 既存 API check を作成前フローへ統合する論点 |
| #97 `CSVフォーマットエラーをわかりやすくする` | open | none | 文字コード変換後の next slice。まず選択コメント列 / 非空件数 / クラスタ数関係を確認パネルに出す |
| #877 `Windows setup guide` | open | none | 隣接だが別テーマ。起動前の導入摩擦であり、#884 の起動後・作成前確認とは分ける |

## Current main observation

`apps/admin/app/create/page.tsx` では、送信時に CSV / spreadsheet / plugin の `comments` を組み立ててから `createReport` を呼ぶ。CSV path と plugin path では `comments.length < clusterLv2` の時に `window.confirm` が出る。一方、spreadsheet path は comments を組み立てるが、同じ警告は通らない。[[source-code]]より

`EnvironmentCheckDialog` は作成画面に表示されているが、送信前の go / no-go 判断とは分離した手動ボタンである。内部では `verifyApiKey` を呼び、成功、`authentication_error`、`insufficient_quota`、`rate_limit_error`、`unknown_error` を表示できる。つまり足りないのは API check の存在ではなく、作成前確認 flow への統合である。[[source-code]]より

reuse は未実装ではない。`docs/user-guide/reuse-report.md`、`/reuse/:slug` ページ、`DuplicateReportDialog`、analysis-core の `reuse_from` が存在し、既存レポートの中間成果物を再利用して重い extraction / embedding を避ける導線がある。したがって #884 では、大規模入力時の `sample-first / reuse` は新規巨大機能ではなく、既存 reuse 能力への入口として扱う方がよい。[[source-code]]より

## Reading

#884 は 2026-06-30 時点でも妥当な first slice である。現行 UI にはすでに「確認らしきもの」が複数あるが、ユーザーが実行前に知りたい情報は分散している。`window.confirm` は件数とクラスタ数の一部だけ、API check は手動、費用/時間は注意書きまたは実行後の情報、reuse は別導線である。

最初にやるべきことは、精密な費用予測や ETA ではなく、CSV / Spreadsheet / plugin のすべての入力経路を同じ pre-create review に通し、入力件数、コメント列、属性列、クラスタ数、provider/model、API check status、警告、費用/時間の placeholder を 1 箇所に集めることである。

spreadsheet path に既存 warning がない点は、#884 の first PR で自然に塞げる current gap である。`window.confirm` の単純置換ではなく、「全入力経路で同じ review model を作る」ことを完了条件に入れる必要がある。

## Open Questions

- API check が `authentication_error` / `insufficient_quota` の時、submit を hard block するか、警告付きで続行可能にするか。
- `rate_limit_error` は一時的な状態なので、hard block と retry guidance のどちらに寄せるか。
- 粗い費用帯 / 時間帯の bucket を、comment count、文字数、model、provider のどこまでで切るか。
- 大規模入力時に sample-first を勧めるだけにするか、実際に sample report を作る UI まで first slice に含めるか。

## Updates

- 2026-06-30 19:15 JST: #884 / #221 と `work/kouchou-ai/main@d5c9ece` を再確認し、open / high priority / unassigned の state は変わらないことを確認した。
- 2026-06-30: 18:55 JST に #884 / #221 と `work/kouchou-ai/main@d5c9ece` を再確認し、first PR の review model / warning policy / test gates を [[issue-884-pre-create-review-contract-2026-06-30]] に切り出した。
- 2026-06-30: 初回作成。#221/#884 と下位 issue、current main の create / environment check / reuse flow を照合し、#884 first slice が今も妥当であることを固定した。
