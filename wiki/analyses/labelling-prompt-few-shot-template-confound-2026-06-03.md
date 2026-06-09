---
type: analysis
summary: "2026-06-02 LLM grouping 400 件 corpus の human preference A/B (none vs setwise_refine) を label_only で 7 件回した結果、7/7 で setwise_refine が winner。当初この結果を verbosity confound として整理したが、6/8 と 6/9 の再調査で『どちらが verbose か』を逆に誤認していたと判明。実際は refine_none (= top-level refinement なし = merge_labels そのまま) が verbose、refine_setwise (sibling-aware refinement) が shorter。よって v1 結果は『refinement on > refinement off』を捉えており、verbosity 削減効果と sibling-awareness 効果が refinement 内で混じっている、というのが正確な構造。MERGE_LABELLING_PROMPT few-shot の templating 問題は引き続き有効"
sources:
  - label-quality-human-preference-improvement-plan-2026-06-03.md
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
---

> **2026-06-09 大幅補正**: 本ページの 2026-06-03 初版と 2026-06-04 補正は、`refine_none` と `refine_setwise` の verbose / concise の direction を**逆に取り違えていた**。再調査で実際は `refine_none` (refinement なし = merge_labels そのまま) が verbose、`refine_setwise` (sibling-aware refinement) が shorter であり、user の "短い候補が勝つ 7/7" は実際は "refine_setwise が勝つ 7/7" だった。したがって "verbosity confound" の framing 自体が誤りで、v1 結果は実は「refinement on > refinement off」という意味のある signal を捉えていた。詳細は下の「2026-06-09 補正」セクションを参照。本ページの旧版本文は履歴のため残す

## 2026-06-09 補正

### 正しい length ordering

cluster 1_1 で確認:

| labelling_run | label | 長さ |
|---|---|---|
| `refine_none` | AI技術による顧客体験の向上と業務効率化の推進 | **長い** |
| `refine_setwise` | AIによる顧客体験と業務効率の向上 | 中 |
| `refine_short` | AIによる顧客体験向上 | 短い |

`refine_none` mode は **top-level refinement を実行しない** mode で、merge_labels 段の出力をそのまま top-level label として採用する。merge_labels は MERGE_LABELLING_PROMPT (few-shot 例 `AI技術の導入による意見分析の効率化への期待`) に強く誘導されて `AI技術による…の推進` 形に収束しているため、`refine_none` の labels が verbose。

`refine_setwise` は sibling-aware に rewrite するプロセスで、結果として verbose な merge_labels を整理する。length 制約は無いが、sibling と差別化するための rewrite が自然に冗長を削る方向に働く。

`refine_short` は更に `max_label_length=18` を加えて、より短く縮める。

### v1 結果の正しい解釈

[human-pairwise-label-preference-experiment-2026-06-02](human-pairwise-label-preference-experiment-2026-06-02.md) の v1 bundle (none vs setwise_refine) に対する nishio の 7 件回答は:

- 7/7 で `refine_setwise` が winner、confidence 全 3
- "短い候補が勝つ" のは事実だが、その「短い候補」は `refine_setwise`、「長い候補」は `refine_none`
- nishio の free text "他は大体短い方がいい" は「短い方が好み」という意味で正しいが、その preference は `refine_setwise` への preference と同じ

つまり v1 結果は **「sibling-aware refinement (setwise) > no refinement (none)」** を 7/7 で示している。

これは meaningful signal だが、純粋な sibling-awareness 効果ではない:

- refinement on vs off で、(a) sibling-awareness と (b) merge_labels の verbose 表現を rewrite する効果、の **両方が同時に動いている**
- nishio の preference が (a) なのか (b) なのかは、この比較では切り分けられない

### 仕切り直しの方針 (再々補正後)

「verbosity confound」は誤った framing だったので撤回。代わりに以下:

#### 動線 A: MERGE_LABELLING_PROMPT few-shot の templating を直す (current `main`)

これは引き続き有効。`refine_none` mode が verbose なのは MERGE_LABELLING_PROMPT few-shot 例「AI技術の導入による意見分析の効率化への期待」が `〜による〜の〜` 構文を焼き付けているから。few-shot を topic-neutral / 構文多様にすると、refine_none の output が改善され、ひいては refine_setwise の input も改善される。

具体修正案 (A1 + A2 が現実的):

- A1. example を topic-neutral にする: `〜による〜の〜` 形を出力例から外し、内容語で始まる名詞句スタイルに差し替える
- A2. 明示的な禁止: 「`〜による〜の〜` のような定型構文を避ける」「短い名詞句で」を prompt 本文に追加
- A3. 多様な few-shot: 構文の違う複数例を並べる
- A4. zero-shot: example を捨てて instruction だけにする

#### 動線 B (旧): `setwise_refine` の default に length 制約 → **撤回**

旧分析では「setwise_refine が verbose に elaboration している」と誤認していたためこの動線を提案した。実際は setwise_refine は既に shorter な方向に rewrite しているので、default length 制約は不要。`refine_short` は別 mode として残しておけば十分。

#### 動線 D (新): sibling-awareness 単独効果を測る比較を組む

v1 結果 (setwise > none) は refinement on/off の合成効果なので、純粋な sibling-awareness 効果を測るには「sibling-aware refinement vs non-sibling-aware refinement (両方同じくらいの length)」が必要。

`refine_balanced` / `refine_contrast` mode が既存 artifact にあるが、これらが何をする mode なのか未確認。それを先に確認してから A/B 設計する。

#### 動線 C (旧): `none` vs `setwise_refine_short` で組み替え → **棄却**

旧分析では length 統制になると思ったが、実際は none (長い) vs short (最も短い) で length gap が更に広がる。confound 改善にならず、棄却。

## 旧分析の本文 (参考用)

旧 framing と修正後を読み比べたい人のために、本文をそのまま残す。direction 誤認のある内容なので、読む時は上の補正と突き合わせること。

### (旧) 結論

> 2026-06-02 corpus 上の `factor_under_test=labelling_process` (none vs setwise) 比較は、**2 つの独立した issue が confound していた**ため、`labelling_process` 単独の効果を測れない設計になっていた。実験は採用判断材料にはせず、いったん reset。
>
> 2 つの issue (詳細は下):
> 1. **INITIAL/MERGE labelling few-shot template**: 全 labelling 出力に `〜による〜の〜` 構文と "AIによる" prefix を焼き付けている ← Issue 1 自体は有効、ただし焼き付く先は `refine_none` mode の labels (= merge_labels)
> 2. **setwise_refine の length 制約なし**: refinement step が elaboration して "AI技術による…の推進" のような長い form に書き換えてしまう ← **逆だった**。setwise_refine は短くする側

### (旧) 観測 (direction 誤認あり)

> 7/7 で「短い候補」が winner、confidence は全て 3 (高)。勝った 7 件は すべて `AIによる…` で始まる短い名詞句、負けた 7 件は すべて `AI技術による…の推進` / `…への取り組み` のような長めの接頭辞 + 動作名詞

事実関係 (label の形) は正しい。誤りは「短い `AIによる…` = `refine_none`、長い `AI技術による…の推進` = `refine_setwise`」とした direction で、実態は逆。

### (旧) Issue 2 の "elaboration" 説明 → 撤回

旧版の "setwise_refine が base label を AI技術による…の推進 のように展開する" は誤り。実態は base merge_labels が AI技術による…の推進 形で、setwise_refine がそれを短く rewrite する。

## 一般化されるルール (この件から抽出される)

direction 誤認の話とは別に、以下 2 つの一般則は今回の件全体から抽出できる:

1. **A/B 評価する前に、両 candidate の実際の output を spot-check する**。candidate name (none/setwise/short) から style を推測せず、artifact CSV を直接確認する。私はこれをやらず direction を取り違えた
2. **few-shot example はラベル品質の天井になる**。MERGE_LABELLING_PROMPT の `AI技術の導入による意見分析の効率化への期待` は構文を強く誘導しており、refinement なしの merge_labels 出力を verbose にしている。labelling 品質改善は process / sibling-awareness より先に prompt example の見直しから入る方が見返りが大きい

## Open Questions

- ~~`refine_balanced` / `refine_contrast` mode は何をする refinement か。sibling-awareness 単独効果を測る A/B に使えるか~~ → 2026-06-09 確認、4 つすべて sibling-aware の variant で non-sibling-aware は不在。sibling-awareness 単独 isolate には新 mode (D-3) が要る
- MERGE_LABELLING_PROMPT few-shot を topic-neutral に変えた時、refine_none output だけ改善されるのか、refine_setwise output も追従して改善されるのか
- v1 結果 (setwise > none) は refinement on/off の効果だが、これを「採用根拠」にするのは妥当か、それともあくまで exploratory にとどめるか
- v2 (setwise vs short) の結果は length cap on/off だけが factor だが、nishio の v1 free text「短すぎて情報減りすぎ困る」が cluster 1_8 で再現するか、それとも 18 cap でも全 cluster 許容範囲か

## Next Actions

優先順:

1. **v2 bundle (24 件) を nishio が回答** — [raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/bundles/label_preference_ab.html](../../raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/bundles/label_preference_ab.html) を開いて answer。最低でも `label_only` 8 件、できれば全 24 件 (3 contexts × 8 clusters)
2. **動線 A (MERGE_LABELLING_PROMPT few-shot 修正 PR)** — v2 と独立に進められる。`work/kouchou-ai/` の topic branch で `packages/analysis-core/src/analysis_core/prompts/__init__.py:91` 周辺の few-shot 例を topic-neutral + 短さ指示付きに差し替える。issue #881 (label 品質改善 tracking) の child として進めるか、独立 issue にするかは要相談
3. **動線 D-3 (新 mode `refine_independent` 追加)** — sibling-awareness を単独 isolate するなら必要。各 label を sibling 文脈を見ず単独で refine する mode を追加し、setwise vs independent を比較する。コード追加 + 再 labelling が要るので、v2 結果を見てから判断
4. **judge calibration** — v2 で集めた human preferences を再現する judge を作る (本来の [[label-quality-human-preference-improvement-plan-2026-06-03]] の step 4)。v2 回答数が揃ってから着手

## Updates

- 2026-06-09: 大幅補正。`refine_none` と `refine_setwise` の verbose / concise direction を逆に取り違えていた誤りに気づき、framing を「verbosity confound」から「v1 は実は refinement on/off の効果を捉えていた」に修正。動線 B (setwise_refine に length 制約) は誤認に基づく提案だったので撤回、動線 C (none vs short で組み替え) も length gap が広がるだけなので棄却。代わりに動線 D (sibling-awareness 単独効果を測る、`refine_balanced` / `refine_contrast` の確認から) を追加。動線 A (MERGE_LABELLING_PROMPT few-shot 修正) は引き続き有効
- 2026-06-04: (誤認に基づく補正、その後 2026-06-09 で撤回) refinement step を読み直し、verbosity confound の真の構造を 2 つの独立 issue の合成と整理。動線を 3 つに拡張
- 2026-06-03: 初版。nishio による sibling_label_set 設計批判から始まり、3 文脈すべてに同じ prompt few-shot template 由来の冗長度 confound があると判明したため、現実験を仕切り直し決定として記録
