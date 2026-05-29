---
name: zenn-llm-as-a-judge-rubric-evaluation-2026-05-29
type: source
summary: "Ubie Tech Blog の LLM-as-a-Judge / ルーブリック評価記事。抽象的な 1-5 点採点ではなく、true/false 可能な criteria に分解し、重要度ごとの points と negative criteria を持たせると、再現性と改善点の特定が上がるという実務向け整理"
url: https://zenn.dev/ubie_dev/articles/llm-as-a-judge-rubric-evaluation
sources:
  - https://zenn.dev/ubie_dev/articles/llm-as-a-judge-rubric-evaluation
  - https://openai.com/ja-JP/index/healthbench/
---

## What it is

Ubie Tech Blog の「LLM-as-a-Judge とルーブリック評価」。2025-12-19 公開、2026-05-27 更新の記事で、LLM 出力の品質評価を「主観的な 1-5 点採点」「具体的な評価基準つき採点」「ルーブリック評価」の 3 手法で比較している。[[zenn-llm-as-a-judge-rubric-evaluation-2026-05-29]]より

記事の実験では、電子レンジ故障相談への 2 応答を Gemini 2.5 Pro judge で各 50 回評価し、ルーブリック評価では各 criterion を `true/false` で判定し、criteria ごとの points を合算して得点率を出している。[[zenn-llm-as-a-judge-rubric-evaluation-2026-05-29]]より

## Key Points

### 1. 総合点ではなく criteria に分解する

ルーブリック評価の中心は、「この応答は良いか」を直接 1-5 点で聞くのではなく、評価対象が満たすべき具体条件を複数の criteria に分け、それぞれを `true/false` で判定すること。記事の例では、安全注意、電源リセット、チャイルドロック確認、デモモード確認、空焚き防止、マグネトロン言及、問い合わせ時の型番確認などが個別 criterion になっている。[[zenn-llm-as-a-judge-rubric-evaluation-2026-05-29]]より

### 2. positive / negative criteria と重みを併用する

criteria には正の points だけでなく、危険な提案や文脈と矛盾する提案への負の points も置かれている。たとえば分解提案や、ライトが点灯している状況と噛み合わないブレーカー確認は negative criteria として扱われる。[[zenn-llm-as-a-judge-rubric-evaluation-2026-05-29]]より

### 3. 再現性と解釈性が上がるが、設計コストは高い

記事の結果では、ルーブリック評価は 50 回すべてで criteria 判定が一致し、応答 1 は 83%、応答 2 は 33% と差が明確に出た。強みは再現性と、どの criterion が不足しているか分かる解釈性。弱みは criteria 数に応じて評価コストが上がることと、`true/false` で明確に判断できる criteria を設計する手間である。[[zenn-llm-as-a-judge-rubric-evaluation-2026-05-29]]より

### 4. HealthBench 型は「用途ごとの custom rubric」

OpenAI HealthBench は、会話ごとに医師が作成した custom rubric criteria と points を持たせ、モデル回答を model-based grader で採点する構成である。ここで重要なのは、汎用的な「良い回答」採点ではなく、具体的なシナリオに応じて含めるべき要素・避けるべき要素を criteria 化している点。[[zenn-llm-as-a-judge-rubric-evaluation-2026-05-29]]より

## Relevance To kouchou-ai

ラベル品質 judge でも、現状の `一貫性 / 具体性 / 網羅性 / 区別性` のような抽象軸をそのまま 1-5 点で採点すると、judge の主観や self-evaluation バイアスが残る。広聴AIのクラスタラベル評価では、抽象軸をさらに「見えた材料にない主張をしていない」「上位 2-3 軸を落としていない」「sibling と区別できる」のような binary criteria に分解するのがよい。[[label-judge-mechanism-2026-05-25]]より

## Open Questions

- ラベル品質で `true/false` に落とせる criteria はどこまでか。特に「代表性」「読みやすさ」は境界が曖昧になりやすい
- criteria 判定を 1 criterion 1 call にするか、1 cluster 1 call で全 criteria を JSON 返却させるか。前者は記事の厳密性に近いがコストが高い
- human judge と LLM judge の一致率をどの程度まで見てから regression test として使うか

## Updates

- 2026-05-29: 初版作成。Ubie Tech Blog のルーブリック評価記事から、ラベル品質 judge に転用できる要点を整理
