---
type: analysis
summary: "本体 docs の方針系譜（docs-policy-history）と現在地監査（docs-reader-coverage-audit）を踏まえ、「何がどうなると良いか」を 2026-10-13 の live 検証付きで一本化した direction / roadmap。理想像は 3 レンズ（読者体験 / 保守持続性 / 最小介入）で収束し、道筋は『今すぐ出せる write-and-done + rot-gate』→『additive な reader-facing』→『小さな signed content』→『policy-gated な構造の本丸』の 4 層に、意思決定ゲートを明示して分ける"
sources:
  - kouchou-ai-docs-policy-history.md
  - docs-reader-coverage-audit-2026-10-13.md
---

## 何を問うたか

[[kouchou-ai-docs-policy-history]] が本体 docs 方針議論の**系譜と横断原則**を、[[docs-reader-coverage-audit-2026-10-13]] が 5 読者像に対する**現在地のギャップ**を一本化した。本ページはその次の問い——**「で、何がどうなると良いか / どの順で手を付けると良いか」**——に答える direction。2026-10-13 に docs 方針が wiki 上で集約されたのを受け、理想像と道筋を live 検証付きで固定する。

## Freshness marker

- コード基準: `work/kouchou-ai origin/main@a570d689`（2026-10-13 取得）
- GitHub: #876 / #977 / #542 / #885 / #877 / #696 / #903 / #884 を 2026-10-13 に `gh` で live 確認
- 検証方法: 既存 2 ページの live claim を独立に再照合（nav 差集合・`how-to-use.md` grep・`cli-quickstart.md` カバレッジ・入口構造・issue/PR state）。理想像は読者体験 / 保守持続性 / 最小介入の 3 レンズで独立起案し収束を取った
- この検証で既存 2 ページの 3 箇所に訂正が必要と判明（末尾「検証で見つかった訂正」）

## 検証で確定した現在地（2026-10-13）

既存 2 ページの主要 claim はおおむね CONFIRMED。要点のみ：

- **nav 未登録はちょうど 6 ページ**（CONFIRMED）。`mkdocs.yml` は `not_in_nav`（`/refactoring/**`・`misc/github-actions-status-update.md`）で意図除外を管理しており、その外にある 6 ページ（`deployment/static-hosting-csp` / `deployment/storage-snapshot-operations` / `development/model-catalog` / `development/openai-flex-processing` / `development/opinion-classification` / `development/web-ui-node-runtime-dependencies`）は nav になく公開サイト導線から辿れない。書いたのに届いていない。
- **`how-to-use.md` は 104 行で #176/#961/#52/#306 を未記載**（CONFIRMED）。`粒度`・`散布図` は各 1 ヒットするが旧機能（階層クラスタリング / 全体図の定義）の文脈で、新しいインタラクティブ挙動ではない。WebUI 利用者（A/C）向けの中心ページが最新 UI に追従していない。
- **入口は今も setup-first**（CONFIRMED）。`docs/index.md` は「クイックスタート（一般ユーザー向け=OS セットアップ / 開発者向け=docker compose）」で始まり、nav 最上位は section 種別（はじめに / ユーザーガイド / 開発者向け / デプロイ）。読者像でも demo-first でもない。PR #883（利用モード別導線草案, closes #876）は **CLOSED（abandoned）** で main 未着。
- **残る宙吊りは #876 / #977 / #542**（CONFIRMED）。#877・#903・#696・#884 は 2026-09 wave で landing 済み。#885（Node runtime 排除）は no-assignee のまま yasumorishima が方向2・3 の実装計画を提示した planning 段階。

## 収束した理想像（3 レンズの合流点）

読者体験・保守持続性・最小介入の 3 レンズは、強調点こそ違え、**同じ end-state** に収束した。

1. **書いた docs は必ず届く**：nav 未登録 6 ページが読者像に沿って登録され、`opinion-classification`(#975)・`model-catalog`(provider/model/OpenRouter) が CLI/development 導線から辿れる。「書いたのに不可視」がゼロ。
2. **最大読者の WebUI 説明が current**：`how-to-use.md` が #176(分析方式=LLM直接グルーピング選択)/#961(全画面のまま粒度切替)/#52(散布図連動)/#306(帰属可視化・操作ヒント) を反映し、**WebUI feature PR が必ず how-to-use を触る規律**で stale 化しない。CLI 側（feature と同時更新）と同じ運用を WebUI 側にも効かせる。
3. **入口が demo-first**：`docs/index.md` は「まず実例レポートを見る（公開事例 + viewer 案内 + 読み方ガイド）」と 5 読者像 router で始まり、OS/Docker setup は「自分で建てる」分岐に降格。`getting-started/` は入口ではなく分岐先。どの読者像も dead-end にならない（B=managed/仲介者/責任分界を正直に案内、E=CLI + 実験機能カタログ）。
4. **安定 URL 責務は docs ページ、README は改訂可能な入口**：外部ディープリンクは docs 個別ページへ寄せ、README は日本語デフォルト + 言語リンク（#968 後）を保つ。非開発者・非日本語話者は GitHub でなく docs サイトへ着地させる。
5. **docs は AI の default/template として正しい**：AI がコピペする config 例（クラスタ数デフォルト、model/embedding ブロック）が code と乖離しない。`[3,6]` 事件（stale docs = 誤った AI default = バグ）の再発を構造で防ぐ。

## 道筋：4 層に分け、意思決定ゲートを明示する

既存 audit の `1(nav)→2(how-to-use)→3(spine)` は effort/即効順。ここではそれを**「意思決定が要るか」で層化**し直す。律速は文章を書く労力ではなく、どの層が人間の product 判断待ちかである。

### Tier 0 — 今すぐ出せる write-and-done + rot-gate（product 判断ゼロ）

- **nav 未登録 6 ページを `mkdocs.yml` nav に登録**。既存カテゴリにそのまま置き、「E 向けか D 向けか」の読者像配置判断は**ここで解決しない**（spine の Open Question にわざと結合させない）。
- **同じ PR で `validation: {nav: {omitted_files: warn}}` を `mkdocs.yml` に追加**。検証済みの重要点：docs CI（`.github/workflows/docs.yml`）は既に `mkdocs build --strict` で回っているが、`mkdocs.yml` に `validation:` ブロックが無いため omitted-nav は `info` 止まりで strict は落ちない。この 1 行で omitted-nav が `warn`→strict で CI 失敗となり、**7 本目の orphan が二度と silently 復活しない恒久ゲート**になる。登録とゲートは同一 PR に（ゲートだけ=main 赤、登録だけ=また腐る）。
- **`cli-quickstart.md` の設定項目テーブルに embedding ブロックを追記し、`embedding.model` がチャットモデルと独立選択できる旨を 1 行**（#450）。現状 embedding モデルは UMAP 使い回し節の caveat で 1 回触れられるだけで、設定テーブルに embedding ブロックが無い。code 実在（`packages/analysis-core/src/analysis_core/steps/embedding.py:11`, `config["embedding"]["model"]`）。AI がテーブルを template として使うと embedding 設定が欠落する。

> Tier 0 は 100% 既存の価値への配線 + 恒久ゲート。authoring コストでなく connection コストしか払わず、reversible で、止まる product 判断を持たない。**最初の一手はここ**。

### Tier 1 — additive な reader-facing（破壊的変更なし、今出せる）

- **`docs/index.md` 冒頭に demo-first intro + 5 読者像 router を additive に追加**（`getting-started/` は rename しない）。読者が最初に着地するのは index.md で、setup-first のままだと A/B/C は how-to-use に到達する前に離脱する。rename の redirect 判断（Tier 3）を待たずに出せる非破壊 slice であり、#876 の reader-facing な partial として最大レバレッジ。
- **`how-to-use.md` を現 UI に rewrite**（#176/#961/#52/#306、手順/スクショ）。worst-served な A/C の destination を current にする。
- **WebUI docs の再 stale 化を止める process**：PR テンプレに「WebUI の表示・操作を変える PR は `how-to-use.md` を見直したか」チェック（最softest）+ `apps/public-viewer|client|admin/**` を触って `how-to-use.md` を触っていない PR に**非ブロッキング**で comment/label する CI job。これが本命の ROI——一度の catch-up でなく、**CLI/WebUI 保守非対称の根因**を塞ぐ。ブロッキングにすると refactor/test/deps PR で gaming を誘発するので非ブロッキングに留める。

### Tier 2 — 小さな signed content（bounded な判断が 1 つ要る）

- **#542 レポート責任所在ページ**を新設し、report/demo 面で #696 の読み方ガイドの隣に置く。#696(読み方)は landing 済み・#542(責任所在)は 2025-05-19 起票以来ノータッチ、という非対称レーンの片割れ。書く量は小さいが、**責任・免責の文面は AI 起案でなく nishio/org の signoff 必須**（governance/legal リスク）。だから労力でなく「bounded な判断」ゲート。公開境界厳守（Azure 実環境の URL/resource/手順は書かない）。

### Tier 3 — policy-gated な構造の本丸（破壊的・product 判断待ち）

- **demo-first spine 完成 + `getting-started/` rename（#876）**、**README アンカー移行（#977）**。#876 は 2026-09-08 に body 再スコープされ PR #925 / #877・#929・#496・#921 を束ねる umbrella 化している。ここは「書けば済む」ではなく、破壊的な rename と外部リンク切れを伴う。**着手前に要る判断**：
  - (a) rename/old URL の redirect/alias 方針。検証済み：現 `mkdocs.yml` の plugins に redirect 系は無い。`mkdocs-redirects` 導入か旧 path stub かを決めてから rename する。
  - (b) README 外部アンカーの棚卸し（どこから何件）と移行先 docs ページ（#977）。GitHub Markdown はカスタム anchor を固定できないので、安定化は docs 側へ移すしかない。
  - (c) spine tier 2-a「managed service」の実在と、仲介者経路の maintainer/責任分界。managed が不在なら研究者の主入口は CLI + カタログ経由になり、実験機能カタログの重みが上がる。
- **#977 はアンカー衛生の CI 化とセットで**：mkdocs の link/anchor validation（`validation` ブロックの `not_found`/`unrecognized_links: warn` 等）を Tier 0 のゲートに足してから移行する。でないと移行作業自体が #977 の防ぎたいアンカー腐敗を再生産する。

## 実行チェックリスト（2026-10-13 grounding 済み）

各アクションの file / 変更 / 「直接PR可 or 要判断」を、`origin/main@a570d689` 実読で確定した。dedup 確認済み：**Tier 0/1 をカバーする既存 open issue / PR は無い**（repo の open PR は #891 Windows packaging のみ）。

- **T0-a｜nav 6 ページ登録** — `mkdocs.yml`。`デプロイ` 節に `static-hosting-csp` / `storage-snapshot-operations`、`開発者向け` 節に `model-catalog` / `openai-flex-processing` / `opinion-classification` / `web-ui-node-runtime-dependencies` を各ページ H1 由来のラベルで追加。**直接PR可**（判断ゼロ）。
- **T0-b｜nav rot-gate** — 同 PR で top-level に `validation:\n  nav:\n    omitted_files: warn` を追加。CI は既に `mkdocs build --strict`、`validation:` ブロックが無く omitted-nav は info 止まりなのが orphan 発生の原因。**T0-a と必ず同一 PR**（gate 単独=main 赤、登録単独=また腐る）。**直接PR可**。
- **T0-c｜#450 embedding 行追記** — `docs/user-guide/cli-quickstart.md` の「設定項目の説明」表に `embedding.model`（chat 用 `model` と独立・既定 `text-embedding-3-small`）行を追加。code 実在（`embedding.py:11`、他モデルと違い chat model を継承しない=独立が構造的に確定）。#450 は CLOSED なので docs 追従のみ、reopen しない。**直接PR可**。
- **T1-a｜index.md demo-first intro + 読者像 router**（additive、rename なし） — **要判断**：nishio owns #876（umbrella）。additive slice を #876 の子として今出すか確認。
- **T1-b｜how-to-use.md catch-up** — #176（AI詳細設定に「分析方式=LLM直接グルーピング」追記）/ #961・#52・#306（新 H2「散布図の操作」に粒度切替・クリック連動・操作ヒント/帰属凡例を集約）。全機能 CLOSED/MERGED。UI が landing 直後なので pixel スクショより behavior-level 記述。**docs-only は直接PR可**。既知の付随事項：可視化節に `詳細クラスタ` が未記載、doc 用語 `濃いクラスタ` と UI ラベル `濃い意見` の不一致を整理。
- **T1-c｜WebUI docs 非 stale 化プロセス** — PR テンプレ（`.github/PULL_REQUEST_TEMPLATE.md`）のレビュアーチェックリストに how-to-use 更新確認を 1 行 + `apps/public-viewer`/`apps/admin` を触って how-to-use を触らない PR に**非ブロッキング**で comment する新 workflow（`actions/github-script@v7` は既存慣習、`pull_request_target` が要るかは fork 対応の判断）。**要判断**（CI ポリシー・非ブロッキング前提・path 粒度）。注：実フロントは `apps/client` でなく `apps/public-viewer` + `apps/admin`。
- **T2｜#542 責任所在** — **新ページでなく** footer 免責ダイアログ（`apps/public-viewer/components/Footer.tsx` と `apps/admin/components/Footer/Dialog.tsx` の**2 コピー両方**）+ README 免責に「レポートから下した判断の責任は発行者/利用者に帰属し dd2030/広聴AI は免責」を追記。#539 スレッド由来。**要判断**（文面は org signoff 必須・AI 起案不可）。発行者作成の `利用規約`(meta.termsLink) とは別物なので混同しない。
- **T3｜#876 spine rename + #977 anchor 移行** — **要判断**（redirect 方針 / anchor 棚卸し / managed 実在。上記 Tier 3 参照）。

## 構造的な根因と恒久対策

個別ギャップの背後にある root cause は 2 つ。理想像の 2・5 がこれに対応する。

1. **CLI/WebUI 保守非対称**：CLI docs は feature PR が一緒に触るので current、WebUI `how-to-use.md` と nav 登録は誰かが気付かないと腐る。→ **プロセス/CI ゲート**（nav validation / WebUI PR の how-to-use touch check）を feature wave の前に効かせる。one-time の catch-up は非対称を再累積させるだけ。
2. **docs を AI default/template として単一ソース化していない**：AI がコピペする config 例が code と乖離しても気付けない。→ AI-default 地雷（クラスタ数デフォルト、model/embedding ブロック）に限って code から生成 or doctest で照合。全ページには広げない（over-engineering 回避）。

## nishio が実際に下すべき判断（律速）

文章を書く作業ではなく、以下が道筋の律速。Tier 0/1 はこれらを待たずに出せる。

- **#876 の切り方**：additive first slice（index.md demo-first intro、今出せる）と破壊的 rename+redirect（policy 待ち）を分けてよいか。umbrella 化した #876 の子 slice として Tier 1 を切るか。
- **`getting-started/` rename の redirect 方針**（`mkdocs-redirects` 導入 or stub）。
- **spine tier 2-a managed service の実在**と、仲介者経路の責任分界・maintainer。
- **#542 責任所在の文面**（org signoff）。
- **how-to-use touch check を CI/contributing に入れてよいか**（非ブロッキング前提）。

## 検証で見つかった訂正（既存 2 ページへ filing back 済み）

- **[[docs-reader-coverage-audit-2026-10-13]]**: #450（埋め込みモデル独立選択）を「cli-quickstart に記載あり」と列挙していたが、実際は UMAP 節の incidental な caveat のみで**実質未記載**。E の「比較的追従」には #450 の穴がある（→ Tier 0 で塞ぐ）。
- **[[kouchou-ai-docs-policy-history]]**: #876 を「2026-05-31 以降議論なし」としていたが、last *comment* は 2026-05-31 でも **body は 2026-09-08 に再スコープ**され PR #925 / #877・#929・#496・#921 を束ねる umbrella になっている。「議論なし」でなく「umbrella 化」が正確。
- **[[kouchou-ai-docs-policy-history]]**: #696 を閉じた「PR #924・#24」の #24 は **cross-repo の `tokoroten/kouchou-ai-serverless#24`**（単一HTML版の読み方ガイド、2026-09-09 merge）であって `kouchou-ai#24` ではない。collision 回避のため repo を明記。

## Open Questions

- Tier 0 の nav 配置を既存カテゴリのまま置く（最小介入）か、最初から読者像別に置く（読者体験）か。後者は spine の persona-placement Open Question に結合し stall しうるので、**配置は既存カテゴリ→spine で再配置**を推すが、nishio 判断。
- how-to-use touch check を CI に入れる場合、どこまでの path 変更を「UI 変更」と見なすか（false positive を抑える粒度）。
- #306/#961 は a570d689 の約 2 日前に landing したばかりで UI がまだ動くかもしれない。how-to-use はピクセル厳密なスクショより behavior-level の記述を優先すべきか。
- 実験機能カタログ（6 月提案）を Tier 3 で本体 docs に新設する際、freshness（最終確認日）を honor-system でなく code path の最終 commit と機械照合できるか。

## 関連

- [[kouchou-ai-docs-policy-history]]: 方針系譜と横断原則（本ページはその「で、どうする」）
- [[docs-reader-coverage-audit-2026-10-13]]: 5 読者像の現在地ギャップ（本ページの道筋の素材）
- [[kouchou-ai-docs-entry-restructure-2026-06-03]]: demo-first spine の原案（Tier 1/3 の入口設計）
- [[readme-anchor-freeze-and-docs-entry-2026-10-13]]: #977 アンカー凍結回避（Tier 3 の前提）
- [[issue-876-developer-docs-gap-audit-2026-06-30]]: #876 の 6/30 gap audit（本ページは直近 wave 後の再設計）
