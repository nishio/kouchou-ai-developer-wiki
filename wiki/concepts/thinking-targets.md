---
name: thinking-targets
type: concept
summary: "今、人間の思考と判断が要る論点を 1 ページに集めた思考ハブ。完了報告は meeting-report-draft、未着地論点の全体棚卸しは open-decisions、ここは『次に考えると進むもの』だけに絞る"
sources:
  - meeting-minutes.md
  - github-dev-docs.md
  - source-code.md
---

このページは **「次に何を考えれば前に進むか」だけ** を集める。

- 完了した作業の報告は [[meeting-report-draft]] へ
- 未着地論点の全体カタログは [[open-decisions]] へ
- 設計判断の core stance は [[analysis-stance]] へ (広聴AI = 構造把握スタンス、定量分析スタンスではない)
- ここは「思考と判断が入れば、実装 / 実験 / PR がはっきり動き出す論点」のみ

各項目には `問い / 思考の最小単位 / どう決まれば動けるか / 関連ページ` を置く。問いの解像度が上がって実装フェーズに入ったらここから外し、関連 analysis ページへ送る。

## 1. ラベル品質改善の仕切り直し: 5 レイヤ

`label refinement` 実験は polish-only だったため採用候補から外し、品質を作る入力 / 表示する証拠 / 判定する judge を別々に再設計する方針にした。詳細フレーミングは [[label-quality-redesign-reset-2026-05-30]]。

**1-1 は 2026-05-30 の対話で確定済み**: ユースケース契約 = 「全体傾向把握ユースケース」一本。Web UI には契約選択を露出しない。少数重要論点ユースケースは CLI 分析者の prompt 責務で、product として educate しない。全体傾向把握 run の minority residual artifact も作らない。これにより下流 4 レイヤは全体傾向把握最適化で揃う。

### 1-2. ラベル生成入力の sampling (全体傾向把握ユースケース前提)

- 問い: 高頻度トピックの安定カバーを目的とするとき、cluster 内 N 件から LLM に見せるのは全件か、最大被覆 / k-medoids で選んだ部分集合か (FPS は外れ値保存なので全体傾向把握用には外す)
- 思考の最小単位: cluster size 別に「全件入力した時の token / cost / latency」を試算する (現状 API 経路 30 件 / CLI 10 件は seed なし random)
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
- 思考の最小単位: 散布図が今担っている説明責務 5 要素 ([[public-ui-requirements-for-broadlistening]]) を、`semantic island map` などの代替で何 % 満たせれば併用 / 切替に進むかを書く
- 決まれば動けること: prototype 評価の合否ラインができる
- 関連: [[llm-grouping-background-history]], [[ohki-discussion-reflection-2026-05-25]]

### 2-2. `semantic island map` の合否基準 (構造把握用主図候補)

- 問い: cluster 間と cluster 内を分離する `semantic island map` ([[semantic-island-map-prototype-2026-05-26]]) は、構造把握用の主図として広聴AI 本体に入れる候補。「公開UI で散布図の代替たり得る」と判定する基準は何か
- 思考の最小単位: 422 argument / 8 cluster の prototype に対して、(a) 公開UI 7 要件のうち広聴AI 本体担当 5 件、(b) 構造把握の評価軸 (解説素材性 / 突合素材性) ([[analysis-stance]]) の 2 軸、を満たす / 満たさない / 部分の 3 値で評価する
- 決まれば動けること: prototype の次の iteration を見るべきか、別方式へ振り直すかが決まる
- 関連: [[semantic-island-map-prototype-2026-05-26]], [[public-ui-requirements-for-broadlistening]], [[analysis-stance]]

### 2-3. KJ 法的設計原則のうち、どれを次の slice に入れるか

- 問い: KJ 法的に見ると `表札の人間吟味 / 少数残存 / 対立・因果構造 / 継続関与` が未達。このうち最初に product 化するのは何か
- 思考の最小単位: 4 つを「実装コスト / 公開UI 価値 / 既存 schema との衝突」で 1 行ずつ評価する
- 決まれば動けること: pipeline に `interpretation_artifacts` を切るかの判断材料になる
- 関連: [[kj-method-broadlistening-framing-2026-05-25]], [[pipeline-step-addition-framing-2026-05-27]]

### 2-4. スマホ別ビュー方針 (#872)

- 問い: スマホでは散布図を別ビューに置き換えるとして、静的画像 / クラスタ一覧 / 簡略図 / マンダラート (#880) のどれを既定にするか
- 思考の最小単位: 1 つを選び、共有 URL 設計とアクセシビリティ / 画像生成コストを 1 段落で書く
- 決まれば動けること: `#872` 配下の最初の PR slice が切れる
- 関連: [[remaining-bug-issues-2026-05-26]], [[chart-scroll-ux-decision]]

## 3. Pipeline 設計の境界

「step 数」ではなく「新しい成果物責務を first-class にすべきか」で判断する方針 ([[pipeline-step-addition-framing-2026-05-27]]) のもと、未決のもの。

### 3-1. `interpretation_artifacts` を切るか (2026-05-30 暫定: 広聴AI 本体には入れず別ツール)

- 暫定判断 (2026-05-30): KJ 原則 #3 #4 #5 を「広聴AI 本体には入れず別ツールで補完」とした構造把握スタンス採用判断 ([[analysis-stance]]) により、`interpretation_artifacts` 系 (境界 / 反例 / bridge / 未解決カード) は **広聴AI 本体に常時組み込まない** 方向に倒れた。実験経路としては残せる
- 残る問い: 「別ツール」のエコシステムが具体化していない。何ツールがどこで担い、広聴AI とどう接続するかは未整理。これは思考というより **意思決定責任 / 体制** の問題 (block 4 系)
- 関連: [[pipeline-step-default-policy-decision-2026-05-28]], [[public-ui-requirements-for-broadlistening]] の 7 要件のうち #5 #7 が別ツール担当に倒れた

### 3-2. `analysis_mode` の分岐構造

- 問い: `llm_grouping` (#866 で merge) の後、`label refinement` / `interpretation_artifacts` / 次の view 用 layout 生成などをどう mode と直交させるか
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

- 2026-05-30: 用語を descriptive な日本語に統一 (`contract A` → 全体傾向把握ユースケース、`β / α` → 構造把握スタンス / 定量分析スタンス など)
- 2026-05-30: 構造把握スタンス / 全体傾向把握ユースケース / 別ツール 分業の含意を関連ページに伝播。[[public-ui-requirements-for-broadlistening]] に 7 要件のうち #5/#7 は別ツール側、本体 5 件 + 構造把握の評価軸 2 件で評価する、を追記。[[semantic-island-map-prototype-2026-05-26]] に構造把握用主図候補としての評価視点を追記。[[kouchou-ai]] に core stance リンクを追加。3-1 を別ツール側に倒れた旨で更新、2-2 を構造把握の評価軸を含む合否基準に補正
- 2026-05-30: 「広聴AI = 構造把握スタンス」を [[analysis-stance]] として概念ページ化。全体傾向把握ユースケースは構造把握スタンスで実現、定量分析スタンスではない、を core stance に明示
- 2026-05-30: 1-1 ユースケース契約が確定 (全体傾向把握ユースケース一本)。Web UI 非露出、少数重要論点系は CLI 分析者責務、minority residual artifact なし。下流 1-2〜1-5 を全体傾向把握前提で書き換え。詳細判断は [[label-quality-redesign-reset-2026-05-30]] に
- 2026-05-30: 初版。「考えることをやりたい」という方針を受け、思考と判断が要る論点だけを 1 ページに集めるハブとして新設。ラベル品質仕切り直し 5 レイヤ、次の view 方向、pipeline 境界、公開・運用摩擦の 4 ブロックで構成
