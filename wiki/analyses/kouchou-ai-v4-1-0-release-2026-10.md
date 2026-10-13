---
title: "広聴AI v4.1.0 リリース振り返り 2026-10"
type: analysis
summary: "kouchou-ai v4.1.0（2026-10-13 発行）リリースの retrospective。v4.0.0（2025-12-27）以降 ~10 か月・約 160 PR・8 コントリビュータ（新規 2 名）を束ねた大型リリース。コア/実験拡張の分離、pandas→polars 移行、散布図まわりの WebUI 強化、CLI/analysis-core の大幅拡張（UMAP 使い回し・指定カテゴリ分類・意見ラベル・埋め込み独立選択）、Docker イメージ縮小と Windows 移植性、AGPL 表記訂正、mkdocs docs サイト新設と多言語化、までをテーマ別にまとめる"
sources:
  - github-dev-docs.md
  - refactoring-status.md
  - analysis-core-license-intent-2026-10-12.md
  - kouchou-ai-docs-overhaul-2026-10.md
---

## 何のリリースか

[[kouchou-ai]] **v4.1.0**（2026-10-13 発行、[release](https://github.com/digitaldemocracy2030/kouchou-ai/releases/tag/v4.1.0)）は、v4.0.0（2025-12-27）以降に積み上がった **約 160 PR** を束ねたマイナーリリース。期間は ~10 か月、コントリビュータは 8 名（nishio 中心、tokoroten / shingo-ohki / yasumorishima / katsushi2441 / 101ta28 / Copilot・Devin / dependabot）で、**新規コントリビュータ 2 名**（yasumorishima・katsushi2441）を迎えた。tokoroten は既存の中心的コントリビュータ（serverless 版や技術解説資料の作者）で、GitHub の "New Contributors" 表示は `@tokoroten with @Copilot` という Copilot 併用 PR の初回を拾ったもの。

「リリーススプリント」としての実像は、2026-09〜10 に集中した **棚卸し → 並列実装 → レビュー → 一斉 merge → タグ発行**の波（[[pr-982-987-review-round-2026-10-12]] / [[issue-backlog-audit-2026-10-12]]）に、それ以前の継続的な基盤整備（コア分離・polars 化・Docker 縮小・docs サイト）が合流したもの。本ページはテーマ別の総括。docs 面の詳細は [[kouchou-ai-docs-overhaul-2026-10]] に分けてある。

## ハイライト

- **基盤**: 安定コアと実験拡張の分離（PR [#746](https://github.com/digitaldemocracy2030/kouchou-ai/issues/746)）、**pandas → polars 全面移行**（[#753](https://github.com/digitaldemocracy2030/kouchou-ai/issues/753) ほか）、Docker イメージ縮小（api **~34GB → ~2.7GB**、[#807](https://github.com/digitaldemocracy2030/kouchou-ai/issues/807)）。
- **CLI / analysis-core の product 化**: 自動クラスタ数、self-contained HTML 出力、PyPI 公開、UMAP 使い回し・指定カテゴリ分類・意見ラベル・埋め込み独立選択など、WebUI を介さず CLI/core で高度機能を使えるように。
- **WebUI の読み・操作強化**: 散布図の詳細クラスタ/凸包、クラスタ選択の連動、操作ヒントと帰属可視化、全画面のまま粒度切替、作成 UI からの分析方式選択。
- **コンプライアンス**: AGPL 表記の訂正と出力 HTML へのライセンス同梱（[#970](https://github.com/digitaldemocracy2030/kouchou-ai/issues/970) ほか）、CVE 対応。
- **docs**: mkdocs ドキュメントサイト新設（[#754](https://github.com/digitaldemocracy2030/kouchou-ai/issues/754)）＋多言語 README ＋ docs 大掃除（demo-first 入口・rot-gate 等、[[kouchou-ai-docs-overhaul-2026-10]]）。

## テーマ別まとめ

### 基盤・性能・設計
- **コア / 実験拡張の分離**（[#746](https://github.com/digitaldemocracy2030/kouchou-ai/issues/746)）: 安定運用したいコアと実験的拡張を分け、壊れにくい plugin 境界に。[[broadlistening-tool-ecosystem-vision]] の「WebUI=simple / CLI=実験機能」の二段構造を実装面で裏打ち。
- **pandas → polars 移行**（[#753](https://github.com/digitaldemocracy2030/kouchou-ai/issues/753)、追従 [#774](https://github.com/digitaldemocracy2030/kouchou-ai/issues/774)/[#781](https://github.com/digitaldemocracy2030/kouchou-ai/issues/781)/[#789](https://github.com/digitaldemocracy2030/kouchou-ai/issues/789)）: 性能改善のためデータ処理を polars に一本化。
- **Docker イメージ縮小**（[#807](https://github.com/digitaldemocracy2030/kouchou-ai/issues/807), tokoroten）: api を ~34GB → ~2.7GB に。配布・デプロイの実用性が大きく向上。

### CLI / analysis-core（実験機能を CLI 先行で）
WebUI を作り込む前に core/CLI で実行可能にする方針（[[broadlistening-tool-ecosystem-vision]] の二段構造）が結実したフェーズ。
- **自動クラスタ数**（[#832](https://github.com/digitaldemocracy2030/kouchou-ai/issues/832)）、**CLI の .env fail-fast**（[#768](https://github.com/digitaldemocracy2030/kouchou-ai/issues/768)）、**timeout 既定 300s**（[#795](https://github.com/digitaldemocracy2030/kouchou-ai/issues/795)）
- **self-contained HTML レポート出力**（[#825](https://github.com/digitaldemocracy2030/kouchou-ai/issues/825)、壊れていた npm ステップを置換）、**analysis-core の PyPI 公開ワークフロー**（[#831](https://github.com/digitaldemocracy2030/kouchou-ai/issues/831)）
- **UMAP 平面の使い回し**（[#515](https://github.com/digitaldemocracy2030/kouchou-ai/issues/515) → [#988](https://github.com/digitaldemocracy2030/kouchou-ai/issues/988)）、**埋め込みモデルをチャットと独立選択**（[#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450) → [#984](https://github.com/digitaldemocracy2030/kouchou-ai/issues/984)）
- **指定カテゴリ分類（所与カテゴリへの意見分類）**（[#994](https://github.com/digitaldemocracy2030/kouchou-ai/issues/994) → [#996](https://github.com/digitaldemocracy2030/kouchou-ai/issues/996)、「その他」受け皿必須）
- **意見ごとの侮辱・ヘイト/政策提案ラベル**（[#975](https://github.com/digitaldemocracy2030/kouchou-ai/issues/975)）、**OpenRouter 無料モデル向け structured outputs fallback**（[#537](https://github.com/digitaldemocracy2030/kouchou-ai/issues/537) → [#985](https://github.com/digitaldemocracy2030/kouchou-ai/issues/985)）
- **クラスタ品質評価ハーネスの再現可能化**（[#143](https://github.com/digitaldemocracy2030/kouchou-ai/issues/143) → [#982](https://github.com/digitaldemocracy2030/kouchou-ai/issues/982)）
- ローカル LLM 対応（`address` に full URL / `LOCAL_LLM_API_KEY`、[#824](https://github.com/digitaldemocracy2030/kouchou-ai/issues/824)）

### WebUI（レポートの読み・作成）
- 散布図: **詳細クラスタタブ＋凸包**（[#798](https://github.com/digitaldemocracy2030/kouchou-ai/issues/798)）、**クラスタ選択の連動**（[#52](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52) → [#983](https://github.com/digitaldemocracy2030/kouchou-ai/issues/983)）、**操作ヒント＋濃い意見グループの帰属可視化**（[#306](https://github.com/digitaldemocracy2030/kouchou-ai/issues/306) → [#986](https://github.com/digitaldemocracy2030/kouchou-ai/issues/986)）、**全画面のまま粒度切替**（[#961](https://github.com/digitaldemocracy2030/kouchou-ai/issues/961)）、ホバー時ラベル非表示（[#812](https://github.com/digitaldemocracy2030/kouchou-ai/issues/812)）
- **レポート再利用機能**（[#769](https://github.com/digitaldemocracy2030/kouchou-ai/issues/769)）、**レポート別に濃いクラスタ初期値を保存**（[#946](https://github.com/digitaldemocracy2030/kouchou-ai/issues/946)）
- **作成 UI から分析方式（LLM 直接グルーピング）を選択**（[#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176) → [#987](https://github.com/digitaldemocracy2030/kouchou-ai/issues/987)）、JSON ダウンロード（[#755](https://github.com/digitaldemocracy2030/kouchou-ai/issues/755)）、作成前の API 接続・コスト確認（[#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) 系）
- 大きな CSV 投入時の無限スピナー修正（[#804](https://github.com/digitaldemocracy2030/kouchou-ai/issues/804)）、空白コメントの事前除去（[#583](https://github.com/digitaldemocracy2030/kouchou-ai/issues/583) → [#796](https://github.com/digitaldemocracy2030/kouchou-ai/issues/796)/[#813](https://github.com/digitaldemocracy2030/kouchou-ai/issues/813)）

### プラットフォーム・配布・デプロイ
- **日本語 Windows 移植性**（[#992](https://github.com/digitaldemocracy2030/kouchou-ai/issues/992)/[#993](https://github.com/digitaldemocracy2030/kouchou-ai/issues/993) → [#995](https://github.com/digitaldemocracy2030/kouchou-ai/issues/995)、`sys.executable`・UTF-8 明示）、Ollama ホストポートを `OLLAMA_HOST_PORT` で変更可（[#952](https://github.com/digitaldemocracy2030/kouchou-ai/issues/952)）
- Azure デプロイの build context / ヘルスチェック改善（[#780](https://github.com/digitaldemocracy2030/kouchou-ai/issues/780)/[#785](https://github.com/digitaldemocracy2030/kouchou-ai/issues/785) ほか）、**Docker Hub 取得失敗時に ECR Public へ切替**（[#969](https://github.com/digitaldemocracy2030/kouchou-ai/issues/969)）
- shell 配布/静的ビューア系（Node runtime 依存の整理、[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) 系）

### ライセンス・セキュリティ
- **AGPL 表記の訂正**と CLI 出力 HTML へのライセンス案内・表示ソース同梱（[#970](https://github.com/digitaldemocracy2030/kouchou-ai/issues/970)）、資源欠如時の link-only degrade（[#978](https://github.com/digitaldemocracy2030/kouchou-ai/issues/978) → [#980](https://github.com/digitaldemocracy2030/kouchou-ai/issues/980)）、analysis-core 0.1.3 で AGPL 版を PyPI 公開（[#981](https://github.com/digitaldemocracy2030/kouchou-ai/issues/981)）。背景は [[analysis-core-license-intent-2026-10-12]] / [[agpl-output-and-plugin-boundaries-2026-10-12]]。
- CVE 対応（依存更新, [#808](https://github.com/digitaldemocracy2030/kouchou-ai/issues/808)）、Dependabot による next 15→16 系ほか依存更新、CodeQL/CodeRabbit・Biome CI 強制（[#817](https://github.com/digitaldemocracy2030/kouchou-ai/issues/817)/[#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)）

### ドキュメント・多言語
- **mkdocs Material ドキュメントサイト新設**（[#754](https://github.com/digitaldemocracy2030/kouchou-ai/issues/754)）＋ repo README 埋め込み・AI assistant ガイド
- **多言語 README**: 韓国語版追加（[#959](https://github.com/digitaldemocracy2030/kouchou-ai/issues/959)）、英語デフォルト化（[#966](https://github.com/digitaldemocracy2030/kouchou-ai/issues/966)）→ UX 懸念で日本語に差し戻し（[#968](https://github.com/digitaldemocracy2030/kouchou-ai/issues/968)）という一件を経て「日本語デフォルト＋言語リンク」に着地（[[readme-anchor-freeze-and-docs-entry-2026-10-13]]）
- **docs 大掃除**（demo-first 入口・nav rot-gate・content gap・責任3レイヤー・self-hosting rename 等）は本リリース末尾（[#998](https://github.com/digitaldemocracy2030/kouchou-ai/issues/998)〜[#1001](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1001)）で着手し、以後 [#1010](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1010) まで継続。詳細は [[kouchou-ai-docs-overhaul-2026-10]]

## コミュニティ

v4.1.0 も従来どおり複数のコントリビュータによるリリース。nishio が大半の PR を主導しつつ、既存の中心的コントリビュータ tokoroten（Docker 縮小・散布図・エラー改善）・shingo-ohki（CI/デプロイ/依存）、新規コントリビュータ 2 名（yasumorishima＝空白コメント除去・shell-build 計画、katsushi2441＝Ollama ポート・韓国語 README）、Copilot/Devin 併用の PR などが含まれる。

> **申し送り（nishio 指示 2026-10-14）**: **v5.0.0 のリリース時には、この v4.0.0~4.1.0 のコントリビュータも「後見者」として credits/謝辞に明示する**こと。v5.0.0 サイクルの新規貢献者だけで終わらせず、前サイクルで土台を築いた人への敬意を欠かさない。全量は `gh release view v4.1.0` / `compare/v4.0.0...v4.1.0` で再取得できる。

## この wiki の関連深掘り

- [[kouchou-ai-docs-overhaul-2026-10]]: 本リリースに含まれる docs 大掃除の総括
- [[pr-982-987-review-round-2026-10-12]] / [[issue-backlog-audit-2026-10-12]]: 2026-10 の棚卸し→並列実装→レビュー→merge の波
- [[analysis-core-license-intent-2026-10-12]] / [[agpl-output-and-plugin-boundaries-2026-10-12]]: AGPL 訂正の背景
- [[broadlistening-tool-ecosystem-vision]]: WebUI=simple / CLI=実験機能 の二段構造（CLI 先行方針の背景）
- [[refactoring-status]]: コア分離・polars 化など基盤リファクタの文脈

## Open Questions

- v4.1.0 は v4.0.0 から ~10 か月・~160 PR と幅が広い。リリース頻度（もっと刻むか）と、マイナー/メジャーの切り方の基準は明文化されていない。
- コントリビュータが継続的に参加する中で、CONTRIBUTING / docs の開発者導線（[[kouchou-ai-docs-overhaul-2026-10]] で着手）と、レビュー・CI ゲートの運用負荷のバランスが今後の論点。
