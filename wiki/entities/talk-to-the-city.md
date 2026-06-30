---
name: talk-to-the-city
summary: "TTTC — kouchou-ai の上流。AI Objectives Institute 発、現在 archived"
type: entity
sources:
  - meeting-minutes.md
  - note-annotakahiro-broadlistening-resources-2025-02-05.md
  - meeting-cartographer-idobata-boundary-2026-06-30.md
  - public-web-kouchouai-tttc-lineage-2026-06-30.md
---

## What

**Talk to the City (TTTC)** は AI Objectives Institute が開発した [[broadlistening|ブロードリスニング]] ツール。[[kouchou-ai]] はその Scatter 版からフォーク。

公開説明では、TTTC は「広聴AIの前史」と「TTTC direct / adjacent な国内事例」の両方に出てくる。DD2030 公式ページは、2024 年の東京都知事選 / 日本テレビ衆院選報道 / `シン東京2050` を TTTC / AI 意見分析の流れとして示し、2025-03-16 の広聴AI OSS 公開へつなげている。したがって、広聴AIの confirmed case と TTTC direct / pre-kouchou lineage は分けて説明する。[[public-web-kouchouai-tttc-lineage-2026-06-30]]より

## バリエーション

- **TTTC Scatter** — 散布図ベース。kouchou-ai はここから出発
- **TTTC Turbo** — グラフィカルなノードパイプラインエディタを試みたが UX 的に頓挫
- **tttc-light-js** — 現行上流。固定パイプライン、散布図なし
- **オリジナル TTTC リポジトリは 2025-08-01 に archived**

議事録では、オリジナル TTTC が archived になり、現在の上流として `tttc-light-js` が見られている一方、`tttc-light-js` は scatter を持たないと整理されている。Jigsaw Sensemaker は Polis 型 data に強く、広聴AIのような自由記述 survey data には `tttc-light-js` の方が素直ではないか、という見立ても出ている。[[meeting-cartographer-idobata-boundary-2026-06-30]]より

## kouchou-ai がフォークした理由

[[meeting-minutes]] 2025-05-28 で [[nasuka]]：

> ノンエンジニアでも扱えるようにアプリ化する際に、コードとしてはかなり差分が大きくなる

TTTC は CLI ツール。チームあんのが SaaS 風のプレビュー／共有 UI を被せたことで分岐が大きくなり、フォークが現実的になった。詳細経緯は [[nishio]] の note: https://note.com/nishiohirokazu/n/nb37adf96fe50

## 設計面での示唆

- **Turbo の挫折** → kouchou-ai は customization を JSON/YAML config に寄せる方針（[[plugin-system]]）
- **tttc-light-js が散布図を捨てた** → 一方 kouchou-ai では散布図維持／削除が議論されており、[[nishio]] は「少なくとも 2026-09 書籍版リリース時点までは温存し、より良い可視化が見つかれば併用→デフォルト切替もあり得る」というスタンス（詳細は [[open-decisions]] A1）
- **同じ TTTC lineage でも成果物が違う** → TTTC Scatter / kouchou-ai は地図・scatter・drill-down の reader experience を持つ。tttc-light-js / Turbo / Sensemaker 的な route は LLM 直接分類や固定 pipeline に寄るため、公開説明では「TTTC 系譜」と「kouchou-ai の current UI」を同一視しない。

## Updates

- 2026-06-30: [[public-web-kouchouai-tttc-lineage-2026-06-30]] を反映し、DD2030 公式ページ上の TTTC → 国内前史 → 広聴AI OSS 公開の公開 lineage を追加。公開事例では TTTC direct / pre-kouchou lineage と広聴AI confirmed case を分ける。
- 2026-06-30: [[meeting-cartographer-idobata-boundary-2026-06-30]] を反映し、tttc-light-js は現行上流だが scatter なし、Sensemaker とは data fit が異なるという切り分けを追記。
- 2026-05-17: 初回作成
- 2026-05-25: 散布図維持側を「顧客がいる」から、[[nishio]] 本人の時間軸ベースのスタンス（書籍版までは温存／良い代替が出れば併用→切替）に表現を訂正
