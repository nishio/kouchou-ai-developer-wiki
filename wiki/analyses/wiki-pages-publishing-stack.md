---
type: analysis
summary: "developer-wiki の GitHub Pages 配信は、現状の MkDocs adapter より Quartz を第一候補にした方が wiki の記法と公開体験が揃いやすい"
sources:
  - wiki-pages-tooling-observation-2026-05-21.md
  - wiki-maintenance-observation-2026-05-25.md
  - https://gist.github.com/nishio/35d604f23a39aca369ac74db8b65b655
---

この repo の `wiki/` は、普通の docs site というより **wikilink と相互参照を前提にした知識ベース** として育っている。したがって GitHub Pages 配信も「Markdown を HTML にするだけ」ではなく、**wiki 的なナビゲーションをどこまで自然に出せるか** で選ぶ方がよい。[[wiki-pages-tooling-observation-2026-05-21]]より

## 現状の MkDocs 構成をどう見るか

現状は `wiki/` をそのまま MkDocs に食わせているのではなく、`scripts/build_pages_docs.py` で `.pages/docs/` に変換コピーし、その後 `mkdocs build` している。つまり MkDocs は本質的には **後段 renderer** であり、authoring 体験は別途スクリプトで補正している。[[wiki-pages-tooling-observation-2026-05-21]]より

これは最低限の公開には十分だが、repo の運用が育つほど次のズレが目立つ。

- `[[wikilink]]` が native ではないので rewrite script に依存する
- backlink / graph / folder listing のような wiki 向け導線が標準では弱い
- 「index を手で育てる知識ベース」と「docs navigation config」の発想が少しずれる

## Quartz を第一候補にする理由

Quartz は Obsidian Flavored Markdown と wikilink を default で扱い、Explorer / Backlinks / Graph など **知識ベース型 wiki の公開体験** を最初から持つ。`wiki/` 側の書き方を renderer に合わせて曲げるより、renderer を `wiki/` の書き方に寄せた方が repo の意図に合う。[[wiki-pages-tooling-observation-2026-05-21]]より

特にこの repo では、

- `wiki/index.md` を人手で編集してカタログを育てる
- source / concept / analysis を wikilink で横断する
- `log.md` を時系列の知識生成履歴として残す

という運用が中核にある。これは「製品 docs」より「digital garden / research wiki」に近く、Quartz の得意領域と噛み合う。[[wiki-driven-workflow]] / [[wiki-pages-tooling-observation-2026-05-21]]より

## 実装方針

切り替えるなら、まず **`wiki/` を source of truth のまま維持する** ことを崩さない方がよい。`wiki/` を別の `content/` へ再コピーするのではなく、Quartz の `--directory` で `wiki/` を直接読む構成が第一候補。[[wiki-pages-tooling-observation-2026-05-21]]より

そのうえで現実的な段取りは次になる。

1. Quartz 導入時も `wiki/` 配下の Markdown はそのまま使う
2. GitHub Pages workflow は Python + MkDocs から Node + Quartz build へ切り替える
3. `baseUrl` と公開対象の見せ方を調整する
4. 移行確認が済んだら `mkdocs.yml` / `requirements-pages.txt` / `scripts/build_pages_docs.py` を撤去する

2026-05-21 の実切替ではこの段取りをそのまま踏み、**Quartz が `wiki/` を直接読む構成** と **GitHub Pages workflow の Node/pnpm 化** まで反映した。結果として、配信系の source of truth が `wiki/` からぶれない構成になった。[[wiki-pages-tooling-observation-2026-05-21]]より

## Graph 表示の扱い

Quartz の Graph は wiki 的な横断導線として有用だが、この repo では `wiki/index.md` と `wiki/log.md` が全ページの hub になりやすい。2026-05-25 の更新では、page 自体は公開したまま、local / global graph から `index` と `log` の node だけを除外した。`quartz.layout.ts` から `Component.Graph({ localGraph: { removeSlugs: [...] }, globalGraph: { removeSlugs: [...] } })` を渡し、Graph 側で slug filter する実装である。[[wiki-maintenance-observation-2026-05-25]]より

この判断は「`log.md` を隠す」ではなく、graph を概念間の関係把握に寄せるための表示チューニングである。`index` / `log` は Explorer、URL、本文リンクからは引き続き到達できる。[[wiki-maintenance-observation-2026-05-25]]より

## Project Site の subpath 方針

GitHub Pages の project site (`/kouchou-ai-developer-wiki/`) でリンクが壊れた時は、まず Quartz の `baseUrl` 設定と generated URL を見る。Quartz 4 は project-site hosting を想定しており、この repo でも `baseUrl: "nishio.github.io/kouchou-ai-developer-wiki"` が正規の支点である。[[wiki-pages-tooling-observation-2026-05-21]]より

したがって、root だけ `<base>` を入れるような HTML-level workaround は避ける。`<base>` はブラウザ全体の相対 URL 解決を変えるため、Quartz の static HTML / SPA / search / explorer がそれぞれ持つ相対 URL 前提と衝突しやすい。2026-05-28 の修正では、`Head.tsx` を upstream 相当へ戻し、`scripts/check_pages_links.py` で build 後の `public/` を `/kouchou-ai-developer-wiki/` 配下として機械検査する形にした。[[wiki-pages-tooling-observation-2026-05-21]]より

## Scrapbox/Gist 手順との差分

Scrapbox から辿った旧 Gist は、任意の Obsidian Wiki を Quartz + GitHub Pages へ移植するために、`wiki/` を編集用、`content/` を Quartz 入力用として分ける方式だった。これは private/public の分離、alias 解決、Quartz へ渡す Markdown の正規化が必要な一般用途では筋がよい。[[wiki-pages-tooling-observation-2026-05-21]]より

一方、この developer-wiki では `wiki/` がすでに公開 source of truth であり、`index.txt`、`log.txt`、frontmatter lint、wikilink lint も同じ tree を直接見る。ここで `content/` を足すと、公開のためだけに第二の source tree が生まれ、LLM 向け運用との drift が増える。したがってこの repo では `quartz build -d wiki` を維持し、source 側 lint と生成物リンク検査で守る方がよい。[[wiki-pages-tooling-observation-2026-05-21]]より

この差分は新 Gist `Quartz + GitHub Pages project site で Wiki を公開する設計メモ` に外部化した。結論は、`wiki/` direct と `wiki/ -> content/` 変換は project-site subpath 対応のための上下関係ではなく、authoring / publishing の責務分離をどこに置くかの選択である。新 Gistより

## Open Questions

- Quartz 本体をこの repo に vendor するか、publish 用の別 repo / subtree に分けるか
- `wiki/log.md` は graph から除外したが、公開ページとしては残している。将来、内部向け導線へ寄せるかは未決
- source ページを public に出し切るか、analysis / concept だけ前面に出すか

## Updates

- 2026-05-21: 初版作成
- 2026-05-21: 実装まで反映し、Quartz vendor / `pnpm build` / Pages workflow 差し替え / MkDocs 撤去まで進んだ current state を追記
- 2026-05-25: graph から `index` / `log` を除外する表示チューニングと、その意図を追記
- 2026-05-28: GitHub Pages project-site の subpath 対応は upstream Quartz の `baseUrl` に寄せ、`<base>` patch ではなく生成物リンク検査で守る方針を追記
- 2026-05-28: Scrapbox / 旧 Gist の `wiki/ -> content/` 方式と、この repo の `wiki/` direct 方式の選び分けを追記し、新 Gist へ外部化した
