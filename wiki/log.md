# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

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

## [2026-11-11 21:00] filing-back | open PR 7 本を main に入れた（#1162・#1174・#1176・#1177・#1192・#1193・#1198）

- nishio の指示で admin squash merge。#1193 を #1198 より先に。#1192 は #1193 と README が衝突したので、既定モデルの変更を反映して解消してから
- merge 後に別セッションが作った #1200 は対象外として残した

## [2026-11-11 15:40] filing-back | v5.0 の「これまでの貢献者」一覧を作る Issue #1199 を M5 に起票し、M5 の期限を 12-31 に変えた

- コード以外（デザイン、実験フィードバック、事例共有、Issue での報告）も貢献として載せる（nishio）。GitHub の外での貢献は本人の同意を取ってから載せる
- 置き場所・範囲・表記は定例の議題候補に。M5 の期限は 07-01 のまま過ぎていた

## [2026-11-11 15:20] filing-back | open PR 7 本の未解決レビュー指摘を直し、全件 CI green にした（merge は未実施）

- #1174 可視化カタログの各項目に要る入力、#1176 OpenRouter のモデル ID、#1198 効かない reasoning effort で止める、#1162 ホイールガードの重なりをポインタ透過に
- 7 本とも CI green。AI からの admin merge は権限で止まったので、merge は nishio 待ち（#1193 を #1198 より先に）

## [2026-11-11 14:40] filing-back | PR #1198・#1193 の CI 失敗を直した

- #1198: docs に複製する README を docs.yml の監視パスに足し忘れていた。#1193: 新しい env 変数を setup スクリプトが書かず env 検査で落ちていた（任意キーに追加）
- 両方 CI green。残るのは merge 判断

## [2026-11-11 14:00] filing-back | 関連研究ページを「本体未収録の周辺の研究・実験」として紹介し直した（PR #1174）

- nishio の方針で「成熟していない」という呼び方をやめ、本体外の試みを奨励する形にした。本体を変えずに public_result.json や CLI 出力で試すことを歓迎する節と、nishio の可視化カタログのエントリを追加
- #1158 の main 入りを反映し、main を merge して nav の衝突を解消。PR の題と本文も更新。Issue #1173 への追記コメントは未実施

## [2026-11-11 13:30] filing-back | #1197 の前提を見直し、議論をコメントに残した

- 1 つのコードベースで両方を満たそうとしない（nishio）。キーを見られるのは管理画面にログインできる人だけで、できることも増えないので脅威と呼ぶほどではない。Windows 版は Web の管理画面とは別の配布物として考える
- #1197 を閉じるか、#547 をどう扱うか、#885 への伝え方は未実施（定例の議題候補を更新）

## [2026-11-11 13:10] filing-back | チームみらいの品質調査から本体と #471 へ還流した分をまとめた

- [[team-mirai-local-llm-quality-2026-11-10]] に「本体と #471 への還流」の節を足した。測った条件は思考を止めた gemma-4（31B は配信側で思考しない設定）、#471 へのコメント、PR #1192・#1193・#1198、Issue #1194〜#1196
- #471 は推奨スペックの文書（#1195 の結果待ち）が残るので、まだ close できない

## [2026-11-11 13:00] filing-back | 管理画面の API キーの方針の衝突を Issue #1197 にした

- #547（キーをサーバー側に隠す）と #885（Node をなくしてブラウザから FastAPI を直接呼ぶ）が逆向きなので、A／B／C 案のメリットとデメリットを 1 本の Issue にまとめた。#547 は 11-08 に担当が外れた
- 定例の議題候補に追加（meeting-report-draft）。決めたいのは、リモート運用をどこまで支えるか

## [2026-11-11 12:50] filing-back | 測定スクリプトの PR #1198 と、NPU を切り出した Issue #1196

- `experiments/local_llm_bench/`：本物のローカル LLM で CLI を最後まで走らせ、PC の情報・段ごとの時間・メモリの最大値を CSV に取る。ARM 8 コアで gemma-4-E4B 20 件が 4.9 分・2.0GB
- 走らせて、CLI（workflow 経由）の段ごとの時間が `0.0` 固定で記録される不具合を見つけ、同じ PR で直した
- #1196 は NPU（Intel・AMD・Apple・Copilot+ PC）を #471 から切り出したもの。#1195 に #1198 の使い方を追記した

## [2026-11-11 12:27] filing-back | 個人 repo の README から wiki へのリンク 3 か所が 404 だったのを、公開先の nishio.github.io に直した

- `digitaldemocracy2030.github.io/kouchou-ai-developer-wiki/` を指していた。この wiki は org に移していないので、住所は `nishio.github.io/kouchou-ai-developer-wiki/`。個人 repo の commit `6fdee4c` で直し、3 つのリンク先が開くことを確かめた
- 外からこの wiki にリンクするときの住所を [[wiki-pages-publishing-stack]] に足した。本体の main にはこの wiki へのリンクがなく、PR [#1174](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1174) のカタログへのリンクは正しい住所
- [[team-mirai-2025-open-dataset]] の「個人 repo のカタログ」に記録

## [2026-11-11 12:10] filing-back | 他の環境での確認を Issue #1194・#1195 にした

- 手元で確かめられない確認は「検証のお願い」Issue に切り出す方針にした（nishio）。#1194 は Ollama で gemma4:e4b と思考を止める設定が動くか（#1193）、#1195 は x86・GPU なしの PC でレポート全体の時間とメモリ（#471）
- #471 は close できない。残りは全体の所要時間（#1195）、測定スクリプトを本体に入れること、推奨スペックの文書、NPU を範囲外にする判断

## [2026-11-11 11:40] filing-back | #471 に品質の結果をコメントし、Ollama の既定モデルと思考の止め方を直す PR #1193 を出した

- #471 にチームみらいでの測定結果をコメントした（ドキュメントの PR #1192 へのリンク付き）
- PR #1193: `--profile ollama` の既定を ELYZA-JP-8B から gemma4:e4b に、`LOCAL_LLM_REASONING_EFFORT` を設定したときだけ `reasoning_effort` を送る。llama.cpp で 322→57 トークン・17.2→4.1 秒を実測。Ollama での確認は残る（この環境に Ollama を入れられなかった）
- 詳細は [[team-mirai-local-llm-quality-2026-11-10]]

## [2026-11-11 10:40] filing-back | ローカル LLM のモデル選びのページを本体 docs に足す PR #1192 を出した

- チームみらいでの品質の測定結果を、モデルを選ぶ人向けに `docs/self-hosting/local-llm-models.md` にまとめた（gemma-4-E4B が第一候補、ELYZA-JP-8B は入出力例の写しで非推奨）。#471 を nishio に assign
- 残り: `--profile ollama` の既定モデル（ELYZA）を変えるか、LocalLLM から思考を止める指定を送れるようにするか
- 詳細は [[team-mirai-local-llm-quality-2026-11-10]]

## [2026-11-11 07:45] filing-back | チームみらいの比較に使った gemma-4-31B の重みを記録した

- 社内 API の gemma-4-31B は `Intel/gemma-4-31B-it-int4-AutoRound`（int4）だった（nishio）。小さいモデルの測定は、31B も含めて 4 ビット前後どうしの比較になる
- [[team-mirai-local-llm-quality-2026-11-10]] と Hugging Face の README を直した

## [2026-11-11 07:30] filing-back | チームみらいの比較実験を追試できる形で Hugging Face に載せた

- nishio の「追試可能なレベルで報告されてる？」を受けて点検した。結果 5 の 12 組が、温度 0 で送り直す前の 31B の出力で判定されていて、公開データと合っていなかった。判定し直して 141 勝 19 敗を 143 勝 18 敗（勝ち点 0.81 のまま）に訂正
- 判定材料・対応表・判定・判定役への指示の全文・スクリプトを Hugging Face の `experiments/step1-local-llm-2026-11/` に載せ、取り直したものから組と勝ち点が再現できることを確かめた
- 詳細は [[team-mirai-local-llm-quality-2026-11-10]] の「追試に使える材料」、[[team-mirai-2025-open-dataset]]

## [2026-11-11 06:45] filing-back | 小さいモデルの測定に gemma-4-12B を足した

- 同じ入力の 60 件で gemma-4-12B は gpt-4o に 34 勝 8 敗、勝ち点 0.72（95% 区間 0.62〜0.81）。31B 0.76 と E4B 0.68 の間で、入出力例の写しは 0
- 26B-A4B はマシンのメモリ不足で生成が止まり、未計測のまま
- 詳細は [[team-mirai-local-llm-quality-2026-11-10]] の結果 6

## [2026-11-11 06:30] filing-back | チームみらいデータの Hugging Face を本文入りに更新した

- nishio「公開して」を受け、nishiohirokazu/team-mirai-2025-embeddings に 1 コミットで上げた。PR の本文とタイトル、古い行の本文入りの印、1 段目の入力（当時と本文入り）、gemma-4-31B による本文入りの抽出し直し（35,393 件、温度 0）、README の Known issue（89% で本文が抜けていた）
- [[team-mirai-2025-open-dataset]] を更新。2 段目以降（意見・クラスタ・埋め込み）は本文入りの課題ではまだやり直していない

## [2026-11-11 05:30] filing-back | 小さいモデルの測定の途中経過と、温度 0 での繰り返しのループ

- 同じ入力の 60 件で gpt-4o と比べた勝ち点は、31B 0.76、E4B 0.68（下限 0.57）、E2B 0.54、ELYZA 0.26（入出力例の写し 5 件）。gpt-4o 並み以上と言えるのは E4B まで。12B・26B-A4B は実行中。CPU のモデルは 4 ビット前後、31B の量子化は記録なし
- 31B の全件抽出の 5% は、説明欄のループで JSON が閉じなかった。温度を上げるやり直しをやめ、温度 0 のまま切れた出力から課題を取り出す形に直している（nishio「それで直して」）。結果は [[team-mirai-local-llm-quality-2026-11-10]] の結果 6、データ側は [[team-mirai-2025-open-dataset]]
- Hugging Face の更新は、nishio の差分確認とログイン待ち

## [2026-11-11 04:35] filing-back | 散布図が描いていない軸の可視化のうち 4 つを公開し、試作のために本体の契約は変えない方針を A13 に

- 「判断に必要な情報がない」を受けて材料を付け直した 4 項目への nishio の答え：merge された提案を除く 4 つを公開（個人 repo の commit `85d79c4`）、一緒に言われた話題の偶然の見込みは層別のまま、PR の state は入れない。merge された提案は既定の表示が読み違えを招くので見送った
- 本体の公開契約に足す提案（`attribute_meta`、公開設定の許可リストを直す小さな PR）には、nishio「色々実験するたびに本体に色々修正しないといけないのでは切り分けた意味がないのでは？」。試作は今の契約の中で描き、足りない項目は本体に入れると決めたときの材料にする方針として [[open-decisions]] の A13 に書いた。個人 repo の CLAUDE.md も同じく直した（`b1ffc3a`）
- 話題の流れのカタログのリンクは、期間を選ばずに開くようにした。7/3〜19 を選んだ状態では「それ以外」に 5 月が入り、6 月とだけ比べると医療制度の +3.0 ポイントは +1.1 に縮む
- [[new-visualization-axes-2026-11-11]]・[[team-mirai-2025-open-dataset]]・[[meeting-report-draft]] を更新

## [2026-11-11 02:10] filing-back | チームみらいデータの本文を戻す作業と、小さいモデルの測定の途中経過

- nishio「まず正しく本文が入っているデータを作ろう」を受け、全 9,688 件の PR 本文を GitHub から取り直した。当時の収集後に編集されたものは 0 件で、今の本文が当時の本文そのもの。本文入りの入力を作り、gemma-4-31B で課題を抽出し直している（実行中）。Hugging Face の更新案（本文はそのまま載せる、古い行に本文入りの印）は未公開。[[team-mirai-2025-open-dataset]] に
- 小さいモデル（E4B・E2B・ELYZA・12B・26B-A4B）を、gpt-4o と同じ入力の 60 件で測っている。基準の 31B は同じ 60 件で勝ち点 0.76。[[team-mirai-local-llm-quality-2026-11-10]] の「次に見ること」に

## [2026-11-11 01:45] filing-back | 散布図が描いていない軸から、可視化 5 つを個人 repo で作った

- nishio「新しい可視化の方法を考えて」に、AI がチームみらいのデータの集計で下見して 5 案を出し、「all go」で 5 つとも workflow で作って確かめた（話題の流れ・要約から落ちた声・一緒に言われた話題・自分の声を探す・merge された提案）。個人 repo の作業ツリーにあり未 commit・未公開。[[new-visualization-axes-2026-11-11]]
- 話題の流れの 5 月と 6 月以降の比べには、1 段目の抽出で本文が入っていたかの違いが混ざる（PR 1 本あたりの意見 4.17 → 2.30 → 2.01 件）。本文なし同士の 6 月 → 7/1〜19 でも、家族 1.4% → 4.3% などは残る
- どれも `public_result.json` だけで描け、足りないのは属性の型と役割を宣言する場所（`attribute_meta` の案）。次：公開するか、この案を公開契約の提案にするか

## [2026-11-11 00:58] filing-back | Bedrock の構成例の docs（#1191）を main に入れた

- CodeRabbit の指摘で、API キーのリージョン（期限の短いキーは作ったリージョン限定）と、API キー利用・モデル一覧に要る権限を足してから、nishio の指示で admin merge（`67bc798d`）
- 「期限の長いキーもリージョン限定」は根拠がなく反映せず、PR に理由を返した。[[domestic-data-residency-options-2026-11-10]] と [[meeting-report-draft]] を更新
- 次：AWS の実機での確認（構造化出力、`seed` など）を事業者側の参加者に頼めるか

## [2026-11-11 00:40] filing-back | 本文が同じ入力で gemma-4-31B と当時の gpt-4o の課題抽出を比べた

- nishio「精度比較実験に関しては本文のある4oでのデータとの比較で」「急いで」を受け、当時の入力に本文が入っていた 1,105 件から 200 件を選び、同じ入力で比べた（判定役は Claude）
- 31B の 141 勝 19 敗、勝ち点 0.81（0.76〜0.85）。取り出す数はほぼ同じで、gpt-4o の方が多い 43 件でも 31 勝 2 敗。長い文への好みと人の判定は未確認。[[team-mirai-local-llm-quality-2026-11-10]] の結果 5 に
- 並行して、本文を戻した全 9,688 件の抽出し直しと Hugging Face の更新を準備中

## [2026-11-10 23:45] filing-back | チームみらいデータの課題の 79% は PR 本文を見ずに抽出されていた

- nishio「本文を読んでない抽出はどれくらいの割合？」を受け、pr-data の snapshot 全 9,688 件を調べた。PR の 89%、課題の 79%、意見の 76% が本文なしの記録から作られていた（2025-06・07 作成の PR は全件本文なし）
- [[team-mirai-2025-open-dataset]] に節を追加。README の説明と食い違う。README を直すかは未定

## [2026-11-10 23:40] filing-back | #471 元の PR からの抽出の勝敗を撤回した（入力の食い違い）

- nishio「4Bでgpt-4oに勝つの本当ですか？実験手法が間違ってない？」を受けて調べ直した。gpt-4o が見た当時の PR データ（2025-07-27 の snapshot）では 198 件中 153 件の本文が空で、ローカル側だけに今の本文入りの入力（中央値 8 倍の長さ）を渡していた
- 31B 171 勝 4 敗・E4B 166 勝 16 敗などの勝敗を [[team-mirai-local-llm-quality-2026-11-10]] で撤回し、[[meeting-report-draft]] も直した。ELYZA の入出力例の写し、12B の繰り返しは基準に依らない観察として残す
- 根拠：153 件は pr-data の JSON に `body` の項目自体が無く、収集時刻が当時の抽出時刻と一致する。gpt-4o の問題文で本文にだけある言い回しを含むのは、本文ありの PR で 90%、本文なしの PR で 26%
- 本文が抜けた入力でのやり直しはしない（nishio「データがおかしいわけなので」）

## [2026-11-10 22:25] filing-back | #471 元の PR からの抽出を小さいモデルでも測った（E4B・ELYZA・12B）

- nishio「1 go」を受け、結果 4 と同じ条件で gemma-4-E4B（198 件）、ELYZA-JP-8B・gemma-4-12B（66 件）を CPU で回し、当時の gpt-4o と出どころを伏せて比べた
- E4B は 166 勝 16 敗・出力の壊れ 0 で 31B に近い。ELYZA は 32 勝 26 敗で、9 件でプロンプトの入出力例（「高齢者の孤立」）を写した。12B は 9 件で説明欄の繰り返しが止まらず出力が返らなかった（除けば 47 勝 3 敗）。結果は [[team-mirai-local-llm-quality-2026-11-10]] の結果 4 に
- 次：入出力例の写しと繰り返しを防ぐ手当てを本体に入れるか、人の A/B 判定での較正

## [2026-11-10 14:30] filing-back | #471 元の PR からの抽出を gemma-4-31B で測った

- nishio「抽出したデータからさらに抽出してるのでは？元Issueからのextractionで計測した？」を受け、198 の PR 本文を GitHub から取り直し、当時の課題抽出のプロンプトそのままで gemma-4-31B に抽出させ、公開データの gpt-4o の出力と出どころを伏せて比べた
- 31B の 171 勝 4 敗。gpt-4o は具体的な問題を落として抽象的な 1〜3 件に縮める負け方。件数が同じ組でも 28 勝 0 敗だが、判定役が長く具体的な文を好む偏りは人の判定で確かめる。31B は 1 件で説明欄が繰り返しループに入り出力が終わらなかった。結果は [[team-mirai-local-llm-quality-2026-11-10]] の結果 4 に
- 次：同じ条件で E4B・ELYZA・12B を回す、20〜30 組を人が判定する

## [2026-11-10 14:20] filing-back | Bedrock の構成例の docs を本体に書いた

- nishio「Bedrockのドキュメントを作って」を受け、kouchou-ai の branch `docs/amazon-bedrock-setup` に `docs/self-hosting/amazon-bedrock.md` を追加（LocalLLM に Bedrock 東京の OpenAI 互換の接続先を入れる構成、コード変更なし、`mkdocs build --strict` 通過）。PR は未作成
- AWS 公式ドキュメントで確かめたこと（管理画面には `bedrock-mantle` が要る、構造化出力のスキーマの制約に広聴AIのスキーマが収まる）を [[domestic-data-residency-options-2026-11-10]] に、進行中の項目を [[meeting-report-draft]] に追記
- 次：PR を出す、AWS の実機確認を事業者側の参加者に頼めるか

## [2026-11-10 13:50] filing-back | Bedrock 対応への大木さんの返信を読んだ

- 背景は SIer 2 社が真っ先に Bedrock を挙げたこと。自治体向けの提案では AWS のほうが通しやすい。DD2030 の優先度は上げなくてよく、シグナルの共有という位置づけ。nishio は「動作確認なしのプロトタイプとドキュメント」→「気にせずコードを入れればいい」と寄った
- provider `local` ＋サーバー内蔵の埋め込みで、コードを変えずに構成できる見込みと、品質評価は既存の仕組みで AWS なしに測れることを [[domestic-data-residency-options-2026-11-10]] の Updates に追記
- 次：Bedrock の構成を書いた docs、gpt-oss の構造化出力の実機確認（事業者側の参加者に頼めるか）

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
