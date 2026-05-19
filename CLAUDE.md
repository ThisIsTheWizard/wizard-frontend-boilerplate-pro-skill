# CLAUDE.md — `wizard-frontend-boilerplate-pro` Skill

This file provides guidance to Claude Code when working in this repository.

## Architecture

Three locations — one source of truth. See [`docs/architecture.md`](docs/architecture.md) for the full explanation.

| Location | Role |
|---|---|
| **`src/wizard-frontend-boilerplate-pro/`** | **Source of truth** — edit here |
| **`.claude/skills/wizard-frontend-boilerplate-pro/`** | Symlink → `src/` — consumed by Claude Code |
| _(future)_ **`cli/assets/`** | Bundled copy for npm CLI installer |

```
wizard-frontend-boilerplate-pro-skill/
├── src/
│   └── wizard-frontend-boilerplate-pro/    # ← EDIT HERE (source of truth)
│       ├── SKILL.md                        # Universal entry point (7-phase workflow)
│       ├── AGENTS.md                       # One-line alias → SKILL.md
│       ├── workflow.md                     # Detailed playbook with verbatim commands
│       ├── references/
│       │   ├── frameworks/                 # Per-framework scaffold guides
│       │   ├── tailwind/                   # v4 setup, v3 fallback, gotchas
│       │   ├── ui-library/                 # Component integration + adapters
│       │   ├── theming.md
│       │   ├── component-catalog.md
│       │   ├── showcase-layout.md
│       │   └── portability.md
│       ├── assets/
│       │   ├── color-presets.json
│       │   ├── showcase-templates/         # react/ vue/ svelte/
│       │   ├── theme-provider/             # react.tsx  vue.ts  svelte.ts
│       │   └── snippet-template.txt
│       └── scripts/
│           ├── check_versions.sh
│           ├── detect_package_manager.sh
│           ├── generate_palette.py
│           ├── locate_ui_ux_pro_max.sh
│           └── verify_contrast.py
├── .claude/skills/wizard-frontend-boilerplate-pro/  # symlink → ../../src/…
├── docs/                                   # Developer documentation
│   ├── architecture.md
│   └── development.md
├── .github/workflows/                      # CI
│   ├── claude.yml
│   ├── claude-code-review.yml
│   └── python-ci.yml
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skill.json
├── CLAUDE.md
├── README.md
└── LICENSE
```

**Source of truth:** `src/wizard-frontend-boilerplate-pro/`

All skill content lives there. The `.claude/skills/` entry is a symlink — never edit files
there directly. The root holds only repo infrastructure (CI, docs, manifests).

## Session convention

Each session should have a clear, scoped goal agreed on at the start. Work on one improvement area at a time and commit when it is complete before moving to the next.

## Code quality

All generated code files (`.js`, `.ts`, `.tsx`, `.vue`, `.svelte`) must pass:

- **ESLint** — for linting
- **Prettier** — for formatting
- **prettier-plugin-perfectionist** — for import/property sorting

Apply these consistently. Do not leave files that would fail any of these checks.

## Reference files

- `src/wizard-frontend-boilerplate-pro/SKILL.md` — the skill entry point itself
- `docs/architecture.md` — three-location pattern and symlink setup
- `docs/development.md` — how to add presets, update references, run validation
