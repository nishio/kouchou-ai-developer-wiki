---
type: analysis
summary: "Issue #530 の『`server/requirements.txt` を追加すべき』という処方箋は、2026-05-25 時点の current main には合っておらず、現行 repo では API 依存は `apps/api/requirements.lock` と `pyproject.toml` で管理されている"
sources:
  - source-code.md
  - github-dev-docs.md
---

## 問い

`Issue #530` の「Windows 環境で初回セットアップ時に `requirements.txt` が必要」「`server/requirements.txt` に Azure 依存を足せば直る」という主張は、2026-05-25 時点の最新コードに照らして妥当か。[[github-dev-docs]]より [[source-code]]より

## 結論

2026-05-25 に `work/kouchou-ai/` で `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` を確認した限り、`Issue #530` の処方箋は **current main には合っていない**。現行 API は `server/requirements.txt` を読む構造ではなく、`apps/api/Dockerfile` が `apps/api/requirements.lock` / `requirements-dev.lock` を使って依存を入れる。しかも Azure 依存は lock file と `pyproject.toml` に既に含まれ、Windows セットアップの既定 `STORAGE_TYPE` も `local` である。したがって、最新コード基準では「`server/requirements.txt` を新設すれば直る」とは言えない。[[source-code]]より

## Findings

### current main には `server/requirements.txt` という前提自体がない

`origin/main` の API Docker build は `apps/api/Dockerfile` 相当の内容で、`COPY apps/api/pyproject.toml apps/api/requirements.lock apps/api/requirements-dev.lock ...` の後、`uv pip install ... -r requirements.lock` で依存を入れる。`server/requirements.txt` を COPY したり install したりする経路は current main には見当たらない。[[source-code]]より

### Azure 依存は既に `apps/api` 側へ入っている

`apps/api/pyproject.toml` には `azure-storage-blob` `azure-core` `azure-identity` が dependencies として定義されており、`apps/api/requirements.lock` にも `azure-core==1.34.0` `azure-identity==1.22.0` `azure-storage-blob==12.25.1` が lock されている。したがって「Azure 系が requirements に書かれていない」が current main の事実とは一致しない。[[source-code]]より

### ローカル初回セットアップの既定値は Azure ではなく `local`

`setup_win.bat` は `.env` を自動生成する際に `STORAGE_TYPE=local` を書き込む。また `apps/api/src/config.py` でも `STORAGE_TYPE` の default は `local` である。つまり、通常の Windows ローカルセットアップは **Azure Blob を前提にしていない**。issue 本文の「report launcher で Azure Blob を使うから Azure 依存が必須」という説明は、少なくとも current の既定導線とはずれる。[[source-code]]より

### ただし Azure import は unconditional なので、依存注入が壊れれば `ModuleNotFoundError` 自体は起こりうる

`apps/api/src/services/storage.py` は先頭で `from azure.identity import DefaultAzureCredential` と `from azure.storage.blob import BlobServiceClient` を import している。よって、もし Docker build が `apps/api/requirements.lock` を正しく入れていない、あるいは利用者が Docker を使わず別手順で Python 環境を立てたなら `No module named 'azure'` は起こりうる。ただしその場合の current-code 上の論点は、`server/requirements.txt` 不足ではなく **現行依存導線と実際の起動手順の不一致** である。[[source-code]]より

### Windows セットアップの current な現役論点は別 issue / PR に寄っている

2026-05-25 時点の open PR には `PR #863` があり、これは `setup_win.bat` の日本語案内と PowerShell 分離を扱っている。つまり、Windows 導入で maintainers が今見ている current 論点は `requirements.txt` 追加ではなく、セットアップ UX と実行基盤の安定化に寄っていると読める。[[github-dev-docs]]より

## 判断

`Issue #530` は、もし過去の特定 release やローカル改変環境で `ModuleNotFoundError: No module named 'azure'` が出ていたなら、**「依存が入っていない」という観測自体** はあり得る。しかし最新コード基準で見ると、その原因説明を `server/requirements.txt` 欠如に結びつけるのは stale である。current main では依存定義場所が既に `apps/api/pyproject.toml` と lock file へ移っているため、issue の本文は「再現ログの記録」としてはともかく、「修正方針」としては正確でない。[[source-code]]より [[github-dev-docs]]より

## Open Questions

- issue 報告者が実際に使ったのが current source checkout ではなく、当時の release zip だった場合、その配布物に依存欠落や build 不整合があった可能性はある
- `storage.py` の Azure import を lazy import にして、`STORAGE_TYPE=local` では Azure 依存欠落の影響を受けない形へ寄せるべきか
- `setup_win.*` 導線で API コンテナ build failure をどう診断表示するかは、`PR #863` 以後も別途詰める余地がある

## Updates

- 2026-05-25: `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` と open PR を確認し、Issue #530 の current-state 判断として作成
