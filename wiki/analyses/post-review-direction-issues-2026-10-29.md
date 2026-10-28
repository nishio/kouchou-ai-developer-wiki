---
title: "考察の 1〜3 を Issue 化して着手：賛否・新規性の属性ステップ、階層リストの詳細モード化、ビューの選び方ギャラリー（2026-10-29）"
type: analysis
summary: "post-review-product-direction の順序 1〜3 を #1158〜#1160 として Issue 化し、同日に PR #1165〜#1167 を作成。各 PR で AI が置いた設計判断・検証内容・人間に確かめてほしい点と、副産物（httpx 未宣言 #1168）を記録"
sources:
  - post-review-product-direction-2026-10-28.md
  - retrospective-2026-10-28.md
---

## 位置づけ

[[post-review-product-direction-2026-10-28]] の「順序」1〜3 を、nishio の指示（2026-10-29「1〜3 を Issue にして着手して」）で Issue 化し、同日に実装して PR を出した記録。4 以降（付箋表示の CLI artifact、埋め込み重み付け、DivCon）は未着手。

| 順序 | Issue | PR | 状態（2026-10-29） |
|---|---|---|---|
| 1. 賛否・新規性の属性ステップを CLI に | [#1158](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1158) | [#1165](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1165) | CI green、未 merge |
| 2. 階層リストを詳細モードとして正式化 | [#1159](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1159) | [#1166](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1166) | CI green、未 merge |
| 3. 全 view ギャラリー | [#1160](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1160) | [#1167](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1167) | CI 実行中、未 merge |

3 件とも着手前に nishio を assignee に設定し、`work/kouchou-ai-<issue>` の worktree で実装した。merge は人間の判断。

## 1. 属性ステップ 2 つ（#1158 → #1165）

### 何を作ったか

`opinion_classification`（[#971](https://github.com/digitaldemocracy2030/kouchou-ai/issues/971)）と同じ opt-in 型の任意ステップを 2 つ足した。どちらも既定は無効で、WebUI は触っていない。

- **`opinion_stance`**（LLM、`extraction` の後）: 意見 1 件ごとに「対象」への賛否を -1.0〜+1.0 で付ける。対象は `target`、省略時はレポートの `question`。応答は `{applicable, stance_score}` の 2 キーで、対象と無関係な意見は `applicable=false`（判定不能）として CSV は空欄、`attributes` には入れない
- **`opinion_novelty`**（LLM なし、`embedding` の後）: `embeddings.pkl` から「他の意見からの遠さ」を計算し、順位を 0.0〜1.0 にして付ける。既定は k 近傍（k=10）までの平均コサイン距離、`isolation_forest`（farbrain の方式）も選べる
- `hierarchical_aggregation` が有効なステップの CSV を `arguments[].attributes` に **数値** で合流する。公開ビューアの属性フィルタは数値属性を範囲で絞れるので、「賛成だけ」「新規性上位」の地図がそのまま見られる

### 設計判断（AI が置いたもの）

- **判定不能を 0.0 にしない**。中立と無関係は別で、無関係を 0 に寄せると「中立が多い」と誤読される。`applicable` を別キーにしたのは、`stance_score: null` だと strict 構造化出力（local provider のゲートウェイ）で anyOf が必要になるため
- **新規性は生の距離ではなく順位**。埋め込みモデルや件数で距離の絶対値が変わるので、レポート内の相対位置だけを約束する。生の値の min / max / mean は summary JSON に残す
- **意見 1 件ごとの LLM 呼び出しループを `_per_opinion.py` に共通化**し、`opinion_classification` もそれを使うように変えた。失敗時に部分出力を残さない・前回出力を開始時に消す・失敗理由に意見本文と鍵を出さない、という既存の約束はそのまま
- **`question` を global param として再実行判定に入れた**。`target` 省略時の賛否は質問文に依存するので、質問を変えたら賛否だけ再実行される
- 書く列は `attributes` に限定し、`config` / status に新しい値を足していない（[[user-api-key-leak-2026-10]] と同じ型を増やさない）

### 検証

- analysis-core の `pytest` 848 passed、`ruff check` green。追加テストは応答の検証（範囲外・非数値・欠落・`null`）、判定不能の扱い、集約への数値合流、無効時に古い CSV を混ぜないこと、strict スキーマ、実行計画（既定無効、`--force` でも走らない、`question` 変更で再実行）
- **実データでの smoke**: 公開コメント由来の 997 意見（ローカル埋め込み、[[claude-provider-experiment-output-2026-10-17]] の corpus）で `opinion_novelty` を両方式とも 1〜2 秒で完走。k 近傍方式では、同じ公式声明の言い換え 3 件が最下位（0.000〜0.002）、他と離れた意見が最上位になった。Isolation Forest は生の値の幅が狭く（0.37〜0.51）、順位化しないと使いにくい
- CLI の `--dry-run` で両ステップが計画に出ること、`mkdocs build --strict` が通ることを確認
- **未確認**: `opinion_stance` の実 LLM での応答品質。既定プロンプトは同梱したが、対象の書き方でスコアの向きが変わるので「公開前にサンプルを読む」旨を docs に書いた

## 2. 階層リストの詳細モード化（#1159 → #1166）

### 何を作ったか

- view 切替ボタンに **読者の目的** をツールチップで出す（全体をざっくり掴む / 細かい話題ごとに見る / 特に似た意見が集まった所を見る / グループの大きさを比べる / 全部読む・掘り下げる（詳細モード））。これまで `tooltip` は `SegmentGroup.Items` に渡しても表示されていなかった（Chakra がその prop を持たない）ので、ラベル側で `Tooltip` に包んだ。無効時の理由も同じ経路で出るようになった
- 階層リスト plugin の名前を「階層リスト（詳細モード）」、説明を目的ベースにし、「サンプル plugin」の記述をコードと docs から外した
- 最下層の意見に **出典リンク**。条件は散布図と同じ（`config.enable_source_link` が有効かつ `url` あり）
- 文言は ja / en / ko。**既定の view・順序・狭い画面の初期表示は変えていない**

### 設計判断

- 「正式化」を「既定にする」とは読まなかった。[[post-review-product-direction-2026-10-28]] のとおり既定は散布図のままで、リストは目的名で案内する
- 原文本文の表示は [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155)（[#56](https://github.com/digitaldemocracy2030/kouchou-ai/issues/56)）が担うので重複実装していない。同じファイルの props 追加が衝突するので、どちらかを先に merge した後にもう一方を rebase する
- 「ウケない」仮説の測り直し（どの view が選ばれたかを数える）は範囲外とした。計測を足すかは人間判断

### 検証

- public-viewer の `tsc`・`biome`・`jest` 46 suites green。追加テストは出典リンクの有無（有効かつ URL あり / 無効 / 設定なし）
- 未確認: 実ブラウザでのツールチップの見た目。全画面ツールバー（`ScatterLevelSwitch`）にも同じ目的文が出る

## 3. ビューの選び方ギャラリー（#1160 → #1167）

### 何を作ったか

`docs/user-guide/view-gallery.md`。「やりたいこと → 見方 → 分かること・分からないこと」の表と、同じレポートの 5 view のスクリーンショット。コーパスはリポジトリ同梱のテスト用レポート（AIと著作権、9,568 件・3 階層。CI の `client build` が使うもの）で、ライセンス確認が不要な範囲に留めた。撮影時点と本体バージョンを明記。

### 作り方（再現手順）

CI と同じ fixture API を立て `build:static` → `python3 -m http.server` で配信 → Playwright で各 view を切り替えて撮影 → PIL で 256 色に減色（5 枚で約 500KB）。この環境（arm64）では Playwright が対応版の Chromium を落とせないので、キャッシュにあった別版の Chromium を `executablePath` で指定した。ツリーマップは文字クリックだと切替インジケータが動かないことがあり、radio を直接 check した。

### 残したもの

- 属性で絞った見方は「準備中」。テスト用レポートに属性が無い。#1165 が入った後に同梱サンプル（`sample_comments.csv`）で賛否・新規性を付けて回し、同じ並びで足す
- #1166 が入ったらリストのスクリーンショット（見出し・説明文が変わる）を撮り直す。`opinion-scores.md` が main に入ったらギャラリーのリンクを Issue からそのページに差し替える
- 常設公開の置き場は [#518](https://github.com/digitaldemocracy2030/kouchou-ai/issues/518) の判断に従う

## 副産物

- **analysis-core を lock なしで入れると `import httpx` で落ちる**（[#1168](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1168)）。`rate_limit.py` が `httpx` を直接 import しているのに `dependencies` に無く、新しい `openai` 3.x は `httpx2` 依存。CI は `requirements-dev.lock` で入れるので気づかれていなかった。PyPI 利用者と `pip install -e` のコントリビュータが当たる
- Dependabot に low 1 件（npm、`pnpm-lock.yaml`）が新規に出ている。修正版の有無は未確認
- 本体の `ruff format --check` は main 時点で 6 ファイルが差分ありだが、CI は `ruff check` だけなので影響なし

## 次に見るもの

1. 3 本の merge 判断（人間）。順序の提案: #1165（本体に影響しない CLI 追加）→ #1155 または #1166（どちらかを先に、残りを rebase）→ #1167
2. #1165 merge 後、同梱サンプルで賛否・新規性を実 LLM（または ollama）で回し、スコアの向きを目視確認してからギャラリーに属性つきの例を足す
3. #1168 の対応（`httpx` の宣言か `openai<3` の固定）
4. 順序 4〜6（付箋表示の書き出し契約、埋め込み重み付けの clean experiment、DivCon の契約）は [[open-decisions]] A13・A14 の判断待ち

## Open Questions

- `stance_score` の既定の対象を `question` にしたが、質問文が「〜についてどんな意見があるか」型だと賛否の対象として弱い。パブコメなら「この案」を `target` に明示する運用で足りるか、`intro` も渡すべきか
- 新規性スコアの k の既定（10）と、意見数が数千〜数万のときの計算時間（brute force の cosine kNN）。1 万件で数十秒なら許容か
- view の目的ツールチップの文言。英語・韓国語は機械的に当てたので、ネイティブ確認が要るか

## Updates

- 2026-10-29: 初回作成
