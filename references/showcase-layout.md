# Showcase Layout

Specification for the `/library` showcase shell: route structure, Sidebar,
Header, component blocks, and the `CodeBlock` utility.

## Table of Contents

- [Route structure](#route-structure)
- [Layout scope](#layout-scope)
- [Sidebar](#sidebar)
- [Header](#header)
- [Library landing page](#library-landing-page)
- [Category page structure](#category-page-structure)
- [Component block pattern](#component-block-pattern)
- [CodeBlock utility](#codeblock-utility)
- [Framework routing maps](#framework-routing-maps)

---

## Route structure

| Route | Purpose |
|---|---|
| `/` | Immediate redirect → `/library` |
| `/library` | Landing: summary + quick-links to each category |
| `/library/inputs` | Button, Input, Textarea, Select, Checkbox, RadioGroup, Switch |
| `/library/display` | Card, Badge, Avatar, Separator, Skeleton, Table |
| `/library/feedback` | Alert, Toast, Progress, Tooltip, Dialog |
| `/library/navigation` | Tabs, Breadcrumb, Pagination, NavigationMenu |
| `/library/overlay` | Popover, DropdownMenu, Sheet |
| `/library/data-viz` | Chart, DataTable, Calendar |

The redirect at `/` must be a hard redirect (HTTP 307 or equivalent) so it
does not flash the Sidebar layout before navigating.

---

## Layout scope

The Sidebar + Header shell is applied **only to `/library` and all
`/library/*` routes**. The root `/` route must redirect before the layout
renders — never wrap it in the library layout.

```
/                  → redirect (no layout rendered)
/library           → LibraryLayout (Sidebar + Header + main)
/library/inputs    → LibraryLayout
/library/display   → LibraryLayout
…
```

---

## Sidebar

### Visual structure

```
┌──────────────────────┐
│  [Logo / App name]   │
├──────────────────────┤
│  Inputs              │  ← category heading (non-clickable label)
│    Button            │  ← anchor link to #button
│    Input             │
│    Textarea          │
│    Select            │
│    Checkbox          │
│    RadioGroup        │
│    Switch            │
├──────────────────────┤
│  Display             │
│    Card              │
│    Badge             │
│    …                 │
├──────────────────────┤
│  Feedback            │
│    …                 │
├──────────────────────┤
│  Navigation          │
│    …                 │
├──────────────────────┤
│  Overlay             │
│    …                 │
├──────────────────────┤
│  Data viz            │
│    …                 │
└──────────────────────┘
```

### Behaviour

- **Active route:** the current category's heading is highlighted
  (`text-primary font-semibold`).
- **Active anchor:** the currently visible component's sidebar link is
  highlighted using an IntersectionObserver on each component section heading.
- **Component links** are `#<component-slug>` anchor links within the current
  route, not separate pages.
- **Category links** navigate to `/library/<category>`.
- **Collapsed on mobile:** sidebar is hidden off-screen (translate-x) and
  toggled by a hamburger button in the Header. Overlay backdrop closes it.
- **Width:** `w-64` (256 px) fixed on desktop. Full-width slide-in on mobile.

### Sidebar nav data

```ts
const NAV_ITEMS = [
  {
    category: "Inputs",
    slug: "inputs",
    components: ["Button", "Input", "Textarea", "Select", "Checkbox", "RadioGroup", "Switch"],
  },
  {
    category: "Display",
    slug: "display",
    components: ["Card", "Badge", "Avatar", "Separator", "Skeleton", "Table"],
  },
  {
    category: "Feedback",
    slug: "feedback",
    components: ["Alert", "Toast", "Progress", "Tooltip", "Dialog"],
  },
  {
    category: "Navigation",
    slug: "navigation",
    components: ["Tabs", "Breadcrumb", "Pagination", "NavigationMenu"],
  },
  {
    category: "Overlay",
    slug: "overlay",
    components: ["Popover", "DropdownMenu", "Sheet"],
  },
  {
    category: "Data viz",
    slug: "data-viz",
    components: ["Chart", "DataTable", "Calendar"],
  },
];
```

Component slugs used in anchor IDs are kebab-case: `NavigationMenu` →
`#navigation-menu`, `RadioGroup` → `#radio-group`, `DropdownMenu` →
`#dropdown-menu`, `DataTable` → `#data-table`. All others are lowercase of the
name.

---

## Header

### Visual structure

```
┌──────────────────────────────────────────────────────────────────┐
│  ☰  (mobile only)   Component Library         ○ GitHub   ◑ Theme │
└──────────────────────────────────────────────────────────────────┘
```

### Elements

| Element | Notes |
|---|---|
| Hamburger icon | Mobile only (`md:hidden`), toggles sidebar |
| App name | `"Component Library"` — plain text, links to `/library` |
| GitHub link | `<a href="#">` placeholder, opens in `_blank`, icon + label |
| Theme toggle | Icon button: sun/moon, calls `toggleTheme()` from theme provider |

### Sticky behaviour

Header is `sticky top-0 z-40`. The main content area has `pt-16` (header height).

---

## Library landing page

Route: `/library`

Renders inside the LibraryLayout (Sidebar + Header visible). Content:

1. **Hero heading:** `"Component Library"` with a one-line description:
   *"28 components across 6 categories — themed, accessible, ready to use."*
2. **Category grid:** 2-column (desktop) / 1-column (mobile) grid of cards,
   one per category. Each card shows the category name, component count, and
   links to `/library/<category>`.
3. No component examples on this page — it is purely navigational.

---

## Category page structure

Each category route renders a vertical list of component sections. Example
for `/library/inputs`:

```
<main>
  <h1>Inputs</h1>
  <p>Brief category description (1 sentence).</p>

  <section id="button">
    <h2>Button</h2>
    <p>Component description (1–2 sentences).</p>
    <!-- Live example -->
    <div class="component-preview">…</div>
    <!-- Collapsible code snippet -->
    <CodeBlock code={buttonExampleCode} language="tsx" filename="Button.tsx" collapsible />
  </section>

  <section id="input">…</section>
  …
</main>
```

### Spacing conventions

- `gap-16` (`64px`) between component sections.
- `gap-4` (`16px`) between heading, description, preview, and code block within
  a section.
- Preview area: `rounded-lg border border-border bg-card p-8` — centered,
  generous padding.

---

## Component block pattern

Each component section follows this template regardless of framework:

```
<section id="{component-slug}">
  <h2>{Component Name}</h2>
  <p>{One or two sentence description}</p>

  <!-- Preview: centered, card-style wrapper -->
  <div class="preview-wrapper">
    {rendered live example}
  </div>

  <!-- Code snippet: collapsible, shows the minimal usage example -->
  <CodeBlock
    code="{minimal usage code}"
    language="{tsx|vue|svelte}"
    filename="{ComponentName}.{tsx|vue|svelte}"
    collapsible
    defaultOpen={false}
  />
</section>
```

The **minimal usage example** is the simplest meaningful use of the component
— typically 5–15 lines. It must be self-contained (imports included) and
match exactly what renders in the preview.

---

## CodeBlock utility

`CodeBlock` is a 29th utility component, installed with the 28 showcase
components but **not exported as a user-facing component**. It lives at:

- React/Next.js: `src/components/ui/code-block.tsx`
- Vue/Nuxt: `src/components/ui/CodeBlock.vue`
- SvelteKit: `src/lib/components/ui/CodeBlock.svelte`

### Behaviour

- Renders `<pre><code>` with monospace font and `bg-muted` background.
- **Collapsible:** when `collapsible={true}` and `defaultOpen={false}`, the
  block renders collapsed with a *"Show code"* toggle button. Clicking expands
  it. Button label flips to *"Hide code"*.
- **Copy button:** top-right corner. Copies `code` to clipboard via
  `navigator.clipboard.writeText`. Icon switches from clipboard → check for
  2 seconds on success.
- **Filename chip:** if `filename` is provided, render it as a small label
  above the code block (`text-xs text-muted-foreground font-mono`).
- **Syntax highlighting:** no external library — use CSS classes applied via
  regex or simple token detection for keywords. Keep it zero-dependency.
  Alternatively, accept pre-highlighted HTML via a `highlightedCode` prop and
  render it with `dangerouslySetInnerHTML` / `v-html` / `{@html}` only when
  explicitly provided (never auto-parse).

### Props (all frameworks)

```ts
interface CodeBlockProps {
  code: string;
  language?: string;
  filename?: string;
  collapsible?: boolean;
  defaultOpen?: boolean;
  highlightedCode?: string; // pre-highlighted HTML — use with caution
  className?: string;
}
```

### Accessibility

- `<pre>` has `role="region"` and `aria-label="Code snippet"` (or
  `aria-label="{filename} code snippet"` when filename is provided).
- Copy button: `aria-label="Copy code"` → `"Copied!"` on success, resets after
  2 seconds.
- Collapse toggle: `aria-expanded={isOpen}`, `aria-controls` pointing to the
  pre element's id.

---

## Framework routing maps

### Next.js (App Router)

```
app/
  page.tsx                  → redirect to /library
  library/
    layout.tsx              → LibraryLayout (Sidebar + Header)
    page.tsx                → landing page
    inputs/page.tsx
    display/page.tsx
    feedback/page.tsx
    navigation/page.tsx
    overlay/page.tsx
    data-viz/page.tsx
```

Redirect at `app/page.tsx`:

```ts
import { redirect } from "next/navigation";
export default function Home() { redirect("/library"); }
```

### React + Vite (React Router v7)

```
src/
  App.tsx                   → <Route path="/" element={<Navigate to="/library" replace />} />
  routes/
    library/
      _layout.tsx           → LibraryLayout
      index.tsx             → landing page
      inputs.tsx
      display.tsx
      feedback.tsx
      navigation.tsx
      overlay.tsx
      data-viz.tsx
```

### Vue + Nuxt (Nuxt 4)

```
app/
  pages/
    index.vue               → definePageMeta redirect or <NuxtRouteAnnouncer />
    library/
      index.vue             → landing page
      inputs.vue
      display.vue
      feedback.vue
      navigation.vue
      overlay.vue
      data-viz.vue
  layouts/
    library.vue             → LibraryLayout (Sidebar + Header)
```

`index.vue` redirect:

```vue
<script setup>
navigateTo("/library", { replace: true });
</script>
```

### Vue + Vite (Vue Router)

```
src/
  router/index.ts           → { path: "/", redirect: "/library" }
  views/
    library/
      LibraryLayout.vue
      LibraryHome.vue
      InputsView.vue
      DisplayView.vue
      FeedbackView.vue
      NavigationView.vue
      OverlayView.vue
      DataVizView.vue
```

### SvelteKit

```
src/routes/
  +page.svelte              → <script>import { redirect } from "@sveltejs/kit"; throw redirect(307, "/library");</script>
  library/
    +layout.svelte          → LibraryLayout (Sidebar + Header)
    +page.svelte            → landing page
    inputs/+page.svelte
    display/+page.svelte
    feedback/+page.svelte
    navigation/+page.svelte
    overlay/+page.svelte
    data-viz/+page.svelte
```

SvelteKit redirect in `src/routes/+page.server.ts`:

```ts
import { redirect } from "@sveltejs/kit";
export function load() { throw redirect(307, "/library"); }
```
