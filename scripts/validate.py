#!/usr/bin/env python3
"""
validate.py
CI validation for PRs that modify ecosystem-tools.yaml or ainative-projects.yaml.

Checks:
  - Required fields present
  - Slugs are unique and URL-safe
  - Category exists in categories.yaml
  - URLs are syntactically valid (no schema check to avoid flakiness)

Usage:
  python3 scripts/validate.py

Exit 0 = pass, Exit 1 = validation errors found.

Refs: AINative-Studio/ainative-ecosystem#5
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
ERRORS = []


def err(msg: str):
    ERRORS.append(msg)
    print(f"  ERROR: {msg}", file=sys.stderr)


def validate_slug(slug: str) -> bool:
    return bool(re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', slug))


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def validate_projects(projects: list, valid_categories: set, context: str):
    slugs = set()
    required = ["name", "slug", "description", "category"]

    for i, p in enumerate(projects):
        loc = f"{context}[{i}] '{p.get('name', '?')}'"

        for field in required:
            if not p.get(field):
                err(f"{loc}: missing required field '{field}'")

        slug = p.get("slug", "")
        if slug:
            if not validate_slug(slug):
                err(f"{loc}: slug '{slug}' must be lowercase alphanumeric + hyphens")
            if slug in slugs:
                err(f"{loc}: duplicate slug '{slug}'")
            slugs.add(slug)

        cat = p.get("category", "")
        if cat and valid_categories and cat not in valid_categories:
            err(f"{loc}: unknown category '{cat}' (valid: {sorted(valid_categories)})")

        repo = p.get("repo", "")
        if repo and not (repo.startswith("http") or "/" in repo):
            err(f"{loc}: repo '{repo}' should be 'owner/name' or full URL")

    return slugs


def main():
    print("Validating YAML data files...")

    cats_file = ROOT / "data" / "categories.yaml"
    cats_data = load_yaml(cats_file)
    valid_categories = set()
    for section in ["ainative", "ecosystem"]:
        for cat in cats_data.get(section, []):
            if isinstance(cat, dict):
                valid_categories.add(cat.get("id", ""))
            else:
                valid_categories.add(str(cat))

    # Validate AINative projects
    projects_file = ROOT / "data" / "ainative-projects.yaml"
    if projects_file.exists():
        d = load_yaml(projects_file)
        projects = d.get("projects", [])
        print(f"\nValidating {len(projects)} AINative projects...")
        validate_projects(projects, valid_categories, "ainative-projects.yaml")
    else:
        err("data/ainative-projects.yaml not found")

    # Validate ecosystem tools
    tools_file = ROOT / "data" / "ecosystem-tools.yaml"
    if tools_file.exists():
        d = load_yaml(tools_file)
        tools = d.get("tools", [])
        print(f"\nValidating {len(tools)} ecosystem tools...")
        validate_projects(tools, set(), "ecosystem-tools.yaml")  # open category set
    else:
        print("\n  NOTE: data/ecosystem-tools.yaml not found — skipping")

    if ERRORS:
        print(f"\n{len(ERRORS)} validation error(s) found.")
        sys.exit(1)
    else:
        print("\nAll checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
