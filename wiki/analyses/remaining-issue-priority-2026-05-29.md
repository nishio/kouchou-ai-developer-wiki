---
type: analysis
summary: "2026-05-29 時点の open issue / open PR を見ると、最優先は新規 feature ではなく、進行中 PR の着地、Windows 導線のサポート境界、ラベル品質実験の採用判断、deploy safety の Blob health check 化である"
sources:
  - github-dev-docs.md
  - source-code.md
  - development-priority-roadmap-2026-05-23.md
  - issue-877-windows-setup-guide-scope.md
  - label-coverage-policy-2026-05-29.md
  - label-refinement-input-scope-2026-05-29.md
  - fetch-reports-deprecation-and-storage-health-2026-05-26.md
  - remaining-bug-issues-2026-05-26.md
  - chart-scroll-ux-decision.md
---

## 結論

2026-05-29 18:04 JST 時点の live GitHub state では、以前の優先候補だった `#741` は `PR #873` merge により close 済み、`#584` と `#629` も open ではない。さらに `#866` `#867` `#868` は merge 済みで、`#869` の label refinement 整理は前提 PR 待ちではなくなっている。したがって、残件の優先順は次のように組み替えるのがよい。[[github-dev-docs]]より

1. **進行中 PR を先に着地させる**: `#883 -> #876` と `#863 -> #731`
2. **Windows beginner guide のサポート境界を確定する**: `#877`
3. **ラベル品質改善を実験として採用判断できる形にする**: `#881`, `#882`, `#869`
4. **deploy safety を current storage contract に合わせる**: `#871`
5. **viewer UX は mobile 方針を先に決めてから個別修正する**: `#872`, `#493`, `#121`, `#283`

新しい可視化案 `#879` `#880` や大型 feature 群は重要だが、上の 5 レーンより後でよい。

## Current State

open PR は `#883` と `#863` の 2 本。`#883` は `#876` を close する開発者向け導線整理で、checks は green、review required。`#863` は `#731` を close する Windows setup の `.bat` / `.ps1` 分離で、checks は green だが Windows 実機検証が未完了とコメントされている。[[github-dev-docs]]より

`#873` は 2026-05-28 に merge 済みで、`#741` は close 済み。`#870` も close 済みで、deploy safety の残作業は `#871` に絞られている。[[github-dev-docs]]より

`work/kouchou-ai/` の `origin/main` は `0c294da` まで取得済み。常用 clone 自体は `codex/issue-876-developer-quickstart` branch 上にいるため、コード断定は `origin/main` と open PR を分けて読む必要がある。[[source-code]]より

open issue のうち `bug` ラベルは `#731`, `#700`, `#477` の 3 件。ただし `#700` は既に `Devesh36` が担当しているため、AI エージェントが独断で着手すべきではない。`#731` は `PR #863` で対応中、`#477` は Azure model selection の UI 不整合で、小さく直せるが Windows / label quality / deploy safety よりは一段後ろでよい。[[github-dev-docs]]より

## Priority 1: 進行中 PR の着地

まず `#883 -> #876` を通す。理由は、PR が ready で CI も通っており、developer onboarding の混乱を小さい human review コストで減らせるからである。これは新規開発というより、既に積んだ作業を backlog から消す cleanup に近い。[[github-dev-docs]]より

次に `#863 -> #731` の扱いを決める。`#863` は Windows setup の文字化け問題に対して設計上は筋がよく、GitHub Actions の `windows-setup-script` も green だが、作者コメントでは Windows 実機検証が未完了。ここは実装を足すより、実機または self-hosted Windows で最低 1 回の確認を取り、merge するか、`#731` を current main の英語化で close するかを決めるのが優先である。[[github-dev-docs]]より [[remaining-bug-issues-2026-05-26]]より

## Priority 2: Windows Guide の境界

`#877` は `#863` の後続 docs として優先度が高い。Windows 利用者が多い一方で、Docker Desktop を入れられる個人 PC、組織管理端末、Docker / WSL2 が禁止された環境が混ざっているため、単なるトラブルシュート表では足りない。[[issue-877-windows-setup-guide-scope]]より

短期の完了条件は、標準入口を `Windows 10/11 + Docker Desktop + Linux containers + Docker Desktop を起動できる権限 + OpenAI または Gemini の API key どちらか一方` と明示すること。Docker Desktop や WSL2 が組織ポリシーで使えない環境は beginner guide の対象外または別の上級者向け導線へ切り出す。[[issue-877-windows-setup-guide-scope]]より

## Priority 3: Label Quality Experiments

`#881` を上位トラッキングとして、少なくとも 1 本の固定条件つき実験を先に回すべきである。現状の論点は、label refinement を PR 化するかだけではなく、上流 `hierarchical_initial_labelling` / `hierarchical_merge_labelling` の `sampling_num=10` ランダムサンプリングがラベルのカバレッジを落としている可能性に移っている。[[label-coverage-policy-2026-05-29]]より

順序としては、`#869` の label refinement PR を default-on に近づける前に、`sampling_num` を実質無効化して全件をラベリング LLM に渡す比較を行うのがよい。そのうえで `#882` の KJ prompt 比較は、baseline / KJ prompt / neutral structured prompt の差を同一 hierarchy で見る。これにより「KJ法という語が効いた」のか「代表性・カバレッジを明示した構造化 prompt が効いた」のかを分けられる。[[label-coverage-policy-2026-05-29]]より [[label-refinement-input-scope-2026-05-29]]より

## Priority 4: Deploy Safety

`#741` は close 済みだが、deploy safety の残課題は `#871` に残っている。current の canonical backing store は Azure Blob sync / restore なのに、古い deploy safety は API scrape / `fetch_reports.py` の発想に寄っていた。旧 `#629` は `#870` / `#871` に分解済みなので、次は `#871` で Blob Storage の read/write health check を deploy 前確認にするのが筋である。[[fetch-reports-deprecation-and-storage-health-2026-05-26]]より [[github-dev-docs]]より

これは user-facing feature ではないが、private / unlisted report を含む運用安全性に効く。公開・運用中のレポートを守る観点では、可視化新機能より上に置いてよい。

## Priority 5: Viewer UX

scatter / mobile 系は、個別の `#121` `#283` を先に直すより、`#872` で mobile は別ビューにするかを決める方がよい。既存分析では、PC 向けの `#493` は「短い遅延つき自動ロック解除 + 視覚フィードバック」が良さそうだが、スマホは同じ散布図責務をそのまま持ち込むと厳しい。[[chart-scroll-ux-decision]]より [[github-dev-docs]]より

したがって、viewer UX の直近判断は `#872` を umbrella とし、mobile では静的画像、クラスタ一覧、階層一覧、簡略図のどれを既定にするかを決めること。`#493` の PC wheel 問題はその次に別 PR で扱う。

## 後ろでよいもの

`#879` ヒートマップ、`#880` マンダラート、`#648` 一括編集、`#679` 任意カテゴリ分類、`#537` OpenRouter 無料モデル、`#690` ts-node-dev 置換は、現時点では優先度を下げてよい。理由は、導入・品質・運用安全性のボトルネックを先に減らさないと、新しい view / feature を足しても product 全体の信頼性が上がりにくいからである。[[development-priority-roadmap-2026-05-23]]より

`#564` 活用事例公開と `#221` 試行錯誤の負担軽減は high priority label が付いているが、どちらも issue 1 件で実装する対象というより、対外説明・導入設計の上位テーマである。実務 issue としては `#877`, `#876`, `#881` のような具体レーンに分解して進める方が扱いやすい。[[github-dev-docs]]より

## Open Questions

- `#863` は Windows 実機検証なしでも GitHub Actions green を根拠に merge するか、実機確認まで待つか
- `#877` は `#863` merge 後に着手するか、current main docs に先にサポート境界だけ入れるか
- `#881` の最初の実験は全件ラベリング比較から始めるか、KJ prompt 比較を同時に走らせるか
- `#871` の Blob health check は GitHub Actions 内で Azure credentials を使って直接行うか、既存 `apps/api/scripts/test_storage.py` を再利用するか

## Updates

- 2026-05-29: 初版作成。live open issues / PRs、`origin/main@0c294da`、既存 wiki 分析を照合し、`#741` close 後の残件優先順として整理した。
