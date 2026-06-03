---
name: talk-to-the-city
summary: "TTTC — kouchou-ai の上流。AI Objectives Institute 発、現在 archived"
type: entity
sources:
  - meeting-minutes.md
  - note-annotakahiro-broadlistening-resources-2025-02-05.md
---

## What

**Talk to the City (TTTC)** は AI Objectives Institute が開発した [[broadlistening|ブロードリスニング]] ツール。[[kouchou-ai]] はその Scatter 版からフォーク。

## バリエーション

- **TTTC Scatter** — 散布図ベース。kouchou-ai はここから出発
- **TTTC Turbo** — グラフィカルなノードパイプラインエディタを試みたが UX 的に頓挫
- **tttc-light-js** — 現行上流。固定パイプライン、散布図なし
- **オリジナル TTTC リポジトリは 2025-08-01 に archived**

## kouchou-ai がフォークした理由

[[meeting-minutes]] 2025-05-28 で [[nasuka]]：

> ノンエンジニアでも扱えるようにアプリ化する際に、コードとしてはかなり差分が大きくなる

TTTC は CLI ツール。チームあんのが SaaS 風のプレビュー／共有 UI を被せたことで分岐が大きくなり、フォークが現実的になった。詳細経緯は [[nishio]] の note: https://note.com/nishiohirokazu/n/nb37adf96fe50

## 設計面での示唆

- **Turbo の挫折** → kouchou-ai は customization を JSON/YAML config に寄せる方針（[[plugin-system]]）
- **tttc-light-js が散布図を捨てた** → 一方 kouchou-ai では散布図維持／削除が議論されており、[[nishio]] は「少なくとも 2026-09 書籍版リリース時点までは温存し、より良い可視化が見つかれば併用→デフォルト切替もあり得る」というスタンス（詳細は [[open-decisions]] A1）

## Updates

- 2026-05-17: 初回作成
- 2026-05-25: 散布図維持側を「顧客がいる」から、[[nishio]] 本人の時間軸ベースのスタンス（書籍版までは温存／良い代替が出れば併用→切替）に表現を訂正
