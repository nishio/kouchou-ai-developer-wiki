#!/usr/bin/env python3
"""Convert bare GitHub issue/PR refs (#NNN) in wiki markdown into explicit links.

Quartz's ObsidianFlavoredMarkdown turns bare `#NNN` into (wrong) tag links, and
even when it doesn't, `#NNN` is not clickable. kouchou-ai PR/issue refs should be
GitHub links. This rewrites `#NNN` -> `[#NNN](https://github.com/digitaldemocracy2030/kouchou-ai/issues/NNN)`
(GitHub redirects /issues/NNN <-> /pull/NNN automatically).

Safe-skips: YAML frontmatter, fenced code blocks, inline code spans, hex colors
(`#2577b1`), markdown headings (`## `), already-linked refs (`[#NNN](...)`),
and refs that are part of a URL path.

Usage:
  python3 scripts/linkify_github_refs.py [--apply] [paths...]
Default: dry-run over wiki/**/*.md (prints per-file counts + samples).
"""
import re
import sys
from pathlib import Path

REPO = "https://github.com/digitaldemocracy2030/kouchou-ai/issues"
WIKI = Path(__file__).resolve().parent.parent / "wiki"

# #NNN not preceded by word-char / # / [ (avoid ##, [#, hex tails, existing links)
# and not followed by a word char (avoid hex #2577b1, and partial matches).
# NOTE: `/` is intentionally NOT excluded so slash-grouped refs (#992/#993) both convert;
# markdown-link URL fragments in this wiki use #word (letters), not #digits, so they stay safe.
REF = re.compile(r"(?<![\w#\[])#(\d+)(?![\w])")


def protect_inline_code(line: str):
    """Split a line into (text, is_code) spans on backticks so we skip inline code."""
    parts = re.split(r"(`+[^`]*`+)", line)
    return [(p, p.startswith("`")) for p in parts]


def convert_line(line: str) -> tuple[str, int]:
    out, n = [], 0
    for span, is_code in protect_inline_code(line):
        if is_code:
            out.append(span)
            continue
        new, c = REF.subn(lambda m: f"[#{m.group(1)}]({REPO}/{m.group(1)})", span)
        out.append(new)
        n += c
    return "".join(out), n


def process(text: str) -> tuple[str, int]:
    lines = text.split("\n")
    out, total = [], 0
    in_front = False
    in_fence = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        # YAML frontmatter (only at very top)
        if i == 0 and line.strip() == "---":
            in_front = True
            out.append(line)
            continue
        if in_front:
            out.append(line)
            if line.strip() == "---":
                in_front = False
            continue
        # fenced code blocks
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        new, n = convert_line(line)
        out.append(new)
        total += n
    return "\n".join(out), total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    if args:
        files = [Path(a) for a in args]
    else:
        # log.md is excluded: it is machine-maintained and refresh_logs.py derives
        # log.txt (a plain TSV) from its headings; markdown links would leak into the TSV.
        files = [p for p in sorted(WIKI.rglob("*.md")) if p.name != "log.md"]
    grand = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        new, n = process(text)
        if n:
            grand += n
            print(f"{'WROTE' if apply else 'would change'} {f}: {n}")
            if apply:
                f.write_text(new, encoding="utf-8")
    print(f"\nTotal refs: {grand} across {len(files)} files ({'applied' if apply else 'dry-run'})")


if __name__ == "__main__":
    main()
