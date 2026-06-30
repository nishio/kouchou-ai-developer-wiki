---
type: source
summary: "2026-06-29 の Slack #2_開発_広聴ai_アルゴリズム開発で、Embedding 最前線資料の共有をきっかけに、embedding algorithm の見直し、Spherical K-means、Faiss K-means が短く言及された thread"
sources:
  - slack-logs-repository.md
  - slack-niizuma-umap-kmeans-thread-2026-03-18.md
  - niizuma-thread-algorithm-critique.md
  - one-factor-experiment-principle-2026-06-02.md
---

## What it is

2026-06-29 に `#2_開発_広聴ai_アルゴリズム開発` で、ベクトル検索 / embedding の資料共有をきっかけに、現行の embedding / clustering 周辺を見直す可能性が短く出た。[[slack-logs-repository]]より

この source は、採用判断ではなく **次に clean experiment へ切り出すべき候補メモ** として読む。

## Freshness marker

この source の鮮度基準は、**2026-06-30 に `work/slack-logs` を `main@341cf8022d32` まで pull し、mirror の `#2_開発_広聴ai_アルゴリズム開発` を読んだ時点**。

- local source: `work/slack-logs/mirror/slack/C08PX74S5T4.jsonl.gz`
- channel: `C08PX74S5T4` / `2_開発_広聴ai_アルゴリズム開発`
- mirror sync: `synced_at=2026-06-30T04:12:50.909454+00:00`
- mirror window: `2026-06-16T04:12:50.909454+00:00` 〜 `2026-06-30T04:12:50.909454+00:00`
- messages read: channel meta + 6 messages

発言者 ID は `U08J6JR5SNQ` だったが、local `work/slack-logs/mirror/users.json` からは名前解決できなかったため、この page では人名を断定しない。

## Observed thread

2026-06-29 01:56 JST に、SpeakerDeck `【2026年版】 ベクトル検索とEmbedding最前線` へのリンクが共有され、「そろそろ、エンベディングのアルゴリズムを変えてもいいのかもなぁ」という趣旨のコメントがあった。Slack attachment 上では、Encraft #25 生成AI時代の検索設計の登壇資料として表示されていた。[[slack-logs-repository]]より

その後、同じ短い連投で次の語が出た。

- embedding を直接 clustering するには `Spherical K-means` がよさそう、という趣旨
- `Faiss K-means`
- ChatGPT と話すと知らないものが出てくる、という趣旨
- image attachment 1 件と、「この構造は分かりいい」という趣旨の反応

## Interpretation boundary

この thread から言えるのは、**現行 pipeline の clustering / embedding 周辺を見直す候補として Spherical K-means と Faiss K-means が浮上した** ところまでである。

注意点：

- Slack log だけでは、embedding model 自体を変える話なのか、既存 embedding の clustering space / clustering objective を変える話なのかがまだ混ざっている。
- SpeakerDeck 本文はこの source では独立に読んでいない。根拠に使っているのは Slack attachment metadata と Slack message だけ。
- image attachment の内容は未確認。したがって画像の中身を根拠にした主張はしない。
- 採用判断や実装 issue 化はまだ行われていない。

## Relationship

この thread は、過去の [[slack-niizuma-umap-kmeans-thread-2026-03-18]] / [[niizuma-thread-algorithm-critique]] が扱った `UMAP` 後 `k-means` 批判の続きとして読める。ただし、過去の論点は「どの clustering method が正しいか」だけではなく、分析 artifact / 表示 artifact / 説明 artifact を分ける必要性だった。

したがって、Spherical K-means や Faiss K-means も、単純な置換候補ではなく、[[one-factor-experiment-principle-2026-06-02]] の clean experiment へ分解して検証する必要がある。

## Open Questions

- `Spherical K-means` を試す場合、入力は raw embedding、normalized embedding、clustering 用 UMAP 15D〜25D のどれにするか。
- `Faiss K-means` は algorithmic quality の候補なのか、既存 KMeans の高速化 / 大規模化実装なのか。
- 現行の階層構築は KMeans の cluster center を `ward` で merge している。Spherical / Faiss 系へ変えた時、階層 merge の距離や center 表現をどう揃えるか。
- SpeakerDeck 本文を読む必要があるか。Slack 上の候補整理だけなら不要だが、embedding model 更新まで踏み込むなら一次資料として読むべき。

## Updates

- 2026-06-30: 初回作成。`work/slack-logs/main@341cf8022d32` の mirror から、2026-06-29 の Spherical K-means / Faiss K-means 言及を source 化した。
