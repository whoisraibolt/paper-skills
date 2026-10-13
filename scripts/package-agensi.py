#!/usr/bin/env python3
"""Package each skill as a zip for upload to the Agensi marketplace.

Writes dist/<skill>.zip for every directory under skills/. Each zip has SKILL.md
at its root, the skill's own subfolders kept as they are, and a copy of the
repository LICENSE.

Usage: python scripts/package-agensi.py

Standard library only. Uploading is done by hand; this script never touches the
network.
"""

import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
DIST_DIR = REPO / "dist"
LICENSE = REPO / "LICENSE"

MAX_BYTES = 50 * 1024 * 1024  # Agensi's limit per zip
REQUIRED_FIELDS = ("name", "description")
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}
IGNORED_DIRS = {"__pycache__", "node_modules", ".git"}
# Fixed timestamp, so the same tree always produces the same zip.
ZIP_DATE = (2020, 1, 1, 0, 0, 0)


class PackagingError(Exception):
    pass


def read_frontmatter(skill_md):
    """Return the top-level `key: value` pairs of a SKILL.md frontmatter."""
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise PackagingError(f"{skill_md}: no frontmatter (first line must be '---')")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        raise PackagingError(f"{skill_md}: frontmatter is never closed with '---'")

    fields = {}
    key = None
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            # A block scalar marker carries no text of its own.
            fields[key] = "" if value in {">", "|", ">-", "|-"} else value
        elif key and line[:1] in {" ", "\t"}:
            fields[key] = f"{fields[key]} {line.strip()}".strip()
    return {k: v.strip("'\"") for k, v in fields.items()}


def validate(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise PackagingError(f"{skill_dir}: SKILL.md not found")
    fields = read_frontmatter(skill_md)
    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            raise PackagingError(
                f"{skill_md}: frontmatter field '{field}' is missing or empty"
            )
    if fields["name"] != skill_dir.name:
        raise PackagingError(
            f"{skill_md}: frontmatter name '{fields['name']}' does not match "
            f"the directory name '{skill_dir.name}'"
        )
    if (skill_dir / "LICENSE").exists():
        raise PackagingError(
            f"{skill_dir}: already has a LICENSE; the repository one would overwrite it"
        )


def skill_files(skill_dir):
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.name in IGNORED_NAMES:
            continue
        if IGNORED_DIRS.intersection(path.relative_to(skill_dir).parts):
            continue
        yield path


def add(archive, source, arcname):
    info = zipfile.ZipInfo(arcname, date_time=ZIP_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, source.read_bytes())


def package(skill_dir):
    validate(skill_dir)
    target = DIST_DIR / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(target, "w") as archive:
        for path in skill_files(skill_dir):
            add(archive, path, path.relative_to(skill_dir).as_posix())
        add(archive, LICENSE, "LICENSE")

    with zipfile.ZipFile(target) as archive:
        entries = archive.infolist()
    if "SKILL.md" not in {entry.filename for entry in entries}:
        raise PackagingError(f"{target}: SKILL.md is not at the root of the zip")
    size = target.stat().st_size
    if size >= MAX_BYTES:
        raise PackagingError(
            f"{target}: {size / 1024 / 1024:.1f} MB, over Agensi's 50 MB limit"
        )

    print(f"\n{target.relative_to(REPO).as_posix()}  ({size / 1024:.1f} KB)")
    for entry in entries:
        print(f"  {entry.file_size:>8}  {entry.filename}")


def main():
    if not LICENSE.is_file():
        raise PackagingError(f"{LICENSE}: not found")
    skills = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skills:
        raise PackagingError(f"{SKILLS_DIR}: no skill directories found")
    DIST_DIR.mkdir(exist_ok=True)
    for skill_dir in skills:
        package(skill_dir)
    print(f"\n{len(skills)} zips written to {DIST_DIR.relative_to(REPO).as_posix()}/")


if __name__ == "__main__":
    try:
        main()
    except PackagingError as error:
        sys.exit(f"error: {error}")
