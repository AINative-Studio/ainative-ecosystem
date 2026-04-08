#!/usr/bin/env python3
"""
sync-github-repos.py
Pull live GitHub stats (stars, forks, last_updated, language) for every
project in data/ainative-projects.yaml and write them to
dist/ainative-projects.json.

Usage:
  GITHUB_TOKEN=ghp_xxx python3 scripts/sync-github-repos.py

Refs: AINative-Studio/ainative-ecosystem#4
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "data" / "ainative-projects.yaml"
OUT_FILE = ROOT / "dist" / "ainative-projects.json"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
if not TOKEN:
    print("Warning: GITHUB_TOKEN not set — rate limit is 60 req/hr", file=sys.stderr)


def fetch_repo(repo: str) -> dict:
    url = f"https://api.github.com/repos/{repo}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code == 404:
        return {}
    r.raise_for_status()
    d = r.json()
    return {
        "stars": d.get("stargazers_count", 0),
        "forks": d.get("forks_count", 0),
        "language": d.get("language"),
        "last_updated": d.get("pushed_at"),
        "open_issues": d.get("open_issues_count", 0),
        "homepage": d.get("homepage") or None,
    }


def main():
    with open(DATA_FILE) as f:
        data = yaml.safe_load(f)

    projects = data.get("projects", [])
    print(f"Syncing {len(projects)} projects from GitHub...")

    enriched = []
    for i, project in enumerate(projects):
        repo = project.get("repo")
        if repo and "/" in repo:
            try:
                live = fetch_repo(repo)
                project.update(live)
                print(f"  [{i+1}/{len(projects)}] {repo} — {live.get('stars', '?')} stars")
            except Exception as e:
                print(f"  [{i+1}/{len(projects)}] {repo} — ERROR: {e}", file=sys.stderr)
            time.sleep(0.1)  # stay well within rate limit
        enriched.append(project)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(enriched),
        "projects": enriched,
    }

    with open(OUT_FILE, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nWrote {OUT_FILE}")


if __name__ == "__main__":
    main()
