---
name: kj-method-broadlistening-framing-2026-05-25
summary: "広聴AIを川喜田二郎の野外科学 / KJ法に接続すると、中心は要約ではなく `渾沌から公共的仮説を立ち上げる装置` になる。書籍 13.2.6 の `KJ法プロンプト` は prompt の話に留まらず product 設計原則として読み直せる"
type: analysis
sources:
  - gpt-kawakita-kj-method-broadlistening-2026-05-25.md
  - broad-listening-book-extractions.md
  - broadlistening.md
  - public-ui-requirements-for-broadlistening.md
---

[[gpt-kawakita-kj-method-broadlistening-2026-05-25]] は、広聴AIを川喜田二郎 / KJ法に接続するブレストである。  
要約すると、広聴AI を **「行政のための要約ツール」ではなく「公共圏のための KJ 的な意味生成装置」** として再定義する論考になる。  
これは技術論ではなく **目的論** であり、current `kouchou-ai` の設計判断にどう効くかをここで整理する。

## 1. 「KJ法プロンプト」を product 設計原則として読み直す

[[broad-listening-book-extractions]] は書籍 13.2.6 を引いて「KJ法 / 表札 という日本語専門用語をプロンプトに載せると labeling 品質が上がる」と整理していた。これは **prompt engineering tips** として読まれてきた。

しかし [[gpt-kawakita-kj-method-broadlistening-2026-05-25]] が示すのは、KJ法は単なるラベリング技法ではなく **混沌から公共的仮説を立ち上げる方法論** であり、prompt に「KJ法」と書くだけでは KJ法的 product にはならないということだ。  
つまり「KJ法 prompt を使う」ことと「KJ法的設計原則を product に通す」ことは別問題である。

書籍 13.2.6 を出発点にするなら、その背後の方法論を product 全体に展開する道が残されている。

## 2. KJ法的に見た広聴AIの 6 つの設計原則

[[gpt-kawakita-kj-method-broadlistening-2026-05-25]] が提示する原則を current `kouchou-ai` の状態に重ねると、達成度はまちまちである：

| 原則 | 内容 | current `kouchou-ai` の現状 |
| --- | --- | --- |
| 原文に戻れる | ラベル・クラスタ・要約から原コメントに辿れる | scatter / hierarchy view から原文 drill-down は実装されている。`report.html` でも保たれる |
| 既存カテゴリに当てはめない | 行政カテゴリへの自動分類は「混沌を黙らせる」 | 現状そういう自動分類はしていない。`analysis_mode=llm_grouping` でも自由クラスタ |
| 表札は AI が確定しない | クラスタ名は人間が吟味する仮説 | label 編集 UI はない。AI 生成のラベルが事実上の確定値 |
| 少数・矛盾・分類困難を残す | `unresolved_cards.md` 的な「次の問いの種」 | exhaustive partitioning が前提で、「収まらない」を表現する schema がない |
| 論点の構造を示す | 「結論」より対立・補完・因果の図解 | scatter + 階層 tree で構造は出る。対立・因果は出ない |
| 現場に返却する | 一回限りの分析で終わらせない | analysis 単位は基本 one-shot。継続関与は product 外 |

つまり「原文復帰」と「既存カテゴリ非適用」は達成、「表札の人間吟味」「少数残存」「対立・因果構造」「継続関与」は未達である。  
この棚分けは、product としての未来の枝を整理しやすくする。

## 3. ohki-shingo の公開UI要件との重なり

[[public-ui-requirements-for-broadlistening]] が整理した公開UI 7 要件と、KJ法的原則は部分的に重なる：

- **原文に戻れる** — ohki-shingo 要件の「個別意見へ drill-down」と同じ
- **少数残存** — 「少数派の声を埋もれさせない」要件と対応
- **編集可能性** — 「自治体・市民が結果を訂正できる」要件と対応する可能性

つまり KJ法的設計原則は、ohki-shingo の議論を **理論的に裏付ける枠組み** として使える。  
[[ohki-discussion-reflection-2026-05-25]] が「散布図互換の技術論から公開UI の説明責務への問い直し」と整理した構図に、本ブレストは「公開UI の説明責務とは KJ法的な公共仮説生成のことだ」という解像度を加えうる。

## 4. 「広く聴く」と「深く聴く」の緊張は product にも露出する

[[gpt-kawakita-kj-method-broadlistening-2026-05-25]] は、行政の広聴で働く 4 つの圧力を挙げている：

- 「多くの人が言っていること」を重視する
- 「既存施策に対応しやすい意見」を拾う
- 「説明しやすいクラスタ名」に整える
- 「例外的・少数的な声」をノイズとして扱う

これらは current `kouchou-ai` の設計判断にも直接効く：

- `analysis_mode=llm_grouping` は **既存カテゴリでない自由クラスタ** を作る方向で、原則を守っている
- `濃いクラスタ抽出` 機能（`digitaldemocracy2030/kouchou-ai` README）は **多数派攻撃に対する防御** として明示されており、KJ法的に重要
- 一方、`auto_cluster_defaults`（[[auto-cluster-defaults]]）の `∛n` 経験値は **視認性ベース** で決まっており、「分かりやすさ」優先のバイアスを構造的に持つ

書籍 13.4.2 が脚注で「シルエットスコア等の自動最適化を採用していない理由：利用者が見たい粒度を選べる方が実用的」と書いているのは、まさにこの緊張を product に露出させない設計判断だが、KJ法的には「見たい粒度」自体が探索対象になりうる。

## 5. 「LLM に KJ法やらせて」では届かない

[[gpt-kawakita-kj-method-broadlistening-2026-05-25]] の核心は、

> 単に LLM に「KJ法で整理して」と投げるのは避けるべきです。それでは過程がブラックボックス化し、KJ法で重視される「発想の根拠・プロセス・産物が見える」性質が失われます。

である。これは [[jigsaw-llm-grouping-experiment-output-2026-05-25]] が観測した「LLM grouping は top-level label では強いが scatter 互換は悪い」「分類根拠が `reason` 列にしか残らない」状況にも当てはまる。

LLM grouping の次の改良点としては、`reason` を意思決定に乗る形式で残す（cluster ごと、boundary case ごと、unresolved case ごと）ことが、KJ法的観点では重要になる。  
これは [[jigsaw-llm-grouping-implementation-plan]] の延長で `analysis_capabilities` の output に明示できる。

## 6. 設計判断への落とし込み（優先度低）

current `kouchou-ai` の implementation backlog に対しては、本ブレストの結論はすぐ実装に落ちる種類ではない。優先度を整理すると：

- **schema 拡張**（`representative_docs`、`boundary_cases`、`unresolved_cards`、`edge reasons`）は中期。`analysis-core` の plugin contract に乗せられる。
- **label 編集 UI** は短期にも価値あるが、view plugin 設計（[[public-ui-requirements-for-broadlistening]]）が固まってから。
- **対立・因果構造表示** は [[graph-visualization-proposal-2026-05-25]] の bridge edge `relation type` と接続できる：`contrast` `cause-effect` `same claim across clusters` は KJ法の「対立・補完・因果」と直接対応する。
- **継続関与** は product 単体の問題ではない。書籍リリース・実証実験との接続で考える話。

[[development-priority-roadmap-2026-05-23]] / [[strategic-development-order-2026-05-23]] の優先順位（Windows 配布・既知バグ・運用基盤を上位）に変更を求めるものではない。  
ただし、研究テーマ層の「広聴AI は何を最適化しているのか」という問いに対し、**「公共的仮説の生成を最適化している」** という答えの候補を 1 つ追加する。これは [[kouchou-ai-paper-draft-strategy]] / [[kouchou-ai-paper-draft-ja]] の論文執筆にも効く視座である。

## 7. graph-visualization-proposal との接続

[[graph-visualization-proposal-2026-05-25]] の bridge edge `relation type`（same claim / adjacent issue / cause-effect / contrast / boundary）は、KJ法の「対立・補完・因果」と直接対応する。  
つまり、graph visualization 提案は **KJ法的な図解化を product に落とす具体的設計** として読める。可視化と方法論が偶然合っている。

これは co-design の好機である：  
- KJ法的原則は **何を見せるべきか** の指針
- graph visualization 提案は **どう見せるか** の手段

両者を独立に成立する設計案として持ちながら、合流させる時にどちらかが歪まないかを確認するのがよい。

## Open Questions

- 「収まらない／揺れる／反例」を表現する schema を current `analysis-core` に入れる場合、`cluster_id` の exhaustive partitioning と両立できるか。`cluster_id = unresolved` のような sentinel を入れるか、別フィールドにするか。
- 「現場への返却」を product 単体で扱うのは無理がある。一方、書籍リリース（2026-09）と実証実験を組み合わせる場で、`kouchou-ai` がこの原則をどう体現するかは未整理。
- KJ法的な「結論より論点の構造」を current report 形式（HTML / Web UI）にどう落とすか。今は cluster list と scatter という flat 構造で、対立・補完・因果の関係は表現できていない。
- 鈴木健の「ブロードリスニングは用途ごとに欲しいインサイトが違う」（[[kensuzuki-broad-listening-insight-types-2025-11-29]]）と本ブレストの「公共的仮説生成」は、どちらが上位の問題設定か。前者は産業構造論、後者は方法論。

## Updates

- 2026-05-25: 川喜田二郎 / KJ法 に接続するブレストを、product 設計原則の棚として整理。既存の「KJ法 prompt」言及（書籍 13.2.6）からは方法論側に展開され、ohki-shingo の公開UI要件、jigsaw LLM grouping、graph visualization 提案と複数地点で接続する
