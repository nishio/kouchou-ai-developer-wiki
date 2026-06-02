---
type: analysis
summary: "LLM groupingを実装するなら、short term は workflow canonical path に `analysis_mode=llm_grouping` を差し込み viewer 互換を保ち、long term は `analysis_capabilities` と plugin `requirements` へ収束させるのが筋がよい"
sources:
  - llm-grouping-implementation-observation-2026-05-25.md
  - pr-827-llm-grouping-capabilities-plan-2026-05-18.md
  - llm-grouping-background-history.md
  - public-ui-requirements-for-broadlistening.md
---

LLM groupingを current `kouchou-ai` に入れる時の本質は、**新しい clustering step を 1 本足すこと** ではなく、**「散布図を自然には生まない分析モード」を current product にどう受け入れるか** である。  
そのため、実装は短期互換と長期契約を分けて設計した方がよい。短期は `analysis_mode=llm_grouping` を workflow canonical path に差し込み、viewer 互換の `x/y` と `cluster-level-*` を暫定的に出す。長期は `analysis_capabilities` と chart plugin `requirements` を整え、scatter-first 前提を弱める。[[llm-grouping-background-history]]より [[pr-827-llm-grouping-capabilities-plan-2026-05-18]]より [[llm-grouping-implementation-observation-2026-05-25]]より

## 先に結論

実装順は次の 5 段がよい。

1. **workflow canonical path に限定して `analysis_mode` を導入する**  
   direct-step `run()` ではなく `run_default() -> run_workflow()` が canonical なので、`llm_grouping` の入口は workflow 選択に寄せる。[[llm-grouping-implementation-observation-2026-05-25]]より
2. **短期の `llm_grouping` は embedding を残す**  
   目的は viewer 互換と product への最短搭載であり、理想的な分析純度ではない。`x/y` は embedding 由来でよい。[[pr-827-llm-grouping-capabilities-plan-2026-05-18]]より [[public-ui-requirements-for-broadlistening]]より
3. **`llm_grouping` step は cluster tree と assignment を canonical artifact として返す**  
   旧 hierarchical 実装の副産物に寄せるのでなく、`argument -> cluster_ids` と `clusters(level/id/parent/label/takeaway/value)` を first-class に作る。[[llm-grouping-background-history]]より
4. **aggregation で `analysis_capabilities` を生成する**  
   capability は config で人間が宣言する値ではなく、result artifact から導出する派生値として持つ。[[pr-827-llm-grouping-capabilities-plan-2026-05-18]]より [[llm-grouping-implementation-observation-2026-05-25]]より
5. **viewer 側は scatter を default 前提にせず、available mode から fallback する**  
   長期は `hierarchyList` / `treemap` / scatter を対等に扱う。LLM grouping 系の default view は当面 `hierarchyList` が無難で、scatter は capability がある時だけ出せばよい。[[public-ui-requirements-for-broadlistening]]より [[llm-grouping-background-history]]より

## 実装の芯

### 1. `analysis_mode` は workflow 選択で持つ

current `main` は `PipelineOrchestrator.run_default()` が `run_workflow()` を呼び、default workflow は `HIERARCHICAL_DEFAULT_WORKFLOW` 固定である。ここに legacy 分岐を増やすより、

- `hierarchical-default`
- `llm-grouping-compatible`

の 2 workflow を持ち、`analysis_mode` から選ぶ方が自然である。[[llm-grouping-implementation-observation-2026-05-25]]より

理由は次の 3 つ。

- `run()` 側に branch を入れると current canonical path と逆行する
- step plugin / workflow definition の既存資産をそのまま使える
- 将来 taxonomy-guided 亜種を `llm-grouping-taxonomy-guided` のように増やしやすい

したがって、最初の実装対象は `analysis_core.orchestrator.run_workflow()` と workflow registry であり、step 関数群の if 文ではない。[[llm-grouping-implementation-observation-2026-05-25]]より

### 2. `llm_grouping` は 1 本の workflow step として始める

初回実装では、LLM groupingを細かく 3 step に分けるより、まずは 1 plugin で

- グループ候補の発見
- 各 argument の cluster assignment
- `cluster-level-*` 互換列の生成

まで返す方がよい。理由は、今いちばん不確実なのは step 境界の再利用性ではなく **出力契約が viewer と aggregation に通るか** だからである。[[pr-827-llm-grouping-capabilities-plan-2026-05-18]]より

分解は後からでよい。初回から細分化すると、

- intermediate artifact 形式
- retry 単位
- prompt 単位
- taxonomy-guided 分岐

が同時に open question になり、PR が太る。

### 3. 短期互換のため、embedding は切らない

理想論としては LLM grouping 系は embedding 非依存でよい。しかし current product に最短で載せるには、

- scatter の URL / UI / shared understanding を壊さない
- 既存 viewer の大半をそのまま使う
- `public-ui` の 7 要件のうち「全体像」「個票への辿り」をすぐ失わない

ことの方が重要である。[[public-ui-requirements-for-broadlistening]]より

そのため short term では

- `extraction`
- `embedding`
- `llm_grouping`
- `overview`
- `aggregation`

で十分で、`hierarchical_clustering` だけを外す構成が妥当である。`x/y` は semantic truth ではなく viewer compatibility layer と割り切る。[[pr-827-llm-grouping-capabilities-plan-2026-05-18]]より [[llm-grouping-background-history]]より

## 具体的な変更順

### Phase 0. schema を先に決める

先に決めるべきはアルゴリズム詳細ではなく、`hierarchical_result.json` に何を増やすかである。最小でも次が必要である。

- `config.analysis_mode`
- `analysis_capabilities`
- `arguments[].cluster_ids`
- `clusters[].level/id/parent/label/takeaway/value`

ここで重要なのは、`analysis_capabilities` を top-level に置くことだ。viewer の mode 可否は `clusters` の偶然の形から毎回推論するより、この派生情報を見る方が安定する。[[llm-grouping-implementation-observation-2026-05-25]]より

### Phase 1. analysis-core に `llm-grouping-compatible` workflow を追加

最小変更は次で足りる。

- `packages/analysis-core/src/analysis_core/workflows/llm_grouping_compatible.py` を追加
- `orchestrator.py` で `config.analysis_mode` に応じて workflow 選択
- `analysis.llm_grouping` plugin を追加
- aggregation で `analysis_capabilities` を追記

この段階では API/Admin/UI は `analysis_mode` の受け渡しだけ通せばよい。taxonomy-guided はまだ入れない。[[llm-grouping-implementation-observation-2026-05-25]]より

### Phase 2. viewer に `requirements` を入れる

current viewer には既に `mode.isDisabled(result)` があるので、変更は全面再設計ではない。`ChartMode` か `ChartPluginManifest` に

```ts
requirements?: CapabilityKey[]
```

を足し、

- scatter: `has_xy`, `has_hierarchy`
- treemap: `has_hierarchy`
- hierarchyList: `has_hierarchy`
- density: `has_hierarchy`, `has_multi_level`, `has_density_rank`

のように置き換えるのが自然である。[[llm-grouping-implementation-observation-2026-05-25]]より

ここまで行けば、LLM grouping 系 mode の default chart を `hierarchyList` にしても UI が破綻しない。

### Phase 3. taxonomy-guided を別 mode で増やす

taxonomy-guided は `llm_grouping` のオプションでも動くが、product / UX 上は別 mode に寄せた方がよい。理由は

- 新規論点発見モード
- 既存カテゴリへの整列モード

が目的としてかなり違うからである。[[llm-grouping-background-history]]より

短期は `analysis_mode=llm_grouping` だけで始め、taxonomy-guided は

- `analysis_mode=llm_grouping_taxonomy`
- あるいは `analysis_mode=llm_grouping` + `grouping_strategy=taxonomy_guided`

のどちらかへ後で切るのがよい。

## 実装上の注意

### `analysis_capabilities` は aggregation で作る

`llm_grouping` step の返り値で capability を持たせるより、最終 artifact を組む aggregation で一度まとめて判定した方がよい。そうすれば hierarchical / llm_grouping の両方で同じ detector を使える。[[pr-827-llm-grouping-capabilities-plan-2026-05-18]]より

### scatter の default は mode ごとに切り替える

LLM grouping 系で `enabledCharts` を手でいじるより、`defaultChart` の fallback を

1. report 設定の希望
2. mode requirements に適合するか
3. 適合しなければ `hierarchyList`

の順で決めた方がよい。current viewer は `enabledCharts[0] ?? "scatterAll"` を default にしているので、ここは明示的に直す必要がある。[[llm-grouping-implementation-observation-2026-05-25]]より

### 最初の PR でやりすぎない

初回 PR で同時にやらない方がよいのは次である。

- taxonomy-guided 実装
- 専用 LLM grouping view の導入
- scatter を消す判断
- capability の viewer 再計算と warning 可視化

ここまで混ぜると review 単位が大きくなり、`PR #827` が避けようとしていた「長期の理想と短期の互換実装が一緒に崩れる」状態に戻る。[[pr-827-llm-grouping-capabilities-plan-2026-05-18]]より

## 推奨 PR 分割

1. `analysis_mode` の受け渡しと workflow 分岐だけ
2. `analysis.llm_grouping` plugin と smoke test
3. aggregation の `analysis_capabilities`
4. viewer `requirements` + default fallback

この 4 本なら、それぞれ失敗点が分かりやすい。

## Open Questions

- `llm_grouping` の出力 tree を multi-level にするのか、まず 1 level だけで始めるのか
- `overview` prompt を hierarchical 前提の文面から mode 別に分ける必要があるか
- taxonomy-guided を同じ mode の strategy として持たせるか、別 mode に分けるか
- LLM grouping 系の default view は当面 `hierarchyList` で十分か、それとも最初から専用 view を切るべきか

## Updates

- 2026-05-25: 初版作成。`PR #827` 計画文書、LLM grouping 系の歴史整理、public UI 要件、current main の code 観測を突き合わせて implementation order を具体化
