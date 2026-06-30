---
type: analysis
summary: "Issue #884 の作成前確認パネル first PR 向け実装契約。CSV / Spreadsheet / plugin を同じ review model に通し、既存 API check / reuse / token usage 表示を混同せず段階実装する"
last_checked: 2026-06-30 18:55 JST
sources:
  - github-issues-221-884-trial-burden-live-2026-06-30.md
  - trial-and-error-burden-reduction-2026-05-29.md
  - development-next-actions-live-2026-06-30.md
  - source-code.md
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/884
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/221
---

## Conclusion

#884 の first PR は、`window.confirm` の見た目改善ではなく、CSV / Spreadsheet / plugin の 3 入力経路を同じ `pre-create review model` に通す実装として切るべきである。2026-06-30 18:55 JST 時点で GitHub #884 / #221 は open / unassigned のまま、`work/kouchou-ai/main@d5c9ece` でも #884 は未実装である。[[github-issues-221-884-trial-burden-live-2026-06-30]]より

既存部品はすでに多い。`apps/admin/app/create/page.tsx` は送信直前に comments を組み立て、CSV / plugin だけ `comments.length < clusterLv2` を `window.confirm` で警告する。Spreadsheet は comments を組み立てるが同じ警告を通らない。`EnvironmentCheckDialog` は `/admin/environment/verify` を呼べるが、送信前 flow とは分離した手動 dialog である。再利用は `docs/user-guide/reuse-report.md`、`/reuse/:slug`、`DuplicateReportDialog`、analysis-core `reuse_from` に既に存在する。[[source-code]]より

したがって first PR の contract は、「既存の分散した確認を 1 つの review surface に集める」ことであり、精密な cost estimator、sample report 作成、reuse 実行、Windows setup、実行中 ETA は含めない。

## Review Model

作成前確認パネルに渡す最小 model は次で足りる。

| field | source in current main | note |
|---|---|---|
| input_type | `inputData.inputType` | `file` / `spreadsheet` / `plugin:<id>` を表示用 label に変換する |
| comment_count | built `comments.length` | plugin preview の `totalCount` ではなく import 後の実 comments 件数を使う |
| selected_comment_column | `inputData.selectedCommentColumn` または `pluginData.pluginSelectedCommentColumn` | 自動選択された列でもユーザーが確認できるように出す |
| selected_attribute_columns | `inputData.selectedAttributeColumns` または `pluginData.pluginSelectedAttributeColumns` | 個人情報・属性誤選択の確認にも効く |
| cluster_lv1 / cluster_lv2 | `clusterSettings` | `recommendedClusters` と現在値がずれていれば warning 候補 |
| provider / model | `aiSettings.provider` / `aiSettings.model` | OpenAI / Gemini / local などの違いを見せる |
| user_api_key_present | `aiSettings.userApiKey.trim()` | key 値は出さない。ある / ないだけ |
| warnings | derived | まずは `comment_count < clusterLv2` と missing/empty risk |
| api_check_state | existing verify result or unverified | first PR では `未確認` 表示でもよい。統合呼び出しは次 slice でも可 |
| estimate_state | placeholder / coarse bucket | 実行後 token usage の cost 表示とは別物として扱う |

この model は、`createReport` に送る payload そのものではない。送信 payload を作る前に review すると二重実装になりやすいため、first PR では current `onSubmit` 内の comments construction を小さな helper に切り出し、`review -> confirm -> createReport` が同じ comments を使う形に寄せるのが自然である。

## Warning Policy

first PR の warning は増やしすぎない。

- `comment_count < clusterLv2` は 3 入力経路すべてで出す。これは既存 warning の横展開であり、Spreadsheet の抜けを塞ぐ。
- `comment_count === 0` は validation error として扱い、review dialog ではなく既存 validation / toast に寄せる。
- selected comment column が空の時も review 以前の validation error とする。
- `clusterLv2` が `recommendedClusters.lv2` より大きい場合は warning 候補だが、first PR では existing `comment_count < clusterLv2` に絞ってもよい。
- API check が `authentication_error` / `insufficient_quota` の時 hard block するかは未決。first PR では state 表示だけに留め、block policy は次 slice の人間判断に残してよい。

## Cost / Time Scope

作成後の `TokenUsage` は、実行済み report の `tokenUsageInput` / `tokenUsageOutput` / `estimatedCost` を表示する部品である。これは #884 の作成前見積もりとは違う。[[source-code]]より

first PR で cost / time を入れるなら、精密な金額ではなく `目安なし`、または `小 / 中 / 大` の粗い帯にする。価格表や provider 差分を正確に追う実装は、first PR の scope 外に置く。

## Reuse / Sample Scope

reuse は未実装の大物ではなく、既存の再利用機能である。作成前確認では、大規模入力や再実行時に「既存レポートを再利用できる」導線を出すだけで十分である。実際に `/reuse/:slug` へ誘導する条件や、sample-first report を作る UI は後続 slice とする。[[source-code]]より

plugin 入力では preview が 10 件で、import は `maxResults = 1000` が default である。review に表示すべきなのは preview 件数ではなく、import 後の `comments.length` である。preview だけで review に進ませると、ユーザーが全件実行規模を誤認する。

## Test Gates

first PR の最低 test / QA は次を見ればよい。

- CSV path: comments 件数が `clusterLv2` 未満の時、既存 `window.confirm` ではなく review panel の warning が出る。
- Spreadsheet path: 同じ条件で warning が出る。これは現行 main の gap を塞ぐ確認。
- Plugin path: imported data の comments 件数で warning が出る。preview 件数では判定しない。
- Cancel: review panel で戻ると `createReport` が呼ばれず、loading が解除される。
- Continue: review panel で続行すると、review に使った comments と同じ payload で `createReport` が呼ばれる。
- Environment check: first PR で統合しない場合でも、panel 上に `未確認` として表示され、既存の手動 `EnvironmentCheckDialog` と矛盾しない。

## Open Questions

- API check の `authentication_error` / `insufficient_quota` を hard block にするか、警告付き続行にするか。
- `rate_limit_error` は一時的な状態なので、block ではなく retry guidance に寄せるか。
- cost / time bucket を first PR に入れるか、表示領域だけ先に作るか。
- reuse 導線は作成前確認内の静的リンクにするか、大規模入力時だけ conditional に出すか。

## Updates

- 2026-06-30: 初回作成。GitHub #884 / #221 と `work/kouchou-ai/main@d5c9ece` の create flow / EnvironmentCheckDialog / reuse / TokenUsage を照合し、first PR の実装契約として整理した。
