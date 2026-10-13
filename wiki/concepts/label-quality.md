---
title: "ラベル品質戦略 — クラスタラベルの契約と評価レイヤ"
type: concept
summary: "広聴AI のクラスタラベル品質の durable hub。pipeline step4-6 でのラベルの位置づけ、「全体傾向を歪めず少数軸も保持する」ラベル契約、品質評価を5レイヤ(入力sampling・代表例選び・judge較正・UI表示文脈・人手pairwise)に分解する枠組み、judge を生成と同系統モデルで採点する罠を束ねる。"
sources:
  - label-quality-redesign-reset-2026-05-30.md
  - label-coverage-policy-2026-05-29.md
  - label-judge-mechanism-2026-05-25.md
  - label-refinement-input-scope-2026-05-29.md
  - label-quality-rubric-evaluation-2026-05-29.md
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - label-quality-human-preference-improvement-plan-2026-06-03.md
  - labelling-prompt-few-shot-template-confound-2026-06-03.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
---

# ラベル品質戦略 — クラスタラベルの契約と評価レイヤ

ここでいう「ラベル品質」は、GitHub の issue label ではなく、広聴AI の解析結果に出る **クラスタの label / description の品質** を指す。ラベルは一連の dated な実験と議論の正本があちこちに散っているので、このページでは **時間が経っても変わらない枠組みと結論** だけをまとめ、個別の実測値・改稿履歴は各 analysis へリンクで送る。追跡用の tracking issue は [#881](https://github.com/digitaldemocracy2030/kouchou-ai/issues/881)。

関連する核概念: 広聴AI = 構造把握スタンス ([[analysis-stance]])、パイプライン全体 ([[pipeline]])、思考の論点ハブ ([[thinking-targets]] の「ラベル品質改善の仕切り直し」節)。

## パイプラインにおけるラベルの位置づけ (step 4-6)

[[pipeline]] の 8 ステップのうち、ラベルを作るのは step 4-6 である。

4. `hierarchical_initial_labelling` — 各クラスタに初期ラベルを付ける。cluster 内の意見から `sampling_num` 件を取り出して LLM に見せる。
5. `hierarchical_merge_labelling` — 子クラスタの label / description を束ねて上位ラベルへ統合する。
6. `hierarchical_overview` — label set 全体から全体サマリを生成する。

ここで durable に効く構造的事実がいくつかある。

- **ラベルは下流の共通基盤**である。公開 UI の見出し、drill-down の入口、そして品質を測る judge 入力が、いずれもこの label / description を土台にする。したがってラベル品質の問題は「judge が弱い」だけでなく「ラベルを作る入力に実体が見えていない」ことからも起きる。
- **ラベル生成入力は random sample**。step4/5 とも `cluster_data.sample(n=sampling_num)` で seed なしランダム抽出する。件数上限は実行経路で違い、管理画面/API 経路は 30 件、analysis-core / CLI default は 10 件。大規模クラスタほど、ラベルに反映される軸が「クラスタの実体」ではなく「ランダムに当たった 10/30 件」に引っ張られる。詳細なコード位置と経路差は [[label-coverage-policy-2026-05-29]]。
- **UI の個別意見表示も「設計された代表例」ではない**。表示も judge 入力も配列先頭やランダム sample に依存しがちで、ラベル品質を測る材料とユーザが見る材料がどちらも非設計である。これを揃えるのが後述「代表例選び」レイヤの狙い。
- **refinement step は current main には無い**。label を後段で polish する `hierarchical_label_refinement` は実験ブランチ上の step であり、しかも representative arguments を入力に取らず「既存ラベル + 子クラスタラベル」だけを書き換える polish-only 設計だった。そのため上流が間違えたラベルを中身と照らして直せず、磨くほど「整った嘘」を固定化しうる。この発見がラベル品質を仕切り直す起点になった。構造の詳細は [[label-refinement-input-scope-2026-05-29]]。

ラベルは [[analysis-stance]] のいう構造把握スタンスの入口でもある。「クラスタ + ラベル + サイズの一覧で完結」させる (定量分析倒れ) のではなく、ラベルを足場にユーザが原文へ戻り構造を読めることが前提になる。

## ラベル契約 — 全体傾向を歪めず、クラスタ内の少数軸も保持する

ラベル品質の仕切り直し (2026-05-30、[[label-quality-redesign-reset-2026-05-30]]) で、2 つの異なる話が整理された。混同しやすいので分けて書く。

### ラベルは「目次」でなく「要約」

人間判断として確定しているのは、ラベルはクラスタの要約であって一覧 UI の目次見出しではない、という product 定義である ([[label-coverage-policy-2026-05-29]])。

- カバレッジ優先。短くて軸が落ちるより、多少冗長でも全軸が見えるほうが安全側 (「カテゴリ外が混ざっている」ように見せない)。
- 1 キーワードでの完全包括は不可能なので、上位 2-3 軸まで `A と B` 程度に広げる。4 軸以上は scanability を崩すので許容しない。

つまり **クラスタ内に実在する少数軸を黙って落とすと、そのクラスタについての全体傾向の見え方自体が歪む**。これが「全体傾向を歪めず少数軸も保持する」というラベル契約の中身で、greedy max-coverage の発想 (最頻トピック A → 残差の最頻 B) につながる。

### ユースケース契約は「全体傾向把握」一本

これとは別のレイヤで、Web UI / 標準 run の **唯一のユースケース契約を「全体傾向把握」一本** に固定した ([[label-quality-redesign-reset-2026-05-30]])。tokoroten の言い換えでは「デカい見落とし / デカい違和感を見つける」装置。

- 「少数だが重要な論点の発見」は、product として並列の契約に **しない**。理由は (1)「重要」が確率的で保証できない、(2)「重要」の定義は分析者の責務で prompt に書く必要がある、から。この経路は CLI / `analysis-core` のカスタム prompt に寄せる ([[usage-modes]])。
- 全体傾向把握 run の副産物として minority residual artifact を product として約束しない。
- 全体傾向把握も **構造把握スタンスで実現する** ([[analysis-stance]])。「上位 N トピックの頻度を見るだけ」ではない。

この 2 つは別物である。前者 (クラスタ内の上位軸を要約に保持する) は常に満たすべきラベル契約、後者 (少数重要論点の *発見*) は Web UI の約束から外して CLI 側へ分業した境界、という切り分けを崩さないこと。この確定により、下流の評価レイヤはすべて全体傾向把握最適化で揃う (FPS / 境界保存のような外れ値保存系の道具は標準パイプラインに入れない)。

## 品質評価を 5 レイヤに分解する

「ラベル品質を上げる」を 1 つの塊で扱うと、何が効いたのか分からなくなる。採用判断用の実験は 1 要素ずつ変える ([[one-factor-experiment-principle-2026-06-02]])。そのために品質を次の 5 レイヤに分解し、各レイヤを独立に設計・比較する。

| レイヤ | 問い | durable な方針 |
|---|---|---|
| 1. 入力 sampling | cluster 内の何をラベル生成 LLM に見せるか | まず sampling を外して全件入力を試す。ダメなら max-coverage / k-medoids |
| 2. 代表例選び | UI と judge が見る rep args をどう選ぶか | 配列先頭依存をやめ、`典型例 + 幅` を主軸にした rep args artifact を UI と judge で共有 |
| 3. judge 較正 | 品質をどう自動採点するか | 絶対批評でなく、人間 pairwise preference を再現できるかで較正 |
| 4. UI 表示文脈 | どの提示文脈でラベルを評価するか | `label_only` / `sibling_label_set` / `label_with_representatives` に分解 |
| 5. 人手 pairwise | 人間に何を聞くか | 単独批評でなく、出どころを隠した blind A/B で選好を集める |

### 1. 入力 sampling

ラベル品質の根本原因の一つは、上流の random sample で情報が落ちることである ([[label-coverage-policy-2026-05-29]])。ラベリングのコストは extraction と比べて小さいので、複雑なアルゴリズムに飛ぶ前に **まず全件を渡して試し、ダメなら減らす** のが筋。全件で品質が上がらない、または context window が厳しいクラスタが出た時に初めて max-coverage / k-medoids を比較する。

### 2. 代表例選び (rep args artifact)

「代表例」を 1 種類で考えると、typical だけを並べてクラスタ内の散らばりを過小に見せ、公開 UI でも judge でも過信を誘う。少なくとも役割を分ける ([[label-coverage-policy-2026-05-29]])。

- **典型例**: centroid 近傍 / label embedding との類似度が高い。意味を素早く掴ませる。
- **幅を見せる例**: 典型から遠いがクラスタ内の意見。散らばり・副論点を見せる。
- **境界例**: sibling との境界に近い意見。ラベル間の曖昧さを点検する。

この rep args artifact を **UI 表示と judge 入力で同じものに揃える** のが肝。人間が見る材料と judge が見る材料がずれていると較正が成立しない。

### 3. judge 較正

judge は後述「罠」の通り、絶対点を上げる道具ではなく **人間の pairwise preference を再現する道具** として育てる ([[label-quality-rubric-evaluation-2026-05-29]])。抽象的な 1-5 点ではなく binary criteria + points + fatal penalty に分解し、「材料にない軸を主張している (unsupported axis)」「見える重要軸が落ちている (missing visible axis)」のような失敗を fatal 寄りに扱う。この judge で winner を機械的に決めるのではなく、**なぜ悪いかを分解して次の実験を決める** ために使う。

### 4. UI 表示文脈 (presentation context)

ラベルは現実 UI で単独に存在するとは限らないので、「どの文脈で良いラベルか」を分けて評価する ([[human-pairwise-label-preference-experiment-2026-06-02]])。

- `label_only` — heading として自立しているか。
- `sibling_label_set` — 隣と区別できるか、label set として読めるか。
- `label_with_representatives` — 代表例に支えられ、重要軸を落としていないか。

full UI での統合確認は、cluster size・description・隣接 label・階層・interaction が同時に効いて解釈しにくいので、**最初の clean A/B には入れない**。分解テストで候補を絞った後の統合確認として扱う。

### 5. 人手 pairwise (blind A/B)

人間は単独ラベルを見てすぐ「coverage が弱い」「sibling と紛らわしい」と言語化できるとは限らない。だが同じクラスタの 2 案を並べれば「どちらが中身に近いか」は判断しやすい ([[human-pairwise-label-preference-experiment-2026-06-02]])。

- 人間には `A / B / tie / unsure` と軽い confidence、任意の理由タグだけを求める。自由記述は optional。
- algorithm / process 由来は **隠す** (`current main` / `setwise` 等の名前が見えると先入観で選ぶ)。A/B の表示順は randomize / counterbalance する。
- この preference dataset が揃ってから、judge に同じ A/B を見せ、人間の winner / tie / 理由タグを再現できるかで judge v1 を較正する。

## judge の罠と設計原則

judge を設計で使う前に、次の罠を踏まない ([[label-judge-mechanism-2026-05-25]])。

- **生成と同系統モデルで採点する self-evaluation バイアス**。生成側 (ラベル生成 / LLM grouping) と judge 側が同じ系統の LLM だと、judge は自分好みの出力に甘くなる。judge はそのまま最終審判にせず、Claude / 人間 judge で較正してから使う。実際、rubric v0 は過去出力の 4 候補を再評価してもほぼ満点になり、人間 / Claude judge が見つけたズレを検出できなかった ([[label-quality-rubric-evaluation-2026-05-29]])。
- **cluster 単位 judge と label-set 全体 judge は見ているものが違う**。前者は個別クラスタの代表性、後者は一覧の読みやすさ・粒度の揃いを好むので、winner が割れても不思議ではない。「どちらを最適化したいのか」を先に決める。
- **judge は弱い評価器**。representative は少数しか見ず、実 UI 文脈でなく text dump で判断し、prompt が「良いラベル」をかなり誘導する。数点差で algorithm を複雑化しない。

評価の実務でもう一つ durable な教訓がある ([[labelling-prompt-few-shot-template-confound-2026-06-03]])。

- **A/B する前に、両 candidate の実際の output を spot-check する**。candidate 名 (none / setwise / short) から style を推測すると、どちらが verbose かを取り違える事故が起きる。artifact を直接確認すること。
- **few-shot example はラベル品質の天井になる**。merge labelling の few-shot が `〜による〜の〜` 構文を焼き付けていると、process / sibling-awareness を変える前に、まず prompt example を見直すほうが見返りが大きい。

## 実務順序 (durable な進め方)

これらを組む順序は固定されている ([[clustering-labeling-comparison-corpus-2026-06-02]], [[label-quality-human-preference-improvement-plan-2026-06-03]])。

1. **比較コーパスを作る** — dataset / tree / labelling / label output / 人間メモを分けて蓄積する。何を入力 tree にし、どの labelling process が出したラベルかを追えないと judge を較正しようがない。
2. **同じ tree / evidence で label variants を作る** — この段階では winner を決めない。比較できる候補を作るのが目的。
3. **blind A/B で human preference を集める** — 由来を隠し、presentation context を固定して。
4. **judge を preference に合わせて較正する** — 合格するまで judge で label prompt の winner を決めない。
5. **clean experiment へ進む** — evidence policy / labelling process / tree generation を 1 要素ずつ比較する。tree を変えると label も従属的に変わるので、tree を比較する時は labelling / evidence / judge を固定する。

raw artifact と preference records は権限管理できる場所 (`raw/experiments/<experiment_id>/` など) に置き、公開 wiki には manifest / summary / 判断だけを残す ([[experiment-result-storage-policy-2026-06-02]])。

## このハブが束ねる dated analysis

- [[label-quality-redesign-reset-2026-05-30]] — 仕切り直しの起点。ユースケース契約の確定と 5 レイヤの提示。
- [[label-coverage-policy-2026-05-29]] — 「ラベルは目次でなく要約」の人間判断と、上流 sampling 制約の発見。
- [[label-refinement-input-scope-2026-05-29]] — refinement が rep args を見ない polish-only 設計であることの構造分析。
- [[label-judge-mechanism-2026-05-25]] — 2 種類の judge と、同系統モデル採点の罠。
- [[label-quality-rubric-evaluation-2026-05-29]] — binary criteria + fatal penalty への分解と rubric v0 の限界。
- [[human-pairwise-label-preference-experiment-2026-06-02]] — blind A/B と presentation context 3 分解。
- [[label-quality-human-preference-improvement-plan-2026-06-03]] — preference collection → judge calibration の実務計画。
- [[labelling-prompt-few-shot-template-confound-2026-06-03]] — few-shot 交絡と direction 取り違えの再調査 (A/B 前の spot-check 教訓)。
- [[clustering-labeling-comparison-corpus-2026-06-02]] — 評価の前段としての比較コーパス / 実験台帳の構想。

## Open Questions

- 全件入力はどのクラスタ規模まで現実的か (token / cost の試算)。
- rep args artifact は aggregation step に入れるか独立 step にするか。
- 全体傾向把握用 rubric の具体形 (何を criteria にし、何を fatal にするか)。
- 何件の pairwise preference があれば judge v1 の較正と呼べるか。複数 evaluator の disagreement を label ambiguity と扱うか rubric 不足と扱うか。
- merge labelling の few-shot を topic-neutral にした時、refinement なしの出力だけ改善するのか、後段も追従するのか。
