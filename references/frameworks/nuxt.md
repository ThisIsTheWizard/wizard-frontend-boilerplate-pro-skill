# Nuxt 4 — Scaffold Reference

## Table of contents

1. [Package list for version resolution](#1-package-list-for-version-resolution)
2. [Scaffold command](#2-scaffold-command)
3. [CLI flag matrix](#3-cli-flag-matrix)
4. [Post-scaffold cleanup](#4-post-scaffold-cleanup)
5. [Routing setup](#5-routing-setup)
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
| Nuxt | `nuxt` |
| Vue | `vue` |
| TypeScript | `typescript` |

> Nuxt bundles Vite, Vue Router, and `vue-tsc` — do not list them separately.
> The installed versions of those packages are managed by Nuxt internally and
> should not be pinned in `package.json` by the user.

**Tailwind v4 (default)**

| Package | Registry name |
|---|---|
| `@nuxtjs/tailwindcss` module | `@nuxtjs/tailwindcss` |
| Tailwind CSS | `tailwindcss` |

> As of Nuxt 4, the recommended Tailwind v4 integration is the
> `@nuxtjs/tailwindcss` module with Tailwind v4 specified as a peer. Confirm
> current module docs in `references/tailwind/per-framework-gotchas.md` before
> scaffolding — this is an area that evolves quickly.

**Tailwind v3 (fallback — only if user chose v3)**

| Package | Registry name |
|---|---|
| `@nuxtjs/tailwindcss` module | `@nuxtjs/tailwindcss` |
| Tailwind CSS | `tailwindcss` (v3 tag: `tailwindcss@3`) |
| PostCSS | `postcss` |
| Autoprefixer | `autoprefixer` |

---

## 2. Scaffold command

Use `nuxi init` — the official Nuxt CLI — with the `--no-install` flag so the
scaffold is separated from installation, matching the workflow used by the other
framework scaffolders.

**TypeScript project (default)**

```bash
npx nuxi@latest init <project-name> --no-install --package-manager <package-manager>
```

**JavaScript project**

```bash
npx nuxi@latest init <project-name> --no-install --package-manager <package-manager>
```

> `nuxi init` does not have a `--js` / `--ts` flag — it always scaffolds
> TypeScript by default. For a JavaScript project, remove `tsconfig.json`
> after scaffolding and rename `.ts` files to `.js` manually (see step 4).

> `--package-manager` accepts `npm`, `pnpm`, `yarn`, or `bun`. Pass the value
> detected by `scripts/detect_package_manager.sh`.

> `--no-install` skips the automatic `npm install` so the skill can run
> `<package-manager> install` itself in the next step.

> pnpm / yarn / bun syntax — replace the `npx nuxi@latest` prefix:

```bash
# pnpm
pnpm dlx nuxi@latest init <project-name> --no-install --package-manager pnpm

# yarn
yarn dlx nuxi@latest init <project-name> --no-install --package-manager yarn

# bun
bunx nuxi@latest init <project-name> --no-install --package-manager bun
```

---

## 3. CLI flag matrix

| User choice | Action |
|---|---|
| TypeScript (default) | No change — `nuxi init` always scaffolds TS |
| JavaScript | After scaffold, delete `tsconfig.json`; rename `server/**/*.ts` → `.js` |
| Specific Nuxt version | Replace `nuxi@latest` with `nuxi@<version>` |
| Package manager | Pass `--package-manager <pm>` |

---

## 4. Post-scaffold cleanup

After `nuxi init` exits, install dependencies, then remove the demo content.

```bash
cd <project-name>

# Install base deps
<package-manager> install

# Remove demo page and component
rm -f app.vue                       # replaced by showcase app shell
rm -f pages/index.vue               # pages/ may not exist yet — ignore if absent
rm -rf components/NuxtWelcome.vue   # present in some nuxi templates
rm -f public/favicon.ico            # keep only if user wants it

# Create directory layout expected by showcase templates
mkdir -p pages
mkdir -p components/ui
mkdir -p assets/styles
mkdir -p utils
```

> Nuxt 4 uses an `app/` directory layout by default (the "app directory"
> convention introduced as opt-in in Nuxt 3 and made default in Nuxt 4). All
> application source lives under `app/` instead of the project root. Confirm
> the layout after scaffolding — if `nuxi init` placed files under `app/`,
> adjust the paths below accordingly.

Create the global stylesheet that imports tokens (written in Phase 4):

```bash
cat > assets/styles/globals.css << 'EOF'
@import "./tokens.css";

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

Create `app.vue` (or `app/app.vue` in the app directory layout) as a minimal
shell that provides the theme class on `<html>` and renders the Nuxt layout:

```vue
<script setup lang="ts">
useHead({
  htmlAttrs: { class: "light" },
});
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
```

> The `class="light"` default on `<html>` is overwritten at runtime by the
> theme provider installed in Phase 4. It prevents a flash of unstyled content
> before the provider runs.

---

## 5. Routing setup

Nuxt uses **file-based routing** — no router config is needed. Create the six
showcase page files and Nuxt generates the routes automatically.

```bash
# Create the six category pages (content added in Phase 6)
touch pages/index.vue
touch pages/inputs.vue
touch pages/display.vue
touch pages/feedback.vue
touch pages/navigation.vue
touch pages/overlay.vue
touch "pages/data-viz.vue"
```

> In the Nuxt 4 app directory layout, pages live at `app/pages/` — adjust the
> `touch` paths above if `nuxi init` used that convention.

Create the default layout that wraps every page with Sidebar and Header. This
file is the Nuxt equivalent of the root layout in Next.js or `AppLayout.vue`
in the Vue+Vite variant. It is installed from
`assets/showcase-templates/vue/AppLayout.vue.template` in Phase 6; create the
stub now so the dev server does not error:

```bash
mkdir -p layouts

cat > layouts/default.vue << 'EOF'
<script setup lang="ts">
</script>

<template>
  <div class="flex min-h-screen bg-background text-foreground">
    <slot />
  </div>
</template>
EOF
```

Phase 6 replaces this stub with the full Sidebar + Header layout.

---

## 6. Tailwind integration

### v4 (default)

Install the Nuxt Tailwind module:

```bash
<package-manager> add -D @nuxtjs/tailwindcss@<resolved-version> tailwindcss@<resolved-version>
```

Register the module in `nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  compatibilityDate: "2025-01-01",
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss"],
  tailwindcss: {
    cssPath: "~/assets/styles/globals.css",
  },
  css: ["~/assets/styles/globals.css"],
});
```

Add the v4 import at the top of `assets/styles/globals.css`:

```css
@import "tailwindcss";
@import "./tokens.css";
```

> No `tailwind.config.ts` is needed for v4 when using `@nuxtjs/tailwindcss`.
> The module handles PostCSS wiring internally.

Full v4 setup: `references/tailwind/v4-setup.md`.

### v3 (fallback)

Install the module with the v3 peer:

```bash
<package-manager> add -D @nuxtjs/tailwindcss tailwindcss@3 postcss autoprefixer
```

Register the module in `nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  compatibilityDate: "2025-01-01",
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss"],
  tailwindcss: {
    cssPath: "~/assets/styles/globals.css",
    configPath: "tailwind.config.js",
  },
});
```

Create `tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./app.vue",
    "./app/**/*.{vue,js,ts}",
  ],
  darkMode: "class",
  theme: { extend: {} },
  plugins: [],
};
```

Replace the top of `assets/styles/globals.css` with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
@import "./tokens.css";
```

Full v3 setup: `references/tailwind/v3-setup.md`.

---

## 7. Expected directory structure

After scaffold + cleanup + Phase 4 setup (standard root layout — not app directory):

```
<project-name>/
├── public/
│   └── favicon.ico
├── assets/
│   └── styles/
│       ├── globals.css
│       └── tokens.css           # Phase 4
├── components/
│   ├── ui/                      # 28 components — Phase 5
│   │   └── ...
│   ├── CodeBlock.vue            # Phase 5c utility
│   ├── Sidebar.vue              # Phase 6
│   └── Header.vue               # Phase 6
├── layouts/
│   └── default.vue              # wraps Sidebar + Header + slot
├── pages/
│   ├── index.vue
│   ├── inputs.vue
│   ├── display.vue
│   ├── feedback.vue
│   ├── navigation.vue
│   ├── overlay.vue
│   └── data-viz.vue
├── utils/
│   └── utils.ts                 # cn() helper
├── app.vue
├── nuxt.config.ts
├── tsconfig.json
└── package.json
```

**Nuxt 4 app directory layout** — if `nuxi init` placed source under `app/`,
the structure above shifts:

```
<project-name>/
├── public/
├── app/
│   ├── assets/styles/           # same contents
│   ├── components/              # same contents
│   ├── layouts/                 # same contents
│   ├── pages/                   # same contents
│   ├── utils/
│   └── app.vue
├── nuxt.config.ts
├── tsconfig.json
└── package.json
```

> Nuxt auto-imports components, composables, and utils — no import statements
> needed for files under `components/`, `composables/`, or `utils/`. The
> `cn()` helper in `utils/utils.ts` is available as `utils` throughout the app
> without an explicit import.

---

## 8. tsconfig adjustments

`nuxi init` generates a `tsconfig.json` that extends Nuxt's auto-generated
`.nuxt/tsconfig.json`. Do not flatten this — Nuxt regenerates its base config
on every `nuxi prepare` / dev server start.

Add stricter options on top of the Nuxt base:

```json
{
  "extends": "./.nuxt/tsconfig.json",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```

> The `@/` import alias and all Nuxt auto-import type declarations are injected
> by `.nuxt/tsconfig.json` — do not redefine `paths` manually. Running
> `<package-manager> run dev` (or `npx nuxi prepare`) must happen before
> `vue-tsc --noEmit` so `.nuxt/` is populated.

---

## 9. Verification

Before advancing to Phase 4:

```bash
# Generate .nuxt/ type declarations first
npx nuxi prepare

# TypeScript check (TS projects only)
npx vue-tsc --noEmit

# Dev server smoke test
<package-manager> run dev
```

Expected output:
- `nuxi prepare` exits 0 and creates `.nuxt/`.
- `vue-tsc --noEmit` exits 0 with no errors.
- Nuxt reports `Local: http://localhost:3000/` (Nuxt defaults to port 3000).
- Browser shows a blank page or minimal layout — both are fine at this stage.

> If `vue-tsc` reports errors in `.nuxt/` auto-generated files, ignore them.
> Errors in files under `components/`, `pages/`, `layouts/`, or `app/` are
> not ignorable.

> Nuxt devtools open as an overlay in the browser. They do not affect the
> showcase and can be left enabled during development.
