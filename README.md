# AINative Open Source Ecosystem

> 80+ open source projects. 624+ AI-native tools. One directory.

## What Is This

The data repository powering [ainative.studio/open-source](https://ainative.studio/open-source) — a consolidated hub for all AINative open source projects and the broader AI-native developer tools landscape.

## Submit Your Project

1. Fork this repo
2. Add your project to `data/ecosystem-tools.yaml`
3. Submit a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## Structure

```
data/
├── ainative-projects.yaml    # AINative open source projects (auto-synced from GitHub)
├── ecosystem-tools.yaml      # Broader AI-native tools directory (624+ tools)
└── categories.yaml           # Unified category taxonomy
scripts/
├── sync-github-repos.py      # Pull live stats from GitHub API
├── validate.py               # CI validation for PRs
└── generate-json.py          # YAML → JSON for site consumption
```

## License

Code: MIT | Data: CC-BY-SA 4.0

