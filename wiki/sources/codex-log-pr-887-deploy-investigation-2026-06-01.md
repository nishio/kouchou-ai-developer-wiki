---
title: "Codex ログ: PR #887 デプロイ調査 2026-06-01"
type: source
summary: "2026-06-01 17:47 / 19:33 (月曜日) の Codex 2 ターン会話ログ。nishio の「直ってなくないですか？」「az login したけど見れるようになった？」というひと言の問いに対し、Codex が false positive の根拠 (Turn 1) と SIGKILL/OOM の根拠 (Turn 2) を順に返した、runtime build 撤去エピソードの起点ログ"
sources:
  - codex-log-pr-887-deploy-investigation-2026-06-01.txt
---

# Codex ログ: PR [#887](https://github.com/digitaldemocracy2030/kouchou-ai/issues/887) デプロイ確認 2026-06-01

## このソースについて

2026-06-01 (月曜日) の 17:47 と 19:33 に行われた、nishio と Codex の 2 ターン会話ログ。raw は `raw/codex-log-pr-887-deploy-investigation-2026-06-01.txt`。

## Turn 1: 17:47

**nishio**:

> プロダクションデプロイ完了したっぽいけど直ってなくないですか？

**Codex** (9m 18s 作業):

> はい、直ってないです。
>
> 確認したところ、PR [#887](https://github.com/digitaldemocracy2030/kouchou-ai/issues/887) は merge 済みで Azure Deployment も success ですが、本番 stable URL はまだ旧 CSP を返しています。`script-src` に `'unsafe-eval'` が入っておらず、Playwright でも `.no-webgl` overlay が visible のままでした。
>
> 原因はデプロイ確認の false positive っぽいです。Actions log では `latestRevisionName`（最新 revision）は進んでいる一方、`latestReadyRevisionName`（Ready な revision）は旧版のまま。deploy confirmation が stable root の 200 を見て成功扱いにしていて、新 revision が Ready になったことは確認していません。

## Turn 2: 19:33

**nishio**:

> az login したけど見れるようになった？

**Codex** (2m 52s 作業):

> はい、見れるようになりました。結論はかなり明確です。
>
> 新 revision が Ready になっていません。最新 revision は deploy されているのに、Ready なのは旧 revision のままでした。
>
> revision health は Unhealthy / Degraded で、replica が起動完了していない状態（progress deadline 超過）でした。
>
> 原因も判明しました。startup 時の `pnpm run build`（`next build`）が TypeScript チェックの途中でメモリ不足により Killed され、コンテナは exit 137（SIGKILL）で終了していました。
>
> つまり **起動時 `next build` が ACA の public-viewer コンテナのメモリ上限で OOM kill されています**。そのため `next start` まで到達せず、HTTP listen しないので Ready になりません。

<!-- 公開境界 sanitize（2026-10-12, [[wiki-self-audit-2026-10-12]]）: 具体的な revision ID・replica health JSON・コンテナログ・resource サイズは公開 wiki から除去。sanitize 前 verbatim は Google Drive「広聴AI-Azureデモ環境」で管理（local 退避: raw/deploy-detail-preservation/）。 -->

## この 2 ターンが示しているもの

- 起点は常に人間側の観察と短い問い ("直ってなくないですか？" / "az login したけど見れるようになった？") で、Codex はそれを受けて裏取りと細部を返している
- Turn 1 (9m18s) では `latestRevisionName` と `latestReadyRevisionName` の食い違い + Playwright で `.no-webgl` overlay 残存 + 旧 CSP header 残存、の 3 点を独立に確認して「false positive」と整理
- Turn 2 (2m52s) では Azure access 権限が通った直後、revision health（Unhealthy / Degraded、replica 未起動）→ 起動時 `next build` の OOM Killed → exit 137（SIGKILL）、を順に並べて「起動時 build が OOM で SIGKILL されている」と特定。ここで初めて「画面が変わらない」の真の原因 (新 revision が Ready にならない) が判明
- 2 ターン合計 12 分で、「success と表示された理由」と「画面が変わらない理由」がそれぞれ別の根拠で接続された。前者は deploy confirmation の judging criteria、後者は startup build の OOM

## どこで使われたか

- [[deploy-success-but-nothing-changed-story-2026-06-01]] 第 1-2 節の発端として引用
- [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] 第 2 ステップの観測根拠として引用
- [[pr-887-production-deploy-observation-2026-06-01]] の deploy false positive 議論の一次観測

## Open Questions

- この 1 ターンに続く Codex とのやりとり (SIGKILL 発見、`#821` への遡及、archeology) は別ログとして残すか、wiki の analysis ページ側に書ききるか
- 「直ってなくないですか？」のような短い問いから Agent が複合観測を返せた条件 (CLAUDE.md の live state 観測ルール、past PR 番号の事前 indexing 等) を、別途 [[wiki-driven-workflow]] に集約するか

## Updates

- 2026-06-02: 初版作成。runtime build 撤去エピソードの起点として、1 ターン会話ログを source ページ化。
- 2026-10-12: 公開境界（CLAUDE.md）に合わせ、具体的な revision ID・replica health JSON・console/system コンテナログ・resource サイズを除去し、設計の教訓（deploy 判定基準の誤り／起動時 build の OOM SIGKILL）を残す形へ sanitize。verbatim は `raw/deploy-detail-preservation/`（local）に退避し一次置き場は Google Drive「広聴AI-Azureデモ環境」。[[wiki-self-audit-2026-10-12]]
