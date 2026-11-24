# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-11-25 00:10] filing-back | civic.ai（6-Pack of Care）のソース要約ページを足した

- トップと Pack 1〜6 の要約、広聴AI との接点（言及なし・日本は 2 か所）、提案と実績を区別する注意。未読ページは coverage に明記
- 更新: [[public-web-civic-ai-6pack-of-care-2026-11-24]]、[[civic-ai-6pack-docs-mapping-2026-11-24]]

## [2026-11-24 23:59] filing-back | org fork のブラウザ版を GitHub Pages で公開した

- digitaldemocracy2030/kouchou-ai-serverless の Pages を有効にし、main をデプロイ。サンプルレポートの描画とコンソールエラー無しを確認
- 本体 docs のリンクはまだ tokoroten 版。更新: [[serverless-integration-options-2026-11-24]]

## [2026-11-24 23:55] filing-back | ブラウザ版を dd2030 org に fork し、本体との適合性テストで 22 点のずれを見つけた

- digitaldemocracy2030/kouchou-ai-serverless を作成（nishio 指示で移管ではなく fork）。本体の analysis-core を実際に動かして期待値を作るテストを fork の PR #1 に（未 merge）
- 54 件中 32 件一致。ずれは上位クラスタの分け方（ward.D / ward.D2）、元コメント本文の既定公開、同じ文面の意見のまとめ方、壊れた応答を概要・ラベルにそのまま使う点など
- 更新: [[serverless-integration-options-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 23:50] filing-back | Civic AI（6-Pack of Care）の観点で docs を点検し、公開後に止める・直す手順と大量投稿への注意を PR #1234 にした

- civic.ai に広聴AI への言及は無いが、broad listening・Polis・Community Notes を例に使い、観点は大きく重なる。docs は遡れること・ローカル完結が厚く、止め方・直し方・異議の受け方と大量投稿への注意が無かった
- 管理画面の削除はファイルを消さない、再利用では入力を差し替えられない、などをコードで確かめて書いた。未 merge
- 更新: [[civic-ai-6pack-docs-mapping-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 23:30] filing-back | ブラウザ版（serverless）の取り込み方を 3 案で比べ、repo 移管＋契約合わせを推奨

- org への repo 移管／本体 monorepo への統合／結果形式だけ合わせる、を両 repo の main で比較。統合しても分析処理は TS と Python の 2 本のままで、道具の世代差（pnpm・TS・Biome）と Pages の相乗りが重い
- ブラウザ版のサンプル JSON は本体の validate_output で問題 0 件。ただし build_public_result が元コメントをそのまま写すので、既定 off（#1155）を素通りする
- 移管は tokoroten にしか実行できない。更新: [[serverless-integration-options-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 23:00] filing-back | Lean の検証で見つかったものをすべて直す PR #1227〜#1230 を作った

- 無効に戻したら集計を再実行（#1227）、依存の宣言の検査（#1228）、llm_grouping の id "0" の拒否（#1229）、入れ子でない階層クラスタで止める（#1230）。いずれも未 merge
- どれも直す前のコードで追加テストが落ちることを確認、analysis-core 全体と ruff check は通過
- 更新: [[lean-verification-trial-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 21:35] filing-back | fork の PR #1 merge と Pages を main に揃えたことを反映し、関連ページをつないだ

- PR #1 は 20:29 に nishio が merge 済みだった（wiki は「未 merge」のままだった）。取り消されていた main のデプロイを再実行し、Pages を `d15fb57` に揃えた
- 別セッションの実装調査 [[serverless-implementation-2026-11-24]] と取り込み方の検討をつなぎ、tokoroten の人物ページと index.md にブラウザ版を足した。fork の PR #2（差の修正）は進行中
- 更新: [[serverless-integration-options-2026-11-24]]、[[meeting-report-draft]]、[[tokoroten]]

## [2026-11-24 21:31] filing-back | 未解決 Issue から CLI の HTML 出力設定と小さな修正候補を選んだ

- 未解決 70 件と進行中 PR 7 本を確認し、[#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954) を通常の階層クラスタリングと LLM grouping の設定検証で再現。課金案内 [#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292) は管理画面のリンクが残る。
- 公開用 JSON [#1178](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1178) の実装と関連テストを確認。v5.0 の公開契約の告知が残る。更新は [[issue-resolution-candidates-2026-11-24]] と [[meeting-report-draft]]。

## [2026-11-24 21:31] filing-back | org serverless PR #2をCI全成功後にmergeしmainの成功も確認

- nishioの承認でPR #2をsquash merge（main `2341235`）。最終headのCI全成功・merge可能・未解決レビューなしを確認した。merge後mainのCIも成功
- local cloneをmainに追従。Wikiへの並行更新も取り込み、PR作成時点の未merge記録を残したまま完了を追記した
- 更新: [[serverless-implementation-2026-11-24]]、[[serverless-integration-options-2026-11-24]]、[[meeting-report-draft]]。既知の差10項目と実LLM品質は残る

## [2026-11-24 21:30] filing-back | analysis-core の判定ロジックを Lean で検証し、意見分類を無効に戻すと古い結果が残る不具合を見つけた

- 依存解決・再実行の判定・クラスタの木の組み立てを Lean に写して証明し、本物の Python との差分テスト（各 1500 件）でモデルのずれが無いことを確かめた。検証一式は実験ブランチ（未 push）
- 見つかったこと：意見分類などを無効に戻すと集計がスキップされ古い分類が残る（CLI のみ）、spec が依存順という前提が未検査、`validate_dependencies` が存在しない依存で例外を投げる
- 更新: [[lean-verification-trial-2026-11-24]]、[[testing]]、[[meeting-report-draft]]

## [2026-11-24 21:25] filing-back | serverlessの回答対応・失敗復帰・公開範囲を修正しorg PR #2を作成

- org PR #2（`codex/serverless-correctness-and-public-output`）を作成。回答単位の意見保持・ward2・失敗結果のキャッシュ防止・元コメント既定OFFと公開JSON/HTMLを実装。未merge
- テストは292成功・既知差10件、lint・build成功。ブラウザで既定OFF/明示ON・JSON/HTML出力・HTML単体表示・旧工程キャッシュ拒否を確認。実LLM品質は未検証
- GitHub CIのlint・test・buildと本体からの期待値再生成も成功。更新: [[serverless-implementation-2026-11-24]]、[[meeting-report-draft]]。証跡は `raw/serverless-fixes-2026-11-24/`。次はPRの確認

## [2026-11-24 21:03] filing-back | serverlessの実装を3経路で調べ、本体との差と失敗の扱いを整理した

- org main `d15fb57e` と本体 main `a775d3d2` を取得。適合性テストPR #1のmerge済みを確認し、通常分析・対話的再クラスタリング・賛否スペクトラムの実装を整理
- 同文の別回答の属性が初出に寄ること、元コメントの既定同梱、ラベル失敗のキャッシュ、賛否スペクトラムの抽出失敗を空結果として保存する経路を記録。固定重心7ケースは現行wardで5件、ward2で7件一致
- 通常成功253件・既知不一致22件、lint・build成功。偽APIでラベル失敗と賛否スペクトラムの失敗回答が再実行でもキャッシュされることを再現。証跡は `raw/serverless-implementation-2026-11-24/`
- 更新: [[serverless-implementation-2026-11-24]]、[[serverless-integration-options-2026-11-24]]、[[meeting-report-draft]]。graspの書込用journalがないため、既存のMarkdown運用で追記

## [2026-11-24 20:00] filing-back | 研究会の作業で踏んだ落とし穴を gotchas に、利用者定義ラベルを pipeline に入れた

- [[gotchas]]：管理画面の「再利用」は入力も引き継ぐ／`prompt_file` は検査を通るが読まれない／意見分類のラベル ID が属性名になり同名の入力属性を上書き／`git -C` の worktree パス／Next.js 16.4 の `next dev` の初回停止
- [[pipeline]]：`opinion_classification` の利用者定義ラベル（PR #1232）

## [2026-11-24 19:40] filing-back | 意見分類の利用者定義ラベル（#1232）を main に入れた

- nishio が手元で admin merge（`a775d3d2`）。#1210・#1213 に設定例、#1225 に入ったものと残件（ビューアでのラベル名など）をコメント
- 更新: [[municipal-workshop-issues-triage-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 19:10] filing-back | 意見分類のラベルを利用者が定義できるようにする PR #1232 を出した（#1225）

- `labels` に利用者定義のラベルを書け、プロンプトは定義から組み立て、誤りは実行前に止まる。社内の gemma-4-31B で 3 ラベルの分類を確認。未 merge
- 残件：ビューアでラベル名を出す、入力の同名属性の上書き。別件で `prompt_file` が読まれていないことに気づいた
- 更新: [[municipal-workshop-issues-triage-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 18:25] filing-back | ミューテーションテストを再実行の判定と集計に広げ、管理画面に響く穴を見つけた

- `core/orchestration.py` と `steps/hierarchical_aggregation.py` で 2,832 変異、テストが気づいた割合 71.5%（本体は変更なし、main `2a924af6`）
- 本番経路の生存 605 件を 3 領域に分けて仕分け、約 135 件が本番の穴。上位はラベル編集後の再集約（`--only`）、管理画面の config の検証、期限切れロック、結果 JSON のクラスタ ID・元コメント
- 旧経路（`run_step` / `termination`）の 152 件は Python API を残すかの判断待ちで未仕分け
- 更新: [[mutation-testing-orchestration-aggregation-2026-11-24]]、[[mutation-testing-trial-2026-11-24]]、[[testing]]、[[meeting-report-draft]]

## [2026-11-24 18:10] filing-back | #1220 を main に入れた

- nishio の指示で admin merge（squash、main `2a924af6`）。merge 前に CI 全件 pass・CodeRabbit の指摘なし、merge 後の main も全件 success
- 更新: [[mutation-testing-trial-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 17:45] filing-back | #1220 の CI が全件通り、ミューテーションテストの知見をテスト体系のページに入れた

- [#1220](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1220)（穴 3 つを塞ぐテスト）は CI 全件 pass、未 merge。merge 判断で見る点（名前の並びを固定する実装寄りのテスト 1 本）を分析ページに残した
- [[testing]] に、mutmut を使う時の設定（forkserver 方式）と、生存した変異の選び方を追記。分析ページへの常設の入口にもした
- 更新: [[testing]]、[[mutation-testing-trial-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 17:40] filing-back | #1222 を main に入れ、研究会の要望から出した 4 本の PR が揃った

- rebase 後の CI 全件 pass を確認し、nishio が手元で admin merge（`3649fe41`）。#1205 は検索欄の置き場所が残件で open のまま
- 更新: [[municipal-workshop-issues-triage-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 17:20] filing-back | #1221・#1223・#1224 を main に入れ、利用者定義のラベル（#1225）と会議の分析の線引き（#1226）を Issue にした

- 3 本は nishio が手元で admin merge（`f6df8b53`・`d9920fc6`・`ef8a16c4`）、#1206 が閉じた。#1222 は #1221 と衝突したので rebase し、CI 全件 pass で merge 待ち
- #1226 は既定の案（閲覧画面の改善と入力手順は本体、時系列・横断・評価は本体の外で試作）と期限案 12-08 つき
- 更新: [[municipal-workshop-issues-triage-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 17:20] filing-back | ミューテーションテストで見つけた穴 3 つを塞ぐテストを PR #1220 にした

- 429 の配線・`chat_http_client`・工程をまたぐトークン数の合計を確かめるテスト 4 本（未 merge、本体のコードは変更なし）
- 生き残っていた変異 10 件を手で入れ、すべて新しいテストで落ちることを確認。analysis-core 全体は 876 passed
- 更新: [[mutation-testing-trial-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 16:40] filing-back | analysis-core にミューテーションテストを試し、テストの穴 3 つを見つけた

- mutmut 3.8.1 で 4 モジュール 770 変異、テストが気づいた割合 76%（本体は変更なし、main `600479b7`）
- 穴は部品のつなぎ目: 429 の結果を同時実行数の制御へ渡す配線、`chat_http_client` のフック、工程をまたぐトークン数の合計
- mutmut の既定（fork 方式）では 220 件が誤って timeout になる。forkserver 方式が要る
- 更新: [[mutation-testing-trial-2026-11-24]]、[[meeting-report-draft]]

## [2026-11-24 16:35] filing-back | 自治体の研究会で出た要望 14 件を振り分け、閲覧画面の 4 件を PR #1221〜#1224 にした

- #1203〜#1216 を main と照らし合わせて全件にコメント・ラベル。PR は一括展開・検索で一致した枝を開く・件数の単位・散布図の見方（いずれも未 merge）
- 見つかった穴：新しいデータに調整済みのプロンプトを当てる手段が無い／意見ごとのラベルを利用者が定義できない
- 更新: [[municipal-workshop-issues-triage-2026-11-24]]、[[slack-municipal-workshop-issues-2026-11-18]]、[[meeting-report-draft]]

## [2026-11-24 13:35] filing-back | #1201・#1202 を main に入れ、#471 が閉じた

- どちらも CI 成功・指摘なし。AI からの admin merge は自動モードの安全チェックで止まり、nishio が手元で merge（main `ca485200`・`c56eddcf`）
- #1202 の `Closes #471` で #471 が閉じた。根拠にした検証依頼の #1194・#1195 も、katsushi2441 へのお礼と反映先をコメントして閉じた
- 更新: [[meeting-report-draft]]、[[team-mirai-local-llm-quality-2026-11-10]]、[[domestic-data-residency-options-2026-11-10]]

## [2026-11-20 23:15] filing-back | #1219 を main に入れ、#994 が閉じて 11-02 の棚卸しが全件片付いた

- PR #1219（LLM 直接グルーピングの段も全体の model を使う）を merge（`600479b7`）、#994 も close
- 11-02 の棚卸しで扱いを決めた Issue はこれで全件処理済み。残るのは管理画面での動作確認だけ
- 更新: [[llm-grouping-supervised-classification]]、[[stale-issue-disposition-2026-11-02]]、[[meeting-report-draft]]

## [2026-11-20 19:00] filing-back | 棚卸しの本人判断 3 件を処理し、#994 の確認で見つかった不具合を PR #1219 にした

- #370・#879 を close（経緯は #345、時間の軸の試作と論点は #1214 へ）
- #994 を実際の LLM で最後まで回したら、LLM 直接グルーピングの段だけが `gpt-4o-mini` に固定されていて失敗 → PR #1219（未 merge、merge で #994 も閉じる）。管理画面の同じモードにも効く不具合
- 更新: [[llm-grouping-supervised-classification]]、[[stale-issue-disposition-2026-11-02]]、[[meeting-report-draft]]

## [2026-11-20 18:05] filing-back | #1217・#1218 を main に入れ、#337・#643 が閉じた

- CI 全件成功・CodeRabbit の指摘なし。AI からの admin merge は自動モードの安全チェックで止まり、nishio が手元で merge（main `fca1d407`・`e43911b7`）
- 11-02 棚卸しの assignee 確認分は、本人判断の #370・#879・#994 を除いて片付いた

## [2026-11-20 16:00] filing-back | 11-02 棚卸しの assignee 確認の期限切れ分を既定どおり処理した

- 11-16 までに担当者からの返信はなし。#324・#170 を not planned、#310・#280・#809 を completed で close し、残りの要件をコメントに残した
- #337 は PR #1218（全体図と階層図の色を揃える。階層図は大きさ順に別パレットで塗っていた）、#643 は PR #1217（使われない build-arg を削る）。どちらも未 merge
- 残り：本人判断の #370・#879・#994。更新: [[stale-issue-disposition-2026-11-02]]、[[meeting-report-draft]]

## [2026-11-19 16:30] filing-back | 受けた箇所を引用させてリンクを判定し直し、議論の楽譜に線を重ねて公開した

- 引用の照合で落ちたのは 4 本だけで、線が 1,152→898 本に減ったのは指示と「同じ話題だけ」の受け皿による。無作為 15 本のうち直接受けていると読めたのは約 10 本
- 楽譜に `?links=` を足し、点ごとの線と「時間をおいて受けた発言」の一覧を出した（個人 repo `6da2edc`）
- 更新: [[meeting-transcript-score-prance-2026-11-19]]、[[meeting-report-draft]]

## [2026-11-19 15:30] filing-back | PRANCE の意見 939 件にリンコグラフィーの線を LLM で付けた

- 社内 API の gemma-4-31B で、後の手ごとに 12 候補から受けている手と種類を選ばせた（約 9 分、1,152 本）。半分強は 1 分以内の「話し続け」で、発散は会の冒頭の一般的な主張に偏り、線を引きすぎる
- 次：話者の交代で手を切る、受けている箇所を引用させる、位置の偏りをならす
- 更新: [[meeting-transcript-score-prance-2026-11-19]]

## [2026-11-19 15:10] filing-back | 対立軸ビューの軸ごとの左右の件数を追記

- チームみらいのデータに当てた対立軸ビューの 12 本の軸について、左右の件数・判定不能の件数と、合意できそうな点・対立する点の例を公開 JSON から集計して載せた
- エネルギーと移民は両側があり、家族は反対側が各軸 10 件ほど、皇位継承の「男系 vs 女系」は 97 件中 16 件しか採点されない
- 更新: [[team-mirai-2025-open-dataset]]

## [2026-11-19 14:45] filing-back | 議論の楽譜とリンコグラフィーの対応を書いた

- 「どの発言を受けて次の発言が出たか」は、設計研究のリンコグラフィー（手をつなぎ、発散・収束の重要な手とつながらない手を数える）に近い。nishio の Cosense のまとめを元に対応を整理
- 次：同じまとまりか近い時刻に絞って LLM でリンクを判定し、重要な手が「面白い展開」と合うかを見る
- 更新: [[meeting-transcript-score-prance-2026-11-19]]

## [2026-11-19 14:30] ingest | 議論の楽譜の試作への Slack の反応

- 大木さん：戻ってきた話題が前とどう変わったか、まとまり同士のつながり、面白い展開を AI に挙げさせる入口が見たい。会議では発言の前後関係に意味がある
- nishio：トピックでゆるくまとめ、後の発言が前の発言に賛成・反対・根拠の追加・新しい切り口のどれをしているかを出せると面白い
- 更新: [[slack-municipal-workshop-issues-2026-11-18]]、[[meeting-transcript-score-prance-2026-11-19]] の Open Questions

## [2026-11-19 13:00] filing-back | 議論の楽譜の試作に「実験の記録」を足した

- meeting-transcript-score-prance-2026-11-19 に、実験の区分（exploratory）、非公開の置き場、公開した範囲（public_result.json だけ）、やり直し方を追記
- 社内 API の URL は wiki にも manifest にも残していない

## [2026-11-19 12:30] filing-back | 会議の文字起こしを広聴AI にかけ、「議論の楽譜」を作って公開した

- #1214 を受け、PRANCE 国際シンポジウムの文字起こしを本体の CLI＋gemma-4-31B で分析し、個人 repo で話題の流れの分単位と「議論の楽譜」を公開（`46dcc57`）
- 戻ってきた論点 68・一度だけ出た論点 5。次は話者の区別と会議向けの抽出プロンプト
- 新規: [[meeting-transcript-score-prance-2026-11-19]]

## [2026-11-19 10:30] ingest | Slack 11/8〜11/18：自治体の研究会で出た要望 14 件ほか

- 大木さんが自治体の研究会で会議の録音を広聴AI でその場で分析し、要望を #1203〜#1216 にした。会議の分析をどこまで広聴AI で扱うかは未定
- ほかに散布図の輪郭（凸包）の重なり、UMAP・FAISS の更新、政策案を出す機能の歪みを「あとから確かめられる状態」で防ぐ議論
- 新規: [[slack-municipal-workshop-issues-2026-11-18]]
