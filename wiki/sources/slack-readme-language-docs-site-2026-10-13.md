---
type: source
summary: "2026-10-12〜13 Slack #2_開発_広聴ai で、README を一旦英語版にした後に日本語版へ戻した件をめぐる nishio / ohki-shingo のやりとり。nishio は『section 名アンカーリンクが存在することを理由に README 改訂を止めるのは筋が悪い、外部リンクは個別ドキュメントページへ張るべき』、ohki は『全面英語の README は日本語ユーザーを面食らわせて離脱させる懸念』、nishio は『英語で怯む層が見るべきは英語UIの GitHub ではなくドキュメントサイト』と整理した"
sources:
  - slack-logs mirror (#2_開発_広聴ai, 2026-10-12〜13)
  - github-dev-docs.md
---

## 何のソースか

`digitaldemocracy2030/slack-logs` の `mirror/`（synced_at 2026-10-13T00:28Z、直近 75 日窓）から読んだ #2_開発_広聴ai の 2026-10-12 のスレッドと、2026-10-13 11:15 JST の nishio 返信（これは user から貼られたもの。mirror sync 時刻より後の発言のため、本スナップショット時点では mirror には未収録）。最終読解日 2026-10-13。`raw/` への固定 snapshot はまだない。

スレッドの起点（thread root）は nishio の 2026-10-12 17:58 JST の投稿。

## 背景にある README の言語切り替え事件

このスレッドは、直前に起きた [[kouchou-ai]] README の言語差し替えと差し戻しを受けたもの。`work/kouchou-ai/` の main コミット履歴で裏が取れる。

- **PR #959**（merged 2026-10-09, by katsushi2441）: 韓国語版 `README.ko.md` を追加
- **PR #966**（merged 2026-10-09, by nishio）: `README.md` を英語版にし、日本語版を `README.ja.md` へ移す（= トップの README をデフォルト英語化）
- **PR #968**（merged 2026-10-12, by shingo-ohki）: 日本語 README をデフォルトに戻す（本スレッドで言う「緊急避難的」な差し戻し）

差し戻し後の current main の `README.md` は日本語がデフォルトで、先頭行に `[English](./README.en.md) | 日本語 | [한국어](./README.ko.md)` という言語リンクを持つ形。英語版は `README.en.md`、韓国語版は `README.ko.md` として併存する。

英語化の発端は 2026-10-09 17:23 JST の nishio 投稿：「日本国外からの注目も集まってきつつある状況で、英語の README がないのは問題。README.md を英語にして、日本語版を 1 行目からリンクする、韓国語版もする」。

## スレッドの内容

### nishio（2026-10-12 17:58 JST, thread root）

- README を日本語に戻すのは今回は緊急避難的に OK
- ただし「README の section 名リンクが存在すること」を根拠に変更を妨げると、金輪際 README の改訂ができなくなるので基本的には筋が悪い
- 外部からリンクしたいなら、ドキュメントに個別ページを作るべき
- 徐々にそういう形態に置き換えていきたい

### ohki-shingo（2026-10-12 20:25 JST）

- 自分の懸念はむしろ UX。マニュアルを見ようとアクセスした人が全面英語のドキュメントを見て面食らい、そのまま閉じてしまわないか
- そもそも GitHub へのアクセス自体が脱落の原因になりそう
- 長期的には README ではなく、ちゃんとしたドキュメントを用意する必要がある点には賛成

### nishio（2026-10-13 11:15 JST）

- 英語で怯むような人が見るべきものは、英語 UI の GitHub ではなくドキュメントサイトでは
- ドキュメントサイトも用意したような気がするが記憶の彼方

## 読解上の注意・事実確認

- nishio が「記憶の彼方」と言うドキュメントサイトは**実在する**。`mkdocs.yml` の `site_name: 広聴AI Documentation` / `site_url: https://digitaldemocracy2030.github.io/kouchou-ai/`。README からも各種 setup / user-guide ページがこの GitHub Pages サイトへリンクしている
- したがって論点は「ドキュメントサイトが無い」ではなく、「非開発者・非英語話者が最初にドキュメントサイトへ着地する導線になっていない（README / GitHub が入口になっている）」ことにある。これは [[nishio-docs-entry-restructure-discussion-2026-06-03]] / [[kouchou-ai-docs-entry-restructure-2026-06-03]] の『docs 入口がセットアップ起点』問題の延長線上
- nishio の「section 名リンクで README を凍結するな」は、README への外部ディープリンク（`#アンカー`）と README 改訂の間にできる結合を footgun として指摘したもの。distill した設計判断は [[readme-anchor-freeze-and-docs-entry-2026-10-13]]。これは GitHub issue **#977**（open / nishio 起票 / 2026-10-12「README 見出しアンカーへの外部直リンク依存をやめ、安定URL(docs)へ寄せる（PR #968 残件）」）として実トラッキングされている
- この source をきっかけに docs サイトを読み直したところ、ホームの OS カードで mkdocs のアイコンショートコードが生テキスト表示されている別バグが見つかった（[[docs-site-icon-shortcode-bug-2026-10-13]]、PR #990 で修正）
- 同じ Slack 窓（2026-10-11〜12）では analysis-core のライセンス表記（MIT→AGPL）も別スレッドで走っていたが、それは [[analysis-core-license-history-2026-10-12]] / [[analysis-core-license-intent-2026-10-12]] 側の話題で、本スレッド（README 言語・ドキュメント導線）とは別

## Updates

- 2026-10-13: 初版作成。README 言語差し戻し（#966→#968）と docs 導線の Slack スレッドを source 化。設計判断は [[readme-anchor-freeze-and-docs-entry-2026-10-13]] へ filing back
