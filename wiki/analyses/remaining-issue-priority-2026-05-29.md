---
type: analysis
summary: "2026-05-29 時点の open issue 121 件を全件メタデータ確認し、本文を古い high-priority / user-facing issue まで読み直すと、project-wide 優先は `#221` 試行錯誤負担削減と `#564` 活用事例公開であり、tactical next は進行中 PR 着地と Windows / cost / API 不安の解消である"
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

ただし、この結論は「すぐ着手できる tactical next」に寄りすぎていた。2026-05-29 の再確認で、open issue は **121 件**、`high priority` label は `#221` と `#564` の 2 件であることを確認した。古い issue の本文まで読み直すと、project-wide には次の順で見る方が正確である。[[github-dev-docs]]より

1. **試行錯誤の負担を減らす**: `#221` を上位テーマとして、`#11`, `#79`, `#292`, `#391`, `#97`, `#877` を束ねる
2. **活用事例と責任ある読み方を公開する**: `#564`, `#696`, `#542`
3. **進行中 PR と Windows 導線を着地させる**: `#883 -> #876`, `#863 -> #731`, `#877`
4. **公開・deploy safety と static 確認を固める**: `#871`, `#518`, `#838`
5. **ラベル品質改善を実験として採用判断できる形にする**: `#881`, `#882`, `#869`
6. **viewer UX は mobile 方針を先に決めてから個別修正する**: `#872`, `#493`, `#121`, `#283`

新しい可視化案 `#879` `#880` や大型 feature 群は重要だが、上のレーンより後でよい。

## Full-Issue Recheck

ユーザから「最近話題になったものだけ見ていないか」と指摘を受け、`gh issue list --state open --limit 1000` で current open issue **121 件**を再取得した。前回も一覧メタデータは全件見ていたが、本文精読は最近動いた issue と既存分析の優先候補に偏っていた。したがって、今回は古い `high priority` issue と user-facing issue を追加で読み直した。[[github-dev-docs]]より

追加で本文を確認した主要 issue:

- `#221` 試行錯誤の負担を減らす
- `#564` 活用事例を集めて公開する
- `#11` レポート出力時間の目安
- `#79` CSV アップロード時の事前コスト表示
- `#97` CSV フォーマットエラーの分かりやすさ
- `#292` OpenAI API 課金設定の混乱
- `#391` レポート作成時の API 異常 preflight
- `#542` レポート責任所在
- `#592` Azure OpenAI Service エラーハンドリング
- `#696` レポート誤読防止
- `#496` Docker Desktop なし導線
- `#537` OpenRouter 無料モデル
- `#255` OpenAI が使えないケース
- `#285` 利用可能 LLM 拡張
- `#253` static HTML file URL エラー
- `#318` extraction 失敗ログ

この再確認により、前回の「進行中 PR -> Windows -> label quality -> deploy safety」という並びは、Codex が今日実装するなら妥当だが、project-wide priority としては不十分だったと判断を修正する。

## Project-Wide Priority

### 1. `#221` 試行錯誤の負担削減を上位テーマに戻す

`#221` は古いが、`high priority` label が付いており、内容も現在の課題と合っている。問題は「実装者が何か 1 機能を作る」ではなく、初回利用者がコスト・時間・API 設定・入力形式・クラスタ数・サンプリングの不安を抱えたまま高コスト処理へ入ること。[[github-dev-docs]]より

この上位テーマにぶら下げるべき直近 issue は `#11` `#79` `#292` `#391` `#97` である。`#11` は処理時間、`#79` は処理前コスト、`#292` は ChatGPT Plus と OpenAI API 課金の混同、`#391` は作成開始時の API 健全性、`#97` は CSV 入力エラーで、いずれも「試す前の不安 / 失敗後の原因不明」を減らす。[[github-dev-docs]]より

したがって code task としては、まず **作成前確認パネル** を小さく設計するのがよい。中身は、概算処理時間、概算コスト帯、API billing / quota check、入力 CSV の列・文字コード・件数確認、クラスタ数との関係の警告。これを全部精密に作る必要はなく、`#79` のコメントにある通り「100 円未満 / 100〜1000 円 / 1000 円以上」の粗い帯でも不安を減らせる。詳細は [[trial-and-error-burden-reduction-2026-05-29]] に分けた。

### 2. `#564` 活用事例と `#696` / `#542` trust layer

`#564` も `high priority` label 付きで、活用事例は導入ハードルに直結する。これは code issue ではなく website / docs / 広報寄りだが、project-wide には上位で扱うべきである。[[github-dev-docs]]より

ただし事例だけを出すと、`#696` が示す「広聴AIレポートを過度に正しい分析として誤読する」問題が残る。したがって `#564` は単独で進めるより、`#696` と `#542` の責任範囲・読み方・限界の説明とセットにする方がよい。導入検討者向けには「何ができるか」と同時に「何を保証しないか」を見せるべきである。[[github-dev-docs]]より

## Current State

open PR は `#883` と `#863` の 2 本。`#883` は `#876` を close する開発者向け導線整理で、checks は green、review required。`#863` は `#731` を close する Windows setup の `.bat` / `.ps1` 分離で、checks は green だが Windows 実機検証が未完了とコメントされている。[[github-dev-docs]]より

`#873` は 2026-05-28 に merge 済みで、`#741` は close 済み。`#870` も close 済みで、deploy safety の残作業は `#871` に絞られている。[[github-dev-docs]]より

`work/kouchou-ai/` の `origin/main` は `0c294da` まで取得済み。常用 clone 自体は `codex/issue-876-developer-quickstart` branch 上にいるため、コード断定は `origin/main` と open PR を分けて読む必要がある。[[source-code]]より

open issue のうち `bug` ラベルは `#731`, `#700`, `#477` の 3 件。ただし `#700` は既に `Devesh36` が担当しているため、AI エージェントが独断で着手すべきではない。`#731` は `PR #863` で対応中、`#477` は Azure model selection の UI 不整合で、小さく直せるが Windows / label quality / deploy safety よりは一段後ろでよい。[[github-dev-docs]]より

## Tactical Priority 1: 進行中 PR の着地

まず `#883 -> #876` を通す。理由は、PR が ready で CI も通っており、developer onboarding の混乱を小さい human review コストで減らせるからである。これは新規開発というより、既に積んだ作業を backlog から消す cleanup に近い。[[github-dev-docs]]より

次に `#863 -> #731` の扱いを決める。`#863` は Windows setup の文字化け問題に対して設計上は筋がよく、GitHub Actions の `windows-setup-script` も green だが、作者コメントでは Windows 実機検証が未完了。ここは実装を足すより、実機または self-hosted Windows で最低 1 回の確認を取り、merge するか、`#731` を current main の英語化で close するかを決めるのが優先である。[[github-dev-docs]]より [[remaining-bug-issues-2026-05-26]]より

## Tactical Priority 2: Windows Guide の境界

`#877` は `#863` の後続 docs として優先度が高い。Windows 利用者が多い一方で、Docker Desktop を入れられる個人 PC、組織管理端末、Docker / WSL2 が禁止された環境が混ざっているため、単なるトラブルシュート表では足りない。[[issue-877-windows-setup-guide-scope]]より

短期の完了条件は、標準入口を `Windows 10/11 + Docker Desktop + Linux containers + Docker Desktop を起動できる権限 + OpenAI または Gemini の API key どちらか一方` と明示すること。Docker Desktop や WSL2 が組織ポリシーで使えない環境は beginner guide の対象外または別の上級者向け導線へ切り出す。[[issue-877-windows-setup-guide-scope]]より

## Tactical Priority 3: Label Quality Experiments

`#881` を上位トラッキングとして、少なくとも 1 本の固定条件つき実験を先に回すべきである。現状の論点は、label refinement を PR 化するかだけではなく、上流 `hierarchical_initial_labelling` / `hierarchical_merge_labelling` の `sampling_num=10` ランダムサンプリングがラベルのカバレッジを落としている可能性に移っている。[[label-coverage-policy-2026-05-29]]より

順序としては、`#869` の label refinement PR を default-on に近づける前に、`sampling_num` を実質無効化して全件をラベリング LLM に渡す比較を行うのがよい。そのうえで `#882` の KJ prompt 比較は、baseline / KJ prompt / neutral structured prompt の差を同一 hierarchy で見る。これにより「KJ法という語が効いた」のか「代表性・カバレッジを明示した構造化 prompt が効いた」のかを分けられる。[[label-coverage-policy-2026-05-29]]より [[label-refinement-input-scope-2026-05-29]]より

## Tactical Priority 4: Deploy Safety

`#741` は close 済みだが、deploy safety の残課題は `#871` に残っている。current の canonical backing store は Azure Blob sync / restore なのに、古い deploy safety は API scrape / `fetch_reports.py` の発想に寄っていた。旧 `#629` は `#870` / `#871` に分解済みなので、次は `#871` で Blob Storage の read/write health check を deploy 前確認にするのが筋である。[[fetch-reports-deprecation-and-storage-health-2026-05-26]]より [[github-dev-docs]]より

これは user-facing feature ではないが、private / unlisted report を含む運用安全性に効く。公開・運用中のレポートを守る観点では、可視化新機能より上に置いてよい。

## Tactical Priority 5: Viewer UX

scatter / mobile 系は、個別の `#121` `#283` を先に直すより、`#872` で mobile は別ビューにするかを決める方がよい。既存分析では、PC 向けの `#493` は「短い遅延つき自動ロック解除 + 視覚フィードバック」が良さそうだが、スマホは同じ散布図責務をそのまま持ち込むと厳しい。[[chart-scroll-ux-decision]]より [[github-dev-docs]]より

したがって、viewer UX の直近判断は `#872` を umbrella とし、mobile では静的画像、クラスタ一覧、階層一覧、簡略図のどれを既定にするかを決めること。`#493` の PC wheel 問題はその次に別 PR で扱う。

## 後ろでよいもの

`#879` ヒートマップ、`#880` マンダラート、`#648` 一括編集、`#679` 任意カテゴリ分類、`#537` OpenRouter 無料モデル、`#690` ts-node-dev 置換は、現時点では優先度を下げてよい。理由は、導入・品質・運用安全性のボトルネックを先に減らさないと、新しい view / feature を足しても product 全体の信頼性が上がりにくいからである。[[development-priority-roadmap-2026-05-23]]より

`#537` を下げるのは、OpenRouter provider の存在だけでは無料モデル・embedding・parse 経路の検証がまだ残り、provider UX 全体 (`#477`, `#473`, `#592`, `#255`, `#285`) の中で順序づけるべきだからである。Azure model UI 不整合の `#477` は小さく直せる active bug だが、初回不安・Windows 境界・作成前 preflight よりは後ろでよい。

`#564` 活用事例公開と `#221` 試行錯誤の負担軽減は **後ろでよいわけではない**。ただし issue 1 件で実装する対象ではなく、上位テーマとして具体 issue に分解して進める必要がある。`#221` は `#11` / `#79` / `#292` / `#391` / `#97` へ、`#564` は `#696` / `#542` と website / docs 側の作業へ分けるのが扱いやすい。[[github-dev-docs]]より

## Open Questions

- `#863` は Windows 実機検証なしでも GitHub Actions green を根拠に merge するか、実機確認まで待つか
- `#877` は `#863` merge 後に着手するか、current main docs に先にサポート境界だけ入れるか
- `#221` の最初の具体 PR は、作成前確認パネル (`#11` / `#79`) から始めるか、API billing / quota preflight (`#292` / `#391`) から始めるか
- `#564` は kouchou-ai repo で持ち続けるか、website repo 側へ移して事例公開 workflow を別管理するか
- `#881` の最初の実験は全件ラベリング比較から始めるか、KJ prompt 比較を同時に走らせるか
- `#871` の Blob health check は GitHub Actions 内で Azure credentials を使って直接行うか、既存 `apps/api/scripts/test_storage.py` を再利用するか

## Updates

- 2026-05-29: `#221` 系の concrete tracking issue として `#884` `[FEATURE] レポート作成前に入力・コスト・API状態を確認できるパネルを追加する` を起票し、下位 issue `#11`, `#79`, `#292`, `#391`, `#97` へ相互リンクコメントを追加した。
- 2026-05-29: 初版作成。live open issues / PRs、`origin/main@0c294da`、既存 wiki 分析を照合し、`#741` close 後の残件優先順として整理した。
