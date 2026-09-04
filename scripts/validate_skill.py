#!/usr/bin/env python3
"""Validate Moru's public skill package without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PATHS = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/MORU.template.md",
    "assets/moru-mark.svg",
    "references/input-contract.md",
    "references/routing.md",
    "references/quality-contract.md",
)


def parse_frontmatter(skill_text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", skill_text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, raw_value = line.partition(":")
        if not separator:
            raise ValueError(f"unsupported frontmatter line: {line}")
        values[key.strip()] = raw_value.strip().strip('"').strip("'")
    return values


def local_markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text)
    return [link.split("#", 1)[0] for link in links if link and not re.match(r"^[a-z]+://|^#", link)]


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        try:
            frontmatter = parse_frontmatter(skill_text)
        except ValueError as error:
            errors.append(str(error))
        else:
            name = frontmatter.get("name", "")
            description = frontmatter.get("description", "")
            if name != "moru":
                errors.append("frontmatter name must be 'moru'")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                errors.append("frontmatter name must use lowercase hyphen-case")
            if not description:
                errors.append("frontmatter description is required")
            elif len(description) > 1024:
                errors.append("frontmatter description exceeds 1024 characters")

    for markdown_path in root.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        if "[TODO:" in text:
            errors.append(f"unfinished TODO marker: {markdown_path.relative_to(root)}")
        if re.search(r"[A-Za-z]:\\Users\\[^\\\s]+", text):
            errors.append(f"personal absolute path: {markdown_path.relative_to(root)}")
        for link in local_markdown_links(markdown_path):
            target = (markdown_path.parent / link).resolve()
            if not target.exists():
                errors.append(f"broken link in {markdown_path.relative_to(root)}: {link}")

    openai_yaml = root / "agents/openai.yaml"
    if openai_yaml.is_file() and "$moru" not in openai_yaml.read_text(encoding="utf-8"):
        errors.append("agents/openai.yaml default_prompt must mention $moru")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate(root)

    if errors:
        print("Moru skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Moru skill is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

