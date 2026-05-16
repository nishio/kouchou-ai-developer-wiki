"""Wiki lint: duplicate IDs, orphan detection, broken links, missing frontmatter.

Usage: python3 scripts/lint_wiki.py
"""
import re
from pathlib import Path
from collections import defaultdict

WIKI = Path(__file__).parent.parent / "wiki"

# Collect all pages by basename (without .md). Wikilinks resolve by basename, so
# duplicate stems make links ambiguous and must not be silently overwritten.
page_paths = []
pages_by_stem = defaultdict(list)
for p in sorted(WIKI.rglob("*.md")):
    if p.name in ("index.md", "log.md"):
        continue
    page_paths.append(p)
    pages_by_stem[p.stem].append(p)

duplicate_stems = {
    stem: paths for stem, paths in pages_by_stem.items() if len(paths) > 1
}
pages = {stem: paths[0] for stem, paths in pages_by_stem.items()}


def page_ref(path):
    """Return a stable display key. Unique stems keep the old output format."""
    if len(pages_by_stem[path.stem]) == 1:
        return path.stem
    return path.relative_to(WIKI).with_suffix("").as_posix()

# Parse each page: extract frontmatter + outgoing wikilinks
WIKILINK = re.compile(r"\[\[([^\]\|#]+?)(?:\|[^\]]*)?\]\]")
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

outgoing = defaultdict(set)   # page -> set of pages it links to
incoming = defaultdict(set)   # page -> set of pages linking to it
frontmatter = {}              # page -> dict of fm fields (raw text per key)

for path in page_paths:
    name = page_ref(path)
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    fm_text = m.group(1) if m else ""
    body = text[m.end():] if m else text

    # crude frontmatter parse: only keys we care about
    fm = {}
    for line in fm_text.splitlines():
        line = line.rstrip()
        if line.startswith(("type:", "summary:", "sources:", "date:", "url:", "raw_sources:")):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
        # detect indented list items as part of last list-key (sources/raw_sources)
    # check whether sources/raw_sources actually has any value (list item or inline)
    has_sources = False
    in_sources_block = False
    for line in fm_text.splitlines():
        stripped = line.rstrip()
        if stripped.startswith(("sources:", "raw_sources:")):
            tail = stripped.split(":", 1)[1].strip()
            if tail:  # inline value like "sources: foo.md"
                has_sources = True
            in_sources_block = True
            continue
        if in_sources_block:
            if line.startswith(("  -", "    -", "\t-")) and line.strip().startswith("-"):
                has_sources = True
            elif stripped and not stripped.startswith(" "):
                in_sources_block = False
    fm["__has_sources__"] = has_sources
    frontmatter[name] = fm

    # strip code blocks and inline code before wikilink extraction
    no_fence = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    no_code = re.sub(r"`[^`\n]*`", "", no_fence)

    # extract outgoing wikilinks
    for link_text in WIKILINK.findall(no_code):
        target = link_text.strip()
        outgoing[name].add(target)
        incoming[target].add(name)

# also parse index.md to count its outgoing links (it's the catalog)
index_text = (WIKI / "index.md").read_text(encoding="utf-8")
INDEX_LINK = re.compile(r"\(([a-zA-Z0-9_-]+/)?([a-zA-Z0-9_-]+)\.md\)")
index_targets = set()
for prefix, stem in INDEX_LINK.findall(index_text):
    index_targets.add(stem)
indexed = set(pages) & index_targets

# ---------- Reports ----------
print("=" * 60)
print("WIKI LINT REPORT")
print("=" * 60)
print(f"Total page files (excluding index/log): {len(page_paths)}")
if duplicate_stems:
    print(f"Unique wikilink IDs: {len(pages)}")
print()

# 0. Duplicate page IDs
print(f"## 重複ページID（同じbasename）: {len(duplicate_stems)}")
for stem, paths in sorted(duplicate_stems.items()):
    rels = [str(p.relative_to(WIKI)) for p in paths]
    print(f"  - [[{stem}]] が曖昧: {', '.join(rels)}")
print()

# 1. Orphan detection: pages with no incoming wikilinks
orphans = sorted(page_ref(path) for path in page_paths if not incoming.get(path.stem))
print(f"## 孤立ページ（incoming wikilinkなし）: {len(orphans)}")
print("（index.md登録は別カウント）")
for name in orphans:
    stem = name.rsplit("/", 1)[-1]
    in_index = "✓index" if stem in indexed else "✗index"
    typ = frontmatter[name].get("type", "?").strip()
    print(f"  - [{typ}] {name} ({in_index})")
print()

# 2. Broken links: targets not in pages
referenced = set()
for src, targets in outgoing.items():
    referenced.update(targets)
broken = sorted(referenced - set(pages))
print(f"## 壊れたwikilink（リンク先ページが存在しない）: {len(broken)}")
broken_with_src = defaultdict(list)
for src, targets in outgoing.items():
    for t in targets:
        if t in broken:
            broken_with_src[t].append(src)
for target in broken:
    srcs = broken_with_src[target]
    print(f"  - [[{target}]] ← from: {', '.join(sorted(srcs))}")
print()

# 3. Missing index entries
missing_in_index = sorted(set(pages) - indexed)
print(f"## index.mdに未登録: {len(missing_in_index)}")
for name in missing_in_index:
    typ = frontmatter[name].get("type", "?").strip()
    print(f"  - [{typ}] {name}")
print()

# 4. Frontmatter health
print("## フロントマター不備")
missing_type = [n for n, fm in frontmatter.items() if "type" not in fm]
missing_summary = [n for n, fm in frontmatter.items() if "summary" not in fm]
missing_sources_required = [
    n for n, fm in frontmatter.items()
    if fm.get("type", "").strip() in ("source", "concept") and not fm["__has_sources__"]
]
print(f"  type欠落: {len(missing_type)}")
for n in missing_type:
    print(f"    - {n}")
print(f"  summary欠落: {len(missing_summary)}")
for n in missing_summary:
    print(f"    - {n}")
print(f"  sources欠落 (source/concept type): {len(missing_sources_required)}")
for n in missing_sources_required:
    typ = frontmatter[n].get("type", "?").strip()
    print(f"    - [{typ}] {n}")
print()

# 5. Frequently referenced concepts that don't have a page
print("## 頻出だがページがない名前（新規ページ候補）")
ref_count = defaultdict(int)
for src, targets in outgoing.items():
    for t in targets:
        if t not in pages:
            ref_count[t] += 1
candidates = sorted(ref_count.items(), key=lambda x: -x[1])
for name, cnt in candidates:
    if cnt >= 2:
        print(f"  - {cnt}回参照: [[{name}]]")
print()

# 6. Most-linked pages (positive signal)
print("## 最もリンクされているページ（top 10）")
top_incoming = sorted(((n, len(incoming[n])) for n in pages), key=lambda x: -x[1])[:10]
for name, cnt in top_incoming:
    print(f"  - {cnt:3d} ← {name}")
print()

# 7. Pages with very few outgoing links (poorly integrated)
print("## outgoing wikilinkが少ないページ（≤1）")
low_outgoing = sorted(
    page_ref(path) for path in page_paths if len(outgoing.get(page_ref(path), set())) <= 1
)
for name in low_outgoing:
    typ = frontmatter[name].get("type", "?").strip()
    cnt = len(outgoing.get(name, set()))
    print(f"  - [{typ}] ({cnt} out) {name}")
