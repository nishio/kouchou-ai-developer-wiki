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
- **マンダラート**（[#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880)）：階層が [20, 400] で、マンダラートの前提 [8, 64] と合わない。11-07 の nishio の案は **8 分割を、各マスが意見 1 枚になるまで繰り返す**（8, 64, 512, … と降りる）。21,348 件なら log8 ≈ 4.8 なので 5 段前後
  - 広聴AI の既定の階層づくり（最細の段を k-means で切り、Ward で上へ併合する）では、親 1 つあたりの子の数が揃わない。このデータでも上位 20 の子の数は 1〜38（中央値 18.5）。段数を [8, 64, 512, …] と指定しても「子は 8 つ以下」は保証されない
  - したがって、上から順に「8 つ以下に割る」を再帰的に繰り返す分割が要る。子が 8 以下になった節は意見そのものをマスに並べる。木の深さは枝ごとに変わってよい
  - 内部の節は約 3,000 個になるので、全部に LLM で表札を付けると数が多い。深い段は中心に最も近い意見をそのまま表札にする手もある
  - 入れ子の 3×3 は、そのまま拡大縮小できる格子になる。付箋ズームの配置を UMAP 座標でなくこの格子にする案とも重なる
- **日英の両方で見せられる**：英訳の列があるので、海外の研究者向けにも同じデータで見せられる

## 使うときの注意（README より）

- PR の本文は市民が直接書いたものではなく、AI インタビュアーが会話から書いたもの。課題・意見はさらに 2 回の LLM 抽出を経ている
- 参加者はチームみらいの AI と話すことを選んだ人で、有権者の標本ではない
- `umap_x` / `umap_y` は同じ設定で UMAP をやり直しても再現しない（ライブラリの版と環境で変わる）。公開されている座標とクラスタを基準として扱う
- 英訳は機械翻訳。用語が大事なときは日本語の列を見る

## 位置づけ（2026-11-07 の nishio の方針）

可視化（付箋ズーム・ツリー表示・マンダラートなど）は、このデータを共通の題材にして **nishio の個人 repo で作ってカタログ化し、kouchou-ai 本体に入れるかはそこで試してから決める**。詳細は [[open-decisions]] A13。

## 個人 repo のカタログ

2026-11-07 に [nishio/broadlistening-visualizations](https://github.com/nishio/broadlistening-visualizations)（public、コードは MIT、デモは GitHub Pages）を作った。

- 変換スクリプトでこのデータを `public_result.json` の形にし、可視化はそれを読む
- 最初の項目は **意見マンダラート**（[デモ](https://nishio.github.io/broadlistening-visualizations/mandalart/)）。1536 次元の埋め込み（cosine）を上から k-means（k=8）で割り続け、5,848 節・最大 7 段（段ごとの節の数は 1, 8, 64, 509, 2811, 2279, 170, 6）。表札は各まとまりの中心に最も近い意見（LLM 不使用）で、上の段ほど「〜が不足している」のような一般的な文になる。9×9 と 3×3（スマホ）、日英の切替、最下層から元の PR へのリンク
- カタログには付箋ズーム（未着手）と階層リスト（本体に入った）も最終確認日つきで載せた

## Open Questions

- 本体 docs の関連研究ページ（PR [#1174](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1174)、未 merge）から個人 repo のカタログへのリンクの張り方
- マンダラート用に 8 分割を再帰的に繰り返した木を、このデータセットに別の設定として足すか、カタログ側だけに置くか。深い段の表札を LLM で付けるか代表意見で済ませるか

## Updates

- 2026-11-07: 初版作成
- 2026-11-07: マンダラートについて nishio の案（8 分割を意見 1 枚になるまで繰り返す）と、既定の階層づくりでは子の数が揃わないこと（このデータで 1〜38）を追記
- 2026-11-07: 個人 repo nishio/broadlistening-visualizations を作り、意見マンダラートの試作を公開したことを追記
