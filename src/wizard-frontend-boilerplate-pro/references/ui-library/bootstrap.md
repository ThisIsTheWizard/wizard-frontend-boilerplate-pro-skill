# Bootstrap 5.3 Integration Reference

## Overview

Bootstrap is a CSS framework providing utility classes, pre-built component styles, and optional JavaScript plugins. Unlike MUI or shadcn, Bootstrap works across React (`react-bootstrap`), Vue (`bootstrap-vue-next`), and Svelte (`@sveltestrap/sveltestrap` or Bootstrap CSS + JS directly). All three frameworks share the same underlying Bootstrap CSS, making Bootstrap the most framework-agnostic option in the skill's library roster.

Bootstrap's design tokens are SCSS variables compiled at build time, while the skill's token system uses CSS custom properties at runtime. A two-layer bridge is required: SCSS overrides for build-time color values, and CSS variable overrides for runtime dark mode sync.

---

## Install

### React / Vite (`react-bootstrap`)

```bash
npm install react-bootstrap bootstrap
```

Import CSS in `src/main.tsx`:

```ts
import "bootstrap/dist/css/bootstrap.min.css";
```

### Next.js 15 (App Router)

```bash
npm install react-bootstrap bootstrap
```

Import CSS in `app/globals.css`:

```css
@import "bootstrap/dist/css/bootstrap.min.css";
```

> No special SSR adapter is needed. `react-bootstrap` components are all client-side rendered. Add `"use client"` to any file that uses interactive Bootstrap components (modals, dropdowns, toasts) to satisfy the App Router boundary.

### Vue 3 (`bootstrap-vue-next`)

```bash
npm install bootstrap bootstrap-vue-next
```

In `src/main.ts`:

```ts
import "bootstrap/dist/css/bootstrap.min.css";
import { createBootstrap } from "bootstrap-vue-next";
import { createApp } from "vue";
import App from "./App.vue";

const app = createApp(App);
app.use(createBootstrap());
app.mount("#app");
```

### Svelte / SvelteKit (`@sveltestrap/sveltestrap`)

```bash
npm install bootstrap @sveltestrap/sveltestrap
```

Import CSS in the root layout (`src/routes/+layout.svelte`):

```ts
import "bootstrap/dist/css/bootstrap.min.css";
```

Import `@sveltestrap/sveltestrap` components directly in any `.svelte` file:

```ts
import { Button, Card, Alert } from "@sveltestrap/sveltestrap";
```

---

## CDN alternative (prototyping only)

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
/>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

> Use CDN only for quick prototyping. For skill-generated projects, always install via npm so the SCSS bridge can be applied.

---

## Theming bridge — SCSS variable overrides

Bootstrap's design tokens are SCSS variables compiled at build time. The skill's tokens are CSS custom properties resolved at runtime. The bridge strategy has two layers.

### Layer 1 — SCSS (build-time)

Create `src/styles/_bootstrap-overrides.scss` and import it in place of `bootstrap/dist/css/bootstrap.min.css`:

```scss
// Static values matching your chosen color preset — update when switching presets.
$primary:          #4f46e5; // matches --color-accent-500 at build time
$danger:           #ef4444; // matches --destructive
$border-radius:    0.5rem;
$border-radius-sm: 0.375rem;
$border-radius-lg: 0.75rem;

@import "bootstrap/scss/bootstrap";
```

Update `$primary` to match the active color preset whenever the project preset changes.

Install the SCSS preprocessor if not already present:

```bash
npm install -D sass
```

Then replace the `.min.css` import in `main.tsx` / `main.ts` / `+layout.svelte` with the override file:

```ts
import "@/styles/_bootstrap-overrides.scss";
```

### Layer 2 — CSS custom properties (runtime dark mode)

Bootstrap 5.3 exposes its own CSS variables (`--bs-primary`, `--bs-body-bg`, etc.). Override them in the project's root CSS (after the Bootstrap import) to stay in sync with the skill's token system at runtime:

```css
:root {
  --bs-primary:      var(--color-accent-500);
  --bs-border-color: var(--border);
  --bs-body-bg:      var(--background);
  --bs-body-color:   var(--foreground);
  --bs-secondary-bg: var(--surface);
  --bs-tertiary-bg:  var(--muted);
}
```

---

## Token mapping table

| Skill CSS token | Bootstrap SCSS var | Bootstrap CSS var |
|---|---|---|
| `--color-accent-500` | `$primary` | `--bs-primary` |
| `--background` | `$body-bg` | `--bs-body-bg` |
| `--foreground` | `$body-color` | `--bs-body-color` |
| `--surface` | `$card-bg` | `--bs-secondary-bg` |
| `--border` | `$border-color` | `--bs-border-color` |
| `--destructive` | `$danger` | `--bs-danger` |
| `--radius` | `$border-radius` | `--bs-border-radius` |
| `--muted` | `$secondary-bg` | `--bs-tertiary-bg` |

---

## Dark mode

Bootstrap 5.3 ships built-in dark mode activated by setting `data-bs-theme="dark"` on the `<html>` element. Bridge the skill's theme system by watching the `useTheme()` value and syncing it to that attribute.

### React

```tsx
import { useEffect } from "react";
import { useTheme } from "@/components/ThemeProvider";

export function BootstrapThemeBridge() {
  const { theme } = useTheme();

  useEffect(() => {
    document.documentElement.setAttribute("data-bs-theme", theme);
  }, [theme]);

  return null;
}
```

Place `<BootstrapThemeBridge />` inside the skill's `ThemeProvider` in the root layout so it runs before any Bootstrap component renders.

### Vue

```ts
import { watch } from "vue";
import { useTheme } from "@/composables/useTheme";

const { theme } = useTheme();

watch(
  theme,
  (val) => {
    document.documentElement.setAttribute("data-bs-theme", val);
  },
  { immediate: true },
);
```

Add this block to the root `App.vue` `<script setup>` section.

### Svelte

```ts
import { useTheme } from "$lib/composables/useTheme";

const { theme } = useTheme();

$effect(() => {
  document.documentElement.setAttribute("data-bs-theme", theme);
});
```

Add this block to `src/routes/+layout.svelte` `<script>`.

---

## Tailwind coexistence

Bootstrap's global resets and Tailwind's `preflight` both zero out browser defaults and can conflict when both are active. Two strategies:

1. **Disable Tailwind preflight** (recommended when Bootstrap is primary): In `tailwind.config.ts`, set `corePlugins: { preflight: false }`. Bootstrap's own Reboot handles the reset.
2. **Scope Bootstrap** (when Tailwind is primary): Import only Bootstrap's component CSS instead of the full bundle. Use `bootstrap/scss/utilities` for Bootstrap utilities only, and exclude Bootstrap's reboot.

For skill-generated showcase templates, Bootstrap is the primary UI library — disable Tailwind preflight.

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{ts,tsx,vue,svelte}"],
  corePlugins: {
    preflight: false,
  },
} satisfies Config;
```

---

## Component coverage map

| Skill slot | Bootstrap equivalent | React package | Vue package | Svelte package |
|---|---|---|---|---|
| Button | `Button` | `react-bootstrap` | `BButton` (bootstrap-vue-next) | `Button` (@sveltestrap) |
| Input | `Form.Control` | `react-bootstrap` | `BFormInput` | `Input` |
| Textarea | `Form.Control as="textarea"` | `react-bootstrap` | `BFormTextarea` | `Input type="textarea"` |
| Select | `Form.Select` | `react-bootstrap` | `BFormSelect` | `Input type="select"` |
| Checkbox | `Form.Check type="checkbox"` | `react-bootstrap` | `BFormCheckbox` | `Input type="checkbox"` |
| RadioGroup | `Form.Check type="radio"` | `react-bootstrap` | `BFormRadioGroup` | `Input type="radio"` |
| Switch | `Form.Check type="switch"` | `react-bootstrap` | `BFormCheckbox switch` | `Input type="switch"` |
| Card | `Card` sub-components | `react-bootstrap` | `BCard` | `Card` |
| Badge | `Badge` | `react-bootstrap` | `BBadge` | `Badge` |
| Avatar | Custom `div` with Bootstrap classes | — | — | — |
| Separator | `<hr>` / `.vr` | native HTML | native HTML | native HTML |
| Skeleton | `Placeholder` | `react-bootstrap` | `BPlaceholder` | custom CSS |
| Table | `Table` | `react-bootstrap` | `BTable` | `Table` |
| Alert | `Alert` | `react-bootstrap` | `BAlert` | `Alert` |
| Toast | `Toast` + `ToastContainer` | `react-bootstrap` | `BToast` | `Toast` |
| Progress | `ProgressBar` | `react-bootstrap` | `BProgress` | `Progress` |
| Tooltip | `OverlayTrigger` + `Tooltip` | `react-bootstrap` | `BTooltip` | `Tooltip` |
| Dialog | `Modal` sub-components | `react-bootstrap` | `BModal` | `Modal` |
| Tabs | `Tab.Container` + `Nav` + `Tab.Content` | `react-bootstrap` | `BTabs` + `BTab` | `TabContent` + `TabPane` |
| Breadcrumb | `Breadcrumb` + `Breadcrumb.Item` | `react-bootstrap` | `BBreadcrumb` | `Breadcrumb` |
| Pagination | `Pagination` sub-components | `react-bootstrap` | `BPagination` | `Pagination` |
| NavigationMenu | `Navbar` + `Nav` | `react-bootstrap` | `BNavbar` | `Navbar` |
| Popover | `OverlayTrigger` + `Popover` | `react-bootstrap` | `BPopover` | `Popover` |
| DropdownMenu | `Dropdown` sub-components | `react-bootstrap` | `BDropdown` | `Dropdown` |
| Sheet | `Offcanvas` sub-components | `react-bootstrap` | `BOffcanvas` | `Offcanvas` |
| Chart | recharts directly | `recharts` | `recharts` | `recharts` |
| DataTable | `Table` + sortable logic | `react-bootstrap` | `BTable` | `Table` |
| Calendar | `react-day-picker` | `react-day-picker` | custom or `v-calendar` | `v-calendar` / custom |

---

## No-Tailwind note for component content

Bootstrap manages its own component styling. Tailwind utility classes are not applied to Bootstrap components directly. Use Bootstrap utility classes (`d-flex`, `gap-2`, `p-4`, `mb-3`, `text-muted`, etc.) inside component templates, and reserve Tailwind for project-level layout wrappers only when preflight is disabled.

---

## Graceful fallback

If Bootstrap installation fails (network issues, peer dependency conflicts), fall back to `references/ui-library/custom-tailwind.md`. The `/library` route structure and sidebar navigation remain unchanged.
