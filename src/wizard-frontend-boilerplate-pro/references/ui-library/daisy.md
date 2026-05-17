# DaisyUI v5 Integration Reference

## Overview

DaisyUI is a Tailwind CSS plugin providing 50+ semantic component class names. It works across React, Vue, and Svelte without a per-framework wrapper package — all styling is pure CSS applied via HTML class attributes such as `btn btn-primary`, `card`, `badge badge-success`. There is no JavaScript runtime and no component import needed from a DaisyUI package.

DaisyUI v5 requires Tailwind v4. Because components are plain HTML + class strings, DaisyUI is the most framework-agnostic choice in the skill's library roster — the same markup pattern works verbatim in `.tsx`, `.vue`, and `.svelte` files.

## Install

### Tailwind v4 projects (all frameworks)

```bash
npm install -D daisyui@latest
```

Then in the project CSS entry file (`globals.css` / `app.css`):

```css
@import "tailwindcss";
@import "daisyui";
```

No `tailwind.config.js` change is needed for Tailwind v4 — `@import "daisyui"` registers the plugin automatically via the CSS layer system.

### Tailwind v3 fallback

```bash
npm install -D daisyui@4   # DaisyUI v4 supports Tailwind v3
```

In `tailwind.config.ts`:

```ts
import daisyui from "daisyui";

export default {
  plugins: [daisyui],
};
```

## Theming bridge

DaisyUI v5 theming is handled by setting `data-theme` on the `<html>` element and by custom CSS variable overrides.

### Built-in themes

DaisyUI ships `light` and `dark` themes by default. Apply them at runtime:

```js
document.documentElement.setAttribute("data-theme", "light" /* or "dark" */);
```

### Custom theme — CSS variable bridge

Create a custom DaisyUI theme that maps to the skill's token system. Add this block in `globals.css` / `app.css` after `@import "daisyui"`:

```css
[data-theme="custom"] {
  --color-primary: var(--color-accent-500);
  --color-primary-content: #ffffff;
  --color-secondary: var(--color-accent-700);
  --color-secondary-content: #ffffff;
  --color-accent: var(--color-accent-400);
  --color-neutral: var(--muted);
  --color-base-100: var(--background);
  --color-base-200: var(--surface);
  --color-base-300: var(--muted);
  --color-base-content: var(--foreground);
  --color-error: var(--destructive);
  --radius-btn: var(--radius);
  --radius-box: var(--radius);
}
```

Use `data-theme="custom"` to activate the skill's palette, or use `"light"` / `"dark"` for DaisyUI's default themes.

### Dark mode integration

Bridge the skill's theme system to DaisyUI's `data-theme` attribute. Watch the skill's `useTheme()` value and sync:

**React:**
```tsx
useEffect(() => {
  document.documentElement.setAttribute("data-theme", theme);
}, [theme]);
```

**Vue:**
```ts
watch(theme, (val) => {
  document.documentElement.setAttribute("data-theme", val);
}, { immediate: true });
```

**Svelte:**
```ts
$effect(() => {
  document.documentElement.setAttribute("data-theme", theme);
});
```

## Token mapping table

| Skill CSS token        | DaisyUI CSS variable        |
|------------------------|-----------------------------|
| `--color-accent-500`   | `--color-primary`           |
| `--color-accent-700`   | `--color-secondary`         |
| `--background`         | `--color-base-100`          |
| `--surface`            | `--color-base-200`          |
| `--muted`              | `--color-base-300`          |
| `--foreground`         | `--color-base-content`      |
| `--destructive`        | `--color-error`             |
| `--radius`             | `--radius-btn`, `--radius-box` |
| `--border`             | (use `border-base-300` class) |

## Tailwind coexistence

DaisyUI and Tailwind utility classes work together by design — DaisyUI IS a Tailwind plugin. No extra configuration is needed. You can freely combine Tailwind utilities (`flex`, `gap-4`, `p-4`, `text-sm`, etc.) alongside DaisyUI component classes (`btn`, `card`, `badge`).

There is no preflight conflict since DaisyUI uses the same Tailwind preflight.

## Component coverage map

| Skill slot       | DaisyUI approach                                            |
|------------------|-------------------------------------------------------------|
| Button           | `<button class="btn btn-primary">`                          |
| Input            | `<input class="input input-bordered w-full">`               |
| Textarea         | `<textarea class="textarea textarea-bordered w-full">`      |
| Select           | `<select class="select select-bordered w-full">`            |
| Checkbox         | `<input type="checkbox" class="checkbox">`                  |
| RadioGroup       | `<input type="radio" class="radio">` (grouped by `name`)   |
| Switch/Toggle    | `<input type="checkbox" class="toggle">`                    |
| Card             | `<div class="card bg-base-100 shadow-sm">`                  |
| Badge            | `<span class="badge badge-primary">`                        |
| Avatar           | `<div class="avatar placeholder">`                          |
| Separator        | `<div class="divider">` or `divider-horizontal`             |
| Skeleton         | `<div class="skeleton h-4 w-full">`                         |
| Table            | `<table class="table table-zebra">`                         |
| Alert            | `<div role="alert" class="alert alert-info">`               |
| Toast            | `<div class="toast toast-end">` + alert inside              |
| Progress         | `<progress class="progress progress-primary">`              |
| Tooltip          | `<div class="tooltip" data-tip="…">`                        |
| Dialog/Modal     | `<dialog class="modal">` + `showModal()`                    |
| Tabs             | `<div role="tablist" class="tabs tabs-bordered">`           |
| Breadcrumbs      | `<div class="breadcrumbs"><ul>…</ul></div>`                 |
| Pagination       | `<div class="join">` with `join-item btn`                   |
| NavigationMenu   | `navbar` + `menu menu-horizontal`                           |
| Popover          | `tooltip` (CSS-only); for rich content: `dropdown`          |
| DropdownMenu     | `<div class="dropdown dropdown-end">`                       |
| Sheet/Drawer     | `<div class="drawer">`                                      |
| Chart            | recharts (DaisyUI provides no chart primitive)              |
| DataTable        | `table` + manual sort logic                                 |
| Calendar         | react-day-picker / custom (no DaisyUI primitive)            |

## No third-party package note

DaisyUI itself is the only additional dependency beyond Tailwind CSS. Components are written in plain HTML markup with DaisyUI class names — no import statements for individual components are needed. This makes DaisyUI templates the most portable across frameworks and the easiest to copy-paste between them.

## Graceful fallback

If DaisyUI installation fails or conflicts arise, fall back to `references/ui-library/custom-tailwind.md`. The `/library` route structure and sidebar navigation remain unchanged — only the component class names differ.
