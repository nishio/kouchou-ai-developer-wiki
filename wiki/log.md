# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-11-14 13:40] filing-back | #1193・#1198 の CI とレビューを確認し、merge と行き違いになった #1198 の指摘を #1200 で直した

- #1193・#1198 は CI green のまま 11-11 に merge 済み。#1198 の最後のコミットは CodeRabbit の上限で見られておらず、その前のレビューの diff 外の指摘 2 件（`--n` が 0 以下、同じ件数を 2 回測ると出力名がかぶる）が残っていた → #1200（CI green、未 merge）
- #1193 の解決済みの指摘への返信・resolve と、#1198 への #1200 の案内コメントは、自動モードの安全チェックで止められて未投稿
- 更新: [[team-mirai-local-llm-quality-2026-11-10]]、[[meeting-report-draft]]

## [2026-11-14 13:15] filing-back | チームみらい 2025 データセットの本文入りの版に DOI 10.57967/hf/11618

- nishio が「Generate new DOI」で、2026-11-11 の版 `033d1e7`（PR 本文の抜けを直した版）に DOI を発行。前の 11333（`bca82bd`）・11332（`05e2273`）は古い版を指したまま残る
- 更新: [[team-mirai-2025-open-dataset]]、[[team-mirai-2025-open-dataset-2026-10-30]]

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

## [2026-11-07 20:30] filing-back | ページをまたいだ食い違いの監査（Codex gpt-6.1-sol、閉じる 145・現状更新 65・継続 764・人の判断待ち 10、本物 11・古い方が残っている 6・判定できない 3）

- grasp-nishio のセッションから、Codex にページ間の矛盾（数値・日付・決定・名前・状態）を探させ一次ソースでどちらが現状かを確かめさせ、別の Codex セッションが全件を敵対的に検証した。報告は raw/consistency-audit-2026-11-07.md・raw/consistency-verify-2026-11-07.md

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

## [2026-11-07 17:30] filing-back | Open Questions 984 項目の現状突合（Codex gpt-6.1-sol、閉じる 142・現状更新 68・継続 764・人の判断待ち 10）

- grasp-nishio のセッションから、Codex に `## Open Questions` の各項目を一次ソース（本 wiki の git blame・Updates、kouchou-ai upstream/main 085366779、slack-logs、dd2030-website、local-llm-experiments、grasp-nishio の LOG）で突合させ、根拠のある項目だけを閉じる／現状更新した（132 ページ）
- 閉じた 145 件は Claude の検証エージェント 2 本が commit・path:line・コード行を全件確認し、引用の捏造は 0。3 件（OQ-0254 複数選択のユースケース、OQ-0750 粗い帯の後続 slice、OQ-0846 config 欠損の混入経路）は二択の片方が実装で消えただけなので現状更新に戻し、2 件（OQ-0081 先行 commit の書き方、OQ-0115 「CLI コマンド」の強さ）は Updates に訂正を添えた。Codex が約 50 字で切っていた旧項目 99 件は原文に戻した。空になった Open Questions 節は外した
- 報告は raw/open-questions-triage-2026-11-07.md（gitignored）

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
