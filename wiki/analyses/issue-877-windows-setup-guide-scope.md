---
type: analysis
summary: "Issue #877 は Windows setup guide の文言修正だけでなく、Docker Desktop を標準入口にする範囲、組織管理端末で動かない場合の非サポート境界、WSL2 + Docker Engine を別ルートにするかを切り分ける issue として扱うのが妥当"
sources:
  - issue-877-windows-setup-guide-scope-2026-05-29.md
  - docker-desktop-license-2026-05-29.md
  - windows-distribution-options.md
  - docker-engine-wsl2-alternative-2026-05-23.md
  - windows-real-machine-e2e-lessons.md
---

## 結論

`#877` は「Windows setup guide の前提条件とトラブルシュートを current main に合わせる」issue だが、コメントを踏まえると、単なる文言改善では不足する。最初に決めるべきなのは **どの Windows 環境を supported path と呼び、どの環境を beginner guide の外へ出すか** である。[[issue-877-windows-setup-guide-scope-2026-05-29]]より

当面の方針としては、`#877` では Docker Desktop が使える Windows 10/11 を標準入口として整理しつつ、Docker Desktop を入れられない / WSL2 も禁止されている組織貸与 PC は「このガイドの対象外」と明示するのがよい。Docker Desktop 回避策である WSL2 Ubuntu + Docker Engine は、初心者向けガイドに混ぜず、別 issue / 別 docs で上級者・組織管理者向けに切るべきである。[[docker-engine-wsl2-alternative-2026-05-23]]より

## コメントが変えた見方

issue 本文だけを見ると、`OpenAI または Gemini のどちらか一方で可`、Docker Desktop 起動確認、WSL2 初回セットアップ、メモリ不足、貼り付け不能の分岐表を足せば終わるように見える。これは必要だが、コメントは問題を一段上へ引き上げている。つまり、Windows 利用者が多いなら、Unix-like 前提の暗黙知を docs に押し付けないだけでなく、Windows の中でも「Docker Desktop が使える個人 PC」と「組織ポリシーで Docker / WSL が塞がれた貸与 PC」を分ける必要がある。[[issue-877-windows-setup-guide-scope-2026-05-29]]より

この分離をしないと、初心者向け docs が「あり得る全失敗を救う巨大な FAQ」になってしまう。特に Docker Desktop が契約・端末管理ポリシーで使えないケースは、kouchou-ai の setup script だけでは解けない。ここは技術的 troubleshooting ではなく、利用環境の調達・権限・サポート体制の問題として扱うべきである。[[docker-desktop-license-2026-05-29]]より

## #877 でやるべき範囲

`#877` の最小修正は、current main の `docs/getting-started/windows-setup.md` に次の境界を入れることだと考える。

- 標準入口は `Windows 10/11 + Docker Desktop + Linux containers + Docker Desktop を起動できる権限 + OpenAI または Gemini の API key どちらか一方` と明示する。
- 冒頭に「このガイドで解決できる範囲」を置き、Docker Desktop がインストールできない / 起動できない / WSL2 が組織ポリシーで禁止されている場合は、所属組織の IT 管理者または技術者に相談する、と切る。
- トラブルシュート表は supported path 内の失敗に限定する。例: Docker Desktop 未起動、`docker` command not found、WSL2 有効化要求、メモリ不足、API key prefix 警告、localhost にアクセスできない。
- `docs/development/windows-real-machine-setup-verification.md` は「ユーザーが読む追加手順」ではなく、「開発者・AI エージェントが再現確認に使う検証手順」と説明する。

この範囲なら `#877` は docs issue として閉じやすい。逆に、Docker Desktop を使わない WSL2 + Docker Engine 手順まで入れると、systemd、Docker daemon、Windows / WSL path、port forwarding、組織 VPN / セキュリティソフトまで扱う必要が出て、初心者向けガイドのスコープを超える。[[docker-engine-wsl2-alternative-2026-05-23]]より

## #863 との関係

`#863` が merge されると、ユーザーが直接見る入力 UI は `cmd.exe` の `set /p` ではなく `setup_win.ps1` の GUI dialog になる。したがって `#877` の docs 修正は、`#863` の merge 前にやるなら current main 向けの `.bat` 文言、merge 後にやるなら `.bat` launcher + `.ps1` dialog 文言に合わせる必要がある。[[issue-877-windows-setup-guide-scope-2026-05-29]]より

ただし `#863` は文字化け・入力 UI の問題を下げるだけで、Docker Desktop ライセンス、組織管理端末、WSL2 禁止の問題は解決しない。したがって `#877` は `#863` の後続 docs cleanup として進める価値があるが、`#863` に吸収して終わりにするべきではない。[[windows-distribution-options]]より

## ドキュメント構成案

Windows guide の冒頭を、手順から始めず、次のような環境判定にするのがよい。

| 状態 | 案内 |
| --- | --- |
| 個人 PC / Docker Desktop を入れられる / WSL2 有効化できる | このガイドの標準手順へ進む |
| 組織 PC / Docker Desktop の利用可否が不明 | 先に所属組織の IT 管理者に Docker Desktop 利用可否とライセンスを確認する |
| Docker Desktop は不可だが WSL2 Ubuntu は使える技術者 | 初心者向けガイドではなく、別の上級者向け Docker Engine in WSL2 手順へ誘導する。現状は未整備 |
| Docker Desktop も WSL2 も不可 | ローカル Windows 実行はこのガイドの対象外。使える環境を持つ技術者、別 PC、またはホスト済み環境を検討する |

この書き方なら、コメントの「まともに動かない環境で頑張るより、使えるエンジニアを雇う方が現実的」という判断を、ユーザーに冷たく見えにくい形で docs に落とせる。重要なのは、ユーザーを突き放すことではなく、初心者が自分の権限では解けない問題に時間を溶かさないよう境界を明示すること。[[issue-877-windows-setup-guide-scope-2026-05-29]]より

## Open Questions

- `#877` の実装順は `#863` merge 後にするか、current main で先に docs boundary だけ入れて後で rebase するか。
- Docker Desktop 回避ルートを公式 docs にするなら、誰が WSL2 Ubuntu + Docker Engine で `compose up` まで実機検証するか。
- 非専門家向け Windows 体験の最終ゴールを、`setup_win.*` で止めるのか、Docker Desktop を操作する launcher exe まで進めるのか。
- 自治体・大企業向けにはローカル Windows setup より、クラウド / managed deployment を主導線にした方がよい場面があるか。

## Updates

- 2026-05-29: 初回作成。Issue #877 とコメント、Docker Desktop ライセンス公式確認、current main docs、関連 PR #863 を踏まえ、Windows guide のサポート境界を整理した。
