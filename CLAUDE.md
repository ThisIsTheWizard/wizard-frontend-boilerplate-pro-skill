# CLAUDE.md — `wizard-frontend-boilerplate-pro` Skill

This file provides guidance to Claude Code when working in this repository.

## Architecture

```
wizard-frontend-boilerplate-pro-skill/       # Repo root
├── skill.json                               # Root manifest (name, version, platforms, skills pointer)
├── CLAUDE.md                                # This file — dev guidance for Claude Code
├── README.md                                # Public-facing documentation
├── LICENSE                                  # MIT
├── PLAN.md                                  # Architecture decisions (source of truth)
├── TODO.md                                  # Ordered build checklist
├── .claude-plugin/
│   ├── plugin.json                          # Claude Marketplace plugin metadata
│   └── marketplace.json                     # Marketplace listing (plugins[] array)
└── .claude/skills/wizard-frontend-boilerplate-pro/   # ALL SKILL CONTENT LIVES HERE
    ├── SKILL.md                             # Universal entry point (7-phase workflow)
    ├── AGENTS.md                            # One-line alias → SKILL.md
    ├── workflow.md                          # Detailed playbook with verbatim commands
    ├── references/
    │   ├── frameworks/                      # Per-framework scaffold guides
    │   ├── tailwind/                        # v4 setup, v3 fallback, gotchas
    │   ├── ui-library/                      # Component integration + adapters
    │   ├── theming.md
    │   ├── component-catalog.md
    │   ├── showcase-layout.md
    │   └── portability.md
    ├── assets/
    │   ├── color-presets.json
    │   ├── showcase-templates/              # react/ vue/ svelte/
    │   ├── theme-provider/                  # react.tsx  vue.ts  svelte.ts
    │   └── snippet-template.txt
    └── scripts/
        ├── check_versions.sh
        ├── detect_package_manager.sh
        ├── generate_palette.py
        ├── locate_ui_ux_pro_max.sh
        └── verify_contrast.py
```

**Source of truth:** `.claude/skills/wizard-frontend-boilerplate-pro/`

All skill content (SKILL.md, references, assets, scripts) lives there. The root only holds repo infrastructure.

## Session convention

Each session completes **exactly one TODO item** from `TODO.md`. Do not move to the next item unless the user explicitly starts a new session for it.

Mark the item `[x]` in `TODO.md` when complete.

## Code quality

All generated code files (`.js`, `.ts`, `.tsx`, `.vue`, `.svelte`) must pass:

- **ESLint** — for linting
- **Prettier** — for formatting
- **prettier-plugin-perfectionist** — for import/property sorting

Apply these consistently. Do not leave files that would fail any of these checks.

## Reference files

- `PLAN.md` — architecture decisions and full skill structure (source of truth for build decisions)
- `TODO.md` — ordered build checklist, one item per session
- `.claude/skills/wizard-frontend-boilerplate-pro/SKILL.md` — the skill entry point itself
