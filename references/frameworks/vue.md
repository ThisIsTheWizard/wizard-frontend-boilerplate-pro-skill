# Vue 3.5+ — Scaffold Reference

## Table of contents

1. [Package list for version resolution](#1-package-list-for-version-resolution)
2. [Scaffold command](#2-scaffold-command)
3. [CLI flag matrix](#3-cli-flag-matrix)
4. [Post-scaffold cleanup](#4-post-scaffold-cleanup)
5. [Router setup](#5-router-setup)
6. [Tailwind integration](#6-tailwind-integration)
7. [Expected directory structure](#7-expected-directory-structure)
8. [tsconfig adjustments](#8-tsconfig-adjustments)
9. [Verification](#9-verification)

---

## 1. Package list for version resolution

Pass these names to `scripts/check_versions.sh` during Phase 2.

**Core**

| Package | Registry name |
|---|---|
| Vue | `vue` |
| create-vue (scaffolder) | `create-vue` |
| Vue Router | `vue-router` |
| TypeScript | `typescript` |
| Vite | `vite` |
| `@vitejs/plugin-vue` | `@vitejs/plugin-vue` |
| `vue-tsc` | `vue-tsc` |

**Tailwind v4 (default)**

| Package | Registry name |
|---|---|
| Tailwind CSS | `tailwindcss` |
| Vite plugin | `@tailwindcss/vite` |

**Tailwind v3 (fallback — only if user chose v3)**

| Package | Registry name |
|---|---|
| Tailwind CSS | `tailwindcss` (v3 tag: `tailwindcss@3`) |
| PostCSS | `postcss` |
| Autoprefixer | `autoprefixer` |

> Gotchas: see `references/tailwind/per-framework-gotchas.md`. Tailwind v4
> ships a first-class Vite plugin (`@tailwindcss/vite`) — the same plugin used
> for React+Vite. Do not mix `@tailwindcss/postcss` with the Vite plugin.

---

## 2. Scaffold command

Use `create-vue` — the official Vue scaffolding tool — with explicit flags so
the scaffold is non-interactive and reproducible in headless environments.

**TypeScript project (default)**

```bash
npm create vue@latest <project-name> -- \
  --typescript \
  --router \
  --eslint \
  --prettier
```

**JavaScript project**

```bash
npm create vue@latest <project-name> -- \
  --router \
  --eslint \
  --prettier
```

> `create-vue` does not accept a version pin for the _generated_ Vue app — it
> always installs the latest stable `vue` package. To pin to a specific Vue
> version, run the scaffold first, then update `package.json` manually and
> reinstall.

> `--router` installs Vue Router 4 and generates the `src/router/index.ts`
> stub. Always include it — the showcase routes depend on it.

> Do not pass `--pinia` or `--vitest` unless the user explicitly requests them;
> neither is required by the boilerplate showcase.

> pnpm / yarn / bun syntax:

```bash
# pnpm
pnpm create vue@latest <project-name> -- --typescript --router --eslint --prettier

# yarn
yarn create vue@latest <project-name> --typescript --router --eslint --prettier

# bun
bun create vue@latest <project-name> -- --typescript --router --eslint --prettier
```

---

## 3. CLI flag matrix

| User choice | Flag(s) to pass |
|---|---|
| TypeScript | `--typescript` (default) |
| JavaScript | _(omit `--typescript`)_ |
| Vue Router | `--router` (always include) |
| ESLint | `--eslint` (always include) |
| Prettier | `--prettier` (always include) |

> `create-vue` generates `eslint.config.js` and `.prettierrc.json` when both
> flags are passed. Phase 3 relies on these files existing; do not skip them.

---

## 4. Post-scaffold cleanup

After `create-vue` exits, install dependencies, then remove the demo content
that ships with every fresh scaffold.

```bash
cd <project-name>

# Install base deps first
<package-manager> install

# Remove demo views and components
rm -f src/views/AboutView.vue
rm -f src/views/HomeView.vue        # replaced by showcase home view
rm -rf src/components/HelloWorld.vue
rm -rf src/components/TheWelcome.vue
rm -rf src/components/WelcomeItem.vue
rm -rf src/components/icons/

# Remove default demo assets
rm -f src/assets/base.css
rm -f src/assets/main.css
rm -f src/assets/logo.svg

# Create directory layout expected by showcase templates
mkdir -p src/components/ui
mkdir -p src/views
mkdir -p src/styles
mkdir -p src/lib
```

Create the global stylesheet that imports tokens (written in Phase 4):

```bash
cat > src/globals.css << 'EOF'
@import "./styles/tokens.css";

*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  -webkit-font-smoothing: antialiased;
}
EOF
```

Update `src/main.ts` (or `src/main.js`) to import the global stylesheet instead
of the old `assets/main.css`:

```ts
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./globals.css";

const app = createApp(App);
app.use(router);
app.mount("#app");
```

Replace `src/App.vue` with a minimal shell that delegates layout to the
showcase root component (installed in Phase 6):

```vue
<script setup lang="ts">
import AppLayout from "@/components/AppLayout.vue";
</script>

<template>
  <AppLayout />
</template>
```

---

## 5. Router setup

`create-vue --router` generates `src/router/index.ts` with two placeholder
routes. Replace the entire file with the showcase routes. `/` redirects to
`/library` and all showcase pages are nested under `/library`:

```ts
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/library",
    },
    {
      path: "/library",
      component: () => import("@/views/LibraryHomeView.vue"),
    },
    {
      path: "/library/inputs",
      component: () => import("@/views/InputsView.vue"),
    },
    {
      path: "/library/display",
      component: () => import("@/views/DisplayView.vue"),
    },
    {
      path: "/library/feedback",
      component: () => import("@/views/FeedbackView.vue"),
    },
    {
      path: "/library/navigation",
      component: () => import("@/views/NavigationView.vue"),
    },
    {
      path: "/library/overlay",
      component: () => import("@/views/OverlayView.vue"),
    },
    {
      path: "/library/data-viz",
      component: () => import("@/views/DataVizView.vue"),
    },
  ],
});

export default router;
```

All routes use dynamic imports so Vue can code-split each category page. The
`AppLayout.vue` component (installed in Phase 6) wraps `<RouterView />` with
the persistent Sidebar and Header — it renders for every route including
`/library` because it lives in `App.vue`. The actual view files are installed
from `assets/showcase-templates/vue/` in Phase 6.

---

## 6. Tailwind integration

### v4 (default)

Install the Vite plugin:

```bash
<package-manager> add -D tailwindcss@<resolved-version> @tailwindcss/vite@<resolved-version>
```

Update `vite.config.ts`:

```ts
import path from "node:path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

> `create-vue` already adds the `@/` alias via `vite.config.ts`; confirm it is
> present and uses `path.resolve` — do not rely on the string shorthand
> `"@": "./src"` as it breaks in some environments.

Add the v4 import at the top of `src/globals.css`:

```css
@import "tailwindcss";
@import "./styles/tokens.css";
```

No `tailwind.config.ts` is needed for v4.

Full v4 setup: `references/tailwind/v4-setup.md`.

### v3 (fallback)

Install via PostCSS:

```bash
<package-manager> add -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
```

Update `tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: { extend: {} },
  plugins: [],
};
```

> The `content` glob must include `.vue` files — Tailwind v3 does not scan
> them by default.

Replace the globals.css imports with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
@import "./styles/tokens.css";
```

Full v3 setup: `references/tailwind/v3-setup.md`.

---

## 7. Expected directory structure

After scaffold + cleanup + Phase 4 setup:

```
<project-name>/
├── public/
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── ui/                  # 28 components — Phase 5
│   │   │   └── ...
│   │   ├── CodeBlock.vue        # Phase 5c utility
│   │   ├── AppLayout.vue        # wraps Sidebar + Header + RouterView
│   │   ├── Sidebar.vue          # Phase 6
│   │   └── Header.vue           # Phase 6
│   ├── views/
│   │   ├── LibraryHomeView.vue  # /library landing
│   │   ├── InputsView.vue       # /library/inputs
│   │   ├── DisplayView.vue      # /library/display
│   │   ├── FeedbackView.vue     # /library/feedback
│   │   ├── NavigationView.vue   # /library/navigation
│   │   ├── OverlayView.vue      # /library/overlay
│   │   └── DataVizView.vue      # /library/data-viz
│   ├── router/
│   │   └── index.ts
│   ├── styles/
│   │   └── tokens.css           # Phase 4
│   ├── lib/
│   │   └── utils.ts             # cn() helper
│   ├── globals.css
│   ├── App.vue
│   └── main.ts
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tsconfig.app.json            # TS projects only
├── tsconfig.node.json           # TS projects only
├── eslint.config.js
├── .prettierrc.json
└── package.json
```

---

## 8. tsconfig adjustments

`create-vue` with `--typescript` generates three tsconfig files:

- `tsconfig.json` — references the two below
- `tsconfig.app.json` — compilation settings for `src/`
- `tsconfig.node.json` — compilation settings for `vite.config.ts`

Apply stricter settings to `tsconfig.app.json`:

```json
{
  "extends": "@vue/tsconfig/tsconfig.dom.json",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*", "src/**/*.vue"],
  "exclude": ["src/**/__tests__/*"]
}
```

- `noUncheckedIndexedAccess` prevents silent `undefined` bugs when indexing
  arrays in the showcase's data-driven component lists.
- The `paths` alias must match the alias in `vite.config.ts`; `create-vue`
  sets this in both files — verify before continuing.

> Vue 3.5+ ships improved TypeScript support for generic components and
> `defineModel()`. Use `vue-tsc` (the type-checker for `.vue` files, installed
> by `create-vue --typescript`) instead of plain `tsc`.

---

## 9. Verification

Before advancing to Phase 4:

```bash
# TypeScript check (TS projects only)
npx vue-tsc --noEmit

# Dev server smoke test
<package-manager> run dev
```

Expected output:
- `vue-tsc --noEmit` exits 0 with no errors.
- Vite reports `Local: http://localhost:5173/` (default Vite port).
- Browser shows a blank page — the demo content was removed in step 4.

> Vue + Vite defaults to port **5173**, matching the React+Vite variant. Add
> `server: { port: 3000 }` to `vite.config.ts` if the user wants a consistent
> port across all frameworks.

> If `vue-tsc` reports errors in auto-generated declaration files inside
> `node_modules` or `.vue-tsc/`, ignore them. Errors in files under `src/` are
> not ignorable.
