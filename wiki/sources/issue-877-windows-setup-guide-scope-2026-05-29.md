---
type: source
summary: "GitHub issue #877 とコメントの観測。Windows setup guide の API key / Docker Desktop / WSL2 / メモリ不足分岐を整理する issue だが、コメントにより Docker Desktop ライセンス・組織管理端末・生 Windows サポート境界の論点へ広がっている"
sources:
  - github-dev-docs.md
  - source-code.md
  - docker-desktop-license-2026-05-29.md
---

## 何のソースか

2026-05-29 13:31 JST に `gh issue view 877`、GitHub connector の issue comment fetch、`gh pr list` / `gh pr view 863`、および `work/kouchou-ai/` の current main `6955202` を確認した観測メモ。対象は GitHub issue `#877`「[DOCUMENT] Windows セットアップガイドの前提条件と失敗時の分岐を current main に合わせて整理する」。

## Issue #877 の本文

`#877` は open の documentation issue で、assignee はまだいない。本文の中心は、`docs/getting-started/windows-setup.md` が一般ユーザー向け入口として重要な一方で、前提条件と手順の表現がずれていること。具体的には、前提条件では OpenAI API key と Gemini API key が並列に必須のように見えるが、手順ではどちらか一方でよいと書いている。[[github-dev-docs]]より

同 issue は、Docker Desktop / WSL2 / メモリ不足 / 貼り付け不能などの詰まりどころについて、症状別の分岐が弱いとも指摘している。完了条件は、初見 Windows ユーザーが最小条件を誤解しないこと、`setup_win.bat` 実行前後の確認点が明確なこと、Docker Desktop / WSL2 / メモリ不足 / API key 入力ミスの切り分け導線があること、一般ユーザー向けガイドと開発者向け実機検証ガイドの住み分けが明示されること。[[github-dev-docs]]より

## コメントで追加された論点

コメントは、Windows setup docs を単なる FAQ 整理としてではなく、kouchou-ai の利用者層とサポート境界の問題として再定義している。要点は、Unix-like 環境を暗黙前提にしてきたが、実際には Windows マシンで使いたい利用者が多く観測された、ということ。[[github-dev-docs]]より

コメントはさらに、Windows で「Docker か WSL を使えば動く」という説明の中で、もっとも楽な Docker Desktop ルートにはライセンスと端末管理ポリシーの問題があると指摘している。Docker 公式文書を確認しても、大規模 enterprise の商用利用や government entity では paid subscription が必要になり得るため、この懸念は current docs に反映すべき実務論点である。[[docker-desktop-license-2026-05-29]]より

もう一つの論点は、非エンジニア向けの組織貸与 PC では Docker Desktop も WSL もインストール・起動できない場合があること。この場合、kouchou-ai 側が技術的 workaround を初心者向け docs に積むより、使える環境を持つ技術者・管理者に依頼する方が現実的ではないか、という判断がコメントに含まれる。[[github-dev-docs]]より

## 関連する current state

`work/kouchou-ai/` は 2026-05-29 13:31 JST 時点で `origin/main@6955202` に同期済み。current main の `docs/getting-started/windows-setup.md` は Docker Desktop を標準入口とし、前提条件に OpenAI API key と Gemini API key を並べている。一方、手順ではどちらか一方でもよいと書いている。[[source-code]]より

`#860` は closed で、`docs/development/windows-real-machine-setup-verification.md` には Windows 実機または self-hosted runner で Docker Desktop + `setup_win.bat` を検証する手順が入っている。これは開発者・AI エージェント向けの検証手順であり、一般ユーザー向け入口とは役割が違う。[[github-dev-docs]]より [[source-code]]より

Windows setup の関連 open PR として `#863`「Windows setup の日本語案内を PowerShell に分離」が残っている。`#863` は `setup_win.bat` を薄い ASCII launcher にし、`setup_win.ps1` に日本語案内と入力処理を移す。checks は green だが、作者コメントでは Windows 実機検証が未完了とされている。[[github-dev-docs]]より

`#877` 自体に紐づく open PR は見つからなかった。Windows 関連の open issue としては、文字化け issue `#731` が残り、`#863` がその対応 PR として open のまま。[[github-dev-docs]]より

## Open Questions

- `#877` は current main の `.bat` ベース docs を修正するのか、`#863` merge 後の `.bat` + `.ps1` 導線を前提にするのか。
- Docker Desktop が使えない組織端末を「非サポート」と明記するのか、「上級者向け WSL2 + Docker Engine ルート」へ誘導するのか。
- Windows 初心者向けガイドに、Docker Desktop ライセンス確認をどの程度まで書くべきか。

## Updates

- 2026-05-29: 初回作成。Issue #877 本文、コメント、current main docs、関連 issue / PR の状態を観測して整理した。
