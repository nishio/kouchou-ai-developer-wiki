---
title: "Quartz Explorer を更新新しい順にする実装と client 再評価の落とし穴"
type: analysis
summary: "developer-wiki の Explorer を ABC 順から更新新しい順へ。sortFn/mapFn/filterFn は client で再評価されるため date を index に残す必要があり、inner named 関数は esbuild の __name 注入で壊れる"
---

## 何をしたか

公開 wiki（Quartz）左サイドバーの Explorer を **ABC 順（フォルダ優先＋アルファベット）から更新新しい順**に変更した（2026-10-14, developer-wiki main）。変更は 2 ファイル。

- **`quartz.layout.ts`**: `sortByRecency` を追加し、両レイアウト（content / list）の `Component.Explorer({ sortFn })` に渡す。フォルダは**配下ページの最新更新日で代表**（部分木の最大 date）、同点は `localeCompare`（numeric）でアルファベット・タイブレーク。
- **`quartz/plugins/emitters/contentIndex.tsx`**: client 用 index（`static/contentIndex.json`）から `date` を削除していた処理（`delete content.date`）をやめ、**保持**するようにした。これが無いと client 側ソートで日付が参照できない。

「更新日」の供給元は `quartz.config.ts` の `defaultDateType: "modified"`（`CreatedModifiedDate` の priority = frontmatter → git → filesystem）。wiki ページは日付 frontmatter を持たないので、**実質 git の最終コミット時刻**になる。`linkify_github_refs` や日本語 title 一括付与のような**一括コミットは多数ページを同一日に揃える**ため、その分は同点となり辞書順にフォールバックする（仕様どおりの挙動）。

Explorer の**フォルダ見出し日本語化（`mapFn`）**と**全ページ日本語 title 付与**は別作業であり、sort とは独立（同じ `quartz.layout.ts` に `mapFn` として同居するが役割が違う）。[[wiki-driven-workflow]]より

## なぜ 2 段構えが要るか（Explorer の仕組み）

この版の Quartz Explorer は、**ソート/フィルタ/マップを server ではなく client で行う**。

1. server は `sortFn`/`filterFn`/`mapFn` を **`.toString()` で直列化**し、各ページの `data-data-fns` 属性に JSON で載せる（`quartz/components/Explorer.tsx`）。
2. client は `new Function("return " + str)()` で**グローバルスコープで再評価**し（`quartz/components/scripts/explorer.inline.ts`）、`static/contentIndex.json` から `FileTrieNode` の trie を作って適用する。

つまり「どの階層のどのページを、どの順で出すか」は**ブラウザ側の計算**であり、そこで参照できるデータは `contentIndex.json` に載っている分だけ。date でソートしたいなら、emitter が date を落とさず client に届ける必要がある——これが上の 2 ファイル目の理由。

## 既知の落とし穴（将来 Explorer の fn を触る人向け）

- **sortFn / mapFn / filterFn に inner named 関数・外部参照を書かない**。esbuild の `--keep-names` が named function / 名前付き変数に代入した arrow へ `__name(...)` を注入するが、client の `new Function` スコープには `__name` が存在しない。結果 `ReferenceError: __name is not defined` で **Explorer 全体が落ちる**（ページは出るが左ツリーが空になる）。再帰は**反復（明示スタック）**で、helper を使わず object literal と built-in だけで書く。server(Node) 側には `__name` があり build は通ってしまうので、build 成功だけでは気づけない。
- date を使うなら、`contentIndex.tsx` の `delete content.date` をやめて client に date を残す（デフォルトは RSS 用途だけ残して削除する）。date は JSON 直列化で ISO 文字列になるので、fn 内では `new Date(node.data.date).getTime()` で扱う。
- **検証は client 相当で行う**。`pnpm build` 後、`public/*.html` の `data-data-fns` から `sortFn` 文字列を取り出し、`new Function("return "+s)()` で**グローバル評価して throw しないこと**と、サンプルノードで期待順になることを確認する。Node スコープでそのまま呼ぶと `__name` があるため素通りしてしまう。

## 関連

[[wiki-pages-publishing-stack]] / [[wiki-pages-tooling-observation-2026-05-21]] / [[wiki-driven-workflow]]
