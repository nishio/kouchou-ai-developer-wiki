---
title: "docs サイトのアイコン表示バグ 2026-10-13"
type: source
summary: "2026-10-13 に kouchou-ai ドキュメントサイト（mkdocs-material）のホームを確認したところ、`docs/index.md` のアイコンショートコード `:fontawesome-brands-windows:` 等が変換されず生テキストで表示されていた。原因は `mkdocs.yml` の `markdown_extensions` に `pymdownx.emoji` が無いこと。3行追加する PR #990 を作成し、ローカル build で描画を確認した"
sources:
  - github-dev-docs.md
  - slack-readme-language-docs-site-2026-10-13.md
---

## 何のソースか

公開ドキュメントサイト `https://digitaldemocracy2030.github.io/kouchou-ai/` のライブ HTML と、`work/kouchou-ai main@8f402d2e` の `mkdocs.yml` / `docs/index.md` を照合した観測。最終確認日 2026-10-13。[[slack-readme-language-docs-site-2026-10-13]] の「ドキュメントサイトを読み直して確認して」という依頼をきっかけに見つけた。

## 症状（ライブサイトで確認）

ホームの「クイックスタート → 一般ユーザー向け」の OS カード（grid cards）で、アイコンの代わりにショートコードが生テキストで表示されていた。配信 HTML:

```html
<div class="grid cards">
<ul>
<li>
<p>:fontawesome-brands-windows: <strong>Windows</strong></p>
```

`:fontawesome-brands-windows:` / `:fontawesome-brands-apple:` / `:fontawesome-brands-linux:` の 3 件（`docs/index.md:25,30,35`）が該当。

一方、テーマ側のアイコン（palette のダーク/ライト切替トグル `material/brightness-7`、`extra.social` の `fontawesome/brands/github`、検索・ナビ）は inline SVG として正常描画されていた（ページ内 `<svg>` 13 個）。

## 原因

`mkdocs.yml` の `markdown_extensions` に **`pymdownx.emoji` が未設定**だった。

- `:fontawesome-...:` / `:material-...:` という**本文中のアイコンショートコード**は、`pymdownx.emoji`（material の `twemoji` index + `to_svg` generator）で初めて inline SVG に変換される。拡張が無いとコロン記法がそのまま素通りする
- テーマ側の `extra.social` `icon:` や palette `toggle.icon` はテンプレートが直接 SVG を埋め込むので拡張不要。**だからテーマアイコンは出るのに本文アイコンだけ出ない**という症状の食い違いになり、気づきにくい
- Material for MkDocs はアイコンをバンドル済み inline SVG で描くため、FontAwesome の webfont / CDN は使わない。CDN 読み込みの問題ではない

## 修正（PR [#990](https://github.com/digitaldemocracy2030/kouchou-ai/issues/990)）

`markdown_extensions` に 3 行追加:

```yaml
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
```

`docs/requirements.txt` は `mkdocs-material>=9.7.1` なので import パスは新しい `material.extensions.emoji.*`（旧 `materialx.emoji.*` ではない）。

### 動作確認

`mkdocs-material 9.7.7` でローカル build し、ホーム `index.html` を確認:

- 生テキストの `:fontawesome-brands-*:` が **0 件**（修正前は 3 件残存）
- grid cards 内に `<span class="twemoji"><svg ...>` が **3 件**描画され、各 OS のブランドアイコンが inline SVG になった

## Updates

- 2026-10-13: 初版作成。ライブサイトで症状を確認、原因を特定し PR [#990](https://github.com/digitaldemocracy2030/kouchou-ai/issues/990)（`pymdownx.emoji` 追加）を作成・ローカル build で検証。footgun は [[gotchas]] の「ドキュメント・運用」に登録
