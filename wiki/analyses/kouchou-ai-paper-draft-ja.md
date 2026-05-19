---
name: kouchou-ai-paper-draft-ja
summary: 広聴AI紹介論文の日本語下書き。まずは問題設定、システム、事例、評価、限界の骨組みを置く
type: analysis
sources:
  - kouchou-ai-paper-draft-strategy.md
  - role-model-papers-polis-birdwatch.md
  - kouchou-ai.md
  - open-decisions.md
---

本ページは、将来的な広聴AI紹介論文の**日本語下書き**である。現段階では完成稿ではなく、主張・節構成・必要証拠を育てるための骨組みとして使う。[[kouchou-ai-paper-draft-strategy]]より

## 仮タイトル案

- 広聴AI: 日本語自由記述を対象としたブロードリスニング支援システムの設計と運用
- 広聴AI: 自治体・政党向け大規模意見分析 OSS の設計と事例
- 広聴AI: 日本語圏におけるブロードリスニング実践のためのシステムと知見

## 0. Abstract

広聴AIは、自治体や政党などが集めた大量の自由記述コメントを、抽出、埋め込み、クラスタリング、可視化を通じて理解しやすい形に変換するブロードリスニング支援システムである。[[kouchou-ai]]より  
本稿では、広聴AIのシステム構成と運用上の設計判断を示し、日本語圏の市民参加・政策対話の文脈でどのような課題に応えるかを論じる。あわせて、Polis / vTaiwan や Birdwatch / Community Notes などの先行事例を参照しつつ、広聴AIの特徴、限界、今後の評価課題を整理する。[[role-model-papers-polis-birdwatch]]より

## 1. Problem Setting

日本の自治体・政党・市民参加の現場では、自由記述コメントを数百件から数万件単位で扱う場面がある。しかし人手で全件を読むことは難しく、単純な集計だけでは論点構造や対立軸が見えにくい。広聴AIは、この問題に対してコメント群から意見地図を生成し、全体像把握と深掘りの両立を支援することを狙う。[[kouchou-ai]]より

### TODO

- 具体的な現場課題を 2-3 例に絞って書く
- 「なぜ既存の要約や単純分類だけでは不十分か」を先行研究と比較して足す

## 2. Related Work

Polis / vTaiwan 系の研究は、大規模オンライン参加を制度や対話プロセスに接続した点を強く扱う。Birdwatch / Community Notes 系の研究は、コミュニティによる注釈やファクトチェックの helpfulness や効果を評価している。[[role-model-papers-polis-birdwatch]]より  
広聴AIは両者の中間に位置し、参加者間の合意形成だけでも、誤情報訂正だけでもなく、**大量自由記述の構造把握を支援する OSS** として位置づけられる。

### TODO

- 日本語圏の自治体参加やパブコメ分析の関連研究を追加
- Talk to the City との関係を書く

## 3. System Overview

広聴AIは、CSV 入力から抽出、埋め込み、階層クラスタリング、可視化までを一連のパイプラインとして提供する。加えて、Web UI と CLI の 2 つの主要利用モードを持つ。[[kouchou-ai]]より

### 3.1 Input and Extraction

自由記述をそのまま扱うのではなく、まず argument / comment 単位へ整形・抽出する設計を取る。

### 3.2 Embedding and Clustering

意味的に近い意見を近傍へ置き、二段階のクラスタリングで全体像と詳細の両方を見やすくする。

### 3.3 Visualization and Sharing

散布図、ツリーマップ、階層ビューなど複数の表現を持つ。共有や限定公開の扱いも設計上の論点である。[[open-decisions]]より

### TODO

- 実際の図を 1-2 枚入れる
- Web UI と CLI の役割分担をもっと明確に書く

## 4. Design Rationale

広聴AIの特徴は、アルゴリズムだけでなく、実運用から生じた設計判断にある。

- 日本語利用を主戦場にしていること
- Web UI と CLI の二層運用
- 散布図を残すか縮退させるかが未解決であること
- LocalLLM や plugin system のように将来拡張を見据えた経路を持つこと

この節では、成功だけでなく未解決論点も含めて書く必要がある。[[open-decisions]]より

### TODO

- どの判断が field requirement 由来で、どの判断が技術的制約由来かを分ける

## 5. Case Studies

この節には、代表的な運用事例を 1 つか 2 つ入れる。Polis 論文が UberX 事例を背骨にしているのと同様、広聴AIでも本文を支える canonical case が必要である。[[role-model-papers-polis-birdwatch]]より

### TODO

- 公表可能な事例候補を列挙する
- その事例で入力件数、利用者、意思決定との接続を整理する

## 6. Evaluation

評価は今後の要強化点である。少なくとも次のどれかを置く必要がある。

- 利用者が論点構造を把握するまでの時間短縮
- 人手コーディングや単純要約との比較
- 運営者が重要クラスタを見つけるまでの工数削減
- 可視化ごとの理解しやすさ

Birdwatch 系のロールモデルにならい、効果が限定的だった点も含めて書ける形が望ましい。[[role-model-papers-polis-birdwatch]]より

### TODO

- 定量評価が難しい場合の定性評価デザインを考える
- どのログやアンケートを今後取るべきか整理する

## 7. Limitations

- 評価データがまだ十分ではない
- 散布図やクラスタリングは解釈依存性がある
- 公開可能な事例データに制約がある
- 日本語圏に特化した設計は国際一般化に限界がある

## 8. Conclusion

広聴AIは、日本語圏の自由記述を対象としたブロードリスニング支援システムとして、実務的にも研究的にも意味のあるケースになりうる。今後は、事例記述だけでなく評価設計を強めることで、国際的な civic tech / HCI / digital democracy 議論への接続可能性を高めたい。

## Open Questions

- canonical case として何を置くか
- 定量評価をどこまでやるか
- 国内発表を先に挟むか、英語投稿を先に狙うか

## Updates

- 2026-05-19: 初回作成
