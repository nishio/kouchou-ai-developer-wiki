---
type: analysis
summary: "PR #887 の deploy success false positive を起点に、public-viewer の runtime build 撤去 (PR #888) と Dependabot 対応 (PR #889) まで 1 日で連続実行した過程を、PR 番号と検証ステップ込みで時系列に並べた技術エピソード資料"
sources:
  - pr-887-production-deploy-observation-2026-06-01.md
  - public-viewer-runtime-build-history-2026-06-01.md
  - public-viewer-build-serve-split-refactor-plan-2026-06-01.md
  - issue-887-scattergl-csp-regression-2026-06-01.md
  - github-dev-docs.md
  - meeting-minutes.md
---

# PR 887 から PR 888 へ: runtime build 撤去エピソード 2026-06-01

## このページの目的

2026-06-01 の一日で起きた「PR #887 を merge したのに画面が変わらない」から、`public-viewer` の runtime build 撤去 (PR #888) と Dependabot 対応 (PR #889 draft) まで連続実行された一連の流れを、PR 番号と検証ステップ込みの技術資料として時系列に固定化する。

このページは資料寄りの記録であり、前提知識ゼロの読者向けに同じ出来事をストーリーで読みたい場合は [[deploy-success-but-nothing-changed-story-2026-06-01]] を参照する。個別の技術詳細は [[pr-887-production-deploy-observation-2026-06-01]] / [[public-viewer-runtime-build-history-2026-06-01]] / [[public-viewer-build-serve-split-refactor-plan-2026-06-01]] / [[issue-887-scattergl-csp-regression-2026-06-01]] に分けて固定化済みで、このページはそれらをつなぐメタ視点を残す。

## エピソード

### 1. 観測のズレ

環境のバグ報告 → 修正 PR #887 (Plotly `scattergl` のための CSP `unsafe-eval` 追加) → nishio が merge → GitHub Actions が deploy success → 画面更新 → 変わっていない。

### 2. Codex への問いかけと初動の Azure live state 観測

2026-06-01 17:47 (月曜日)、nishio が Codex に投げたのは 1 行だけだった。

> プロダクションデプロイ完了したっぽいけど直ってなくないですか？

Codex は 9m 18s 作業して次を返した。

> はい、直ってないです。確認したところ、PR #887 は merge 済みで Azure Deployment も success ですが、本番 stable URL はまだ旧 CSP を返しています。`script-src` に `'unsafe-eval'` が入っておらず、Playwright でも `.no-webgl` overlay が visible のままでした。原因はデプロイ確認の false positive っぽいです。Actions log では `latestRevisionName` は `public-viewer--0000166` まで進んでいる一方、`latestReadyRevisionName` は旧 `public-viewer--0000163` のまま。deploy confirmation が stable root の 200 を見て成功扱いにしていて、新 revision が Ready になったことは確認していません。

この時点で、(1) 本番 CSP は旧版のまま、(2) Playwright で WebGL overlay が visible、(3) deploy confirmation は stable root の 200 だけ見ていて新 revision の readiness を見ていない、の 3 点が裏取り済みで返ってきた。raw artifact は [[codex-log-pr-887-deploy-investigation-2026-06-01]] に保存。

Wiki 価値: 「main / open PR だけでは拾えない live state を見にいけ」「公開 wiki にはサニタイズ版だけ残せ」という運用ルールが CLAUDE.md にあったので、Codex 側も live 確認とその記述境界の両方を迷わず実行できた。

### 3. workflow の判定条件を特定

Azure Deployment workflow は `latestReadyRevisionName` を見ておらず、stable URL の 200 だけで success にしていた。判定そのものに bug がある、と整理。

### 4. 「今回固有か」を遡及検証

過去の successful Azure Deployment logs を `gh` で順に確認し、同じ false positive が少なくとも `#821` (2026-04-11) まで遡れることを確認。「今回のために壊れたのではなく、ずっと壊れていた」と整理。

Wiki 価値: 「`#821` も SIGKILL の証拠か？」と一旦書きかけたあと、revision metadata を見て「ただの readiness lag であって SIGKILL とは断定できない」と訂正できた。filing-back の log がそのまま訂正履歴になっている。

### 5. `az login` 後の Codex Turn 2 で OOM/SIGKILL を特定

2026-06-01 19:33、nishio が `az login` 完了を Codex に伝える。

> az login したけど見れるようになった？

Codex は 2m 52s で次を返した。

> `public-viewer--0000166` は Ready になっていません。revision health は `Unhealthy / Degraded / 0/1 replicas ready`。console log の `pnpm run build` は `next build` → `Compiled successfully in 11.5s` → `Running TypeScript ...` → `Killed`。system log の最後は `Container 'public-viewer' was terminated with exit code '137'`。137 は SIGKILL なので、起動時 `next build` が ACA の `cpu: 0.5, memory: 1Gi` でメモリ不足 kill されている。そのため `next start` まで到達せず、HTTP listen しないので Ready にならない。

ここで初めて「画面が変わらない」の真の原因が確定する。新 revision はそもそも Ready になっていない、なぜなら起動時 build が OOM で殺されるから。raw artifact は [[codex-log-pr-887-deploy-investigation-2026-06-01]] Turn 2。

その後、約 2 時間後に `public-viewer--0000166` は self-recover して Ready になった。「OOM」と「container 起動時に build」の組み合わせが原因と判明。

### 6. なぜ container 起動時に build しているのか、git history を archeology

`PR #8` (2025-03 の初期 Docker 化) で `entrypoint.sh` に「build 時に APIサーバーを参照するため、APIサーバーの起動を待ってから build を行う」というコメントとともに導入されていた、と発掘。

### 7. 以降の延命策の系譜を整理

`#746` (monorepo)、`#780/#782` (Docker context)、`#784` (turbopack root)、`#785` (health check retry 6→15)、`#828/#835` (build-time API 依存)、`#851/#862` (shared copy 漏れ) — すべて「runtime build を温存したまま成立条件を足す」延命だったと判明。

Wiki 価値: [[public-viewer-runtime-build-history-2026-06-01]] を新規作成し、「なぜ沼か」「誤解しやすい点」を 1 ページに固定化。次に誰が触っても同じ archeology を繰り返さなくて済むようになった。

### 8. 2026-06-01 定例議事録と照合

同じ問題が定例でも「問題1: チェックがおかしい」「問題2: 時々 OOM で死ぬ」の二層として共有され、暫定 memory 2Gi → deploy CI 改善 → build/serve 分離、の順序が示されていたと確認。Agent の独立調査と人間側の議論が同じ結論に収束していると確認できた。

### 9. Next.js docs を読み実装スケッチを作成

`generateStaticParams()` を空、`connection()` で request-time 化、`NEXT_PUBLIC_OUTPUT_MODE=export` の時だけ build-time API fetch、という分岐方針を [[nextjs-dynamic-build-docs-2026-06-01]] に固定化。

### 10. 段階的リファクタ計画を作成

[[public-viewer-build-serve-split-refactor-plan-2026-06-01]] を作成。Phase 0 baseline → Phase 1 dynamic build API-less → Phase 2 Docker image build へ移動 → Phase 3 CI regression → Phase 4 Azure readiness → Phase 5 resource 再評価、と PR split と合格条件を明文化。

Wiki 価値: いきなり実装に入らず、Wiki に計画ページを残してから実装に入る。後工程の reviewer も「何を意図したか」を Wiki で読める。

### 11. Phase 0 baseline 再現

API なし `pnpm --filter @kouchou-ai/public-viewer build` が `/` / `/faq` の static generation timeout で止まることを実測。失敗 mode を記録。

### 12. PR #888 として実装

`codex/public-viewer-build-serve-split` branch / PR #888 で、dynamic build API-less 化、static export build を fixture API ありで分離、Dockerfile に build stage、entrypoint を `next start` のみに。

### 13. 実装中の判断: `[slug]` には `connection()` を採用しない

`/example` が `DYNAMIC_SERVER_USAGE` で 500 になるため、`generateStaticParams() => []` と fallback metadata、runtime env 読み (`process.env[key]`) で request 時 API を読む形に妥協。

Wiki 価値: 「採用しなかった選択肢とその理由」が計画ページの Updates に残る。後で「なぜ `[slug]` だけ違うのか」と聞かれても answer が固定化されている。

### 14. ローカル検証

Jest 94 件、API-less dynamic build、static export build、runtime smoke (`/`, `/faq/`, `/example/`) を確認。

### 15. CI green

PR #888 CI で API-less dynamic build、static export build、Docker build がすべて green。

### 16. CodeRabbit review への対応

CodeRabbit が `/` の dynamic metadata fallback を指摘 (「fallback だと reporter-specific title が失われる」)。指摘の妥当性を独立検証し、`/` の `generateMetadata()` は `connection()` で request-time 化できると確認、reporter-specific title を復元。`[slug]` は #13 の理由で fallback metadata 維持と決定し、その判断も計画ページに追記。CodeRabbit thread は resolved。

### 17. PR #888 merge 後の deploy 再観測

Azure Deployment は 7m41s で success、今回は `/example` を実際に開いて scattergl が描画されることまで確認して deploy 完了。`#887` 直後の「success と言うけど直っていない」状態は再現せず、起動時 build 撤去の効果として観測。

### 18. Dependabot alerts へ着手

GitHub Security の Dependabot alerts (`security/dependabot`) を live state として観測し、npm transitive dependency 群を patched version に寄せる draft PR #889 `[codex] Dependabot npm alerts に対応する` を作成中。

Wiki 価値: 「main / open PR / issue だけでは security alert を拾えない」「公開 wiki / PR 本文には脆弱性詳細を転記せず、対応 issue / PR / 優先度判断だけ残す」という運用方針を CLAUDE.md / [[wiki-driven-workflow]] / [[codeql-introduction-context]] に同日 filing-back していたので、PR 本文も「公開 PR 本文には alert の詳細内容は転記せず、依存更新の範囲だけを記載」と境界を明示する形で書けた。

### 19. PR #889 の検証範囲

`pnpm audit --json` → vulnerabilities 0、`public-viewer` Jest 94 件、`admin` Jest 111 件、`static-site-builder` build、`git diff --check` をすべて通した上で draft 維持。`pnpm lint` は差分外の既存指摘で落ちるため、この PR では触らないと明示。

## Wiki つき Coding Agent 視点での総括

- **live state 観測と公開境界の同時運用**: Azure revision を直接見て切り分けつつ、公開 wiki にはサニタイズ版だけを残せる
- **「今回固有か / もっと前からか」の遡及検証**: 過去 Actions logs を遡って「`#887` 固有の regression ではない」と確定させ、無駄な focus を防いだ
- **沼の archeology の固定化**: 2 時間の git history 調査を Wiki ページに 1 回固定化したので、次の人は読み返すだけで済む
- **計画 → 実装 → review 反映を 1 日で**: 計画ページが先にあるので、実装中の妥協 (`[slug]` に `connection()` を採用しないなど) や review 反映 (`/` の metadata 復元) も「計画への追記」として一貫した記録になる
- **人間側の議論との合流確認**: 独立に調査した結論と、同日定例で共有された方針が一致したことを Wiki で照合し、議論の重複や乖離を避けられた
- **同日内の方針 filing-back の即時再利用**: 公開境界 (デプロイ詳細・脆弱性詳細を公開 wiki に書かない) は同じ日の中で運用ルールとして filing-back され、即 PR #889 の本文方針として再利用された

## なぜこれが Wiki なしだと難しいか

- 「runtime build がいつから入っているか」「以降の PR がそれをどう延命してきたか」は、`git log` だけで集めることはできるが、毎回 2 時間かけて再現する作業になる。Wiki に固定化して初めて、次のセッションが「読み返すだけ」で済む
- 「`#821` も SIGKILL の証拠か？」のような途中の誤読は、log がなければ翌日に同じ誤読が再発する。filing-back の log entry は「いったん書いて訂正した」過程ごと残せる
- 「公開 wiki に何を書かないか」のような運用ルールは、コード側には encode できない。CLAUDE.md と log.md の 7 日窓に置いて初めて、同日に新しい PR (#889) の本文方針として再利用できる
- 「定例で共有された方針」と「Agent の独立調査」が同じ結論に収束したかどうかは、議事録 wiki ([[meeting-report-2026-06-01]]) と analysis ページの両方を持っていないと突き合わせられない

## Open Questions

- 計画ページ ([[public-viewer-build-serve-split-refactor-plan-2026-06-01]]) の Phase 4 (Azure deploy readiness) と Phase 5 (memory 2Gi → 1Gi 再評価) は未実施。これらが完了したらこのエピソードページにも追記するか、別エピソードとして切るか
- このエピソードを外部発信用に書き直すとき、公開 wiki の境界 (resource 値・revision 名・実環境 URL なし) で十分に伝わるか
- 「Wiki なしだと難しい」の節は、Wiki 運用を持たない読者にとって本当に説得力があるか。具体的な「Wiki なしで同じ調査を再現したらどれくらいかかるか」の対比を入れた方がよいか

## Updates

- 2026-06-01: 初版作成。PR #887 deploy success false positive 観測から、runtime build archeology、計画作成、PR #888 実装と CodeRabbit 反映、deploy 再観測、PR #889 draft 着手までを Wiki つき Coding Agent 視点で記録。
- 2026-06-01: ストーリー版を [[deploy-success-but-nothing-changed-story-2026-06-01]] に分離。こちらは PR 番号・検証コマンド込みの資料寄りページとして維持。
