# Tailwind CSS v4 — Setup Reference

## Table of contents

1. [What changed from v3](#1-what-changed-from-v3)
2. [Integration paths](#2-integration-paths)
3. [PostCSS path — Next.js and Nuxt](#3-postcss-path--nextjs-and-nuxt)
4. [Vite plugin path — React+Vite, Vue, SvelteKit](#4-vite-plugin-path--reactvite-vue-sveltekit)
5. [CSS entry-point](#5-css-entry-point)
6. [@theme block — CSS-first configuration](#6-theme-block--css-first-configuration)
7. [Color token integration](#7-color-token-integration)
8. [Dark mode strategy](#8-dark-mode-strategy)
9. [Utility class changes](#9-utility-class-changes)
10. [Verification](#10-verification)

---

## 1. What changed from v3

| Concern | v3 | v4 |
|---|---|---|
| Config file | `tailwind.config.js` / `.ts` | None — CSS `@theme` block instead |
| CSS entry | `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| PostCSS plugin | `tailwindcss` (direct) | `@tailwindcss/postcss` |
| Vite integration | PostCSS only | Dedicated `@tailwindcss/vite` plugin |
| Design tokens | `theme.extend` in JS config | CSS variables inside `@theme {}` |
| Dark mode class | `dark` + `darkMode: "class"` in config | `@variant dark (.dark &)` — automatic |
| Content scanning | `content: [...]` in config | Auto-detects all files under project root |
| Arbitrary values | `[value]` syntax | Same, plus CSS variable shorthand |

> **No `tailwind.config.js` in v4.** If you see one in a freshly scaffolded
> project (some scaffolders still generate it), delete it — it does nothing
> in v4 and causes confusion.

---

## 2. Integration paths

Pick the path that matches the framework's build system.

| Framework | Build system | Integration path |
|---|---|---|
| Next.js | Webpack / Turbopack (PostCSS) | PostCSS — `@tailwindcss/postcss` |
| Nuxt | Vite (default) or Webpack | Vite plugin — `@tailwindcss/vite` |
| React + Vite | Vite | Vite plugin — `@tailwindcss/vite` |
| Vue + Vite | Vite | Vite plugin — `@tailwindcss/vite` |
| SvelteKit | Vite | Vite plugin — `@tailwindcss/vite` |

> **Do not mix the two paths.** Using `@tailwindcss/postcss` in a Vite project
> causes double-processing. Using `@tailwindcss/vite` in a Next.js project is
> unsupported (Next.js does not expose the Vite config).

---

## 3. PostCSS path — Next.js and Nuxt

### Install

```bash
<package-manager> add -D tailwindcss@<resolved-version> @tailwindcss/postcss@<resolved-version> postcss@<resolved-version>
```

### postcss.config.mjs

Create or overwrite at the project root:

```js
/** @type {import('postcss').Config} */
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
```

> Do **not** list `autoprefixer` — v4's PostCSS plugin includes vendor-prefixing
> internally. Adding autoprefixer again produces duplicate prefixes.

### Remove old config (if scaffolder generated one)

```bash
rm -f tailwind.config.ts tailwind.config.js tailwind.config.cjs
```

---

## 4. Vite plugin path — React+Vite, Vue, SvelteKit

### Install

```bash
<package-manager> add -D tailwindcss@<resolved-version> @tailwindcss/vite@<resolved-version>
```

> No separate `postcss` package needed — the Vite plugin bypasses PostCSS
> entirely and processes Tailwind in Vite's transform pipeline.

### vite.config.ts

Add the plugin **before** the framework plugin:

**React + Vite**

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss(), react()],
});
```

**Vue**

```ts
import path from "node:path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss(), vue()],
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
});
```

**SvelteKit** (`vite.config.ts` at the project root)

```ts
import { defineConfig } from "vite";
import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss(), sveltekit()],
});
```

> Plugin order matters: `tailwindcss()` must be listed before the framework
> plugin so CSS is transformed before the framework's HMR layer processes it.

### Remove old config (if present)

```bash
rm -f tailwind.config.ts tailwind.config.js postcss.config.mjs postcss.config.js
```

---

## 5. CSS entry-point

Replace all `@tailwind` directives with a single import. The exact file differs
by framework:

| Framework | CSS entry file |
|---|---|
| Next.js | `src/app/globals.css` |
| React + Vite | `src/index.css` |
| Vue | `src/assets/main.css` |
| Nuxt | `assets/css/main.css` |
| SvelteKit | `src/app.css` |

Minimal content for the CSS entry file at scaffold time:

```css
@import "tailwindcss";
@import "./tokens.css";
```

> `tokens.css` holds the CSS variable definitions generated in Phase 4. Keep
> it as a separate import rather than inlining it so Phase 4 can overwrite it
> without touching the entry file.

> The `@import "tailwindcss"` single line replaces all three of the old v3
> directives (`@tailwind base`, `@tailwind components`, `@tailwind utilities`).
> Do not mix old and new directives — pick one style for the entire file.

---

## 6. @theme block — CSS-first configuration

All design tokens that were previously in `tailwind.config.js` under
`theme.extend` move into a `@theme` block in CSS.

### Syntax

```css
@import "tailwindcss";

@theme {
  --color-primary-50: oklch(97% 0.01 265);
  --color-primary-100: oklch(93% 0.03 265);
  /* ... 50–950 scale ... */
  --color-primary-500: oklch(55% 0.18 265);
  --color-primary-900: oklch(25% 0.08 265);
  --color-primary-950: oklch(15% 0.05 265);

  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;

  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
}
```

### Token naming convention

Tailwind v4 maps CSS variables to utility classes automatically using this
convention:

| CSS variable | Generated class |
|---|---|
| `--color-primary-500` | `text-primary-500`, `bg-primary-500`, `border-primary-500` |
| `--font-sans` | `font-sans` |
| `--radius-lg` | `rounded-lg` |
| `--spacing-4` | `p-4`, `m-4`, `gap-4`, etc. |

> Only variables declared inside `@theme {}` are scanned by Tailwind and
> turned into utilities. CSS variables declared in `:root {}` are accessible
> via `var(--name)` in arbitrary values but do **not** generate utilities.
> Put design tokens in `@theme`; put runtime theme values (dark-mode swaps)
> in `:root` and `.dark`.

### Keeping @theme in tokens.css

For this skill, the `@theme` block lives in `tokens.css` (generated in Phase 4)
rather than in the entry file. The entry file just `@import`s it:

```css
/* globals.css / index.css / app.css */
@import "tailwindcss";
@import "./tokens.css";
```

```css
/* tokens.css — generated by generate_palette.py */
@theme {
  --color-neutral-50: oklch(…);
  /* … full 50–950 neutral scale … */
  --color-accent-50: oklch(…);
  /* … full 50–950 accent scale … */
}

:root {
  --background: var(--color-neutral-50);
  --foreground: var(--color-neutral-950);
  --surface: var(--color-neutral-100);
  --border: var(--color-neutral-200);
  --primary: var(--color-accent-500);
  --primary-foreground: var(--color-neutral-50);
  --muted: var(--color-neutral-400);
}

.dark {
  --background: var(--color-neutral-950);
  --foreground: var(--color-neutral-50);
  --surface: var(--color-neutral-900);
  --border: var(--color-neutral-800);
  --primary: var(--color-accent-400);
  --primary-foreground: var(--color-neutral-950);
  --muted: var(--color-neutral-500);
}
```

---

## 7. Color token integration

Components consume semantic tokens via CSS variables, not raw scale values.
This ensures they automatically adapt when the theme switches.

### In component classes

```html
<!-- Correct: semantic token -->
<div class="bg-[var(--background)] text-[var(--foreground)]">…</div>

<!-- Also correct: expose semantics as @theme aliases -->
```

### Exposing semantic tokens as Tailwind utilities (recommended)

Add aliases in `@theme` pointing at the semantic variables so you get clean
class names:

```css
@theme {
  /* Palette scale tokens (from generate_palette.py) */
  --color-neutral-50: oklch(…);
  /* … */

  /* Semantic aliases — these become bg-background, text-foreground, etc. */
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-surface: var(--surface);
  --color-border: var(--border);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-muted: var(--muted);
}
```

Components then use:

```html
<div class="bg-background text-foreground border-border">…</div>
```

> `bg-background` expands to `background-color: var(--color-background)` which
> resolves to `var(--background)` which resolves to the active theme value.
> This two-level indirection is intentional — `@theme` variables are static
> compile-time aliases; `:root` / `.dark` variables are runtime-swappable.

---

## 8. Dark mode strategy

v4 does not require `darkMode: "class"` in a config file. Instead, use the
`.dark` class on `<html>` and the built-in `dark:` variant.

### How the variant works

```css
/* Tailwind's built-in dark variant targets .dark ancestors */
/* dark:bg-surface → background: var(--color-surface) when .dark is on <html> */
```

The ThemeProvider (in `assets/theme-provider/`) toggles `document.documentElement.classList`
between `""` and `"dark"`. No additional configuration is required.

### Inline usage

```html
<!-- Light: white background. Dark: dark surface. -->
<div class="bg-white dark:bg-surface">…</div>

<!-- Using semantic tokens (preferred — no dark: variant needed) -->
<div class="bg-background">…</div>
```

> Prefer semantic tokens over `dark:` variants wherever possible. Components
> written with `bg-background text-foreground` work in both themes with no
> extra classes — the CSS variable swap handles the transition.

---

## 9. Utility class changes

A few v3 classes were renamed or removed in v4. The most common:

| v3 class | v4 equivalent |
|---|---|
| `shadow-sm` / `shadow` | Unchanged |
| `ring-offset-*` | `ring-offset-*` — unchanged |
| `decoration-clone` | `box-decoration-clone` |
| `truncate` | `truncate` — unchanged |
| `overflow-ellipsis` | `text-ellipsis` |
| `flex-shrink-0` | `shrink-0` |
| `flex-grow` | `grow` |
| `transform` (bare) | No longer needed — transforms apply automatically |
| `filter` (bare) | No longer needed — filters apply automatically |
| `backdrop-filter` (bare) | No longer needed |

> If migrating from v3 source, run the official v4 upgrade tool:
> `npx @tailwindcss/upgrade@latest`. For fresh scaffolds, these are
> non-issues — just use the current class names from the start.

---

## 10. Verification

After completing setup, run the following to confirm Tailwind v4 is active:

```bash
# Start the dev server
<package-manager> dev
```

In the browser dev tools console:

```js
// Should print the resolved OKLCH value, not the variable name
getComputedStyle(document.documentElement).getPropertyValue("--color-neutral-500").trim()
```

In the Elements panel, inspect a utility-classed element (e.g. `class="bg-background"`).
Computed styles should show the resolved CSS variable value, not `initial`.

If Tailwind classes are not applied:

1. Confirm `@import "tailwindcss"` appears in the CSS entry file (not the old
   `@tailwind` directives).
2. Confirm the correct integration path for the framework (PostCSS vs Vite
   plugin) — see [Section 2](#2-integration-paths).
3. Confirm `tailwind.config.js` was deleted — its presence does not break v4
   but can mislead debugging.
4. For Vite projects: confirm `tailwindcss()` is listed in `plugins` before the
   framework plugin.
5. For PostCSS projects: confirm `postcss.config.mjs` lists
   `"@tailwindcss/postcss"` as the only plugin (remove `autoprefixer` and
   `tailwindcss` if they appear separately).
