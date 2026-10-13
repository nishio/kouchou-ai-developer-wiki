---
title: "公開サイトの表示規約（タイトル・slug・Explorer）"
name: quartz-site-presentation
type: concept
summary: "公開 Quartz サイトの表示規約。URL は英語 slug（ファイル名）のまま、ページ見出しと Explorer の表示名は frontmatter title（日本語）で与える。Explorer のフォルダ見出しは quartz.layout.ts の mapFn で日本語化し、mapFn/sortFn は client 側で再評価されるため制約がある"
sources:
  - source-code.md
---

## これは何か

この Wiki は [Quartz](https://quartz.jzhao.xyz/) で静的サイト化し、GitHub Pages に公開している（build は `quartz.config.ts` / `quartz.layout.ts`、deploy は `.github/workflows/deploy-pages.yml`）。本ページは、公開サイト上で各ページがどう表示されるか（URL と表示タイトル、Explorer のラベル）の規約をまとめる。[[source-code]]より

## URL と表示タイトルを分離する

- **URL** は Markdown ファイル名由来の slug。英語 slug のまま変えない（既存リンク・被リンクを壊さないため）。
- **表示タイトル** は frontmatter の `title`。Quartz の FrontMatter transformer は「`title` があればそれ、無ければ `file.stem`（＝英語 slug）」を表示名に採用する。
- この表示名は**ページ見出し (ArticleTitle)** と **Explorer 左ペインのページ名**の**両方**が使う（Explorer のツリーノード `displayName` が `data.title` 由来）。したがって `title` を 1 つ足すだけで両方が同時に日本語化され、URL は不変のまま。
- 運用: 全ページに日本語 1 行 `title` を付ける。**未設定だと英語 slug が見出しに出る**ので、新規作成・rename 時は必ず付ける。日付つき snapshot はタイトル末尾に日付 (YYYY-MM-DD) を残す。用語は用語ルール（広聴AI / LLM grouping / Jigsaw Sensemaker 等）に従う。[[source-code]]より

## Explorer のフォルダ見出しは mapFn で日本語化する

ページ（ファイル）の表示名は `title` で決まるが、分類フォルダ（`concepts` / `entities` / `sources` / `analyses`）の見出しはフォルダ slug のまま残る。これは `quartz.layout.ts` の Explorer `mapFn` で `node.displayName` を上書きして日本語化している。

| フォルダ slug | 表示 |
| --- | --- |
| concepts | 概念 |
| entities | 人物・ツール |
| sources | ソース要約 |
| analyses | 考察・分析 |

Explorer の並び順は同ファイルの `sortFn`（`sortByRecency`、配下ページの最新更新日で新しい順）。[[source-code]]より

## 落とし穴: Explorer の mapFn / sortFn は client 側で再評価される

Explorer に渡した `mapFn` / `sortFn` は、サーバで `.toString()` により文字列化され、client 側で `new Function` によりグローバルスコープで再評価される（`quartz/components/scripts/explorer.inline.ts`）。このため関数は**自己完結**でなければならない:

- **inner named 関数を置かない**。esbuild の `--keep-names` が注入する `__name(...)` 参照が、再評価時に未定義になって壊れる。
- 外部変数を閉じ込めない（object literal と built-in のみ）。
- 実装は top-level の `const 名前 = (引数) => {...}` 形にして Explorer に渡す（`sortByRecency` / `mapFolderLabels` が実例）。

検証は実ビルドで行う: `pnpm build` が通れば直列化は成功、生成 HTML の `data-data-fns` に（日本語は `\uXXXX` エスケープで）関数が埋まる。[[source-code]]より

## 関連ファイル / CI gate

- `quartz.config.ts` — locale=ja-JP、フォント、theme、plugin 構成。
- `quartz.layout.ts` — Explorer の `sortFn` / `mapFn`、各ペインの構成。
- `scripts/check_pages_links.py` — 生成物（`public/`）の内部リンク検査。`deploy-pages.yml` の CI gate。
- `scripts/build_index_txt.py` — frontmatter `summary` から AI 向けカタログ `index.txt` を生成（`title` は使わない。表示用と AI カタログ用は別物）。

二層運用の全体像は [[wiki-driven-workflow]]、コントリビュート手順は [[contributing]] を参照。[[source-code]]より
