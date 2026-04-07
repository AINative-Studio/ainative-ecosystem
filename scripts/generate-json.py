#!/usr/bin/env python3
"""Convert YAML data files to JSON for site consumption.

Outputs:
- dist/ainative-projects.json
- dist/ecosystem-tools.json
- dist/categories.json
"""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DIST_DIR = ROOT / "dist"


def load_yaml(path: Path) -> dict:
    """Load a YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def write_json(data: object, path: Path) -> None:
    """Write JSON with pretty formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  Wrote {path.name} ({path.stat().st_size:,} bytes)")


def main():
    print("Generating JSON from YAML...\n")

    # Categories
    categories_path = DATA_DIR / "categories.yaml"
    if categories_path.exists():
        data = load_yaml(categories_path)
        write_json(data.get("categories", []), DIST_DIR / "categories.json")

    # AINative projects
    projects_path = DATA_DIR / "ainative-projects.yaml"
    if projects_path.exists():
        data = load_yaml(projects_path)
        write_json(data.get("projects", []), DIST_DIR / "ainative-projects.json")

    # Ecosystem tools
    tools_path = DATA_DIR / "ecosystem-tools.yaml"
    if tools_path.exists():
        data = load_yaml(tools_path)
        write_json(data.get("tools", []), DIST_DIR / "ecosystem-tools.json")

    print("\nDone.")


if __name__ == "__main__":
    main()
