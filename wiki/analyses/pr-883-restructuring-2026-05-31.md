---
type: analysis
summary: "PR #883 developer-quickstart は merge を急がず、直近 1 週間で固まった整理 (利用主体先行分岐、platform 安定性ティア、Docker Desktop license の決定フロー上の重み、データ量前提、構造把握スタンス) を docs に取り込んでから書き直すべき。現状の 4 モード分岐は読者像と Mode 選択前提が暗黙のため、Docker Desktop が使えない人や自治体担当が詰む構造になっている"
sources:
  - decision-flowchart-prototype-2026-05-30.md
  - slack-flowchart-feedback-2026-05-30.md
  - docker-desktop-license-2026-05-29.md
  - analysis-stance.md
  - issue-877-windows-setup-guide-scope.md
  - github-dev-docs.md
---

## 状況

PR #883 (`[codex] 開発者向け導線を利用モード別に整理する`, closes `#876`) は 2026-05-29 に作成し、CodeRabbit 2 件 address 済みで人間 reviewer 承認待ち。nishio が 2026-05-31 に「もうちょっと何が語られるべきかを整理してから作るべきだな」と判断。直近 1 週間 (2026-05-26〜30) に固まった整理が docs に反映されていないため、merge を急がず再構成してから land する方針に倒す。

## 現状 PR #883 の構成 (developer-quickstart.md)

1. 冒頭: 「自分はどの起動モードを使うべきか」を判断してから進むよう案内
2. 一般ユーザは別ページ (OS 別 setup) へ誘導
3. 4 モードの選択表 (Mode 1〜4)
4. 各 Mode の手順、確認 URL、よくある落とし穴
5. 「迷ったら Mode 1 (Docker Compose) から」

## 直近 1 週間で固まった、まだ反映されていない整理

| 出典 | 反映されるべき含意 |
|---|---|
| [[decision-flowchart-prototype-2026-05-30]] 試作 B v2 | 環境構築の最初の分岐は **OS ではなく利用主体 (個人 / 大組織)**。Docker Desktop license が個人無料 / 大組織有料 |
| [[docker-desktop-license-2026-05-29]] 追記 | platform 安定性ティア **Linux > Mac > Windows** (CI 実証 / 開発実証 / 検証薄い) |
| [[slack-flowchart-feedback-2026-05-30]] | 「ダマで Docker Desktop を使う」灰色領域は推奨しない、と率直に書くべき |
| [[analysis-stance]] | 広聴AI は構造把握スタンスのツールであって定量分析スタンスではない (開発者にも core stance として共有する価値あり) |
| [[broadlistening-tool-ecosystem-vision]] | Web UI = simple、CLI = 実験機能、コミュニティ共有、の二段構造ビジョン |
| `#876` 本文 | 「Mode 4 (CLI / analysis-core) でデータが少なすぎると意味がない」のような前提条件 (数百件以上) は明記されていない |

## 現状 PR #883 で詰まる読者シナリオ

1. **大組織所属 / Docker Desktop ライセンスなし**: 「迷ったら Mode 1」と書かれているが、そもそも Mode 1 を使えない (license)。代替ルートは現状記載なし → **詰む**
2. **Windows ユーザ**: 「Mode 1 を Docker Desktop で」と書かれているが、Windows での実機検証が薄いことは明記されていない → 期待値ずれ
3. **自治体担当 (実装ではなくレビューしたい)**: 「一般ユーザは OS 別 setup」と「開発者は本 page」の二分しかない。**「導入の検討役 / 評価役」** に該当する読者像が想定されていない
4. **小規模データ持ちユーザ**: Mode 4 (CLI) を選ぶが、データ量の前提が書かれていないので「数十件しかない」状態で実行して結果が薄い → ユーザ失望

## 再構成の提案

### 1. 読者像セクションを冒頭に追加

開発者・自治体担当・一般ユーザの 3 像を最初に切り、それぞれが本 page のどこを読むかを示す。「開発者向け」と銘打つだけでは、自治体担当の評価役が迷う。

### 2. 環境構築の決定フローを Mode 選択の前に置く

[[decision-flowchart-prototype-2026-05-30]] 試作 B v2 を導入し:

- **最初の分岐 = 利用主体 (個人 / 大組織)**: Docker Desktop license の取得可否を確認させる
- **二段目 = OS**: platform 安定性ティア (Linux > Mac > Windows) を明示
- **代替ルート**: 大組織 + Docker Desktop ライセンスなしの人向けに WSL2 / SaaS 待ち / 「使える人を探す」を明示
- **「ダマ運用」**: product としては推奨しないと率直に書く

これを通過してから Mode 1〜4 の選択に進む。

### 3. 各 Mode に前提条件を明示

- **Mode 1**: Docker Desktop または Docker Engine + Compose。大組織は license 確認
- **Mode 2**: pnpm 必須 (npm 非対応の理由は [[npm-vs-pnpm]])。UI のみ触る
- **Mode 3**: Rye + pnpm のローカル install。デバッガ / ホットリロード用途
- **Mode 4**: pip install のみ。**ただしデータが数百件以上ないと結果は薄い** ([[analysis-stance]] 参照)

### 4. 構造把握スタンスの一行紹介を `#876` 文脈に入れる

開発者向け docs であっても、「広聴AI は何のためのツールか」を 1 段落で共有しないと、Mode 4 (CLI) を見た開発者が「scikit-learn の代替か?」のような誤解を抱きうる。[[analysis-stance]] へ 1 行リンクを置く。

### 5. 「困ったらこっち」の出口を明示

scikit-learn 図の「使える人を探せ」のような率直さで、「自分の環境で動かせない場合は SaaS 待ち / コミュニティに依頼」のような代替経路を明示する。

## 修正後の構成案 (案)

```
1. このページは誰のため (読者像 3 像)
2. 広聴AI とは何のツールか (構造把握スタンス 1 段落)
3. 環境を選ぶ (試作 B v2 相当のフロー: 利用主体 → OS → Mode)
4. Mode 1〜4 の詳細手順 (前提条件込み)
5. 困ったら (代替経路 / コミュニティ)
6. よくある落とし穴 (現行通り)
```

## 次の一手の選択肢

- (a) **本ページの再構成提案を PR #883 に追記コメントとして渡し、nishio が書き直す**: 人間 attention を使う操作なので AI 独断はしない (CLAUDE.md 運用方針)。nishio が判断してコメントするか、本ページを直接 docs 草案として使うか
- (b) **本ページを input に nishio が新しい developer-quickstart 草案を書く**: 既存 PR を draft に戻すか、別 PR として切り出すか
- (c) **PR #883 の現状 docs を fix の上ベースとして merge し、追加 PR で再構成を入れる**: 段階的に進める。ただし「不十分な docs を一旦 main に入れる」リスク

私の推奨は **(b)**。PR は draft に戻し、本ページの再構成案を基に書き直してから land する方が、内容の整合性が取れる。

## Open Questions

- 読者像の 3 分割 (開発者 / 自治体担当 / 一般ユーザ) は適切か、もう一段細分化が要るか
- 「環境を選ぶフロー」を mermaid で developer-quickstart 内に埋め込むか、テキストで書き下すか
- 「ダマで Docker Desktop」の灰色領域を docs に書くトーン (率直に書く / 婉曲に書く / 触れない) の選択
- `#876` 本文との整合性確認 (要件として何が書かれているか再読が必要)
- `developer-quickstart` と OS 別 `*-setup` docs の役割分担を再整理する必要があるかも

## Updates

- 2026-05-31: 初版。nishio が「もうちょっと何が語られるべきかを整理してから作るべきだな」と判断したのを受けて、現状 PR の構成 / 直近 1 週間の未反映知見 / 詰まる読者シナリオ / 再構成提案を整理した
