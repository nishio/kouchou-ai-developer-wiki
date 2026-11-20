# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

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

## [2026-11-16 15:00] filing-back | 長期戦略の叩き台に 11-16 時点の更新を追記した

- 11-02 以降の動き（#1187 merge、ローカル LLM・Bedrock への需要、検証のお願い Issue への外部の応答）から、2〜3 年後の姿を 5 つと、計画とのずれ 4 つを long-term-strategy-2026-11-02 の Updates に足した
- 提案：v5.0 を書籍と切り離して rc1 を切る、「導入できる」を 6 本目の柱にする、wiki の置き場所を問いとして出す。採否は未定

## [2026-11-15 10:00] filing-back | PR #1202 の CI が通り、merge 判断待ちにした

- #1202（PC の目安と compose.cpu.yaml、Closes #471）は build・CodeQL 成功、未解決の指摘なし。merge すると #471 が閉じるので nishio の判断待ち
- 11-11〜11-14 に merge した PR の後の main の CI（CodeQL・docs deploy・Code Quality）も成功
- 残り：GPU の無い PC で compose.cpu.yaml を重ねた実際の起動の確認（merge 前に検証 Issue にするかも判断待ち）

## [2026-11-15 00:15] filing-back | Bedrock の docs の思考の強さの PR #1201 は CI 通過・レビュー待ち

- PR #1201 の CI（build・CodeQL）と CodeRabbit が通り、指摘はなかった。レビュー承認待ちで、merge は人間の指示待ち
- `domestic-data-residency-options-2026-11-10` の Updates と定例向けの下書きに反映
- 次：merge されたら下書きの #1201 を main 済みにする

## [2026-11-14 14:20] filing-back | #1194・#1195 の検証結果を取り込み、#471 の推奨スペックを PR #1202 にした

- katsushi2441 の検証（4 コア・GPU なし・gemma4:e4b・思考を止める）：100 件約 38 分、400 件約 104 分、メモリ 16GB 以上が目安。止めないと待ち時間切れ
- compose の ollama は NVIDIA GPU を予約するので GPU の無い PC で起動しない → compose.cpu.yaml を足し、README の前提条件を直した
- #1200 は名前の重なりの指摘を直して merge。#1199 に katsushi2441 の貢献を追記

## [2026-11-14 13:40] filing-back | #1193・#1198 の CI とレビューを確認し、merge と行き違いになった #1198 の指摘を #1200 で直した

- #1193・#1198 は CI green のまま 11-11 に merge 済み。#1198 の最後のコミットは CodeRabbit の上限で見られておらず、その前のレビューの diff 外の指摘 2 件（`--n` が 0 以下、同じ件数を 2 回測ると出力名がかぶる）が残っていた → #1200（CI green、未 merge）
- #1193 の解決済みの指摘への返信・resolve と、#1198 への #1200 の案内コメントは、自動モードの安全チェックで止められて未投稿
- 更新: [[team-mirai-local-llm-quality-2026-11-10]]、[[meeting-report-draft]]

## [2026-11-14 13:15] filing-back | チームみらい 2025 データセットの本文入りの版に DOI 10.57967/hf/11618

- nishio が「Generate new DOI」で、2026-11-11 の版 `033d1e7`（PR 本文の抜けを直した版）に DOI を発行。前の 11333（`bca82bd`）・11332（`05e2273`）は古い版を指したまま残る
- 更新: [[team-mirai-2025-open-dataset]]、[[team-mirai-2025-open-dataset-2026-10-30]]

## [2026-11-14 10:30] filing-back | Bedrock の docs の思考の強さの行を直す PR を出した

- nishio の指示で [#1201](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1201) を作成。#1193 の `LOCAL_LLM_REASONING_EFFORT` に合わせ、gpt-oss は `low`・`medium`・`high`（`none` は不可）、Bedrock が受け付けるかは未確認と書いた
- [[domestic-data-residency-options-2026-11-10]] と [[meeting-report-draft]] を更新
- 次：CI と CodeRabbit を見てから merge 判断

## [2026-11-14 10:00] filing-back | 管理画面の API キーと Windows 版の分離を考察ページにした

- admin-api-key-threat-model-2026-11-11 を新規作成。キーを見られるのはログインできる人だけで脅威と呼ぶほどではなく、Windows 版は Web の管理画面とは別の配布物、という 11-11 の結論と根拠をまとめた
- #885 で担当者が 10-22 に出した確認（書き出しを Route Handler で中継するか、ブラウザから直接呼ぶか）が返答待ちと分かった。この整理からは中継する案が導ける。返答は nishio の確認待ち

## [2026-11-14 10:00] filing-back | Bedrock 対応のその後を確認した

- 大木さんが 11-10 に「事業者の方の環境で、LocalLLM に Bedrock を入れるやり方で動いているようです」と Slack で報告（伝聞、モデル・接続先・構造化出力の詳細なし）。#1169・#1170・#1190 は動きなし
- #1193 で `LOCAL_LLM_REASONING_EFFORT` が入り、Bedrock の docs の「思考の強さを指定する手段はない」が古くなった。[[domestic-data-residency-options-2026-11-10]] の Updates に記録
- 次：docs の該当行の修正、事業者の構成の詳細を #1169 に書いてもらえるか
