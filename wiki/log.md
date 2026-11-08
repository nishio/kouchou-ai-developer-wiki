# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-11-08 17:30] filing-back | 個人 repo の可視化カタログに賛否スライダー（センチメント次元の付与）を追加

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

## [2026-11-03 03:00] filing-back | 査読で見落としとされた living ページの状態記述を GitHub と照合して訂正（#679 close、10-28 close 候補のその後、v4.2.0）

- [[meeting-report-draft]]: 指定カテゴリ分類の項の「#679 を統合候補」を、11-02 の close（completed、WebUI の残件は #997）に直した。10-28 棚卸しの項に、close 候補 #285・#529・#558 が 11-02 に close され #809 は assignee 確認中（期限 11-16）という「その後」を 1 行足した
- [[broad-listening-book]] の v4 / v5 方針の行に v4.2.0（2026-10-26）を足し、[[versioning-strategy]] の「その後の実際」の見出しの時点を 11-03 に改めた
- 次：#1128 の「関連して残っている点」（json_object の拒否、finish_reason の専用例外）は close コメントで別 Issue に引き継がれていない。追跡先を作るかは人間判断

## [2026-11-03 02:00] filing-back | living ページの古い状態記述を GitHub・PyPI・main と照合して訂正（最新タグ v4.2.0、PyPI 0.3.0、11-02 close 済み Issue）

- 最新タグ「v4.1.0」を v4.2.0（2026-10-26）に（[[versioning-strategy]]・[[kouchou-ai]]・[[plugin-system]]・index）。PyPI 最新「0.1.3」を 0.3.0（2026-10-29）にし、`predefined_groups` などが 0.2.0 以降の PyPI 版に入っていることを反映（[[cli]]・[[llm-grouping-supervised-classification]]・[[refactoring-status]]）
- 11-02 の棚卸しで close 済みの #56・#1128・#507・#518・#323・#374・#586 を「open のまま」「close するか」と書いていた箇所を訂正（[[meeting-report-draft]]・[[issue-56-original-comments-opt-in-2026-10-29]]・[[extraction-faithfulness]]・[[open-decisions]] B9・[[other-contributors]]）。定例下書きの情報鮮度と [[meeting-minutes]] の `last_checked` を 11-02 の再取得・Slack 同期に合わせた
- index の「最新の全件棚卸し」を superseded 済みの 10-12 版から [[issue-backlog-audit-2026-10-28]] に差し替え。次：open-decisions B9 を残すか、kouchou-issue-audit キューの STATUS.md（10-12 時点）を更新するか（人間）

## [2026-11-03 01:35] filing-back | 結果 JSON の層分離 第 1 段（PR #1179）を main に merge

- nishio が「手順表示用のプロンプトは公開契約に含めて OK」と判断し、PR #1179 を squash merge（`79981407`）。以後、集計・レイアウト生成・翻訳 CLI は `public_result.json` も書く。古いレポートは次回実行で集計をやり直す
- Issue #1178 は第 2・3 段のため open のまま。次：第 2 段（公開 API とビューアが `public_result.json` を読む）と [#1180](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1180) の A/B

## [2026-11-02 19:40] filing-back | 公開用の属性表から hidden_properties の列を外し（PR #1179）、設定の意味の判断を #1180 に切り出し

- nishio「提案どおり属性表から外して、A/B は別 Issue に」。`public_result.json` の `propertyMap` から `hidden_properties` に指定した属性を列ごと外す実装とテストを追加（23b1f255、analysis-core 813 件通過）。`hierarchical_result.json` は不変
- 現状は元コメント本文だけが隠れ、抽出した意見と属性値は残る。本文だけを隠す（A）か、その値を持つコメント由来の意見ごと隠す（B）かを [#1180](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1180) で判断する。次：PR #1179 の merge 判断

## [2026-11-02 19:00] filing-back | PR #1179 の CI green、CodeRabbit 指摘で hidden_properties の値が propertyMap に残る既存挙動を確認

- CodeRabbit の Minor 1 件（docs が「隠した属性値は propertyMap から除かれる」と書いていた）を確認し、実際は元コメント本文だけが除かれ、`propertyMap` には値が残る main の既存挙動だったので docs を修正（64f0880c）。PR にコメントで判断点として残した
- 次：nishio の merge 判断と、`propertyMap` からも除くかの判断

## [2026-11-02 18:30] filing-back | 結果 JSON の層分離 第 1 段を Issue #1178 / PR #1179 として実装

- 長期戦略の柱 4（v5.0 前倒し案）に nishio が「OK go」。集計・レイアウト生成・翻訳 CLI が結果を書くたびに、ホワイトリストで作る `public_result.json`（schema_version 1）も書くようにし、契約を本体 docs に記載。Blob 同期と秘密の検査・除去スクリプトも対象に追加。既存の挙動は不変
- analysis-core 812 件・api 340 件のテスト、mkdocs strict build が通過。[[long-term-strategy-2026-11-02]] と定例下書きに反映。次：merge 判断（nishio）と第 2 段（公開 API・ビューアの読み替え）

## [2026-11-02 17:20] filing-back | 結果 JSON の層分離を v5.0 に前倒しする案（3 段に割り、契約だけ v5.0）

- nishio「書籍の時期は保証がないので巻いて v5.0 に入れるのも手では」に、賛成の上で 3 段案を回答。第 1 段（集計ステップが公開用 artifact を書く）と第 2 段（公開 API とビューアの切替、旧レポートは読む時に変換）を v5.0 に、第 3 段（丸ごと埋め込みをやめる、静的書き出しの JSON 分離）を 5.x に。main `d2702d48` で範囲を確認（書き手 1 箇所、公開 API 1 本、ビューア 1 fetch、ファイル名参照は api 側約 10）
- [[long-term-strategy-2026-11-02]] の柱 4・要約・直近 90 日を更新。採否は nishio。次：採用なら公開用 artifact の形の RFC から

## [2026-11-02 16:55] filing-back | 長期戦略の考察に「AI の叩き台であり決定ではない」を明記

- nishio の指示で、[[long-term-strategy-2026-11-02]] のタイトル・summary・冒頭の注記に、この戦略案が AI（Claude Code）の叩き台であってチームの決定でも nishio の見解でもないことを明記。index と定例下書きの導線にも「AI の叩き台」を付けた

## [2026-11-02 16:45] filing-back | 長期戦略の考察に、戦略会議でそのまま読める「要約」節を追記

- nishio の「改めて簡潔にまとめて」への回答を [[long-term-strategy-2026-11-02]] の冒頭に「要約」として filing back。方向性・根拠・5 本の柱・やらないこと・成功の定義・いま人間の判断が要るもの、の順で 1 画面に収めた
- 本文（観測の数字と診断）はそのまま。次：戦略会議の日程確定と書籍の発売日の確認（人間）

## [2026-11-02 16:30] filing-back | 長期戦略の柱 3 の目的を「人間がボトルネックにならない形にする」に寄せた

- nishio の追加指摘「nishio 一人でやると解釈されないように」を受け、[[long-term-strategy-2026-11-02]] の柱 3 を書き直した。目的は人間が誰で何人でもボトルネックにならないこと。人間の関与は規則の決定・例外・承認に限り、進める作業は AI が担う。「一人でも回る」は結果であって目的ではない
- 直近 90 日の表の列を「判断者」から「人間の関与」に変え、index と定例下書きの文言も揃えた

## [2026-11-02 16:10] filing-back | 長期戦略の柱 3 を撤回・書き直し（人を増やす案 → 判断を既定＋期限の規則にして一人＋AI で回す）

- nishio の指摘「人間を増やす戦略は OSS では誰かをアサインできないので筋が悪く、実行可能なプランがない」を受け、[[long-term-strategy-2026-11-02]] の柱 3 を書き直した。計画の変数から「人が増える」を外し、nishio 一人と AI で実行できる項目（判断の規則化、branch protection の実態合わせ、止まっても壊れない自動化、手順の checked-in、貢献入口は下げるが期待しない、フォーク可能性の担保）に限定
- 成功の定義・直近 90 日の判断者欄・戦略会議への問い・反論も同じ前提に揃え、index と定例下書きの文言を更新

## [2026-11-02 15:45] filing-back | 現状把握と長期戦略の考察（活動量・貢献者・利用・運営の場を棚卸し、12〜18 か月の戦略 5 本）

- nishio「現状を把握して、長期的な戦略を考えてみて」に回答。main `d2702d48`、GitHub live、Slack mirror（11-02 同期）、議事メモ export（11-02 再取得、07-27 で停止のまま）、PyPI を観測し、[[long-term-strategy-2026-11-02]] を新設
- 診断：製品の形は収束し負債は一巡したが、2026-05 以降の merged PR の 9 割超が nishio、週次定例は 7 月末で停止、鈴木健との戦略会議は 10/25 から日程調整中、利用の観測が無い（PyPI はほぼチーム内、派生製品 Maniken「聴くAI」は 11-01 に発見）
- 戦略：書籍同期の v5.0 を「約束の確定」として切る / 利用の観測を仕組みにする / 判断者を複数にする / 結果 JSON の層分離 / 入口の役割分担を戦略会議で決める。直近 90 日の案と戦略会議への問い 5 つを付けた。index・定例下書き・議事録 source の鮮度を更新。次：戦略会議の日程と書籍発売日の確認（人間）

## [2026-11-02 15:20] filing-back | open PR 8 本の live 状態を確認、#1165 の CodeRabbit 指摘 5 件未対応と #1162 の衝突を記録

- nishio の「現状の PR はどうなってる？」に GitHub の live state で回答。open PR は #1161〜#1167 と #1174 の 8 本、全件 CI green・人間コメントなし。branch protection のレビュー必須で nishio の admin merge が要る
- 10-29 の記録との差 2 点: #1165 は rebase 直後に CodeRabbit が Minor 5 件を付けていて未対応（軽い 3 件、planner 変更 1 件、設計判断 1 件）。#1162 は #1155 の merge で翻訳ファイル 1 本が衝突
- analyses/open-pr-status-2026-11-02 に内訳と判断点を記録し、定例下書き・両 analysis ページの Updates に反映。次：#1165 を直してから merge するか先に merge するかの判断（nishio）、#1162 の rebase

## [2026-11-02 15:17] filing-back | 棚卸し後の更新日分布（1 か月以上 9 件）と、棚卸しコメントで更新日が若返る注意を記録

- nishio の「古い Issue は何か月か / 1 か月以上は何件か / 1 か月以内が 57 件か」に回答。今回の 42 件は「最終更新が 2026-03 より前」で切ったもので実測 8〜19 か月（40 件は 15 か月以上）、ルールの閾値は 12 か月。実行後の open 66 件で 1 か月以上更新なしは 9 件、全件扱い決定済み
- 1 か月以内 57 件の内訳は、棚卸しコメントで若返った 19 / 10-28 以降の新規 7 / 10 月に実際に動いた 31。次回以降は棚卸しコメントの日付を除いて停滞を測る、または考察ページの「次の動き」で追う。analyses/stale-issue-disposition-2026-11-02 に節を追加、定例下書きに 1 行

## [2026-11-02 14:08] filing-back | 棚卸しの承認済み操作を nishio が実行、30 件 close・コメント 19 件・PR #1177（open 96 → 66）

- nishio が手元で `raw/issue-audit/2026-11-02-actions/run.sh` を実行し、49 操作すべて成功。close 30（A 9・B 12・統合 4・#285 #869 #1128 #56 #518）、親への転記 4、open 維持の追記 7、assignee 確認 8（期限 2026-11-16）。Cold List 運用ルールの PR は #1177、docs の openrouter 抜けは #1176
- 状態を GitHub で照合（30 件 CLOSED、#454 コメントに PR URL あり）。analyses/stale-issue-disposition-2026-11-02 と 10-28 棚卸し、定例下書きに結果を反映
- 次：#1176 / #1177 の merge、本人判断 3 件（#370 実データ、#879 時刻列、#994 実 LLM 1 回）、11-16 以降に無反応 assignee 分の既定処理（#337 色マップ・#643 build-arg 削除の PR、#324+#170 / #310 / #280 / #809 の close、#547 unassign）

## [2026-11-02 14:02] filing-back | 停滞 Issue 56 件の処し方を nishio が全件承認、PR #1176 作成、close / コメント投稿は手元実行待ち

- レビュー用ページ（判断を保存できる artifact）で 56 件すべて「承認」。承認分のうち docs の抜け（#285: CLI の provider 一覧に openrouter）を PR #1176 に、Cold List 運用ルール（#454）を `docs/454-cold-list-policy` branch の commit に用意
- GitHub への close 30 件・コメント 19 件と #454 の PR 作成は Claude Code の権限判定（外部システムへの書き込み）で止まった。実行 script と dry-run を `raw/issue-audit/2026-11-02-actions/` に置き、nishio が手元で実行する
- 次：実行結果を wiki に反映、2026-11-16 以降に assignee 無反応分の既定処理、#994 は nishio の実 LLM 1 回

## [2026-11-02 08:59] filing-back | 更新停滞順に open Issue 96 件を見直し、18 か月停滞の 42 件に処し方と close コメント案を付けた

- nishio の「最近更新のない Issue から順にどうすると良いか考察」。10-28 棚卸し以降 close は 0 件で 96 件。最終更新の古い順に並べ、停滞 42 件を close 25（完了・動機解消 9 / not planned 12 / 親に統合 4）、assignee 確認 10（期限 2026-11-16、無反応時の既定処理つき）、open 維持 7 に振り分け、貼れるコメント案を analyses/stale-issue-disposition-2026-11-02 に置いた
- Cold List 運用のルール案（12 か月更新なし・assignee なし・要件未具体化 → 棚卸しで not planned close、bot は入れない）で PROJECTS.md の TBD を埋めれば #454 も close できる。2026-05〜09 更新の 11 件は短い所見、2026-10 の 43 件は即 close 可能な 3 件（#1128 / #56 / #518）だけ挙げた
- GitHub への書き込みはなし。次：nishio が 25 件の一括 close と確認コメント 9 通を実行するか判断、AI は PROJECTS.md の PR draft と E 群の追記案を用意する
