---
title: "書籍『政治・自治体・企業に広がるブロードリスニング』"
name: broad-listening-book
summary: "DD2030 書籍「政治・自治体・企業に広がるブロードリスニング」（インプレス、CC BY-NC 4.0。2026-07-21 に旧仮題「選挙を変えたブロードリスニング」から改題）。設計判断・運用知見・将来開発の素材として開発向け参照源にも使う"
type: entity
sources:
  - meeting-minutes.md
  - broad-listening-book-source.md
---

## What

DD2030 の書籍「政治・自治体・企業に広がるブロードリスニング」（出版社はインプレス）。原稿は公開リポジトリ `digitaldemocracy2030/broad-listening-book` で管理されている。2026-07-21 に、旧仮題「選挙を変えたブロードリスニング 生成AIが実現する民意の可視化と分析(仮)」から現在の書名に改題された（book repo の PR [#144](https://github.com/digitaldemocracy2030/broad-listening-book/pull/144)、[[meeting-minutes]] 2026-07-27 見出しより）。[[broad-listening-book-source]] など改題前に取り込んだページは、旧仮題の時期の原稿にもとづいている。

## この wiki での扱い

書籍本文は、kouchou-ai 開発の一次資料として読む（特に 12〜13 章・10_00 DD2030 節・現場 column / case 章）。読む対象は [[broad-listening-book-source]]、開発向けに抽出した知見は [[broad-listening-book-extractions]]。書籍そのものの運営（インプレスとのやりとり、表紙、組版、印税、CC ライセンス選定の議論）は扱わない。

## なぜ開発 wiki に取り込む価値があるか

[[kouchou-ai]] のコードに影響する判断が書籍タイミングで決まる／確定する：

- **v4 凍結 / v5 リリース時期** — 2025-12 に、書籍出版前後の安定性要件からリリース方針を決めた。実際には v4.0.0 を 2025-12 末に打ち、リファクタは main 上で段階的に進めて v4.1.0（2026-10-13）、v4.2.0（2026-10-26）を発行した。v5 は 2026-11-03 時点で未リリース（[[versioning-strategy]]）
- **書籍 CC ライセンス** — CC-BY → CC-BY-NC に変更（タグ `license-cc-by-4.0-final` 以前は CC-BY 4.0）
- **書籍用の用語整理**（民意 vs 統計的世論 など）が [[kouchou-ai]] の UI 文言に波及する
- **設計判断の公開版** — Slack / 議事メモに散在していた「なぜ K-means」「なぜ UMAP→クラスタリング」「なぜ KJ法プロンプト」が出版可能形でまとまった（13 章）
- **現場運用知見** — 自治体・選挙メディア・国政選挙の取材で観測された label 抽象問題、off-topic 大クラスタ、自己理解ボトルネックなど、開発機会として読める指摘が章ごとに散在

## 主担当

- [[tokoroten]] — 主担当
- インプレス（出版社）— 編集側
- Luke Closs — 英語版／Web サイト

## 外部リンク

- https://broadlisteningbook.com （Web ブック。英語版のサイト名は "Broad Listening: Across Politics, Local Government, and Business"、日本語版は `/ja/`）
- `digitaldemocracy2030/broad-listening-book` リポジトリ（GitHub）

## Updates

- 2026-05-17: 初回作成（スコープ外の参照用スタブ）
- 2026-05-21: clone を `work/broad-listening-book/` に取得し、書籍を開発向け source として扱う方針へ更新。[[broad-listening-book-source]] と [[broad-listening-book-extractions]] を新設
- 2026-10-21: 書名を 2026-07-21 の改題後の「政治・自治体・企業に広がるブロードリスニング」に更新し、旧仮題を summary と本文に併記した（book repo の PR [#144](https://github.com/digitaldemocracy2030/broad-listening-book/pull/144)、[[meeting-minutes]] 2026-07-27 見出しより）。あわせて「Scope note」を「この wiki での扱い」に改め、Updates の 2026-05-21 の行と重複していた経緯とローカルのパスを除いた。v4 / v5 方針の行を、2025-12 の決定とその後の実際が分かる書き方に直した
- 2026-11-25: 書籍 Web 版は「先行公開ドラフト」で、目次（`/ja/`）以外の各章はログインが必要だった。サイトのソースと問題報告先は `lukec/broad-listening-book-site`。書籍本文（wip を除く）には広聴AIのリポジトリ・docs・ブラウザ版へのリンクがないため、読者向けの入口を本体 docs の「書籍を読んだ方へ」として作った（[PR #1265](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1265)、11-25 に main 済み。URL は `https://digitaldemocracy2030.github.io/kouchou-ai/book`。判断と根拠は [[book-reader-entry-2026-11-25]]）
- 2026-11-03: v4 / v5 方針の行に v4.2.0（2026-10-26。`gh release list` で Latest）を足し、v5 未リリースの確認日を 11-03 にした
- 2026-11-25: [DD2030 公式のブロードリスニングページ](https://dd2030.org/broad-listening/)が案内する書籍サイトの実装リポジトリは [lukec/broad-listening-book-site](https://github.com/lukec/broad-listening-book-site)。[原稿リポジトリ](https://github.com/digitaldemocracy2030/broad-listening-book)の内容から多言語のHTML版を生成し、[日本語Web版のトップ](https://broadlisteningbook.com/ja/)と「この本について」のページを持つ。広聴AIへの導線は [[book-release-reader-readiness-2026-11-25]] を参照。
