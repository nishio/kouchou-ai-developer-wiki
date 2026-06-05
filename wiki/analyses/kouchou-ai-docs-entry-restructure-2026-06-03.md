---
type: analysis
summary: kouchou-ai 本体 docs の入口を「セットアップ」起点から「デモ閲覧 → 自分で作りたい人向け分岐 → 研究者・開発者向け分岐」という spine に組み替える提案。`getting-started/` というネーミング自体がバイアスを産んでいたという指摘も含む
sources:
  - nishio-docs-entry-restructure-discussion-2026-06-03.md
  - nishio-slack-azure-demo-visibility-proposal-2026-06-04.md
  - azure-demo-visibility-thread-resolution-2026-06-05.md
---

## 背景と問題提起

[[kouchou-ai]] 本体 docs (mkdocs サイト, `digitaldemocracy2030.github.io/kouchou-ai/`) は現在、入口が `getting-started/` から始まる。トップカテゴリは `getting-started/ user-guide/ development/ deployment/ refactoring/ misc/`。

[[nishio-docs-entry-restructure-discussion-2026-06-03]] で nishio から提起された違和感は次の 2 点。

1. **セットアップを入口にする構造が「興味を持った人 = 自分でツールを立てる開発者」というバイアスを産む**。本来の主役であるレポート (出力物) と broad listening という方法論が後景に追いやられ、レポートの読み手・分析者・方法論研究者が振り落とされる
2. **`getting-started/` というディレクトリ名そのものが「ここから始めろ」という暗黙のメッセージ**であり、構造のバイアスと同じ罪を犯している。spine の入口が変わるなら、self-host setup を担うディレクトリ名も中身を表す名前に変える必要がある

## 提案する spine

```
1. 入口: デモサイトでレポートを見る
   ├ レポート viewer の使い方 (クラスタ閲覧 / representative / フィルタ等)
   └ dd2030 以外でレポートを公開しているサイト・自治体へのリンク集

2. 「自分のデータで分析レポートを作りたい」分岐
   ├ a. 誰かが建ててくれたサーバを使う (dd2030 が SaaS 提供するならここ)
   ├ b. サーバを建ててくれる人を探す (仲介者・代行者の連絡先リスト)
   └ c. 自分でサーバを建てる (技術力と適切な計算環境が必要)
       └ ここで初めてセットアップ手順 (現 getting-started/* の中身) が登場

3. 「研究者・開発者はこちら」分岐
   ├ CLI 版 (analysis-core / pipeline) の紹介
   └ [[experimental-features-catalog-proposal-2026-06-03]] へリンク
```

セットアップは spine の入口ではなく、特定のニーズを持った人 (= 自分で host したい人) が辿り着く先のページ。

tier 2 の 3 択化は 2026-06-04 の [[nishio-slack-azure-demo-visibility-proposal-2026-06-04]] で refinement された。従来案の「(a) managed / (b) self-host」では「自分で建てる気はないが、社内 / 自治体内に建ててくれそうな人がいる」読者の経路がなかった。仲介者経路 (b) を明示することで、[[broadlistening-tool-ecosystem-vision]] の「組織内デモ役」「橋渡し役」が docs 内で対応する分岐を持てる。

## ネーミング方針

- `getting-started/` という名前は廃止する。「ここから始めろ」のニュアンスを路径名から外す
- self-host setup を担うディレクトリは `self-hosting/` など、何をするページかが名前から読める形にする
- 現状の `getting-started/quickstart.md`、`getting-started/mac-setup.md`、`getting-started/windows-setup.md`、`getting-started/linux-setup.md` は self-host stream の 2 階層下に押し込む

## 既存 docs の扱い

根本から構造が変わるので、既存ページは「新 spine のどこにも当てはまらない」「重複する」「stale」になる可能性がある。**既存のドキュメントは改善や削除も含めて柔軟に考える**。新構造に当てはめるためだけに無理に残さない (nishio 指示)。

`development/` 配下も、AI 側 memory `feedback_developer_label_caution` にある「開発者」3 サブ役割 (組織内デモ役 / WebUI 開発者 / 分析者・研究者) で見直すと、現状の `development/` は WebUI 開発者向けと CLI 開発者向けと plugin 作者向けが混在している。

## 関連 (memory / wiki)

- AI 側 memory `feedback_developer_label_caution` (「開発者」を一括りにしない、3 サブ役割) と整合させると、spine の 3 番目「研究者・開発者」も、もう一段の分岐 (CLI 研究者 / WebUI contributor / 組織内デモ役) が要る可能性
- [[experimental-features-catalog-proposal-2026-06-03]]: spine の 3 番目分岐配下に置く実験的機能カタログ
- [[meeting-report-draft]]: 構造の議論として次回定例で扱う候補

## Open Questions

### managed service 経路の実在性

- spine 2-a「誰かが host したサービスで分析する」は、現時点で actually 提供されているか未確認
- Azure デモ環境は存在するが、それは展示用であって「任意のユーザーが任意データを投げる service」とは違う可能性が高い
- 2026-06-04 に [[azure-demo-public-visibility-proposal-2026-06-04]] として 4 問が Ohki さんに投げられ、2026-06-05 に着地した ([[azure-demo-visibility-thread-resolution-2026-06-05]])。**viewer 公開と admin 共用は進める方向**で、これにより spine tier 1 と tier 2-a の docs 動線が埋められる前提が立った。ただし前提として container env の dd2030 fallback `OPENAI_API_KEY` を外し、3 点明示文言 (共用 / 機微情報禁止 / 保存・継続稼働非保証) を加える必要がある
- spine tier 1 のコンテンツ目的は **「使い方や準備すべきデータを理解するための参照環境」** であって「データ投入の予行演習」ではない、という再フレームも同 thread で出ている。docs 内コンテンツの設計 (viewer 操作解説 + サンプル CSV ダウンロード導線 + 公開事例リンク集) に直接効く

### 仲介者経路の docs 表現

- spine tier 2 選択肢 b「サーバを建ててくれる人を探す」は、docs に連絡先リスト or 代行可能な個人 / 法人ディレクトリを置く形で実装する想定
- 誰がリストをメンテするか、申告のあった代行者を docs に載せる基準、紹介後のトラブル時の責任分界点は未決

### レポート viewer の使い方をどこまで書くか

- spine の入口は「デモを見る」だが、ただ眺めるだけなのか、active に探索する (フィルタ / クラスタ深掘り) ことを期待するのかで、書くべき分量が変わる
- viewer 機能の網羅的なリファレンスを目指すか、最初の 5 分の体験 (見るべき 3 つのこと) に絞るか

### WebUI contributor の置き場

- 「apps/ を改修したい contributor」は spine の 3 番目「研究者・開発者」に並列するのか、別の分岐か
- AI 側 memory `feedback_developer_label_caution` と整合させると、CLI 研究者と WebUI contributor は読者として別物。spine をもう一段細分化するか、catalog 同様にフラットなランディングを置くか

### 既存 mkdocs ナビ構造の移行手順

- mkdocs.yml の nav は手書きの順序リスト。spine 変更は nav 全面書き換えになる
- 段階移行 (新 spine の入口だけ先に作って既存ページは順次移動) か、PR 一発で構造刷新するか

## Updates

- 2026-06-04: tier 2 を「(a) managed / (b) self-host」の 2 択から「(a) 誰かが建てたサーバ / (b) 建ててくれる人を探す / (c) 自分で建てる」の 3 択へ refinement ([[nishio-slack-azure-demo-visibility-proposal-2026-06-04]])。Azure デモを docs から動線化するための具体 4 問は [[azure-demo-public-visibility-proposal-2026-06-04]] へ切り出した
- 2026-06-05: Azure デモ動線化 4 問が [[azure-demo-visibility-thread-resolution-2026-06-05]] で着地。viewer 公開 + admin 共用は進める方向で、spine tier 1 と tier 2-a の docs 動線が埋められる前提が立った。tier 1 のコンテンツ目的は「データ投入の予行演習」ではなく「使い方や準備すべきデータを理解するための参照環境」、と再フレーム
