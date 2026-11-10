# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-11-10 14:30] filing-back | #471 元の PR からの抽出を gemma-4-31B で測った

- nishio「抽出したデータからさらに抽出してるのでは？元Issueからのextractionで計測した？」を受け、198 の PR 本文を GitHub から取り直し、当時の課題抽出のプロンプトそのままで gemma-4-31B に抽出させ、公開データの gpt-4o の出力と出どころを伏せて比べた
- 31B の 171 勝 4 敗。gpt-4o は具体的な問題を落として抽象的な 1〜3 件に縮める負け方。件数が同じ組でも 28 勝 0 敗だが、判定役が長く具体的な文を好む偏りは人の判定で確かめる。31B は 1 件で説明欄が繰り返しループに入り出力が終わらなかった。結果は [[team-mirai-local-llm-quality-2026-11-10]] の結果 4 に
- 次：同じ条件で E4B・ELYZA・12B を回す、20〜30 組を人が判定する

## [2026-11-10 13:30] filing-back | Slack の Bedrock 対応の議論を読んで考察した

- #1169・#1170 は GitHub だけで提案され、Slack の議論は 11-10 朝の nishio の投稿が最初で、まだ返信はない。対立点は慎重さではなく「誰の要件のために、誰の費用で検証するか」
- オープンウェイトの候補（GPT-OSS 120B・Qwen3）の品質は Bedrock の契約なしで既存の評価の仕組みで測れること、本体の provider `local` に Bedrock の OpenAI 互換エンドポイントを入れればコード変更なしで試せる可能性があることを [[domestic-data-residency-options-2026-11-10]] の Updates に追記
- 次：大木さんに想定利用者と「国内」の段階を確認する

## [2026-11-10 10:40] filing-back | #471 ローカル LLM の品質比較に、8B 級と中くらいのモデルを足した

- nishio「それから 8B」「間の大きさのモデルも試せるといいな」を受け、ELYZA-JP-8B・gemma-4-E4B・12B・26B-A4B を同じ課題 200 件・40 クラスタで回し、gpt-4o-mini と出どころを伏せて比べた。抽出の判定基準には境界の規則を足し、30B 級も判定し直した
- どのモデルも gpt-4o-mini に大きく劣らない。ラベルの勝ち点は gemma-4-E4B が最も高く（0.67）、26B-A4B だけが長く強い表札で負け越した（0.47）。ELYZA は 200 件中 2 件でプロンプトの例文をそのまま返した。40 クラスタでは区間が重なり、大きさの順位は付かない。結果は [[team-mirai-local-llm-quality-2026-11-10]] の結果 3 に。[[meeting-report-draft]] と [[domestic-data-residency-options-2026-11-10]] も更新
- 次：人の A/B 判定で判定役を較正する。受け入れ基準に「入力に無い内容を出さない」を入れる

## [2026-11-10 10:10] filing-back | 国内完結の選択肢の整理に、ローカル LLM の品質比較の結果をつないだ

- [[domestic-data-residency-options-2026-11-10]] の Updates に、案 1（ローカル計算）の品質の材料として [[team-mirai-local-llm-quality-2026-11-10]] を追記（30B 級は gpt-4o-mini に劣らない判定、8B 級は未測定）
- #1190 の本文には未反映。8B 級の品質が測れたら Issue 側にも足す

## [2026-11-10 09:40] filing-back | データ分析を国内だけで完結させる選択肢を整理し、上位 Issue #1190 を作成

- nishio の依頼で、Bedrock 対応（#1169）を実装案の一つとする上位 Issue #1190「データ分析が国内だけで完結できるようにしたい」を作り、#1169 を子 Issue にした。第一候補はローカル計算。Azure は今の機能でデプロイ種別を Standard（リージョン単位）にすれば国内処理になるが、Japan East の従量課金のチャットモデルは 2 つだけで 2027-04-14 に廃止予定（公式で確認）
- 判断の筋と鮮度を [[domestic-data-residency-options-2026-11-10]] に、Azure の要点を [[llm-providers]] に、議題を [[meeting-report-draft]] に。あわせて #1162 の CI が main の取り込み直しで green になったことを記録
- 次：「国内」の意味（処理場所／事業者／端末・庁内）を決める。#1170 の検証対象を Azure・Vertex に広げるか

## [2026-11-10 00:25] filing-back | #471 ローカル LLM の品質をチームみらいのデータで gpt-4o-mini と比べた

- nishio「速度ではなく品質が知りたい。チームみらいデータセットを使って実験してみて」を受け、組織内 API の gemma-4-31B・Qwen3.8-27B に当時のプロンプトで抽出 200 件・ラベル 40 クラスタを作らせ、gpt-4o-mini の公開出力と出どころを伏せた 2 案比較（判定役は Claude、ラベルは順を入れ替えて 2 回）
- 抽出は gemma 16 勝 6 敗・Qwen 14 勝 13 敗（Qwen は「〜すべき」への強め 12 件）、ラベルは両モデルが優勢だが判定役の 2 回の一致は 67%。結果と評価方法の残り（人の較正・境界の規則・受け入れ基準の形）を [[team-mirai-local-llm-quality-2026-11-10]] に、定例向けの 1 項を [[meeting-report-draft]] に
- 次：8B 級を同じ足場で回す、120 組を人が A/B 判定して判定役を較正する

## [2026-11-10 00:05] filing-back | 対立軸ビューを活用するユーザストーリー案

- nishio「対立軸ビューを活用して行くユーザストーリーを考えられるといいなと思う」への AI の案を [[divcon-view-user-stories]] として新規作成。5 つの場面（政策を書き直す人・ファシリテーター・パブコメの回答者・参加者・報告をまとめる人）と、共通して足りないもの（「関係なし」と中立・全件の数が合う集計・採点を人が直す手段）、最初に詰める候補（1 か 3）
- [[team-mirai-2025-open-dataset]] と [[meeting-report-draft]] からリンク

## [2026-11-08 23:10] filing-back | 対立軸ビューと賛否スライダーを作ってみた見立て

- nishio「この 2 つを作ってみてどう思う？」への AI の答えを記録。対立軸ビューは読む道具になる（少数側が埋もれない、採点の誤り・中立なし・費用が課題）。賛否スライダーは説明用で新しく見えるものは少なく、収穫は「広聴AI の散布図は話題の地図で賛否は描いていない」こと
- 残る判断へのおすすめ（賛否の対象のキーは足す、`opposition_axes` はまだ足さない、本体に入れるなら散布図の賛否色分け）を [[team-mirai-2025-open-dataset]] と [[meeting-report-draft]] に。色分けの試作は nishio が今は作らないと判断

## [2026-11-08 23:00] filing-back | 個人 repo の可視化カタログに賛否スライダー（センチメント次元の付与）を追加

- nishio/broadlistening-visualizations の commit `6971f97`（main に push・公開済み）。本体の `opinion_stance` と同じプロンプトで 4 まとまり・2,167 件に賛否スコアを付け、埋め込みに重みつきで足した配置を重み 0〜1.5 で作った。学習率 0.1 と Procrustes で漂いを 12% → 2.5% に
- nishio の問い「賛否を無視したら元の広聴AI になるか」への答え（元の配置はすでに賛否をほぼ無視している・線形には消えきらない）と、`public_result.json` に足りない項目（賛否の対象）を [[team-mirai-2025-open-dataset]] に、試した事実を [[open-decisions]] A14 に、定例向けの 1 項を [[meeting-report-draft]] に反映

## [2026-11-08 15:20] filing-back | 個人 repo の可視化カタログに DivCon の対立軸ビューを追加

- nishio/broadlistening-visualizations の commit `b18593f`（main に push・公開済み）。tokoroten/divcon の Stage 3a〜5 を、広聴AI の上位クラスタをトピックにして回した。賛否の割れそうな 4 まとまり・2,167 件で軸 12 本・延べ採点 3,338 件、組織内の OpenAI 互換 LLM で 358 回
- 結果・誤りの傾向・`public_result.json` に足りない項目（軸の定義）を [[team-mirai-2025-open-dataset]] に、方針は変えずに試した事実を [[open-decisions]] A14 に、定例向けの 1 項を [[meeting-report-draft]] に反映

## [2026-11-08 10:00] filing-back | #921 ブラウザ版の本流化は tokoroten のアクション待ち

- nishio「方向性としてはそれでいいけど tokoroten のアクション待ち」。論点1（「本流」の範囲）を先に決めて Issue に記録する方針は了承済み
- [[meeting-report-draft]] の #921 の項と Updates、kouchou-issue-audit-queue の STATUS に反映

## [2026-11-08 09:57] filing-back | 個人 repo の可視化カタログ：付箋の文字を全文が収まる最大の大きさに

- nishio/broadlistening-visualizations の commit `23a2584`（main に push・公開済み）。マンダラートはマスごと、付箋ズームは付箋ごとに、全文が収まる最大の文字サイズを決める
- 付箋ズームのまとまりの代表の付箋は、nishio の判断で表札だけにした（表札と本文を 1 枚に入れると 10〜12px にしかならなかった）。確かめた文字の大きさを [[team-mirai-2025-open-dataset]] の「個人 repo のカタログ」に記録

## [2026-11-08 06:45] filing-back | PR #1187（公開 API が公開用レポート結果を返す）と #1189（minimatch 11.0.1 / glob 14.0.2）を merge

- merge 直前に両 PR の mergeable・CI 全件 pass・未解決スレッドなしを確認し、nishio の承認で順に admin merge。方式は直近の #1188・#1185・#1183 に合わせて squash。#1187 は main `3d7a8f9a`、#1189 は #1187 の後も mergeable で CI 結果が有効なことを確かめてから main `ddd0bacd`
- main で走ったテスト・ビルド・CodeQL は green（`3d7a8f9a` の CodeQL は `ddd0bacd` の実行に場所を譲って cancelled）。minimatch・glob の alert は fixed、open alert は low 1 件（#949）だけ
- [[meeting-report-draft]] の 2 項と [[security-maintenance]] の Updates に反映

## [2026-11-08 06:25] filing-back | PR #1184（Playwright のランナーを 24.04 に固定）を close

- #1185（Playwright 1.64.1）の merge で同じ `runs-on` の行が `ubuntu-26.04` に変わり、#1184 は conflict して不要になっていた。nishio の判断で 11-08 06:19 JST に close し、理由をコメントした
- [[meeting-report-draft]] の Playwright の項（議題から外してよい）と [[testing]] の Updates に反映

## [2026-11-07 22:52] filing-back | minimatch 11.0.1 / glob 14.0.2 の PR #1189（override を範囲形式に揃える）

- 完全固定の版を上げるだけでは壊れた: minimatch 11 は jest の glob 7 を壊し、brace-expansion 5.0.12 の完全固定は戻ってくる minimatch 3 / 5 を壊す。minimatch・brace-expansion・glob の override を alert の範囲に合わせた範囲形式に変え、依存元ごとに宣言どおりの版（すべて advisory 0 件）が入るようにした
- lockfile は対象パッケージとその依存の変更だけに絞り、frozen install・jest 2 app・build 3 本・archiver の zip 作成で確認。PR #1189 を作成、merge は人間の判断
- 壊れ方と確かめ方を [[gotchas]] に、現状を [[meeting-report-draft]] と [[security-maintenance]] に反映

## [2026-11-07 22:34] filing-back | PR #1188 を merge（follow-redirects 1.16.2）。同日に medium alert 2 件（minimatch・glob）が新規

- CI 全件 green と CodeRabbit の未解決指摘なしを確認し、nishio が admin merge（main `dd31bebe`）。follow-redirects の alert は fixed。作業 worktree と branch は削除
- 残る open alert は 3 件。medium 2 件は 11-07 に新規で、minimatch は root override の完全固定（10.2.5）が修正版 11.0.1 を弾くので次の Dependabot Updates も失敗する見込み。glob は 10 → 14 のメジャー跨ぎ。low 1 件は修正版なし（#949）
- [[meeting-report-draft]] と [[security-maintenance]] の Updates に反映。対応 PR は未着手

## [2026-11-07 22:25] filing-back | follow-redirects の override を 1.16.2 に上げる PR #1188（main の Dependabot Updates が 10-23 から失敗していた件）

- main の「Dependabot Updates」workflow が 10-23 から毎回 `security_update_not_possible` で失敗していた。原因は #1153 で root の `pnpm.overrides` を 1.16.1 に完全固定していて、10-25 公開の 1.16.2 を Dependabot が解決できなかったこと。Playwright の件が #1185 の merge で解けた後、main の赤はこれだけ
- override を 1.16.2 にし、lockfile は follow-redirects の 4 箇所だけ手で書き換えた（`pnpm install --lockfile-only` は無関係な再解決を混ぜる）。`--frozen-lockfile` と `http-server` の静的配信で確認し、PR #1188 を作成。merge は人間の判断
- 完全固定 override の扱いを [[security-maintenance]] の Open Questions と [[gotchas]] に、現状を [[meeting-report-draft]] に反映

## [2026-11-07 21:50] filing-back | 付箋ズームを事前計算の方式で作り直し（拡大で震える問題）

- 最初の版は画面の升目ごとに付箋を毎フレーム選び直していて、拡大すると震えた。オリジナル（canvas_kozaneba_prototype）を読んで、格子＋螺旋で全意見の位置を固定し、拡大率の段ごとに優先度順の衝突判定で「出始める拡大率」を事前計算する方式に変えた
- 引いた状態でも代表の意見が表札つきの付箋で読める点は残した。[[team-mirai-2025-open-dataset]] に作りを追記

## [2026-11-07 21:40] filing-back | PR #1187 の CodeRabbit 再指摘で、公開 API は写しを読まず正本からだけ作る形に

- 前回の変更後も「正本が無く写しだけの配信では、写しの鮮度・`hidden_properties` との整合を確かめられない」と再指摘。写しだけの配信は現状どの構成でも使っていないので、写しは読まず、正本が無ければ従来どおり 404 にした（2a055d62）。api 577 件通過
- 写しを直接配るのは第 3 段とし、正本との食い違いの検出（書き出し時の指紋など）とあわせて入れる、と docs に明記

## [2026-11-07 21:10] filing-back | PR #1187 の CodeRabbit 指摘で、公開 API は結果ファイルから毎回作る形に変更

- 当初は `public_result.json` を更新日時で新旧判定して優先していたが、ファイル単位の復元で古い写し（隠すと指定する前の列が残る）が新しい日時を持ちうると指摘（Major）。結果ファイルがあれば `build_public_result()` で毎回作り、`public_result.json` は結果ファイルが無い配信でだけ読む形に変えた（4615be67）。読む量は従来と同じ
- 公開用の写しは「速くするための cache」ではなく「結果ファイルを持たない配信先のための成果物」と位置づけ直した形。第 3 段（分割読み込み）で写しを直接配る時は、食い違いを検出する手段（書き出し時の指紋など）が要る

## [2026-11-07 20:30] filing-back | 結果 JSON の層分離 第 2 段を PR #1187 に（公開 API が public_result.json を返す）

- nishio「第 2 段に着手して」。公開 API `GET /reports/{slug}` を `public_result.json` 優先に変え、無い・壊れている・結果より古い場合は `hierarchical_result.json` から `build_public_result()` で変換。ビューアの `Config` 型から公開しない項目を外した（ビューアは使っていなかった）。docs に「公開 API が返すもの」と静的 shell 書き出しの注意を追記
- api 578 件・viewer jest 318 件・tsc・biome・mkdocs strict が通過。[[long-term-strategy-2026-11-02]] と定例下書きに反映。次：merge 判断（外部から公開 API を直接読む利用者への影響）、第 3 段は 5.x

## [2026-11-07 19:00] filing-back | 11-07 の照合を査読で見直し、open PR の数（11-02 は 10 本）・#1176 の未解決指摘・Playwright の件の範囲・Dependabot が自動 PR を出せないことを訂正

- [[open-pr-status-2026-11-02]] の「open PR 8 本」は観測時点から誤りで、#1176・#1177 も open の 10 本だった（[[long-term-strategy-2026-11-02]] の 10 が正しい）。元の文は残して訂正を追記し、title は表の範囲（10-28〜29 作成の 8 本）がわかる形にした。11-07 の 12 本は 10 本から #1166 が抜けて 3 本増えた数
- #1176 は 11-07 の修正 push の後に CodeRabbit の Major 指摘が付いて未解決（反映済みは #1177 だけ）。Playwright の失敗は runner のイメージが原因で、main の取り込みと関係なく 10-31 以降の PR が落ちる（#1183 は初回から）。11-05 の Dependabot の alert は自動 PR が `security_update_not_possible` で出せず、手で上げる必要がある。[[meeting-report-draft]] の第 1 群・#1128（→ #1181）の項も 11-07 の状態に揃えた
- [[testing]] に 23 本目の `infra-checks.yml` と、Client Tests が viewer states の Playwright も回すことを追記。[[security-maintenance]] の hub から件数を外し、[[post-review-direction-issues-2026-10-29]] の #1167 の行、[[stale-issue-disposition-2026-11-02]] の #250（#1166 merge 後も open）を更新
- 次：#250 を close するか、#1176 の指摘の対応、Dependabot の high alert を手で上げる担当（人間）。[[index]] 冒頭の「#1023 の a/b を選ぶ」は 10-26 に決着済みで古い（curated ページなので人間判断）

## [2026-11-07 17:30] filing-back | living ページを 11-03 以降の GitHub の動きと照合（#1165 の指摘の片付けと #1186、main の CI が Playwright で赤い件、Dependabot 2 件、#1128 の残件は #1181）

- 11-03 の照合以降の 4 commit と、GitHub の live state（open PR 12・open Issue 70・release v4.2.0・PyPI 0.3.0・Dependabot open 2）を突き合わせた。wiki に無かったのは、11-07 の [#1165] の修正（軽い 3 件を直し、重い 2 件を #1186 に）、#1162 / #1164 の main 取り込み、shingo-ohki の #1182〜#1185、11-05 に増えた Dependabot alert の 4 つ
- main の E2E の定時実行は 10-31 から 8 回続けて失敗、11-07 の push では Client Tests も落ちた。原因は `ubuntu-latest` が Ubuntu 26.04 に移り、Playwright 1.57.0 が Chromium を入れられないこと。手当ては #1184 / #1185（未 merge）。[[meeting-report-draft]] の議題候補・[[testing]]・[[open-pr-status-2026-11-02]] に反映し、[[testing]] の Open Questions の「E2E は CI 非実行」が古いことを書き足した
- 前回「人間判断」とした #1128 の残件は、11-03 に #1181 として切り出し済みだったので [[sprint-group1-prs-2026-10-29]] に反映。[[security-maintenance]] の「直近の観測」の参照先を 11-02 / 11-07 まで延ばし、[[post-review-direction-issues-2026-10-29]] の表に 11-07 の状態を書き足した
- 次：#1184 / #1185 のどちらを入れるかと merge（人間）、Dependabot の新しい alert の担当、kouchou-issue-audit キューの STATUS.md（10-12 のまま）と open-decisions B9 の扱い（人間）

## [2026-11-07 16:30] filing-back | 可視化カタログに付箋ズームと階層リストの試作を追加

- nishio の指示で、マンダラートの既定を 3×3 にし、付箋ズーム（升目ごとに 1 枚の付箋を置く semantic zoom）と階層リスト（検索つきの単体版）を broadlistening-visualizations に追加。どちらも `public_result.json` をそのまま読む
- [[team-mirai-2025-open-dataset]] に作りを追記。次：上の段の表札を LLM で付けるか、引いた状態で表札が半分しか出ない点

## [2026-11-07 15:40] filing-back | 可視化カタログの個人 repo を作成し、意見マンダラートの試作を公開

- nishio/broadlistening-visualizations（public、MIT）を作成。チームみらいのデータを `public_result.json` の形に変換し、8 つ以下に割るのを意見 1 枚になるまで繰り返した木（5,848 節・最大 7 段）を 9×9 / 3×3 で見せるページを GitHub Pages に置いた
- [[team-mirai-2025-open-dataset]]・[[open-decisions]] A13 に所在と作りを追記
- 次：上の段の表札を LLM で付けるか、付箋ズームの着手

## [2026-11-07 15:20] filing-back | マンダラートは 8 分割を意見 1 枚になるまで繰り返す案を記録

- nishio の案を [[team-mirai-2025-open-dataset]] と [[open-decisions]] A13 に追記。既定の階層づくりは下から併合するため子の数が揃わない（このデータの上位 20 で 1〜38）ので、上から 8 つ以下に割る再帰分割が要る
- 次：内部の節 約 3,000 個の表札を LLM で付けるか、深い段は代表意見で済ませるか

## [2026-11-07 15:00] ingest | チームみらい 2025 オープンデータを source 化し、可視化は個人 repo のカタログで試してから昇格を判断する方針を記録

- [[team-mirai-2025-open-dataset]] を新規作成（Hugging Face の README を 11-07 に読解、CC BY 4.0、意見 21,348 件・20/400 クラスタ）。公開用 artifact `public_result.json` の項目とほぼ 1 対 1 に対応することを main `7253efcc` で照合
- [[open-decisions]] A13・[[meeting-report-draft]]・[[experimental-features-catalog-proposal-2026-06-03]] に、付箋ズーム・ツリー表示・マンダラートを個人 repo でカタログ化してから本体への昇格を判断する方針を追記
- 次：個人 repo の置き場所と変換スクリプト、マンダラート用の [8, 64] の切り直し

## [2026-11-07 14:20] filing-back | 階層リストの詳細モード化（PR #1166）を main に merge

- nishio の指示で PR #1166 を admin squash merge（`7253efcc`）、Issue #1159 は自動 close。CI は 10-29 時点で green、その後の main の変更と触るファイルが重ならず merge-tree で衝突なしを確認
- [[open-decisions]] A13 は階層リストの位置づけが決着し、付箋表示の置き場だけが残る。[[meeting-report-draft]]・[[post-review-direction-issues-2026-10-29]] に反映
- 次：#1167 のスクリーンショット撮り直し、#60（最下層を濃いクラスタに絞る）の着手、#250 を出典リンクでどこまで満たせたかの照合
