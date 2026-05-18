#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "wiki"
OUTPUT_DIR = ROOT / ".pages" / "docs"
WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")


def build_stem_index(markdown_files: list[Path]) -> dict[str, Path]:
    stem_index: dict[str, Path] = {}
    duplicates: dict[str, list[Path]] = {}

    for path in markdown_files:
        relative_path = path.relative_to(SOURCE_DIR)
        stem = path.stem
        if stem in stem_index:
            duplicates.setdefault(stem, [stem_index[stem]]).append(relative_path)
            continue
        stem_index[stem] = relative_path

    if duplicates:
        lines = ["Duplicate wiki slugs detected:"]
        for stem, paths in sorted(duplicates.items()):
            rendered = ", ".join(str(path) for path in paths)
            lines.append(f"  - {stem}: {rendered}")
        raise SystemExit("\n".join(lines))

    return stem_index


def resolve_target(target: str, stem_index: dict[str, Path], source_file: Path) -> Path:
    target_path = Path(target)
    if target_path.suffix != ".md":
        candidate = SOURCE_DIR / f"{target}.md"
        if candidate.exists():
            return candidate.relative_to(SOURCE_DIR)

    candidate = SOURCE_DIR / target_path
    if candidate.exists():
        return candidate.relative_to(SOURCE_DIR)

    stem = target_path.stem
    if stem in stem_index:
        return stem_index[stem]

    raise SystemExit(f"Unresolved wikilink [[{target}]] in {source_file.relative_to(ROOT)}")


def rewrite_wikilinks(text: str, source_relative: Path, stem_index: dict[str, Path]) -> str:
    source_output_path = OUTPUT_DIR / source_relative

    def replace(match: re.Match[str]) -> str:
        raw_target = match.group(1).strip()
        label = (match.group(2) or "").strip()

        target_part, anchor = (raw_target.split("#", 1) + [""])[:2]
        target_relative = resolve_target(target_part, stem_index, SOURCE_DIR / source_relative)
        target_output_path = OUTPUT_DIR / target_relative
        link_path = os.path.relpath(target_output_path, source_output_path.parent).replace("\\", "/")
        if anchor:
            link_path = f"{link_path}#{anchor}"

        rendered_label = label or Path(target_part).stem
        return f"[{rendered_label}]({link_path})"

    rewritten_lines: list[str] = []
    inside_fence = False

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            inside_fence = not inside_fence
            rewritten_lines.append(line)
            continue

        if inside_fence or "`" not in line:
            rewritten_lines.append(WIKILINK_RE.sub(replace, line) if not inside_fence else line)
            continue

        parts = line.split("`")
        for index in range(0, len(parts), 2):
            parts[index] = WIKILINK_RE.sub(replace, parts[index])
        rewritten_lines.append("`".join(parts))

    return "".join(rewritten_lines)


def main() -> None:
    markdown_files = sorted(SOURCE_DIR.rglob("*.md"))

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stem_index = build_stem_index(markdown_files)

    for source_path in markdown_files:
        relative_path = source_path.relative_to(SOURCE_DIR)
        output_path = OUTPUT_DIR / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = source_path.read_text(encoding="utf-8")
        output_path.write_text(
            rewrite_wikilinks(content, relative_path, stem_index),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
