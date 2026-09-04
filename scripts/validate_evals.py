#!/usr/bin/env python3
"""Validate Moru's behavioral evaluation dataset without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


REQUIRED_CASE_FIELDS = {
    "id",
    "kind",
    "prompt",
    "fixture",
    "expectedBehavior",
    "expectedResultShape",
}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"cannot read evaluation dataset: {error}"]

    if payload.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")

    cases = payload.get("cases")
    if not isinstance(cases, list):
        return errors + ["cases must be an array"]

    counts: Counter[str] = Counter()
    seen_ids: set[str] = set()
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            errors.append(f"case {index} must be an object")
            continue

        missing = REQUIRED_CASE_FIELDS - set(case)
        if missing:
            errors.append(f"case {index} is missing: {', '.join(sorted(missing))}")

        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"case {index} has an invalid id")
        elif case_id in seen_ids:
            errors.append(f"duplicate case id: {case_id}")
        else:
            seen_ids.add(case_id)

        kind = case.get("kind")
        if kind not in {"positive", "negative"}:
            errors.append(f"case {case_id or index} kind must be positive or negative")
        else:
            counts[kind] += 1

        for field in ("prompt", "fixture", "expectedResultShape"):
            if not isinstance(case.get(field), str) or not case.get(field, "").strip():
                errors.append(f"case {case_id or index} has an invalid {field}")

        behavior = case.get("expectedBehavior")
        if not isinstance(behavior, list) or not behavior or not all(
            isinstance(item, str) and item.strip() for item in behavior
        ):
            errors.append(f"case {case_id or index} expectedBehavior must be a non-empty string array")

    if counts["positive"] < 5:
        errors.append("at least five positive cases are required")
    if counts["negative"] < 3:
        errors.append("at least three negative cases are required")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="evals/cases.json")
    args = parser.parse_args()
    errors = validate(Path(args.path).resolve())

    if errors:
        print("Moru evaluation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Moru evaluation dataset is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
