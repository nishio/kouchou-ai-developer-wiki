---
name: broad-listening-book
summary: DD2030 書籍「選挙を変えたブロードリスニング」（インプレス、CC BY-NC 4.0）。設計判断・運用知見・将来開発の素材として開発向け参照源にも使う
type: entity
sources:
  - meeting-minutes.md
  - broad-listening-book-source.md
---

## Scope note (2026-05-21 更新)

当初は `raw/init.txt` の指示により書籍プロジェクト自体は Wiki スコープ外としていた。しかし 2026-05-21 に本書 clone を `work/broad-listening-book/` に取り、**12〜13 章・10_00 DD2030 節・現場 column / case 章は kouchou-ai 開発の一次資料として価値が高い** ことを確認したため、書籍本文を source として扱う方針に変更した。

- 書籍 source として読む対象: [[broad-listening-book-source]] を参照
- 開発向けに抽出した知見: [[broad-listening-book-extractions]]

書籍そのものの運営（インプレスとのやりとり、表紙、組版、印税、CC ライセンス選定の議論）はなお Wiki スコープ外。

## なぜ開発 wiki に取り込む価値があるか

[[kouchou-ai]] のコードに影響する判断が書籍タイミングで決まる／確定する：

- **v4 凍結 / v5 リリース時期** — 書籍出版前後の安定性要件で決定（[[versioning-strategy]]）
- **書籍 CC ライセンス** — CC-BY → CC-BY-NC に変更（タグ `license-cc-by-4.0-final` 以前は CC-BY 4.0）
- **書籍用の用語整理**（民意 vs 統計的世論 など）が [[kouchou-ai]] の UI 文言に波及する
- **設計判断の公開版** — Slack / 議事メモに散在していた「なぜ K-means」「なぜ UMAP→クラスタリング」「なぜ KJ法プロンプト」が出版可能形でまとまった（13 章）
- **現場運用知見** — 自治体・選挙メディア・国政選挙の取材で観測された label 抽象問題、off-topic 大クラスタ、自己理解ボトルネックなど、開発機会として読める指摘が章ごとに散在

## 主担当

- [[tokoroten]] — 主担当
- インプレス（出版社）— 編集側
- Luke Closs — 英語版／Web サイト

## 外部リンク

- https://broadlisteningbook.com
- `digitaldemocracy2030/broad-listening-book` リポジトリ（GitHub）

## Updates

- 2026-05-17: 初回作成（スコープ外の参照用スタブ）
- 2026-05-21: clone を `work/broad-listening-book/` に取得し、書籍を開発向け source として扱う方針へ更新。[[broad-listening-book-source]] と [[broad-listening-book-extractions]] を新設
