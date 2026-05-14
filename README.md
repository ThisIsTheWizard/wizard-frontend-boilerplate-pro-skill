# Wizard Frontend Boilerplate Pro

Scaffold a production-ready frontend app with a themed, sidebar-navigated
component showcase in one session. Covers five frameworks, 28 UI components,
an OKLCH color palette generator, and full light/dark theming — out of the box.

## What you get

- **28 UI components** across 6 categories, each with a live example and collapsible code snippet
- **Sidebar showcase** at `/library` with one route per component category
- **OKLCH color palette** — 8 built-in presets or custom hex/OKLCH input, 50–950 scales
- **Light/dark mode** with FOUC prevention and `localStorage` persistence
- **Tailwind v4** (`@theme` directive) with v3 fallback when needed
- **WCAG AA** contrast validation baked into the palette pipeline
- **TypeScript or JavaScript**, any of four package managers

## Supported frameworks

| Framework | Version | Router |
|---|---|---|
| Next.js | 15+ | App Router |
| React + Vite | Latest | React Router v7 |
| Vue | 3.5+ | Vue Router 4 |
| Nuxt | 4 | File-based (built-in) |
| SvelteKit | Svelte 5 | File-based (built-in) |

## Quick start

Invoke the skill from your AI agent. The skill interviews you through six
questions and then scaffolds the project end-to-end.

**Claude Code**
```
use the wizard-frontend-boilerplate-pro skill
```

**Cursor / Windsurf / Continue**
```
@wizard-frontend-boilerplate-pro scaffold a new Next.js project
```

**OpenCode**
```bash
opencode skill wizard-frontend-boilerplate-pro
```

**Gemini CLI / Codex / Aider**
```
load SKILL.md from the wizard-frontend-boilerplate-pro skill and follow it
```

## Interview questions

The skill asks six questions before running any commands:

1. **Framework** — Next.js / React + Vite / Vue 3 / Nuxt 4 / SvelteKit
2. **Version** — latest stable (default), specific semver, or LTS
3. **Language** — TypeScript (default) or JavaScript
4. **Tailwind version** — v4 (default) or v3
5. **Color theme** — pick a preset or supply custom hex/OKLCH values
6. **Project name + package manager** — auto-detected, confirm or override

## Color presets

| # | Preset | Neutral | Accent |
|---|---|---|---|
| 1 | Modern Slate | Slate | Indigo |
| 2 | Warm Earth | Stone | Amber |
| 3 | Fresh Mint | Zinc | Emerald |
| 4 | Royal | Gray | Violet |
| 5 | Sunset | Stone | Rose |
| 6 | Ocean | Slate | Cyan |
| 7 | Forest | Zinc | Green |
| 8 | Monochrome | Neutral | — |
| 9 | Custom | user hex/OKLCH | user hex/OKLCH |

## Component showcase

The `/library` route hosts the full showcase. Home (`/`) redirects there
immediately. The sidebar links to one route per category.

| Category | Route | Components |
|---|---|---|
| Inputs (7) | `/library/inputs` | Button, Input, Textarea, Select, Checkbox, RadioGroup, Switch |
| Display (6) | `/library/display` | Card, Badge, Avatar, Separator, Skeleton, Table |
| Feedback (5) | `/library/feedback` | Alert, Toast, Progress, Tooltip, Dialog |
| Navigation (4) | `/library/navigation` | Tabs, Breadcrumb, Pagination, NavigationMenu |
| Overlay (3) | `/library/overlay` | Popover, DropdownMenu, Sheet |
| Data viz (3) | `/library/data-viz` | Chart, DataTable, Calendar |

Each component block shows a heading, one-sentence description, a live
rendered example, and a `<CodeBlock>` toggle with the example source.

## Pairing with ui-ux-pro-max

When the `ui-ux-pro-max` skill is installed alongside this one, component
output uses that skill's higher-fidelity implementations. If it is not found,
the skill falls back to its own built-in Tailwind-only components automatically
— no configuration needed.

## Workflow phases

| Phase | What happens |
|---|---|
| 1 — Interview | Six questions collect framework, version, language, Tailwind, theme, project name |
| 2 — Version resolution | `check_versions.sh` queries the npm registry; you confirm or override |
| 3 — Scaffold | Framework CLI runs non-interactively; demo files removed; route stubs created |
| 4 — Theming | `generate_palette.py` builds OKLCH scales; `verify_contrast.py` gates WCAG AA |
| 5 — Components | 28 components adapted to the target framework and CSS token system |
| 6 — Showcase | Sidebar layout + 6 category routes installed from templates |
| 7 — Verify | Type check → build → dev server → route walk → theme toggle → contrast gate |

## Directory structure

```
wizard-frontend-boilerplate-pro/
├── SKILL.md                        # Main skill entry point (universal)
├── AGENTS.md                       # One-line alias → SKILL.md
├── workflow.md                     # Detailed playbook with verbatim commands
├── references/
│   ├── frameworks/                 # Per-framework scaffold guides
│   │   ├── nextjs.md
│   │   ├── react-vite.md
│   │   ├── vue.md
│   │   ├── nuxt.md
│   │   └── svelte-kit.md
│   ├── tailwind/
│   │   ├── v4-setup.md
│   │   ├── v3-setup.md
│   │   └── per-framework-gotchas.md
│   ├── ui-library/
│   │   ├── ui-ux-pro-max-bridge.md # Integration contract with sibling skill
│   │   ├── custom-tailwind.md      # Standalone fallback components
│   │   └── framework-adapters/
│   │       ├── react-adapter.md
│   │       ├── vue-adapter.md
│   │       └── svelte-adapter.md
│   ├── theming.md                  # CSS variable tokens, dark mode strategy
│   ├── component-catalog.md        # All 28 components — props, deps, source mapping
│   ├── showcase-layout.md          # Sidebar nav, header, CodeBlock utility
│   └── portability.md              # Notes for non-Claude agents, tested agent list
├── assets/
│   ├── color-presets.json          # Pre-computed OKLCH scales for all 8 presets
│   ├── showcase-templates/
│   │   ├── react/                  # layout, sidebar, 6 category page templates
│   │   ├── vue/                    # AppLayout, Sidebar, 6 page templates
│   │   └── svelte/                 # +layout, 6 route templates
│   └── theme-provider/
│       ├── react.tsx
│       ├── vue.ts
│       └── svelte.ts
├── scripts/
│   ├── check_versions.sh           # Query npm registry for latest stable versions
│   ├── detect_package_manager.sh   # Detect pnpm / yarn / npm / bun
│   ├── generate_palette.py         # Hex/OKLCH → 50–950 OKLCH scale + CSS vars
│   ├── locate_ui_ux_pro_max.sh     # Find sibling skill on disk
│   └── verify_contrast.py          # WCAG AA contrast gate
└── .claude-plugin/
    ├── plugin.json
    └── marketplace.json
```

## Requirements

- **Node.js** 18+ (20 LTS or 22 LTS recommended)
- **Python** 3.10+ (stdlib only — no pip installs required)
- **bash** (macOS, Linux, WSL)
- Any AI agent that can read markdown, run shell commands, and write files

## License

MIT — see [LICENSE](./LICENSE).
