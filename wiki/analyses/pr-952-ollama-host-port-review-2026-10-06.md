---
type: analysis
summary: "外部PR #952（Ollamaのホスト側ポートを OLLAMA_HOST_PORT で変更可能に）のレビュー判断。ホスト公開ポートとコンテナ間接続先を分けて見る観点、初回コントリビュータPRではCodeQLが承認待ちで走らない点、軽微なdocs追随はmain直接修正で済ませた判断を記録"
sources:
  - source-code.md
---

# PR #952 Ollama ホスト側ポート変更のレビュー（2026-10-06）

外部コントリビュータが立てた Issue #951 と PR #952 を、変更の正しさ・残件・CI の 3 点から見てマージ可能と判断した。2026-10-06 21:30 JST に main `73ce8df` へ反映され、残件の docs 追随は main `a12d68e` へ直接修正した。[[source-code]] より（work clone `fedf67a` 時点で grep）。

## 変更内容

- `compose.yaml` の ollama サービスの `"11434:11434"` を `"${OLLAMA_HOST_PORT:-11434}:11434"` に変更。`.env.example` に `OLLAMA_HOST_PORT=11434` を、README に衝突時の対処を追加した（+7/−2）
- 動機: ホストで既に Ollama が 11434 を使っていると `docker compose --profile ollama up -d` が `address already in use` で起動しない

## レビュー観点: ホスト公開ポートとコンテナ間接続先を分ける

- 変えたのは**ホスト側の公開ポートだけ**で、コンテナ側の 11434 は変わらない。admin / api は `NEXT_PUBLIC_LOCAL_LLM_ADDRESS=ollama:11434`（`apps/admin/app/create/hooks/useAISettings.ts` の既定値も同じ）でコンテナ間通信するため、アプリ側の設定変更は要らない
- 例外として、api / analysis-core には `localhost:11434` という既定値がある（`apps/api/src/services/llm_models.py`、`packages/analysis-core/src/analysis_core/services/llm.py`）。api を Docker 外のホストで動かし、ポートを変えた ollama コンテナへつなぐ場合だけ、UI で接続先を変える必要がある。今回の PR の想定外の構成なので対応は不要と判断した
- 1 か所の値を変える PR でも、同じ値を `git grep` して他の記載との整合を見る。今回はこれで `docs/index.md` のポート一覧表の更新漏れが見つかった

## CI 観測: 初回コントリビュータの PR

- 初めての人の PR では、GitHub Actions（CodeQL）が `action_required` で止まり、メンテナが「Approve and run workflows」を押すまで走らない。PR 画面で緑なのが CodeRabbit だけでも、CI が通ったことにはならない
- ワークフローの承認は人間の attention を使う操作なので、AI エージェントは指摘するだけで実行しない（CLAUDE.md の運用方針）。CodeRabbit の SUCCESS の読み方は [[current-status-2026-10-05]] の「利用上限で未実行」の件と同じ系統の注意

## 軽微な docs 追随は main 直接修正

- `docs/index.md` のポート表に 1 行追記するだけの追随は、西尾の判断で PR を立てずに kouchou-ai main へ直接 push した（`a12d68e`）
- 外部コントリビュータに追加修正を頼むより往復が少ない。ただしこれは表記追随の規模に限った判断で、コードの変更は従来どおり PR を経由する

## Open Questions

- api / analysis-core の `localhost:11434` という既定値を `OLLAMA_HOST_PORT` に追随させる必要があるか。Docker 外で api を動かす開発者が増えたら再検討する
