# workflow.md — Detailed Playbook

Verbatim commands for every step of the seven-phase scaffold. Load this file
when you need the exact shell syntax for a given framework or phase. For the
high-level flow, see `SKILL.md`. For framework-specific detail beyond what is
shown here, see `references/frameworks/<choice>.md`.

---

## Table of contents

1. [Phase 1 — Interview](#phase-1--interview)
2. [Phase 2 — Auto-resolve](#phase-2--auto-resolve)
3. [Phase 3 — Scaffold](#phase-3--scaffold)
4. [Phase 4 — Theming](#phase-4--theming)
5. [Phase 5 — Component installation](#phase-5--component-installation)
6. [Phase 6 — Showcase routes](#phase-6--showcase-routes)
7. [Phase 7 — Verify](#phase-7--verify)
8. [Failure protocols](#failure-protocols)

---

## Phase 1 — Interview

Collect all **five answers** before running any commands. Never start Phase 2
early. Three values are resolved automatically — do not ask:

| Auto value | Rule |
|---|---|
| Version | Always latest stable. Use in all install commands. |
| Tailwind version | Check `references/tailwind/per-framework-gotchas.md` after Q1 + Q2 are known. Default v4; switch to v3 silently if a conflict is detected, or prompt only if user input is needed. |
| Package manager | Run `scripts/detect_package_manager.sh`. Store as `PM`. Only ask if the script returns ambiguous/no result. |

```
Q1  Framework?
    1) Next.js (App Router)
    2) React + Vite
    3) Vue 3
    4) Nuxt 4
    5) SvelteKit (Svelte 5)

Q2  UI library?
    Show only rows compatible with the framework chosen in Q1.
    Default: 0 (Custom Tailwind — zero extra deps).
    Libraries marked [TW] install Tailwind automatically.

    All frameworks:
      0) Custom Tailwind [TW]  — no extra deps, hand-rolled Tailwind components
      1) shadcn/ui       [TW]  — React/Next (native), Vue (shadcn-vue), Svelte (shadcn-svelte)
      3) Bootstrap             — react-bootstrap / bootstrap-vue-next / svelte
      4) DaisyUI         [TW]  — Tailwind plugin, works in all frameworks

    React / Next.js only:
      2) Material UI           — @mui/material + emotion
      5) Chakra UI             — @chakra-ui/react
      6) Mantine               — @mantine/core
      7) Ant Design            — antd
     11) NextUI / HeroUI [TW]  — @heroui/react (Tailwind-based)

    Vue / Nuxt only:
      8) PrimeVue              — primevue
      9) Vuetify               — vuetify
     12) Element Plus          — element-plus

    React + Vue (not Svelte):
     10) Headless UI     [TW]  — @headlessui/react or @headlessui/vue

    Store the answer as UI_LIB (e.g. "shadcn", "mui", "bootstrap", "daisy",
    "chakra", "mantine", "antd", "primevue", "vuetify", "headlessui",
    "heroui", "elementplus", or "custom").

Q3  Language?
    [ TypeScript (default) | JavaScript ]

Q4  Color theme?
    1) Modern Slate   — slate neutral + indigo accent
    2) Warm Earth     — stone neutral + amber accent
    3) Fresh Mint     — zinc neutral + emerald accent
    4) Royal          — gray neutral + violet accent
    5) Sunset         — stone neutral + rose accent
    6) Ocean          — slate neutral + cyan accent
    7) Forest         — zinc neutral + green accent
    8) Monochrome     — neutral only, no accent hue
    9) Custom         — provide hex or oklch() values for neutral and accent

Q5  App name?
    No default. Required before continuing.
```

---

## Phase 2 — Auto-resolve

Run both commands immediately after the interview. No user interaction needed
unless an anomaly is found.

### 2a — Detect package manager

```bash
bash scripts/detect_package_manager.sh
# Output: one of:  bun  |  pnpm  |  yarn  |  npm
```

Store as `PM`. Only ask the user if the script returns no result or multiple
candidates.

### 2b — Query latest versions

```bash
bash scripts/check_versions.sh --json
```

Store all resolved versions as variables (e.g. `NEXT_VERSION`, `TW_VERSION`).
Use them verbatim in every install command — never re-query mid-session.

Key packages per framework:

| Framework | Packages resolved |
|---|---|
| Next.js | `next`, `react`, `react-dom`, `tailwindcss`, `@tailwindcss/postcss` |
| React + Vite | `vite`, `react`, `react-dom`, `react-router-dom`, `tailwindcss`, `@tailwindcss/vite` |
| Vue 3 | `vue`, `vite`, `vue-router`, `tailwindcss`, `@tailwindcss/vite` |
| Nuxt 4 | `nuxt`, `vue`, `tailwindcss`, `@nuxtjs/tailwindcss` |
| SvelteKit | `@sveltejs/kit`, `svelte`, `tailwindcss`, `@tailwindcss/vite` |

### 2c — Tailwind compatibility check

```bash
# Check if the chosen framework + UI_LIB combo requires Tailwind v3
grep -i "<FW>" references/tailwind/per-framework-gotchas.md
```

- If no conflict → set `TW_MAJOR=4`, proceed silently.
- If conflict detected → set `TW_MAJOR=3`, inform the user once, continue.
- If `UI_LIB` is `mui`, `chakra`, `mantine`, `antd`, `primevue`, `vuetify`,
  or `elementplus` → skip Tailwind install entirely, set `TW_MAJOR=none`.

---

## Phase 3 — Scaffold

Load `references/frameworks/<FW>.md` and follow it verbatim.

Pass the variables resolved in Phase 2:

| Variable | Value |
|---|---|
| `PM` | detected package manager |
| `PROJECT_NAME` | from Q5 |
| `LANG` | `ts` or `js` from Q3 |
| `TW_MAJOR` | `4`, `3`, or `none` from Phase 2c |
| version vars | e.g. `NEXT_VERSION`, `TW_VERSION` — from Phase 2b |

The reference file covers: CLI scaffold command (per `PM` and `LANG`),
post-scaffold cleanup, Tailwind setup (v4 when `TW_MAJOR=4`, v3 when
`TW_MAJOR=3`, skipped when `TW_MAJOR=none`), tsconfig adjustments, and an
initial type-check + dev-server smoke test.

| Framework | Reference file |
|---|---|
| Next.js | `references/frameworks/nextjs.md` |
| React + Vite | `references/frameworks/react-vite.md` |
| Vue 3 | `references/frameworks/vue.md` |
| Nuxt 4 | `references/frameworks/nuxt.md` |
| SvelteKit | `references/frameworks/svelte-kit.md` |

---

## Phase 4 — Theming

### 4a — Generate palette

**Named preset**

```bash
python3 scripts/generate_palette.py --preset "Modern Slate"
# Prints @theme CSS block to stdout
```

**Custom hex seeds**

```bash
python3 scripts/generate_palette.py "#0ea5e9" "#f59e0b"
```

**Custom OKLCH seeds**

```bash
python3 scripts/generate_palette.py "oklch(55% 0.18 200)" "oklch(70% 0.15 85)"
```

**Write `tokens.css` directly** (full `@theme` + `:root` + `.dark` in one pass):

```bash
# Next.js / React + Vite
python3 scripts/generate_palette.py --preset "Modern Slate" \
  > src/styles/tokens.css

# Vue 3
python3 scripts/generate_palette.py --preset "Modern Slate" \
  > src/styles/tokens.css

# Nuxt 4
python3 scripts/generate_palette.py --preset "Modern Slate" \
  > assets/styles/tokens.css

# SvelteKit
python3 scripts/generate_palette.py --preset "Modern Slate" \
  > src/lib/styles/tokens.css
```

> The default output already includes `@theme`, `:root`, and `.dark` blocks.
> No post-processing is needed.

### 4b — Verify contrast

```bash
# Check all presets against assets/color-presets.json (auto-located)
python3 scripts/verify_contrast.py

# Check a single preset only
python3 scripts/verify_contrast.py --only "Modern Slate"

# Check a custom color pair directly (spot-check)
python3 scripts/verify_contrast.py "#0f172a" "#f8fafc"

# Quiet mode — print failures only
python3 scripts/verify_contrast.py --quiet
```

Exit code is `0` if all pairs pass WCAG AA (4.5:1 for normal text, 3:1 for
muted/large text). If non-zero, adjust lightness of the failing stops and
re-generate `tokens.css` before continuing.

### 4c — Install theme provider

Copy the provider from `assets/theme-provider/` to the project:

| Framework | Source | Destination |
|---|---|---|
| Next.js | `assets/theme-provider/react.tsx` | `src/components/ThemeProvider.tsx` |
| React + Vite | `assets/theme-provider/react.tsx` | `src/components/ThemeProvider.tsx` |
| Vue 3 | `assets/theme-provider/vue.ts` | `src/plugins/theme-provider.ts` |
| Nuxt 4 | `assets/theme-provider/vue.ts` | `plugins/theme-provider.ts` |
| SvelteKit | `assets/theme-provider/svelte.ts` | `src/lib/theme-provider.ts` |

Mount the provider in the root layout:

- **Next.js** — import `ThemeProvider` and wrap `{children}` inside `src/app/layout.tsx`
- **React + Vite** — import and wrap `<App />` inside `src/main.tsx`
- **Vue 3** — `app.use(themeProvider)` inside `src/main.ts`
- **Nuxt 4** — Nuxt auto-registers files under `plugins/`; no manual wiring needed
- **SvelteKit** — call `initTheme()` inside `<script>` in `src/routes/+layout.svelte`

**FOUC-prevention inline script** — add as the first child of `<head>`:

```html
<script>
  (function () {
    var stored = localStorage.getItem('theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var theme = stored || (prefersDark ? 'dark' : 'light');
    if (theme === 'dark') document.documentElement.classList.add('dark');
  })();
</script>
```

For Next.js App Router, use `<Script strategy="beforeInteractive">` inside the
`<head>` element in `src/app/layout.tsx`. For all Vite-based frameworks, place
the raw `<script>` tag in the `<head>` of `index.html`.

---

## Phase 5 — Component installation

### 5a — Route by UI_LIB

Branch on `UI_LIB`:

#### UI_LIB = "custom" (default)

```bash
bash scripts/locate_ui_ux_pro_max.sh
# Prints absolute path on success (exit 0)
# Prints error to stderr and exits 1 if not found
```

Store the result as `UI_SKILL_PATH`.

**If skill found** — for each of the 28 components:
1. Find the source using the name-mapping table in
   `references/ui-library/ui-ux-pro-max-bridge.md`.
2. Adapt to the target framework using
   `references/ui-library/framework-adapters/<choice>-adapter.md`:
   - **React** — JSX, hooks, `React.forwardRef`, `cn()` for class merging
   - **Vue** — SFC `<script setup>`, `defineProps`, `defineEmits`, `v-model`
   - **Svelte 5** — `$props()` rune, snippets (`{@render children()}`), `$state()`
3. Replace any hard-coded color values with CSS variable tokens from Phase 4.
4. Write the adapted file to the destinations in the table below.

**If skill not found** — use implementations from
`references/ui-library/custom-tailwind.md` (minimal Tailwind-only, zero deps).
Write them to the same destinations.

#### UI_LIB = named library (shadcn | mui | bootstrap | daisy | chakra | mantine | antd | primevue | vuetify)

Do **not** run `locate_ui_ux_pro_max.sh`. Instead:

1. Read `references/ui-library/<UI_LIB>.md` in full.
2. Follow its install, provider wiring, and theming steps exactly.
3. Consult the Library Component Mapping table in
   `references/component-catalog.md` to identify the native component for each
   of the 28 catalog slots.
4. Write thin wrapper files (if needed for consistent import paths) or
   re-export library components directly to the destinations below.

#### Component destinations (all paths)

| Framework | Destination |
|---|---|
| Next.js / React + Vite | `src/components/ui/<ComponentName>.tsx` |
| Vue 3 / Nuxt 4 | `src/components/ui/<ComponentName>.vue` |
| SvelteKit | `src/lib/components/ui/<ComponentName>.svelte` |

### 5b — Install 28 components

### 5c — Install cn() utility

```bash
${PM} add clsx tailwind-merge
```

Write the helper:

```ts
// Next.js / React + Vite / Vue 3 / Nuxt 4 → src/lib/utils.ts (or utils/utils.ts for Nuxt)
// SvelteKit → src/lib/utils/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 5d — Install CodeBlock utility

Using `assets/snippet-template.txt` as the markup reference, create a
framework-native `CodeBlock` component:

| Framework | Path |
|---|---|
| Next.js / React + Vite | `src/components/CodeBlock.tsx` |
| Vue 3 / Nuxt 4 | `src/components/CodeBlock.vue` |
| SvelteKit | `src/lib/components/CodeBlock.svelte` |

Props: `code: string`, `language: string` (optional, default `"tsx"`).
Behavior: renders `<pre><code>` block, with a toggle button that collapses the
block to ~4 lines and expands it on click. Collapsed state is the default.

---

## Phase 6 — Showcase routes

### 6a — Resolve template folder

Determine the template source directory from `UI_LIB` and the framework family:

```
UI_LIB = "custom"  →  assets/showcase-templates/<framework-family>/
UI_LIB = <other>   →  assets/showcase-templates/<framework-family>-<UI_LIB>/
```

Framework family mapping:

| Framework | Family |
|---|---|
| Next.js | `react` |
| React + Vite | `react` |
| Vue 3 | `vue` |
| Nuxt 4 | `vue` |
| SvelteKit | `svelte` |

Examples:
- Next.js + custom → `assets/showcase-templates/react/`
- Next.js + shadcn → `assets/showcase-templates/react-shadcn/`
- Vue 3 + Bootstrap → `assets/showcase-templates/vue-bootstrap/`
- SvelteKit + DaisyUI → `assets/showcase-templates/svelte-daisy/`

### 6b — Install layout templates

Copy from the resolved template folder and place in the project:

| Framework | Template files | Destination |
|---|---|---|
| Next.js | `layout.tsx.template`, `sidebar.tsx.template` | `src/app/library/layout.tsx`, `src/components/Sidebar.tsx` |
| React + Vite | `layout.tsx.template`, `sidebar.tsx.template` | `src/components/LibraryLayout.tsx`, `src/components/Sidebar.tsx` |
| Vue 3 / Nuxt 4 | `AppLayout.vue.template`, `Sidebar.vue.template` | `src/components/AppLayout.vue`, `src/components/Sidebar.vue` |
| SvelteKit | `+layout.svelte.template` | `src/routes/library/+layout.svelte` |

Replace all `{{PLACEHOLDER}}` tokens in every copied file:

| Token | Value |
|---|---|
| `{{PROJECT_NAME}}` | User's project name |
| `{{COLOR_PRESET}}` | Selected preset label (e.g. `"Modern Slate"`) |
| `{{NEUTRAL_VAR}}` | `--color-neutral` |
| `{{ACCENT_VAR}}` | `--color-accent` |
| `{{IMPORT_ALIAS}}` | `@/` for React/Vue/Next.js; `$lib/` for SvelteKit |

### 6c — Install category page templates

Copy the six category templates from the resolved folder and write them to the
routes established in Phase 3:

| Category | React destination | Vue destination | Svelte destination |
|---|---|---|---|
| Inputs | `src/pages/Inputs.tsx` | `src/views/InputsView.vue` | `src/routes/library/inputs/+page.svelte` |
| Display | `src/pages/Display.tsx` | `src/views/DisplayView.vue` | `src/routes/library/display/+page.svelte` |
| Feedback | `src/pages/Feedback.tsx` | `src/views/FeedbackView.vue` | `src/routes/library/feedback/+page.svelte` |
| Navigation | `src/pages/Navigation.tsx` | `src/views/NavigationView.vue` | `src/routes/library/navigation/+page.svelte` |
| Overlay | `src/pages/Overlay.tsx` | `src/views/OverlayView.vue` | `src/routes/library/overlay/+page.svelte` |
| Data viz | `src/pages/DataViz.tsx` | `src/views/DataVizView.vue` | `src/routes/library/data-viz/+page.svelte` |

> For Next.js, templates go to `src/app/library/<category>/page.tsx` (not `src/pages/`).

### 6d — Install /library landing page

The `/library` landing is generated (not from a template). Compose six `<Card>`
components — one per category — each containing:

- Category name as heading
- Component count (from `references/component-catalog.md`)
- One-line description of the category
- A link/button navigating to the category route

Categories and counts:

| Category | Route | Count |
|---|---|---|
| Inputs | `/library/inputs` | 7 |
| Display | `/library/display` | 6 |
| Feedback | `/library/feedback` | 5 |
| Navigation | `/library/navigation` | 4 |
| Overlay | `/library/overlay` | 3 |
| Data viz | `/library/data-viz` | 3 |

---

## Phase 7 — Verify

### 7a — Install all dependencies

```bash
${PM} install
```

### 7b — Type check

```bash
# Next.js / React + Vite
npx tsc --noEmit

# Vue 3 / Nuxt 4
npx vue-tsc --noEmit

# SvelteKit
npx svelte-check --tsconfig ./tsconfig.json
```

Fix every reported error. Do not use `// @ts-ignore` or `as any` to silence
errors without a documented reason.

### 7c — Build

```bash
# Next.js
${PM} run build                  # runs next build

# React + Vite / Vue 3 / SvelteKit
${PM} run build                  # runs vite build

# Nuxt 4
${PM} run build                  # runs nuxt build
```

A clean build (exit 0) is required before starting the dev server. Build
errors indicate missing imports or broken templates — fix them before 7d.

### 7d — Dev server

```bash
${PM} run dev
```

Expected start URLs:

| Framework | Default URL |
|---|---|
| Next.js | http://localhost:3000 |
| React + Vite | http://localhost:5173 |
| Vue 3 | http://localhost:5173 |
| Nuxt 4 | http://localhost:3000 |
| SvelteKit | http://localhost:5173 |

### 7e — Route verification

Visit every route and confirm it renders without console errors:

```
/                        → immediate redirect to /library
/library                 → landing page with 6 category cards
/library/inputs          → Button, Input, Textarea, Select, Checkbox, RadioGroup, Switch
/library/display         → Card, Badge, Avatar, Separator, Skeleton, Table
/library/feedback        → Alert, Toast, Progress, Tooltip, Dialog
/library/navigation      → Tabs, Breadcrumb, Pagination, NavigationMenu
/library/overlay         → Popover, DropdownMenu, Sheet
/library/data-viz        → Chart, DataTable, Calendar
```

For each route confirm:
- Every component in the category is rendered with a heading and description
- A `<CodeBlock>` toggle appears below each component and expands/collapses
- No `undefined`, `null`, or `[object Object]` renders as visible text
- The Sidebar highlights the active category link

### 7f — Theme toggle

1. Click the theme toggle button in the Header.
2. Open browser DevTools → Elements. Confirm `<html>` has class `dark`.
3. All component backgrounds, text, and borders visually reflect the dark palette.
4. Reload the page. Confirm the `dark` class is restored before first paint (no FOUC).
5. Toggle back to light. Confirm `localStorage.getItem('theme')` equals `"light"`.
6. Simulate system dark mode in DevTools. Confirm the app respects
   `prefers-color-scheme` when no `localStorage` entry is present.

### 7g — Final contrast check

```bash
python3 scripts/verify_contrast.py --quiet
```

Must exit `0`. If any pair fails after template installation (components may
introduce new foreground/background combinations), adjust the affected `@theme`
stop in `tokens.css` and re-run.

---

## Failure protocols

### Version conflict (peer deps)

Present the full conflict output clearly. Suggest the minimum downgrade that
resolves it (e.g. Tailwind v3 when a plugin has no v4 support yet). Ask for
confirmation before applying. Note: do not use `--legacy-peer-deps` or
`--force` without informing the user of the risk and receiving explicit approval.

### Tailwind v4 incompatibility

If `references/tailwind/per-framework-gotchas.md` marks the chosen combination
as v3-only, prompt the user before switching. After confirmation, re-run the
Tailwind setup section of Phase 3 with the v3 commands.

### Contrast failure

```bash
python3 scripts/verify_contrast.py --quiet
# Prints: FAIL  <label>  <ratio>:1 < <threshold>:1
```

For each failure, print the token pair and its ratio. Offer two options:

1. **Auto-adjust** — increase the lightness delta between the fg and bg stops
   in `tokens.css`, re-run `generate_palette.py`, and re-check.
2. **New preset** — let the user pick a different preset; re-run Phase 4 from 4a.

### Missing sibling skill

```
ui-ux-pro-max skill not found.
Falling back to references/ui-library/custom-tailwind.md.
```

Proceed automatically with the fallback implementations. Inform the user once —
do not block or repeat the warning on every component.

### Build error after install

Read the full error output. Identify the failing file and line. Fix the root
cause directly. Only ask the user to make a decision if the fix requires a
choice between two valid approaches (e.g. two incompatible type signatures).
Never ask the user to run commands themselves unless a privilege or environment
constraint makes it impossible to do so from the current context.

### Dev server port conflict

For Vite-based frameworks, add to `vite.config.ts`:

```ts
export default defineConfig({
  server: { port: 3001 },
});
```

For Next.js:

```bash
${PM} run dev -- --port 3001
```

For Nuxt:

```bash
${PM} run dev -- --port 3001
```
