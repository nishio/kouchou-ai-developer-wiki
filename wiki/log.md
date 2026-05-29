# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-05-29 18:06] filing-back | 残 Issue の優先順を live state で組み直し

- 2026-05-29 18:04 JST 時点の live GitHub state を確認し、`#873` merge により `#741` は close 済み、`#584` / `#629` は open ではなく、`#866` / `#867` / `#868` は merge 済みであることを反映
- 新規 analysis [[remaining-issue-priority-2026-05-29]] を追加し、優先順を (1) `#883 -> #876` と `#863 -> #731` の進行中 PR 着地、(2) `#877` Windows guide 境界、(3) `#881` / `#882` / `#869` ラベル品質実験、(4) `#871` Blob health check、(5) `#872` / `#493` viewer UX に整理
- 新しい可視化案 `#879` / `#880` や大型 feature は、導入・品質・運用安全性の bottleneck を先に減らした後でよいと位置づけた

## [2026-05-29 18:05] filing-back | Issue #876 開発者向け導線を利用モード別に整理 (PR #883)

- `docs/development/developer-quickstart.md` を新規追加し、Docker Compose / dummy-server frontend dev / native (apps/api・apps/admin) / CLI (analysis-core) の 4 モードを「最初の 1 ページ」で判断できる canonical 入口にした。各モードに必要な環境変数・起動コマンド・確認 URL・落とし穴 (env file 置き場所、Docker rebuild trigger、analysis-core editable install) を集約
- `README.md` を 240 行 → 92 行へ trim し、長い setup 説明はドキュメントサイトに集約。`docs/index.md` / `docs/getting-started/quickstart.md` / `mkdocs.yml` を新ページに合わせて整理（重複削除、nav 追加、Mode 別 anchor を `{#mode-1-docker-compose}` 等で固定し strict build pass）
- branch `codex/issue-876-developer-quickstart` で PR #883 を開いた。次は CI と review コメント待ち

## [2026-05-29 16:42] filing-back | FPS for labeling は 2025-06-18 にも提案されて 11 ヶ月保留だった

- `raw/meeting_minutes.txt:5169-5170` (2025-06-18 定例) に、tokoroten「ラベリングのためには、ランダムサンプリングではなくて、Farthest Point Sampling を使った方がよさそう」、nishio「アルゴリズム的には良い、計算量がどうかは未確認」というやり取りがあり、約 11 ヶ月実装されないままだった
- 今回 tokoroten が Slack で「Farestなんたらサンプリングで全体のサンプルを包括してタイトルをつけるってはいってるんだっけ」と書いたのは、自分の過去提案を思い出していたもの。今日の nishio「全件渡し」提案は、**過去に gating question として残っていた『FPS の計算量未確認』を、FPS を実装する前に sampling 自体の必要性を問うルートで回避する**構図になっている
- [[label-coverage-policy-2026-05-29]] の Updates に history を 1 段落追記。実装コスト未確認のまま放置されてきたアイデアを別角度から前進させた事例として記録

## [2026-05-29 16:18] filing-back | sampling 改善は「全件渡し → ダメなら減らす」順で

- 前 entry の「sampling 戦略を `random → max coverage / FPS / k-medoids` に切り替える」という方針について、nishio から「ラベリングは extraction に比べてコストが小さいことが既知なので、まず `sampling_num` 無効化で全件渡して試す方が先」という指摘
- [[label-coverage-policy-2026-05-29]] の Updates に、実験順序を (1) sampling_num 無効化で全件、(2) ダメなら max coverage / FPS / k-medoids、(3) tokoroten 案の emb 類似度総和は並行、と整理し直して追記。複雑なアルゴリズム選択より「上流 sampling が本当にボトルネックか」を最小コストで確認するのが先

## [2026-05-29 16:05] filing-back | ラベル設計の人間判断と上流 sampling 制約を集約

- Claude judge 後の 3 論点に Slack で人間判断が出たので [[label-coverage-policy-2026-05-29]] に集約: (1) ラベルは「目次」ではなく「要約」、欠落より冗長を取る (tokoroten: 「カテゴリ外が含まれてるほうが気持ち悪い」)、(2) 1 キーワード完全包括は不可能なので greedy max-coverage で上位 2〜3 軸まで「AとB」、(3) 口語 register は post-processing で吸収可能で優先度低
- tokoroten が指摘した上流 sampling の問題をコードで確認: `hierarchical_initial_labelling` `merge_labelling` とも `sampling_num` デフォルト **10** (tokoroten 発言の 30 は誤りだが本質は正しい)、`polars.DataFrame.sample(n=...)` で完全ランダム → 大規模クラスタほどラベルが「実体」ではなく「ランダム 10 件」に引っ張られる。refinement の入力強化より上流 sampling 戦略 (max coverage / FPS / k-medoids) の見直しが本質
- アルゴリズム候補として tokoroten 案 (タイトル候補 emb × 各要素 emb の cos 類似度総和最大化) と nishio 案 3 (候補を UI で人間に選ばせる) を記録。今回のループ (GPT judge → Markdown export → Claude judge → 論点 → 人間判断 → コード確認) が分業として機能した lesson も同 page に追記
- [[label-refinement-input-scope-2026-05-29]] の Updates に新方針へのリンクを追加し、[[meeting-report-draft]] にも次回定例向け要点を保守した

## [2026-05-29 15:42] filing-back | label_refinement step が rep args を入力に取らない設計を確認

- Claude judge による bundle 検査で、4 mode (`none / setwise / contrast / balanced`) すべてが上流の誤ラベル (cluster 3 = 倫理 args なのに `公共安全`、cluster 5 = 業務効率 args なのに `顧客体験`) を保存していたので `hierarchical_label_refinement.py` の `_build_cluster_section` を読み、refinement LLM に渡しているのが `current_label / current_description / size / children` だけで、**rep args は一切渡していない**ことを確認
- 新規 analysis [[label-refinement-input-scope-2026-05-29]] を追加し、これが「polish only」スコープの仕様通りの挙動であること、書き換え権限はあるのに中身に照らす材料は無いという構造が「整った嘘」リスクになること、default-on 昇格時には rep args 追加か上流品質 gate が前提になることを記録
- 当面 `experimental default-off` で main 同梱する判断には影響しないが、refinement の責務範囲を product 判断として明示しておく必要がある

## [2026-05-29 13:31] filing-back | Issue #877 の Windows setup guide 境界を整理

- 新規 source [[issue-877-windows-setup-guide-scope-2026-05-29]] と [[docker-desktop-license-2026-05-29]] を追加し、`#877` 本文・コメント・current main docs・関連 `#863` の状態・Docker Desktop 公式ライセンス注意を整理
- 新規 analysis [[issue-877-windows-setup-guide-scope]] を追加し、短期は Docker Desktop が使える Windows 10/11 を標準入口にし、Docker Desktop / WSL2 が組織ポリシーで使えない環境は beginner guide の対象外または別上級者ルートへ切る判断を記録
- [[meeting-report-draft]] に、次回定例で共有する Windows setup support boundary の要点を追記

## [2026-05-29 03:02] filing-back | dirty 実験 clone を snapshot branch へ退避して clean main に戻した

- `work/kouchou-ai/` の dirty 状態から、Jigsaw 系実験の入力・config・出力 artifact と Next.js 生成差分を branch `codex/remaining-experiment-artifacts-2026-05-29`、commit `b56ac9b` として push
- 新規 source [[remaining-experiment-artifacts-snapshot-2026-05-29]] を追加し、何を退避したか、なぜ `work/kouchou-ai/` を dirty のまま残さないか、実験再開時の branch を記録した
- 退避後は `work/kouchou-ai/` を `main` へ戻して `origin/main@6955202` まで fast-forward し、developer-wiki から参照する一次 clone を clean 状態へ復帰させた

## [2026-05-29 03:00] filing-back | niizuma-thread-algorithm-critique の違和感マーカー 2 件を反映

- annotation-0013 を受け、3-artifact 列挙の直前に「ここでの artifact は『広聴AI が返す出力物』の意で、前述の『2D 上の配置アーティファクト』の『歪み』とは別語義」と注を追加し、同一ページ内で artifact が二義的に使われる落とし穴を明示した
- annotation-0014 を受け、Open Question「supervised UMAP は短期互換案として十分か」を Open Questions から外し、`work/kouchou-ai-mst-visualization-prototype/` で実験否定済みであることを 2026-05-29 Updates として記録（詳細は [[semantic-island-map-prototype-2026-05-26]] を参照）

## [2026-05-28 17:41] filing-back | `#874` を標準 8 step contract 維持へ修正

- `codex/mst-visualization-prototype` に commit `51a7c77` を push し、`hierarchical_layout_generation` を標準 workflow / specs / orchestrator / config defaults / standard step exports から外した
- layout 生成 step と `layouts` 対応 visualization は実験コードとして残しつつ、default では走らない形にした
- 手元では Ruff と analysis-core tests `184 passed` を確認し、GitHub Actions でも Ruff / Pytest / Server Tests / CodeQL は pass、CodeRabbit は review in progress

## [2026-05-28 13:25] filing-back | Quartz + GitHub Pages project-site の新 Gist を作成

- Scrapbox から辿った旧 Gist の `wiki/ -> content/` 変換方式と、この repo の `wiki/` direct build 方式を分けて整理した
- 新 Gist `https://gist.github.com/nishio/35d604f23a39aca369ac74db8b65b655` を public で作成し、Quartz `baseUrl`、`<base>` patch 回避、生成物リンク検査、GitHub Actions の `fetch-depth: 0` をまとめた
- [[wiki-pages-tooling-observation-2026-05-21]] と [[wiki-pages-publishing-stack]] に、方式選択の判断と新 Gist への導線を追記した

## [2026-05-28 12:38] filing-back | developer-wiki Pages の subpath link check を追加

- Quartz は GitHub Pages project-site hosting を `baseUrl` で扱えるため、root 専用 `<base>` patch は撤去し、`Head.tsx` を upstream 相当へ戻した
- `scripts/check_pages_links.py` を追加し、build 後の `public/` 全 HTML について内部リンク・asset・`fetch()` が `/kouchou-ai-developer-wiki/` 配下の存在する path に解決されることを検査するようにした
- [[wiki-pages-tooling-observation-2026-05-21]] と [[wiki-pages-publishing-stack]] に、subpath 問題は HTML patch ではなく Quartz `baseUrl` + 生成物検査で守る方針として追記した

## [2026-05-28 12:33] filing-back | `#874` は実験的機能なので標準パイプラインに追加しない判断へ修正

- [[pipeline-step-default-policy-decision-2026-05-28]] を追加し、`#874` の semantic island layout 生成は現時点では標準パイプラインに追加せず、明示有効化される実験用経路として扱う判断にした
- [[pipeline-step-addition-framing-2026-05-27]] と [[meeting-report-draft]] も、`標準 9 step 化を検討する` ではなく `8 steps` 固定テストを標準パイプラインの gate として維持する整理へ補正した
- 以前のメンテナー議論用 brief は判断ページへ置き換え、貼り付け用文面は削除した

## [2026-05-28 10:54] filing-back | pipeline step 追加設計のメンテナー議論用 brief を追加

- 新規 analysis を追加し、当初は `#874` の CI failure を「`8 steps` 固定テストを修正して標準パイプラインへの step 追加を許容するか」という意思決定として整理した
- その後の判断で、この brief は [[pipeline-step-default-policy-decision-2026-05-28]] に置き換えた。結論は、実験的な semantic island layout 生成を標準パイプラインに追加しない、である
- [[pipeline-step-addition-framing-2026-05-27]] と [[meeting-report-draft]] から導線を張った

## [2026-05-28 00:08] filing-back | pipeline step 追加判断に open PR `#866` / `#867` / `#874` を反映

- 新規 source [[open-pr-pipeline-step-observation-2026-05-28]] を追加し、2026-05-28 時点の open PR 6 本のうち、step 追加判断に関係する `#866` LLM grouping、`#867` reuse-from、`#874` semantic island layout を整理した
- [[pipeline-step-addition-framing-2026-05-27]] に open PR 節を追記し、`#866` は new mode を workflow として切る良い例、`#867` は downstream step 比較の基盤、`#874` は named layout という表示 artifact の first-class 化として筋があるが CI failure と default 9 step 化の整理が必要、と補正した
- `#874` の失敗は Ruff の import / `np` annotation と、`tests/test_orchestration.py` などに残る `8 steps` 固定期待が主因だと確認した

## [2026-05-27 15:26] filing-back | pipeline step 追加案を成果物責務で判断する整理を追加

- 新規 analysis [[pipeline-step-addition-framing-2026-05-27]] を追加し、直近研究で繰り返し出た step 追加案を「step 数」ではなく「新しい成果物責務を first-class にする必要があるか」で判断する方針として整理した
- `label_refinement` は default complexity として見せない optional 実験、境界・反例・bridge・未解決カードは `aggregation` に押し込まず `interpretation_artifacts` として切るのが筋、と結論づけた
- `work/kouchou-ai/` は dirty な `codex/remaining-experiment-wip@47008bc` だったため破壊せず、`origin/main@e5ed743` と WIP の差を分けて扱った

## [2026-05-26 22:23] filing-back | `LLM grouping` 可視化は semantic island map を主図候補にする整理を追加

- `work/kouchou-ai-mst-visualization-prototype/` で 422 argument / 8 clusters の可視化を、MST overlay, supervised UMAP, semi-supervised UMAP, LDA, centroid-MDS まで比較し、embedding 由来散布図を主図にすると「離れすぎ」か「混ざりすぎ」のどちらかに寄りやすいと整理した
- 新規 analysis [[semantic-island-map-prototype-2026-05-26]] を追加し、cluster 間配置と cluster 内配置を分離して点を所属島から出さない `semantic island map` を、`LLM grouping` 向け cluster-first view の基準線として記録した
- [[meeting-report-draft]] も、MST 試作の途中経過ではなく「最終的にどの方向を採るか」が読める書き方へ更新した

## [2026-05-26 20:01] github-ci | draft PR `#873` の checks を確認し、失敗は CodeQL action 取得エラーだと切り分け

- `gh pr checks 873 --watch` で draft PR `#873` の checks を確認し、`Analyze (javascript)` は pass、`CodeRabbit` は skipped、`CodeQL/Analyze (python)` だけが fail していることを確認
- failed log を見ると、原因は `github/codeql-action@v3` archive の取得失敗 (`An action could not be found at the URI ...`) であり、今回の `.github/workflows/azure-deploy.yml` 修正内容による failure ではなかった
- [[meeting-report-draft]] にも「PR #873 の check failure は CodeQL infrastructure 側で、concurrency 修正自体の失敗ではない」と追記

## [2026-05-26 19:56] filing-back | `#741` 向けに Azure deploy の workflow concurrency を追加

- issue `#741` の assignee を確認して `nishio` を assign し、dirty な `work/kouchou-ai/` は触らず `origin/main` から clean worktree `work/kouchou-ai-issue-741/` を作成
- branch `codex/issue-741-azure-deploy-concurrency` で `.github/workflows/azure-deploy.yml` に `concurrency: group: azure-deploy-${{ github.ref }}, cancel-in-progress: false` を追加し、main 向け deploy を 1 本ずつ順番待ちさせる最小修正を入れた
- 直近 failure の主因が `ContainerAppOperationInProgress` だったため、まずは npm retry ではなく workflow-level serialization を優先する判断として [[issue-741-current-state-2026-05-26]] と整合させた

## [2026-05-26 19:51] filing-back | `#741` の現況を整理し、主因を Azure 更新競合へ読み替え

- 新規 analysis [[issue-741-current-state-2026-05-26]] を追加し、`Azure Deployment` の recent runs を再読した結果、2026-05-21 の連続 failure は repo 再編直後の build-context / admin build breakage で、その後の main では解消済みだと整理
- 直近の実質的な failure は 2026-05-22 `run 26270671888` の `ContainerAppOperationInProgress` で、同時刻の別 success run とぶつかった Azure Container Apps 更新競合だと読んだ
- これにより `#741` は「npm flaky」より「workflow concurrency / Azure update retry」の問題として扱う方が筋だと判断し、[[meeting-report-draft]] にも反映した

## [2026-05-26 19:45] github-triage | `#121` と `#283` から `bug` ラベルを外し、`#872` の参考課題へ寄せた

- GitHub 上で `#121 [BUG] 縦長画面での散布図の表示がおかしい` と `#283 [BUG] ScatterChartの全画面表示で要約文が「全画面終了」ボタンの後ろに隠れないようにする処理が不安定` から `bug` ラベルを除去
- 上位 issue `#872` が「スマホでは別ビューを提供する方針を検討する」入口になったため、両 issue は緊急 bug ではなく mobile/scatter UX の参考課題として扱う方針へ揃えた
- [[remaining-bug-issues-2026-05-26]] と [[meeting-report-draft]] も、`#741` だけが `bug` ラベルを保ち、`#121` `#283` `#478` は `[BUG]` title は残るが label は外れた状態だと分かるよう更新した

## [2026-05-26 19:43] filing-back | スマホ向けに散布図と別ビューを検討する issue `#872` を追加

- GitHub 上で新規 issue `#872 [FEATURE] スマホ環境では散布図と別ビューを提供する方針を検討する` を作成
- `#121` の「portrait では tap tooltip が plot 幅の大半を覆う」観測と、`#283` の「mobile-sized viewport でも hover overlap が起こりうる」観測を背景に、responsive 調整だけでなく mobile 専用ビュー方針を明示的に検討する入口として切り出した
- 関連 issue は `#121` `#283` `#266` `#52` を本文で束ね、静的画像 / クラスタ一覧 / 簡略図などを候補として列挙した

## [2026-05-26 19:33] filing-back | `#121` を実スマホ想定で再観測し、portrait では tap tooltip の広さが主要な使いづらさだと整理

- Browser で `http://localhost:3000/example` の fullscreen 散布図を `390x844` / `360x640` / `844x390` / `1280x720` で比較し、portrait では annotation は bounds 内に収まるが、249px 幅ラベルが画面に対して相対的に大きく、散布図の余白がかなり圧迫されることを確認
- 実スマホ寄りの tap 相当操作では tooltip は `#283` のようにボタン裏へ潜るのではなく button 下へ出る一方、`390x844` では tooltip 幅が `363-366px` と plot 幅 `390px` の大半を覆い、散布図を読み続けにくい
- [[remaining-bug-issues-2026-05-26]] の `#121` 節に、`#283` の hover 問題とは別に「縦長では tap tooltip が広すぎる」という実スマホ寄りの使いづらさを追記

## [2026-05-26 19:29] filing-back | `#283` の viewport 別再確認で、一般的なスマホ幅でも overlap が出ることを確認

- Browser で fullscreen 散布図の hover overlap を viewport 別に再確認し、`390x844` で 4 件、`393x852` で 5 件、`412x915` で 3 件、`430x932` では 0 件、`360x640` で 8 件、`360x520` で 7 件を観測
- これにより `#283` は「かなり極端に小さい viewport だけ」の問題ではなく、一般的なスマホ幅相当でも hover 条件次第で再現しうると判断した。ただし観測は touch ではなく mobile-sized viewport 上の desktop hover である点を明記した

## [2026-05-26 19:27] filing-back | `#283` を browser で再観測し、極小 viewport で hover overlap を再現

- `work/kouchou-ai/` で `public-viewer` と `dummy-server` を起動し、Browser で `http://localhost:3000/example` を fullscreen 表示して `#283` の再現条件を再観測
- viewport `420x720` では hover がボタン直下に寄る程度だったが、`360x520` まで縮めると `fullScreenButtons` と hover text が重なる座標を少なくとも 7 点確認し、issue 本文の「極小サイズで不安定」は current main でも再現すると判断
- [[remaining-bug-issues-2026-05-26]] の `#283` 節 Updates に、button rect と overlap 件数を含む観測結果を追記

## [2026-05-26 19:19] github-triage | `#478` から `bug` ラベルを外し、改善 feature 寄りの扱いへ揃えた

- GitHub 上で `#478 [BUG] Clientの意見の説明が禁則処理ができていない` から `bug` ラベルを除去
- [[remaining-bug-issues-2026-05-26]] と [[meeting-report-draft]] も更新し、`#478` は title 上の `[BUG]` は残るが triage 上は改善 feature 寄りの低優先先として扱う状態に揃えた

## [2026-05-26 19:17] filing-back | `#478` を bug というより改善 feature 寄りの低優先先として位置づけ直し

- [[remaining-bug-issues-2026-05-26]] を更新し、`#478` は原因コードこそ current main に残るものの、解法が禁則処理実装か HTML tooltip 再設計に限られ、コストに対する効果が小さいため、bug というより改善 feature 寄りの低優先先として扱う判断を追記
- [[meeting-report-draft]] にも同じ判断を反映し、残存 `[BUG]` のうち積極的に詰める対象から `#478` を外し、`#741` `#283` `#121` を相対的に上位へ置く形にした

## [2026-05-26 18:37] filing-back | 残っている `[BUG]` issue を live state と current main で棚卸し

- 新規 analysis [[remaining-bug-issues-2026-05-26]] を追加し、2026-05-26 時点で open の `[BUG]` issue が `#741` `#731` `#478` `#283` `#121` の 5 件であることを整理
- `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` を照合すると、`#478` `#283` `#121` は散布図 UI の未解決課題、`#741` は Azure deploy workflow の flakiness としてまだ active と判断した
- `#731` は current `setup_win.bat` から issue 本文の日本語バッチ行が既に消えており stale 寄りだが、日本語 UX を戻す open PR `#863` が残っているため、close するか PR を進めるかの判断論点として切り出した

## [2026-05-26 15:36] filing-back | 旧 issue `#629` を close し、`fetch_reports` 論点を `#870` / `#871` に再編

- GitHub 上で `#629 [BUG] scripts/fetch_reports.pyでは「限定公開」「非公開」状態のレポートがバックアップできない` を close
- 新規 issue `#870 [REFACTOR] fetch_reports.py を migration / 緊急救済専用へ降格し、通常運用から外す` を作成し、script の役割整理・docs 反映・通常 workflow からの分離を追う形にした
- 新規 issue `#871 [BUG] Azure deploy の safety を fetch_reports 依存から Blob Storage health check に切り替える` を作成し、deploy safety の本線を API scrape ではなく Blob health check に置き換える実装課題として分離した

## [2026-05-26 15:31] filing-back | `fetch_reports.py` を migration 手段として読み直し、storage health check 置換案を整理

- 新規 analysis [[fetch-reports-deprecation-and-storage-health-2026-05-26]] を追加し、`fetch_reports.py` が「ストレージ機能が無かったころの deploy 前バックアップ」の名残であり、current `ReportSyncService` / `initialize_from_storage()` 本線とはずれていることを整理
- `.github/workflows/azure-deploy.yml` が今も deploy 前に `python3 tools/scripts/fetch_reports.py` を叩いている一方、script 自体は `PUBLIC_API_KEY` で public `/reports` を読むだけなので non-public report を救えない、と current contract の破綻点を明記
- 代案として、`fetch_reports.py` を migration / 緊急救済専用へ降格し、通常の deploy safety は Azure Blob の read/write を軽く確認する storage health check に置き換える方が筋だと整理

## [2026-05-26 15:10] filing-back | log を「人間向け 7 日 log.md」と「AI 向け全件 log.txt」に分離、無検出 lint は記録対象外に

- 振り返り対象: `wiki/log.md` 1631 行 / 285 entries のうち lint type が 102 件 (36%) で、内容はすべて「無検出」のため信号対雑音比を悪化させていた。また全 entry が単一ファイルに積み上がる構造で、長期で読みづらくなる前提が無かった
- 設計: `index.md` / `index.txt` 分離と同じパターンを log にも適用。`log.md` = 人間向け直近 7 日 full detail、`log.txt` = AI 向け全件 compact (`<ts>\t<type>\t<title>`)
- 新規スクリプト `scripts/refresh_logs.py` を追加。log.md の現状を parse → 既存 log.txt と merge → log.txt を newest-first で regenerate、続けて log.md を直近 7 日分に trim。`type=lint` の entry は両方から自動除外
- 移行結果: log.md 1631 → 952 行 / 127 entries (直近 7 日, cutoff 2026-05-19 14:30)。log.txt 189 行 / 184 entries (全期間)。lint 102 件と 7 日超過 58 件が log.md から落ちた
- `CLAUDE.md` を更新: 直系ディレクトリ説明、Ingest / Filing-back の手順、Lint セクションの「無検出は記録しない」、新規「### Log メンテ方針」セクション

## [2026-05-26 14:30] filing-back | wiki index を「人間向け curated index.md」と「AI 向け全件 index.txt」に分離

- 振り返り対象: `wiki/index.md` が 172 行・`wiki/log.md` が 1631 行 (285 entries 全部 2026-05、うち lint が 36%) と発散。新規コントリビュータ向けの onboarding 導線が 130 行のフラットカタログに埋もれていた
- ユーザ判断: AI ナビゲーションは Markdown である必要がなく、ファイル名+要約の text file で十分。`index.md`（人間向け curated nav）と `index.txt`（AI 向け全件カタログ）を分離する
- 新規スクリプト `scripts/build_index_txt.py` を追加し、各ページの frontmatter から `<stem>\t<type>\t<path>\t<summary>` を 156 ページ分生成。`wiki/index.txt` は auto-generated として commit する
- `wiki/index.md` を 172 → 47 行に縮小。Concepts (16) / Entities (12) の curated list は残し、Sources (61) / Analyses (66) のフラットリストは削除して `index.txt` ポインタへ集約。onboarding 5 ページ導線も維持
- `scripts/lint_wiki.py` の「index.md 未登録」チェックを「index.txt 未登録」チェックへ切り替え。auto-gen の同期忘れだけを検出する形にして、index.md の curation 自由度を確保
- `CLAUDE.md` に `index.txt` regenerate 手順と meeting-report rotate ルールを追記
- lint 通過: 156 pages、broken link 0、index.txt 未登録 0、frontmatter 不備 0

## [2026-05-26 14:03] ingest | 2026-05-25 定例後の議事録再取得と meeting-report-draft の rotate

- Google Doc export から `raw/meeting_minutes.txt` を再取得し、先頭見出しが `2026/05/25（次回分）` で 7534 行になっていることを確認。今回会は「大リファクタリング完了」「LLM grouping 実験 / ラベル refinement 実験」「Issues 棚卸し」「デジタル庁RAG話題」が主議題
- 議事録内で nishio 本人が developer-wiki について「人間が直接読むには情報多すぎ」「indexが溢れたらthinking effort多めで再構成したらいい」と言及している点をメモ。index/log の情報密度問題は本人認知済み
- `wiki/concepts/meeting-report-draft.md` の旧内容（月曜版・次回向け 12 項目・Updates 47 件）を新規 [[meeting-report-2026-05-25]] へ rotate し、draft 本体は 2026-06-01 向けに空テンプレへ戻した。`## 過去回` セクションから archive を辿れる形にし、Open Question の「snapshot を切るか継続か」は snapshot 方針で解消
- `wiki/index.md` にも archive ページを追加。`scripts/lint_wiki.py` は壊れた wikilink 0 / index 未登録 0 / frontmatter 不備 0 で通過

## [2026-05-25 20:38] filing-back | デジタル庁の条文RAGに関する既存知識の有無を整理

- 新規 analysis [[digital-agency-legal-rag]] を追加し、2026-05-25 時点の `wiki/` と `raw/meeting_minutes.txt` には「デジタル庁の条文RAG」を直接説明する整理は無いと記録
- 周辺言及として、一般的な RAG 議論、デジタル庁の中で関連したことをやっている人がいるという伝聞、`eGov` パブコメ連携案、回答案下書きへの RAG 活用案があることを要約

## [2026-05-25 19:54] filing-back | open のまま残した issue 6 件の判断理由を整理

- 新規 analysis [[issue-triage-open-remnants-2026-05-25]] を追加し、`#79` `#253` `#391` `#477` `#537` `#690` を current `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` で close しなかった理由を issue 本文単位で整理
- `#79` は実行後 cost 表示ではなく事前 cost 見積もり、`#391` は手動接続チェックではなく作成開始時 preflight、`#477` は Azure 実行経路ではなく model UI 不整合が残る点を明記
- `#253` は CLI 用 `report.html` の file URL 対応と Web 静的 export の失敗 UX を分離し、`#537` は OpenRouter provider と無料モデル対応を分離、`#690` は `ts-node-dev` がまだ残るため未実装と整理
- `wiki/index.md` と [[meeting-report-draft]] に導線を追加

## [2026-05-25 19:47] filing-back | bug ラベル open issue を current main 基準で再点検し、stale な 3 件を close

- `bug` ラベルの open issue を current `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` と open PR で棚卸し
- `#666` は古い `requirements-torch.txt` ベース Dockerfile を前提にした Windows build error で、current `apps/api/Dockerfile` とは前提が一致しないためコメント付きで close
- `#584` は `execute_aggregation()` rerun 後も token usage を保持する current 実装と回帰テスト `test_execute_aggregation_runs_monitor_flow_and_preserves_existing_status` を根拠に stale と判断し close
- `#177` は current `Makefile` の `az containerapp update --set-env-vars` で値が引用され、`&` による分断経路が見当たらないため close
- `#629` `#477` `#741` `#478` `#283` `#121` は current main だけでは stale と言えず残し、`#731` `#700` は assignee / 進行中状況を踏まえて触れていない

## [2026-05-25 19:47] filing-back | bug issue 再点検の判断を独立 analysis に整理

- 新規 analysis [[bug-issue-triage-2026-05-25]] を追加し、`bug` ラベル open issue のうち `#666` `#584` `#177` を stale として close した根拠と、`#629` `#477` `#741` `#478` `#283` `#121` を active に残した理由を 1 ページで整理
- 環境起因で stale 化した issue と、current product contract 自体の穴として残る issue を分けて読むべきだという triage 観点を明記

## [2026-05-25 19:24] filing-back | remaining experiment WIP branch と issue #869 を作成

- `work/kouchou-ai/` の dirty 実験差分から、生成 outputs / 実験用 config を除いたコードとテストだけを `codex/remaining-experiment-wip` に WIP snapshot として commit
- branch `codex/remaining-experiment-wip`、commit `47008bc` を push
- label refinement PR 化までの残作業を GitHub issue `#869` `[analysis-core] label refinement PR化までの残作業整理` に記録

## [2026-05-25 19:24] filing-back | Issue #530 の current-state 判断を追加

- 新規 analysis [[issue-530-current-state]] を追加し、2026-05-25 時点の `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` では API 依存が `server/requirements.txt` ではなく `apps/api/pyproject.toml` / `requirements.lock` で管理されていること、Azure 依存も既に入っていることを整理
- `setup_win.bat` の既定 `STORAGE_TYPE=local` と `apps/api/src/config.py` の default を根拠に、issue 本文の「ローカル初回セットアップで Azure 依存が必須」という説明は current 導線とずれると明記
- open PR `#863` を併せて確認し、Windows 導入の current 論点が `requirements.txt` 追加ではなく setup UX / PowerShell 分離に寄っていることも記録

## [2026-05-25 19:22] filing-back | wiki graph 表示調整と main 直接 push 運用を記録

- 新規 source [[wiki-maintenance-observation-2026-05-25]] を追加し、Quartz graph から `index` / `log` を除外した実装、`pnpm build` / wiki lint の検証結果、`pnpm check` が `work/` clone を拾う問題を整理
- [[wiki-pages-publishing-stack]] に graph 表示チューニングの意図を追記し、[[wiki-driven-workflow]] に developer-wiki 更新は PR 経由ではなく `main` 直接 push を基本にする運用を明文化
- [[meeting-report-draft]] に、developer-wiki 側の整備と残る `pnpm check` 課題を定例向け要点として追記

## [2026-05-25 18:54] filing-back | 散布図維持側の nishio スタンスを訂正

- ユーザ本人から「『見た目のインパクトが強くて求める顧客がいる』（特にチームみらい等の宣伝用途）」という表現は不適切と指摘
- 実際の議論は「少なくとも 2026-09 書籍版リリース時点までは温存」「より良い可視化が見つかれば併用→デフォルト切替もあり得る」という時間軸ベースのスタンス
- [[open-decisions]] A1 / [[pipeline]] Open Questions / [[jigsaw-sensemaker-history]] §2 / [[talk-to-the-city]] の 4 箇所を更新
- `raw/meeting_minutes.txt` の line 3689 / 7326 を確認し、議事録には「顧客が割といる」「書籍化進行なども勘案」の両方が含まれていたが、wiki が前者だけを「チームみらい宣伝用途」へ過剰一般化していたことを訂正

## [2026-05-25 18:02] github-ci | draft PR #868 の checks 通過を確認

- `gh pr checks 868 --watch --interval 10` で、Ruff / Pytest / Server Tests / CodeQL / CodeRabbit がすべて pass したことを確認

## [2026-05-25 17:59] filing-back | runtime user API key plumbing を draft PR #868 として切り出し

- `USER_API_KEY` を `analysis-core` の API key validation、`StepContext`、built-in plugin の legacy runtime config、legacy step の LLM 呼び出しへ通す修正を clean worktree `work/kouchou-ai-user-api-key-pr/` で構成
- user API key は `initialization()` の戻り config と status JSON に保存しないよう regression test を追加
- branch `codex/user-api-key-plumbing`、commit `a21bf27` を push し、draft PR `#868` `[codex] 実行時ユーザーAPIキーの受け渡しを直す` を作成
- `packages/analysis-core` で `OPENAI_API_KEY=dummy rye run python -m pytest -q` を実行し、通常テスト `181 passed` を確認

## [2026-05-25 17:23] github-ci | draft PR #867 の checks 通過を確認

- `gh pr checks 867 --watch --interval 10` で、Ruff / Pytest / Server Tests / CodeQL / CodeRabbit がすべて pass したことを確認

## [2026-05-25 17:18] filing-back | reuse-from を draft PR #867 として先に切り出し

- `work/kouchou-ai/` の混在した実験差分から、既存出力を seed して再利用する `--reuse-from` だけを clean worktree `work/kouchou-ai-reuse-from-pr/` に再構成
- LLM grouping / label refinement の実装は含めず、比較実験の土台として先に PR 化する方針にした
- branch `codex/reuse-from-outputs`、commit `977d7eb` を push し、draft PR `#867` `[codex] 既存出力を再利用して再実行できるようにする` を作成
- `packages/analysis-core` で `OPENAI_API_KEY=dummy rye run python -m pytest -q` を実行し、通常テスト `181 passed` を確認

## [2026-05-25 17:09] github-triage | current main で解決済みの open issue を close

- `work/kouchou-ai/` で `origin/main@e5ed743` を fetch 済みとして参照し、open PR は `#863` と `#866` の 2 本であることを確認
- open issue を番号順に見て、merged PR / current code / docs / tests で解決済みと判断できた `#19` `#271` `#281` `#290` `#315` `#333` `#380` `#385` `#396` `#398` `#400` `#456` `#613` `#721` `#799` `#815` を close
- `#79` `#253` `#391` `#477` `#537` `#690` などは、関連実装はあるが issue 本文の要件がまだ残る、または部分実装に留まるため open のまま残した

## [2026-05-25 16:57] filing-back | LLM grouping 最小実装を draft PR #866 として切り出し

- `work/kouchou-ai/` の混在した実験差分から、`analysis_mode=llm_grouping` の workflow / spec / plugin / step / default prompt / tests だけを clean worktree `work/kouchou-ai-llm-grouping-pr/` に再構成
- label refinement 系の step / prompt / 実験 config / outputs は含めず、別 PR に回す方針にした
- branch `codex/llm-grouping-pr`、commit `4f893ab` を push し、draft PR `#866` `[codex] LLM grouping 分析モードを追加` を作成
- `packages/analysis-core` で `rye run python -m pytest -q` を実行し、通常テスト `186 passed` を確認

## [2026-05-25 15:48] ingest | nishio ↔ GPT のブレスト 4 本を source / analysis 化

- `raw/a.txt` `b.txt` `c.txt` `kawakita.md` を以下にリネーム
  - `raw/gpt-umap-clustering-bertopic-deep-research-2026-05-25.txt`
  - `raw/gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25.txt`
  - `raw/gpt-mst-bridge-visualization-brainstorm-2026-05-25.txt`
  - `raw/gpt-kawakita-kj-method-broadlistening-2026-05-25.md`
- 各ブレストに対し source 4 本を追加：[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]]、[[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]]、[[gpt-mst-bridge-visualization-brainstorm-2026-05-25]]、[[gpt-kawakita-kj-method-broadlistening-2026-05-25]]
- 派生 analysis 3 本：[[clustering-deep-research-findings-2026-05-25]]（survey bucket への deep-research 応答整理）、[[graph-visualization-proposal-2026-05-25]]（MST + bridge を niizuma 批判への visualization 側の答えとして読み直し）、[[kj-method-broadlistening-framing-2026-05-25]]（KJ法を product 設計原則として再定義）
- [[clustering-research-survey-plan]] / [[clustering-research-survey-seeds-2026-05-25]] / [[niizuma-thread-algorithm-critique]] / [[tokoroten-spectral-clustering-reading]] / [[broad-listening-book-extractions]] の Updates から新 analysis へ導線を張った
- `index.md` の Sources / Analyses 両方を更新

## [2026-05-25 13:42] filing-back | judge の仕組み説明と Claude / 人間比較 bundle を追加

- ここまでの label quality judge が OpenAI/GPT ベースで、生成側も同系統 LLM を使っている点を明文化し、[[label-judge-mechanism-2026-05-25]] を追加
- `scripts/export_label_judge_bundle.py` を追加し、`[8,40]` の `none / setwise / contrast / balanced` について top-level label, description, size, representative arguments を同一フォーマットで書き出す [[label-refinement-judge-bundle-2026-05-25]] を生成
- [[jigsaw-llm-grouping-experiment]] / [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[meeting-report-draft]] / `index.md` も更新し、次の優先度を「refinement mode 追加」から「judge calibration」へ置き直した

## [2026-05-25 13:19] filing-back | ohki-shingo との公開UI議論を振り返って考察

- 2026-05-23 の [[slack-public-ui-requirements-2026-05-23]] を、2025-12 の方向性議論にあった [[ohki-shingo]] の「ユーザー」「自治体」「材料」「実課題」志向と接続して [[ohki-discussion-reflection-2026-05-25]] に整理
- 散布図互換の技術論ではなく、散布図が公開UIで担っていた説明責務をどう別 UI で満たすか、という読みを filing-back
- [[ohki-shingo]] entity と [[meeting-report-draft]] にも導線を追加

## [2026-05-25 13:18] filing-back | `setwise_refine` の prompt variation を比較

- `contrast`（sibling 差分を前半に出す）と `balanced`（短さより領域保持を優先する）の 2 prompt を追加し、既存 `setwise` と同じ `[8,40]` 構造で比較
- downstream token usage は `setwise 8,767`, `contrast 8,484`, `balanced 8,363`、平均ラベル長は `17.6`, `13.0`, `12.0`
- OpenAI judge の cluster 平均点は `contrast 85.0 > setwise 84.4 > balanced 83.8` で、個別品質の best tradeoff は `contrast` に見えた
- 一方で direct judge は `balanced > setwise > contrast` を返しており、algorithm 的な見出し品質と UI 上の一覧 readability を分けて扱う必要がある、という解釈を [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に追記

## [2026-05-25 13:08] filing-back | BERTopic と日本語 tokenizer の役割も整理

- upstream / fork の `clustering.py` を見直し、`janome` + `CountVectorizer(tokenizer=...)` は spectral / `UMAP` の幾何を変える差分ではなく、BERTopic の topic representation / document info 取得を日本語で成立させるための差分だと整理
- [[tttc-spectral-clustering-code-observation-2026-05-25]] に、fork の本丸差分は clustering 核ではなく BERTopic 周辺の日本語対応だという点と、current `analysis-core` では BERTopic / CountVectorizer 自体が消えているため main line では使われていない点を追記
- [[meeting-report-draft]] にも、TTTC 系 tokenizer 差分は current clustering path では歴史的差分になっていることを反映

## [2026-05-25 13:05] filing-back | label refinement 3 mode の初回比較を実施

- 同じ `[8,40]` cluster 構造を固定し、`none / setwise_refine / setwise_refine_short` の 3 条件を `jigsaw_sample_comments_400_hierarchical_8_40_refine_*.json` で実行
- downstream cost は `none = 1,864 tokens / 7.5s`, `setwise_refine = 8,767 tokens / 23.8s`, `setwise_refine_short = 8,754 tokens / 18.8s`、平均ラベル長は `24.2 -> 17.6 -> 12.8` へ短縮
- OpenAI judge の cluster 平均点は `none 87.0 > short 85.4 > setwise 84.1` だった一方、ラベル集合全体の direct judge は `setwise_refine` を 1 位、`none` を 2 位、`short` を 3 位と判定
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、「個別クラスタの代表性」と「一覧で見た時の readability」は別軸で、top-level label set の最適化では `setwise_refine` が有望だという知見を追記

## [2026-05-25 13:02] filing-back | TTTC fork 差分の本丸は日本語 tokenization だと追記

- upstream `talk-to-the-city-reports` と fork `shugiinsenyo2024-tttc` の `scatter/pipeline/steps/clustering.py` を比較し、`UMAP -> SpectralClustering` や `n_neighbors <= 10` は共通である一方、目立つ差分は `janome` と `CountVectorizer(tokenizer=tokenize_japanese)` の導入だと確認
- [[tttc-spectral-clustering-code-observation-2026-05-25]] に、fork 側の変更は clustering 核より BERTopic の語彙処理を日本語向けに寄せたもの、という読みを追記
- [[meeting-report-draft]] にも、current `analysis-core` では BERTopic / CountVectorizer 自体が消えているため、この tokenizer 差分は main line では生きていない点を補足

## [2026-05-25 12:56] filing-back | nasuka 考察を現在の開発タスクへ落とし込み

- [[nasuka-statements-retrospective-2026-05-25]] に「今の開発への落とし込み」を追加
- 失敗例収集 loop、再利用と手動編集、公開範囲、政党 fork から upstream へ戻す基準、facilitation role と domain contributor の分離を整理
- [[meeting-report-draft]] に、次回定例で共有できる 2 行要約として追記

## [2026-05-25 12:52] filing-back | nasuka の過去発言を振り返って考察

- Google Doc export から `raw/meeting_minutes.txt` を再取得し、先頭見出しが `2026/05/25（次回分）` であることを確認
- `meeting-minutes` 内の `nasuka` / `sumino` / `角野` 発言を読み、運用基盤、実利用、分析品質、governance、チームみらい fork の観点で整理
- 新規 analysis [[nasuka-statements-retrospective-2026-05-25]] を追加し、[[nasuka]] entity と `index.md` から導線を張った

## [2026-05-25 12:50] filing-back | TTTC fork / upstream repo 内の spectral 意図説明の有無も確認

- `/tmp/shugiinsenyo2024-tttc` と `/tmp/talk-to-the-city-reports` を見比べ、`README`、`git log --grep='spectral|UMAP|cluster|neighbor|BERTopic|HDBSCAN'`、`git blame`、GitHub issues 一覧を確認
- fork 側 `clustering.py` は commit `dc13082` の `first commit`、upstream 側の対応実装は commit `0debc1a` の `first open-source commit` 由来で、どちらにも spectral / `n_neighbors` の explicit rationale はほぼ残っていないことを確認
- [[tttc-spectral-clustering-code-observation-2026-05-25]] に、「fork / upstream の表層履歴から読めるのは実装形までで、意図はなお未確定」という点を追記

## [2026-05-25 12:44] filing-back | tokoroten とのアルゴリズム議論を振り返り

- 新規 analysis [[tokoroten-algorithm-discussion-retrospective]] を追加し、tokoroten との議論を「手法比較」ではなく「散布図 product / 深い分析 / 説明責務 / 運用ワークフローの分離」として整理
- [[kouchou-ai-direction-2025-12-06]] / [[kouchou-ai-direction-2-2025-12-13]] / [[slack-tokoroten-spectral-clustering-notes-2026-q1]] / [[slack-niizuma-umap-kmeans-thread-2026-03-18]] / [[jigsaw-llm-grouping-experiment-output-2026-05-25]] を突き合わせ、stable v4 と次世代 analysis mode を分ける読みを追記
- `wiki/index.md` / [[tokoroten]] / [[meeting-report-draft]] に導線を追加

## [2026-05-25 12:43] filing-back | clustering 議論の Deep Research 前に survey 計画を整理

- 新規 source [[clustering-research-survey-seeds-2026-05-25]] を追加し、`UMAP -> clustering`、次元圧縮の caution、spectral clustering、BERTopic、可視化と分析の分離、評価軸の 6 棚に survey bucket を分解
- 新規 analysis [[clustering-research-survey-plan]] を追加し、新妻 thread と tokoroten spectral 議論を外部研究で検証する時の優先読書順と、次の実作業候補を整理
- `wiki/index.md` と [[meeting-report-draft]] にも、TTTC 意図掘り前に survey の棚を切ったことを反映

## [2026-05-25 12:39] filing-back | 新妻 thread の設計含意を追記

- [[niizuma-thread-algorithm-critique]] に、`HDBSCAN` / `spherical k-means` への単純置換ではなく、分析 artifact / 表示 artifact / 説明 artifact を分けるべきという考察を追加
- 後続の [[jigsaw-llm-grouping-experiment-output-2026-05-25]] も根拠に加え、意味分類の品質と scatter 上の自然さは別指標として評価すべきだと整理
- [[meeting-report-draft]] にも、次回定例で読み上げやすい短い要点を追記

## [2026-05-25 12:39] filing-back | label refinement 実験用の新 step を `analysis-core` に追加

- `merge_labelling` の後ろで top-level label set をまとめて見直す `hierarchical_label_refinement` step / plugin を追加し、`mode = none / setwise_refine / setwise_refine_short` を config で切り替えられるようにした
- workflow, compat config, rerun specs も更新し、以後は clustering を固定したまま top-level label / description の改善案だけを比較実験できる土台を整備
- `packages/analysis-core` では関連 test を追加・更新し、`rye run pytest tests/test_label_refinement.py tests/test_prompts.py tests/test_compat.py tests/test_imports.py tests/test_steps_paths.py tests/test_cli.py tests/test_integration.py tests/test_llm_grouping.py tests/test_pipeline_paths_integration.py tests/test_orchestration.py -q` で `123 passed`
- [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、この実装を「aggregation 改善のための新しい実験系」として追記

## [2026-05-25 12:15] filing-back | TTTC spectral の Slack 解釈を historical code で検証

- `ntv-experiment-public/shugiinsenyo2024-tttc@5e0a439` の `scatter/pipeline/steps/clustering.py` と、`digitaldemocracy2030/kouchou-ai@53f1209` の `hierarchical_clustering.py` を一次参照で確認
- 新規 source [[tttc-spectral-clustering-code-observation-2026-05-25]] を追加し、TTTC が `UMAP` 後に `SpectralClustering` を掛け、`n_neighbors` 上限が 10、最終 `cluster-id` も spectral ラベルであることを記録
- [[slack-tokoroten-spectral-clustering-notes-2026-q1]] と [[tokoroten-spectral-clustering-reading]] を更新し、「実装形までは確認済み」「紐状構造を作って切るのが方針、は未確定」という線引きを明示

## [2026-05-25 12:15] filing-back | tokoroten の spectral clustering メモを独立ページ化

- `oss_weekly_reporter` の `2026-02-11_to_2026-02-18` / `2026-03-04_to_2026-03-11` にある tokoroten の spectral clustering メモを再読し、近接文脈として `#2_開発_広聴ai` 2026-02-04 の mode 切替整理も併読
- 新規 source [[slack-tokoroten-spectral-clustering-notes-2026-q1]] を追加し、「TTTC は小さめ `n_neighbors` で紐状分離を作り、それを `SpectralClustering` で切る」という読みを記録
- 新規 analysis [[tokoroten-spectral-clustering-reading]] を追加し、spectral clustering を高次元での正しい代替というより scatter-first な cut 手法として理解していた点を整理
- [[tokoroten]] entity / `wiki/index.md` / [[meeting-report-draft]] にも導線を追加

## [2026-05-25 12:11] filing-back | 新妻 thread を独立ページ化し、アルゴリズム論点を塊で整理

- `oss_weekly_reporter` の `2026-03-18_to_2026-03-25/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` から、新妻氏参加の thread を切り出して再読
- 新規 source [[slack-niizuma-umap-kmeans-thread-2026-03-18]] を追加し、論点を「`UMAP` 後 `k-means` 批判」「前段クラスタリング / `HDBSCAN` 案」「散布図とのトレードオフ」「LLM 直分類と説明責務」の 4 塊に整理
- 新規 analysis [[niizuma-thread-algorithm-critique]] を追加し、この thread の本質を「幾何の自然さ・散布図の受容性・外部説明責務の衝突」として要約
- `wiki/index.md` に新規 source / analysis を登録し、[[meeting-report-draft]] にも次回定例向けの短いメモを追記

## [2026-05-25 12:02] filing-back | 実験の product 含意と aggregation 改善仮説を追記

- `K=8` では LLM grouping が強く、`K=20` では従来 hierarchical が強いという結果から、LLM grouping は粗い俯瞰向き、従来 hierarchical は細粒度分析向きという役割分担の仮説を整理
- `[8,40]` で `一貫性 / 網羅性` が上がり `区別性` が少し下がったことを踏まえ、現状の改善ボトルネックは clustering 本体より top-level ラベル同士の差別化かもしれない、という読みを追加
- 次の改善焦点として、`aggregation` step で「短い見出し」「sibling との差分強調」「粒度の揃い」「重複語の回避」を促す prompt / algorithm 変更案を [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に追記

## [2026-05-25 11:49] filing-back | `LLM grouping K=8` と `hierarchical [8,40] level1` を直接 judge

- `~/kouchou-ai/.env` の OpenAI API key を使い、`outputs/jigsaw_sample_comments_400_config/` と `outputs/jigsaw_sample_comments_400_hierarchical_8_40/` の top-level labels を同じ judge で比較
- 結果は `work/kouchou-ai/packages/analysis-core/outputs/label_quality_judge_k8_llm_vs_hierarchical_8_40_2026-05-25.json` に保存し、cluster 平均点は `LLM grouping K=8 = 85.6`, `hierarchical [8,40] level1 = 88.0`
- 一方でラベル集合全体の direct judge は `llm_grouping_k8` 勝ちで、`[8,40]` は代表性に強いが見出しが長くなりやすく、readability では LLM grouping に分があると分かった
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、代表性と readability を別軸で持つべきことと、hierarchical 集約に短いラベルを後付けする折衷案の次ステップを追記

## [2026-05-25 11:36] filing-back | 多層 hierarchical `[8, 40]` の集約効果を確認

- `jigsaw_sample_comments_400_hierarchical_8_40.json` を追加し、同じ 422 argument / embedding を `--reuse-from sample_comments_400_upstream_seed` で再利用して `[8, 40]` を実行
- `level 1 = 8` の geometry は単層 `K=8` と大差なかったが、top-level label は `公共サービスと都市インフラ`, `顧客体験と業務効率化`, `医療・教育・生活の質向上` のように、より集約的な意味づけへ変化
- OpenAI judge で単層 `K=8` と比較すると、`[8,40] level1` は平均 `82.1`、単層 `K=8` は `79.4` で、集約後の 8 layer の方が一貫性・網羅性で上回った
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、「差が出るのは 40 layer そのものより、そこから作る 8 layer の意味構成」という知見を追記

## [2026-05-25 10:34] filing-back | `K=20` でも同一 args 比較を実施

- `jigsaw_sample_comments_400_k20_llm.json` / `jigsaw_sample_comments_400_k20_hierarchical.json` を追加し、`--reuse-from sample_comments_400_upstream_seed` で同じ 422 argument / embedding を再利用して `K=20` 比較を実施
- `LLM grouping K20` は `52,088 tokens / 152s`、`hierarchical K20` は `17,387 tokens / 59s` で、geometry 指標は引き続き従来法が優位
- OpenAI judge では cluster 平均点が `LLM K20 83.3`, `hierarchical K20 85.0` で、`K=8` と逆転した。一方でラベル集合をまとめて見た direct judge は `llm_grouping_k20` 勝ちを返しており、judge 粒度によるぶれも観測
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に、`K` と judge granularity も主要変数として扱うべきという解釈を追記

## [2026-05-25 10:06] filing-back | 費用対効果の解釈を実験記録へ追記

- same-args downstream 比較で `LLM grouping` が `35,654 tokens / 149s`、従来法が `7,088 tokens / 49s` だったことを、散布図品質・ラベル品質と並べて解釈
- 「scatter 目的だと割高、label semantics 目的なら検討余地あり」という読みを [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に追記

## [2026-05-25 10:03] filing-back | `broadlistening-research` の 2025-02 judge を使ってラベル品質も比較

- `~/broadlistening-research/publish/2025-02-11-02-NISHIO.md` と `experiments/2025-02/evaluate_cluster_labels.py` を確認し、当時の評価軸が `一貫性 / 具体性 / 網羅性 / キーワード適切性` だったことを確認
- 今回の `analysis-core` 出力には keyword が無いので、4 項目目を `区別性` に置き換え、各 top-level cluster の `label`, `description`, 意見例 5 件, 他ラベル一覧を OpenAI judge に与えて比較
- judge 結果は `work/kouchou-ai/packages/analysis-core/outputs/label_quality_judge_2026-05-25.json` に保存し、平均総合点は `LLM grouping 85.0`, `hierarchical 80.4`、全体 winner も `llm_grouping`
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に「geometry と label semantics を別軸で評価すべき」という判断を追記

## [2026-05-25 10:00] filing-back | 同一 args で従来 hierarchical clustering と比較

- `jigsaw_sample_comments_400_hierarchical_compare.json` を追加し、同じ 422 argument / 同じ `embeddings.pkl` を使って `cluster_nums: [8]` の従来 hierarchical clustering を別出力へ実行
- 比較用出力では `hierarchical_status.json` を seed して `extraction` / `embedding` を skip し、clustering 以降だけを実行
- 従来法は silhouette score `0.400`、centroid ベース再分類精度 `1.000` で、LLM grouping の `-0.039` / `0.488` より scatter 適合が明確に高いことを確認
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] に比較結果を追記

## [2026-05-25 09:58] filing-back | 400 件日本語データで `analysis_mode=llm_grouping` の初回実験結果を記録

- `~/kouchou-ai/.env` の OpenAI キーを使い、`apps/admin/public/sample_comments.csv` 400 件を `analysis-core` 入力形式へ整形して `analysis_mode=llm_grouping` を実行
- 422 argument を 8 群へ分類し、`outputs/jigsaw_sample_comments_400_config/` に `hierarchical_result.json` と `report.html` を生成
- 途中で `llm_grouping` spec の prompt 欠落と visualization workflow の `${config.report_dir}` 強制解決バグを検出し、current working tree の `analysis-core` を修正
- 新規 source [[jigsaw-llm-grouping-experiment-output-2026-05-25]] と [[jigsaw-llm-grouping-experiment]] / [[meeting-report-draft]] を更新し、scatter 互換の限界と次に group-first view を優先すべき判断を反映

## [2026-05-25 09:41] filing-back | Jigsaw LLM grouping の実験ページを追加し、400 行日本語データ採用を記録

- 新規 analysis [[jigsaw-llm-grouping-experiment]] を追加し、この実験は専用 wiki ページで継続観察すべきこと、最初の入力データとして `work/kouchou-ai/apps/admin/public/sample_comments.csv` の 400 行日本語コメントを使う判断を記録
- 同ページに、目的、入力前処理の必要性（`comment` 1 列を `comment-id` / `comment-body` 形式へ変換）、観察ポイント、次に残すべき実験ログを整理
- `wiki/index.md` Analyses に追記

## [2026-05-25 09:32] filing-back | `analysis_mode=llm_grouping` の最小実装を analysis-core に追加

- `work/kouchou-ai/` で `packages/analysis-core` に `analysis_mode=llm_grouping` を追加し、workflow / spec / config normalization を mode 切替対応に更新
- 新規 step/plugin `llm_grouping` を追加し、`embedding` は `x/y` 用に残しつつ、cluster assignment 自体は raw argument を直接 LLM で決めて `hierarchical_clusters.csv` / `hierarchical_merge_labels.csv` を生成する最小実装を入れた
- targeted test として `rye run pytest tests/test_compat.py tests/test_integration.py tests/test_llm_grouping.py -q` を実行し、20 件通過まで確認
- [[meeting-report-draft]] にも、散布図互換の短期実装と次の代替 view 検討を追記

## [2026-05-25 09:26] filing-back | 議事録 HTML から URL 棚卸しを抽出し、派生 source 化

- `raw/meeting_minutes.html` を取得し、`scripts/extract_meeting_minutes_urls.py` を追加。Google redirect を実 URL に戻しつつ、anchor と本文ベタ書き URL を合わせて `raw/meeting_minutes_urls.tsv` / `raw/meeting_minutes_urls_summary.md` を生成
- 新規 source [[meeting-minutes-url-extraction-2026-05-25]] を追加し、531 unique URLs / 89 domains、`kouchou-ai repo` 136 件、`weekly history` 81 件、`slack permalink` 49 件などの棚卸し結果を要約
- [[meeting-minutes]] にスクリプト導線を追記し、[[index]] Sources と [[meeting-report-draft]] にも反映

## [2026-05-25 09:16] filing-back | 議事録 txt export のリンク欠落リスクと html 補助取得を運用へ反映

- `CLAUDE.md` の ingest / query / 運用方針を更新し、`raw/meeting_minutes.txt` は検索用、URL 確認が必要な時は `raw/meeting_minutes.html` を併用するルールを明記
- [[meeting-minutes]] に `txt` export がリンク URL を落としうる制約と `html` export の補助取得コマンドを追記
- [[wiki-driven-workflow]] / [[local-dev-setup]] にも同じ二段運用を反映し、オンボーディング時に URL 確認経路を確保しやすくした

## [2026-05-25 08:49] filing-back | Jigsaw 的 LLM 分類の implementation plan を current tree に即して整理

- 新規 source [[llm-grouping-implementation-observation-2026-05-25]] を追加し、`work/kouchou-ai/main` と GitHub current state から、`PR #827` 計画文書は main 済みだが `analysis_mode` 分岐・`analysis_capabilities`・viewer `requirements` は未実装と観測
- 新規 analysis [[jigsaw-llm-grouping-implementation-plan]] を追加し、Jigsaw 系実装は direct-step ではなく workflow canonical path に `analysis_mode` を差し込み、短期は embedding 併用の互換 `llm_grouping`、長期は capability contract へ進む順序が妥当と整理
- `wiki/index.md` Analyses に新ページを追加

## [2026-05-25 08:38] filing-back | Windows setup PR #863 の保留状態とローカル除外設定を反映

- `.claude/` を親 wiki repo の `.git/info/exclude` に追加し、ローカル設定由来の未追跡ノイズを作業ツリーから除外
- [[meeting-report-draft]] に、`PR #863` は open のままだが Windows 検証環境が整備中のため review / merge 保留、という current state を追記
- [[development-priority-roadmap-2026-05-23]] にも同じ保留状態を反映し、「最優先テーマではあるが直近の実作業は環境整備後の再確認」と補正

## [2026-05-25 00:19] ingest | 方向性会議 2 本と鈴木健ブログを source 化

- Google Docs export から `raw/kouchou-ai-direction-2025-12-06.txt` と `raw/kouchou-ai-direction-2-2025-12-13.txt` を取得し、2025-12 の「広聴AIの方向性について」会議 2 本を独立 source として分離
- はてな記事 `2025-11-29 ブロードリスニングにおけるインサイトの分類とツールの使い分け` を `raw/kensuzuki-broad-listening-insight-types-2025-11-29.*` に保存し、新規 source [[kensuzuki-broad-listening-insight-types-2025-11-29]] を追加
- [[versioning-strategy]] に v4 / v5 分離判断の前史を補強し、[[slack-design-intents-2025-q4]] と [[strategic-development-order-2026-05-23]] にも新 source への導線を追加
- `wiki/index.md` Sources を更新

## [2026-05-24 00:06] filing-back | PR #865 merge を反映し、Refactoring Status を current `main` に同期

- `work/kouchou-ai/` を `git fetch origin && git pull --ff-only` で更新し、`main@e5ed743` を一次参照として確認
- [[refactoring-status]] を更新し、legacy cleanup merge 後の current state に合わせて Phase 8 を完了、refactoring 全体を done 判定へ補正
- [[open-decisions]] から Phase 8 の open item を除外し、[[source-code]] / [[pipeline]] / [[gotchas]] / [[workflow-defaultization-blockers]] も current tree に合わせて補正
- [[meeting-report-draft]] に `PR #865` と CI 修正を次回定例向け要点として追記

## [2026-05-23 15:20] ingest | Slack thread (2026-05-23) で ohki-shingo が整理した公開UI要件を取り込み

- 新規 source [[slack-public-ui-requirements-2026-05-23]] を追加し、`#2_開発_広聴ai` 想定の 2026-05-23 thread を記録。oss_weekly_reporter dump は 2026-05-20 までなので、当面 `raw/slack-public-ui-requirements-2026-05-23.txt` を一次根拠にする旨も明記
- 新規 analysis [[public-ui-requirements-for-broadlistening]] を追加し、(a) 散布図が受け入れられている要因 5 要素、(b) 公開UIに求められる 7 要件、(c) embedding 距離精度の非本質性（クラスタ間分離は必要だがクラスタ内距離精度は不要）を整理。view plugin の上位契約として明示
- [[jigsaw-sensemaker-history]] に Updates と Open Questions を追記し、ohki-shingo の整理を「散布図役割の別 view 代替」への回答として接続
- [[ohki-shingo]] entity に 2026-05-23 の contribution を追記
- [[meeting-report-draft]] にも次回定例向けの要点として追記
- `index.md` に新規 source / analysis を登録

## [2026-05-23 14:48] filing-back | WebUI / analysis-core 分離の設計判断を独立ページ化し、旧語を廃止

- 新規 source [[analysis-core-web-ui-separation-decision-2026-05-23]] と新規 concept [[analysis-core-and-web-ui]] を追加し、「WebUI で包んだ理由」「その後 core を切り出した理由」「Web は JSON、CLI は `report.html` を持つ理由」を歴史ページと分離して整理
- [[tttc-to-analysis-core-history]] は歴史、[[analysis-core-and-web-ui]] は現在のソフトウェア設計判断、という役割分担になるよう導線を追加
- wiki 全体で旧語をやめ、`report.html` は `CLI 向け観察用HTML`、一般論では `補助出力` という言い方へ統一
- 関連ページとして [[usage-modes]] / [[cli]] / [[architecture-overview]] / [[deployment]] / [[pipeline]] / [[refactoring-status]] / [[gotchas]] / [[meeting-report-draft]] / source 群も同じ用語に補正

## [2026-05-23 13:38] filing-back | `report.html` を Web canonical にしない判断を wiki に反映

- 新規 source [[report-html-non-web-canonical-decision-2026-05-23]] を追加し、`report.html` は Web canonical にしないという maintainer の明示判断を記録
- [[open-decisions]] から stale になった `report.html` Web canonical 論点を外し、[[usage-modes]] / [[cli]] / [[refactoring-status]] / [[workflow-defaultization-blockers]] / [[strategic-development-order-2026-05-23]] を確定判断へ補正
- [[meeting-report-draft]] にも、CLI 観察用HTMLと Web canonical path の分離を次回定例向け要点として追記

## [2026-05-23 13:21] filing-back | 入口設計の歴史整理に broad-listening-book の根拠を追加

- [[tttc-to-analysis-core-history]] に、書籍 `10_00_DD2030による広聴AIの開発活動.md` の `TTTC Scatter vs 広聴AI` 比較表を反映し、Web 化の意味が「GUI追加」ではなく `環境構築責任と共有導線をサーバ側へ寄せること` だと明記
- あわせて 13.3 の「Python 環境を持つ読者は手元でミニ広聴AIを動かす」導線を根拠として追記し、研究者・開発者向けに軽量な Python 実験入口が必要だった、という読みを補強

## [2026-05-23 13:06] filing-back | TTTC clone 前提から Web UI 包装、analysis-core/PyPI 再切り出しまでの歴史を整理

- 新規 analysis [[tttc-to-analysis-core-history]] を追加し、TTTC / 初期広聴AIの clone / CUI 前提、実務上の共有要請からの Web UI / server 化、研究開発向けに `packages/analysis-core` と CLI / PyPI を切り出して API が consumer に回った流れを 1 ページに整理
- [[usage-modes]] と [[kouchou-ai]] から新ページへの導線を追加し、「Web UI と CLI は後付けの対立ではなく、歴史的に分化した役割分担」という読み方を補強
- [[meeting-report-draft]] にも 1 行追記し、定例会議でこの歴史整理を口頭共有しやすくした

## [2026-05-23 13:02] filing-back | workflow plugin の legacy config 重複削減と回帰テスト追加を記録

- `analysis_core.plugins.builtin.*` に散らばっていた `_input_base_dir` / `_output_base_dir` / token usage 初期化の重複を `_legacy_config.py` に寄せて整理
- `packages/analysis-core/tests/test_builtin_plugins.py` に、`analysis.extraction` が comment artifact から解決した input path と `ctx.output_dir.parent` を legacy step に渡す regression test を追加
- 確認として `cd packages/analysis-core && rye run pytest tests/test_builtin_plugins.py tests/test_workflow_engine.py -q`、`rye run ruff check src/analysis_core/plugins/builtin tests/test_builtin_plugins.py`、`cd apps/api && ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy rye run pytest tests/manual/report_launcher_subprocess_smoke.py -q -s`、`... rye run pytest tests/services/test_report_launcher.py -q` を実行し通過

## [2026-05-23 12:50] filing-back | API 通常フローの manual smoke と workflow path bug 修正を testing / meeting report に追記

- [[testing]] の API subprocess smoke 行を更新し、`execute_aggregation()` だけでなく `launch_report_generation()` から通常フロー全体を local provider + 偽 OpenAI 互換 LLM で踏めることを追記
- full flow smoke の初回実行で、workflow plugin が `--input-dir` / `--output-dir` を legacy step に渡しておらず相対 `inputs/` / `outputs/` を見に行くバグを検出したため、[[meeting-report-draft]] に「手元 smoke を足しただけでなく、そこで見つかった path bug まで直した」要点を追記
- `ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy rye run pytest tests/manual/report_launcher_subprocess_smoke.py -q -s` と `... rye run pytest tests/services/test_report_launcher.py -q` の通過を記録

## [2026-05-23 12:28] filing-back | API -> subprocess -> analysis-core の手元 smoke test を testing / meeting report に追記

- `work/kouchou-ai/apps/api/tests/manual/report_launcher_subprocess_smoke.py` を追加。`execute_aggregation()` から **本物の subprocess** を起動し、`hierarchical_result.json`・`hierarchical_status.json`・`report_status.json` 更新まで確認する手元 smoke test として整理
- [[testing]] に明示実行コマンド `ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy rye run pytest tests/manual/report_launcher_subprocess_smoke.py -q -s` を追加し、既定収集の対象外であることと、analysis-core 単体 e2e と API mock test の間を埋める目的を明記
- [[meeting-report-draft]] にも、「analysis-core 単体の e2e だけでなく API 境界を手元で 1 回は踏めるようにした」という要点を追記

## [2026-05-23 11:32] filing-back | 定例会議向け下書きに Jigsaw 系第2モードの長期論点を追記

- [[meeting-report-draft]] の「月曜にそのまま読む用」と「次回定例向け下書き」に、Jigsaw Sensemaker 的な第2分析モードは自然な散布図を出しにくい一方、散布図は依然としてユーザ価値が高い、という緊張関係の整理を追加
- 短期は散布図互換の暫定案、長期は散布図必須ビューの前提解体、という二段構えを会議で口頭共有しやすい形に圧縮し、[[strategic-development-order-2026-05-23]] と [[jigsaw-sensemaker-history]] への導線もつないだ

## [2026-05-23 10:02] filing-back | current roadmap を open issues / wiki から再整理

- 新規 analysis [[development-priority-roadmap-2026-05-23]] を追加。2026-05-23 時点の GitHub current state を確認し、`#836` `#837` `#833` `#845` `#846` `#716` `#740` など 5/21-5/22 に close 済みの前提作りタスクを除外した current roadmap を作成
- 優先順を「Windows 初回導入 (`#731`) → user-facing bug (`#584` `#493` `#629`) → 運用基盤 (`#741` `#518` `#558` `#546` `#838`) → 説明責務 / 研究テーマ (`#696` `#542` `#564` `#577` `#809`)」へ組み替え、実装工数と calendar の目安も追記
- `wiki/index.md` Analyses に新ページへの導線を追加

## [2026-05-23 10:02] filing-back | issue-centric roadmap を補う長期戦略ページを追加

- 新規 analysis [[strategic-development-order-2026-05-23]] を追加。`usage-modes`, `plugin-system`, `refactoring-status`, `book-release-development-plan-2026-09`, `broad-listening-book-extractions` を束ね、`kouchou-ai` を「共通実験基盤 / 製品導線 / 探索枝」の 3 層 platform として見る長期順序を整理
- 優先順を「`analysis-core` の canonical contract 固定 → plugin 実証 1 本目 → Web / CLI / distribution の役割固定 → experiment portfolio 運用 → trust layer」の順で記述し、短期 bugfix 順と別レイヤだと明示
- [[development-priority-roadmap-2026-05-23]] に、本ページが short / mid-term triage であり、長期順は新ページを参照すべき旨を追記
- `wiki/index.md` Analyses に新ページへの導線を追加

## [2026-05-23 10:02] filing-back | 第2分析モードを散布図前提が縛る問題を長期戦略へ明記

- [[strategic-development-order-2026-05-23]] に `Core Problem` 節を追加し、「分析モード数の少なさ」より「第1モードが散布図を自然に出せることが product の既定前提になっており、第2モードが scatter-compatible な形へ無理に射影されやすいこと」が本質的問題だと追記
- current code 上でも `apps/api/src/schemas/visualization_config.py`、`apps/admin/.../VisualizationConfigDialog.tsx`、`apps/public-viewer/components/charts/SelectChartButton.tsx` が `scatterAll` を既定にしている一方、`docs/development/plugin-guide.md` には散布図なし設定例があり、設計意図とプロダクト既定のズレがあることを確認
- 長期戦略の問いを「analysis mode を増やすこと」から「散布図を前提にしない analysis mode でも product が成立する capability contract へ移れるか」へ寄せ直した

## [2026-05-23 10:02] filing-back | Jigsaw Sensemaker と散布図の緊張関係を時系列で整理

- Google Doc export から `raw/meeting_minutes.txt` を再取得したうえで、meeting minutes / `#2_開発_広聴ai` / `#2_開発_広聴ai_アルゴリズム開発` を再読
- 新規 analysis [[jigsaw-sensemaker-history]] を追加し、2025 4Q の「現行散布図方式の限界認識」から、2026 Q1 の「Jigsaw 系を受け入れるには可視化を分析から切り離す必要がある」という設計意図までを時系列で整理
- [[strategic-development-order-2026-05-23]] で現在の core problem として書いた「scatter-first な product 契約が第2モードを縛る」という見立てが、過去ログにも連続して現れていたことを明文化
- `wiki/index.md` Analyses に新ページへの導線を追加

## [2026-05-23 10:02] filing-back | Jigsaw系第2モードの移行戦略を一文で要約

- [[strategic-development-order-2026-05-23]] に `Working Formulation` を追加し、「embedding を前提としない分析様式でも、短期は embedding 併用で散布図互換に載せ、長期は散布図必須ビューをやめる」という二段構えを作業仮説として明文化
- [[jigsaw-sensemaker-history]] に `Distilled Take` を追加し、この要約が 2025 4Q 〜 2026 Q1 の議論の収束形として読めることを補記

## [2026-05-23 00:10] ingest | Docker Desktop 回避策（WSL2 + Docker Engine）の GPT ブレストを反映

- `raw/docker-engine-wsl2-alternative-2026-05-23.txt` を新規追加
- 新規 source [[docker-engine-wsl2-alternative-2026-05-23]] を追加。Docker Desktop ライセンス問題の回避策として WSL2 Ubuntu に Docker Engine + Compose plugin を直接入れる構成、UX コスト、2 本立て docs 案を critical lens で要約
- [[windows-distribution-options]] にランタイム基盤の選択軸（ルート A: Docker Desktop / ルート B: Docker Engine in WSL2）を段階軸と直交する第 2 軸として追加し、Open Question にルート B を主要ルートへ昇格させるかを追記
- [[local-dev-setup]] の Windows 配布 note を 2 軸（段階 / ランタイム基盤）案内に拡張
- `wiki/index.md` の Sources / Analyses entry を更新

## [2026-05-22 23:55] filing-back | `.bat` から PowerShell へ逃がす判断理由を source / analysis 化

- 新規 source [[issue-731-windows-setup-mojibake]] を追加。issue #731 の再現ログから、問題が表示崩れではなく `cmd.exe` のパース破綻を含むことを整理
- 新規 analysis [[windows-setup-encoding-decision]] を追加。`.bat` 単体で設定非依存に日本語対話を安全に扱いにくい理由と、ASCII ランチャー + PowerShell 本体へ分離する判断を整理
- [[windows-distribution-options]] と [[local-dev-setup]] から、この判断理由へ辿れるようリンクを追加

## [2026-05-22 23:55] filing-back | `.bat` から PowerShell へ逃がす判断理由を source / analysis 化

- 新規 source [[issue-731-windows-setup-mojibake]] を追加。issue #731 の再現ログから、問題が表示崩れではなく `cmd.exe` のパース破綻を含むことを整理
- 新規 analysis [[windows-setup-encoding-decision]] を追加。`.bat` 単体で設定非依存に日本語対話を安全に扱いにくい理由と、ASCII ランチャー + PowerShell 本体へ分離する判断を整理
- [[windows-distribution-options]] と [[local-dev-setup]] から、この判断理由へ辿れるようリンクを追加

## [2026-05-22 23:45] ingest | Windows 配布形態に関する nishio ↔ GPT ブレストを取り込み

- `raw/a.txt` を `raw/windows-distribution-gpt-brainstorm-2026-05-22.txt` にリネーム
- 新規 source [[windows-distribution-gpt-brainstorm-2026-05-22]] を追加。GPT ブレストを critical lens で要約し、既存 [[usage-modes]] / [[local-dev-setup]] / 進行中の `setup_win.*` 作業と突き合わせた
- 新規 analysis [[windows-distribution-options]] を追加。非専門家 Windows 配布を `setup_win.*` / ランチャー exe / デスクトップアプリ / 単体 exe の 4 段階で整理し、現状は段階 1 で進行中・段階 2 以降は open question として記録
- [[usage-modes]] の Open Questions と [[local-dev-setup]] の Windows 落とし穴節から新 analysis へリンクし、`wiki/index.md` Sources / Analyses に追記

## [2026-05-22 23:43] filing-back | Windows PowerShell 標準搭載の根拠を公式 source として追加

- 新規 source [[windows-powershell-default-installation]] を追加。Microsoft Learn を根拠に、Windows PowerShell 5.1 は Windows client 10 以降で既定インストール、ただし `pwsh` とは別物であることを整理
- [[local-dev-setup]] に「通常の Windows 10/11 なら PowerShell は入っている」と書ける根拠を追記
- [[windows-distribution-options]] に、`setup_win.bat -> powershell.exe` 方針が Windows 10/11 対象として置きやすい前提であることを補記

## [2026-05-22 23:27] filing-back | Issue #731 の Windows setup 対応方針を PowerShell 分離へ切り替え

- `PR #858` は close し、issue #731 に「`.bat` 単体の ASCII 化ではなく、`setup_win.bat` を ASCII ランチャー、`setup_win.ps1` を日本語案内本体に分離する」方針をコメント
- `work/kouchou-ai/` で branch `codex/issue-731-windows-setup-powershell` を切り、`setup_win.bat` の薄化、`setup_win.ps1` 新設、Windows セットアップ手順の doc 更新を実施
- 新しい提案として `PR #863` を作成し、console codepage 依存を避けつつ日本語案内を残す構成へ切り替えた

## [2026-05-22 23:00] filing-back | 個人マシン runner の実行条件を手動限定へ変更

- PR #862 の review comment を受け、`actions/checkout` を SHA pinning し、`persist-credentials: false` を追加
- 公開 repo の workflow が個人 Windows 実機 runner を使う危険を踏まえ、Real Windows E2E の `pull_request` trigger と `schedule` を削除
- Real Windows E2E は `workflow_dispatch` かつ workflow に定義された実行者条件を満たす場合だけ動く形に変更
- [[windows-real-machine-e2e-lessons]] / [[gotchas]] / [[meeting-report-draft]] に、個人マシン runner は PR や定期実行から動かさない判断を反映

## [2026-05-22 22:43] filing-back | CI success と実機 E2E failure の観測面の違いを追記

- [[windows-real-machine-e2e-lessons]] に、docs deploy / repo checkout 上の client build / Docker image build / container 起動後 runtime build は別の観測面であることを追記
- PR #862 の `public-viewer` failure は、repo には `apps/shared` が存在しても Docker image runner stage には入っていない、という runtime image 欠落だったと整理
- [[gotchas]] に「CI の success はどの層の success かを確認する」という項目を追加

## [2026-05-22 22:37] filing-back | Windows 実機 E2E 構築の学びを wiki 化

- 新規 analysis [[windows-real-machine-e2e-lessons]] を作成し、Issue #860 / PR #862 の runner、Docker Desktop、readiness check の学びを整理
- [[gotchas]] の Windows インストール地獄に、runner 設定・app 実装・到達確認の問題を層で分ける注意点を追記
- `index.md` に新規 analysis を登録
- 個人情報を避け、公開 Issue / PR / commit / workflow と一般化できる症状だけを記録

## [2026-05-22 22:33] filing-back | Issue #860 実機 E2E の readiness check を修正して成功確認

- Windows 実機では `curl.exe -I` が各 service に即 200 を返す一方、PowerShell の `Invoke-WebRequest` は同じ URL でタイムアウトすることを確認
- `.github/workflows/windows-real-machine-e2e.yml` の readiness check を `Invoke-WebRequest` から `curl.exe --fail --head --silent --show-error --max-time 5` に変更
- commit `5981d9e1` を PR branch に push し、`Windows real-machine setup E2E` を含む PR checks が全て success になったことを確認
- [[meeting-report-draft]] に実機 E2E 成功まで反映

## [2026-05-22 22:26] filing-back | Issue #860 実機 E2E で見つかった Dockerfile 欠落を修正

- `#860 -> draft PR #862` の Windows 実機 E2E が `public-viewer` の `Cannot find module '../shared/csp'` で失敗していることを確認
- 原因は runtime build を行う Docker image に `apps/shared` が入っていないことだったため、`apps/public-viewer/Dockerfile` と `apps/static-site-builder/Dockerfile` に `apps/shared` の copy を追加
- Windows 実機の Docker Desktop で `public-viewer` と `static-site-builder` の image build が成功することを確認し、commit `2928890b` を PR branch に push
- [[meeting-report-draft]] に進行中項目として追記

## [2026-05-22 22:12] filing-back | Issue #860 を runner 実装込みで PR 化

- `#860 -> draft PR #862` として、Windows 実機検証 docs に加えて `setup_win.bat` の `--non-interactive` / `--skip-docker-start` / API key 引数を追加
- `.github/workflows/windows-setup-script.yml` で hosted `windows-latest` 上の文字コード・Docker 未起動・`.env` 生成回帰を確認する軽量 CI を追加
- `.github/workflows/windows-real-machine-e2e.yml` で self-hosted Windows runner label `kouchou-ai-e2e` を使う実機 E2E を追加し、`setup_win.bat` 実行後に `localhost:4000` / `3000` / `8000/docs` を待つ構成にした
- CI 初回失敗は PowerShell 7 が期待 exit 1 を step failure として扱ったためで、commit `7287350e` で `$PSNativeCommandUseErrorActionPreference = $false` と `call .\setup_win.bat` に修正して push
- hosted Windows では Docker が Windows containers として動いていたため、fake `docker.bat` を安定して使えるよう `setup_win.bat` の Docker 呼び出しを `call docker ...` に変更し、commit `1f6fa753` で再 push
- PowerShell step が検査後も `$LASTEXITCODE=1` を job 終了コードとして返したため、commit `80787ccb` で軽量 CI の検査成功時に `exit 0` するよう修正して再 push
- 実機 E2E job が custom label `kouchou-ai-e2e` 待ちで queued だったため、commit `db2676b5` で `runs-on: [self-hosted, Windows, X64]` に変更して再 push。PR checks 上で実機 runner が job を pickup した
- 実機 runner `GALLERIA` には `pwsh` がなかったため、commit `08f5e76c` で self-hosted E2E workflow の shell を Windows PowerShell (`powershell`) に変更して再 push
- 実機 runner の PowerShell execution policy が `.ps1` 実行を拒否したため、commit `6d21549a` で E2E workflow の PowerShell shell template に `-ExecutionPolicy Bypass` を追加して再 push
- 実機 runner service の PATH に Docker CLI がなかったため、commit `5a7bc352` で `C:\Program Files\Docker\Docker\resources\bin\docker.exe` を明示し、`setup_win.bat` 実行時だけ PATH に Docker bin を追加して再 push
- `docker compose down` の warning が PowerShell native error として step failure になったため、commit `66b96c0d` で Docker 操作ステップを `cmd` shell に寄せて再 push
- 任意の PR で self-hosted runner を実行するのは危険という指摘を受け、commit `c2d220ed` で PR 起動時は PR author が `nishio` の場合だけ Real Windows E2E job を実行する条件を追加。nightly schedule と手動 `workflow_dispatch` は維持
- 同じ PR への連続 push で古い E2E run が runner を占有し、最新 run が queued のままになる問題を確認。commit `146ec779` で `concurrency` / `cancel-in-progress` を追加し、古い in-progress run を手元で止めて最新 run が pickup されることを確認
- [[meeting-report-draft]] に `#860 -> draft PR #862` の進行中項目を追記

## [2026-05-22 21:12] filing-back | Issue #860 Windows 実機セットアップ検証 docs を作成

- `work/kouchou-ai/` を `main@e6b2d72` まで同期し、assignee なしの `#860` を `nishio` に assign
- `docs/development/windows-real-machine-setup-verification.md` を追加し、`setup_win.bat` + Docker Desktop (Linux containers) の実機検証手順を整理
- `docs/getting-started/windows-setup.md` から検証手順へリンクし、`mkdocs.yml` の nav に登録
- `python -m mkdocs build --strict` と `git diff --cached --check` を実行。新規ページの nav 未登録は解消済み
- commit `b1fa148d` を `codex/windows-real-machine-setup-docs` に push 済み。PR 作成は GitHub コネクタ操作が拒否されたため未作成
- [[meeting-report-draft]] に進行中項目として追記

## [2026-05-22 20:24] filing-back | Codex による Windows 環境構築メモを追加

- 新規 [[codex-windows-environment-memo]] を作成
- Issue #731 / draft PR #858 と Python 導入・wiki lint 復旧の体験を、個人情報を含めずに整理
- `index.md` に analysis ページとして登録

## [2026-05-22 20:09] filing-back | Windows setup Issue #731 の進行中修正を記録

- `work/kouchou-ai/` を `main@e6b2d72` まで同期し、open Issue から Windows 系の重要候補を確認
- assignee なしの `#731` を `nishio` に assign してから、`codex/fix-windows-setup-mojibake` で `setup_win.bat` を修正
- `setup_win.bat` の実行メッセージを ASCII 化し、API キー検証の重複を整理。Docker 未インストール環境で `cmd /c "echo. | setup_win.bat"` による停止パスを確認
- commit `886c91a0` を push し、draft PR #858（`[codex] Windows setup の文字化け耐性を改善`）を作成
- [[meeting-report-draft]] に進行中項目として追記

## [2026-05-22 19:28] filing-back | 月曜定例会向けの meeting-report-draft をやさしい表現に整備

- [[meeting-report-draft]] に「月曜にそのまま読む用」セクションを追加
- technical term を減らし、`#740 -> PR #856` と `#710 -> PR #857` まで反映
- 箇条書き全体も、会議で口頭共有しやすい短い文へ言い換え
