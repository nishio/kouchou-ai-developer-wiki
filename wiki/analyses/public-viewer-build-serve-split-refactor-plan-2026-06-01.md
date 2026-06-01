---
type: analysis
summary: "public-viewer の build-time API 依存を dynamic hosting から外し、container 起動時 next build を撤去するための段階的リファクタ計画"
sources:
  - source-code.md
  - github-dev-docs.md
  - nextjs-dynamic-build-docs-2026-06-01.md
  - public-viewer-runtime-build-history-2026-06-01.md
  - pr-887-production-deploy-observation-2026-06-01.md
---

# Public Viewer Build Serve Split Refactor Plan 2026-06-01

## Goal

`public-viewer` の通常 dynamic hosting では `next build` 中に API を叩かず、API fetch は request-time に寄せる。その上で Docker image build 時に `.next` を作り、container 起動時の `pnpm run build` を撤去する。static export だけは従来どおり build-time に API を叩いて静的 HTML を生成する。[[public-viewer-runtime-build-history-2026-06-01]]より

## Non-Goals

- static export 機能を廃止しない
- report 表示の data contract (`/reports`, `/reports/{slug}`, `/meta/metadata.json`) は変えない
- Azure deploy readiness check の本格修正は別段階に分ける
- まずは `public-viewer` に限定し、`admin` / `static-site-builder` へ不要な変更を広げない

## Phase 0: Baseline Repro

目的: 現状の失敗・成功条件を明示して、後続変更の検出基準にする。

作業:

- `work/kouchou-ai` の clean topic branch / worktree を作る
- API なし dynamic build の現状を確認する
- dummy-server あり static export build の現状を確認する
- Docker build / compose 起動の現状を確認する

確認コマンド候補:

```bash
unset API_BASEPATH NEXT_PUBLIC_API_BASEPATH NEXT_PUBLIC_PUBLIC_API_KEY
pnpm --filter @kouchou-ai/public-viewer build
```

```bash
API_BASEPATH=http://127.0.0.1:8002 \
NEXT_PUBLIC_API_BASEPATH=http://127.0.0.1:8002 \
NEXT_PUBLIC_PUBLIC_API_KEY=public \
pnpm --filter @kouchou-ai/public-viewer build:static
```

合格条件:

- 現状の dynamic build が API 依存で失敗・timeout するなら、その failure mode を記録する
- static export は dummy-server の有無で期待どおり success / fail するかを記録する

## Phase 1: Dynamic Build から API Fetch を外す

目的: 通常 `pnpm --filter @kouchou-ai/public-viewer build` が API なしで通るようにする。

作業:

- `app/[slug]/page.tsx`
  - non-export の `generateStaticParams()` は API を叩かず `[]` を返す
  - non-export の `Page` は `await connection()` で request-time rendering に送る
  - non-export の `generateMetadata()` はまず fallback metadata を返す
  - export 時だけ `/reports`, `/reports/{slug}`, `/meta/metadata.json` を build-time fetch する
- `app/page.tsx`
  - non-export の `Page` は `await connection()` 後に request-time fetch
  - non-export の `generateMetadata()` は fallback metadata
  - export 時だけ build-time metadata / reports fetch を残す
- `app/faq/page.tsx`
  - non-export の `Page` は `await connection()` 後に request-time fetch
  - export 時だけ build-time fetch を残す
- helper
  - `isStaticExportBuild()` を既存 helper から使い回す
  - export 専用 fetch helper を作る場合は、static export failure message を維持する

確認コマンド:

```bash
unset API_BASEPATH NEXT_PUBLIC_API_BASEPATH NEXT_PUBLIC_PUBLIC_API_KEY
pnpm --filter @kouchou-ai/public-viewer build
```

```bash
API_BASEPATH=http://127.0.0.1:8002 \
NEXT_PUBLIC_API_BASEPATH=http://127.0.0.1:8002 \
NEXT_PUBLIC_PUBLIC_API_KEY=public \
pnpm --filter @kouchou-ai/public-viewer build:static
```

合格条件:

- API なし dynamic build が成功する
- static export の成功条件は壊れない
- dummy-server なし static export は明示 error で fail する
- `generateMetadata()` が build-time API fetch の抜け道になっていない

## Phase 2: Runtime Build を Docker Image Build へ移す

目的: container 起動時 build をなくし、startup path を `next start` だけにする。

作業:

- `apps/public-viewer/Dockerfile`
  - builder stage で `pnpm --filter @kouchou-ai/public-viewer build` を実行する
  - runner stage に `.next`, `public`, `package.json`, runtime deps を持ち込む
  - runner stage に runtime build 用の余分な source / build tools を残しすぎない
- `apps/public-viewer/entrypoint.sh`
  - `.next` 削除を消す
  - `pnpm run build` を消す
  - `exec pnpm run start` だけにする

確認コマンド:

```bash
docker build --platform linux/amd64 \
  -f ./apps/public-viewer/Dockerfile \
  --build-arg NEXT_PUBLIC_API_BASEPATH=http://localhost:8000 \
  --build-arg NEXT_PUBLIC_PUBLIC_API_KEY=public \
  --build-arg API_BASEPATH=http://api:8000 \
  -t kouchou-public-viewer-test .
```

```bash
docker run --rm -p 3000:3000 \
  -e NEXT_PUBLIC_API_BASEPATH=http://host.docker.internal:8000 \
  -e API_BASEPATH=http://host.docker.internal:8000 \
  -e NEXT_PUBLIC_PUBLIC_API_KEY=public \
  kouchou-public-viewer-test
```

合格条件:

- Docker build 中に `.next` が作られる
- container logs に startup `pnpm run build` が出ない
- API 起動済みなら root / representative report が 200
- API 未起動なら `next start` 自体は起動し、page access 時に `ApiConnectionError` へ落ちる

## Phase 3: CI Regression Coverage

目的: 今後 `public-viewer` の API-less dynamic build が壊れた時に PR で検出する。

作業:

- `.github/workflows/client-build.yml` または別 job で API なし dynamic build を追加
- static export build は dummy-server / mock API ありの別 check として維持
- 可能なら Docker build smoke を軽量に追加

確認項目:

- API なし dynamic build check が PR で実行される
- static export check が static export 専用の失敗を拾う
- build log に API fetch timeout retry が出ない

合格条件:

- 通常 dynamic build と static export build の責務が CI 上で分かれている
- API なし dynamic build を壊す変更が CI で落ちる

## Phase 4: Azure Deploy Readiness

目的: Deploy Success false positive をなくす。

作業:

- `Azure Deployment` の job timeout を 25〜30 分程度へ引き上げる
- script 側 readiness timeout を 10 分程度で明示する
- `az containerapp update` 後に latest revision を取得し、latest ready になるまで poll する
- timeout 時は revision status / logs を出して fail する
- representative report smoke を追加する

合格条件:

- latest revision が Ready になるまで deploy success にならない
- Ready にならない場合は GitHub Actions timeout ではなく、script 側 timeout の明示 error で落ちる
- stable URL だけでなく representative report URL も見る

## Phase 5: Resource Re-evaluation

目的: runtime build を消した後、2Gi が必要かを再評価する。

作業:

- 2Gi 暫定増強後に Phase 1〜4 を入れる
- startup build が消えた後、1Gi に戻して revision readiness / memory pressure を観測する
- `minReplicas: 1` を続けるか、cold start と固定費の tradeoff を別途検討する

合格条件:

- 1Gi に戻しても deploy / startup / representative report smoke が安定する
- 1Gi に戻せない場合、理由が runtime serve memory なのか別要因なのか切り分けられている

## Suggested PR Split

1. `public-viewer` dynamic build を API-less にする PR
2. Dockerfile / entrypoint から runtime build を撤去する PR
3. CI に API-less dynamic build と static export build checks を追加する PR
4. Azure Deployment readiness / smoke を改善する PR
5. memory 2Gi -> 1Gi の再評価 PR または infra change

この順序なら、各 PR の rollback 単位が小さく、runtime build 撤去前に dynamic build の正しさを確認できる。

## Risks

- `generateMetadata()` の fallback により dynamic hosting の OGP/title が request-specific でなくなる可能性がある。必要なら後続で runtime metadata を再導入する。
- `connection()` の導入により route cache / ISR 挙動が変わる可能性がある。`revalidate = 300` との関係を実測する必要がある。
- Docker runner stage の copy 最小化を攻めすぎると runtime module resolution が壊れる。最初は保守的に copy し、後で削る。
- static export と dynamic hosting を同じ route file で保つため、分岐漏れが起きやすい。CI で両方を必ず回す。

## Open Questions

- dynamic hosting でも metadata を API 由来にしたい場合、`generateMetadata()` を request-time に安全に寄せられるか。
- `connection()` と `revalidate = 300` の組み合わせで、期待どおり API response が更新されるか。
- representative report smoke の slug は固定 fixture にするか、本番 API から ready report を選ぶか。

## Updates

- 2026-06-01: `codex/public-viewer-build-serve-split` / PR #888 で Phase 0〜3 を実装確認。baseline では API なし dynamic build が `/` / `/faq` の static generation timeout で止まり、実装後は API なし `pnpm --filter @kouchou-ai/public-viewer build`、fixture API あり `build:static`、runtime smoke (`/`, `/faq/`, `/example/`) が成功した。実装中に `[slug]` page へ `connection()` を入れると `/example` が `DYNAMIC_SERVER_USAGE` で落ちたため採用せず、non-export の `generateStaticParams() => []` と runtime env 読み (`process.env[key]`) で request 時 API を読む形にした。Docker build は手元 Docker daemon 未起動で未検証だが、CI に Docker build step を追加した。
- 2026-06-01: 初版作成。dynamic build/API 依存除去、runtime build 撤去、CI、Azure readiness、resource reevaluation を段階分割。
