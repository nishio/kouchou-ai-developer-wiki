---
type: source
summary: "2026-10-05 Slack #2_開発_広聴ai で大木真吾が、自治体内で流用可能な Windows 11 PC に WSL2 + `./start_linux.sh`（Docker Desktop を使わず WSL2 内の Docker Engine）で広聴AIを動かせたと報告し、nishio も Docker Desktop を推奨から外す方向に同意した"
sources:
  - slack-logs mirror (#2_開発_広聴ai, 2026-10-05)
---

## 何のソースか

`digitaldemocracy2030/slack-logs` の `mirror/`（synced_at 2026-10-06T13:09Z、直近 75 日窓）から読んだ #2_開発_広聴ai の 2026-10-05 のやりとり。最終読解日 2026-10-06。`raw/` への固定 snapshot はまだない。

## 内容

- 大木真吾が「自治体内で自由に広聴AIを使えるように」、自治体内で流用可能な Windows 11 ノート PC に広聴AIをセットアップした。すぐには PR を出せないため、本体に返せそうな項目だけをメモした
  - レポート生成時のモデル選択に付いている「（未検証）」ラベルは、いくつか外せそう。少なくとも o4-mini は動いた
  - 自治体 PC に Docker Desktop を導入するのは適切でないと感じた。マニュアル上は非推奨となっている WSL2 + `./start_linux.sh` で十分動くので、推奨手順を考え直してよいのでは
- nishio の返答: WSL 3 の話もある。Docker Desktop は個人開発なら無料で手軽だったが、自治体では最初から有料というのは盲点だった。おすすめの方法から外していく方向でもよさそう

## 読解上の注意

- `start_linux.sh` / `setup_linux.sh` は中で `docker compose up` を呼ぶ。したがって報告された構成は **Docker を使わない構成ではなく、WSL2 Ubuntu 内の Docker Engine で compose を動かす構成**（[[windows-distribution-options]] のルート B）と読むのが自然。Docker Engine の入れ方は Slack には書かれていない
- 「マニュアル上非推奨」の出典は特定できていない。current main（`a12d68e`）で「非推奨」と明記されている Windows 手順は、Docker を使わない `docs/repo-readmes/experiments/direct-win.md` だけ。`docs/getting-started/windows-setup.md` は WSL 内での手動構築を「扱いません」としており、非推奨ではなく対象外の扱い

## Updates

- 2026-10-06: 初版作成。ルート B の実機成功の初報として [[windows-distribution-options]] に反映
