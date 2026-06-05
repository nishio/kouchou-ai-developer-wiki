---
type: analysis
summary: "2026-06-02 LLM grouping 400 件 corpus の human preference A/B (none vs setwise) を label_only で 7 件回した結果、全て『短い候補』が勝った。当初は labelling prompt の few-shot 例『AIによる業務効率の大幅向上とコスト効率化』が原因と整理したが、再調査で実は (1) INITIAL/MERGE labelling 段の few-shot template、(2) setwise_refine の length 制約なしによる elaboration、という 2 つの独立した issue が confound していたと判明。さらに length 制約付きの setwise_refine_short variant が既に存在していたことも分かり、仕切り直しの選択肢を 3 つに整理し直した"
sources:
  - label-quality-human-preference-improvement-plan-2026-06-03.md
  - human-pairwise-label-preference-experiment-2026-06-02.md
  - clustering-labeling-comparison-corpus-2026-06-02.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
---

> **2026-06-04 補正**: 本ページの初版 (2026-06-03) は、verbosity confound の根本を「INITIAL/MERGE labelling few-shot」1 点に集約していたが、refinement step を読み直したところ実は **2 つの独立した issue** が重なっていたと分かった (詳細は下の「補正」セクション)。「仕切り直しの方針」も A/B/C の 3 択に拡張した。一般化されるルールはそのまま有効。

## 結論

2026-06-02 corpus 上の `factor_under_test=labelling_process` (none vs setwise) 比較は、**2 つの独立した issue が confound していた**ため、`labelling_process` 単独の効果を測れない設計になっていた。実験は採用判断材料にはせず、いったん reset。[[label-quality-human-preference-improvement-plan-2026-06-03]] の Plan セクションはこの reset を受けてアーカイブ扱いになる。

2 つの issue (詳細は下):
1. **INITIAL/MERGE labelling few-shot template**: 全 labelling 出力に `〜による〜の〜` 構文と "AIによる" prefix を焼き付けている
2. **setwise_refine の length 制約なし**: refinement step が elaboration して "AI技術による…の推進" のような長い form に書き換えてしまう。`setwise_refine_short` variant は既に存在し `max_label_length=18` を持っている

## 観測

[[llm-grouping-400-tree-label-corpus-2026-06-02]] を baseline corpus に、[[human-pairwise-label-preference-experiment-2026-06-02]] の方針で label_only 文脈で 7 件 (cluster 1_1〜1_7) の blind A/B を実施した結果:

- 7/7 で「短い候補」が winner、confidence は全て 3 (高)
- 勝った 7 件は **すべて `AIによる…` で始まる短い名詞句**、負けた 7 件は **すべて `AI技術による…の推進` / `…への取り組み` のような長めの接頭辞 + 動作名詞**
- nishio による free text: "他は大体短い方がいい" / "ここだけ（cluster 1_8）情報減りすぎ"

つまり `none` と `setwise` の差は意味的な distinguishability ではなく、出力ラベルの冗長度に集約されていた。

## 根本原因 (補正後)

### Issue 1: INITIAL/MERGE labelling few-shot template

`packages/analysis-core/src/analysis_core/prompts/__init__.py` の base labelling prompt が、構文を強く誘導する例を 1 つだけ与えていた。

INITIAL_LABELLING_PROMPT (`__init__.py:67`):

```
"label": "AIによる業務効率の大幅向上とコスト効率化"
```

MERGE_LABELLING_PROMPT (`__init__.py:91`):

```
"label": "AI技術の導入による意見分析の効率化への期待"
```

問題は 2 重:

1. **構文テンプレ**: どちらも `[topic word] による [abstract noun] の [verbal noun]` 形。LLM はこのスキーマをコピーする
2. **トピック語の二重露出**: corpus が AI 主題なので、example の "AI" がそのまま prefix として再出力される。気候政策 corpus なら "気候政策による…" になっていたはず

これは `none` / `setwise` 両方の base label に共通して焼き付く template。両者で **共通**しているので A/B の差は生まないが、両方が "AIによる" prefix で始まるという意味でラベル一般の天井を下げている。

### Issue 2: setwise_refine の length 制約なし

`packages/analysis-core/src/analysis_core/steps/hierarchical_label_refinement.py:137-163` の refinement prompt は **zero-shot** (few-shot 例なし)。ただし mode によって length 制約の有無が異なる。

- `setwise_refine`: 長さに関する指示なし
- `setwise_refine_short`: `max_label_length` 文字以内、見出しとして scan しやすく、の指示あり

今回の bundle は `none` (refinement なし、短い base label そのまま) vs `setwise_refine` (refinement あり、length 制約なし、LLM が自由に elaboration) を比較していた。後者は base "AIによる業務効率化" を "AI技術による業務効率化と競争力向上の推進" のように展開する。

結果として A/B で観測された "短い vs 長い" の差は、**sibling-awareness の効果ではなく refinement 段階での elaboration 有無**を測っていた。これが 7/7 で「短い候補」が勝った真の構造。

### `setwise_refine_short` が既存していたこと

[llm-grouping-400-tree-label-corpus-2026-06-02](../sources/llm-grouping-400-tree-label-corpus-2026-06-02.md) の labelling_runs には `refine_short` が含まれており、`max_label_length=18` の sibling-aware refinement が既に生成済みだった。A/B bundle 作成時にこれを candidate に含めず `none` vs `setwise_refine` を選んだ判断 (現 `scripts/build_label_preference_bundle.py` の hard-coded pair) が、verbosity confound を招いた**実装上の選択ミス**でもある。

## sibling_label_set / label_with_representatives も同じ問題

3 文脈すべてに同じ confound が乗っている (Issue 1 + 2 の合成)。

- **sibling_label_set**: focal label の bundle に加えて、その labelling run で生成された **兄弟ラベル全体** が表示される。`none` 候補の bundle は「全部短い `AIによる…` セット」、`setwise` 候補の bundle は「全部長い `AI技術による…の推進` セット」になり、focal label の良し悪しではなくラベル集合の文体を比較することになる
- **label_with_representatives**: 評価軸 (representatives がラベルを支えているか) より先に focal label 自身のまだるっこしさが目に入り、評価できない

したがって 3 文脈をいくら回しても、現在の candidate pair (`none` vs `setwise_refine`) では「refinement step の elaboration 有無 + base prompt の templating」の合成効果を測るだけ。

## 仕切り直しの方針 (補正後)

issue が 2 つに分かれたので、対応も 3 つの独立した動線になる。

### 動線 A: INITIAL/MERGE labelling few-shot を直す (current `main`)

`packages/analysis-core/src/analysis_core/prompts/__init__.py` の few-shot example を topic-neutral / 多様 / 短さ指示付きに差し替える PR。

修正方向 (PR 内で組み合わせる):

- A1. example を topic-neutral にする: `〜による〜の〜` 形を出力例から外し、内容語で始まる名詞句スタイルに差し替える
- A2. 明示的な禁止: 「`〜による〜の〜` のような定型構文を避け、内容語で始める短い名詞句にする」「20 文字程度を目安にする」を prompt 本文に追加
- A3. 多様な few-shot: 1 例だと模倣されるので、構文の異なる複数例を並べる
- A4. zero-shot: example を捨てて instruction だけにする

A1 + A2 が現実的。範囲が広く効き、refinement の有無に関わらず base label の templating を下げる根本対策。ただし `none` vs `setwise_refine` の verbosity gap 自体は別 issue なので残る。

### 動線 B: `setwise_refine` の default に length 制約を入れる (WIP branch)

`codex/remaining-experiment-artifacts-2026-05-29` worktree の `packages/analysis-core/src/analysis_core/steps/hierarchical_label_refinement.py` で、`setwise_refine` mode にも `setwise_refine_short` 相当の length constraint を default で適用する。あるいは `setwise_refine` を deprecate して `setwise_refine_short` に統合する。

これで A/B 比較の verbosity confound を直接解消できる。ただし WIP branch がまだ main に統合されていないため、PR は WIP branch 内の改修になる。

### 動線 C: 既存 artifact で candidate pair を組み替える (即実行可能)

`raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` 内の既存 `setwise_refine_short` artifact (`labelling:hierarchical_8_40_refine_short`, `max_label_length=18`) を使い、`scripts/build_label_preference_bundle.py` の candidate pair を `none` vs `setwise_refine_short` に差し替えて bundle を再生成する。

- コード変更不要 (build script の hard-coded pair を 1 箇所変えるだけ)
- 既に生成済みの label を使う
- 「length を統制した状態で sibling-aware refinement に効果があるか」を最短で測れる
- 旧 corpus を fully terminated とせず、partial 利用する形になる (manifest の status をこれに合わせて更新)

3 つは独立に進められる。コスト最小 → C、根本対策 → A、A/B 設計を直す → B。組み合わせると、A + (B or C) が最も clean。

## 旧 corpus の扱い

`raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/` は **terminated** として manifest に明示する。

- 既に保存した 7 件の `human_preferences.jsonl` は **exploratory record** として保持。`labelling_process` の優劣根拠にはしないが、「旧 prompt 下で冗長度が支配的だった」証拠としては有効
- 残り 17 件 (sibling_label_set / label_with_representatives) は埋めない。同じ confound を踏むだけなので
- bundle (`bundles/label_preference_ab.*`) も再生成しない

## 一般化されるルール

この件から二つの一般則が抽出できる:

1. **labelling_process を A/B 評価する前に、両者が生成するラベルが prompt 由来のテンプレ収束を共有していないか確認する**。共有していると、process 比較の意味が消える
2. **few-shot example はラベル品質の天井になる**。example より良い / 短い / 多様な出力は LLM から自然には出てこない。labelling 品質改善は process / sibling-awareness より先に prompt example の見直しから入る方が見返りが大きい

## Open Questions

- prompt 修正後の再実験では、`none` vs `setwise` 自体を残すか、もっと根本に近い factor (prompt few-shot のスタイル) を先に test するか
- example を topic-neutral にした時、AI 主題の corpus でも自然にトピック語を含むラベルが出るか、それともトピック語が落ちて意味が薄くなるか
- 「20 文字程度」のような明示制約は instruction として効くか、それとも example の重力に再び負けるか

## Updates

- 2026-06-04: 補正。refinement step (`hierarchical_label_refinement.py`) を読み直したところ、verbosity confound の真の構造は (1) INITIAL/MERGE few-shot template と (2) `setwise_refine` の length 制約なし の **2 つの独立 issue の合成**だった。さらに `setwise_refine_short` が `max_label_length=18` で既に存在しており、A/B candidate pair の選択 (build script で `none` vs `setwise_refine` を hard-code した) が confound の実装上の引き金でもあったと判明。「仕切り直しの方針」を 1 動線から A/B/C の 3 動線に拡張し、初版の「prompt few-shot だけが root cause」の単純化を撤回した
- 2026-06-03: 初版。nishio による sibling_label_set 設計批判から始まり、3 文脈すべてに同じ prompt few-shot template 由来の冗長度 confound があると判明したため、現実験を仕切り直し決定として記録
