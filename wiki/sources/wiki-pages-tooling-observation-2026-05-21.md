---
type: source
summary: "この developer-wiki repo の GitHub Pages 現状実装と Quartz 公式 docs を突き合わせた観測メモ"
sources:
  - https://quartz.jzhao.xyz/
  - https://quartz.jzhao.xyz/authoring-content
  - https://quartz.jzhao.xyz/build
  - https://quartz.jzhao.xyz/hosting
  - https://scrapbox.io/nishio/Quartz_+_GitHub_Pages_%E3%81%A7_Obsidian_%E3%82%92%E5%85%AC%E9%96%8B%E3%81%99%E3%82%8B%E6%89%8B%E9%A0%86
  - https://gist.github.com/nishio/e316a87d94291bd91f2480ad0492cef9
  - https://gist.github.com/nishio/35d604f23a39aca369ac74db8b65b655
  - init.txt
---

この source は、**この repo 自身の Pages 配信実装** と **Quartz 4 の公式 docs** を並べて読むためのもの。`kouchou-ai` 本体ではなく、`kouchou-ai-developer-wiki` の公開方法に関する一次参照として使う。

## Pre-switch repo observation

- 現状の Pages 配信は `mkdocs.yml`、`requirements-pages.txt`、`scripts/build_pages_docs.py`、`.github/workflows/deploy-pages.yml` で成立している。`mkdocs.yml` は `docs_dir: .pages/docs`、workflow は Python を立てて `mkdocs build` する構成。`mkdocs.yml` / `.github/workflows/deploy-pages.yml` / `requirements-pages.txt` より
- `scripts/build_pages_docs.py` は `wiki/` 以下の Markdown を `.pages/docs/` へコピーしつつ、`[[wikilink]]` を通常 Markdown link に書き換える adapter である。つまり MkDocs は source of truth ではなく、**変換済み docs tree の renderer** として使われている。`scripts/build_pages_docs.py` より
- この repo の wiki 本文は `[[foo]]` / `[[foo|label]]` 形式の wikilink と YAML frontmatter を前提にしている。`wiki/index.md` や各 `wiki/analyses/*.md` より

## Quartz official docs

- Quartz 4 は Markdown をサイト化する static-site generator で、authoring content は `/content` folder 配下を前提とする。wikilinks を含む Obsidian Flavored Markdown を default で扱える。[Welcome to Quartz 4](https://quartz.jzhao.xyz/) / [Authoring Content](https://quartz.jzhao.xyz/authoring-content) より
- Quartz の build command は `npx quartz build` で、`-d` ないし `--directory` で content folder を差し替えられる。つまり `wiki/` をそのまま content root として指定できる余地がある。[Building your Quartz](https://quartz.jzhao.xyz/build) より
- GitHub Pages 配信は GitHub Actions workflow で `npm ci` → `npx quartz build` → `public/` を upload するのが公式導線。`baseUrl` を正しく設定しないと RSS や sitemap など一部機能に影響する。[Hosting](https://quartz.jzhao.xyz/hosting) より
- Quartz は `file.html` 形式を出力するため、GitHub Pages では trailing slash 付き既存リンクを持っていると移行時に注意が要る。[Hosting](https://quartz.jzhao.xyz/hosting) より

## Interpretation

- この repo の現行 MkDocs 構成は「Markdown authoring 体験」と「公開 renderer」の間に custom rewrite script を挟む暫定構成と読める。`scripts/build_pages_docs.py` より
- 一方 Quartz は wikilinks を default で解釈し、Explorer / Backlinks / Graph / Folder listing のような wiki 向け導線を持つので、**この repo の wiki 的な書き方と公開体験の距離が近い** と判断しやすい。[Welcome to Quartz 4](https://quartz.jzhao.xyz/) / [Authoring Content](https://quartz.jzhao.xyz/authoring-content) より

## Current repo observation (after switch)

- 2026-05-21 の切替後は、repo root に Quartz 本体ソース (`quartz/`)、`package.json`、`quartz.config.ts`、`quartz.layout.ts`、`tsconfig.json` を置き、`pnpm build` が `node ./quartz/bootstrap-cli.mjs build -d wiki` を呼ぶ構成になった。repo 実装より
- GitHub Pages workflow も Python + MkDocs から Node 22 + pnpm + Quartz build へ差し替わり、upload 対象は `site/` ではなく `public/` になった。`.github/workflows/deploy-pages.yml` より
- `wiki/` は変わらず source of truth で、Quartz が `-d wiki` で直接読む。MkDocs 時代に必要だった `.pages/docs/` への変換コピーは消えた。repo 実装より
- 切替の過程で、既存 page の frontmatter は lint が想定していたより緩く、Quartz の YAML parser では落ちる summary 行が複数見つかったため、summary を quoted string に正規化し、`scripts/lint_wiki.py` も strict YAML parse を行うよう補強した。repo 実装より

## Project-site subpath observation

- Quartz 4 の GitHub Pages project-site 配信では、`configuration.baseUrl` に `nishio.github.io/kouchou-ai-developer-wiki` のように subpath まで含めるのが公式導線である。内部リンク自体は相対 URL として出るため、renderer 本体は project-site hosting を前提にできる。[Hosting](https://quartz.jzhao.xyz/hosting) より
- 2026-05-28 時点で、GitHub Pages は `https://nishio.github.io/kouchou-ai-developer-wiki` を `https://nishio.github.io/kouchou-ai-developer-wiki/` へ 301 redirect していた。したがって root の末尾 slash 欠落を Quartz `Head` で補正する必要性は低い。repo 実装と live Pages 確認より
- 以前の local patch では `quartz/components/Head.tsx` に root 専用 `<base href="https://nishio.github.io/kouchou-ai-developer-wiki/">` と redirect script を足していたが、これは upstream Quartz v4.5.2 の `Head.tsx` にはない差分だった。project-site 対応は `baseUrl` 設定に寄せ、HTML `<base>` に頼らない方が Quartz の相対 URL 設計と合う。repo 実装と upstream Quartz より
- 2026-05-28 の修正で `Head.tsx` を upstream 相当へ戻し、`scripts/check_pages_links.py` を追加した。build 後の `public/` 全 HTML を `/kouchou-ai-developer-wiki/` 配下として解決し、内部リンク・静的 asset・`fetch()` が subpath 外へ逃げないこと、存在する public path に解決されること、生成 HTML に `<base>` が入らないことを CI で検査する。repo 実装より
- Scrapbox から辿った旧 Gist は、`wiki/` を編集用、`content/` を Quartz 入力用に分け、`resolve-links.py` で wikilink を正規化する汎用移植ガイドだった。これは Obsidian vault から公開用 tree を作る方式として有効だが、この repo のように `wiki/` 自体が公開 source of truth である場合には `quartz build -d wiki` の直接方式が自然である。旧 Gist より
- この整理を新 Gist `Quartz + GitHub Pages project site で Wiki を公開する設計メモ` として外部化した。新 Gist では、`baseUrl` が project-site hosting の正規支点であること、`<base>` patch を避けること、`wiki/` direct と `wiki/ -> content/` 変換は用途で選ぶこと、生成物リンク検査を CI に入れることをまとめた。新 Gist より

## Open Questions

- Quartz をこの repo に vendor するか、別 repo で publish layer を持つか
- `wiki/log.md` や source ページ群を公開ナビゲーションにどう見せるか
- 既存の `mkdocs.yml` / `scripts/build_pages_docs.py` を完全撤去するか、移行期間だけ残すか
- Quartz vendor 側の local patch をどこまで許すか。project-site hosting のように upstream が持つ前提は、まず公式設定に寄せる方がよい

## Updates

- 2026-05-21: 初版作成
- 2026-05-21: Quartz 実切替を反映。MkDocs 関連ファイルを撤去し、Node/pnpm/Quartz workflow へ移行した current state を追記
- 2026-05-28: project-site subpath のリンク切れ再発を受け、local `<base>` patch を撤去して `baseUrl` + 生成物リンク検査へ寄せる観測を追記
- 2026-05-28: Scrapbox / 旧 Gist の `wiki/ -> content/` 方式と、この repo の `wiki/` direct 方式を分けて整理し、新 Gist として外部化したことを追記
