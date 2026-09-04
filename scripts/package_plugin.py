#!/usr/bin/env python3
"""Create a release zip containing only the installable Moru plugin files."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


PACKAGE_PATHS = (".codex-plugin", "skills", "assets")


def files_under(root: Path, relative: str):
    path = root / relative
    if path.is_file():
        yield path
    elif path.is_dir():
        yield from sorted(file for file in path.rglob("*") if file.is_file())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    output_dir = root / "dist"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"moru-{version}.zip"

    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for relative in PACKAGE_PATHS:
            for path in files_under(root, relative):
                archive.write(path, Path("moru") / path.relative_to(root))

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
