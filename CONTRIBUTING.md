# Contributing to ainative-ecosystem

> Add your tool or project to the AI-Native Developer Ecosystem Directory.

## What belongs here

This repo tracks two things:

1. **AINative projects** (`data/ainative-projects.yaml`) — maintained by the AINative Studio team
2. **AI-native developer tools** (`data/ecosystem-tools.yaml`) — the broader landscape of tools developers use to build AI-native applications

We accept additions to the ecosystem tools list from anyone. AINative projects are managed internally.

---

## Adding a tool

### 1. Fork and clone

```bash
gh repo fork AINative-Studio/ainative-ecosystem --clone
cd ainative-ecosystem
```

### 2. Add your tool to `data/ecosystem-tools.yaml`

Append a new entry to the `tools` list. Required fields are marked with `*`:

```yaml
- name: "Your Tool Name"          # * Display name
  slug: "your-tool-name"          # * Unique, URL-safe slug (lowercase, hyphens only)
  description: "One sentence."    # * 10–120 chars. What it does, not marketing copy.
  category: "llm-frameworks"      # * See categories below
  homepage: "https://example.com" # Optional
  repo: "https://github.com/..."  # Optional but strongly encouraged
  license: "MIT"                  # Optional — use SPDX identifier
  language: "Python"              # Optional — primary language
  open_source: true               # Optional — default: inferred from license
  tags: ["tag1", "tag2"]          # Optional — max 6, lowercase kebab-case
```

### 3. Validate locally

```bash
pip install pyyaml
python3 scripts/validate.py
```

All checks must pass before opening a PR.

### 4. Open a PR

Branch name: `add/your-tool-slug`

PR title: `Add [Tool Name] to ecosystem`

CI will run `validate.py` automatically on your PR.

---

## Categories

| ID | Description |
|----|-------------|
| `llm-frameworks` | Frameworks for building LLM applications |
| `agent-frameworks` | Multi-agent orchestration and coordination |
| `vector-databases` | Vector search and embedding storage |
| `rag` | Retrieval-augmented generation tools |
| `mcp-servers` | Model Context Protocol servers |
| `agent-memory` | Persistent memory for AI agents |
| `observability` | Tracing, debugging, and monitoring |
| `prompt-engineering` | Prompt tools and structured generation |
| `embedding-services` | Embedding models and APIs |
| `inference` | LLM serving and inference engines |
| `ide` | AI-powered IDEs and coding assistants |
| `ui-components` | Chat and AI UI component libraries |
| `evaluation` | LLM and RAG evaluation frameworks |
| `integrations` | Connectors and adapters |
| `starter-kits` | Templates and boilerplate |
| `community` | Community projects and resources |

Don't see your category? Open an issue first.

---

## Criteria

We accept tools that are:
- Actually used by developers building AI-native applications
- Maintained (last commit within 12 months) or actively supported
- Have a public homepage or GitHub repo

We do not accept:
- Closed-source tools without a public API or documentation
- Promotional entries with no technical substance
- Duplicates of existing entries (open an issue to request merging)

---

## Questions

Open an issue or reach us at [ainative.studio](https://ainative.studio).
