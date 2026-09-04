#!/usr/bin/env python3
"""Validate Moru's public plugin package without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_RUNTIME_PATHS = (
    ".codex-plugin/plugin.json",
    "skills/moru/SKILL.md",
    "skills/moru/agents/openai.yaml",
    "skills/moru/assets/MORU.template.md",
    "skills/moru/assets/moru-mark.svg",
    "assets/moru-mark.svg",
    "skills/moru/references/input-contract.md",
    "skills/moru/references/routing.md",
    "skills/moru/references/quality-contract.md",
)

PLUGIN_RELATIVE_PATH = Path("plugins/moru")
MARKETPLACE_RELATIVE_PATH = Path(".agents/plugins/marketplace.json")

REQUIRED_SOURCE_PATHS = (
    "VERSION",
    "evals/cases.json",
    ".agents/plugins/marketplace.json",
    "PRIVACY.md",
    "SUPPORT.md",
    "TERMS.md",
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


def validate(root: Path, packaged: bool = False) -> list[str]:
    errors: list[str] = []
    plugin_root = root if packaged else root / PLUGIN_RELATIVE_PATH

    for relative in REQUIRED_RUNTIME_PATHS:
        if not (plugin_root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if not packaged:
        for relative in REQUIRED_SOURCE_PATHS:
            if not (root / relative).is_file():
                errors.append(f"missing required source file: {relative}")

    manifest_path = plugin_root / ".codex-plugin/plugin.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"invalid plugin manifest JSON: {error}")
        else:
            if manifest.get("name") != "moru":
                errors.append("plugin manifest name must be 'moru'")
            version_path = root / "VERSION"
            if not packaged and version_path.is_file():
                if manifest.get("version") != version_path.read_text(encoding="utf-8").strip():
                    errors.append("plugin manifest version must match VERSION")
            elif not packaged:
                errors.append("VERSION is required when validating the source tree")
            if manifest.get("skills") != "./skills/":
                errors.append("plugin manifest skills must be './skills/'")

    skill_path = plugin_root / "skills/moru/SKILL.md"
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

    markdown_root = plugin_root if packaged else root
    for markdown_path in markdown_root.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        if "[TODO:" in text:
            errors.append(f"unfinished TODO marker: {markdown_path.relative_to(root)}")
        if re.search(r"[A-Za-z]:\\Users\\[^\\\s]+", text):
            errors.append(f"personal absolute path: {markdown_path.relative_to(root)}")
        for link in local_markdown_links(markdown_path):
            target = (markdown_path.parent / link).resolve()
            if not target.exists():
                errors.append(f"broken link in {markdown_path.relative_to(root)}: {link}")

    openai_yaml = plugin_root / "skills/moru/agents/openai.yaml"
    if openai_yaml.is_file():
        openai_yaml_text = openai_yaml.read_text(encoding="utf-8")
        if "$moru" not in openai_yaml_text:
            errors.append("agents/openai.yaml default_prompt must mention $moru")
        if "allow_implicit_invocation: false" not in openai_yaml_text:
            errors.append("Moru must disable implicit skill invocation")

    if not packaged:
        marketplace_path = root / MARKETPLACE_RELATIVE_PATH
        if marketplace_path.is_file():
            try:
                marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                errors.append(f"invalid marketplace JSON: {error}")
            else:
                if marketplace.get("name") != "moru":
                    errors.append("marketplace name must be 'moru'")
                if marketplace.get("interface", {}).get("displayName") != "Moru":
                    errors.append("marketplace displayName must be 'Moru'")
                plugins = marketplace.get("plugins")
                if not isinstance(plugins, list) or len(plugins) != 1:
                    errors.append("marketplace must contain exactly one plugin")
                else:
                    entry = plugins[0]
                    expected_source = {"source": "local", "path": "./plugins/moru"}
                    expected_policy = {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    }
                    if entry.get("name") != "moru":
                        errors.append("marketplace plugin name must be 'moru'")
                    if entry.get("source") != expected_source:
                        errors.append("marketplace plugin source must point to ./plugins/moru")
                    if entry.get("policy") != expected_policy:
                        errors.append("marketplace plugin policy is invalid")
                    if entry.get("category") != "Productivity":
                        errors.append("marketplace plugin category must be 'Productivity'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--packaged", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate(root, packaged=args.packaged)

    if errors:
        print("Moru skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Moru plugin package is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
