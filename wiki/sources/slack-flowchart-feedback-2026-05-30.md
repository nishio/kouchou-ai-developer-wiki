---
type: source
summary: "2026-05-30 #2_開発_広聴ai Slack で decision flowchart 試作 (試作 A / 試作 B) に対する nishio / tokoroten の feedback。試作 A は最初の分岐が『データ量』であるべき + 『ラベル付きデータ』は jargon。試作 B はそもそも前提が違い、AI = wiki から把握できないほど platform 知識が抜けていた"
sources:
  - slack-flowchart-feedback-2026-05-30.txt
---

[[decision-flowchart-prototype-2026-05-30]] 試作 A / B に対する team channel での feedback。試作の方向は否定されず、内容の精度が指摘された。

## 試作 A への指摘

- **最初の分岐は「ラベル付きデータがあるか」ではなく「すでにあるデータの量」**: 試作 A の出発点は scikit-learn の estimator chart を真似て「ラベル付きデータ持ってる?」にしたが、これは間違い。広聴AI 系で最初に判断すべきはデータ量である。scikit-learn の図でも「データ50件ない？もっと集めてこい」が早い段階に出てくるのと同じ
- **「ラベル付きデータ」は jargon**: tokoroten 指摘。「普通の人には分からん」。一般読者を対象にするフローチャートでは使うべき語ではない

## 試作 B への指摘

- **「だいぶ違う」**: nishio から全否定気味。理由は試作 B が暗黙に置いていた前提が広聴AI の実際の動作環境と合っていなかった
- **「AI も正しいフローチャートをかけないくらい把握できてない」**: つまり wiki に必要な platform 知識が積まれていない。AI = 私はそれを抽出できなかった
- **Mac だから Docker Desktop インストール可能、は飛躍**: Docker Desktop のライセンスは個人 / 組織で違うので、OS が Mac であることは Docker Desktop 利用可能を意味しない (組織問題)。tokoroten も指摘
- **Linux が一番安定 (CI 実証)**: GitHub Actions の CI が Linux で回って tests を pass している以上、理屈上は生 Linux が最も動作実証されている platform
- **Mac も大差ない (開発実証)**: nishio は Mac で開発して push しているので、Mac は CI の Linux と大差ないことが実証されている
- **Windows は未検証**: 上記の含意として、Windows は安定実証が薄い
- **Docker Desktop は個人無料、大組織 (自治体含む) 有料**: 「個人で試すのは無料、自治体は有料、って話が抜けてるんだな」(nishio)。`[[docker-desktop-license-2026-05-29]]` には license の話があるが、決定フロー上の重み付けには反映されていなかった
- **ダマで使う組織は多いが推奨できない**: tokoroten。「デカい組織で使うと有料」「ダマで使ってる組織は無限にあるが、それを勧めるわけにもいかん」。フローチャートではこの灰色領域を「推奨しない」側に倒す必要がある

## 含意 (wiki への追記)

私 (= Claude) が試作 B を書く時に拾えなかった知識を、wiki の追記対象として明示する:

- **platform 安定性ティア**: Linux (CI 実証) > Mac (nishio 開発実証) > Windows (実機検証薄い)。これは [[local-dev-setup]] / [[architecture-overview]] / [[docker-desktop-license-2026-05-29]] のどこにも明示されていない
- **Docker Desktop ライセンスの decision-flow 上の重み**: [[docker-desktop-license-2026-05-29]] は条文確認の source だが、「個人 / 自治体 / 大企業」を flowchart 上の最初の分岐として扱う観点が抜けていた
- **「ダマ運用」の存在**: 大組織が Docker Desktop を実態ベースで無断利用している現実は wiki に書いていない。書く時は「実態として広く存在する灰色領域だが、product としては推奨できない」というスタンスで書く必要がある

## Updates

- 2026-05-30: 初版作成。試作 A / B への team feedback を fix。[[decision-flowchart-prototype-2026-05-30]] の修正 + 関連知識の wiki 追加 (platform 安定性ティア、Docker Desktop 重み) の input として使う
