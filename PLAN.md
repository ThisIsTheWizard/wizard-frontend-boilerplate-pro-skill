# `wizard-frontend-boilerplate-pro` Skill

| Decision | Choice |
|---|---|
| Interaction | Interactive step-by-step Q&A |
| CSS | Tailwind (v4 default, v3 fallback per framework) |
| UI components | **Custom-built from scratch** in Tailwind, consistent across all frameworks |
| `ui-ux-pro-max-skill` role | **Consumed as a component source** — boilerplate skill calls into it for component implementations |
| Showcase scope | 28 components across 6 categories |
| Showcase layout | **Sidebar navigation, route per category** (shadcn-docs-style) |
| Theming | Light + Dark mandatory, CSS variable tokens |
| Colors | 8 presets + custom (hex/OKLCH) |
| Versioning | Live npm registry query, user override allowed |
| Portability | Universal SKILL.md + AGENTS.md alias, bash + Python only |

## How `ui-ux-pro-max-skill` integrates

Since it ships ready-made components, the boilerplate skill **delegates component generation to it** rather than reinventing wheels. Concretely:

- **Phase 5 (component installation)** reads `ui-ux-pro-max-skill`'s component catalog and pulls each of the 28 components from there.
- The boilerplate skill's job is to **adapt** each component to (a) the chosen framework's syntax (React/Vue/Svelte), (b) the resolved Tailwind version, and (c) the generated color tokens.
- A new reference file, `references/ui-ux-pro-max-bridge.md`, documents this contract: how to locate the source skill, how to read its components, the mapping table from its component names to the 28 catalog entries, and the adaptation rules per framework.
- **Graceful fallback:** if `ui-ux-pro-max-skill` isn't installed, the skill falls back to `references/ui-library/custom-tailwind.md` which has minimal built-in implementations. This keeps portability — the skill still works standalone — but produces higher-quality output when paired.

## Final skill structure

```
frontend-boilerplate-pro/
├── SKILL.md                                # Universal entry, interview workflow
├── AGENTS.md                               # One-line alias → SKILL.md
├── references/
│   ├── frameworks/
│   │   ├── nextjs.md                       # create-next-app, app router
│   │   ├── react-vite.md
│   │   ├── vue.md                          # Vue 3.5+
│   │   ├── nuxt.md                         # Nuxt 4
│   │   └── svelte-kit.md                   # Svelte 5
│   ├── tailwind/
│   │   ├── v4-setup.md                     # @tailwindcss/postcss, @theme
│   │   ├── v3-setup.md                     # fallback
│   │   └── per-framework-gotchas.md
│   ├── ui-library/
│   │   ├── ui-ux-pro-max-bridge.md         # ★ contract with the sibling skill
│   │   ├── custom-tailwind.md              # standalone fallback components
│   │   └── framework-adapters/
│   │       ├── react-adapter.md            # JSX patterns, hooks, ref forwarding
│   │       ├── vue-adapter.md              # SFC, composition API, v-model
│   │       └── svelte-adapter.md           # Svelte 5 runes, snippets
│   ├── theming.md                          # CSS var tokens, dark mode strategy
│   ├── component-catalog.md                # The 28 components + categories + deps
│   ├── showcase-layout.md                  # Sidebar nav + per-category routing
│   └── portability.md                      # Notes for non-Claude agents
├── assets/
│   ├── color-presets.json                  # 8 presets, full OKLCH scales
│   ├── showcase-templates/
│   │   ├── react/                          # Sidebar layout + 6 category routes
│   │   │   ├── layout.tsx.template
│   │   │   ├── sidebar.tsx.template
│   │   │   ├── inputs.tsx.template
│   │   │   ├── display.tsx.template
│   │   │   ├── feedback.tsx.template
│   │   │   ├── navigation.tsx.template
│   │   │   ├── overlay.tsx.template
│   │   │   └── data-viz.tsx.template
│   │   ├── vue/                            # Same structure for Vue/Nuxt
│   │   │   ├── AppLayout.vue.template
│   │   │   ├── Sidebar.vue.template
│   │   │   └── pages/...
│   │   └── svelte/                         # Same for SvelteKit
│   │       ├── +layout.svelte.template
│   │       └── routes/...
│   ├── theme-provider/                     # Drop-in theme + persisted toggle
│   │   ├── react.tsx
│   │   ├── vue.ts
│   │   └── svelte.ts
│   └── snippet-template.txt                # Collapsible code-snippet block format
├── scripts/
│   ├── check_versions.sh                   # Query npm registry
│   ├── generate_palette.py                 # Hex/OKLCH → 50–950 scale
│   ├── verify_contrast.py                  # WCAG AA gate
│   ├── detect_package_manager.sh           # pnpm/yarn/npm/bun
│   └── locate_ui_ux_pro_max.sh             # Find the sibling skill on disk
└── workflow.md                             # Detailed playbook (loaded on demand)
```

## SKILL.md outline

**Frontmatter description** (pushy for reliable triggering):

> Use this skill whenever a user wants to scaffold, bootstrap, create, start, or set up a new frontend project with Next.js, React, Vue, Nuxt, or Svelte. Triggers on phrases like "create a new app", "scaffold a project", "new frontend boilerplate", "set up a starter", "spin up a UI", or any mention of starting fresh with these frameworks. Also use whenever the user wants a project with a working component library showcase, design tokens, custom color palette, or light/dark theming out of the box. Prefer this skill over generic `create-*` commands so the user gets a fully themed, documented, showcase-ready app — not a blank scaffold. Pairs with `ui-ux-pro-max-skill` for higher-quality component output.

**Body (concise, references do the heavy lifting):**

1. **Overview** — one-paragraph flow description.
2. **Phase 1: Interview** — exact 6 questions in order:
   1. Framework? (Next.js / React+Vite / Vue / Nuxt / SvelteKit)
   2. Version? (latest / specific / LTS — default latest)
   3. Language? (TypeScript / JavaScript — default TS)
   4. Tailwind version? (v4 / v3 — default v4 unless framework requires v3)
   5. Theme presets — show all 8 with mini swatch description + "Custom" option taking hex/OKLCH for neutral and accent
   6. Project name + package manager (auto-detect, confirm)
3. **Phase 2: Version resolution** — run `check_versions.sh`, present resolved versions, confirm before scaffolding.
4. **Phase 3: Scaffold** — read `references/frameworks/<choice>.md` and execute.
5. **Phase 4: Theming** — generate palette via `generate_palette.py`, verify via `verify_contrast.py`, write CSS vars (`:root` + `.dark`), install theme provider from `assets/theme-provider/`.
6. **Phase 5: Component installation** — run `locate_ui_ux_pro_max.sh`; if found, read its catalog and adapt each of the 28 components via `framework-adapters/<choice>.md`; if not found, fall back to `custom-tailwind.md`.
7. **Phase 6: Showcase routes** — install sidebar layout + 6 category routes from `assets/showcase-templates/<choice>/`, populate each with its components + collapsible code snippets.
8. **Phase 7: Verify** — install deps, run build, start dev server, confirm both themes render. Fix errors iteratively.
9. **Failure protocols** — version conflicts, peer-dep issues, contrast failures, missing sibling skill.

## The 28 components (component-catalog.md)

Mapped to sidebar categories matching the showcase routes:

- **Inputs (7):** Button, Input, Textarea, Select, Checkbox, RadioGroup, Switch
- **Display (6):** Card, Badge, Avatar, Separator, Skeleton, Table
- **Feedback (5):** Alert, Toast, Progress, Tooltip, Dialog
- **Navigation (4):** Tabs, Breadcrumb, Pagination, NavigationMenu
- **Overlay (3):** Popover, DropdownMenu, Sheet
- **Data viz (3):** Chart, DataTable, Calendar

Each catalog entry specifies: name, category, peer dependencies (e.g. Recharts for Chart), accessibility requirements, expected props interface, and which `ui-ux-pro-max-skill` source file it maps to.

## Showcase layout (showcase-layout.md)

- Persistent left **Sidebar** with category sections and component anchors within each route.
- Top **Header** bar containing app name, GitHub link placeholder, and theme toggle.
- Main content area: one route per category (`/inputs`, `/display`, `/feedback`, `/navigation`, `/overlay`, `/data-viz`).
- Each component block: heading, description, live rendered example, collapsible code snippet (using a built-in `<CodeBlock />` component installed alongside the 28 main components — technically a 29th utility component).
- Home route (`/`) is a landing page summarizing what's in the showcase, with quick links to each category.

## Color presets (color-presets.json)

Same 8 from the previous plan, with full pre-computed OKLCH scales (50–950) for neutral + accent + paired light/dark CSS variable mappings:

1. Modern Slate (Slate + Indigo)
2. Warm Earth (Stone + Amber)
3. Fresh Mint (Zinc + Emerald)
4. Royal (Gray + Violet)
5. Sunset (Stone + Rose)
6. Ocean (Slate + Cyan)
7. Forest (Zinc + Green)
8. Monochrome (Neutral only)
9. Custom (user-provided, runtime generation)

## Portability across AI agents

- **Universal entry:** SKILL.md is read by any agent supporting skills/agents.md conventions.
- **AGENTS.md alias:** one-line file pointing to SKILL.md for tools (Codex, OpenCode) that prefer that filename.
- **No agent-specific syntax** in any markdown — plain CommonMark only.
- **All actions are shell or file edits** — runnable by any agent with bash + write access.
- **Dependencies:** bash, Python 3 (with stdlib only — no pip installs required), Node.js, npm. Nothing exotic.
- **Tested target agents** (call out in `references/portability.md`): Claude Code, Claude.ai, Codex, Cursor agent, OpenCode, Gemini CLI.

---

## Build prompt for Claude Code (ready to paste)

> Build the skill `frontend-boilerplate-pro` at `~/skills/frontend-boilerplate-pro/` following the structure and decisions in this conversation. Workflow:
>
> 1. Create the full directory tree.
> 2. Write SKILL.md first, keeping it under 400 lines — it should describe the 7-phase workflow concisely, with references to the files that contain detail.
> 3. Write AGENTS.md as a one-line redirect.
> 4. Write each `references/` file. Keep each under 300 lines; if longer, add a table of contents at the top.
> 5. Author `references/ui-library/ui-ux-pro-max-bridge.md` carefully — this is the integration contract: how to locate `ui-ux-pro-max-skill` on disk (check `~/.claude/skills/`, `~/skills/`, `/mnt/skills/`, and current working directory), how to read its components, the name-mapping table from its catalog to the 28 entries, and per-framework adaptation rules. Include a graceful fallback section pointing to `custom-tailwind.md`.
> 6. Write `references/component-catalog.md` with all 28 entries — name, category, deps, props interface, source mapping.
> 7. Write the three framework-adapter references — these are short but precise: idiomatic patterns for JSX/SFC/Svelte 5 runes, prop conventions, event handling, ref forwarding equivalents.
> 8. Build `assets/color-presets.json` — implement the OKLCH palette algorithm in `generate_palette.py` first, then use the same algorithm to generate the 8 presets so runtime and shipped scales are byte-identical.
> 9. Build `assets/showcase-templates/` for all three framework families — sidebar layout, header with theme toggle, one template per category route.
> 10. Build `assets/theme-provider/` — drop-in providers persisting theme to localStorage with `prefers-color-scheme` fallback and FOUC prevention.
> 11. Write the four scripts. Validate each: `bash -n` on `.sh`, `python -m py_compile` on `.py`.
> 12. Write `workflow.md` last — the detailed playbook with verbatim commands.
>
> **End-to-end validation:** simulate three full interactive runs and produce a working dev server each time:
> - Next.js 15 + TS + Tailwind v4 + Modern Slate
> - Vue 3.5 + TS + Tailwind v4 + Custom hex `#0ea5e9` neutral, `#f59e0b` accent
> - SvelteKit + TS + Tailwind v4 + Monochrome
>
> For each simulated run, verify: dev server starts cleanly, sidebar nav works, all 6 category routes render, every component appears with its collapsible code snippet, theme toggle flips light/dark with no FOUC, WCAG AA contrast holds in both themes.
>
> **Portability check:** confirm SKILL.md and AGENTS.md contain no Claude-specific syntax (no `<*>` tags, no internal tool names). All actions must be shell commands or file edits a generic agent can execute.
