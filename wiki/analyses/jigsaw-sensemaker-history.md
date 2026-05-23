---
type: analysis
summary: "Jigsaw Sensemaker 的な第2分析モードと散布図の緊張関係は、2025 4Q の『現行散布図方式の限界認識』から始まり、2026 Q1 に『可視化を分析から切り離す必要条件』として明文化されていた"
sources:
  - meeting-minutes.md
  - slack-dev-kouchouai-2025-q4.md
  - slack-dev-kouchouai-2026-q1.md
  - slack-kouchouai-algorithm-dev.md
  - broad-listening-book-extractions.md
  - pipeline.md
  - plugin-system.md
---

Jigsaw Sensemaker 的な第2分析モードと、現行の散布図中心プロダクトの緊張関係は、2026-05 に突然見えた論点ではない。  
Slack と議事録を振り返ると、少なくとも **2025 4Q には「現行散布図方式は役に立つが深掘りには限界がある」** という認識が共有され、**2026 Q1 には「Jigsaw 系分析を入れるなら可視化を分析から切り離す必要がある」** という設計意図まで進んでいた。[[slack-design-intents-2025-q4]]より [[slack-design-intents-2026-q1]]より

## 結論

振り返ると、議論は次の 4 段で進んでいる。

1. **散布図方式の価値は認めるが、限界も強く意識されていた**
2. **Jigsaw / Sensemaker は別分析モードとして早くから視野に入っていた**
3. **ただし第2モードをいきなり本流にせず、既存構造に寄せた互換枝として試す方針になった**
4. **その過程で「散布図を自然に出せない mode を扱うには、可視化を分析から疎結合にする必要がある」と明文化された**

つまり現在の論点は「新しい問題」ではなく、**過去に見えていた設計課題が、plugin / analysis_mode / capability の話として表面化した段階** と理解するのが正確である。

## 1. 2025 4Q: 現行散布図方式は有用だが、深いインサイト探索には限界

2025 4Q の Slack では、広聴AIの現行方式について

- 全体像把握には役立つ
- 抜け漏れ発見には効く
- 市民参加の入口としてキャッチー

と評価されていた。  
一方で、政治家や実務家が深いインサイトや対立の調停に使うにはしんどい、という認識もかなり明確だった。[[slack-design-intents-2025-q4]]より

同時期には、埋め込み散布図方式の限界として

- 文脈埋め込みはトピック寄りで、同一トピック内の賛否が近くに置かれやすい
- 次元圧縮してからクラスタリングすると少数意見が潰れやすい
- 「切り口を先に発見してから再分類する」方が筋がよい

という不満が出ていた。[[slack-design-intents-2025-q4]]より

この段階では、Jigsaw / Sensemaker はまだ plugin 設計の文脈ではなく、**現行散布図方式の外にある高級オプション** として意識されていた。[[slack-design-intents-2025-q4]]より

## 2. 2025-10 の議事録: 散布図を捨てたい気持ちと、捨てにくさが同時にある

議事メモ `2025-10-22` では、議論がより露骨である。

- TTTC は Scatter から Turbo / `tttc-light-js` に移り、Turbo 以降は散布図を捨てている
- Google Jigsaw Sensemaker も embedding を介さず、LLM でトピック特定と分類を行う
- `nishio` は「散布図で表示するための embedding が、より良い分析をする上での障害になっている」と感じている
- しかし一方で、想定ユーザは散布図を欲しがる可能性があり、目立つ機能を切り捨てる判断は簡単ではない

と整理されている。[[meeting-minutes]]より

同じ時期の議事録には、

- 「散布図を見て満足する時代ではない」
- 「ただし散布図は見た目のインパクトが強く、それを求める顧客がいる」

という両義的な記述もある。[[meeting-minutes]]より

この時点で既に、問題は「散布図が良いか悪いか」ではなく、**分析最適化と product / marketing 上の強さが衝突している** ことだった。

## 3. アルゴリズム開発 Slack: 散布図中心だと分析の自由度が奪われる

`#2_開発_広聴ai_アルゴリズム開発` では、より技術的に

- UMAP 後にクラスタリングするのは精度が悪い
- 賛否や対立軸は embedding 空間では埋もれやすい
- 分析と可視化を同じものとして扱うべきではない

という議論が蓄積している。[[slack-algorithm-themes]]より

特に重要なのは、「可視化を分析から分けるべきだ」という認識が、抽象的な拡張性ではなく、

**散布図を中心に据えたままだと分析の自由度が奪われる**

という不満から出ている点である。[[slack-algorithm-themes]]より

2025-10 以降は Jigsaw SenseMaker や対立軸発見、taxonomy 当てはめ、LLM 直接分類が有力視され、**第2モードは scatter の改良版ではなく、別の分析様式** として見られていた。[[slack-kouchouai-algorithm-dev]]より

## 4. 2026 Q1: Jigsaw 系を「まず既存構造に寄せて入れる」方針

2026 Q1 の `#2_開発_広聴ai` では、Jigsaw 系分類をどう導入するかがかなり具体化する。

2026-02-11 週の Slack では、

- Jigsaw 的 LLM 分類を `extraction, embedding` の後ろに差し込む
- まずは既存のパイプラインや可視化と両立する形で試す

という互換性優先案が語られている。[[slack-design-intents-2026-q1]]より

2026-02-25 週にはさらに、

- 現状
- クラスタリング部分を LLM ベースに変える枝
- 既存カテゴリーツリーをパラメータで与える亜種

という 3 段整理が明示される。[[slack-design-intents-2026-q1]]より

ここで重要なのは、`embedding` 後に分岐するのは **理論的必然ではなく、実装の楽さと後での可視化のため** だと説明されていることだ。  
つまり当時から、互換枝はあくまで移行上の便法であり、本質的には **距離空間から tree / taxonomy へ分類基準を移す** 試みだと理解されていた。[[slack-design-intents-2026-q1]]より

## 5. 2026 Q1: 「可視化を分析から切り離す」は必要条件として明文化

この論点が最もはっきり出るのは 2026-01-28 週の Slack である。

- Jigsaw Sensemaker 的アプローチは分析の選択肢として十分あり得る
- しかし自然な散布図は出せない
- したがって、管理者が可視化方式を選択可能にし、散布図を作れない分析も同じプラットフォームで扱えるようにする必要がある

と書かれている。[[slack-design-intents-2026-q1]]より

この記述から分かるのは、可視化分離は nice-to-have ではなく、**Jigsaw 系分析を platform に受け入れるための必要条件** だったということだ。[[plugin-system]]より

## 6. 2026-05 の docs / plan に残った形

2026-05 の `PR #827` 計画では、

- 短期: `analysis_mode=llm_grouping` を追加し、`x/y` と `cluster-level-*` を従来互換で出して viewer 互換を維持
- 長期: `analysis_capabilities` を自動導出し、可視化 mode の可否を `requirements` で判定

という形で整理されている。[[pipeline]]より

これは 2026 Q1 の設計意図をかなり忠実に写している。  
ただし、短期案はあくまで **scatter-compatible な形への暫定射影** であり、長期の本丸は mode 数を増やすことではなく、

**散布図を自然に出さない analysis mode でも first-class citizen として扱える capability contract を作ること**

だと読むべきである。[[strategic-development-order-2026-05-23]]より

## Distilled Take

この履歴を 2026-05-23 時点の言葉で要約すると、議論は次の二段構えへ収束している。

- **短期**: embedding を前提としない分析様式（Jigsaw Sensemaker 系）でも、互換のために一時的に embedding を併用し、散布図互換で product に載せる
- **長期**: 散布図を必須ビューとみなす前提をやめ、scatter を自然に出さない analysis mode でも first-class citizen として扱う

これは「散布図を残すか捨てるか」の二択ではなく、**ユーザが欲しがる散布図の強さを利用しつつ、その前提に分析の将来を縛られないようにする移行戦略** と理解するのがよい。

## Practical Read

この論点を今後読む時は、次の順で理解するとよい。

1. 2025 4Q: 現行散布図方式の限界認識
2. 2025-10 議事録: 散布図を捨てたいが捨てにくい、という product 上の葛藤
3. アルゴリズム開発 Slack: 分析と可視化の分離要求
4. 2026 Q1: Jigsaw 系を互換枝として試しつつ、可視化疎結合を必要条件とする設計意図
5. 2026-05 docs: `analysis_mode` / `analysis_capabilities` / `requirements` という言葉への結晶化

## Open Questions

- Jigsaw Sensemaker 的な第2モードの default view は `hierarchyList` / `treemap` / 専用 view のどれが妥当か
- `PR #827` の短期互換案である `x/y` 射影を、本当に product 実装へ入れるのか、それとも docs 上の移行案に留めるのか
- taxonomy-guided な実務モードと、新規論点発見モードを同じ UI に載せるべきか分けるべきか

## Updates

- 2026-05-23: 初版作成。Jigsaw Sensemaker 的な第2分析モードと散布図の緊張関係を、meeting minutes / Slack / current docs の流れとして時系列に整理
