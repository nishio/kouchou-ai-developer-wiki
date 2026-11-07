---
title: "チームみらい 2025 参院選「しゃべれるマニフェスト」オープンデータ"
type: source
summary: "nishio が Hugging Face に CC BY 4.0 で公開した、チームみらい 2025 参院選の政策提案 PR 9,688 件 → 課題 18,967 → 意見 21,348 件の広聴AI 分析結果（2 次元座標・20/400 クラスタ・表札・密度・出典 URL・埋め込み・英訳）。kouchou-ai の公開用 artifact とほぼ 1 対 1 に対応し、付箋ズーム・ツリー表示・マンダラートなどの可視化を個人 repo で試す共通データとして使う"
sources:
  - https://huggingface.co/datasets/nishiohirokazu/team-mirai-2025-embeddings
  - https://scrapbox.io/nishio/チームみらい2025参院選「しゃべれるマニフェスト」オープンデータ
---

## 鮮度

- Hugging Face のデータセットページ（README・ファイル一覧・メタデータ）を 2026-11-07 に読んだ。データセットの最終更新は 2026-10-30（英訳の追加）
- 紹介ページは [[nishio]] の Scrapbox（2026-09-09 に Hugging Face への移行を告知、2026-10-30 に英訳を追加）
- 照合した kouchou-ai main は `7253efcc`（2026-11-07）

## 何のデータか

2025 年 7 月の参院選で、チームみらいの「しゃべれるマニフェスト」（AI がインタビューして政策提案の PR を書く仕組み。中身は [[idobata]] のいどばた政策）に届いた提案を、広聴AI で分析した結果。各段の出力を全部残してあるので、後段だけを別の方法でやり直せる。

| 段 | 件数 | 方法 |
|---|---|---|
| 政策提案の PR | 9,688 | 2025-05-15〜07-26 の team-mirai/policy の PR。97.9% は AI インタビュアーの bot が作成 |
| 課題の抽出 | 18,967 | gpt-4o（policy-pr-hub のスクリプト） |
| 意見の抽出 | 21,348 | 広聴AI（gpt-4o-mini）、2025-07-30 実行 |
| 配置とクラスタ | 上位 20・下位 400 | 広聴AI。text-embedding-3-small → UMAP 2 次元 → 2 次元座標の上で k-means 400 → Ward で 20 に併合。表札は gpt-4o-mini |

ほかに 1536 次元の埋め込み 2 種類（広聴AI が UMAP に入れたものと、2025-10 に計算し直したもの）、取り込み可否つきの PR 表、広聴AI の実行設定（全プロンプト・パラメータ・各段のコード）、英訳（`argument_en`・`label_en`・`takeaway_en`、2026-10 にオープンウェイトのモデルで機械翻訳、人手の確認なし）が入っている。

**ライセンスは CC BY 4.0**。元の team-mirai/policy も CC BY 4.0 で、チームみらいの許可を得て公開したと README に明記されている。PR のタイトルなどニックネームが入りやすい列は除いてある。

## kouchou-ai の公開用 artifact との対応

結果 JSON の層分離の第 1 段（PR [#1179](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1179)）で入った `public_result.json` の項目（`packages/analysis-core/src/analysis_core/public_result.py` の `ARGUMENT_KEYS` / `CLUSTER_KEYS`）と、ほぼ 1 対 1 で対応する。

| `public_result.json` | このデータセット |
|---|---|
| 意見 `arg_id` / `argument` / `comment_id` | `arguments.id` / `argument` / `comment_id` |
| 意見 `x` / `y` | `umap_x` / `umap_y` |
| 意見 `cluster_ids` | `cluster_level1` / `cluster_level2`（根のクラスタは補う） |
| 意見 `url` | `pr_url` |
| クラスタ `id` / `level` / `label` / `takeaway` / `parent` / `density_rank_percentile` | `clusters` の同名の列 |
| クラスタ `value` | `num_arguments` |

足りないのは根（level 0）のクラスタだけで、全体の概要文は `pipeline/kouchou-ai-overview.txt` にある。したがって変換スクリプト 1 本で `public_result.json` の形にでき、その形を読む可視化はそのまま本体の公開ビューアの plugin に移しやすい。

## 可視化の題材としての向き不向き

- **付箋ズーム**：意見・座標・クラスタの経路・表札が全部ある。[[open-decisions]] A13 で「先に決める」としていた書き出しの取り決めを、`public_result.json` の形で代用できる。21,348 件なので 1 万件超の表示の検証にもなる
- **ツリー表示（階層リスト）**：20 → 400 → 意見 → 元の PR まで辿れる。`density_rank_percentile` で [#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60) の「濃いクラスタだけに絞る」も試せる
- **マンダラート**（[#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880)）：階層が [20, 400] で、マンダラートの前提 [8, 64] と合わない。公開されている 2 次元座標から [8, 64] でクラスタを切り直す（ここは LLM 不要、表札の付け直しには LLM が要る）か、20 を 8 にまとめる規則を作る必要がある
- **日英の両方で見せられる**：英訳の列があるので、海外の研究者向けにも同じデータで見せられる

## 使うときの注意（README より）

- PR の本文は市民が直接書いたものではなく、AI インタビュアーが会話から書いたもの。課題・意見はさらに 2 回の LLM 抽出を経ている
- 参加者はチームみらいの AI と話すことを選んだ人で、有権者の標本ではない
- `umap_x` / `umap_y` は同じ設定で UMAP をやり直しても再現しない（ライブラリの版と環境で変わる）。公開されている座標とクラスタを基準として扱う
- 英訳は機械翻訳。用語が大事なときは日本語の列を見る

## 位置づけ（2026-11-07 の nishio の方針）

可視化（付箋ズーム・ツリー表示・マンダラートなど）は、このデータを共通の題材にして **nishio の個人 repo で作ってカタログ化し、kouchou-ai 本体に入れるかはそこで試してから決める**。詳細は [[open-decisions]] A13。

## Open Questions

- 個人 repo のカタログの置き場所（repo 名）と、本体 docs の関連研究ページ（PR [#1174](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1174)、未 merge）からのリンクの張り方
- マンダラート用に [8, 64] で切り直した結果を、このデータセットに別の設定として足すか、カタログ側だけに置くか

## Updates

- 2026-11-07: 初版作成
