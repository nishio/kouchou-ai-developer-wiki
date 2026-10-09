---
type: analysis
summary: "public-viewer の Biome 全体 lint が main で落ちている 7 件の由来と、2025-04 の導入初日から一度も CI / hook で強制されず、PR ごとに「触ったファイルだけ clean」で積み上がった構造"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/961
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/270
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/264
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/502
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/700
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/701
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/734
  - source-code.md
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/962
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/963
---

## 問い

PR #961 の動作確認欄に「既知: Biome の全体 lint（`pnpm --filter @kouchou-ai/public-viewer lint`）は main 時点から残っている別ファイルのエラーで失敗する。本 PR の変更・新規ファイルはすべて clean」とある。何が落ちていて、なぜこの状態が放置されたのか。

2026-10-09 に `work/kouchou-ai/` main `a12d68e`（Biome 1.9.4）で観測。

## 現状: 7 件、5 ファイル、すべて機械的に直せる

| ファイル | 種別 | 持ち込んだ commit / PR | 日付 |
| --- | --- | --- | --- |
| `apps/public-viewer/tsconfig.json` | format（配列の展開） | `5e8ca85` / PR #769 (nishio) | 2026-02-04 |
| `app/faq/Contact.tsx` | format（124 文字で lineWidth 120 超過） | `53cdfa8` / PR #769 (nishio) | 2026-02-04 |
| `components/charts/plugins/scatter.tsx` | format | `6bfbd13` / PR #798 (tokoroten) | 2026-02-22 |
| `components/report/DisplaySettingDialog.tsx` | format | `6bfbd13` / PR #798 (tokoroten) | 2026-02-22 |
| `components/report/attributeFilterUtils.ts` | format | `83cfaed` / PR #811 (tokoroten) | 2026-03-02 |
| `app/utils/__tests__/shell-data.test.ts` 83, 88 行 | lint `performance/noDelete` × 2 | `77fd96d` / PR #935 (yasumorishima) | 2026-09-09 |

admin は別に 7 件、dummy-server は 9 件落ちている。root の `pnpm lint` は `apps/api/.venv` 配下まで舐めて 1113 件になるので、root からの全体 lint は実質使われていない。

### 個別の注意

- **tsconfig.json は人が崩したのではない**。PR #769 の diff は `jsx: preserve → react-jsx`、`.next/dev/types/**/*.ts` の追加と同時に配列が展開されており、Next.js 16 が `next dev` / `next build` 時に tsconfig.json を自動書き換えした痕跡。admin の tsconfig.json も同じ日に同じパターンで崩れている。`biome check --write` で畳んでも次に Next.js が触れば戻るので、`biome.json` の `files.ignore` に `tsconfig.json` を入れるのが筋
- **Contact.tsx** は 2025-09-04 に `npm run format` 済みだったが、2026-02-04 に `src=` を `getImageFromServerSrc(...)` で包んだ 1 行が 124 文字になった。format をかけ直さなかっただけ
- **shell-data.test.ts の `noDelete`** は Biome が FIXABLE と出すが、提示される unsafe fix `process.env.X = undefined` は Node では文字列 `"undefined"` が入るため、「未設定」を試すテストの意味が変わる。`--unsafe` で機械適用してはいけない。`biome-ignore` コメントか `Reflect.deleteProperty` で逃がす

## 時系列: いつから落ちているか

歴代 main の snapshot に現行 Biome 1.9.4 をかけた結果（`git worktree` で確認）。

| 日付 | main | viewer のエラー数 | 備考 |
| --- | --- | --- | --- |
| 2025-04-10 | `d5d861a` PR #270 merge | 0 | lefthook 導入 |
| 2025-05-14 | `2f027fe` PR #511 merge | 0 | #502 の一括修正直後 |
| 2025-09-25 | `8508ecb` | 1 | #706 の一括修正後に Header.tsx が 1 件残存 |
| 2026-01-19 | `1c18e71` monorepo 移行 | 0 | 移行作業で掃除された |
| 2026-01-23 | `8920e0d` | 1 | `type.ts` |
| 2026-02-05 | `cb85b9e` | 4 | PR #769 で tsconfig / Contact が落ち始める |
| 2026-02-22 | `b075fe2` | 9 | PR #798 |
| 2026-03-02 | `0e42748` | 10 | PR #811 |
| 2026-06-01 | `3c5d1f0` | 5 | 5〜6 月の nishio の build 整理で page.tsx / next.config.ts 等は消えた |
| 2026-09-09 | `751e2c8` | 7 | PR #935 で noDelete が 2 件追加 |
| 2026-10-09 | `a12d68e` | 7 | 現在 |

つまり「main が clean だった最後」は 2026-01-19 で、そこから 2 月に 3 つの PR が連続して崩し、以後 8 か月間 5〜10 件の間を上下している。一括で 0 にしたのは #502 → PR #508/#511（2025-05、nasuka / 大木）、#701 → PR #706（2025-09、mochizuki-pg）、monorepo 移行（2026-01、nishio）の 3 回で、いずれも「気づいた人が手で一掃」であり、再発防止の仕組みは入っていない。

## なぜ放置されたか

### 1. 強制する場所がどこにもない（導入初日から）

- lefthook（PR #270、2025-04-10、shgtkshruch）は Biome 系 3 コマンドすべてに **初版から `skip: true`**。意図は PR 本文に明記されていて、「server 側の開発者に弊害が出ないよう opt-in にし、良さそうなら default on に変えてもよい」。その「変えてもよい」は 1 年半経っても起きていない。有効化には各自が `lefthook-local.yml` を書く必要があり、CONTRIBUTING はそれを案内しているが、書いている人がいるかは観測できない
- `.github/workflows/` に Biome を走らせる workflow は **一度も存在したことがない**（git 履歴全体で `.github` に `biome` の文字列が出ない）。`client-build.yml` は build と docker build だけ
- CodeRabbit の設定（`.coderabbit.yaml`）も `auto_review.drafts: false` のみで、lint ツールの指定はない
- 唯一の gate 候補だった **Issue #264「GitHub Actions で Biome の lint, format のチェックを実行する」（2025-04-08 起票）は、2025-04-19 に nasuka がコメントも紐付け PR も無しで COMPLETED として close** している。実装は入っていないので、PR #270 の lefthook 導入で「代替された」と見なしたのが最もありそうな説明。これで CI 化の issue が消え、以後は誰も追っていない

### 2. PR 単位では「触ったファイルだけ clean」で合理的に済む

- Biome は全体 lint が all-or-nothing なので、一度 main に 1 件でも入ると、後続 PR の作者にとって「全体 lint を通す」は自分の変更と無関係なファイルを直すことを意味する。関係ない差分がレビュー負荷を上げるという懸念は #264 本文にも書かれていた
- 結果として PR 本文の定型は「変更ファイルの Biome 成功」になった。この wiki 内でも Codex の完了報告は一貫して「変更 TS の Biome 検査成功」と書いている（[[other-issue-candidates-2026-09-07]]、[[pr-935-shell-hydration-fix-2026-09-09]]）。PR #961 の「既知」注記はその延長で、注記としては正直だが、残件を誰が引き取るかは書かれていない
- 2025-05-13 の Slack（#502 に引用）で なのくろ が「元々は eslint を強制していたのでエラーがなかった。biome 導入でルールが変わったのが原因」「PR が少ないタイミングで全ファイル biome fix できると良い」と述べており、当時から「一括修正はタイミング依存」という認識だった

### 3. 直しても戻る種類のエラーが混ざっている

tsconfig.json は Next.js が書き換えるため、人が整形しても再発する。直しても戻るエラーが 1 件でも残っていると「全体 lint が通らないのは仕様」という空気ができ、他の 6 件も一緒に放置されやすい。

### 4. 設定整理の issue が別の問題に吸われた

Issue #700「Biome 設定の調整」（nishio、2025-09-09）は本来 Devin のセットアップ失敗の報告で、Biome の lint 強制とは別の話。外部コントリビュータ Devesh36 が 2025-12 に引き取ったが、提出された PR #734 は 3 フェーズ導入計画書 6 本と report-only workflow の大作で、旧 `client/` 構成前提のまま放置され、2026-05-18 に stale として close した（[[non-nishio-human-pr-status]]）。#700 は今も open で Devesh36 が assignee のまま。「Biome 周りは誰かがやっている」ように見える状態が、着手を遠ざけた面もある。

## 判断と次の一手

- 修正自体は小さい。viewer の 7 件は tsconfig.json を ignore に入れれば残り 5 ファイル、format 4 件は `biome check --write`、noDelete 2 件は手直し。admin 7 件、dummy-server 9 件も同程度
- 仕組みとしては、`client-build.yml` / `client-admin-build.yml` に `biome ci` を 1 step 足すのが最小。#264 の提案そのもの。ただし「0 にしてから gate を入れる」順序が必須で、どちらか片方だけでは再発する
- lefthook の `skip: true` を外すかは別判断。PR #270 の懸念（Python 側開発者の pre-push で `npx biome` が動く）は今も同じ
- #700 は Devesh36 の assign を解除して「CI gate + 一括修正」の issue に作り直すか、close して新規にするか。古い issue に新しい要件を上書きしない方針に従い、新規起票 + #700 への参照が素直

## Open Questions

- #264 を close した判断の根拠は issue 上に残っていない。Slack の 2025-04-19 前後の記録は `work/slack-logs/` の snapshot に無く、未確認
- lefthook-local.yml で Biome を有効にしているコントリビュータが実在するか
- CodeRabbit は設定無しでも Biome を走らせることがある。PR #961 等で Biome 由来の指摘が出ていないかは未確認

## Updates

- 2026-10-09: nishio の判断で「一括修正で 0 → build workflow に `biome ci`」を 1 PR で実施。#962 を起票して nishio に assign し、[PR #963](https://github.com/digitaldemocracy2030/kouchou-ai/pull/963)（`fix/biome-lint-zero-and-ci`、`07287a6`、未merge）を作成した。
  - viewer / admin / dummy-server とも `biome ci` 0 件。`tsconfig.json` は `files.ignore` へ。`noDelete` は `Reflect.deleteProperty` で置き換え。dummy-server は `node:` import と `let data: unknown`
  - `client-build.yml`（viewer + dummy-server）と `client-admin-build.yml`（admin）に `biome ci --reporter=github` を追加し、`biome.json` 変更でも走るようにした。CONTRIBUTING.md に追記
  - CI 全成功、両 build job で Biome step が実際に success したことを job の step 結果で確認。CodeRabbit は指摘なし。マージには必須承認 1 件が必要
  - lefthook の `skip: true` と #700 の整理は範囲外として残した
- 2026-10-09: nishio の指示で #700 を not planned で close。要件を main `a12d68e` と照合した結果、Biome が起動しない問題・個別インストール・環境変数の案内は 2026-01 の pnpm workspace 移行で解消済みで、残っていた「全体 lint が通らない・CI で強制されない」は #962 / PR #963 に引き継いだ。close コメントに経緯を記録した。
