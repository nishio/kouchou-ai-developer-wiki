# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

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

## [2026-10-21 23:00] filing-back | 第 3 弾レビューの GitHub 側の指摘: Issue 16 件を更新、cli-quickstart の例を直す PR #1059

- 現状と残件を日付つきで追記: #56・#266・#292・#464・#496・#881・#885・#912・#913・#44・#638・#1012 にコメント、#921・#949 は本文末尾に追記（元の本文は保持）。書き込み直前に更新時刻を照合し、書き込み後に取り直して確認。
- #211（OOM で処理中のまま固まる）と #295（rate limit）は、満たした範囲と残件を書いて close。#295 の Tier 周知は #292 に引き継いだ。#496 と #638 は閉じずに相互リンク。
- cli-quickstart §9 の例から `cluster_nums` の固定値を外す PR #1059 を作成（未 merge）。gotchas に再発として記録。#976 の載せ替えは出す時期の判断待ち。

## [2026-10-21 19:10] filing-back | 第 3 弾レビューの修正 PR 11 本を merge（#1048–#1058）

- nishio が admin merge。merge 後の main（b675e032）で analysis-core 422 件・api 392 件のテストが通ることを手元で確認。
- main の push CI は、連続 merge のため一部のコミットでしか起動しなかった（起動した分はすべて success）。
- 定例会議向け下書き（meeting-report-draft）を merge 済みに更新。

## [2026-10-21 18:30] filing-back | 第 3 弾レビューの未報告候補の残り 8 件を修正 PR に（#1051–#1058）

- 手順書の環境変数名、タイムアウトの空欄、OpenAI キー無しで API が起動しない件、OpenRouter のフェンス付き JSON、CI の対象パス、api のテストが手元のレポート一覧を消す件、Docker で GA が CSP に止められる件、何も確かめていなかった E2E。
- それぞれ現行 main で再現してから直し、直す前のコードでテストが落ちることも確かめた。#1048–#1050 と合わせて 11 本が未 merge。
- 定例会議向け下書き（meeting-report-draft）を更新。

## [2026-10-21 16:30] filing-back | 第 3 弾レビューの未報告候補 3 件を修正 PR に（#1048–#1050）

- 利用上限で途中終了した調査の記録にあった候補を現行 main で再現し、PR にした。テストが .env のキーで実際に LLM へ要求を送る（#1048）、pip で入れた CLI が作業ディレクトリの .env を読まない（#1049）、api のテストが 2027-01-01 以降に必ず落ちる（#1050）。
- 週次枠が均等ペースより先行していたので、ワークフローは使わず 1 セッションで確認・修正した。
- 定例会議向け下書き（meeting-report-draft）を更新。

## [2026-10-21 13:30] filing-back | 第 3 弾レビューの Wiki 指摘を訂正（約 70 件）、#NNN リンク化の破損を修復

- living ページ（concepts / entities / gotchas / open-decisions / index など）の古い・誤った記述を main と GitHub に照合して訂正。日付つき snapshot は ## Updates で訂正。
- 一括リンク化（dd19e9d）で入れ子になったリンク・広聴AI 以外の番号への誤リンクを修復。scripts/linkify_github_refs.py を冪等にしてテストを追加し、素のまま残っていた #NNN もリンク化。消えていた Yandex 検証ページの結論と log entry を復元。
- 公開境界（デモ環境の構成・認証まわりの詳細、個人 PC のパス）と、公開ページに残っていた下書き表示・編集メモを除去。CLAUDE.md の文言の食い違い 2 件（Slack mirror の窓、二分原則の書き方）は nishio 判断として残した。

## [2026-10-21 12:40] filing-back | 第 3 弾レビューの回帰修正 PR 5 本を admin merge（#1043–#1047）

- #1031・#1033・#1034・#1039 で入った／広がった不具合 6 件を #1043（--reuse-from とトークン引き継ぎ）・#1044（再利用で全段再実行）・#1045（完了後もカードが作成中）・#1046（濃い意見 0 件の切り替え先）で修正。nishio「CI が通ったら admin merge」で squash merge。
- #1043 と #1044 が合わさって落ちたテストの前提を #1047 で直し、main の Server Tests green を確認。CodeRabbit の範囲外の指摘 2 件は後続で扱う。
- [[meeting-report-draft]] を更新。
