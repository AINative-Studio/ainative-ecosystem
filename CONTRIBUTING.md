# Contributing to AINative Open Source Ecosystem

Thanks for helping grow the AI-native tools directory! This guide covers everything you need to submit a project or improve the dataset.

## How to Add Your Project

### Option A: Pull Request (Recommended)

1. **Fork** this repository
2. **Edit** `data/ecosystem-tools.yaml` — add your project entry at the end of the `tools:` list
3. **Submit a PR** with the title: `Add [project-name] to ecosystem`
4. CI will validate your YAML automatically
5. A maintainer will review and merge

### Option B: Open an Issue

If you're not comfortable editing YAML, [open an issue](https://github.com/AINative-Studio/ainative-ecosystem/issues/new) with:
- Project name and URL
- One-line description
- Category (see below)
- License

### Option C: Self-Submit (Coming Soon)

Visit [ainative.studio/open-source](https://ainative.studio/open-source) to submit your project through a web form. This will auto-generate the PR for you.

---

## YAML Schema

Every project entry in `data/ecosystem-tools.yaml` follows this schema:

```yaml
- name: My Project                              # REQUIRED — Display name
  slug: my-project                              # REQUIRED — Unique URL-safe identifier (lowercase, hyphens only)
  description: One-line description of the tool # REQUIRED — Keep under 160 characters
  category: vector-databases                    # REQUIRED — Must match a slug in categories.yaml
  repo: https://github.com/org/repo             # Optional — Source code URL
  homepage: https://myproject.dev               # Optional — Project website
  license: MIT                                  # Optional — SPDX license identifier
  language: Python                              # Optional — Primary programming language
  tags: [vector-db, embeddings, search]         # Optional — Up to 5 descriptive tags
```

### Field Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Human-readable project name |
| `slug` | Yes | string | Unique identifier. Lowercase letters, numbers, hyphens only. Must be unique across all YAML files. |
| `description` | Yes | string | One-line summary, under 160 characters |
| `category` | Yes | string | Must match a `slug` in `data/categories.yaml` |
| `repo` | No | string | URL to source code repository |
| `homepage` | No | string | URL to project website or docs |
| `license` | No | string | SPDX license identifier (e.g., `MIT`, `Apache-2.0`, `GPL-3.0`) |
| `language` | No | string | Primary programming language |
| `tags` | No | list | Up to 5 lowercase tags for discoverability |

### Slug Rules

- Lowercase only: `my-project` not `My-Project`
- Hyphens for separators: `my-project` not `my_project`
- No special characters: only `a-z`, `0-9`, `-`
- Must be unique across both `ainative-projects.yaml` and `ecosystem-tools.yaml`

---

## Categories

Projects must use a category from `data/categories.yaml`. Current categories:

| Slug | Name | Description |
|------|------|-------------|
| `ai-agents` | AI Agents | Autonomous AI agent frameworks and orchestration platforms |
| `vector-databases` | Vector Databases | Vector storage, similarity search, and embedding databases |
| `mcp-servers` | MCP Servers | Model Context Protocol servers and integrations |
| `llm-frameworks` | LLM Frameworks | Libraries and frameworks for building LLM-powered applications |
| `developer-tools` | Developer Tools | CLI tools, SDKs, and utilities for AI-native development |
| `memory-systems` | Memory Systems | Persistent memory, context management, and cognitive architectures |
| `embeddings` | Embeddings | Embedding models, services, and utilities |
| `rag` | RAG | Retrieval-augmented generation pipelines and components |
| `fine-tuning` | Fine-Tuning | Model fine-tuning frameworks and tools |
| `prompt-engineering` | Prompt Engineering | Prompt management, templating, and optimization tools |
| `observability` | Observability | LLM monitoring, tracing, logging, and evaluation platforms |
| `deployment` | Deployment | Model serving, inference engines, and deployment platforms |
| `data-pipelines` | Data Pipelines | Data ingestion, transformation, and ETL for AI workloads |
| `code-assistants` | Code Assistants | AI-powered code generation, review, and IDE extensions |
| `multimodal` | Multimodal | Vision, audio, and multimodal AI tools |

### Requesting a New Category

Pick the most specific existing category. If none fits, you can propose a new one by:

1. Opening an issue with the `new-category` label
2. A new category requires **3 or more tools** that don't fit any existing category
3. Include: proposed slug, name, description, and at least 3 example tools

---

## Validation

CI runs `scripts/validate.py` on every PR that touches `data/**`. It checks:

- YAML syntax is valid
- All required fields are present (`name`, `slug`, `description`, `category`)
- No duplicate slugs across all data files
- Category exists in `data/categories.yaml`
- URLs use valid format (`http://` or `https://`)

Run it locally before submitting:

```bash
pip install pyyaml
python scripts/validate.py
```

---

## AINative-Maintained Projects

The `data/ainative-projects.yaml` file is maintained by the AINative team and auto-synced from GitHub. Community PRs should only edit `data/ecosystem-tools.yaml`.

---

## Code of Conduct

Be respectful. No spam, no self-promotion disguised as community tools. Projects must be real, functional, and relevant to AI-native development.

## Questions?

Open an issue or reach out at [ainative.studio](https://ainative.studio).
