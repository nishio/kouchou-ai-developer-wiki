# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

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

## [2026-10-29 21:30] filing-back | 関連研究の紹介ページを本体 docs の PR #1174 として作成（#1173）、wiki に記録

- open-decisions A14 の残作業だった「docs から成熟していない関連研究として紹介する」ページを `docs/development/related-research.md` として作成。センチメント次元の付与・DivCon・farbrain を所在 / 状態 / 担当 / 最終確認日つきで載せ、本体の属性ステップ（#1158）と `llm_grouping` との関係を書いた
- 2026-06 の実験的機能カタログ提案の「最終確認日」ルールを初めて本体 docs で実装。所在 URL は同日に到達確認
- #1168（httpx 未宣言）は PR #1171 で main 入り。直接関係ないので考察ページと定例下書きの記述だけ更新
- 次：tokoroten さんへの確認と merge 判断（人間）。記録は [[post-review-direction-issues-2026-10-29]] 4 節、[[open-decisions]] A14

## [2026-10-29 20:30] filing-back | open-decisions A14 に nishio の方針（本体に取り込まず docs で関連研究として紹介、入れるなら CLI から）を追記

- tokoroten の 2 手法（センチメント次元の付与・DivCon）は本体に取り込まず、docs から「成熟していない関連研究」として紹介する。入れるとしても CLI から。考察ページの順序 5・6 と定例下書きも合わせて更新
- 残る作業は docs 側の紹介ページ（要点・pointer・最終確認日・属性ステップとの関係）。主担当と評価データの確認は CLI で試す段階になってから

## [2026-10-29 20:10] filing-back | open-decisions A13 に付箋表示の置き場の暫定意向（standalone HTML と Web plugin の両方）を追記

- nishio の「A13 は standalone HTML と Web の可視化プラグインかな」を暫定の意向として A13 に記録（Kozaneba 側には置かない。確定と着手順は未定）
- 先に決めるのは結果 JSON からの書き出し契約、という考察の整理に接続

## [2026-10-29 19:00] filing-back | 考察の 1〜3 を Issue 化して着手（#1158〜#1160 → PR #1165〜#1167）、副産物 #1168

- post-review-product-direction の順序 1〜3 を Issue 化（assignee 設定済み）し、worktree ごとに実装して同日に PR 作成（未 merge）。(1) 賛否・新規性の属性ステップ（analysis-core、848 tests green、実データ 997 件で新規性 smoke）、(2) 階層リストの詳細モード化＋目的ツールチップ＋出典リンク（public-viewer、46 suites green）、(3) 同梱テスト用レポート 5 view のギャラリー docs（静的ビルドを Playwright で撮影）
- 設計判断・検証・人間に確かめてほしい点は analyses/post-review-direction-issues-2026-10-29。open-decisions A13・A14 と meeting-report-draft に反映
- 副産物: lock なしの analysis-core が `import httpx` で落ちる件を #1168 に。次は 3 本の merge 判断と、#1165 後に属性つきギャラリー例を足す

## [2026-10-29 16:30] filing-back | スプリント第 1 群 4 件を PR 化（#1161〜#1164）、#1128 は #1154 で対応済み

- 10-28 棚卸しの第 1 群 5 件に着手。#292 docs→#1161、#493 散布図ホイール→#1162、#1130 エラー詳細→#1163、#79 費用概算→#1164 を issue ごとの worktree で並行実装し PR 作成（未 merge）。着手前に nishio を assignee に設定
- #1128 は別セッションの #1154 で本体修正が merge 済みだったため着手せず。#1163 と #1164 は CreateReportConfirmation を両方触るので後の方を rebase
- 各 PR で AI が置いた仮定と人間に確かめてほしい点（費用係数の較正、600ms の操作感、unknown_error 限定の詳細表示、docs の残件）を analyses/sprint-group1-prs-2026-10-29 に記録。次は #1161 の CodeRabbit 指摘対応と merge 判断

## [2026-10-29 15:29] filing-back | PyPI の analysis-core 0.3.0 を公開（polars 2 で 0.2.0 の集計が失敗する件）

- #1168 の確認中に、PyPI の 0.2.0 が lock なしだと polars 2 に解決され集計で毎回失敗すると判明。#1171 で直し、#1172 で 0.3.0 に上げてタグを push、公開後に lock なしで動作を確認。gotchas と定例の下書きに追記。

## [2026-10-29 15:10] filing-back | PR #1165 を main に rebase、CodeQL 指摘を修正して merge 待ち

- nishio の「#1165 merge して」を受け、main（#1171 / #1172 の analysis-core 修正）との spec JSON の conflict を解消して rebase。CodeQL の「`value != value`」指摘は `math.isnan` に直した。ruff とテスト 852 件 green、CI も green（d86f56da）
- admin merge は Claude Code の権限判定で止まるので、merge 自体は nishio が手元で実行する。次：merge 後に #1167 を含む残り 2 本（#1166 / #1167）の merge 判断

## [2026-10-29 14:30] filing-back | PR #1166 を #1155 merge 後の main に rebase

- #1155 merge で CONFLICTING になった #1166（階層リストの詳細モード化）を rebase。`HierarchyListChart` と plugin で、元コメント本文（#1155）と出典リンク（#1166）の両方を残す形で解消し、tsc / biome / viewer テスト 317 件 green。force-with-lease で push（7450a17c）、MERGEABLE に戻った
- 次：#1166 の CI 確認と merge 判断（提案順 #1165 → #1166 → #1167）

## [2026-10-29 14:10] filing-back | PR #1155（#56 元コメント表示）の CodeRabbit 対応と merge を記録

- CodeRabbit の指摘 2 件（再利用画面で `ReportConfig` が flag を落とす、ホバー文の二重エスケープ）を直して push 後、CI green を確認。admin merge は Claude Code の権限判定で止まり、nishio が手元で squash merge（8e95ceb1）
- analyses/issue-56-original-comments-opt-in-2026-10-29 と meeting-report-draft、issue-backlog-audit-2026-10-28 を merge 済みに更新。`work/kouchou-ai` の main を最新化し、worktree を片付け
- 次：#56 を close するか（残件は per-comment 再頒布フラグと #1156）、shingo-ohki への返信、#1166 の rebase

## [2026-10-29 03:00] filing-back | PR #1155 に利用ガイドの追記を push、GitHub 側の新着なしを確認

- PR #1155 はレビュー・コメントともに未着。CI の how-to-use リマインダー（WebUI 変更で利用ガイド未更新）だけ残っていたので、`docs/user-guide/how-to-use.md` に「元コメントの確認」を追記して push。
- #56 / #1156 にも新しいコメントは無し。次：PR の review / merge。

## [2026-10-29 02:30] filing-back | 「多対多参照とは何か」の回答を #56 の analysis ページに補足

- nishio の問いに答えた「本体は 1 対多（#1032 以降は回答と文面の組で重複判定）、多対多は serverless 版が同じ文面の意見を回答をまたいで束ねる構造、serverless PR #22 の ID 誤対応はその経路」の説明を [[issue-56-original-comments-opt-in-2026-10-29]] に節として追記。
- 次：PR #1155 の review / merge。設計変更は #1156 で扱う。

## [2026-10-29 02:00] filing-back | #56 からデータ構造の設計変更を #1156 に切り出し

- nishio が #56 に「設計としては serverless 版のように同一内容コメント・同一意見を束ねた方がよいが、まず現状構造で元コメント表示を実現し、設計変更は別 Issue」とコメント。指示を受けて [#1156](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1156) を作成（束ね方の基準、`comment_ids` への拡張、`comment_id` の型揃え、serverless との契約統一、#250 の表示）。
- [[issue-56-original-comments-opt-in-2026-10-29]] と定例 draft の #56 項目を更新。次：PR #1155 の review / merge。

## [2026-10-29 01:30] filing-back | #56 元コメントの表示をレポート単位 opt-in で実装し PR #1155 を作成

- shingo-ohki の 10/28 コメント（url 列が無いと抽出意見止まり）を受け、現行 main `1028da9c` を照合。`comments` は空のまま、`_build_comments_value` は dead code と確認。公開可否の契約を「レポート単位 opt-in」と「per-comment フラグ」の 2 案に分け、nishio が前者を選択。
- worktree `work/kouchou-ai-issue-56` で analysis-core / api / admin / viewer / docs を実装し、PR [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155)（未 merge）。テストは analysis-core 798 / api 72 / viewer 314 / admin 117 が通過。判断と残論点は [[issue-56-original-comments-opt-in-2026-10-29]]。
- 次：PR の review / merge と、#56 を close するか残件（多対多・serverless 契約・#250）を別 Issue に切るかの判断。shingo-ohki への返信は未投稿。

## [2026-10-29 01:26] filing-back | 入力 plugin の依存、構造化出力の usage、override のメジャー版、CodeRabbit の check を記録

- plugin-system に「入力 plugin の依存は本体のイメージに入るかで考える」節（#1149 の経緯）を追加。gotchas に、parse が弾いた応答の usage（#1154）・override でメジャー版をまたぐときの確かめ方（#1153・#1157）・CodeRabbit の check がレビュー済みを意味しない場合を追記。
- versioning-strategy に v4.2.1 を出さない判断と、タグとリリースを対にする慣行を、security-maintenance に今回の alert 対応を追記。

## [2026-10-29 00:35] filing-back | Dependabot の alert 3 件（#1153）とトークン数の数え漏れ（#1154）を merge

- `follow-redirects`・`zod` を override で上げて alert 3 件を解消。merge 直後に新しい alert 2 件（開発用の道具経由）が出た。#1128 の修正で、弾かれた応答と諦めた回答のトークン数も集計に入るようにした。定例の下書きに追記。

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
