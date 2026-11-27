#!/usr/bin/env python3
"""公開境界チェック: 公開 wiki に出してはいけない文字列を push 前に止める。

CLAUDE.md の「公開境界」（デプロイ詳細・脆弱性詳細・secret を公開 wiki に書かない）を
指示だけでなくソフトウェアでも守るための検査。2 種類の規則を見る。

1. スクリプトに書いた一般的な型（鍵の形、クラウドの host 名の形など）
2. gitignored の手元一覧 `raw/boundary/denylist.tsv`
   具体的な host 名や、期限つきで伏せる話題の語のように、語そのものが秘密のものはここに置く。

denylist.tsv の形式（タブ区切り、`#` で始まる行はコメント。`#1026` のような語も書けるよう行の途中の `#` はコメント扱いしない）:

    <until>\t<pattern>\t<note>

- until: `YYYY-MM-DD`（期限つき）または `-`（常設）。
  期限を過ぎても **止めたまま** にし、「解除するなら行を消す」と知らせる。
  公開してよいかは人が決める（期限は見直しの目安）。
- pattern: 既定は大文字小文字を区別しない部分一致。`re:` で始めると正規表現。
- note: 止めた時に表示する説明（例: 「API キー漏洩、公開は nishio の指示待ち」）。

使い方:
    python3 scripts/check_public_boundary.py            # 作業ツリーの追跡ファイル全体を検査
    python3 scripts/check_public_boundary.py --range A..B  # A..B の commit で足した行と commit メッセージを検査
    python3 scripts/check_public_boundary.py --pre-push  # git の pre-push hook から呼ぶ（stdin に push 対象）

見つかった文字列は先頭だけ表示して残りを伏せる（出力がログに残っても漏れないように）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DENYLIST = ROOT / "raw" / "boundary" / "denylist.tsv"
ZERO_SHA = "0" * 40

# 1. 一般的な型。公開 repo に書いてよい形だけを置く。
GENERIC_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("秘密鍵", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Anthropic API キーの形", re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI API キーの形", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}")),
    ("AWS アクセスキーの形", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API キーの形", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("GitHub トークンの形", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{50,})")),
    ("Slack トークンの形", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("Azure 接続文字列の鍵", re.compile(r"AccountKey=[A-Za-z0-9+/=]{20,}")),
    (
        "Azure の実環境 host 名の形",
        re.compile(
            r"\b[a-z0-9][a-z0-9.-]*\.(?:azurecontainerapps\.io|azurewebsites\.net|"
            r"azurestaticapps\.net|azurecr\.io|blob\.core\.windows\.net|azure-api\.net)\b",
            re.IGNORECASE,
        ),
    ),
    ("Container Apps の revision 名の形", re.compile(r"\b[a-z0-9-]+--[0-9]{7}\b")),
]

# 一般的な型に当たるが、kouchou-ai のデプロイとは無関係な公開サイト。
ALLOWED = {
    "lamport.azurewebsites.net",  # Leslie Lamport の TLA+ サイト
}

# 検査しない追跡ファイル（この検査自体の定義・テスト）
SKIP_PATHS = {
    "scripts/check_public_boundary.py",
    "scripts/test_check_public_boundary.py",
}


@dataclass
class LocalRule:
    until: dt.date | None
    pattern: re.Pattern[str]
    note: str
    lineno: int


@dataclass
class Finding:
    where: str
    label: str
    excerpt: str


def mask(s: str) -> str:
    keep = min(4, max(1, len(s) // 4))
    return s[:keep] + "*" * min(8, len(s) - keep)


def parse_denylist(text: str) -> tuple[list[LocalRule], list[str]]:
    rules: list[LocalRule] = []
    errors: list[str] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip("\r\n")
        if line.lstrip().startswith("#") or not line.strip():
            continue
        cols = line.split("\t")
        if len(cols) < 2:
            errors.append(f"denylist.tsv:{lineno}: タブ区切りで <until> <pattern> [note] が必要")
            continue
        until_s, pat_s = cols[0].strip(), cols[1]
        note = cols[2].strip() if len(cols) > 2 else ""
        until = None
        if until_s != "-":
            try:
                until = dt.date.fromisoformat(until_s)
            except ValueError:
                errors.append(f"denylist.tsv:{lineno}: until は YYYY-MM-DD か - ({until_s!r})")
                continue
        try:
            if pat_s.startswith("re:"):
                pattern = re.compile(pat_s[3:], re.IGNORECASE)
            else:
                if not pat_s.strip():
                    errors.append(f"denylist.tsv:{lineno}: pattern が空")
                    continue
                pattern = re.compile(re.escape(pat_s.strip()), re.IGNORECASE)
        except re.error as e:
            errors.append(f"denylist.tsv:{lineno}: 正規表現の誤り ({e})")
            continue
        rules.append(LocalRule(until, pattern, note, lineno))
    return rules, errors


def load_local_rules() -> tuple[list[LocalRule], list[str]]:
    if not DENYLIST.exists():
        return [], []
    return parse_denylist(DENYLIST.read_text(encoding="utf-8"))


def scan_text(text: str, where: str, local_rules: list[LocalRule], today: dt.date) -> list[Finding]:
    found: list[Finding] = []
    for label, rx in GENERIC_RULES:
        for m in rx.finditer(text):
            if m.group(0).lower() in ALLOWED:
                continue
            found.append(Finding(where, label, mask(m.group(0))))
    for rule in local_rules:
        for m in rule.pattern.finditer(text):
            if rule.until is None:
                label = f"手元一覧 {rule.lineno} 行目（常設）"
            elif today <= rule.until:
                label = f"手元一覧 {rule.lineno} 行目（{rule.until} まで伏せる）"
            else:
                label = (
                    f"手元一覧 {rule.lineno} 行目（期限 {rule.until} を過ぎた。"
                    "公開してよいと決まったら、その行を消す）"
                )
            if rule.note:
                label += f": {rule.note}"
            found.append(Finding(where, label, mask(m.group(0))))
    return found


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace"
    ).stdout


def scan_tree(local_rules: list[LocalRule], today: dt.date) -> list[Finding]:
    found: list[Finding] = []
    for rel in git("ls-files", "-z").split("\0"):
        if not rel or rel in SKIP_PATHS:
            continue
        p = ROOT / rel
        if not p.is_file() or p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff", ".woff2"}:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            found += scan_text(line, f"{rel}:{lineno}", local_rules, today)
    return found


def scan_range(rev_args: list[str], local_rules: list[LocalRule], today: dt.date) -> list[Finding]:
    """rev_args の commit が足した行と commit メッセージを検査する。

    途中の commit で足して後の commit で消した語も、履歴として公開されるので拾う。
    """
    found: list[Finding] = []
    shas = git("rev-list", *rev_args).split()
    for sha in shas:
        short = sha[:8]
        msg = git("log", "-1", "--format=%B", sha)
        for line in msg.splitlines():
            found += scan_text(line, f"commit {short} のメッセージ", local_rules, today)
        diff = git("show", "--format=", "--unified=0", "--no-color", "--no-ext-diff", sha)
        path = "?"
        for line in diff.splitlines():
            if line.startswith("+++ "):
                path = line[6:] if line.startswith("+++ b/") else line[4:]
            elif line.startswith("+") and path not in SKIP_PATHS:
                found += scan_text(line[1:], f"commit {short} {path}", local_rules, today)
    return found


def pre_push_rev_args(stdin_text: str) -> list[list[str]]:
    ranges = []
    for line in stdin_text.splitlines():
        parts = line.split()
        if len(parts) != 4:
            continue
        _local_ref, local_sha, _remote_ref, remote_sha = parts
        if local_sha == ZERO_SHA:  # ブランチ削除
            continue
        if remote_sha == ZERO_SHA:
            ranges.append([local_sha, "--not", "--remotes"])
        else:
            ranges.append([f"{remote_sha}..{local_sha}"])
    return ranges


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--range", help="検査する commit 範囲（例: origin/main..HEAD）")
    g.add_argument("--pre-push", action="store_true", help="git pre-push hook として stdin を読む")
    args = ap.parse_args()

    today = dt.date.today()
    local_rules, errors = load_local_rules()
    for e in errors:
        print(f"公開境界チェック: {e}", file=sys.stderr)
    if errors:
        return 2

    if args.pre_push:
        findings = []
        for rev_args in pre_push_rev_args(sys.stdin.read()):
            findings += scan_range(rev_args, local_rules, today)
    elif args.range:
        findings = scan_range([args.range], local_rules, today)
    else:
        findings = scan_tree(local_rules, today)

    if not findings:
        return 0
    print("公開境界チェック: 公開してはいけない可能性のある文字列が見つかりました。", file=sys.stderr)
    for f in findings:
        print(f"  - {f.where}: {f.label} [{f.excerpt}]", file=sys.stderr)
    if args.pre_push or args.range:
        print(
            "  commit 済みの場合は、該当 commit を書き直してから push してください"
            "（後の commit で消しても履歴に残ります）。",
            file=sys.stderr,
        )
    print(
        f"  誤検知なら scripts/check_public_boundary.py の ALLOWED に足すか、手元一覧（{DENYLIST.relative_to(ROOT)}）を直してください。",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
