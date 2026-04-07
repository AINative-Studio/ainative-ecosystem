#!/usr/bin/env python3
"""Convert AI-Native-Dev-Community landscape tools to our ecosystem schema."""

import re
import yaml
from datetime import date

# Map source categories to our slugified categories
CATEGORY_MAP = {
    "Autonomous Agent": "ai-agents",
    "Browser": "browser",
    "Code Benchmark": "benchmarking",
    "Compliance": "compliance",
    "Design": "design",
    "Documentation": "documentation",
    "Editor": "ide",
    "Execution Sandbox": "sandbox",
    "Frontend & Mobile": "frontend",
    "Gateway": "gateway",
    "Infrastructure As Code": "infrastructure",
    "MCP": "mcp",
    "Migration": "migration",
    "Model": "model",
    "Nocode": "nocode",
    "Observability": "observability",
    "Prompting": "prompting",
    "Prototyping": "prototyping",
    "Requirements": "requirements",
    "Review": "review",
    "SRE": "sre",
    "Spec Driven": "spec-driven",
    "Terminal": "cli",
    "Testing": "testing",
    "Vuln Scanning": "security",
}

TODAY = date.today().isoformat()


def slugify(name: str) -> str:
    """Convert a tool name to a URL-friendly slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def normalize_date(date_str: str) -> str:
    """Convert DD/MM/YYYY to YYYY-MM-DD, or return today's date."""
    if not date_str:
        return TODAY
    try:
        parts = date_str.strip().split("/")
        if len(parts) == 3:
            d, m, y = parts
            return f"{y}-{int(m):02d}-{int(d):02d}"
    except (ValueError, IndexError):
        pass
    return TODAY


def convert(source_path: str, output_path: str):
    with open(source_path) as f:
        data = yaml.safe_load(f)

    tools = []
    seen_slugs = set()

    for domain in data.get("domains", []):
        for cat in domain.get("categories", []):
            cat_name = cat.get("name", "")
            our_category = CATEGORY_MAP.get(cat_name, slugify(cat_name))

            for tool in cat.get("tools", []):
                name = (tool.get("name") or "").strip()
                if not name:
                    continue

                slug = slugify(name)
                # Deduplicate — same tool may appear in multiple categories
                if slug in seen_slugs:
                    continue
                seen_slugs.add(slug)

                website = (tool.get("website_url") or "").strip()
                description = (tool.get("description") or "").strip()
                # Collapse multi-line descriptions to single line
                description = re.sub(r"\s+", " ", description)
                # Truncate very long descriptions
                if len(description) > 300:
                    description = description[:297] + "..."

                tags = [t for t in (tool.get("tags") or []) if t not in ("OSS", "GA")]
                if not tags:
                    tags = [our_category]

                entry = {
                    "name": name,
                    "slug": slug,
                    "website": website,
                    "description": description,
                    "category": our_category,
                    "tags": tags,
                    "open_source": bool(tool.get("oss", False)),
                    "date_added": normalize_date(tool.get("date_added", "")),
                }
                tools.append(entry)

    # Sort by name for readability
    tools.sort(key=lambda t: t["name"].lower())

    header = (
        "# AI-Native Developer Tools Ecosystem\n"
        "# Seeded from AI-Native-Dev-Community/ai-native-dev-landscape (MIT License)\n"
        "# Attribution: https://github.com/AI-Native-Dev-Community/ai-native-dev-landscape\n"
        "#\n"
        f"# Generated: {TODAY}\n"
        f"# Total tools: {len(tools)}\n\n"
    )

    output = {"tools": tools}
    yaml_str = yaml.dump(output, default_flow_style=False, sort_keys=False, allow_unicode=True)

    with open(output_path, "w") as f:
        f.write(header)
        f.write(yaml_str)

    print(f"Wrote {len(tools)} tools to {output_path}")


if __name__ == "__main__":
    convert("/tmp/source-tools.yaml", "data/ecosystem-tools.yaml")
