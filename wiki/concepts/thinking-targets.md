---
title: "今考えるべき論点の思考ハブ"
name: thinking-targets
type: concept
summary: "今、人間の思考と判断が要る論点を 1 ページに集めた思考ハブ。完了報告は meeting-report-draft、未着地論点の全体棚卸しは open-decisions、ここは『次に考えると進むもの』だけに絞る"
sources:
  - meeting-minutes.md
  - github-dev-docs.md
  - source-code.md
  - current-status-2026-06-30.md
  - docs-issue-map-2026-06-30.md
  - event-2026-08-02-broadlistening-readiness-2026-06-30.md
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - japan-broadlistening-use-case-map-2026-06-30.md
  - public-case-page-skeleton-2026-06-30.md
  - report-reading-guide-minimum-wording-2026-06-30.md
  - broad-listening-book-public-case-appendix-2026-06-30.md
  - meeting-brand-compass-information-strategy-2026-06-30.md
  - meeting-municipality-user-research-scope-2026-06-30.md
  - github-issues-221-884-trial-burden-live-2026-06-30.md
  - development-next-actions-live-2026-06-30.md
  - slack-logs-repository.md
  - meeting-cartographer-idobata-boundary-2026-06-30.md
  - public-tool-catalog-draft-2026-06-30.md
  - slack-prance-event-broadlistening-session-2026-06-30.md
---

このページは **「次に何を考えれば前に進むか」だけ** を集める。

- 完了した作業の報告は [[meeting-report-draft]] へ
- 未着地論点の全体カタログは [[open-decisions]] へ
- 設計判断の core stance は [[analysis-stance]] へ (広聴AI = 構造把握スタンス、定量分析スタンスではない)
- ここは「思考と判断が入れば、実装 / 実験 / PR がはっきり動き出す論点」のみ

各項目には `問い / 思考の最小単位 / どう決まれば動けるか / 関連ページ` を置く。問いの解像度が上がって実装フェーズに入ったらここから外し、関連 analysis ページへ送る。

## 0. 2026-06-30 immediate thinking queue

> この 0 章は 2026-06-30 時点の queue。2026-10-21 時点の状況は次のとおり（日付は GitHub の UTC 表記）。
> - 0-1: 8/2（デジタル民主主義サミット2026）は日付を過ぎた。結果は wiki に未記録
> - 0-2: [#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696)（レポートの誤読防止。PR [#924](https://github.com/digitaldemocracy2030/kouchou-ai/issues/924) で読み方ガイドを表示、2026-09-08）と [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)（責任の所在。PR [#1004](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1004) で 2026-10-13 close。docs ページは PR [#1003](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1003)、英語・韓国語 README は PR [#1008](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1008)）は完了した。残る問いは [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) の公開事例ページの置き場所だけ
> - 0-3（docs-safe PR の順序）は決着した: [#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877)（Windows セットアップ、PR [#929](https://github.com/digitaldemocracy2030/kouchou-ai/issues/929)、2026-09-08）と [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876)（開発者向け導線、2026-10-13）が close し、[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) 向けの Node runtime 依存インベントリ PR [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) も 2026-09-08 に merge された。[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) 本体は open のまま（[[issue-885-node-runtime-next-scope-2026-06-30]]）
> - 0-4（作成前確認パネル）は決着した: [#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) は PR [#922](https://github.com/digitaldemocracy2030/kouchou-ai/issues/922)（2026-09-08）で完了し、[#97](https://github.com/digitaldemocracy2030/kouchou-ai/issues/97)（PR [#923](https://github.com/digitaldemocracy2030/kouchou-ai/issues/923)）と [#391](https://github.com/digitaldemocracy2030/kouchou-ai/issues/391)（PR [#922](https://github.com/digitaldemocracy2030/kouchou-ai/issues/922) / [#926](https://github.com/digitaldemocracy2030/kouchou-ai/issues/926) の merge 後）も 2026-09-08 に close した。[#221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/221)・[#11](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11)・[#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79)・[#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292) は open で、費用・所要時間の目安（[#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79) / [#11](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11)）の残件は [[issue-backlog-audit-2026-09-09]] にある
> - docs まわりの経緯は [[kouchou-ai-docs-policy-history]]、全体の現在地は [[current-status-2026-10-05]] を読む

6/30 の source refresh で、直近の「考えると進むもの」は 5/30 時点のラベル品質だけではなくなった。Slack / 議事録 / GitHub live state を合わせると、6/30 時点では **8/2 に何を見せるか / 誰が実践 lane を担うか**、**公開事例と trust layer をどこに置くか**、**[#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) を次の code-safe slice にするか**、**docs-safe PR をどの順で切るか** が人間判断待ちだった（後ろの 2 つは上の注記のとおり決着した）。[[current-status-2026-06-30]]より

Brand Compass は、この queue の外に別途置く議題というより、8/2 first demo、[#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564)/[#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696)/[#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)、docs-safe PR の選び方をふるいにかける上位フィルタとして扱う。議事録上では、stable v4 / M2、情報発信、外部向けの「聞く能力」ストーリー、自治体利用者課題調査、A/B/C/D 配布形態が同じ方向に接続している。[[meeting-brand-compass-information-strategy-2026-06-30]]より

さらに、議事録からは「広聴AI / いどばた / Cartographer / Jigsaw Sensemaker / tttc-light-js」を全部 `ブロードリスニング` と呼ぶと、収集・深掘り・分析・可視化・LLM grouping（LLM 直接グルーピング）が混ざることが見えている。8/2 や [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) では tool ecosystem を出す前に、どの lane を広聴AI本体の約束とするかを決める必要がある。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

### 0-1. 8/2 の first demo を何にするか

- 問い: 8/2 で、自治体公式 proof、viewer demo、deep case のどれを主 artifact にするか。さらに、実践 lane の主役・話者文脈を first demo と同じものにするか分けるか。奈良市 official PDF / 奈良 #全員市長 / 八代 / 舞鶴2040 / 北見 / 渋谷区 / 宇多津町 / 岩手県 / 東京都を同列に見せると、政治文脈、公式性、viewer 実演、Talk to the City 系譜が混ざる
- 思考の最小単位: `公式性を示す 1 件`、`viewer 操作を見せる 1 件`、`深掘り case 1 件`、`実践 lane の話者候補 1 件` を人間が選ぶ。候補ごとに source strength、政治・選挙文脈、許諾・スクリーンショット可否、話者文脈を 1 行で見る。`#dd_prance_event2026` では奈良 / 舞鶴2040 が地方自治側の planning lead として再浮上したが、Slack-only lead は外部 proof にせず primary public source に戻す。Web book 付録由来の大阪府 / チームみらい / DirectVote / サイボウズ / アルティウスリンク / 与謝野町は 2026-06-30 17:30 JST に public source を確認済み、Code for Japan / 加古川市・品川区、公明党 We Connect、litela Recogra、富士通パブリックコメント AI は 18:13 JST に public source ありへ進めた。ただし first demo ではなく、`広義 broad listening` / `政党・政策形成` / `TTTC lineage` / `企業・VOC` / `AI 支援住民対話 adjacent` / `implementation partner` / `対面議論支援` / `LLM grouping adjacent` として別枠に置く。長崎県知事選は public report URL 未確認の候補に残す。Brand Compass 観点では、demo が `聞く能力` の story と A/B/C/D 配布形態のどこに当たるかも 1 行で添える
- 決まれば動けること: 8/2 向けの公開スライド / docs / event page で、何を安全に見せるかが決まる
- 関連: [[event-2026-08-02-broadlistening-readiness-2026-06-30]], [[event-2026-08-02-public-example-inventory-2026-06-30]], [[japan-broadlistening-use-case-map-2026-06-30]], [[slack-prance-event-broadlistening-session-2026-06-30]], [[broad-listening-book-public-case-appendix-2026-06-30]], [[meeting-brand-compass-information-strategy-2026-06-30]]

### 0-2. [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) の公開事例ページをどこに置くか

- 問い: [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) の公開事例リスト（と、そこから入る初回説明）を DD2030 website と kouchou-ai docs のどちらに置くか。レポートの読み方はレポート画面の読み方ガイド（[#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696)）、責任の所在と FAQ は kouchou-ai docs（[#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)、PR [#1003](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1003) / [#1004](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1004)）に置かれたので、事例ページからそれらへの導線もあわせて決める
- 思考の最小単位: canonical copy を 1 つ決め、他の surface は短い導線にする。[#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) の本文に 2026-09-09 付けで足された案（事例の単位を「レポートが作れた」から「どの問いに使い、その後の対話・判断がどう変わったか」へ広げ、対象の問い / 収集方法と偏り / 利用した版・分析方法 / 元の声との照合 / 読者が取った次の行動 / うまくいかなかった点 / 出典と公開範囲をそろえる）に沿って、1 件目の事例でそろえる項目を決める。A/B/C/D 配布形態を public page に出す場合、D hosted trial は現状未提供として表現する（kouchou-ai docs も、誰かが運用する managed サービスは現状提供されていないと書いている）
- 決まれば動けること: [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) の case page first slice を切れる
- 関連: [[public-case-page-skeleton-2026-06-30]], [[report-reading-guide-minimum-wording-2026-06-30]], [[issue-564-public-case-trust-layer-scope-2026-06-30]], [[meeting-brand-compass-information-strategy-2026-06-30]], [[kouchou-ai-docs-policy-history]]

### 0-5. Slack / 議事録 source 運用の次の固定

- 問い: `digitaldemocracy2030/slack-logs` を Slack raw 一次 source として定着させた後、既存の `oss_weekly_reporter` source をどこまで置き換えるか。また、議事録 `2026/06/29` 見出しが export に出た時、どの source / analysis を先に更新するか
- 思考の最小単位: Slack は raw/mirror を一次、weekly reporter は GitHub activity と AI 要約の補助線、という役割を canonical docs にどこまで反映するか決める。2026-06-30 時点では、一括置換せず、直近 Slack は `mirror/`、古い Slack は `raw/`、週次流れは既存 `weekly-log-*` / `oss_weekly_reporter` を残す三分法に寄せた
- 決まれば動けること: 今後の wiki ingest が「どのログを先に読むか」で迷わなくなる
- 関連: [[slack-logs-repository]], [[current-status-2026-06-30]], [[wiki-driven-workflow]]

### 0-6. 自治体利用者課題調査をどう切るか

- 問い: 自治体向けアンケート / user research を、広聴活動一般の実態調査として広く聞くのか、広聴AIが活きるケース発見に絞るのか、2 つの instrument に分けるのか。既存接点は広聴AIを入口にした広報・広聴課 / デジタル推進部署に偏っている可能性がある
- 思考の最小単位: `広聴活動一般の探索` と `広聴AI適合ケースの探索` のどちらを先に聞くか決める。対象部署、役割、人数規模、sampling route、Cartographer / いどばた / 広聴AI のどれに解くべき課題かを 1 枚に分ける
- 決まれば動けること: user research instrument を public case intake と混ぜずに作れる。[#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) の case intake は public artifact / 掲載許諾 / source strength、user research は roadmap 前提検証として分けられる
- 関連: [[meeting-municipality-user-research-scope-2026-06-30]], [[meeting-brand-compass-information-strategy-2026-06-30]], [[public-case-page-skeleton-2026-06-30]]

### 0-7. 企業 / VOC / 広義 broad listening を公開事例ページに入れるか

- 問い: サイボウズ / アルティウスリンクのような企業・VOC case、大阪府のような広義 broad listening case、DirectVote / チームみらいのような政党・TTTC lineage case、Code for Japan / 公明党 / litela / 富士通のような implementation partner / adjacent AI case を、DD2030 website の `kouchou-ai/case` に同居させるか、ブロードリスニング全体 / 応用領域 / 系譜ページへ分けるか
- 思考の最小単位: first page の読者を `自治体導入検討者` に固定するか、`国内 broad listening の広がりを知りたい人` まで広げるかを決める。前者なら first 3 は自治体公式 + viewer + deep case に絞り、企業/VOC、TTTC lineage、政党 AI、implementation partner verified、LLM grouping adjacent は後段または別ページに送る
- 決まれば動けること: [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) public page の章立てと、Web book 付録由来候補の掲載基準を固定できる
- 関連: [[public-web-broadlistening-japan-use-cases-2026-06-30]], [[japan-broadlistening-use-case-map-2026-06-30]], [[public-case-page-skeleton-2026-06-30]], [[broad-listening-book-public-case-appendix-2026-06-30]]

### 0-8. 広聴AI / いどばた / Cartographer / 外部の LLM grouping ツール（Jigsaw Sensemaker・tttc-light-js）の tool catalog をどこに置くか

- 問い: `広聴AI = 収集済み自由記述の分析・可視化`（既定は埋め込み＋階層クラスタリング。LLM grouping も `analysis_mode=llm_grouping`（LLM 直接グルーピング）として持つ）、`いどばた / Cartographer = 収集・深掘り`、`Jigsaw Sensemaker / tttc-light-js = LLM grouping 寄りの外部ツール例`（Sensemaker は Polis 型データ向け、tttc-light-js は TTTC 系譜の固定 pipeline で散布図なし）という役割境界を、DD2030 website、kouchou-ai docs、8/2 event material、[#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) case page のどこに置くか。LLM grouping は方法のカテゴリ名で、特定の外部ツールの名前ではない（[[jigsaw-sensemaker]]）
- 思考の最小単位: [[public-tool-catalog-draft-2026-06-30]] の `collect / deepen / analyze / show / classify / read-and-act` を、外部正本へ置くかどうか決める。対立軸発見は魅力的だが、現行 default ではなく LLM grouping / long-context route の未決論点として表現する
- 決まれば動けること: 8/2 のツール比較、[#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) の初回説明 FAQ、自治体 user research の質問項目、idobata bridge の owner 論点を同じ language で扱える
- 関連: [[public-tool-catalog-draft-2026-06-30]], [[meeting-cartographer-idobata-boundary-2026-06-30]], [[broadlistening]], [[idobata]], [[jigsaw-sensemaker]], [[talk-to-the-city]], [[meeting-municipality-user-research-scope-2026-06-30]]

## 1. ラベル品質改善の仕切り直し: 5 レイヤ

`label refinement` 実験は polish-only だったため採用候補から外し、品質を作る入力 / 表示する証拠 / 判定する judge を別々に再設計する方針にした。詳細フレーミングは [[label-quality-redesign-reset-2026-05-30]]。

**1-1 は 2026-05-30 の対話で確定済み**: ユースケース契約 = 「全体傾向把握ユースケース」一本。Web UI には契約選択を露出しない。少数重要論点ユースケースは CLI 分析者の prompt 責務で、product として educate しない。全体傾向把握 run の minority residual artifact も作らない。これにより下流 4 レイヤは全体傾向把握最適化で揃う。

### 1-2. ラベル生成入力の sampling (全体傾向把握ユースケース前提)

- 問い: 高頻度トピックの安定カバーを目的とするとき、cluster 内 N 件から LLM に見せるのは全件か、最大被覆 / k-medoids で選んだ部分集合か (FPS は外れ値保存なので全体傾向把握用には外す)
- 思考の最小単位: cluster size 別に「全件入力した時の token / cost / latency」を試算する (現状 API 経路 30 件 / CLI 既定 3 件は seed なし random)
- 決まれば動けること: refinement / judge / UI 表示の全レイヤが共通の入力契約に乗る
- 関連: [[label-coverage-policy-2026-05-29]], [[label-refinement-input-scope-2026-05-29]]

### 1-3. 代表例 artifact (全体傾向把握ユースケース前提)

- 問い: UI と judge が見る `rep args` を `典型例 + 幅` 主軸で構成するとして、どう生成するか。境界例は全体傾向把握の主入力ではないので脇に置く
- 思考の最小単位: 1 クラスタを手元で取って「典型例 2 + 幅 2」を embedding と LLM の併用で実際に作ってみる
- 決まれば動けること: aggregation step に組み込むか独立 step にするかが決まり、UI 個別データ表示と judge 入力を同じ artifact で揃えられる
- 関連: [[label-coverage-policy-2026-05-29]] (論点 2), [[pipeline-step-addition-framing-2026-05-27]]

### 1-4. judge の較正 (全体傾向把握ユースケース前提)

- 問い: rubric v0 は過去出力でほぼ満点だった (score_rate 1.0 / 0.9766, fatal 0)。全体傾向把握用の rubric として coverage と sibling distinction を重く採点する設計に書き換えるとき、何を criteria として落とすか / 何を fatal とするか
- 思考の最小単位: 既存 `[8,40] refine_{none,setwise,contrast,balanced}` bundle に対して、人間判断を 1 セット記録し、rubric が落とすべきラベルを 1〜2 件特定する。minority residual の検出は採点対象に入れない
- 決まれば動けること: rubric criteria のどこを締めるかが具体化する
- 関連: [[label-quality-rubric-evaluation-2026-05-29]], [[label-refinement-judge-bundle-2026-05-25]]

### 1-5. refinement の責務

- 問い: 現行 `hierarchical_label_refinement` は polish-only。全体傾向把握前提で「カバレッジを示す要約として整える」責務に統合するか、それとも上流 sampling 改善で polish 不要に近づけるか
- 思考の最小単位: 1-2 の全件入力実験の結果を待ち、それでもラベルがカバレッジを示せない場合に何が起きているかを観察する
- 決まれば動けること: PR / branch をどう畳むかが決まる
- 関連: [[label-refinement-input-scope-2026-05-29]]

## 2. 次の分析モード / 公開UI の方向

散布図前提を外す条件と、その先の view 設計をどう詰めるか。

### 2-1. 散布図の役割再定義と並走条件

- 問い: 「散布図を 2026-09 書籍リリース時点まで温存」「より良い view が見つかれば併用→デフォルト切替」という時間軸スタンス ([[open-decisions]] A1) を、具体的にどんな比較基準で切り替えるか
- 思考の最小単位: 散布図が今担っている説明責務 5 要素 ([[public-ui-requirements-for-broadlistening]]) を、`semantic island map` やマンダラート（[#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880)）などの代替で何 % 満たせれば併用 / 切替に進むかを書く
- 決まれば動けること: prototype 評価の合否ラインができる
- 関連: [[llm-grouping-background-history]], [[ohki-discussion-reflection-2026-05-25]]

### 2-2. `semantic island map` の合否基準 (構造把握用主図候補)

- 問い: cluster 間と cluster 内を分離する `semantic island map` ([[semantic-island-map-prototype-2026-05-26]]) は、構造把握用の主図として広聴AI 本体に入れる候補。「公開UI で散布図の代替たり得る」と判定する基準は何か
- 思考の最小単位: 422 argument / 8 cluster の prototype に対して、(a) 公開UI 7 要件のうち広聴AI 本体担当 5 件、(b) 構造把握の評価軸 (解説素材性 / 突合素材性) ([[analysis-stance]]) の 2 軸、を満たす / 満たさない / 部分の 3 値で評価する
- 決まれば動けること: prototype の次の iteration を見るべきか、別方式へ振り直すかが決まる
- 関連: [[semantic-island-map-prototype-2026-05-26]], [[public-ui-requirements-for-broadlistening]], [[analysis-stance]]

### 2-3. KJ 法の「現場に返却する」（継続関与）を広聴AI でどう扱うか

- 前提: [[kj-method-broadlistening-framing-2026-05-25]] が挙げる KJ 法的な 6 原則のうち、原則 3〜5（表札は AI が確定しない・少数や矛盾や分類困難を残す・論点の構造を示す）は、2026-05-30 に「広聴AI 本体には入れず、別ツール（CLI の実験機能と共有コミュニティ）で補完する」と決まった（3-1、[[analysis-stance]]）。なお表札（クラスタのラベル）は、管理画面の「意見グループ編集」（作成済みレポートの操作メニューから開く）で人が書き換えられる。ただし編集は任意で、公開前に人の確認を求める工程はなく、編集しなければ AI のラベルがそのまま表示される（新規レポートは限定公開で作られる）
- 問い: 本体側の候補として残る原則 6「現場に返却する」（一回限りの分析で終わらせない継続関与）を、広聴AI でどう扱うか。product 単体では決まらず、書籍リリースや実証実験・運用と組にして考える問いである（[[kj-method-broadlistening-framing-2026-05-25]]）
- 思考の最小単位: 同じ主体が同じテーマで意見を集め直す場面を 1 つ想定し、「前回の結果を現場に返す」「次の問いを立てる」「前回と比べる」のうち、製品が支えるものと運用・実証実験に任せるものを 1 行ずつ分ける
- 決まれば動けること: 継続関与のうち製品で支える部分だけを Issue に切り出し、残りを実証実験・運用の設計へ回せる
- 関連: [[kj-method-broadlistening-framing-2026-05-25]], [[analysis-stance]], [[broadlistening-tool-ecosystem-vision]]

## 3. Pipeline 設計の境界

「step 数」ではなく「新しい成果物責務を first-class にすべきか」で判断する方針 ([[pipeline-step-addition-framing-2026-05-27]]) のもと、未決のもの。

### 3-1. `interpretation_artifacts` を切るか (2026-05-30 暫定: 広聴AI 本体には入れず別ツール)

- 暫定判断 (2026-05-30): KJ 原則 3〜5（表札の人間吟味・少数残存・構造を示す）を「広聴AI 本体には入れず別ツールで補完」とした構造把握スタンス採用判断 ([[analysis-stance]]) により、`interpretation_artifacts` 系 (境界 / 反例 / bridge / 未解決カード) は **広聴AI 本体に常時組み込まない** 方向に倒れた。実験経路としては残せる
- 残る問い: 「別ツール」のエコシステムが具体化していない。何ツールがどこで担い、広聴AI とどう接続するかは未整理。これは思考というより **意思決定責任 / 体制** の問題 (block 4 系)。あわせて、原則 3〜5 のどれから CLI の実験機能として試すかも残る。比べる軸は、実装コスト・公開 UI での価値・既存 schema との衝突
- 関連: [[pipeline-step-default-policy-decision-2026-05-28]], [[public-ui-requirements-for-broadlistening]] の 7 要件のうち要件 5（少数意見の埋没回避）と要件 7（次の問いの可視化）が別ツール担当に倒れた

### 3-2. `analysis_mode` の分岐構造

- 問い: `llm_grouping` ([#866](https://github.com/digitaldemocracy2030/kouchou-ai/issues/866) で merge) の後、`label refinement` / `interpretation_artifacts` / 次の view 用 layout 生成などをどう mode と直交させるか
- 思考の最小単位: mode と option の二軸で、現在の `hierarchical_default` と将来 mode 候補 3 つを表にする
- 決まれば動けること: 次の analysis_mode を追加する時の workflow / spec 切り出し方が決まる
- 関連: [[llm-grouping-implementation-plan]], [[plugin-system]]

## 4. 公開・運用の摩擦 (重要だが直近の思考優先度は下)

実装ではなく **責任主体と運用設計** が決まらないと動かない論点。直近 1〜2 週で取り組むか先送りかを意識的に決める対象。

- **静的 HTML のホスト先戦略** ([[open-decisions]] A2): SaaS ホストの責任主体が定まらない
- **private-by-default の既定値** ([[open-decisions]] A4): unlisted default か private default か
- **DB 導入のタイミング** ([[open-decisions]] A3): ファイルストレージ継続が暗黙の現状維持
- **論文投稿戦略** ([[open-decisions]] A12): 日本語 / 英語のどちらを主成果物にするか

これらは思考よりも **意思決定責任** の問題に近い。次の定例で「直近 1 ヶ月で動かす / 動かさない」を決め、動かすものはここから外して [[open-decisions]] の C へ送るのがよい。

## ナビゲーション

- 完了報告 / Codex の進捗 → [[meeting-report-draft]]
- 未着地論点の全体棚卸し (A 未定 / B 方針あり未着手 / C 着手済み未完) → [[open-decisions]]
- 長期方向 → [[strategic-development-order-2026-05-23]], [[issue-priority-through-2026-09]]
- 残 issue 戦術優先順 → [[remaining-issue-priority-2026-05-29]]

## 使い方

- 思考が進んで「問い」が「実装の slice」に変わったら、ここから外して関連 analysis に Updates を追記し、[[meeting-report-draft]] か [[open-decisions]] C に動かす
- 新しい論点が出たら「問い / 思考の最小単位 / 決まれば動けること / 関連ページ」の 4 行で追加する。長い経緯は本文ではなく関連ページに送る
- 1 セクションあたり 3〜5 項目を超えそうになったら、優先 3 項目に絞り、残りは [[open-decisions]] へ降ろす

## Updates

- 2026-06-30: `#dd_prance_event2026` source と 19:15 JST GitHub live check を反映し、0-1 を first demo だけでなく実践 lane の話者・文脈選定まで含む問いに補正。
- 2026-06-30: [[development-next-actions-live-2026-06-30]] を追加し、開発 next action は [#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) 作成前確認パネルを第一候補、[#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) review comment を低リスク補助、[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) / [#898](https://github.com/digitaldemocracy2030/kouchou-ai/issues/898) を次点として見ると 0-4 に追記。
- 2026-06-30: 18:13 JST の book 章確認を反映し、Code for Japan / 公明党 / litela / 富士通は first demo ではなく implementation partner / adjacent practice として 0-1 と 0-7 に追加。
- 2026-06-30: 17:30 JST の direct verification を反映し、大阪府 / チームみらい / DirectVote / サイボウズ / アルティウスリンク / 与謝野町を first demo ではなく source strength / tool lineage で分ける判断を 0-1 と 0-7 に追加。
- 2026-06-30: [[github-issues-221-884-trial-burden-live-2026-06-30]] を追加し、[#221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/221)/[#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) 作成前確認パネルを次 code-safe slice 候補として immediate queue に追加。
- 2026-06-30: 追加Web検索で奈良市 official PDF 群を自治体公式 proof に昇格し、奈良市 document case と奈良 #全員市長 viewer demo を 8/2 first demo 判断で分ける必要を追記。
- 2026-06-30: 6/30 の source refresh と wiki 更新を反映し、8/2 first demo、[#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564)/[#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696)/[#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542) trust layer placement、docs-safe PR 順序、Slack / 議事録 source 運用を immediate thinking queue として先頭に追加。
- 2026-05-30: 用語を descriptive な日本語に統一 (`contract A` → 全体傾向把握ユースケース、`β / α` → 構造把握スタンス / 定量分析スタンス など)
- 2026-05-30: 構造把握スタンス / 全体傾向把握ユースケース / 別ツール 分業の含意を関連ページに伝播。[[public-ui-requirements-for-broadlistening]] に 7 要件のうち #5 / #7 は別ツール側、本体 5 件 + 構造把握の評価軸 2 件で評価する、を追記。[[semantic-island-map-prototype-2026-05-26]] に構造把握用主図候補としての評価視点を追記。[[kouchou-ai]] に core stance リンクを追加。3-1 を別ツール側に倒れた旨で更新、2-2 を構造把握の評価軸を含む合否基準に補正
- 2026-05-30: 「広聴AI = 構造把握スタンス」を [[analysis-stance]] として概念ページ化。全体傾向把握ユースケースは構造把握スタンスで実現、定量分析スタンスではない、を core stance に明示
- 2026-05-30: 1-1 ユースケース契約が確定 (全体傾向把握ユースケース一本)。Web UI 非露出、少数重要論点系は CLI 分析者責務、minority residual artifact なし。下流 1-2〜1-5 を全体傾向把握前提で書き換え。詳細判断は [[label-quality-redesign-reset-2026-05-30]] に
- 2026-05-30: 初版。「考えることをやりたい」という方針を受け、思考と判断が要る論点だけを 1 ページに集めるハブとして新設。ラベル品質仕切り直し 5 レイヤ、次の view 方向、pipeline 境界、公開・運用摩擦の 4 ブロックで構成
- 2026-10-07: lint 注記。0 章の immediate queue は 2026-06-30 時点のもの。0-4 の [#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) は 2026-09-08 に PR [#922](https://github.com/digitaldemocracy2030/kouchou-ai/issues/922) で CLOSED、0-3 の [#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877) も 2026-09-08 に CLOSED（[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) / [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) は open）。0-1 の 8/2 event は日付を過ぎたが結果はこの wiki に未記録。現在地は [[current-status-2026-10-05]] を先に読む
- 2026-10-21: GitHub と kouchou-ai main（b71e0b79）に照合して決着済みの論点を整理した。0 章冒頭の状況注記を 2026-10-21 時点に書き直し、決着した 0-3（docs-safe PR の順序）と 0-4（作成前確認パネル）を外して、0-2 を [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) の置き場所に絞った。2-4（スマホ別ビュー、[#872](https://github.com/digitaldemocracy2030/kouchou-ai/issues/872)）は PR [#933](https://github.com/digitaldemocracy2030/kouchou-ai/issues/933)（2026-09-08 UTC merge）で「幅 600px 以下は階層リストを初期表示し、専用画像は作らない」と決着したので外した（散布図そのものの課題 [#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121) / [#266](https://github.com/digitaldemocracy2030/kouchou-ai/issues/266) は [[open-decisions]] A7、マンダラート [#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880) は 2-1 の代替候補へ）。2-3 は 3-1 の決定（原則 3〜5 は別ツール）と食い違っていたので継続関与（原則 6）の問いに絞り、表札は管理画面で任意に編集できると訂正した。0-8 は LLM grouping（方法のカテゴリ）と外部ツール例を分け、広聴AI も `analysis_mode=llm_grouping` を持つ（PR [#866](https://github.com/digitaldemocracy2030/kouchou-ai/issues/866) で 2026-05-28 UTC に analysis-core へ merge、PR [#987](https://github.com/digitaldemocracy2030/kouchou-ai/issues/987) で 2026-10-12 から作成画面でも選べる）と明記した。1-2 の CLI 既定のラベル生成サンプル数を 10 件から 3 件に訂正した。2026-10-07 の行は、後日の出来事（[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) の close）が書き足されていたので当日の文言に戻した。KJ 原則・公開 UI 要件の番号（3〜5、5・7）が無関係な広聴AI の Issue へのリンクになっていたのを外し、原則名・要件名を添えた
