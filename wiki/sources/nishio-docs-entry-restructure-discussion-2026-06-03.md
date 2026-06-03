---
type: source
summary: 2026-06-03 nishio との対話。kouchou-ai 本体 docs が「セットアップから始まる」構造であることへの違和感と、デモ閲覧を入口にした spine 再設計、実験的機能カタログの提案
sources:
  - user-message-2026-06-03
---

## 文脈

2026-06-03、nishio との対話で「kouchou-ai のドキュメントのあり方が、そもそも今の形が適切でない」という違和感が提起された。対象は本 developer-wiki ではなく [[kouchou-ai]] 本体の `docs/` (mkdocs サイト)。

現状の `docs/` は `getting-started/ user-guide/ development/ deployment/ refactoring/ misc/` という分類で、入口が `getting-started/` (= セットアップ手順) から始まる。

## 対話で出た主張

### セットアップを入口にすることのバイアス

- 「セットアップの仕方」から話が始まる構造は「興味を持った人はみんなセットアップすべきだ」という誤ったバイアスを産んでいたのではないか
- 大多数の「興味を持った人」は、まず広聴AI が何を produce するか (= レポート) を見たい / broad listening という方法論を理解したい段階で、自分でツールを立てる必要はない
- 結果として「興味を持つ ≒ 開発者になる」という経路に絞り込まれ、レポートの読み手・分析者・方法論に興味のある研究者が振り落とされる

### 新しい spine の提案

nishio から提示された入口構造:

1. **まずデモサイトでレポートを見せて「レポート viewer をどう使うか」が必要**
2. **次に「自分も自分の持ってるデータで分析レポートを作りたい」と思った人向けに**、誰かが host したサービスで分析するスタイルと、自分で host するスタイルがある
3. **後者の段階で初めて自前セットアップが必要になる**
4. 連想として「研究者・開発者はこちら」で CLI 版の紹介へのページに分岐する

### 「getting-started」というネーミングへの指摘

- 上記の spine 上で self-host setup を `getting-started/` に置くのは、ネーミング自体がおかしい
- `getting-started` という名前自体が「ここから始めろ」という暗黙のメッセージを発しており、構造のバイアスと同じ罪を犯している

### 実験的機能カタログの提案

- LLM grouping や tokoroten の DivCon / Farbrain、nishio のマンダラート可視化など、実験的機能が CLI に追加されたり関連プロジェクトとして個人 repo で作られたりしている
- これらに対するカタログが必要

#### カタログの置き場と粒度

- 名前は「ecosystem」より「実験的機能」寄り
- kouchou-ai 本体 docs の中に置くべき。理由: 将来的に取捨選択してメンテナンスされるべきものだから
- 細かい分類をしないで、まずはフラットに集めるところから

### 既存 docs と stale 対策の運用ルール化

- 根本から構造が変わりつつあるので既存のドキュメントは改善や削除も含めて柔軟に考えるべき
- 個人 repo は所有者の都合で archive / private / 改名されうるので、catalog エントリには「最後に状態を確認した日」を入れて stale をマークできるようにする ← これはルールとする (developer-wiki 側で source の freshness を明示するルールと同じ発想)

## 関連

- [[kouchou-ai-docs-entry-restructure-2026-06-03]] が spine 再設計の analysis
- [[experimental-features-catalog-proposal-2026-06-03]] が catalog の analysis
- AI 側 memory `feedback_developer_label_caution` (「開発者」には組織内デモ役 / WebUI 開発者 / 分析者・研究者 の 3 サブ役割がある) という観点と整合する
