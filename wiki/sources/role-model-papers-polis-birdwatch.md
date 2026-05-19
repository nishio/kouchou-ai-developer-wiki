---
name: role-model-papers-polis-birdwatch
summary: 広聴AI紹介論文のロールモデルとして参照しやすい vTaiwan / Polis と Birdwatch / Community Notes 論文の要点
type: source
sources:
  - https://ideas.repec.org/p/osf/socarx/xyhft.html
  - https://arxiv.org/abs/2104.07175
  - https://arxiv.org/abs/2307.07960
---

広聴AIを将来的に英語圏へ紹介する論文を考えるとき、少なくとも 2 系統のロールモデルがある。1 つは **大規模熟議・合意形成プロセス** を記述する `vTaiwan: An Empirical Study of Open Consultation Process in Taiwan`、もう 1 つは **コミュニティベースの注釈・ファクトチェック機構** を分析する Birdwatch / Community Notes 論文群である。

## vTaiwan / Polis 系

`vTaiwan: An Empirical Study of Open Consultation Process in Taiwan`（2018, SocArXiv）は、vTaiwan を単なるツール紹介ではなく、**背景、プロセス、使われる OSS 群、UberX 事例、限界**まで含めて記述している。[[role-model-papers-polis-birdwatch]]より

この論文が広聴AIにとって参考になる点は次の通り。

- **ソフトウェア単体ではなく運用プロセスを書く**。Polis 1 個ではなく、オンラインとオフラインを接続した consultation process として描いている
- **制度接続を書く**。参加した行政職員や政策変更可能な主体が process に組み込まれている点を明示している
- **代表事例を 1 つ深く書く**。UberX を canonical case として使い、抽象論だけにしない
- **限界と今後の改善も書く**。成功物語だけで閉じず、feasible model としての条件や制約を残している

広聴AI論文でも、単に「コメントをクラスタリングする OSS」ではなく、**自治体・政党・市民参加のどの運用課題をどう支えるか** まで書かないと、Polis 系の論文に比べて学術的な輪郭が弱くなる。

## Birdwatch / Community Notes 系

`Community-Based Fact-Checking on Twitter's Birdwatch Platform`（2021/2022 系）は、Birdwatch に集まった note と rating を分析し、**どのような note が helpful と見なされるか**、**影響力の大きいアカウント相手では合意形成が難しくなる**こと、**分極化や opinion speculation の課題** を示している。[[role-model-papers-polis-birdwatch]]より

`Did the Roll-Out of Community Notes Reduce Engagement With Misinformation on X/Twitter?`（CSCW 2024）は、Community Notes 導入後の engagement 変化を大規模データで検証し、**導入そのものでは misleading post への engagement 低下を十分確認できず、初期拡散に対しては遅すぎる可能性がある**と述べている。[[role-model-papers-polis-birdwatch]]より

この系統が広聴AIに示す示唆は次の通り。

- **アルゴリズムの社会的効果を検証する**。仕組みの存在だけでなく、何が改善し、何が改善しなかったかを問う
- **helpfulness / consensus / latency のような評価軸を立てる**。UI や可視化の良し悪しを主観で済ませない
- **失敗や限界を論文化できる**。効果が限定的でも、それ自体が知見になる

広聴AIでも、論文にするなら「意見地図を作れた」だけでは弱く、**参加者理解、運営工数、合意形成、対立把握、再利用性** のどこに measurable な改善があったかを置く必要がある。

## 広聴AI論文への含意

この 2 系統を並べると、広聴AI論文には少なくとも次の 3 類型が考えられる。

1. **システム／プロセス論文** — 日本の自治体・政党・市民参加の現場に向けて、広聴AIがどのような運用プロセスを実現したかを書く
2. **評価論文** — コメント要約・クラスタリング・可視化・公開導線が、理解や意思決定にどんな影響を持ったかを検証する
3. **設計判断論文** — Scatter / cluster / extraction / plugin system / LocalLLM 等の設計上の tradeoff を、実運用を通して整理する

Polis 論文に寄せるなら **制度と運用の記述** が強くなり、Birdwatch 論文に寄せるなら **評価設計と限界分析** が強くなる。

## Open Questions

- 広聴AIの最初の論文は、システム紹介、事例研究、効果検証、設計判断のどれを主軸に置くべきか
- 日本の事例データをどこまで匿名化・再利用可能な形で論文に載せられるか
- Birdwatch 系のような定量評価を行うなら、広聴AIでは何を outcome とみなすか

## Updates

- 2026-05-19: 初回作成
