---
type: source
summary: "UMAP / k-means の seed 固定と再現性要求の経緯 — 2025-03 の実装、2025-05 の再現性不満、2025-07 の再評価、2026-02 の PR #810"
sources:
  - source-code.md
  - slack-kouchouai-algorithm-dev.md
  - weekly-log-2026-05-06.md
---

## What it is

`seed` 固定の経緯を、`work/kouchou-ai/` の履歴確認と `oss_weekly_reporter` 由来の GitHub / Slack ログから束ねた source。  
対象は主に `UMAP(random_state=42)` と `KMeans(..., random_state=42)`、およびそれを後から見直した `PR #810` の文脈。

この論点は「なぜ 42 なのか」という数値選択より、**なぜ再現性を欲したのか**、そして **なぜ後から並列性重視へ再評価したのか** を追う方が実態に近い。[[source-code]] / [[slack-kouchouai-algorithm-dev]]より

## Timeline

### 2025-03-04: seed 固定済みの `hierarchical_clustering.py` が repo に現れる

`work/kouchou-ai/` の履歴では、commit `0e37543` (`remove submodule`) の時点で `server/broadlistening/pipeline/steps/hierarchical_clustering.py` に

- `UMAP(random_state=42, n_components=2)`
- `KMeans(n_clusters=initial_cluster_num, random_state=42)`

がすでに入っている。少なくとも **2025-03-04 には seed 固定が実装状態として存在していた**。ただし、この commit message 自体からは固定理由は読めない。[[source-code]]より

### 2025-05-14: 「同じ入力でも結果が揺れる」という不満が前面化

Slack では `2025-05-14` に、

- 「同じデータ、同じバージョンでも結果に再現性がない」
- 「最初できた結果が良かったのに、もう一度作れない」
- 「ここまで再現性がないと非科学的」

という実務的な不満が明示されている。  
その直後に tokoroten が「原因はおそらく分かったのでチケットを切った」として Issue `#514` を共有している。[[slack-kouchouai-algorithm-dev]]より

同時期の GitHub issue 群では、

- `#513` 「確率的挙動がある箇所にはランダムシードを設定して結果を固定する」
- `#514` 「機械学習関連は seed を使っているので、なお揺れる原因は extraction 並列実行や入力順ではないか」
- `#515` 「UMAP の結果がレポート出力ごとに異なり、見た目がかなり変わってしまう」

という並びになっており、**seed 固定の背景には再現性要求と見た目の安定化要求があった** と読める。[[weekly-log-2026-05-06]]より

### 2025-05-14: ただしその場で「seed 固定でも完全再現はできない」認識も出ている

同日の Slack では nasuka が、

- OpenAI API の `seed` 固定でも決定的出力は保証されない
- extraction の結果自体が毎回変わりうる
- 順序固定はやる価値があるが、それでも完璧には再現しない

と補足している。  
つまりこの時点で既に、**後段の seed 固定だけでは再現性問題は解けない** という理解も存在していた。[[slack-kouchouai-algorithm-dev]]より

### 2025-05: 「UMAP を固定・使い回したい」要求が出る

同じ 2025-05-14 の Slack では、

- 「最初の1000件で UMAP を作ってマップを固定する」
- 「一度作った UMAP をいろんなレポートで使い回したい」

という話も出ている。  
これは seed 固定と同じ方向を向いた要求で、**比較可能性や見た目の安定性を強く欲していた** ことを示す。後の Issue `#515` の「別のレポートの UMAP を使い回す」とも連続している。[[slack-kouchouai-algorithm-dev]]より

### 2025-07-27: 「前段がランダムなのに後段だけ固定する意味は薄い」という再評価

アルゴリズム開発チャンネルでは `2025-07-27` に tokoroten が、

- `random_state` を外せば UMAP の処理に並列化が効く
- 前段の extraction ですでにランダム性がある
- 後段で seed 固定をする必要はないのでは

と問題提起している。  
これに対し nishio も「一般的なユースケースではシードの固定はしないだろうから外しても良い」と反応している。ここで論点は、**再現性のための固定** から **並列性を失うわりに得るものが薄い固定** へ転換している。[[slack-kouchouai-algorithm-dev]]より

### 2026-02-25 〜 2026-02-28: Issue `#809` と PR `#810` でオプション化案へ

Issue `#809` と PR `#810` では、

- `random_state=42` は UMAP の並列化を暗黙に無効化している
- upstream の LLM / embedding がすでに非決定的なので、厳密再現性の実益は小さい
- ただし embedding 再利用のようなケースでは再現性オプションが必要かもしれない

という整理になっている。  
PR `#810` の提案は「固定を全面撤廃」ではなく、

- デフォルトは `random_state=None` で並列化
- `enable_reproducibility=true` で従来の `random_state=42` を復元
- admin UI からも切り替え可能

という **再現性をオプションへ後退させる** ものだった。[[weekly-log-2026-05-06]]より

## Related Pages

- 解釈整理は [[umap-seed-history]]
- 背景にある UMAP / 2D clustering への不満は [[slack-algorithm-themes]]
- 現行コード上の `hierarchical_clustering` 実装は [[source-code]]
- 現時点の warning 許容判断は [[gotchas]]

## Open Questions

- `random_state=42` が最初に入った理由は追えるが、**なぜ 42 なのか** 自体の明示記録は今回のソース群からは見つかっていない
- `0e37543` より前の submodule 側履歴や当時の PR コメントを掘れば、導入時の会話が追加で見つかる可能性がある

## Updates

- 2026-05-18: `seed` 固定と `PR #810` の前史を、コード履歴・GitHub issue/PR・Slack から束ねて source 化
