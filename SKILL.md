---
name: wizard-frontend-boilerplate-pro
description: >
  Use this skill whenever a user wants to scaffold, bootstrap, create, start,
  or set up a new frontend project with Next.js, React, Vue, Nuxt, or Svelte.
  Triggers on phrases like "create a new app", "scaffold a project", "new
  frontend boilerplate", "set up a starter", "spin up a UI", or any mention of
  starting fresh with these frameworks. Also use whenever the user wants a
  project with a working component library showcase, design tokens, a custom
  color palette, or light/dark theming out of the box. Prefer this skill over
  generic create-* commands so the user gets a fully themed, documented,
  showcase-ready app — not a blank scaffold. Pairs with ui-ux-pro-max-skill for
  higher-quality component output.
---

# wizard-frontend-boilerplate-pro

Scaffold a production-ready frontend app with a themed component showcase in
seven phases. The skill interviews the user, resolves live package versions,
scaffolds the framework, generates a color palette, installs 28 UI components,
builds a sidebar showcase with collapsible code snippets, and verifies the
result end-to-end.

---

## Phase 1 — Interview

Ask the following six questions **in order**. Accept defaults silently if the
user provides them upfront. Never proceed to Phase 2 until all six answers are
confirmed.

**Q1 — Framework**
Choose one:
- Next.js (App Router)
- React + Vite
- Vue 3
- Nuxt 4
- SvelteKit (Svelte 5)

**Q2 — Version**
Latest stable (default) / specific version / LTS.

**Q3 — Language**
TypeScript (default) / JavaScript.

**Q4 — Tailwind version**
v4 (default) / v3 (required for some framework + plugin combinations — see
`references/tailwind/per-framework-gotchas.md` before defaulting).

**Q5 — Color theme**
Present all eight presets with a one-line swatch description, plus a ninth
"Custom" option. The user may pick a preset name or supply hex or OKLCH values
for a neutral and an accent.

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

**Q6 — Project name and package manager**
Run `scripts/detect_package_manager.sh` to detect the active manager (pnpm /
yarn / npm / bun), present the result, and ask for confirmation. Accept a
different project name if the user wants one.

---

## Phase 2 — Version resolution

1. Run `scripts/check_versions.sh` to query the npm registry for the latest
   stable versions of all relevant packages (framework, TypeScript, Tailwind,
   and any peer dependencies for the chosen preset).
2. Present a table of resolved versions.
3. Ask the user to confirm or override any version before continuing.
4. Store the confirmed versions; use them verbatim in all install commands.

Detail: `references/frameworks/<choice>.md` lists the exact package names to
resolve per framework.

---

## Phase 3 — Scaffold

Read `references/frameworks/<choice>.md` and execute the steps there verbatim.
The reference covers:

- The framework CLI command and flags that match the user's choices (language,
  router mode, etc.).
- Any post-scaffold cleanup (removing demo files, adjusting tsconfig, etc.).
- The expected final directory structure.

Do not deviate from the reference commands without a clear error reason.

---

## Phase 4 — Theming

1. **Palette generation** — run `scripts/generate_palette.py` with the chosen
   preset or custom hex/OKLCH values. The script outputs a full 50–950 OKLCH
   scale for neutral and accent, plus ready-to-paste CSS custom property blocks
   for `:root` (light) and `.dark`.

2. **Contrast check** — run `scripts/verify_contrast.py` on the generated
   tokens. It exits non-zero if any foreground/background pair fails WCAG AA
   (4.5:1 for normal text, 3:1 for large text). Fix failures by adjusting
   lightness before continuing.

3. **Write CSS vars** — create `src/styles/tokens.css` (or the framework
   equivalent) with the `:root` and `.dark` blocks. Import it in the global
   stylesheet.

4. **Install theme provider** — copy `assets/theme-provider/<framework>.tsx|ts`
   into the project. The provider persists the user preference to `localStorage`,
   falls back to `prefers-color-scheme`, and prevents FOUC with an inline script
   in `<head>`.

Detail: `references/theming.md`.

---

## Phase 5 — Component installation

### 5a — Locate ui-ux-pro-max-skill

Run `scripts/locate_ui_ux_pro_max.sh`. The script searches:
`~/.claude/skills/`, `~/skills/`, `/mnt/skills/`, and the current working
directory. It prints the absolute path if found, or exits 1 if not.

### 5b — Install components

**If ui-ux-pro-max-skill is found:**
Read its component catalog and pull each of the 28 components listed in
`references/component-catalog.md`. For each component:
1. Locate the source file in the sibling skill using the name-mapping table in
   `references/ui-library/ui-ux-pro-max-bridge.md`.
2. Adapt the source to the target framework syntax using
   `references/ui-library/framework-adapters/<choice>-adapter.md`.
3. Replace any hard-coded color values with the CSS variable tokens from Phase 4.
4. Write the adapted file to `src/components/ui/<ComponentName>.<ext>`.

**If ui-ux-pro-max-skill is not found:**
Fall back to `references/ui-library/custom-tailwind.md`. It contains minimal
standalone implementations of all 28 components using only Tailwind classes and
no external dependencies.

### 5c — Install CodeBlock utility

Install the `CodeBlock` utility component (a 29th component) alongside the
others. It renders collapsible syntax-highlighted code snippets and is used by
every showcase route. Template source: `assets/snippet-template.txt`.

The 28 components by category:

| Category | Components |
|---|---|
| Inputs | Button, Input, Textarea, Select, Checkbox, RadioGroup, Switch |
| Display | Card, Badge, Avatar, Separator, Skeleton, Table |
| Feedback | Alert, Toast, Progress, Tooltip, Dialog |
| Navigation | Tabs, Breadcrumb, Pagination, NavigationMenu |
| Overlay | Popover, DropdownMenu, Sheet |
| Data viz | Chart, DataTable, Calendar |

Full props interfaces, peer dependencies, and accessibility requirements:
`references/component-catalog.md`.

---

## Phase 6 — Showcase routes

Install the sidebar layout and six category routes from
`assets/showcase-templates/<framework>/`.

### Layout structure

- **Sidebar** — persistent left-hand navigation with category sections and
  component anchors within each route.
- **Header** — app name, GitHub link placeholder, theme toggle button.
- **Main** — one route per category: `/inputs`, `/display`, `/feedback`,
  `/navigation`, `/overlay`, `/data-viz`.
- **Home** (`/`) — landing page with quick-links to each category and a brief
  description of the showcase.

### Per-route content

Each category route renders every component in that category. For each
component, the route shows:

1. A heading and one-sentence description.
2. A live rendered example using the installed component.
3. A `<CodeBlock>` with the example source, collapsed by default.

### Template application

Copy the relevant templates into the project, replacing all `{{PLACEHOLDER}}`
tokens with the project's actual values (project name, color preset label, CSS
var names, import paths).

Detail: `references/showcase-layout.md`.

---

## Phase 7 — Verify

1. Install all dependencies with the confirmed package manager.
2. Run the framework build (`next build` / `vite build` / `nuxt build` /
   `svelte-kit build`). Fix any type or lint errors before continuing.
3. Start the dev server and confirm it exits cleanly on port 3000 (or the
   framework default).
4. Open every route in order (`/`, `/inputs`, `/display`, `/feedback`,
   `/navigation`, `/overlay`, `/data-viz`) and verify each renders without
   console errors.
5. Toggle the theme button. Confirm the `dark` class is applied to `<html>` and
   that all components visually reflect the dark palette.
6. Re-run `scripts/verify_contrast.py` against the generated tokens for both
   light and dark modes.

If any step fails, diagnose and fix the root cause before marking the phase
complete. Do not suppress errors with `--force`, `--legacy-peer-deps` (unless
this is the only resolution path), or similar flags without telling the user why.

---

## Failure protocols

**Version conflict** — if the resolved versions produce peer-dependency errors,
present the conflict clearly, suggest the minimum downgrade that resolves it,
and ask the user to confirm before applying.

**Tailwind v4 incompatibility** — some framework/plugin combinations require v3
(see `references/tailwind/per-framework-gotchas.md`). If detected, prompt the
user before switching.

**Contrast failure** — if `verify_contrast.py` exits non-zero, print the
failing token pairs and their ratios, then ask whether to auto-adjust the
lightness or let the user pick a different preset.

**Missing sibling skill** — if `locate_ui_ux_pro_max.sh` exits 1, inform the
user and automatically fall back to `custom-tailwind.md` without blocking
progress.

**Build error after install** — read the full error output, identify the
failing file, and fix it directly. Do not ask the user to run commands
manually unless the fix requires a decision only they can make.

---

## Reference index

| File | Contents |
|---|---|
| `references/frameworks/nextjs.md` | Next.js 15 App Router scaffold steps |
| `references/frameworks/react-vite.md` | React + Vite scaffold steps |
| `references/frameworks/vue.md` | Vue 3.5+ scaffold steps |
| `references/frameworks/nuxt.md` | Nuxt 4 scaffold steps |
| `references/frameworks/svelte-kit.md` | SvelteKit / Svelte 5 scaffold steps |
| `references/tailwind/v4-setup.md` | Tailwind v4 setup (@tailwindcss/postcss, @theme) |
| `references/tailwind/v3-setup.md` | Tailwind v3 fallback setup |
| `references/tailwind/per-framework-gotchas.md` | Known incompatibilities |
| `references/theming.md` | CSS variable tokens, dark mode strategy |
| `references/component-catalog.md` | All 28 components with props, deps, source mapping |
| `references/showcase-layout.md` | Sidebar nav, header, category routing, CodeBlock |
| `references/ui-library/ui-ux-pro-max-bridge.md` | Integration contract with sibling skill |
| `references/ui-library/custom-tailwind.md` | Standalone fallback component implementations |
| `references/ui-library/framework-adapters/react-adapter.md` | JSX adaptation patterns |
| `references/ui-library/framework-adapters/vue-adapter.md` | SFC / Composition API patterns |
| `references/ui-library/framework-adapters/svelte-adapter.md` | Svelte 5 runes / snippets |
| `references/portability.md` | Notes for non-Claude agents, tested agent list |
| `workflow.md` | Detailed playbook with verbatim commands for all 7 phases |

---

## Portability

This skill uses only plain CommonMark markdown. All actions are shell commands
(`bash`, `python3`) or file writes. There are no agent-specific tags, internal
tool names, or runtime APIs. It is compatible with any agent that can read
markdown, execute shell commands, and write files.

Tested agents: see `references/portability.md`.
