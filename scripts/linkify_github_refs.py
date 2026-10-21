#!/usr/bin/env python3
"""Convert bare kouchou-ai issue/PR refs (#NNN) in wiki markdown into explicit links.

Quartz's ObsidianFlavoredMarkdown turns `#NNN` that is followed by letters (e.g.
`#11は`) into junk tag pages, and a bare `#NNN` is never clickable. kouchou-ai
PR/issue refs should be GitHub links, so this rewrites
`#NNN` -> `[#NNN](https://github.com/digitaldemocracy2030/kouchou-ai/issues/NNN)`
(GitHub redirects /issues/NNN <-> /pull/NNN automatically).

What is never rewritten (protected spans):
  - YAML frontmatter, fenced code blocks (``` / ~~~), inline code spans
  - existing markdown links and images `[label](url)` / `[label][ref]`, INCLUDING
    the label, so `[PR #938](.../pull/938)` stays as it is
  - wikilinks `[[page]]` / `[[page|alias #12]]`
  - URLs (`https://...#123`), `<autolinks>`, HTML tags and `<!-- comments -->`
  - `##` heading markers, `[#12]`, `&#123;`, `\\#12`, and refs glued to ASCII
    letters/digits/underscore on either side: `Serverless#22`, `#2577b1` (hex color),
    `#2_開発_広聴ai` (Slack channel), `#7ac943` (commit)
Refs inside heading text are converted like any other text.

Japanese text around a ref does not block conversion: `本体#941以後` and
`PR #970を参照` are converted (otherwise Quartz makes a junk tag of `#970を参照`).

Numbers that belong to another numbering system are skipped and reported
("skipped"):
  - when the text just before the ref (after skipping a chain such as
    `#22 / #23、`, `PR`, or links) names another repository or site
    (serverless, website, polimoney, Encraft, OJPP, idobata, React; see OTHER_REPO)
    or a list of principles / requirements (`KJ #3`, `原則の #3`, `要件の #5`;
    see NUMBERING)
  - when the same page links that number on another site, e.g.
    `.../kouchou-ai-serverless/pull/22` or `https://react.dev/errors/418`
    (see FOREIGN_URL_NUMBER); the frontmatter `sources:` list counts too
The heuristic cannot see everything, so:
  - write refs to OTHER repositories or sites as links, e.g.
    `[kouchou-ai-serverless#22](https://github.com/tokoroten/kouchou-ai-serverless/pull/22)`,
    `website PR [#192](https://github.com/digitaldemocracy2030/website/pull/192)` or
    `React [#418](https://react.dev/errors/418)`; links are never touched again
  - write list / principle / requirement numbers without `#` (`原則 3〜5`, `要件 5`)
  - Quartz also makes tags of a bare `#3/#4` chain (tag "3/4") and of a link label
    that starts with `#NNN` plus letters (`[#906のコメント](...)`); write
    `#3 / #4` and `[#906 のコメント](...)` instead (a digits-only tag is dropped)
  - review the dry-run output (it prints every change and every skip with its
    context) before `--apply`, then check `git diff --word-diff` before committing

Nested links: an older version of this script turned `[PR #938](.../pull/938)` into
`[PR [#938](.../issues/938)](.../pull/938)`, which CommonMark renders as broken text
plus a URL that swallows the rest of the line. Every run repairs such nested
kouchou-ai links back to the outer link (`[PR #938](.../pull/938)`).

log.md is never touched (it is machine-maintained; refresh_logs.py copies its
headings into the plain-TSV log.txt).

Running the script twice gives no further changes (idempotent).

Usage:
  python3 scripts/linkify_github_refs.py [--apply | --check] [paths...]
  (no paths: all of wiki/**/*.md; a directory argument means its **/*.md)
  default   dry-run: per-file counts, every change and every skipped ref
  --apply   write the files
  --check   dry-run that exits with status 1 when anything would change
Tests: python3 -m unittest discover -s scripts -p 'test_linkify_github_refs.py'
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = "https://github.com/digitaldemocracy2030/kouchou-ai/issues"
WIKI = Path(__file__).resolve().parent.parent / "wiki"

# `#NNN` not glued to an ASCII word char, `#`, `[`, `&` (HTML entity) or `\` (escape)
# on the left, and not followed by an ASCII word char on the right.
# Japanese characters on either side are allowed on purpose.
REF = re.compile(r"(?<![A-Za-z0-9_#\[&\\])#(\d+)(?![A-Za-z0-9_])")

# A kouchou-ai link inside the label of another link (left by the old version).
INNER_KOUCHOU_LINK = re.compile(
    r"\[#(\d+)\]\(https://github\.com/digitaldemocracy2030/kouchou-ai/(?:issues|pull)/\1\)"
)

# Before a ref (or before a chain of refs), these mark the number as belonging to
# another repository (within REPO_WINDOW chars) or to a list of principles /
# requirements (within NUMBERING_WINDOW chars, e.g. `KJ 法 6 原則の #3`).
OTHER_REPO = re.compile(
    r"serverless|サーバーレス|website|ウェブサイト|polimoney|ポリマネー|encraft|ojpp|idobata|いどばた|react",
    re.IGNORECASE,
)
NUMBERING = re.compile(r"原則|要件|ステップ|step|KJ", re.IGNORECASE)
REPO_WINDOW = 12
NUMBERING_WINDOW = 6
# Words that mark the kouchou-ai repository itself; the rightmost marker wins.
KOUCHOU_CONTEXT = re.compile(r"kouchou-ai(?!-)|本体|広聴\s*AI", re.IGNORECASE)
# Tokens skipped when walking back from a ref to the word that governs it:
# whitespace, separators, other refs, existing links, and PR / Issue labels.
CHAIN_TAIL = re.compile(
    r"(?:\s+|[/／・、,，〜~～\-–—]|#\d+|\[[^\[\]]*\]\([^()\s]*\)|PRs?|[Ii]ssues?|と|や|および)$"
)
EARLIER_REF = re.compile(r"#\d+")

# A number that the page already links on another site (another repository's
# issue/PR, a React error page, ...) is ambiguous as a bare ref on that page.
FOREIGN_URL_NUMBER = re.compile(
    r"https?://(?!github\.com/digitaldemocracy2030/kouchou-ai/)[^\s()<>\[\]]*?"
    r"/(?:issues|pull|pulls|discussions|errors)/(\d+)(?![\d])"
)

URL = re.compile(r"https?://[A-Za-z0-9\-._~:/?#@!$&'*+,;=%]+")
HTML_TAG = re.compile(r"</?[A-Za-z][^<>\n]*>")
BACKTICKS = re.compile(r"`+")
# An opening fence; a backtick fence's info string may not contain backticks.
FENCE_OPEN = re.compile(r"^\s*(?:(`{3,})(?!.*`)|(~{3,}))")


@dataclass
class Result:
    text: str
    converted: list[tuple[int, str]] = field(default_factory=list)  # (line no, context)
    repaired: list[tuple[int, str]] = field(default_factory=list)
    skipped: list[tuple[int, str]] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(self.converted or self.repaired)


def _match_bracket(line: str, i: int) -> int | None:
    """Index just past the `]` that closes the `[` at line[i] (balanced), or None."""
    depth = 0
    j = i
    while j < len(line):
        c = line[j]
        if c == "\\":
            j += 2
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return None


def _match_paren(line: str, i: int) -> int | None:
    """Index just past the `)` that closes the `(` at line[i] (balanced), or None."""
    depth = 0
    j = i
    while j < len(line):
        c = line[j]
        if c == "\\":
            j += 2
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return None


def _link_end(line: str, i: int) -> int | None:
    """If line[i] starts `[label](dest)` or `[label][ref]`, return its end index."""
    close = _match_bracket(line, i)
    if close is None or close >= len(line):
        return None
    if line[close] == "(":
        return _match_paren(line, close)
    if line[close] == "[":
        return _match_bracket(line, close)
    return None


def protected_spans(line: str, in_comment: bool = False) -> tuple[list[tuple[int, int, str]], bool]:
    """Return ([(start, end, kind)], still_in_html_comment) for spans never to rewrite."""
    spans: list[tuple[int, int, str]] = []
    i = 0
    n = len(line)
    if in_comment:
        end = line.find("-->")
        if end < 0:
            return [(0, n, "comment")], True
        spans.append((0, end + 3, "comment"))
        i = end + 3
    while i < n:
        c = line[i]
        if c == "`":
            # a code span ends at the next backtick run of exactly the same length
            opening = BACKTICKS.match(line, i)
            run = opening.end() - i
            close = next((m for m in BACKTICKS.finditer(line, opening.end()) if len(m.group(0)) == run), None)
            if close is not None:
                spans.append((i, close.end(), "code"))
                i = close.end()
            else:
                i = opening.end()
            continue
        if line.startswith("<!--", i):
            end = line.find("-->", i + 4)
            if end < 0:
                spans.append((i, n, "comment"))
                return spans, True
            spans.append((i, end + 3, "comment"))
            i = end + 3
            continue
        if c == "<":
            m = HTML_TAG.match(line, i)
            if m:
                spans.append((i, m.end(), "html"))
                i = m.end()
                continue
        if line.startswith("[[", i):
            end = line.find("]]", i + 2)
            if end >= 0:
                spans.append((i, end + 2, "wikilink"))
                i = end + 2
                continue
        if c == "[" or (c == "!" and line.startswith("[", i + 1)):
            start = i
            end = _link_end(line, i + 1 if c == "!" else i)
            if end is not None:
                spans.append((start, end, "link"))
                i = end
                continue
        if c == "h":
            m = URL.match(line, i)
            if m:
                spans.append((i, m.end(), "url"))
                i = m.end()
                continue
        i += 1
    return spans, False


def repair_nested(line: str) -> tuple[str, int]:
    """Flatten kouchou-ai ref links that sit inside another link's label."""
    count = 0
    out = []
    pos = 0
    spans, _ = protected_spans(line)
    for start, end, kind in spans:
        if kind != "link":
            continue
        link = line[start:end]
        offset = 1 if link.startswith("!") else 0
        label_end = _match_bracket(link, offset)
        if label_end is None:
            continue
        label = link[offset + 1 : label_end - 1]
        new_label, k = INNER_KOUCHOU_LINK.subn(r"#\1", label)
        if not k:
            continue
        count += k
        out.append(line[pos:start])
        out.append(link[: offset + 1] + new_label + link[label_end - 1 :])
        pos = end
    if not count:
        return line, 0
    out.append(line[pos:])
    return "".join(out), count


def foreign_context(prefix: str) -> bool:
    """True when the text before a ref says the number is not a kouchou-ai issue/PR."""
    p = prefix
    while True:
        m = CHAIN_TAIL.search(p)
        if not m or m.start() == len(p):
            break
        p = p[: m.start()]
    # A word before an earlier, unchained ref governs that ref, not this one:
    # in `React #418は#942と`, "React" belongs to #418 only.
    earlier = [m.end() for m in EARLIER_REF.finditer(p)]
    if earlier:
        p = p[earlier[-1] :]
    if NUMBERING.search(p[-NUMBERING_WINDOW:]):
        return True
    window = p[-REPO_WINDOW:]
    last_other = max((m.end() for m in OTHER_REPO.finditer(window)), default=-1)
    last_kouchou = max((m.end() for m in KOUCHOU_CONTEXT.finditer(window)), default=-1)
    return last_other > last_kouchou


def _context(line: str, start: int, end: int, width: int = 28) -> str:
    return (line[max(0, start - width) : start] + "⟦" + line[start:end] + "⟧" + line[end : end + width]).strip()


def convert_line(line: str, in_comment: bool = False, foreign_numbers: frozenset[str] = frozenset()):
    """Return (new_line, converted_contexts, skipped_contexts, still_in_comment)."""
    spans, still = protected_spans(line, in_comment)
    blocked = [(s, e) for s, e, _ in spans]
    out, pos = [], 0
    converted, skipped = [], []
    for m in REF.finditer(line):
        if any(s < m.end() and m.start() < e for s, e in blocked):
            continue
        if m.group(1) in foreign_numbers or foreign_context(line[: m.start()]):
            skipped.append(_context(line, m.start(), m.end()))
            continue
        num = m.group(1)
        out.append(line[pos : m.start()])
        out.append(f"[#{num}]({REPO}/{num})")
        pos = m.end()
        converted.append(_context(line, m.start(), m.end()))
    if not converted:
        return line, [], skipped, still
    out.append(line[pos:])
    return "".join(out), converted, skipped, still


def process(text: str) -> Result:
    lines = text.split("\n")
    res = Result(text)
    foreign_numbers = frozenset(FOREIGN_URL_NUMBER.findall(text))
    out = []
    in_front = False
    fence: str | None = None  # the opening fence run, e.g. "```" or "~~~~"
    in_comment = False
    for i, line in enumerate(lines):
        no = i + 1
        stripped = line.strip()
        # YAML frontmatter (only at the very top)
        if i == 0 and stripped == "---":
            in_front = True
            out.append(line)
            continue
        if in_front:
            out.append(line)
            if stripped == "---":
                in_front = False
            continue
        # fenced code blocks: a fence closes only with the same char, at least as long
        if fence is not None:
            if stripped.startswith(fence[0] * len(fence)) and stripped.strip(fence[0]) == "":
                fence = None
            out.append(line)
            continue
        m = FENCE_OPEN.match(line)
        if m and not in_comment:
            fence = m.group(1) or m.group(2)
            out.append(line)
            continue
        line2, k = repair_nested(line) if not in_comment else (line, 0)
        if k:
            res.repaired.append((no, line2.strip()[:120]))
        new, conv, skip, in_comment = convert_line(line2, in_comment, foreign_numbers)
        res.converted += [(no, c) for c in conv]
        res.skipped += [(no, c) for c in skip]
        out.append(new)
    res.text = "\n".join(out)
    return res


def collect(args: list[str]) -> list[Path]:
    if not args:
        roots = [WIKI]
    else:
        roots = [Path(a) for a in args]
    files: list[Path] = []
    for r in roots:
        if r.is_dir():
            files += sorted(r.rglob("*.md"))
        else:
            files.append(r)
    # log.md is machine-maintained and refresh_logs.py derives log.txt (a plain TSV)
    # from its headings; markdown links would leak into the TSV.
    return [f for f in files if f.name != "log.md"]


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    apply = "--apply" in argv
    check = "--check" in argv
    files = collect([a for a in argv if not a.startswith("--")])
    total_conv = total_rep = total_skip = 0
    changed_files = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        res = process(text)
        if res.skipped:
            for no, ctx in res.skipped:
                print(f"skipped (not kouchou-ai?) {f}:{no}: {ctx}")
            total_skip += len(res.skipped)
        if not res.changed:
            continue
        changed_files += 1
        total_conv += len(res.converted)
        total_rep += len(res.repaired)
        verb = "WROTE" if apply else "would change"
        print(f"{verb} {f}: {len(res.converted)} refs, {len(res.repaired)} nested lines repaired")
        for no, ctx in res.repaired:
            print(f"  L{no} repaired: {ctx}")
        for no, ctx in res.converted:
            print(f"  L{no}: {ctx}")
        if apply:
            f.write_text(res.text, encoding="utf-8")
    mode = "applied" if apply else "dry-run"
    print(
        f"\nTotal: {total_conv} refs linked, {total_rep} nested lines repaired in "
        f"{changed_files} of {len(files)} files; {total_skip} refs skipped ({mode})"
    )
    if check and changed_files:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
