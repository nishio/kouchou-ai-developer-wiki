# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-10-29 01:30] filing-back | #56 元コメントの表示をレポート単位 opt-in で実装し PR #1155 を作成

- shingo-ohki の 10/28 コメント（url 列が無いと抽出意見止まり）を受け、現行 main `1028da9c` を照合。`comments` は空のまま、`_build_comments_value` は dead code と確認。公開可否の契約を「レポート単位 opt-in」と「per-comment フラグ」の 2 案に分け、nishio が前者を選択。
- worktree `work/kouchou-ai-issue-56` で analysis-core / api / admin / viewer / docs を実装し、PR [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155)（未 merge）。テストは analysis-core 798 / api 72 / viewer 314 / admin 117 が通過。判断と残論点は [[issue-56-original-comments-opt-in-2026-10-29]]。
- 次：PR の review / merge と、#56 を close するか残件（多対多・serverless 契約・#250）を別 Issue に切るかの判断。shingo-ohki への返信は未投稿。

## [2026-10-28 22:30] filing-back | 新スプリント開始：open Issue 全 89 件を古い順に現行 main と照合し、方針を判定

- nishio「10/28 からの新しいスプリントとして、既存 Issue を古い方から確認して現在の状況と照らし合わせ、どうするかを検討する」を受け、dynamic workflow（12 シャード照合 → 懐疑検証、agent 23）で全 89 件を main `1028da9c` に照合した。前回 10-12 以降の 167 commit で動いた件を更新。結果は [[issue-backlog-audit-2026-10-28]]、方法と未確認範囲は [[issue-audit-2026-10-28-sprint]]。前回ページには superseded の目印を付けた。
- 今スプリント実装候補 19 / close 候補 4 / 統合 4 / 人間判断 40 / 保留 22。懐疑検証で 11 件を「実装・close」から「人間判断・保留」へ戻した（他 assignee あり、製品方針の先取り、size の過小評価）。GitHub への書き込みは未実施。
- 次：第 1 群 5 件（#79 費用概算、#292 課金と 429 の docs、#1128 再試行のトークン数、#493 スクロール拡縮、#1130 接続チェックのエラー詳細）から着手するかを nishio が判断。close 4 件・統合 4 件・停滞 assignee への確認は定例の議題候補に載せた。

## [2026-10-28 19:30] filing-back | 考察：レビュー後の広聴AI は何がどうなるとよいか

- nishio「これらを踏まえて何がどうなるとよいか考察したい」を受けて [[post-review-product-direction-2026-10-28]] を追加。宙に浮いた 5 つ（階層リスト・付箋表示・センチメント次元・DivCon・farbrain）を「view」と「意見ごとの属性」の 2 軸に分解し、既定は散布図のまま、view は目的別 plugin、属性は CLI の任意ステップ、という形に収束させる案。
- 順序は、賛否・新規性の属性ステップ → 階層リストの詳細モード正式化 → 同一コーパスの全 view ギャラリー → 付箋表示の CLI artifact → 埋め込み重み付けの clean experiment → DivCon を mode として別設計。レビューの教訓（出口で検査、結果 JSON 丸ごと埋め込みの構造）を制約として明記。定例下書きの議題候補にも追記。

## [2026-10-28 17:40] filing-back | 振り返りページの訂正：ドリルダウンのツリー表示はチームみらいの階層リスト、farbrain を追記

- nishio の指摘「ドリルダウンはチームみらいでやった可視化」を受けて [[retrospective-2026-10-28]] の 2-a を書き直した。2025 年参院選の policy-pr-hub で Devin が作った階層 bullet list（最下層で個別意見と PR リンク）が元で、2026-01 に公開ビューアの可視化 plugin「階層リスト」として移植済み。「提供してもウケない」（2025-10-31）と「全部読むならツリービュー向き」（2026-05-30）の両方の観測を並べ、「詳細モード」の正式 view にするかを未決として整理。
- tokoroten の farbrain（埋め込み → UMAP → k-means → 凸包 → LLM 表札をリアルタイムで回すブレストツール）を 3 節に付記。自分の投稿のハイライトと新規性スコアが広聴AI に持ち込める要素。open-decisions A13 と定例下書きも合わせて訂正。

## [2026-10-28 16:30] filing-back | 2026-10 の経緯の整理：大規模レビュー → 鍵漏洩の修正 → v4.2.0、残った可視化 2 つと tokoroten の 2 手法

- nishio「今回の経緯について LLM Wiki にまとめる」を受けて [[retrospective-2026-10-28]] を追加。10-16〜10-26 のレビュー 4 段（修正 PR 100 本超、全件 merge 済み）、鍵漏洩の発見・猶予・公開・v4.2.0 を 1 本の流れと教訓にまとめた。
- 宙に浮いた可視化 2 つ（ドリルダウンのツリー表示＝10-17 の Claude 実験の再クラスタリングと #880、ズームできる付箋表示＝canvas_kozaneba_prototype）と、tokoroten の賛否分離 2 手法（センチメント次元の付与・DivCon）の取り込み順を整理。open-decisions に A13・A14、定例下書きの議題候補、index に追記。
- 次：2 つの可視化の置き場と、tokoroten の 2 手法を本体に入れるか・主担当を nishio が判断。該当の推定（どの試作を指すか）も要確認。

## [2026-10-26 23:46] filing-back | YouTube プラグインを google-api-python-client なしで動かす（#1149）

- v4.2.0 の Docker イメージで YouTube の取り込みが失敗する件。lock に extra を入れる案から、httpx で REST を直接呼ぶ形に作り直して merge した（beff715f）。プラグインだけが使う依存を本体に入れないため。定例の下書きに追記。

## [2026-10-26 21:40] filing-back | ユーザー API キーの件の Security Advisory を公開

- nishio が GHSA-xr6j-6w48-xh62 を公開した（Moderate、CVE なし）。公開前に、対象が作成画面の任意の「APIキー」欄であり、空欄なら影響なしと冒頭で示すよう、Advisory・リリースノート・docs（#1148）・wiki をそろえた。
- リリースノートに Advisory へのリンクを足した。詳細は [[user-api-key-leak-2026-10]]。

## [2026-10-26 20:39] filing-back | v4.2.0 と analysis-core 0.2.0 をリリース

- 保留していた修正と依存の脆弱性の解消を、CodeRabbit の指摘を直したうえで順に merge し、v4.2.0 のタグとリリースを作った。冒頭はセキュリティ修正と設定の変更点。
- PyPI の analysis-core 0.1.3 にも鍵の漏洩が含まれていたので、0.2.0 を公開した。Security Advisory は Moderate で下書き、公開は nishio。詳細は [[user-api-key-leak-2026-10]]。

## [2026-10-26 15:30] filing-back | ユーザー API キーの漏洩を公開：修正 #1136 を merge、wiki ページを追加

- 猶予期間が明け、nishio の指示で公開作業を始めた。修正 #1136 を最新の main に載せ替え、CodeRabbit の指摘 4 件を直して merge した。同じ期間に保留していた修正 #1132・#1135 も merge 済みで、#1133・#1134 はレビュー待ち。
- [[user-api-key-leak-2026-10]] を追加した。影響範囲は今のコードと照合して、公開前の調査メモより絞って書いた。gotchas・security-maintenance・code-health-review と、過去の記述 2 ページにリンクと追記を足した。

## [2026-10-26 13:40] filing-back | #1024 を merge して #1023 を close、#1129 を merge、#912 を close して残件を #1131 に

- #1023 の a/b は a（#1024）を採用した。最新の main に rebase し、変更を memo 化後の位置に当て直して merge した。#1025 は close。
- shingo-ohki さんの #1129（OpenAI 4 モデルを検証済み、o3-mini を提供終了）を merge した。
- #912 は完了条件と照合して close し、料金・service_tier・請求額の照合などの残件を #1131 に引き継いだ。

## [2026-10-24 12:30] filing-back | #1079 と #1061 を merge、#1119 の残課題を Issue #1128 に

- #1079 は最新の main に rebase し直してテストを確かめ、nishio が merge した。修正 PR 65 本はすべて merge 済み。
- #1061（yasumorishima さん）は最新の main と照合してレビューし、merge した。軽微な修正は後でこちらが行う。#1119 の CodeRabbit の指摘は #1128 にした。

## [2026-10-24 04:45] filing-back | 第 3 弾レビューの修正 PR 64 本を CodeRabbit を見ながら admin merge

- nishio の指示で 3 陣に分け、1 本ずつ merge した。衝突は事前に書いた方針で rebase して解き、CodeRabbit の実際の指摘（10 件ほど）は commit を足して直した。
- merge 後の main bdc3e469 で、4 種のテストと CLI の通しを確認した。#1079 は権限判定で止まっていて、nishio の判断待ち。台帳は raw の merge-2026-10-24/ledger.md。

## [2026-10-24 00:45] filing-back | Next.js 16.4.2 への更新 #1127 を admin merge

- CI（E2E を含む）がすべて通った後、nishio の指示「CI が通ったら admin merge して」で squash merge した。main `23acd411`。

## [2026-10-24 00:30] filing-back | Next.js を 16.4.2 に上げる PR #1127

- 「上流がまだ直していない」とされていた Next.js の 10/22 の勧告は、16.4.1 で修正済みで、こちらの対応待ちだった。Dependabot の alert にもまだ出ていない。
- nishio「go」を受けて #1127 を作成した。lockfile の差分は next と @next/* だけ。両アプリのビルド・テストと、CI と同じ手順の shell / static の書き出しを確認した。定例会議向け下書き（meeting-report-draft）にも追記。

## [2026-10-23 23:59] filing-back | 第 3 弾レビューの続き（最後）：管理画面の本番ビルドを実ブラウザで検査、修正 PR を #1126 まで

- 深夜の PR の独立レビューで、#1118・#1119 に commit を足した。
- 管理画面の本番ビルドを実ブラウザで操作し、約 10MB を超える CSV からレポートを作れない件を見つけた（#1124、medium）。ほかの 2 件は #1125・#1126 にした。
- 週次枠は月〜火の分を残して止めた。詳細は [[code-review-r3-continuation-2026-10-23]] の Updates。

## [2026-10-23 22:40] filing-back | 第 3 弾レビューの続き（深夜）：批評ラウンドの 2 回目と旧バージョンの互換性、修正 PR を #1123 まで

- 夜の 13 本の独立レビューで、#1113 の Azure の判定を直した。確定済みで未修正だった 3 件（LLM 直接グルーピングの並列化など）を #1118–#1120 にした。
- 批評ラウンドの 2 回目で、PR レビューの抜けと、旧バージョンのレポートの互換性を見た。9 件が確定した。既存の PR 3 本に commit を足し、旧レポートの 3 件を #1121–#1123 にした。
- 詳細は [[code-review-r3-continuation-2026-10-23]] の Updates。

## [2026-10-23 20:55] filing-back | 第 3 弾レビューの続き：PR の独立レビューと残りの 2 観点、修正 PR を #1117 まで

- 独立レビューで 9 件が確定した。#1079・#1084 には commit を足して直し、クラスタ一覧の再描画は #1105 にした。#1060 への指摘は作者に伝えた。
- nishio「そのまま残りの 2 観点も回しといて」を受けて、LLM プロバイダの組み合わせと、分析結果の不変条件を洗い出した。12 件すべてが確定し、#1106–#1117 にした。
- 詳細は [[code-review-r3-continuation-2026-10-23]] の Updates。定例会議向け下書き（meeting-report-draft）も更新した。

## [2026-10-23 19:30] filing-back | oss_weekly_reporter の更新停止と Slack 本文の埋め戻しを反映

- `nishio/oss_weekly_reporter` は 2026-10-22 に workflow を無効化（単独の Slack 抽出 workflow は一度も成功しておらず、週次レポート側が Slack 込みで動いていた。Slack 本体は `digitaldemocracy2030/slack-logs` に移行済み、週次要約・GitHub スナップショットは今後使わないと nishio が判断）。data ブランチは 2026-10-21 週までの凍結アーカイブ。
- reporter にしか無かった Slack 本文は slack-logs PR #10・#12 で `raw/` に全部入った。CLAUDE.md / README / [[local-dev-setup]] / [[wiki-driven-workflow]] / [[slack-logs-repository]] の参照を「過去分のみ」に更新。以降の GitHub activity は live state を見る。

## [2026-10-23 18:50] filing-back | 第 3 弾レビューの続き：残りの洗い出し 4 観点と未検証 43 件を仕上げ、修正 PR 43 本（#1062–#1104）

- nishio「土日に仕事したくないから多めに使っといて」を受けて、利用上限で残っていた範囲を main b675e032 で仕上げた。洗い出しは、テストの質・ドキュメント・設定・規模の 4 観点で 23 件、うち 22 件が確定。未検証 43 件は 39 件が確定し、4 件が反証された。
- 確定した指摘を、指摘ごとに main から別ブランチで修正し、PR にした（どれも修正前に落ちるテストつき、未 merge）。詳細は [[code-review-r3-continuation-2026-10-23]]。
- 次：merge 前の独立レビューを実行中。挙動の判断が要る PR は数本ある。定例会議向け下書き（meeting-report-draft）を更新。
