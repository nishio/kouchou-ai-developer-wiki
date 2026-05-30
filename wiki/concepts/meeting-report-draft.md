---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。会議ごとに過去回を snapshot として archive へ rotate し、本ページは次回向けの差分のみ積み上げる"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
---

## 目的

このページは、**次の定例会議で Codex 関連の作業を短時間で報告するための下書き** である。Issue / PR / CI / wiki の更新が散らばるので、会議前に思い出すのではなく、作業のたびにここへ要点を寄せる。

ポイントは「全部の変更履歴」を書くことではなく、**会議で口頭共有したい判断と進み具合だけを残す** こと。詳しい根拠は各 concept / analysis / source ページへリンクする。[[coding-agents]]より [[contributing]]より

## 使い方

- 1 項目は 2〜4 行程度で、`やったこと / 現在地 / 次の一手` が分かる粒度にする
- merge 済みか進行中かを明記する
- issue 番号、PR 番号、main commit などの検索キーを残す
- 会議で読まない細かい実装詳細はこのページに詰め込まず、関連ページへ送る
- 会議が終わったら本ページを `wiki/concepts/meeting-report-YYYY-MM-DD.md` へ rotate し、本ページは次回向けに空に戻す

## 過去回

- [[meeting-report-2026-05-25]] — 大リファクタリング完了、LLM grouping 実験、ラベル refinement 実験、open issue 棚卸し、Windows setup 切り替えなど

## 次回定例向け下書き (2026-06-01 向け)

- label refinement 実験は、このまま main 昇格を目指すより仕切り直す判断に寄せた。現行 refinement は rep args を見ない polish-only で、上流 sampling は random、UI の個別データも代表例選定ではなく配列先頭、rubric judge v0 も過去のズレを十分に検出できていない。次は refinement prompt を磨くのではなく、(1) sampling 全件入力実験、(2) `典型例 / 幅 / 境界` に分けた rep args artifact、(3) judge 入力と rubric 較正、(4) UI 表示責務を分けて小さく検証する。[[label-quality-redesign-reset-2026-05-30]] に整理済み。
- ohki-shingo の Slack 指摘を受け、ラベル品質改善はまず「全体傾向の把握」を良くしたいのか「少数だが重要な論点の発見」を良くしたいのかを固定する必要があると補正した。前者なら上位トピックの安定カバー、後者なら minority / boundary / residual evidence を別 artifact として残す設計が要る。次の実験では use-case contract を run metadata / judge prompt に明示する。[[slack-label-algorithm-improvement-2026-05-30]]より [[label-quality-redesign-reset-2026-05-30]]より
- current main `0c294da` のラベル入力 sampling と UI 個別データ表示を確認した。ラベル付け時は API 通常経路では initial / merge とも最大 30 件、analysis-core default では 10 件で、どちらも Polars の seed なし random sample。最大被覆 / FPS / k-medoids / ラベル適合度による選択ではない。UI の階層リストも representative selection ではなく、deepest-level cluster の arguments を配列先頭から 10 件表示している。次に改善するなら、まず全件入力でラベル品質が上がるかを見るか、代表例選定を別 artifact として定義する必要がある。
- 実装済み rubric judge を、退避済み過去出力 `jigsaw_sample_comments_400_hierarchical_8_40_refine_{none,setwise,contrast,balanced}` の level 1 に対して `gpt-4o-mini` / `sample-mode all` で実行した。合計 174,839 tokens、概算 $0.03936。結果は `none / setwise / balanced` が score_rate 1.0、`contrast` が 0.9766、fatal flag 0 件で、現行 v0 rubric は human / Claude judge が拾っていたラベルずれを十分に検出できていない。次は criteria を厳格化するか、judge 前に evidence / topic candidates を抽出してから採点する必要がある。
- `codex/remaining-experiment-wip` にラベル品質の rubric judge を実装した。新規 `experiments/evaluation_report/src/evaluation_label_rubric_llm.py` は cluster-level と label-set を `true/false` criteria + points + fatal flags で評価し、`run_evaluation.py --judge rubric` から実行できる。過去出力ディレクトリを直接指定する `--dataset-path` / `--output-dir` も追加したので、既存成果物をコピーせず再評価できる。CSV/HTML には `rubric_score_rate` と要確認フラグを出す。検証は prompt-only smoke、dataset-path smoke、CSV/HTML render smoke、Ruff、py_compile、`tests/test_label_refinement.py` 3 passed まで確認済み。次は既存 `[8,40]` bundle で human judge と照合する。
- Zenn / Ubie の LLM-as-a-Judge ルーブリック評価記事を参考に、ラベル品質 judge を `true/false` criteria + points + negative criteria に分解する案を [[label-quality-rubric-evaluation-2026-05-29]] に整理した。`一貫性 / 具体性 / 網羅性 / 区別性` をそのまま 1-5 点化するのではなく、cluster-level と label-set の 2 層で、coverage / grounding / sibling distinction / scanability / register / fatal penalty を見る。まず既存 `[8,40]` judge bundle で人間判断と照合し、pipeline 標準 step ではなく offline experimental artifact として回すのが次の一手。
- ラベル refinement 実験 (`codex/remaining-experiment-wip`) の独立 judge を Claude で回し、`none / setwise / contrast / balanced` を 3 軸 (個別代表性 / 一覧読みやすさ / 隣接区別性) で比較した結果と、Slack で集めた人間判断を [[label-coverage-policy-2026-05-29]] に集約した。決まった方針: (1) ラベルは「目次」ではなく「要約」として上位 2〜3 軸までカバーする方向、(2) 1 キーワードで完全包括は無理なので greedy max-coverage の発想で「AとB」程度まで広げる、(3) `contrast` の「エンタメ」のような口語 register は post-processing で吸収可。次回提案したい実験は、tokoroten 案の「タイトル候補 emb × 各要素 emb の cos 類似度総和を最大化」と、上流 `hierarchical_initial_labelling` の sampling 戦略を `random → max coverage / FPS` に切り替えるテスト。
- 上記の judge 中に、`hierarchical_label_refinement.py` が rep args を入力に取らず current_label + children labels だけで polish していることを確認し [[label-refinement-input-scope-2026-05-29]] に記録した。default-off で main 同梱は OK だが、default-on 昇格を語る前に上流の `sampling_num=10` 完全ランダムサンプリングの方が本質的なボトルネックである、という方針整理を提示する予定。
- ラベル品質改善の議論が Slack / wiki / WIP branch / issue に散っていたため、上位トラッキング issue `#881` `[analysis-core] ラベル品質改善の実験・議論を追跡可能にする` を起票し、既存 `#869` からもリンクした。未実施実験として、KJ法的プロンプトが本当に効くのかを baseline / KJ prompt / neutral structured prompt で比べる `#882` も切り出した。[[github-dev-docs]]より [[label-coverage-policy-2026-05-29]]より [[kj-method-broadlistening-framing-2026-05-25]]より
- 新しい可視化アイデアとして `#879` `[FEATURE] クラスタと時刻の掛け合わせでヒートマップ表示したい` と `#880` `[FEATURE] [8, 64] の分析をマンダラートで可視化したい` を起票した。`#879` はクラスタ別の時間的な盛り上がりを読むビュー、`#880` は主要 8 観点と 64 下位要素を探索するビューとして、まず mock / prototype で読みやすさを確認するのが次の一手。[[github-dev-docs]]より
- Issue `#876` (`README / docs の開発者向け導線を current main に合わせて整理する`) に対して PR `#883` `codex/issue-876-developer-quickstart` を作成。新規 canonical `docs/development/developer-quickstart.md` を作り、Docker Compose / dummy-server + frontend dev / native (apps/api・apps/admin) / CLI (analysis-core) の 4 モードを「最初の 1 ページ」で判断できる入口にした。各モードに必要な環境変数・起動コマンド・確認 URL・よくある落とし穴（`.env` の置き場所、Docker rebuild trigger、`analysis-core` editable install）を集約し、`README.md` は 240 → 92 行へ trim、`docs/index.md` / `docs/getting-started/quickstart.md` / `mkdocs.yml` も新ページに合わせて整理。`mkdocs build --strict` pass 済み。次回までに CI / review コメントを通したい。
- 残 issue の優先順を live state で組み直した。current open は 121 件で、全件メタデータ確認後に古い high priority も読み直すと、project-wide には `#221` 試行錯誤負担削減と `#564` 活用事例公開を上位に戻すべきだった。tactical next は `#883 -> #876` と `#863 -> #731` の進行中 PR 着地、`#877` Windows guide 境界、`#881` / `#882` / `#869` ラベル品質実験、`#871` Blob health check、`#872` / `#493` viewer UX。[[remaining-issue-priority-2026-05-29]]より
- `#221` 系を掘り下げ、単一 feature ではなく「作成前確認 / API・billing preflight / 入力検証 / 実行中見通し / 再利用」の 5 面で試行錯誤負担を下げるテーマと整理した。この具体 issue として `#884` `[FEATURE] レポート作成前に入力・コスト・API状態を確認できるパネルを追加する` を起票し、`#221`, `#11`, `#79`, `#292`, `#391`, `#97` へ整理コメントを追加。最初の PR は `apps/admin/app/create/page.tsx` の既存 `window.confirm` を作成前確認パネルへ置き換える slice。[[trial-and-error-burden-reduction-2026-05-29]]より

- Windows setup guide issue `#877` は、API key や Docker Desktop 起動確認の文言整理だけでなく、Docker Desktop を入れられる個人 PC と、組織ポリシー / ライセンスで Docker Desktop や WSL2 が使えない貸与 PC を分けるサポート境界の問題として整理した。短期は Docker Desktop が使える Windows 10/11 を標準入口にし、使えない環境は beginner guide の対象外または上級者向け WSL2 + Docker Engine 別ルートへ切り出すのが筋。[[issue-877-windows-setup-guide-scope]]より [[docker-desktop-license-2026-05-29]]より
- developer-wiki の Pages subpath 問題を踏まえ、Quartz + GitHub Pages project-site の設計メモを public Gist `https://gist.github.com/nishio/35d604f23a39aca369ac74db8b65b655` として外部化した。旧 Gist の `wiki/ -> content/` 変換は汎用 Obsidian vault には有効だが、この repo では `wiki/` direct build を維持し、`baseUrl` と生成物リンク検査で守る方針を明文化した。[[wiki-pages-publishing-stack]]より
- developer-wiki の GitHub Pages で、index や検索結果のリンクが project-site subpath と噛み合わず壊れる問題を再点検した。Quartz 4 は `baseUrl` で project-site hosting を扱えるため、root 専用 `<base>` patch は撤去し、`scripts/check_pages_links.py` を CI に入れて build 後の全内部リンクが `/kouchou-ai-developer-wiki/` 配下に解決されることを検査する形に直した。[[wiki-pages-publishing-stack]]より [[wiki-pages-tooling-observation-2026-05-21]]より
- `#874` は commit `51a7c77` で、`hierarchical_layout_generation` を標準 workflow / specs / orchestrator / config defaults / standard step exports から外し、標準パイプラインを 8 step のまま維持する修正を push した。layout 生成 step と `layouts` を読む visualization は実験コードとして残すが、default では走らない。Ruff / Pytest / Server Tests / CodeQL は GitHub Actions で pass、CodeRabbit は review in progress。
- pipeline step 追加判断に、open PR `#866` / `#867` / `#874` も反映した。`#866` は LLM grouping を既存 step に押し込まず workflow として切る良い例、`#867` は downstream step 比較のための reuse/rerun 基盤、`#874` は `layouts` という named layout artifact を作る実験としては筋がある。ただし実験的な semantic island layout 生成を標準パイプラインで常時走らせる理由は弱く、現時点では標準 9 step 化せず、明示有効化される実験用経路に戻す判断とした。[[pipeline-step-addition-framing-2026-05-27]]より [[open-pr-pipeline-step-observation-2026-05-28]]より [[pipeline-step-default-policy-decision-2026-05-28]]より
- `#741` 向けの最小修正として `.github/workflows/azure-deploy.yml` に workflow-level `concurrency` を追加する `PR #873` を作成し、2026-05-28 に merge 済み。これにより `#741` は close 済みで、今後の deploy safety 残課題は `fetch_reports.py` 依存を Blob Storage health check へ置き換える `#871` 側に絞られた。[[issue-741-current-state-2026-05-26]]より [[remaining-issue-priority-2026-05-29]]より
- `#741` は「npm flaky」ではなく、近接する main push が Azure Container Apps 更新で競合する `ContainerAppOperationInProgress` 問題として読み替え、workflow-level serialization で一旦閉じた。次に見るべきは Azure update retry ではなく、current storage contract と deploy safety のズレを解く `#871`。[[fetch-reports-deprecation-and-storage-health-2026-05-26]]より
- `#121` と `#283` の再観測を踏まえ、スマホでは現状の散布図 UI をそのまま使うのは現実的でないという前提で、新規 issue `#872` `[FEATURE] スマホ環境では散布図と別ビューを提供する方針を検討する` を作成した。論点は「responsive 調整で粘るか」ではなく、「mobile では静的画像・クラスタ一覧・簡略図など別ビューを既定にするか」を決めること。これに合わせて `#121` と `#283` の `bug` ラベルは外し、上位検討 issue の参考課題へ寄せた。[[remaining-bug-issues-2026-05-26]]より [[github-dev-docs]]より
- 残っている `[BUG]` title issue は 2026-05-29 時点で再確認し、`#741` は close 済みに更新した。現在の `bug` ラベル open issue は `#731` / `#700` / `#477` で、`#731` は `PR #863` 対応中、`#700` は他 contributor assigned、`#477` は Azure model UI 不整合として残るが直近最優先ではない。[[remaining-issue-priority-2026-05-29]]より
- `worktree: codex/mst-visualization-prototype` で `LLM grouping` 済み 422 argument の可視化を、MST overlay / supervised UMAP / semi-supervised UMAP / LDA / centroid-MDS と順に試したが、どれも「cluster が離れすぎる」か「他 group に混ざって見える」問題を解消できなかった。最終的には、embedding 由来散布図を主図にする発想をやめ、cluster 間配置と cluster 内配置を分離して点を所属島から出さない `semantic island map` を基準線にする判断へ寄せた。[[semantic-island-map-prototype-2026-05-26]]より
- 直近研究で繰り返し出た「pipeline に step を足す」論点を整理した。結論は、step 数そのものではなく、境界・反例・bridge・未解決カードのような新しい成果物責務を first-class にすべきかで判断すること。`label_refinement` は optional 実験、`interpretation_artifacts` は `aggregation` に押し込まず独立成果物として切る方が筋、という整理にした。[[pipeline-step-addition-framing-2026-05-27]]より
- `#629` の掘り下げとして、`fetch_reports.py` はストレージ機能が無かった初期の「deploy 前に API から吸い出して守る」発想の名残で、current main の storage sync / restore 本線とはずれていることを整理した。今後は script 自体を強化するより、migration 専用へ降格し、Azure Blob の read/write を軽く確認する storage health check を deploy safety に据える方が筋がよい。[[fetch-reports-deprecation-and-storage-health-2026-05-26]]より
- その整理に合わせて、旧 `#629` は close し、`#870`（`fetch_reports.py` の役割整理）と `#871`（deploy safety を Blob Storage health check に切り替える）へ分解した。次に実装するなら `#871` を先に進め、その後 `#870` で script / docs の降格を片付ける順がよい。[[github-dev-docs]]より [[fetch-reports-deprecation-and-storage-health-2026-05-26]]より
- `#870` は branch `codex/issue-870-fetch-reports-cleanup` で着手し、`azure-update-deployment` から `tools/scripts/fetch_reports.py` を外し、script 自体も削除した。Blob Storage 本線に合わせて deployment docs を修正し、環境構築後の read/write 確認は既存の `apps/api/scripts/test_storage.py` を使う案内へ寄せた。PR はこれから作成する。[[fetch-reports-deprecation-and-storage-health-2026-05-26]]より
- `work/kouchou-ai/` に残っていた Jigsaw 系実験 artifact と Next.js 生成差分は、branch `codex/remaining-experiment-artifacts-2026-05-29` commit `b56ac9b` として退避した。これにより一次参照 clone は `main@6955202` へ戻して clean にでき、以後の code 観測と実験再開点を分離した。[[remaining-experiment-artifacts-snapshot-2026-05-29]]より

## Open Questions

- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-05-30: Slack のラベル改善議論を source 化し、全体傾向把握と少数重要論点発見では処理・評価が変わるという use-case contract の論点を次回共有項目へ追加
- 2026-05-30: label refinement 実験をそのまま採用せず、sampling / rep args artifact / judge 較正 / UI 表示責務に分けて仕切り直す判断を次回共有項目へ追加
- 2026-05-30: ラベル付け時の sampling が API 経由では最大 30 件、CLI/default では 10 件の random sample で、UI の個別データ表示も代表例選定ではなく配列先頭 10 件であることを次回共有項目へ追加
- 2026-05-30: 実装済み rubric judge で過去出力 4 候補を再評価し、費用と「v0 rubric がまだ甘い」結果を次回共有項目へ追加
- 2026-05-29: `codex/remaining-experiment-wip` に rubric judge 実装を追加し、CLI 接続、CSV/HTML 表示、過去出力を直接再評価できる `--dataset-path`、検証結果を次回共有項目へ追加
- 2026-05-29: Zenn / Ubie のルーブリック評価記事を参考に、ラベル品質 judge を binary criteria + weights に分解する案を次回共有項目へ追加
- 2026-05-29: Issue `#876` (開発者向け導線整理) に対して PR `#883` を作成。`docs/development/developer-quickstart.md` を新規 canonical 入口にし、4 モード分岐と環境変数 / 起動コマンド / 落とし穴を 1 ページに集約。README は概要 + docs 導線に trim
- 2026-05-29: live open issues / PR を再確認し、open issue 121 件のうち `#221` / `#564` の high priority を上位テーマに戻したうえで、tactical next を進行中 PR 着地、Windows guide 境界、ラベル品質実験、Blob health check、viewer UX に整理
- 2026-05-29: `#221` 系を掘り下げ、作成前確認パネルを最初の実装 slice とする考察を [[trial-and-error-burden-reduction-2026-05-29]] に filing back。具体 issue `#884` も起票し、下位 issue へ整理コメントを追加
- 2026-05-29: ラベル品質改善の上位トラッキング issue `#881` と、KJ法的プロンプト比較実験 issue `#882` を起票し、既存 `#869` から辿れるように接続
- 2026-05-29: 新しい可視化アイデアとして、クラスタ x 時刻のヒートマップ issue `#879` と、[8, 64] 分析のマンダラート可視化 issue `#880` を起票
- 2026-05-29: `#877` のコメントを踏まえ、Windows setup guide は単なるトラブルシュート表ではなく、Docker Desktop 標準入口と組織管理端末 / ライセンス制約の非サポート境界を分ける docs issue として扱う整理を追加
- 2026-05-28: `#874` の実装を、実験的 layout 生成を default pipeline へ追加しない方針に合わせて修正し、標準 8 step contract を維持する形で PR branch へ push
- 2026-05-28: Quartz + GitHub Pages project-site の新 Gist を作成し、`wiki/` direct と `wiki/ -> content/` 変換の使い分けを定例共有向けに追記
- 2026-05-28: developer-wiki Pages の subpath link break 再発を受け、Quartz `baseUrl` 方針に戻して `<base>` patch を撤去し、生成物リンク検査を CI に追加した要点を追記
- 2026-05-28: pipeline step 追加判断に open PR `#866` / `#867` / `#874` を反映し、`#874` は named layout artifact として筋がある一方、標準パイプラインへ常時追加する理由は弱いと補正
- 2026-05-28: `#874` の step 追加設計判断を、西尾判断として「実験的機能なので標準パイプラインには入れず、明示有効化される実験用経路に戻す」方針へ修正
- 2026-05-26: draft PR `#873` の checks を確認し、`CodeQL/Analyze (python)` は `github/codeql-action` archive の取得失敗で落ちており、concurrency 修正自体の failure ではないと確認
- 2026-05-26: `#741` 向けに `azure-deploy.yml` へ workflow-level `concurrency` を追加する最小修正を `codex/issue-741-azure-deploy-concurrency` で開始
- 2026-05-26: `#741` の現況を整理し、主因は npm flaky ではなく `main` 近接 push による Azure 更新競合だと読むページ [[issue-741-current-state-2026-05-26]] を追加
- 2026-05-26: `#121` / `#283` の局所修正だけではスマホ利用の根本問題が残ると判断し、mobile 別ビュー方針を検討する issue `#872` を追加。合わせて両 issue の `bug` ラベルも除去
- 2026-05-26: 残存 `[BUG]` title issue 5 件の整理を更新し、`#731` は stale 寄り、`#478` は改善 feature 寄りの低優先先として `bug` ラベルも除去、`#741` `#283` `#121` は active という判断に寄せた
- 2026-05-26: `analysis-core` の単一 HTML 可視化で、クラスタ内 MST + クラスタ間 centroid MST を重ねる試作を `codex/mst-visualization-prototype` worktree で開始
- 2026-05-26: MST overlay / supervised UMAP / LDA 系の試行では所属と geometry の衝突を解消できず、`LLM grouping` 可視化の主図は cluster-first な `semantic island map` に寄せる判断を [[semantic-island-map-prototype-2026-05-26]] として整理
- 2026-05-27: pipeline step 追加案を、step 数ではなく成果物責務で判断する整理として [[pipeline-step-addition-framing-2026-05-27]] に filing back
- 2026-05-26: `fetch_reports.py` を current storage 本線とのズレとして整理し、deploy 前バックアップ常設より storage health check 置換が筋だという analysis を追加
- 2026-05-26: 旧 issue `#629` を close し、`#870` / `#871` に整理し直した
- 2026-05-29: `#870` 向けに `fetch_reports.py` を削除し、`azure-update-deployment` と Azure Blob Storage ドキュメントを Blob sync / `test_storage.py` 前提へ更新
- 2026-05-29: `work/kouchou-ai/` の dirty 実験 artifact を branch `codex/remaining-experiment-artifacts-2026-05-29@b56ac9b` へ退避し、常用 clone を `main@6955202` の clean 状態へ復帰
- 2026-05-26: open PR review コメント対応として、`#867` `codex/reuse-from-outputs` で reuse seed 判定を source run の `completed_jobs` 基準へ修正し、seeded params も current config ではなく source params を保持するよう直した
- 2026-05-26: open PR review コメント対応として、`#866` `codex/llm-grouping-pr` で `analysis_mode` の未知値 validation、prompt 変更の dependency 反映、legacy embeddings 読み込み時の安全化、`assignment_batch_size<=0` 時の batching 修正を入れた
- 2026-05-26: open PR review コメント対応として、`#863` `codex/issue-731-windows-setup-powershell` で API key 改行エラーの日本語化、`docker compose` を `$PSScriptRoot` で実行する修正、非対話失敗時の compose exit code 保持を追加した
