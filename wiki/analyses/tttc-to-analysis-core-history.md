---
name: tttc-to-analysis-core-history
summary: "TTTC の clone / CUI 前提から、Web UI で包んだ広聴AI、さらに PyPI の analysis-core をサーバが呼ぶ現在形までの入口設計の変遷"
type: analysis
sources:
  - meeting-minutes.md
  - source-code.md
  - broad-listening-book-source.md
  - pypi-release-observation-2026-05-19.md
---

## 結論

ユーザの整理は概ね正しい。広聴AIの入口設計は、**TTTC / 初期広聴AIの clone 前提・開発者向け入口** から出発し、**非専門家でも扱えるように server / Web UI で包み**、その結果として **研究者や開発者には重くなったので `analysis-core` を PyPI / CLI として切り出し、server はそれを呼ぶ consumer に戻す**、という順で変化してきた。[[meeting-minutes]]より [[source-code]]より

## 時系列

### 1. 起点は TTTC Scatter 系の clone / CUI 前提

`kouchou-ai` は TTTC Scatter を起点にしたフォークであり、書籍 source でも `10_00_DD2030による広聴AIの開発活動.md` の重要点として「TTTC Scatter からのフォーク経緯」「Web 化」が挙がっている。つまり出発点は、まず分析コアがあり、その周囲に DD2030 側の実務要請に応じた差分を載せていく流れだった。[[broad-listening-book-source]]より

`10_00` 本文でも、TTTC Scatter はコマンドラインで動作するツールであり、Python 環境の構築などソフトウェアエンジニアリングのスキルが必要だったと明記されている。書籍側の叙述でも、最初の問題設定は「分析アルゴリズムが弱い」より前に、**入口が技術者寄りすぎる** ことだった。[[broad-listening-book-source]]より

既存 wiki でも、TTTC は CLI ツールで、チーム安野が SaaS 風のプレビュー／共有 UI を被せたことでフォークが現実的になったと整理されている。広聴AIは最初から Web プロダクトとして設計されたというより、**clone して使う分析ツールを、日本の実務に合わせて包み替えていったもの** と読む方が歴史に合う。[[meeting-minutes]]より

### 2. 実務上の要請で Web UI / server を作った

2025-10-08 の議事録では、現在の Web UI モード C は「CUI ツールである Talk to the City Scatter を使う過程で、実際のプロジェクトに使っていく上ではプレビューを公開前にシェアする環境が必要だと感じたことによって作られた」と説明されている。server / Web UI は単なる見た目改善ではなく、**共有しながら運用するための包み込み** だった。[[meeting-minutes]]より

この点は書籍 `10_00` の比較表でもかなりはっきりしている。そこでは `TTTC Scatter = CLIツール / 環境構築はユーザー側 / 分析はコマンドライン / 結果共有は HTML をホスティング`、`広聴AI = Webアプリ / 環境構築はサーバー側 / 分析はブラウザ操作 / 結果共有は URL を共有するだけ` と整理されている。つまり Web 化の狙いは「GUI を付けた」ことではなく、**環境構築責任と共有導線を利用者からサーバ側へ寄せること** だった。[[broad-listening-book-source]]より

同じ箇所では、「この C を無償公開しておけば地方自治体でも自分たちで使えるかと思ったが、サービスをデプロイできるエンジニアが希少すぎてあまりうまくいかなかった」とも語られている。つまり Web 化で clone / CLI よりは使いやすくなったが、それでも self-host 前提は一般利用者には重かった。[[meeting-minutes]]より

### 3. その反動で、研究者・開発者には逆に重くなった

2025-12 から 2026-01 にかけての議論では、「現在の広聴AIは技術スタックが深すぎるので簡略化したい」「ステップごとに分析したいユーザにとっては Jupyter Notebook、したくないユーザにとっては pip」という整理が出ている。続く Slack 転載では、A=研究者向け ipynb、B=エンジニア向け pip / CLI、C=B をラップした WebUI、D=C の hosted demo、という 4 形態が明示された。[[meeting-minutes]]より

この A/B/C/D 整理が示しているのは、Web UI を否定することではなく、**非専門家向けの入口と、研究開発向けの入口を分け直す必要** が見えてきた、ということだった。議事録でも「アルゴリズム改善の研究をしていくなら A があるとよく、今提供しているのは C」と説明されている。[[meeting-minutes]]より

書籍 13.3 も、この分化を補強する。13.3 は「Python の環境を持っている読者は、手元で動かしながら読んでください」としたうえで、`pip install openai pandas numpy scikit-learn umap-learn matplotlib scipy` から始まるミニ広聴AI実装を提示している。これは現在の `analysis-core` そのものではないが、**研究者・開発者向けには、フルの Web サーバ群より軽い Python 実験入口が必要** だという発想と整合する。[[broad-listening-book-source]]より

### 4. その実装が `packages/analysis-core` と CLI / PyPI 切り出し

2026-01-19 の commit 列では、まず `48cf3c1` で `packages/analysis-core` のパッケージ構造が作られ、続いて `8fb31f8` で `PipelineOrchestrator` と CLI 実装、`e0c051d` で API が旧 `hierarchical_main.py` ではなく `python -m analysis_core` を subprocess で呼ぶよう切り替わった。ここで analysis の本体を package / CLI として独立させ、server はそれを呼ぶ consumer 側へ回したと読める。[[source-code]]より

2026-01 の定例メモでも、「CLI 実行、PyPI からのインストール、プラグイン拡張などを可能にするリファクタリング計画を実行中」「CLI で分析処理が可能」「Python スクリプトから import して使うことも可能」と報告されている。設計意図と実装が一致している。[[meeting-minutes]]より

### 5. 2026-05 には PyPI publish まで自動化された

2026-05-18/19 には `analysis-core-v*` tag push を trigger に `kouchou-ai-analysis-core` を PyPI publish する workflow が実地確認され、`v0.1.2` で公開成功が観測されている。これで `analysis-core` は「repo 内の整理されたサブディレクトリ」ではなく、外部配布される独立 package になった。[[pypi-release-observation-2026-05-19]]より

## この変化をどう読むべきか

### server が本体で、CLI が付録なのではない

現在の canonical な解析本体は `packages/analysis-core` で、FastAPI 側は `apps/api/src/services/report_launcher.py` から `python -m analysis_core` を subprocess 起動している。したがって今の構図は「server の中に解析がある」ではなく、**共通 core を Web UI が利用している** と読む方が正確である。[[source-code]]より

### Web UI と CLI は競合ではなく役割分担

A/B/C/D 整理に沿って読むと、Web UI は非専門家・共有・運用の導線であり、CLI / PyPI は研究者・データサイエンティスト・AI coding agent 向けの導線である。同じ core を別の入口で使う形に戻したことで、非専門家向け UX を保ちながら、研究開発側の experimentation も再びやりやすくした。[[meeting-minutes]]より [[source-code]]より

### PyPI 切り出しの狙いは「配布」だけではない

2026-01-24 の定例メモでは、CLI 化によって「ブラウザの GUI を使わなくても実行可能になったので各種の BI ツールなどと連携して使うことが容易になる」と整理されている。つまり PyPI / CLI 化は install を楽にするだけでなく、**分析手法や可視化を差し替えながら再利用するための土台づくり** でもあった。[[meeting-minutes]]より

書籍 13 章の存在自体も、この方向性を後押ししている。13 章は「広聴AIの実装を読み解く」という章立てで、パイプラインの説明だけでなく「自分でミニ広聴AIを実装する」ハンズオンまで含んでいる。これは利用者像として、完成した Web アプリの利用者だけでなく、**コードを読み、手元で変え、比較実験する読者** を明確に想定している。PyPI / CLI 化は、その読者像に対応する現実の入口だと読める。[[broad-listening-book-source]]より

## いま残る含意

- 今後の新しい analysis mode や plugin は、まず `analysis-core` 側に載せ、Web UI はその consumer として追随する方が筋がよい。[[source-code]]より
- 一方で非専門家向け導線の課題は消えておらず、A/B/C/D 整理でいう D、すなわち「エンジニアがいない組織でも試せる hosted / demo 形態」はまだ未解決である。[[meeting-minutes]]より
- したがって現在の方向性は「Web UI か CLI か」の二者択一ではなく、**core を共通化しつつ入口を複線化する** ことだと読むのが自然である。[[meeting-minutes]]より [[source-code]]より

## Open Questions

- Jupyter Notebook を B の補助とみなすか、A として独立にメンテするか
- Web UI が今後どこまで `analysis-core` の新機能へ即応するべきか
- A/B/C/D のうち D を実際にどう提供するか

## Updates

- 2026-05-23: `raw/meeting_minutes.txt`、書籍 source、local clone の commit history、PyPI release observation を突き合わせて初版作成
- 2026-05-23: 書籍 `10_00` の TTTC Scatter vs 広聴AI 比較表と、13.3 のミニ広聴AI実装導線を根拠として追記
