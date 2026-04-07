#!/usr/bin/env python3
"""Validate ecosystem YAML data files.

Checks:
- YAML syntax is valid
- Required fields present (name, slug, description, category)
- No duplicate slugs across all data files
- Categories exist in categories.yaml
- URLs are valid format (not reachability)
"""

import sys
import re
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

REQUIRED_FIELDS = {"name", "slug", "description", "category"}
URL_PATTERN = re.compile(r"^https?://[^\s]+$")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def load_yaml(path: Path) -> dict:
    """Load a YAML file, exit on parse error."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"FAIL: {path.name} has invalid YAML syntax")
        print(f"  {e}")
        sys.exit(1)


def load_categories() -> set[str]:
    """Load valid category slugs from categories.yaml."""
    path = DATA_DIR / "categories.yaml"
    if not path.exists():
        print(f"FAIL: {path} not found")
        sys.exit(1)
    data = load_yaml(path)
    cats = data.get("categories", [])
    if not cats:
        print("FAIL: categories.yaml has no categories")
        sys.exit(1)
    slugs = set()
    for cat in cats:
        if "slug" not in cat:
            print(f"FAIL: category missing 'slug': {cat}")
            sys.exit(1)
        slugs.add(cat["slug"])
    return slugs


def validate_url(url: str, field: str, entry_name: str) -> list[str]:
    """Validate URL format."""
    if not URL_PATTERN.match(url):
        return [f"  {entry_name}: '{field}' is not a valid URL: {url}"]
    return []


def validate_entries(entries: list[dict], filename: str, valid_categories: set[str]) -> tuple[list[str], list[str]]:
    """Validate a list of project/tool entries. Returns (errors, slugs)."""
    errors = []
    slugs = []

    for i, entry in enumerate(entries):
        label = entry.get("name", f"entry #{i + 1}")

        # Required fields
        for field in REQUIRED_FIELDS:
            if field not in entry or not entry[field]:
                errors.append(f"  {filename} -> {label}: missing required field '{field}'")

        # Slug format
        slug = entry.get("slug", "")
        if slug:
            if not SLUG_PATTERN.match(slug):
                errors.append(f"  {filename} -> {label}: slug '{slug}' must be lowercase alphanumeric with hyphens")
            slugs.append(slug)

        # Category exists
        category = entry.get("category", "")
        if category and category not in valid_categories:
            errors.append(f"  {filename} -> {label}: category '{category}' not in categories.yaml")

        # URL fields
        for url_field in ("repo", "homepage"):
            if url_field in entry and entry[url_field]:
                errors.extend(validate_url(entry[url_field], url_field, f"{filename} -> {label}"))

    return errors, slugs


def main():
    print("Validating ecosystem data...\n")
    errors = []

    # Load categories
    valid_categories = load_categories()
    print(f"  Found {len(valid_categories)} categories")

    # Collect all slugs for duplicate check
    all_slugs: list[tuple[str, str]] = []  # (slug, source_file)

    # Validate each data file
    data_files = {
        "ainative-projects.yaml": "projects",
        "ecosystem-tools.yaml": "tools",
    }

    for filename, key in data_files.items():
        path = DATA_DIR / filename
        if not path.exists():
            print(f"  SKIP: {filename} not found")
            continue

        data = load_yaml(path)
        entries = data.get(key, [])
        if not entries:
            print(f"  WARN: {filename} has no {key}")
            continue

        print(f"  Validating {filename}: {len(entries)} entries")
        file_errors, slugs = validate_entries(entries, filename, valid_categories)
        errors.extend(file_errors)

        for s in slugs:
            all_slugs.append((s, filename))

    # Check for duplicate slugs across all files
    seen = {}
    for slug, source in all_slugs:
        if slug in seen:
            errors.append(f"  Duplicate slug '{slug}' found in {seen[slug]} and {source}")
        else:
            seen[slug] = source

    # Report
    print()
    if errors:
        print(f"FAILED with {len(errors)} error(s):\n")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print(f"PASSED: {len(all_slugs)} entries validated, 0 errors")


if __name__ == "__main__":
    main()
