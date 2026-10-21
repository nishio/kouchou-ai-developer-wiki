---
title: "LLM grouping の指定カテゴリ分類モード"
type: concept
summary: "LLM grouping には枠を自動発見するモードと、人間が与えた所与カテゴリへ割り当てる指定カテゴリ分類（supervised）モードがある。後者は必ず「その他」受け皿を自動付与し、非該当意見を押し込めない。現状は main から入れた CLI 専用（PyPI 0.1.3 には未収録）"
sources:
  - source-code.md
---

## LLM grouping の2モード

広聴AI の分析方式 `analysis_mode` には、既定の階層クラスタリングのほかに **LLM grouping（LLM 直接グルーピング）** がある。LLM grouping は意見をトップレベルのグループへ分類する方式で、散布図の座標は従来どおり embedding から計算するためビューアはそのまま使える。

LLM grouping には枠の決め方で2つのモードがある。

1. **自動グルーピング**: 意見のサンプルから LLM が分類の枠自体を発見し、各意見を割り当てる。枠を事前に決めなくてよい。
2. **指定カテゴリ分類（supervised）**: 分類の枠は人間が与え、LLM は**各意見の割り当てだけ**を行う。あらかじめ決まった観点で意見を整理したいときに使う。

> 用語について：LLM が直接分類・グルーピングする方式の一般名は `LLM grouping` / `LLM 直接グルーピング` と呼ぶ。`Jigsaw Sensemaker` はこの一例の固有名詞であり、LLM grouping 全体を Jigsaw と呼ぶと一般カテゴリと特定ツールが混ざって混乱するので避ける（[[jigsaw-sensemaker]]）。

## 指定カテゴリ分類（supervised）

あらかじめ決めた分類枠に意見を割り当てたいケースは実運用でしばしばある（例: ワークショップで既定のカテゴリに意見を整理したい）。この用途が自動グルーピングと別に必要になる。

設定は `analysis_mode` を `llm_grouping` にし、`llm_grouping.predefined_groups` にカテゴリを与える（下は該当部分の抜粋。実行には `input` / `question` など通常の必須項目も要る）。

```json
{
  "analysis_mode": "llm_grouping",
  "llm_grouping": {
    "predefined_groups": [
      { "label": "交通", "description": "公共交通に関する意見" },
      { "id": "park", "label": "公園・緑地", "description": "公園整備に関する意見" }
    ]
  }
}
```

- 各カテゴリは `label`（必須）と `description`（任意だが推奨。割当精度が上がる）を持つ。`id` 省略時は `g1`, `g2`, … を自動採番。
- `predefined_groups` を与えると**枠の自動発見をスキップ**し、割り当てだけを行う。与えない（または空）場合は従来どおり自動グルーピング。

## 「その他」受け皿を必ず用意する

指定カテゴリ分類では、**どのカテゴリにも当てはまらない意見のための「その他」カテゴリを必ず用意する**。これは設計上の必須要件で、システムが自動付与する（ユーザ指定不要・削除不可）。

理由は、指定カテゴリのどれにも当てはまらない意見を無理に押し込めると、

- 分類の品質が落ちる（関係ない枠に意見が混ざる）
- 分類枠の過不足が見えなくなる

の2点が起きるため。「その他」に意見が多く集まることは、むしろ**分類枠に抜けがあるシグナル**として読める。ラベルは `llm_grouping.other_group_label`（既定「その他」）で変更でき、ユーザが自分で同等の枠（`id: "other"` または同ラベル）を定義していればそれが受け皿として使われ二重には追加されない。

## 実装とスコープ

- engine は `packages/analysis-core/src/analysis_core/steps/llm_grouping.py`。内部は「枠の発見（`_discover_groups`）→ 各意見の割り当て（`_assign_groups`）」の2段で、指定カテゴリ分類は発見段をスキップして固定枠を割り当て段へ渡す。非該当・無効応答は先頭枠ではなく「その他」へ寄せる。
- 現状は **CLI 専用**（`kouchou-analyze --config config.json`）。ただし PyPI の 0.1.3（2026-10-12 公開）には入っておらず、PyPI から入れた `kouchou-analyze` に `predefined_groups` を渡すと、config の検証で `Unknown option 'predefined_groups' for step 'llm_grouping'` として止まる（2026-10-21 時点。main の version 表記も 0.1.3 のままなので `--version` では区別できない）。使うときは main から入れる（手順は [[cli]] の「PyPI 版は main より遅れる」）。
- 作成 UI（管理画面）からの指定カテゴリ分類は未対応で、WebUI 統合は Issue [#997](https://github.com/digitaldemocracy2030/kouchou-ai/issues/997) で扱う（カテゴリ入力フォーム・「その他」固定表示・config の prune/round-trip 整合が論点）。
- 由来は Issue [#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176)（LLM ベース分類の2方向）。自動グルーピングの作成 UI + API + engine は [#987](https://github.com/digitaldemocracy2030/kouchou-ai/issues/987)、指定カテゴリ分類の CLI 実装は [#994](https://github.com/digitaldemocracy2030/kouchou-ai/issues/994) / PR [#996](https://github.com/digitaldemocracy2030/kouchou-ai/issues/996) で main 入り。

## Open Questions

- 「その他」が過大になっていないか（＝枠が不適切でないか）を可視化・警告する仕組みは未実装。
- 階層的な所与タクソノミ（2階層以上の指定枠）は未対応（現状は単層）。
- 実 LLM を伴うフルパイプラインでの大規模な割当品質の評価は未実施。割当品質の評価はラベル品質評価（[[faithful-aggregation-vs-deliberation-dynamics]] 周辺の忠実性評価）とは別軸で設計する。

## Updates

- 2026-10-21: PyPI の 0.1.3（2026-10-12 公開）には指定カテゴリ分類が入っておらず、PyPI 版では config の検証で止まること、使うときは main から入れることを追記。設定例が抜粋であることを明記
