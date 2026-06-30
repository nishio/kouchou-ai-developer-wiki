---
type: analysis
summary: "2026-06-30 19:30 JST 時点の開発 next action 候補。open PR / high priority issue / nishio assigned issue を live 確認し、#884 作成前確認パネルを第一候補、#903 review comment を低リスク補助、#885 prototype と #898 validation を次点として整理する"
last_checked: 2026-06-30 19:30 JST
sources:
  - current-status-2026-06-30.md
  - docs-issue-map-2026-06-30.md
  - github-issues-221-884-trial-burden-live-2026-06-30.md
  - issue-884-pre-create-review-contract-2026-06-30.md
  - trial-and-error-burden-reduction-2026-05-29.md
  - pr-903-review-comment-draft-2026-06-30.md
  - issue-885-node-runtime-next-scope-2026-06-30.md
  - issue-898-close-readiness-2026-06-30.md
  - github-high-priority-label-query-footgun-2026-06-30.md
  - source-code.md
  - https://github.com/digitaldemocracy2030/kouchou-ai/pulls
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/884
---

## Freshness

2026-06-30 19:30 JST に GitHub live state を再確認した。確認範囲は、open PR、`high priority` open issue、nishio assigned open issue、#884 の assignee / labels / updatedAt である。全 open issue の再 triage はしていない。

確認結果は 18:44 JST の確認と同じだった。

| target | live state |
|---|---|
| open PR | #903 `docs: Web UI の Node runtime 依存インベントリを追加 (#885)` が review required / blocked、#891 `Windows スタンドアロン` が draft / dirty / review required |
| high priority issue | #884 / #564 / #221 の 3 件、すべて unassigned |
| nishio assigned issue | #898 / #876 / #519 / #370 / #255 / #11 |
| #884 | open / high priority / unassigned。2026-05-29 から updatedAt は動いていない |

なお、GitHub label の exact name は `high priority` であり、`priority: high` ではない。誤った label 名で `gh issue list` すると 0 件に見えるため、live state 確認では `--label "high priority"` を使う。[[github-high-priority-label-query-footgun-2026-06-30]]より

このため、開発 next action 判断では「今日の文脈に関係する live state は読んだ」と言える。ただし、全 issue を本文・コメントまで読み直した 2026-06-01 triage の更新版ではない。

## Recommendation

開発 next action の第一候補は #884 `レポート作成前に入力・コスト・API状態を確認できるパネルを追加する` である。理由は、(1) high priority かつ unassigned、(2) #221 umbrella から実装可能な first slice に落ちている、(3) current main で CSV / plugin の `window.confirm`、spreadsheet の同警告抜け、手動 API check、別導線 reuse が分散している、(4) `apps/admin/app/create/page.tsx` 周辺に差分を閉じやすい、の 4 点。[[github-issues-221-884-trial-burden-live-2026-06-30]]より

first PR は「既存 confirm の見た目改善」ではなく、CSV / Spreadsheet / plugin の全入力経路で同じ pre-create review model を作る slice にする。表示する最小情報は、コメント件数、コメント列、属性列、クラスタ数、provider / model、API check status、件数とクラスタ数の警告、費用 / 時間の placeholder または粗い帯でよい。[[trial-and-error-burden-reduction-2026-05-29]]より

18:55 JST の追加確認で、この first PR の実装契約を [[issue-884-pre-create-review-contract-2026-06-30]] に切り出した。重要なのは、送信 payload を別途再構築するのではなく、current `onSubmit` 内の comments construction を review と create で共有すること、Spreadsheet path の warning gap を塞ぐこと、plugin preview 件数と import 後 comments 件数を混同しないことである。

実装に着手する場合は、repo 運用上、先に issue #884 の assignee 有無を再確認し、AI が着手するなら自分を assign してから branch / PR へ進む必要がある。[[source-code]]より

## Candidate Matrix

| candidate | why | risk | next gate |
|---|---|---|---|
| #884 作成前確認パネル | high priority / unassigned / first slice が明確。user-facing の試行錯誤負担を直接下げる | medium。UI flow と API check status の block 条件判断が必要 | 着手するなら assignee 確認 → assign → `apps/admin/app/create` 周辺で PR |
| PR #903 review comment | human authored PR に直接 push せず、既存 docs PR を前に進めるだけ | low。コメント投稿だけならコード衝突なし | 人間が GitHub コメント投稿を許可するか |
| #885 admin export / static-site-builder prototype | Windows single-exe / runtime Node free の技術前提として重要 | high。#903 / #891 と絡み、設計判断が多い | #903 inventory 精度を締め、admin export と static-site-builder decision を child slice 化 |
| #898 aarch64 validation | nishio assigned bug の close readiness に関係する | medium。実機確認できるかが blocker | aarch64 Docker 実機確認、できない場合は pending validation として issue comment |
| #877 Windows guide / #876 docs spine | docs-safe で進めやすい | medium。#876 は nishio assigned、#877 は実機検証条件が残る | docs-safe PR を 1 本選ぶ人間判断 |

## Reading

開発以外の整理が進んだ後、次に足りないのは「開発で何を切ればよいか」の圧縮である。#564 / 8/2 / website / public case は docs / public trust layer として材料が増えたが、コード PR としての明確さでは #884 が最も強い。[[current-status-2026-06-30]]より

一方で、#903 は低リスクだが人間 authored PR なので、AI が branch を直接触るべきではない。Wiki に固定済みの review comment draft を人間判断で投稿する補助 action に留めるのがよい。[[pr-903-review-comment-draft-2026-06-30]]より

#885 は重要だが、PR #891 が draft / dirty、PR #903 が blocked のままなので、いきなり packaging 実装に入ると衝突しやすい。次は inventory accuracy、admin static export prototype、static-site-builder runtime build decision を分けるのが安全である。[[issue-885-node-runtime-next-scope-2026-06-30]]より

#898 は nishio assigned で残っているが、PR #899 は main 済みで、残りは aarch64 Docker 実機確認または close 判断である。実機がない場合は実装 PR より issue 上の pending validation 整理が中心になる。[[issue-898-close-readiness-2026-06-30]]より

## Open Questions

- #884 の API check status は、`authentication_error` / `insufficient_quota` を hard block にするか、警告付き続行にするか。
- 費用 / 時間は first slice で placeholder に留めるか、粗い bucket まで入れるか。
- #884 着手時に、sample-first / reuse はリンクだけにするか、review dialog 内の選択肢にするか。
- PR #903 review comment は AI が投稿してよいか、人間が文面を確認して投稿するか。

## Updates

- 2026-06-30 19:15 JST: GitHub live state を再確認し、open PR 2 本 / high priority issue 3 件 / nishio assigned 6 件は 18:44 JST から変化なし。#884 は引き続き open / high priority / unassigned。
- 2026-06-30 19:30 JST: GitHub live state を再確認し、open PR 2 本 / high priority issue 3 件 / nishio assigned 6 件は変化なし。`high priority` label 名の query footgun を [[github-high-priority-label-query-footgun-2026-06-30]] に切り出した。
- 2026-06-30: [[issue-884-pre-create-review-contract-2026-06-30]] を追加し、#884 first PR の review model / warning policy / test gates を実装前仕様として接続した。
- 2026-06-30: 初回作成。18:44 JST の GitHub live state をもとに、開発 next action は #884 作成前確認パネルを第一候補、#903 review comment を低リスク補助、#885 / #898 を次点として整理した。
