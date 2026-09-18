#!/usr/bin/env python3
"""Validate that public n8n exports contain no obvious deployment secrets."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / "workflows"

FORBIDDEN_KEYS = {"credentials", "pinData", "versionId", "meta"}
FORBIDDEN_PATTERNS = {
    "email": re.compile(r"[A-Z0-9._%+-]+@(?!example\.invalid)[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Windows user path": re.compile(r"[A-Z]:\\\\Users\\\\[^\\\\]+", re.I),
    "common secret assignment": re.compile(r"(?:api[_-]?key|client[_-]?secret|password|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}", re.I),
}


def walk(value, path="root"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield path, key, child
            yield from walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def main() -> int:
    errors = []
    for file in sorted(WORKFLOWS.glob("*.json")):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{file.name}: invalid JSON: {exc}")
            continue

        text = file.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{file.name}: possible {label}")

        node_names = {node.get("name") for node in data.get("nodes", [])}
        for path, key, child in walk(data):
            if key in FORBIDDEN_KEYS:
                errors.append(f"{file.name}: forbidden key {path}.{key}")
            if key == "node" and isinstance(child, str) and child not in node_names:
                errors.append(f"{file.name}: connection references missing node {child}")

        for source in data.get("connections", {}):
            if source not in node_names:
                errors.append(f"{file.name}: missing connection source {source}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed: workflow exports are valid JSON and no blocked patterns were found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
