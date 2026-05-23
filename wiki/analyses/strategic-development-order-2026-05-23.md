---
type: analysis
summary: "Issue 消化順ではなく、CLI / workflow / plugin / Web 配布を 3 層のプラットフォームとして見ると、先に固めるべきなのは `analysis-core` の共通基盤と plugin 実験の本番導線である"
sources:
  - usage-modes.md
  - plugin-system.md
  - refactoring-status.md
  - open-decisions.md
  - report-html-non-web-canonical-decision-2026-05-23.md
  - book-release-development-plan-2026-09.md
  - broad-listening-book-extractions.md
  - development-priority-roadmap-2026-05-23.md
  - github-dev-docs.md
  - source-code.md
---

[[development-priority-roadmap-2026-05-23]] は current open issues をもとに「いま詰まっているもの」を優先順に並べた短中期 roadmap である。  
それ自体は必要だが、**それだけでは shallow** で、`kouchou-ai` の長期的な価値である CLI / plugin / 実験可能性を説明しきれない。  
長期視点では、issue を 1 件ずつ閉じることよりも、**どの順番で platform を固めると、新しい分析方式を安全に試し、比較し、製品へ戻せるか** が本題である。[[plugin-system]]より [[book-release-development-plan-2026-09]]より

## 中心仮説

`kouchou-ai` は 1 つのアプリではなく、少なくとも次の 3 層から成る。

1. **共通実験基盤**  
   `packages/analysis-core`、workflow engine、artifact / status / config 契約、PyPI、test
2. **製品導線**  
   非専門家向け Web UI、公開 / static export、Windows / Docker 配布、admin 運用
3. **探索枝**  
   plugin / `analysis_mode` による新しい分析方式、可視化、provider、long-context 系統

長期的な発見を増やしたいなら、優先順は **3 を先に思いつくこと** ではなく、**1 を先に固めて 3 を比較可能にし、その後で 2 に製品化する** になる。  
ここを逆にして、現行 Web UI や Windows 配布だけを先に厚くすると、あとから新しい分析枝を入れるたびに glue code が増えて設計が崩れる。[[usage-modes]]より [[refactoring-status]]より

## Core Problem

現状のボトルネックは、「分析モードがまだ 2 種類程度しかない」こと自体ではない。  
より本質的な問題は、**第 1 の分析モードが事実上「散布図を自然に出せるモード」として product の中心に座っており、想定される第 2 の分析モードはその前提を満たせない可能性が高い** ことである。[[pipeline]]より [[plugin-system]]より

ここでいう **第 2 の分析モード** は、単なる「別のクラスタリング手法」ではなく、ユーザが 2026-05-23 時点で明示したように **Jigsaw Sensemaker 的な分析モード** を念頭に置く。  
すなわち、embedding 空間上の距離と 2D 散布図を前提にするのではなく、LLM がトピック、立場、分類ツリー、対立軸を直接構成する **long-context / taxonomy-guided / tree-native** な系統である。[[slack-design-intents-2026-q1]]より [[broad-listening-book-extractions]]より

このねじれは、現在の実装と計画の両方に見えている。

- current `public-viewer` の chart default は scatter 系が中心である
- admin の visualization config も `scatterAll` を既定に置いている
- `PR #827` の短期計画は、`analysis_mode=llm_grouping` でも一旦 `x/y` と `cluster-level-*` を従来互換で出して viewer 互換を維持する、としている
- しかし Jigsaw Sensemaker / long-context 系の分析は、自然な散布図を出せない可能性が高い

つまり第 2 モードは、「本当にその分析に自然な出力」を返す前に、**scatter-compatible な形へ無理に射影しないと product に乗れない** という圧力を受けている。  
これでは plugin architecture が「分析の自由度を増やす仕組み」ではなく、**既存散布図 UI に合うものだけを第二級市民として追加する仕組み** に劣化する。

したがって長期戦略で最初に解くべき論点は、「分析モードを増やすこと」ではなく、**散布図を前提にしない analysis mode でも product が成立する契約へ移れるか** である。

### Why Jigsaw Makes The Problem Sharper

Jigsaw Sensemaker 的な第 2 モードを想定すると、この問題はさらに明確になる。

- Jigsaw 系は「距離空間の地図」を出したいのではなく、「どんな立場があり、何が対立軸で、どの分類木に属するか」を出したい
- そのため自然な主成果物は `x/y` ではなく、**tree / taxonomy / stance grouping / evidence links** である
- もしこれを scatter 前提の product に載せるためだけに 2D 座標を捏造すると、Jigsaw 系の本来の価値である「賛否や論点の区別」がむしろ読みにくくなる

つまり Jigsaw 系を本気で第 2 モードにするなら、必要なのは「Jigsaw でも散布図を描けるようにすること」より、**散布図を持たない mode が first-class citizen になれる viewer / capability contract** である。

### Working Formulation

2026-05-23 時点の作業仮説を一文でまとめると、次の通りである。

> embedding を前提としない分析様式（例: Jigsaw Sensemaker）を可能にしたい。しかし embedding を前提としている散布図は見た目のインパクトが強く、ユーザが欲しがるので簡単には捨てられない。そこで、互換のために一時的に「embedding を前提としない分析様式」でも embedding を併用して散布図互換にする案と、長期的に「散布図が必須なビュー」をやめる案の二段構えで進むのがよい。

この定式化の重要な点は、短期案と長期案を混同しないことにある。

- **短期案**: Jigsaw 系 mode でも一旦 `x/y` を持たせ、既存 viewer / scatter UX を壊さず比較実験を始める
- **長期案**: scatter を必須 capability から外し、tree / taxonomy / stance grouping を主成果物にできる mode を first-class citizen として扱う

短期案は migration strategy としては合理的だが、長期の到達点にしてはいけない。長期の本丸は、**「新 mode でも散布図を出せるか」ではなく、「散布図を出さない mode でも product が成立するか」** である。

## Why This Matters

この問題を放置すると、次の 3 つが起きる。

1. **第 2 モードが偽の scatter を出す**
   本来は tree / taxonomy / stance map で表現すべき分析を、viewer 互換のためだけに `x/y` へ押し込む。結果として、分析の意味と可視化の意味がずれる。

2. **比較実験がゆがむ**
   「新しい分析方式が悪い」のか、「既存散布図 UI に合わせるための変換が悪い」のかが分からなくなる。

3. **product 側が mode 増加に耐えない**
   新 mode を 1 つ増やすたびに、scatter 前提の fallback、dummy capability、例外 UI が増えて、設計が複雑化する。

したがって、ここで問うべきなのは「Jigsaw 系分析をどう実装するか」より前に、**散布図は『分析の本体』なのか、『特定 capability を持つ mode だけが使える view』なのか** である。

## なぜ短期 bugfix 順では足りないか

`#731` や `#584` のような issue は確かに重要だが、それらは **「どの platform を伸ばしたいのか」** が定まって初めて位置づく。

- `#731` は distribution lane の問題
- `#584` は current Web product の整合性問題
- `#838` は CLI / 共通実験基盤の信頼性問題
- `#496` は Docker 依存をどう扱うかという入口戦略の問題
- `#809` は実験枝の速度最適化の問題

この 5 つは同じ backlog に見えて、実は別レイヤの問題である。  
長期戦略では、**レイヤを混ぜずに順番を決める** 方が重要である。[[usage-modes]]より

## 先にやるべき順番

### 1. `analysis-core` を「共通実験 OS」として固める

最優先は bugfix の総数ではなく、`analysis-core` を **実験と製品の共通母体** として信頼できる状態にすること。  
current `main` では workflow default 化 (`PR #840` 相当) と CLI preflight (`PR #844`) まで既に入っている。つまり基盤は「これから作る」段階ではなく、**仕上げて official にする** 段階へ移っている。[[refactoring-status]]より

ここで先に固めるべきものは次の 4 点。

- Phase 8: 旧 `apps/api/broadlistening/pipeline/` をどう消すか
- artifact 契約: `hierarchical_result.json`, `hierarchical_status.json`, `report.html` をどこまで canonical にするか
- validation 契約: `#838` を runtime fail-fast にするのか、test helper にするのか
- test / release 契約: `#558`, `#546`, PyPI release gate, regression harness

これは見た目には地味だが、ここが固まらないと **新しい分析方式を追加しても、比較のたびに status, rerun, output, release が壊れる**。  
言い換えると、`analysis-core` は単なる CLI ではなく **analysis experiment OS** として扱うべきである。

工数目安:

- 設計判断の整理: **1 週間**
- 実装と test hardening: **2 〜 4 週間**
- 合計: **8 〜 15 人日**

### 2. plugin 計画を「計画」から「1 本の本物の枝」へ進める

次にやるべきなのは、plugin system を docs 上の理念から **本当に価値を生む実験枝** へ進めること。  
現状の問題は plugin framework が無いことではなく、**framework はあるのに、stress test になる外部 / 非既定の analysis branch がまだ少ない** ことである。[[plugin-system]]より

最初の候補として妥当なのは、既に `PR #827` で計画が出ている **LLM grouping / capability auto-detection 系** である。  
これは単なる新機能ではなく、次の論点を一度に検証できる。

- `analysis_mode` を本当に切り替え可能か
- capability metadata から visualization gating ができるか
- 散布図を出せない分析方式を product がどう扱うか
- taxonomy-guided 分類や Jigsaw / long-context 系統を同じ枠に載せられるか

つまりここは「新アルゴリズム 1 件」ではなく、**plugin architecture が現実に耐えるかを調べるための本命テスト** である。[[open-decisions]]より [[broad-listening-book-extractions]]より

ここでやるべきなのは:

- builtin wrapper とは別に、1 本の非既定 analysis branch を end-to-end で通す
- `plugins/analysis/` か同等の外部 plugin 実例を 1 つ置く
- frontend chart plugin registry との capability 契約をつなぐ
- 「散布図なしでも成立する analysis mode」の product 振る舞いを決める

工数目安:

- 最小実装: **2 〜 3 週間**
- 比較評価と UI 追従込み: **3 〜 6 週間**
- 合計: **10 〜 20 人日**

### 3. Web UI と CLI を「同じ製品の 2 入口」ではなく、役割分担した 2 面として固定する

その次にやるべきなのは、Web UI と CLI の関係を曖昧にしないこと。  
`usage-modes` が示す通り、CLI は研究者 / agent 向け、Web UI は非専門家向けで、同じコアを使っても保持したい artifact と UX は違う。[[usage-modes]]より

長期的に重要なのは、ここで **無理に 1 本化しない** ことである。

- CLI: 再現実験、比較、CLI 向け観察用HTMLの `report.html`、中間成果物
- Web UI: admin 操作、公開・共有、`public-viewer`、運用 UX
- distribution: Windows、Zip、Docker / WSL2、static hosting

この 3 面を混ぜると、`report.html` は Web canonical にしないという artifact 契約と、Windows を research path まで正式サポートするのか、という別論点が全部混ざる。[[report-html-non-web-canonical-decision-2026-05-23]]より  
したがって順番としては、**先に基盤と plugin を固め、その後で distribution / Web product を各面ごとに最適化** するのがよい。[[refactoring-status]]より [[windows-distribution-options]]より

ここでの論点は:

- `#496` Docker なし経路を product 本線にするか補助線にするか
- `#518` static export 検証を Web 配信品質の gate にするか
- `#731` `#666` を distribution lane の改善として扱うか、platform 変更の根拠にするか
- `report.html` を CLI 向け観察用HTMLとして固定したうえで、Web artifact 契約を JSON + `public-viewer` 前提で詰める

工数目安:

- 入口戦略の整理: **0.5 〜 1 週間**
- Windows / static / docs 実装: **2 〜 4 週間**
- 合計: **8 〜 15 人日**

### 4. その上で初めて「発見のための研究 backlog」を回す

本当に長期的な発見を増やすのはこの段階である。  
ここで初めて `#809` UMAP 並列化、`#577` 自動クラスタ数評価、`#513` seed、`#679` 任意カテゴリ分類、さらに書籍が示した **off-topic filter**, **sentiment dimension**, **DivCon**, **taxonomy-guided 分類**, **long-context mode** などを同じ実験土台で比較できる。[[broad-listening-book-extractions]]より

重要なのは、これらを feature backlog としてではなく **experiment portfolio** として扱うこと。

- 何を比較したいのか
- どの dataset で評価するのか
- 現行 scatter pipeline に対して何が改善 / 悪化するのか
- どの結果なら plugin として残し、どの結果なら docs-only に戻すのか

この比較条件が無いまま issue を切ると、単発のアルゴリズム改修が積み上がるだけで、長期的な設計知見にならない。  
逆に言えば、長期的な発見とは **新手法を思いつくこと** ではなく、**同じ土台の上で比較し、捨てる理由まで記録すること** である。

工数目安:

- 1 本の experiment spike: **1 〜 2 週間**
- 3 本程度の比較ラウンド: **1 〜 2 か月**
- 合計: **10 〜 30 人日**（並行可能）

### 5. 最後に説明責務と trust layer を強くする

`#696`, `#542`, `#564` は末尾に見えるが、実際には marketing ではなく **plugin / experiment platform の trust layer** である。  
analysis mode が増えるほど、「このレポートは何を保証し、何を保証しないか」を明記しないと利用者の誤読が増える。[[book-release-development-plan-2026-09]]より

したがってこれは最後に回すというより、**各 experiment を product に昇格させるたびに並走で追加する層** と理解した方がよい。

## 逆に、いま後ろでよいもの

長期戦略の観点では、次は後ろでよい。

- `#648` 一括編集のような大きめ運用 feature
- `#586` UI shared package のような整理型リファクタ
- `#690` など周辺保守
- plugin 実験がまだ本物になっていない段階での大型 visualization polish

理由は、これらは platform が決まってからでも遅くない一方、**共通実験基盤と plugin 実証が遅れると、将来の発見の速度そのものが落ちる** からである。

## 実務へ落とした順番

長期戦略を実務へ落とすなら、順番はこうなる。

1. `analysis-core` の canonical contract を固定する  
   Phase 8, validation, artifact, release/test
2. LLM grouping / capability path を 1 本実装する  
   `PR #827` の計画を doc-only で終わらせない
3. Web / CLI / distribution を役割分担として確定する  
   `#496`, `#518`, `#731`, `report.html` の位置づけ
4. 研究 backlog を experiment portfolio として回す  
   `#809`, `#577`, `#513`, taxonomy-guided, long-context, off-topic filter
5. 説明責務を製品と docs に重ねる  
   `#696`, `#542`, `#564`

短期 issue はこの順番の中で意味づけるべきで、これと無関係に backlog を上から消すと shallow になる。

## Calendar 見積もり

1 人主担当で順にやるなら:

- **2026-05 下旬 〜 2026-06 前半**: 共通実験基盤の固定
- **2026-06**: plugin 実証 1 本目
- **2026-06 後半 〜 2026-07**: distribution / Web / CLI の役割固定
- **2026-07 〜 2026-08**: experiment portfolio を回す
- **並行して**: trust layer (`#696`, `#542`, `#564`)

2 〜 3 人で並行できるなら:

- 人 1: `analysis-core` / validation / release / plugin branch
- 人 2: Web UI / distribution / Windows / static export
- 人 3: experiment evaluation / docs / explanation layer

この分け方なら、短期の user-facing bugfix を完全には捨てずに、長期の discovery lane も止めずに済む。

## Immediate Next Step

長期戦略の観点で **次にやるべきことを 1 つに絞る** なら、`analysis-core` を「共通実験基盤」として固定する **短い設計スプリント** を先にやるのがよい。  
ここで言う「設計」は抽象議論ではなく、次の実装判断を止めないための **contract 固定** である。

先に決めるべき項目は 4 つ。

1. **canonical entrypoint**
   `python -m analysis_core` / `PipelineOrchestrator.run_workflow()` を正規経路として明文化し、旧 `apps/api/broadlistening/pipeline/` は Phase 8 の削除対象として扱う。

2. **artifact contract**
   `hierarchical_result.json`, `hierarchical_status.json`, `report.html` のうち、何が必須で、何が利用モード別の補助出力かを固定する。特に `report.html` は CLI 向け観察用HTML、Web canonical path は `hierarchical_result.json` + `public-viewer` と明記する。[[report-html-non-web-canonical-decision-2026-05-23]]より

3. **validation contract**
   `#838` を、end-user CLI の fail-fast 機能にするのか、maintainer 向け diagnostic / test helper にするのか決める。ここを曖昧にしたまま plugin 実験を始めると、artifact の壊れ方と実験失敗が混ざる。

4. **capability contract**
   analysis mode が「散布図を出せるか」「階層結果を返すか」「どの visualization plugin が使えるか」を、capability metadata としてどこまで持つかを決める。これは LLM grouping 実装前の必須前提。

この設計スプリントの成果物は、大きな仕様書ではなく次の 3 点で十分である。

- wiki / docs 上の短い canonical contract 文書 1 本
- stale umbrella (`#721`) を current path に沿って読み替えた follow-up issue 群
- 最初の実証枝として `LLM grouping / capability path` を実装するための具体 issue 1 本

つまり、次にやるべきことは「Windows bug を直す」でも「新 plugin を書き始める」でもなく、**その後のすべての実験を比較可能にする contract を先に固定すること** である。  
これが終わったら、その次の一手は `PR #827` の計画を土台にした **最初の本物の非既定 analysis branch** の実装になる。

## What To Think About

実装前に本当に考えるべきことは、「次の issue は何か」ではなく **どの問いに答えれば順番が決まるか** である。  
長期戦略の観点では、少なくとも次の 8 問を順に考えるとよい。

### 1. 何を増やしたいのか

まず決めるべきなのは、`kouchou-ai` の次のフェーズで増やしたいものが何かである。

- 新規利用者数なのか
- 非専門家が最後まで完走できる確率なのか
- 研究的な発見速度なのか
- 実験した分析方式の本数なのか
- 本番投入できる analysis mode の種類なのか

ここが曖昧だと、Windows 対応も plugin 実装も static export 改善も全部「大事」に見えて順番が決まらない。  
今の文脈では、短期は「完走率」、中長期は「発見速度と product への還元速度」を増やす、と二層で置くのが自然である。

### 2. 何を固定し、何を実験可能に残すのか

plugin 戦略を取るなら、全体を可変にするのではなく、**固定面と可変面の境界** を先に決める必要がある。

- 固定するもの: status file、artifact path、config schema、rerun semantics
- 実験可能にするもの: extraction 以後の analysis mode、provider、visualization capability

ここが曖昧だと、新しい plugin を 1 本足すたびに platform 全体が揺れる。  
逆にここが決まれば、「壊れた」のか「実験結果が悪かった」のかを分けて読める。

### 3. どの利用モードを正規入口として守るのか

`usage-modes` で整理した 2 入口を、実際にどこまで守るのかを考える必要がある。

- CLI は研究者 / agent 向けの正規入口としてどこまで保証するか
- Web UI は非専門家向けの正規入口としてどこまで完走性を保証するか
- Windows は Web UI 側の配布問題として扱うのか、CLI 研究用途まで支えるのか
- Docker なし経路は主戦場なのか補助線なのか

これは機能要件というより **support policy** である。  
support policy が曖昧なまま issue を積むと、入口ごとに別の理想が混ざって backlog が膨らむ。

### 4. 新しい分析方式を何で評価するのか

LLM grouping、taxonomy-guided 分類、sentiment-dim、DivCon、off-topic filter のような探索枝は、**何をもって成功とするか** を先に決める必要がある。

- 既存 scatter pipeline より何が良くなれば採用なのか
- 速度、可読性、賛否分離、現場編集負荷のどれを重視するのか
- どの dataset で比較するのか
- 「面白いが採用しない」結果も記録するのか

ここがないと experiment backlog は知見にならず、単発の feature request に戻る。

### 5. 可視化と分析の結びつきをどう扱うのか

長期で重要なのは、散布図を前提にしない analysis mode が増えた時に product がどう振る舞うかである。

- 散布図を出せない analysis mode を許容するか
- capability metadata で可視化を gating するか
- hierarchy-list だけで見せる mode を正式に持つか
- 可視化 plugin の契約は backend / frontend のどちらで持つか

これは `PR #827` 系の本丸であり、plugin system が本物かどうかを決める論点でもある。

### 6. 実験から製品へどう昇格させるのか

発見を増やすだけでなく、良い発見を main に戻すルールも必要である。

- experiment branch の完了条件は何か
- builtin plugin に昇格する条件は何か
- docs only で止める条件は何か
- experimental flag をどこで剥がすか

ここを決めないと、「実験は増えたが product は複雑化しただけ」になりやすい。

### 7. 説明責務をどこに持たせるのか

analysis mode が増えるほど、利用者に何を説明するかが重要になる。

- このレポートは何を保証し、何を保証しないか
- AI のまとめと元発言の関係をどう見せるか
- 散布図やクラスタ名をどこまで真に受けてよいか
- 違う analysis mode を比較した時に、何を同じものとして読んでよいか

`#696` や `#542` は後回しの docs issue ではなく、platform の信頼境界を作る論点として考える方が正確である。

### 8. 何を今は捨てるのか

最後に必要なのは、やることの列挙ではなく **やらないことの明示** である。

- いまは Web 用 feature を増やさないのか
- いまは Docker-less distribution を本線にしないのか
- いまは visualization polish より capability contract を優先するのか
- いまは 3 本目の experiment より 1 本目の比較可能性を優先するのか

長期戦略は、「全部やる」ではなく「今は何を捨てるか」を決めて初めて実行可能になる。

## Practical Checklist

したがって、次の会議や設計スプリントでは、少なくとも次の問いに yes/no または短文で答えられる状態を目標にするとよい。

- 今期の主目的は、完走率向上か、発見速度向上か、両方か
- `analysis-core` の正規 entrypoint は何か
- 必須 artifact は何か
- mode-specific artifact は何か
- capability metadata はどこまで持つか
- 最初に実装する非既定 analysis branch は何か
- その branch の評価 dataset と比較軸は何か
- 実験を product に昇格させる条件は何か
- 逆に、今期は何をやらないか

## Open Questions

- `analysis_mode` を product 上でどこまで見せるのか、設定ファイルだけで持つのか
- visualization plugin の backend / frontend 契約をどこで一本化するのか
- `#496` を Docker 回避の docs 拡張として済ませるのか、配布戦略の再定義として扱うのか

## Updates

- 2026-05-23: 初版作成。issue-centric な短中期 roadmap とは別に、CLI / workflow / plugin / Web 配布を 3 層 platform として見た長期順序を追加
- 2026-05-23: 「次にやるべきこと」を、`analysis-core` の contract 固定スプリントとして具体化し、entrypoint / artifact / validation / capability の 4 契約を先に決めるべきだと追記
- 2026-05-23: maintainer 判断 [[report-html-non-web-canonical-decision-2026-05-23]] を反映し、`report.html` Web canonical 化の問いを確定事項へ寄せた
