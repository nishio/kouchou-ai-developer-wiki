---
title: "2026-10 の経緯の整理：大規模レビュー・鍵漏洩の修正・宙に浮いた可視化 2 つ・ところてんの分析手法 2 つ（2026-10-28）"
type: analysis
summary: "2026-10-16〜10-26 の大規模コードレビュー（4 段、修正 PR 100 本超）から、ユーザー API キー漏洩の発見・猶予・公開・v4.2.0 までの経緯を 1 本の流れとして整理し、残った 2 つの論点（ドリルダウンのツリー表示と ズームできる付箋表示の置き場、tokoroten の賛否分離 2 手法＝センチメント次元の付与と DivCon の取り込み方）を次の判断材料として並べた 2026-10-28 時点の振り返り"
sources:
  - source-code.md
  - source-review-findings-2026-10-16.md
  - code-health-review-2026-10-18.md
  - deep-code-review-2026-10-19.md
  - code-review-r3-continuation-2026-10-23.md
  - user-api-key-leak-2026-10.md
  - claude-provider-experiment-output-2026-10-17.md
  - broad-listening-book-extractions.md
  - meeting-minutes.md
---

## 位置づけ

nishio「今回の経緯について LLM Wiki にまとめる」を受けた振り返り。対象は 2026-10-16 から 10-28 までの 2 週間で、(1) 大規模コードレビューと、そこで見つかった脆弱性の修正・公開、(2) レビューの過程で「やりたいが本流に入れていない」まま残った可視化 2 つ、(3) [[tokoroten]] が書籍・定例で示した賛否分離の 2 手法をどう取り込むか、の 3 つを扱う。

各段の指摘一覧や PR ごとの内容は、それぞれの analysis ページに既にある。このページは **流れと判断** だけを書き、詳細はリンク先に送る。観測時点は kouchou-ai main `1028da9c`（2026-10-27、[#1152](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1152) merge 後）。

## 1. 大規模レビューから v4.2.0 まで

### 経緯

| 日付 | 出来事 | 詳細 |
|---|---|---|
| 10-16 | ソースコードレビュー棚卸し（main `eb38328d`）。多エージェントで洗い出し、1 件ずつ反証して確定 10 件。[#1015](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1015)〜[#1022](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1022) を PR 化。散布図ラベルの薄表示だけは設計判断が要るので [#1023](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1023) で a/b を質問 | [[source-review-findings-2026-10-16]] |
| 10-17 | 独立した 8 PR を nishio の明示指示で admin merge。同日、Claude 接続の 2 形式を実験（後述のドリルダウンはここで生まれた） | [[claude-provider-experiment-output-2026-10-17]] |
| 10-18 | 健全性レビュー（main `083593ba`）。改善 5 件を [#1027](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1027)〜[#1031](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1031) に。**この調査でユーザー API キーの漏洩を発見**し、再現・修正を作った上で関係者に先行連絡。約 1 週間の猶予期間に入る | [[code-health-review-2026-10-18]] / [[user-api-key-leak-2026-10]] |
| 10-19 | 本格レビュー。8 領域＋横断フロー追跡で 36 件を確定し、10 グループに分けて [#1032](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1032)〜[#1041](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1041)。CI 通過後に 15 本を admin merge | [[deep-code-review-2026-10-19]] |
| 10-19〜21 | 第 3 弾（main `fca42699`）。merge 後の回帰 6 件を [#1043](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1043)〜[#1047](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1047)、途中終了した調査の候補 11 件を [#1048](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1048)〜[#1058](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1058) で修正して merge。Wiki の古い記述約 70 件を訂正、Issue 16 件を現状追記、[#211](https://github.com/digitaldemocracy2030/kouchou-ai/issues/211)・[#295](https://github.com/digitaldemocracy2030/kouchou-ai/issues/295) を close。利用上限に何度も当たり、洗い出し 5 観点と未検証 43 件が残った | [[code-review-r3-continuation-2026-10-23]] |
| 10-23 | 残りを仕上げ（main `b675e032`）。4 観点の洗い出しと未検証 43 件の検証（確定 39・反証 4）、批評ラウンド 2 回、PR の独立レビュー、LLM プロバイダの組み合わせ、分析結果の不変条件、旧バージョンのレポート互換、管理画面の本番ビルドの実ブラウザ検査。修正 PR は [#1062](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1062)〜[#1126](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1126) の 65 本 | 同上 |
| 10-24 | 65 本を 3 陣に分け、CodeRabbit の指摘を直しながら 1 本ずつ admin merge（main `bdc3e469`）。Next.js の勧告対応 [#1127](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1127) も merge | [[meeting-report-draft]] |
| 10-26 | 猶予期間が明け、修正 [#1136](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1136) を merge。同じ期間に非公開で保留していた修正（[#1132](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1132)〜[#1146](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1146)、表示言語切替の載せ替え [#1144](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1144) を含む）と依存の更新 [#1137](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1137) を merge し、**v4.2.0** と PyPI の analysis-core **0.2.0** をリリース。Security Advisory（GHSA-xr6j-6w48-xh62、Moderate、CVE なし）を nishio が公開 | [[user-api-key-leak-2026-10]] |
| 10-26〜28 | v4.2.0 の Docker イメージで YouTube 取り込みが動かない件を [#1149](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1149) で修正（v4.2.1 は出さず次のリリースに含める、nishio 10-28）。429 を受けた側で送信を調整する [#1152](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1152) も main に入った | [[meeting-report-draft]] |

レビュー由来の修正 PR は、4 段を合計すると 100 本を超える（8 + 5 + 10 + 5 + 11 + 65 に、猶予期間中に保留した約 15 本が加わる）。全件が merge 済みで、2026-10-28 時点で open PR は 0 本になった。

### 「大規模スキャン」の進め方

4 段で共通した手順は次のとおり。[[deep-code-review-2026-10-19]]より [[code-review-r3-continuation-2026-10-23]]より

1. **洗い出し**：領域ごとの担当（API、analysis-core の orchestration と各ステップ、LLM プロバイダ、公開ビューア、管理画面、インフラ・CI、テストの質、ドキュメント、設定、規模）に加えて、「入力や設定値がファイルをまたいでどの出口に届くか」を追う横断フロー追跡の担当を置く。離れた場所の古い処理とつながって起きる不具合は、領域担当では見つからない
2. **検証**：指摘を 1 件ずつ、別の担当が反証・再現する。43 件のうち 4 件が反証され、うち 2 件は既に別の PR で直っていた。洗い出しから時間が経った指摘は、検証の前に「main で直っていないか」を見る
3. **修正**：確定した指摘だけを、指摘ごとに main から別ブランチで直す。先に「修正前のコードで落ちるテスト」を書く。修正担当は指摘側の誤りも直す（Plotly のズームの理解違い、既定引数の評価タイミングで効かない案など）
4. **独立レビューと批評ラウンド**：merge 前に PR を別の目で読み、取りこぼし（番号の境目で抜けた PR、旧バージョンとの互換性など）を批評ラウンドで拾う
5. **merge は人間の判断**：admin merge は nishio の明示指示があるときだけ。CodeRabbit の指摘は実際に確かめてから commit を足す（無料枠は約 30 分に 2 回なので順番待ちになる）

コストの実測は次のとおり。洗い出し 1 担当は 12 分〜1 時間半、未検証 14〜15 件の検証は約 7 分。3 担当を並行させると 5 時間枠の利用上限に当たり、中断した担当の消費は丸ごと無駄になる（途中で結果を返さなかった担当が subagent 全体の約 4 割を占めた回があった）。1 本あたり 2 担当にすると上限に当たらずに回せた。[[code-review-r3-continuation-2026-10-23]]より

### 見つかった脆弱性と修正

管理画面で入力した「ユーザー API キー」が、結果ファイル `hierarchical_result.json` の `config.user_api_key` と状態ファイルに平文で書かれ、公開ビューアがレポート全体を client component に渡すため公開ページの HTML にも埋め込まれていた。2026-05-29 の [#868](https://github.com/digitaldemocracy2030/kouchou-ai/pull/868) で混入し、v4.1.0 に含まれていた。サーバーの環境変数のキーは対象外。[[user-api-key-leak-2026-10]]より

気づきにくかったのは、[#868](https://github.com/digitaldemocracy2030/kouchou-ai/pull/868) 自身は「キーを保存しない」ことをテストで確認していたのに、漏れた経路がその外側の 3 段（ステップ共通の補助関数が一時設定にキーを入れる → 集計ステップが設定を丸ごと結果に書き出す → 公開ビューアが結果を丸ごと埋め込む）にあったから。元の [#660](https://github.com/digitaldemocracy2030/kouchou-ai/pull/660) が「キーを設定に入れない」形にしていた理由はコードにもテストにも残っていなかった。

対応は、出口（結果・状態ファイルの書き出し直前）で秘密を再帰的に落とす形に統一し、既存レポートの確認・修正スクリプトを同梱した（[#1136](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1136)）。公開の順序は「関係者に先行連絡 → 約 1 週間の猶予 → 修正 merge・docs・wiki・Advisory を同日に公開」とし、猶予中は公開 wiki・Issue・PR・commit メッセージに詳細を書かなかった。影響範囲の説明は、調査時のメモ（作成・複製・編集）を修正の段階で今のコードと照合して絞った（編集と再利用ページからの複製は対象外）。告知文は「どの画面のどの欄か」を冒頭で特定し、当てはまらない人には影響なしと先に書いた。

### この 2 週間で分かったこと

- **公開物に設定を丸ごと書く処理は、設定の中身が変わると漏洩点になる**。秘密が設定に入りうるかを追いかけるより、出口で落とす方が壊れにくい。[[gotchas]] にも記録した
- **「なぜこうしてあるか」はコードかテストに残す**。残っていないと、後の正しい修正が前提を崩す
- **横断フロー追跡は、領域別レビューの補完として効く**。今回の脆弱性も、再実行判定や再利用の不具合の多くも、ファイルをまたいだつながりで起きていた
- **レビューの規模は利用上限で決まる**。洗い出しは高く検証は安い。並行数を抑え、中断で捨てる分を減らす方が総量が増える
- **merge と告知は人間の判断に残す**。AI は PR 作成・検証・CodeRabbit 対応までを担い、admin merge・Advisory 公開・関係者連絡は nishio が行った

## 2. 宙に浮いている可視化 2 つ

どちらも「作りたい」「試作はある」が、本流（公開ビューア / CLI の既定出力）に入っていない。レビューで公開ビューアの性能を直した（[#1069](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1069)〜[#1071](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1071)、[#1102](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1102)）ことで、大規模レポートの表示そのものは軽くなったが、「読む体験」の設計は手つかずのまま残っている。

### 2-a. ドリルダウンのツリー表示

**何をしたいか**：俯瞰 → ゾーンを選ぶ → 掘り下げる、という読み方（[[nishio-amusement-park-map-metaphor-2026-06-03]]）を、固定した階層ではなく、読者が選んだクラスタをその場で細分化する形で支えたい。

**今あるもの**

- 公開ビューアの階層リストとツリーマップ。深さは `cluster_nums` で作成時に固定され、最下層まで行っても原文に辿れない（[#250](https://github.com/digitaldemocracy2030/kouchou-ai/issues/250)）。最下層を濃いクラスタだけに絞る案（[#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60)）も未着手
- 2026-10-17 の Claude 接続実験で、ローカル埋め込み＋クラスタリングの上で **最大クラスタをその場で再クラスタリングする** ドリルダウンを最小実装した。997 件の最大クラスタ（245 件）が 4 つに割れた。固定パイプラインでは出せない「結果を見て絞り込んで再分析」の実演で、コードは branch `claude-provider-experiment`（未 push）、成果物は `raw/experiments/claude-local-embed-opus-2026-10-17/`。[[claude-provider-experiment-output-2026-10-17]]より
- [8, 64] の分析をマンダラート（中心 → 8 観点 → 64 詳細）で見せる案（[#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880)）。モック未作成

**未決の点**

- ドリルダウンを **分析側**（再クラスタリングして新しい階層を作る）に置くか、**表示側**（既にある階層を折りたたんで見せる）に置くか。前者は結果 JSON の構造を変え、後者は [#250](https://github.com/digitaldemocracy2030/kouchou-ai/issues/250) の延長で済む
- 再クラスタリングした結果をレポートに保存するか、一時的な探索に留めるか。保存するなら、公開ビューアが結果 JSON 全体を HTML に埋め込む現構造（3 万件で SSR 約 1GB。[[code-review-r3-continuation-2026-10-23]] の未修正指摘）が先に効く
- CLI の standalone HTML として出すのか、Web UI に入れるのか。これまでの方針は「CLI で比較可能な artifact を貯めてから昇格判断」（[[cli-pipeline-experiment-roadmap-2026-06-02]]）

### 2-b. ズームできる付箋表示

**何をしたいか**：散布図の点を付箋（意見の本文が読めるカード）に置き換え、引いた状態ではクラスタの表札、寄った状態では個別の意見が読める semantic zoom にする。「リーフノードを単なる点ではなく付箋にする」という nishio の 2025-08 の着想が出発点。

**今あるもの**

- nishio の別 repo `canvas_kozaneba_prototype`（2025-08-26〜29）。広聴AI の embedding＋UMAP の結果を 1 万件の付箋として Canvas に描き、LOD でズームする。実験サブルートには、密度でクラスタを切って大きな付箋にまとめる semantic zoom と、AI による表札の自動付与まである。既定の画面には統合されておらず、最終 commit 日に「クラスタ抽出の方針」「併合の閾値」「1 万件以上を扱う路線と、1,000 件未満を手で構造化する Kozaneba を同一視してよいか」が未解決のまま止まっている。2026-06 に「Google Maps のタイル方式で割り切る」案が出て、前 2 つは解消方向、後 1 つは未決（Kozaneba 側の wiki の記録）
- このレポート wiki では「マンダラート・付箋ビュー」を、ラベル品質の改善ループに接続する view prototype として、Web の既定にせず CLI の standalone HTML / JSON として読みやすさを確認する順序に置いている。[[cli-pipeline-experiment-roadmap-2026-06-02]]より [[meeting-report-2026-10-10]]より

**未決の点**

- 付箋表示を広聴AI 側に持つか、Kozaneba 側に広聴AI の出力を読み込ませるか。前者は公開ビューアの可視化 plugin の話、後者はデータ書き出し（意見・座標・クラスタ・表札）の契約の話になる（[[plugin-system]]）
- 1 万件規模の表示性能。公開ビューアは Plotly の散布図と React の DOM を前提にしており、Canvas 描画の導入は別の技術判断になる
- スマホでの読み方。散布図はスマホでは別ビューにする方針（[[open-decisions]] A7）なので、付箋表示がその「別ビュー」を兼ねられるかは検討に値する

### 2 つに共通する判断

- どちらも、クラスタリングの正しさではなく **「読者が全体から個別へ辿れるか」** という表示 artifact の問題で、[[analysis-stance]]（構造把握スタンス）と [[tokoroten-algorithm-discussion-retrospective]] の「分析 artifact / 表示 artifact / 説明 artifact を分ける」整理に乗る
- 本流に入れる前に、CLI の artifact として出し、同じデータで既存の散布図・階層リストと読み比べる。これは [[experiment-methodology]] の「clean experiment は 1 要素だけ変える」と同じ型で、今回は変える要素が表示方法になる
- Web UI は simple に保つ方針（[[cli-pipeline-experiment-roadmap-2026-06-02]]）に従うなら、最初の置き場は CLI の `visualization` 出力か、実験的機能カタログ（[[experimental-features-catalog-proposal-2026-06-03]]）になる

## 3. tokoroten の分析手法 2 つをどう取り込むか

[[tokoroten]] が書籍 13.4.3「賛否分離」で「次に手を入れる場所」として示し、2025-11〜12 の定例で実装・報告した 2 手法。どちらも **同じトピックの中に賛否が混在すると、政治家にとっての洞察（何が対立しているか）に繋がらない** という問題意識から出ている。[[broad-listening-book-extractions]]より [[kouchou-ai-direction-2025-12-06]]より

| | センチメント次元の付与（sentiment-weighted UMAP） | DivCon（Divide and Conciliate） |
|---|---|---|
| 仕組み | 抽出時に LLM が賛否スコア（-1.0〜+1.0）を推定し、重みを掛けて埋め込みベクトルに連結してから UMAP。重みを上げるとトピック内で賛否が分かれ、上げすぎるとトピックの類似性が消える | 埋め込みを使わない。LLM の long context でトピック発見 → 意見分類 → 対立軸の発見 → アンカー生成 → スコアリング。強硬な意見が上位に並ぶ「対立ビュー」を出す |
| 現物 | 2025-11 の「センチメントスライダー」デモとコード（netlify 配布、[[tokoroten]] 個人）。本体 repo 外 | `tokoroten/divcon`（最終更新 2025-11-20）。自治体データで試行。本体 repo 外 |
| 広聴AI の現行機能との関係 | 散布図を保ったまま賛否を分ける。**`classic_scatter` モードの拡張** | 散布図を持たない group-first の分析。**`analysis_mode=llm_grouping` 系の兄弟**（[[pr-827-llm-grouping-capabilities-plan-2026-05-18]]） |
| 既にある足場 | 意見ごとに LLM で yes/no のラベルを付ける任意ステップ `opinion_classification`（[#971](https://github.com/digitaldemocracy2030/kouchou-ai/issues/971)、結果は `arguments[].attributes` に入り属性フィルタで使える）。賛否スコアは同じ形の「意見ごとの属性」として載せられる | `llm_grouping` の実装と、分析結果の性質（座標があるか、階層があるか）から使える可視化を判定する capability の計画。対立軸は新しい capability になる |

### 取り込みの案（順序つき）

1. **まず所在を公開 docs に固定する**。実験的機能カタログ（[[experimental-features-catalog-proposal-2026-06-03]]）に 2 手法を「tokoroten、別 repo、最終確認日」つきで載せる。コードを本体に入れる前にできる最小の一手で、stale になっても「いつ時点か」が残る
2. **賛否スコアを「意見ごとの属性」として CLI に入れる**。`opinion_classification` と同じ任意ステップとして、抽出済みの意見に -1.0〜+1.0 のスコアを付け、`attributes` に入れる。これだけで属性フィルタによる「賛成だけ / 反対だけの地図」が既存 UI で見られる。LLM 呼び出しの形は [#971](https://github.com/digitaldemocracy2030/kouchou-ai/issues/971) の経路を再利用でき、WebUI には触らない（CLI 先行の方針）
3. **埋め込みへの重み付き連結を、embedding ステップの任意設定として試す**。採用判断は [[experiment-methodology]] に従い、同じ corpus・同じクラスタリング・同じラベリングで `sentiment_weight` だけを変えた clean experiment を回す。書籍の「weight=0.75 で風力発電クラスタが賛否で分離」を再現できるかが最初の問い。評価は「賛否で分かれたか」だけでなく「トピックの近さが壊れていないか」を同時に見る
4. **DivCon は LLM grouping 系の mode として設計し直してから入れる**。埋め込みを使わないので、`llm_grouping` と同じく散布図を出せない。対立軸・アンカー・スコアを結果 JSON にどう持たせ、どの可視化（対立ビュー）がそれを要求するかを capability として先に決める。実装は tokoroten の repo を移植するより、`llm_grouping` のステップ構造に合わせて書き直す方が本体の保守に乗る。用語は「LLM grouping の一例」として扱い、Jigsaw Sensemaker と混同しない（Sensemaker が「long context で 2 階層ツリーを作ってから一次データを分類する」のと同じ型で、DivCon は「long context で対立構造を作ってから分類する」。2025-12 定例での整理）
5. **Web UI には最後に載せる**。2026-05 の Slack で「DivCon を Web UI に載せるのが複雑すぎて発展が抑制されている」という認識が出ており（[[slack-stance-discussion-2026-05-30]]）、CLI で artifact を貯めてから昇格判断する、という既存方針と同じ扱いにする

### 判断が要ること

- **誰が主担当か**。2 手法とも tokoroten の個人 repo にあり、本体への移植は tokoroten 本人か、tokoroten の了解のもとで AI エージェントが進めるかを決める必要がある。2025-12 の時点で tokoroten は「今すぐ自分がやりたいわけではない」と述べていた（[[kouchou-ai-direction-2-2025-12-13]]）
- **評価データ**。賛否分離の効果を見るには、賛否が混在する実データ（パブコメなど）が要る。書籍の電力政策パブコメ約 1,000 件と同等のものを、公開できる形で用意できるか
- **成果物の約束**。「対立を可視化する」を広聴AI の機能として出すなら、分析根拠・分類基準・プロンプトを説明 artifact として残す必要がある（[[tokoroten-algorithm-discussion-retrospective]]）。散布図に賛否の色を載せるだけなら軽いが、「対立ビュー」を出すなら説明責務が増える

## Open Questions

- nishio の言う「ドリルダウンのツリー表示」が、2-a の Claude 実験のドリルダウンと [#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880) のマンダラートのどちら（または両方）を指すか。「ズームできる付箋表示」が `canvas_kozaneba_prototype` を指すかも未確認。このページは既存の記録から推定して書いた
- 2 つの可視化の最初の置き場（CLI の standalone HTML か、公開ビューアの plugin か、Kozaneba 側か）
- tokoroten の 2 手法を本体に入れるかどうか自体と、入れるなら主担当
- 第 3 弾レビューで確定したが設計判断待ちの指摘（結果 JSON 全体の HTML 埋め込み、静的書き出しの全件再生成、LLM 直接グルーピングの逐次割当、抽出 1 件の失敗で全体停止、論理削除など）の扱い。2-a・2-b の置き場の判断と絡む
- 猶予期間の運用（先行連絡 → 1 週間 → 同日公開）を次回も同じにするか。今回は影響ユーザが限られていたので成立した

## Updates

- 2026-10-28: 初回作成
