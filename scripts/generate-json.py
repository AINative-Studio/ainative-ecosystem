#!/usr/bin/env python3
"""
generate-json.py
Convert all YAML data files → JSON for consumption by the website.

Outputs:
  dist/ainative-projects.json
  dist/ecosystem-tools.json
  dist/categories.json

Usage:
  python3 scripts/generate-json.py

Refs: AINative-Studio/ainative-ecosystem#6
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
DIST = ROOT / "dist"
DIST.mkdir(parents=True, exist_ok=True)


def load(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def dump(data: dict, path: Path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  Wrote {path.relative_to(ROOT)}")


def main():
    print("Generating JSON from YAML data files...")
    ts = datetime.now(timezone.utc).isoformat()

    # ainative-projects.yaml → dist/ainative-projects.json
    projects_file = DATA / "ainative-projects.yaml"
    if projects_file.exists():
        d = load(projects_file)
        projects = d.get("projects", [])
        dump({"generated_at": ts, "total": len(projects), "projects": projects},
             DIST / "ainative-projects.json")
    else:
        print("  WARNING: ainative-projects.yaml not found", file=sys.stderr)

    # ecosystem-tools.yaml → dist/ecosystem-tools.json
    tools_file = DATA / "ecosystem-tools.yaml"
    if tools_file.exists():
        d = load(tools_file)
        tools = d.get("tools", [])
        dump({"generated_at": ts, "total": len(tools), "tools": tools},
             DIST / "ecosystem-tools.json")
    else:
        print("  NOTE: ecosystem-tools.yaml not found — skipping")

    # categories.yaml → dist/categories.json
    cats_file = DATA / "categories.yaml"
    if cats_file.exists():
        d = load(cats_file)
        dump({"generated_at": ts, **d}, DIST / "categories.json")
    else:
        print("  WARNING: categories.yaml not found", file=sys.stderr)

    print("Done.")


if __name__ == "__main__":
    main()
