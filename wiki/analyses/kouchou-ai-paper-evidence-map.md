---
name: kouchou-ai-paper-evidence-map
summary: "広聴AI紹介論文で想定する主張ごとに、既存の根拠、追加で必要な証拠、未解決ギャップを対応付けた表"
type: analysis
sources:
  - kouchou-ai-paper-draft-ja.md
  - kouchou-ai-paper-draft-strategy.md
  - role-model-papers-polis-birdwatch.md
  - kouchou-ai.md
  - meeting-minutes.md
  - open-decisions.md
---

本ページは、[[kouchou-ai-paper-draft-ja]] の各節で何を主張し、それを何で支えるかを対応付けるための evidence map である。論文草稿は書き始めると抽象論に流れやすいので、**主張、既存根拠、追加で要る証拠、ギャップ** を先に切り分ける。[[kouchou-ai-paper-draft-strategy]]より

## 使い方

- 「今すぐ書ける節」と「証拠不足で保留すべき節」を分ける
- source / code / case / figure の不足を可視化する
- 日本語草稿を育てる時も、将来の英語投稿で必要になる証拠水準を意識する

## Claim Map

| Claim ID | 主張 | 既存根拠 | 追加で必要な証拠 | 現状評価 |
|---|---|---|---|---|
| C1 | 日本の自治体・政党文脈では、大量自由記述を人手だけで読むのが難しい | [[kouchou-ai]]、[[meeting-minutes]] | 公表可能な運用事例、件数感、関係者コメント | 中 |
| C2 | 広聴AIは日本語自由記述を対象に、抽出→埋め込み→階層クラスタリング→可視化の一連経路を提供する | [[kouchou-ai]] | 実画面または出力図、最新版 code 由来の図 | 強 |
| C3 | 広聴AIの価値はアルゴリズム単体ではなく、運用プロセスと共有導線を含む点にある | [[kouchou-ai]]、[[open-decisions]]、[[meeting-minutes]] | 代表事例ごとの実運用フロー、誰がどこで使ったか | 中 |
| C4 | Web UI と CLI の二重構成は、非専門家利用と研究・開発利用の両立のために生まれた | [[kouchou-ai]] | 実利用者像、モードごとの利用場面 | 中 |
| C5 | 散布図、クラスタ、静的共有、限定公開などの設計は、実務上の tradeoff から生まれている | [[open-decisions]]、[[meeting-minutes]] | 具体的な失敗例、比較 UI、意思決定の時系列 | 中 |
| C6 | 広聴AIは Polis / vTaiwan のような制度接続型研究とも、Birdwatch のような評価研究とも接続可能だが、同一ではない | [[role-model-papers-polis-birdwatch]] | 関連研究節の明文化、差分整理の文章 | 中 |
| C7 | 広聴AIの最初の論文は、システム紹介＋事例研究を主軸にするのが現実的である | [[kouchou-ai-paper-draft-strategy]] | 候補 venue と required contribution の比較 | 弱 |
| C8 | 広聴AIの効果を論じるには、理解速度、論点把握、運営工数、再利用性などの評価軸が必要である | [[role-model-papers-polis-birdwatch]]、[[kouchou-ai-paper-draft-ja]] | 評価プロトコル、比較対象、ログ取得方法 | 弱 |
| C9 | 散布図依存、評価不足、公開可能データ制約は、現時点の主要な限界である | [[open-decisions]]、[[meeting-minutes]] | 制約の具体例、何が公開できないかの整理 | 中 |

## Figure Candidates

論文として説得力を出すには、本文より先に図候補を持っておいた方がよい。

1. **System overview 図**
   CSV / extraction / embedding / clustering / visualization / sharing の流れ
2. **Usage modes 図**
   Web UI と CLI の分岐、利用者像、生成物の違い
3. **Representative output 図**
   散布図、クラスタ一覧、ツリーマップのいずれか
4. **Case study process 図**
   コメント収集から意思決定・公開までの運用フロー
5. **Evaluation design 図**
   人手読解、単純要約、広聴AI 利用の比較軸

## Evidence Gaps

現時点で特に不足しているのは次の 4 点である。

### G1. 公表可能な canonical case

Polis 論文の UberX 事例に相当する、本文の背骨になる事例がまだ固定されていない。[[role-model-papers-polis-birdwatch]]より

### G2. 効果検証の設計

Birdwatch 系のように「何が改善したか」を測る評価軸がまだ設計段階にない。[[role-model-papers-polis-birdwatch]]より

### G3. 図表の原稿化

現状の wiki は言語的整理が中心で、論文図としてそのまま使える図の候補やキャプション案が未整備である。

### G4. Related Work の掘り下げ

Polis / vTaiwan と Birdwatch は押さえたが、日本語圏の参加型民主主義、パブコメ分析、対話可視化の関連研究はまだ薄い。

## 今の段階で書けること / 書けないこと

### 今すぐ比較的書ける

- 問題設定の粗い説明
- システム構成の概要
- Web UI / CLI の二重構成
- 設計判断の一部
- 限界の自覚的整理

### まだ危うい

- 効果があったという強い主張
- 代表事例を用いた具体的叙述
- 先行研究との差分の精密な議論
- 投稿先に最適化した contribution framing

## 次の作業候補

1. canonical case 候補を 3 つまで列挙するページを作る
2. evaluation 指標候補を洗い出すページを作る
3. related work を civic tech / HCI / computational social science に分けて追加調査する
4. 日本語下書きの `Related Work` と `Evaluation` 節に、この evidence map を反映する

## Open Questions

- 事例公開の倫理・契約上の制約を誰が確認できるか
- 定量評価なしでも国内論文として成立するのか
- 英語投稿を狙う場合、どの claim を strongest contribution とみなすか

## Updates

- 2026-05-19: 初回作成
