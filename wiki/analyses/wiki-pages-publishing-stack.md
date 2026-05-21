---
type: analysis
summary: "developer-wiki の GitHub Pages 配信は、現状の MkDocs adapter より Quartz を第一候補にした方が wiki の記法と公開体験が揃いやすい"
sources:
  - wiki-pages-tooling-observation-2026-05-21.md
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

## Open Questions

- Quartz 本体をこの repo に vendor するか、publish 用の別 repo / subtree に分けるか
- `wiki/log.md` をそのまま公開面に出すか、内部向け導線として扱うか
- source ページを public に出し切るか、analysis / concept だけ前面に出すか

## Updates

- 2026-05-21: 初版作成
- 2026-05-21: 実装まで反映し、Quartz vendor / `pnpm build` / Pages workflow 差し替え / MkDocs 撤去まで進んだ current state を追記
