---
type: analysis
summary: "issue #898 aarch64 Docker / UMAP Illegal instruction は PR #899 merge 済みだが、close には Apple Silicon Docker での解消確認または確認不能時の明示判断が必要"
sources:
  - source-code.md
  - github-dev-docs.md
  - current-status-2026-06-30.md
---

## Snapshot

issue #898 は、aarch64 環境の Docker でレポート生成中に `import umap` が `Illegal instruction` で落ちる bug。2026-06-30 確認時点で open、assignee は nishio。PR #899 (`[codex] aarch64 Docker向けに Numba CPU target を generic にする`) は 2026-06-05 に merge 済みで、merge commit は `d5c9ece`。[[current-status-2026-06-30]]より

PR #899 の方針は、`NUMBA_DISABLE_JIT=1` で JIT を丸ごと止めるのではなく、Numba JIT の CPU target を `NUMBA_CPU_NAME=generic` に固定するもの。クラスタリング実装や UMAP 経路は変更していない。[[source-code]]より

## Current Main

`work/kouchou-ai/main@d5c9ece` では、次の 4 箇所に `NUMBA_CPU_NAME=generic` が入っている。[[source-code]]より

- `.env.example`
- `compose.yaml`
- `setup_mac.sh`
- `setup_linux.sh`

PR #899 本文では、確認済みは macOS arm64 の既存 venv で `NUMBA_CPU_NAME=generic` が Numba に読まれ `import umap` が成功することまで。未確認として、Linux/aarch64 Docker コンテナ内での再現・解消確認と、`docker compose up --build` からのレポート生成完走確認が残っている。

issue #898 側には、2026-06-05 の original report と「`NUMBA_DISABLE_JIT=1` は可能なら避けたい」という補足コメント以降、PR #899 merge 後の aarch64 Docker 解消確認コメントはまだない。

## Close Readiness

今すぐ close するには根拠が足りない。PR #899 は正しい方向の最小修正だが、issue の再現環境は Docker/aarch64 であり、merge 前にそこは未確認と明示されている。

close 判定に必要な根拠は次のどれか：

- Apple Silicon など aarch64 Docker で `docker compose up --build` 後に issue #898 の手順を再実行し、レポート生成がクラスタリング以降へ進む。
- API container 内で `python -c "import numba; print(numba.config.CPU_NAME); import umap; print(umap.UMAP)"` が `generic` を表示して成功し、さらに実レポート生成も通る。
- 実機確認できない場合は、issue 上で「PR #899 は merge 済み、未確認条件はこれ」と明示し、original reporter / aarch64 環境を持つ人に確認を依頼する。AI エージェント単独で close しない。

## Safe Next Steps

- 実装には入らず、まず issue #898 に残す確認観点を短くまとめる。
- aarch64 実機を使える人がいるなら、上の 2 コマンド / レポート生成確認を依頼する。
- 確認できたら issue #898 を close。確認不能なら「pending validation」として残す。

## Open Questions

- aarch64 Docker の再現環境を誰が持っているか。Apple Silicon local Docker で十分か、Linux/aarch64 container まで必要か。
- `NUMBA_CPU_NAME=generic` による性能影響をどこまで見るか。今回の close 条件はまず crash 回避でよいのか。

## Updates

- 2026-06-30: 初回作成。issue #898、PR #899、`work/kouchou-ai/main@d5c9ece` の `NUMBA_CPU_NAME` 反映箇所を確認した。
