---
name: broad-listening-book-source
summary: "DD2030 書籍「選挙を変えたブロードリスニング」原稿（CC BY-NC 4.0）を開発向け一次資料として要約。設計判断の出版時点の確定版・現場運用知見・将来開発の素材を含む"
type: source
sources:
  - work/broad-listening-book (digitaldemocracy2030/broad-listening-book)
---

## 出典

- リポジトリ: `digitaldemocracy2030/broad-listening-book`
- ローカル clone: `work/broad-listening-book/`
- 参照 commit: `9c22db6` (2026-06-30 18:13 JST に `work/broad-listening-book/` main を確認。初回章マップは `5826726`)
- ライセンス: CC BY-NC 4.0（タグ `license-cc-by-4.0-final` まで CC BY 4.0）
- 主担当: [[tokoroten]]、出版社はインプレス、英語版／Web は Luke Closs

## 本 wiki 上での位置づけ

書籍そのものは本 wiki のスコープ外（[[broad-listening-book|entity page]] 参照）だったが、2026-05-21 に clone を取得して 12〜13 章および 10 章 DD2030 節、現場取材の column / case 章が **開発者にとっての一次資料として価値が高い** ことを確認したため、本 source として扱う方針へ更新した。理由：

- Slack や議事メモで断片的に語られていた設計判断が、出版可能な形で整理されている
- 自治体・メディア・選挙の現場で観測された運用上の問題（label 抽象すぎ問題、外れ値クラスタ吸収、キーワード設計の難しさ）が記録されている
- 賛否分離プロトタイプ（センチメント次元拡張・DivCon）など「次に手を入れたい場所」が明文化されている

開発者向けの抽出は [[broad-listening-book-extractions]] にまとめている。

## 章マップ（開発向け価値で序列化）

### Priority 1: 設計判断・実装の一次資料

- `13_広聴AIの技術スタック解説.md` — パイプライン 8 ステップ詳解、プロンプト全文、設計トレードオフ、ミニ広聴AI実装 (100 行 Python)、コスト試算、Scatter vs Long Context 二アーキ比較、賛否分離プロトタイプ (sentiment-dim / DivCon)
- `12_ブロードリスニング要素技術解説.md` — Word2Vec→BERT→Sentence-BERT、エンベディングの賛否分離限界 (12.3.5)、Few-shot/Structured Output/Reasoning Model、UMAP の解釈（軸に意味なし・遠距離に意味なし）
- `10_00_DD2030による広聴AIの開発活動.md` — TTTC Scatter からのフォーク経緯、Spectral→K-means 変更理由、Web 化、階層クラスタリング導入、濃いクラスタ抽出、2025-05 のリソース崩壊と最小運用、Devin 利用量 (210 commits / 約 7.6%)、属性フィルタ 2203 行が Copilot Agent 実装、source-link 機能の意義、自治体導入で繰り返された 4 つの障壁

### Priority 2: 現場運用知見 (要求仕様・障害事例)

- `05_東京都、シン東京2050、ブロードリスニングによる政策転換.md` — 多チャネル収集 (Form / X / YouTube / 郵送 / 対面)、Silver Democracy 構造への対抗としての設計意図、40-50 クラスタが分析的には豊かだが読者には過多というジレンマ、運用者が LLM ラベルを手で再ラベリングする実態、off-topic 大クラスタの発生
- `04_05_朝日新聞の特設記事.md` — ラベルが抽象すぎる問題、プロンプトで「見出しを 5 つ付ける」工夫、選挙直前一発勝負への試行錯誤、SNS は綺麗にクラスタリングできずアンケートは綺麗、外れ値除外機能の要望、ローカル実行できる UI ツールの要望、座標を Flourish で再可視化している実装、検索キーワード設計が一番難しい
- `column/1万件の声を集めて気づいたこと.md` — 9,688 件集めても多くが断片的立場表明にとどまる、「スケールアップ」より「スケールアウト」、合意形成のボトルネックは **自己理解**（青山柊太朗 / 多元現実）
- `column/安全な共感.md` — 散布図 UX の固有価値、Polis が返信機能を意図的に排除した設計、SNS 分断装置からの全体像復元、「ノイジーマイノリティ」の留保
- `column/ワードクラウドは分析ではない.md` — 頻度ベース可視化の限界、なぜセマンティッククラスタリングが必要か
- `06_*` 国政選挙各党 — チームみらい・国民民主・公明党・維新・再生の道のそれぞれ異なる利用形態。要件差分が読める。公明党 We Connect は公式 source ありだが、広聴AI confirmed ではなく、党組織・Google Form・AI 分析を組み合わせた broad listening adjacent として扱う
- `08_*` 自治体 (太田市・広島) — 太田市の「自分ごと化会議」は事前 AI 対話による自己理解促進を組み込んだ設計、広島は 3,000 件の自記式意見処理。組織採用がボトルネック
- `11_海外におけるブロードリスニング` — Polis / vTaiwan / Remesh / Birdwatch、AI ツールは熟議文化に上乗せされる accent であって熟議の代替ではない、という設計哲学（Vaidya）

### Priority 3: 補助・背景

- `00_序文.md` / `00_本書の読みかた.md` / `01〜03` — ブロードリスニング概念定義、デジタル民主主義文脈
- `04_01〜04_04` / `06_01〜06_05` / `07_*` / `09_*` / `10_01〜10_05` / `11_02〜11_05` — 個別事例。要求仕様や障害事例として読める箇所は Priority 2 章にも触れられているのでまず Priority 2 を読む。Code for Japan / Democracy X / litela / 富士通 chapter は、implementation partner verified case や adjacent practice の分類根拠として使い、自治体公式 proof や 8/2 first demo 候補とは分ける
- `99_付録_公開事例一覧.md` — Web 公開された国内事例 catalog。外部ページ化では primary URL を個別確認する必要があるので、direct confirmation 済み事例は [[public-web-broadlistening-japan-use-cases-2026-06-30]]、付録由来の追加候補は [[broad-listening-book-public-case-appendix-2026-06-30]] を見る
- `99_付録_用語集.md` — 書籍側用語集。[[glossary]] と突き合わせる

### コードとプロンプト

- `code/llm_opinion_analysis.py` — LLM 分類のリファレンス実装（Structured Output）
- `code/political_wordcloud.py`, `code/rashomon_wordcloud.py` — wordcloud アンチパターンの参照実装
- `code/test_mini_kouchou_ai.py` — 13.3.2 のミニ広聴AIの構造テスト
- 13 章本文のプロンプト全文（抽出・初期ラベリング・統合ラベリング・要約）は kouchou-ai 本体の `apps/api/broadlistening/pipeline/prompts/` および `packages/analysis-core/.../prompts/` と突き合わせる際の参照になる

## 書籍と本体実装の照合上の注意

- 本書は **2026 年出版前** の確定版相当として書かれている。たとえば `analysis-core` への移行・`run_workflow()` 化・[[plugin-system|plugin 化]] のような 2026-Q1 以降の実装変化はほぼ書かれていない
- 「広聴AI では K-means / Ward を使う」「UMAP→クラスタリング順」などの記述は本体実装と一致するが、`analysis_mode=llm_grouping` 等の今後の枝は書籍には登場しない
- column / case の引用は **取材時点の運用** を写しているので、現状の機能整理（[[refactoring-status]]）と必ずしも一致しない

## Updates

- 2026-06-30: `work/broad-listening-book` を `9c22db6` で確認済みとし、Code for Japan / Democracy X / litela / 公明党 / 富士通章を [[broad-listening-book-public-case-appendix-2026-06-30]] と国内事例 map の source strength 補正に使ったことを追記した。
- 2026-06-30: Web 公開版の `99_付録_公開事例一覧.md` を [[broad-listening-book-public-case-appendix-2026-06-30]] として切り出し、公開事例 catalog は primary URL 確認済みと付録由来候補を分ける運用に補正した。
- 2026-05-21: 初回作成。`5826726` 時点で章マップを取得
