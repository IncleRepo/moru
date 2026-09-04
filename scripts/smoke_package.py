#!/usr/bin/env python3
"""Build and validate Moru from the clean release archive."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile


EXPECTED_ARCHIVE_PATHS = {
    "moru/.codex-plugin/plugin.json",
    "moru/skills/moru/SKILL.md",
    "moru/skills/moru/agents/openai.yaml",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    subprocess.run([sys.executable, str(root / "scripts/package_plugin.py"), str(root)], check=True)
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    archive_path = root / "dist" / f"moru-{version}.zip"

    with ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        missing = EXPECTED_ARCHIVE_PATHS - names
        if missing:
            print("Clean package smoke test failed:")
            for path in sorted(missing):
                print(f"- missing archive path: {path}")
            return 1
        forbidden = [name for name in names if "/.git/" in name or "/dist/" in name]
        if forbidden:
            print("Clean package smoke test failed:")
            for path in sorted(forbidden):
                print(f"- forbidden archive path: {path}")
            return 1

        with tempfile.TemporaryDirectory(prefix="moru-package-") as temp_dir:
            archive.extractall(temp_dir)
            subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts/validate_plugin.py"),
                    str(Path(temp_dir) / "moru"),
                    "--packaged",
                ],
                check=True,
            )

    print(f"Clean package smoke test passed: {archive_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
