# workflow.md — Detailed Playbook

Verbatim commands for every step of the seven-phase scaffold. Load this file
when you need the exact shell syntax for a given framework or phase. For the
high-level flow, see `SKILL.md`. For framework-specific detail beyond what is
shown here, see `references/frameworks/<choice>.md`.

---

## Table of contents

1. [Phase 1 — Interview](#phase-1--interview)
2. [Phase 2 — Version resolution](#phase-2--version-resolution)
3. [Phase 3 — Scaffold](#phase-3--scaffold)
4. [Phase 4 — Theming](#phase-4--theming)
5. [Phase 5 — Component installation](#phase-5--component-installation)
6. [Phase 6 — Showcase routes](#phase-6--showcase-routes)
7. [Phase 7 — Verify](#phase-7--verify)
8. [Failure protocols](#failure-protocols)

---

## Phase 1 — Interview

Collect all six answers before running any commands. Never start Phase 2 early.

```
Q1  Framework?
    1) Next.js (App Router)
    2) React + Vite
    3) Vue 3
    4) Nuxt 4
    5) SvelteKit (Svelte 5)

Q2  Version?
    [ latest stable (default) | specific e.g. "15.3.0" | LTS ]

Q3  Language?
    [ TypeScript (default) | JavaScript ]

Q4  Tailwind version?
    [ v4 (default) | v3 ]
    Note: check references/tailwind/per-framework-gotchas.md before defaulting to v4.

Q5  Color theme?
    1) Modern Slate   — slate neutral + indigo accent
    2) Warm Earth     — stone neutral + amber accent
    3) Fresh Mint     — zinc neutral + emerald accent
    4) Royal          — gray neutral + violet accent
    5) Sunset         — stone neutral + rose accent
    6) Ocean          — slate neutral + cyan accent
    7) Forest         — zinc neutral + green accent
    8) Monochrome     — neutral only, no accent hue
    9) Custom         — provide hex or oklch() values for neutral and accent

Q6  Project name and package manager?
    Run detect_package_manager.sh (see Phase 2), show detected PM, confirm.
    Accept a different project name if the user specifies one.
```

---

## Phase 2 — Version resolution

### 2a — Detect package manager

```bash
bash scripts/detect_package_manager.sh
# Output: one of:  bun  |  pnpm  |  yarn  |  npm
```

Store the output as `PM`. Use it in all subsequent `<package-manager>` placeholders.

### 2b — Query npm registry

```bash
bash scripts/check_versions.sh
```

For machine-readable output (useful when parsing inside a script):

```bash
bash scripts/check_versions.sh --json
```

Present the result table to the user. Ask for confirmation or overrides before
continuing. The packages that matter vary by framework:

| Framework | Key packages to confirm |
|---|---|
| Next.js | `next`, `react`, `react-dom`, `tailwindcss`, `@tailwindcss/postcss` |
| React + Vite | `vite`, `react`, `react-dom`, `react-router-dom`, `tailwindcss`, `@tailwindcss/vite` |
| Vue 3 | `vue`, `vite`, `vue-router`, `tailwindcss`, `@tailwindcss/vite` |
| Nuxt 4 | `nuxt`, `vue`, `tailwindcss`, `@nuxtjs/tailwindcss` |
| SvelteKit | `@sveltejs/kit`, `svelte`, `tailwindcss`, `@tailwindcss/vite` |

Store confirmed versions as variables (e.g. `NEXT_VERSION`, `TW_VERSION`).
Use them verbatim in install commands — never re-query inside the same session.

---

## Phase 3 — Scaffold

### Next.js

**TypeScript (default)**

```bash
npx create-next-app@${NEXT_VERSION} ${PROJECT_NAME} \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-turbopack \
  --yes
```

**JavaScript**

```bash
npx create-next-app@${NEXT_VERSION} ${PROJECT_NAME} \
  --js \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-turbopack \
  --yes
```

**Post-scaffold cleanup**

```bash
cd ${PROJECT_NAME}

rm -f src/app/page.tsx src/app/globals.css
rm -rf public/next.svg public/vercel.svg
mkdir -p src/styles

# Clean global stylesheet
cat > src/app/globals.css << 'EOF'
@import "../styles/tokens.css";

@layer base {
  * { box-sizing: border-box; }
  html { -webkit-font-smoothing: antialiased; }
}
EOF

# Home redirect
cat > src/app/page.tsx << 'EOF'
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/library");
}
EOF

# Library route stubs
mkdir -p src/app/library/inputs src/app/library/display \
  src/app/library/feedback src/app/library/navigation \
  src/app/library/overlay "src/app/library/data-viz"

cat > src/app/library/page.tsx << 'EOF'
export default function LibraryPage() { return null; }
EOF

for dir in inputs display feedback navigation overlay data-viz; do
  echo 'export default function Page() { return null; }' \
    > "src/app/library/$dir/page.tsx"
done
```

**Tailwind v4 adjustments**

```bash
# Remove legacy config if present
rm -f tailwind.config.ts tailwind.config.js

# Overwrite PostCSS config for v4
cat > postcss.config.mjs << 'EOF'
/** @type {import('postcss').Config} */
const config = { plugins: { "@tailwindcss/postcss": {} } };
export default config;
EOF

# v4 import in globals (prepend before tokens import)
cat > src/app/globals.css << 'EOF'
@import "tailwindcss";
@import "../styles/tokens.css";

@layer base {
  * { box-sizing: border-box; }
  html { -webkit-font-smoothing: antialiased; }
}
EOF
```

**Tailwind v3 adjustments** (only if user chose v3)

Keep the generated `tailwind.config.ts`. Replace `src/app/globals.css` top with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
@import "../styles/tokens.css";
```

**tsconfig adjustments** — add to `compilerOptions`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "paths": { "@/*": ["./src/*"] }
  }
}
```

**Verification**

```bash
npx tsc --noEmit       # TS projects only — ignore errors in next-env.d.ts
${PM} run dev          # should start on http://localhost:3000
```

---

### React + Vite

**Scaffold**

```bash
# npm
npm create vite@${VITE_VERSION} ${PROJECT_NAME} -- --template react-ts

# pnpm
pnpm create vite@${VITE_VERSION} ${PROJECT_NAME} --template react-ts

# yarn
yarn create vite@${VITE_VERSION} ${PROJECT_NAME} --template react-ts

# bun
bun create vite@${VITE_VERSION} ${PROJECT_NAME} --template react-ts

# JavaScript variant: replace react-ts with react
```

**Post-scaffold cleanup**

```bash
cd ${PROJECT_NAME}
${PM} install

rm -f src/App.tsx src/App.js src/App.css src/index.css src/assets/react.svg public/vite.svg
mkdir -p src/components/ui src/pages src/styles src/lib

cat > src/globals.css << 'EOF'
@import "./styles/tokens.css";
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-font-smoothing: antialiased; }
EOF
```

**Update `src/main.tsx`**

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import "./globals.css";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

**Install React Router**

```bash
${PM} add react-router-dom@${REACT_ROUTER_VERSION}
```

**Create `src/App.tsx`**

```tsx
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import LibraryLayout from "./components/LibraryLayout";
import DataVizPage from "./pages/DataViz";
import DisplayPage from "./pages/Display";
import FeedbackPage from "./pages/Feedback";
import InputsPage from "./pages/Inputs";
import LibraryHome from "./pages/LibraryHome";
import NavigationPage from "./pages/Navigation";
import OverlayPage from "./pages/Overlay";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/library" replace />} />
        <Route path="/library" element={<LibraryLayout />}>
          <Route index element={<LibraryHome />} />
          <Route path="inputs" element={<InputsPage />} />
          <Route path="display" element={<DisplayPage />} />
          <Route path="feedback" element={<FeedbackPage />} />
          <Route path="navigation" element={<NavigationPage />} />
          <Route path="overlay" element={<OverlayPage />} />
          <Route path="data-viz" element={<DataVizPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

**Tailwind v4 adjustments**

```bash
${PM} add -D tailwindcss@${TW_VERSION} @tailwindcss/vite@${TW_VITE_VERSION}
```

`vite.config.ts`:

```ts
import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
});
```

Prepend to `src/globals.css`:

```css
@import "tailwindcss";
@import "./styles/tokens.css";
```

**Tailwind v3 adjustments** (only if user chose v3)

```bash
${PM} add -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
```

`tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: { extend: {} },
  plugins: [],
};
```

Replace top of `src/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
@import "./styles/tokens.css";
```

**tsconfig adjustments** — add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

**Verification**

```bash
npx tsc --noEmit
${PM} run dev          # starts on http://localhost:5173
```

---

### Vue 3

**Scaffold**

```bash
# npm
npm create vue@latest ${PROJECT_NAME} -- --typescript --router --eslint --prettier

# pnpm
pnpm create vue@latest ${PROJECT_NAME} -- --typescript --router --eslint --prettier

# yarn
yarn create vue@latest ${PROJECT_NAME} --typescript --router --eslint --prettier

# bun
bun create vue@latest ${PROJECT_NAME} -- --typescript --router --eslint --prettier

# JavaScript variant: omit --typescript
```

**Post-scaffold cleanup**

```bash
cd ${PROJECT_NAME}
${PM} install

rm -f src/views/AboutView.vue src/views/HomeView.vue
rm -rf src/components/HelloWorld.vue src/components/TheWelcome.vue \
       src/components/WelcomeItem.vue src/components/icons/
rm -f src/assets/base.css src/assets/main.css src/assets/logo.svg
mkdir -p src/components/ui src/views src/styles src/lib

cat > src/globals.css << 'EOF'
@import "./styles/tokens.css";
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-font-smoothing: antialiased; }
EOF
```

**Update `src/main.ts`**

```ts
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./globals.css";

const app = createApp(App);
app.use(router);
app.mount("#app");
```

**Replace `src/App.vue`**

```vue
<script setup lang="ts">
import AppLayout from "@/components/AppLayout.vue";
</script>

<template>
  <AppLayout />
</template>
```

**Replace `src/router/index.ts`** (full showcase routes):

```ts
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", redirect: "/library" },
    { path: "/library", component: () => import("@/views/LibraryHomeView.vue") },
    { path: "/library/inputs", component: () => import("@/views/InputsView.vue") },
    { path: "/library/display", component: () => import("@/views/DisplayView.vue") },
    { path: "/library/feedback", component: () => import("@/views/FeedbackView.vue") },
    { path: "/library/navigation", component: () => import("@/views/NavigationView.vue") },
    { path: "/library/overlay", component: () => import("@/views/OverlayView.vue") },
    { path: "/library/data-viz", component: () => import("@/views/DataVizView.vue") },
  ],
});

export default router;
```

**Tailwind v4 adjustments**

```bash
${PM} add -D tailwindcss@${TW_VERSION} @tailwindcss/vite@${TW_VITE_VERSION}
```

`vite.config.ts`:

```ts
import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
});
```

Prepend to `src/globals.css`:

```css
@import "tailwindcss";
@import "./styles/tokens.css";
```

**Tailwind v3 adjustments** (only if user chose v3)

```bash
${PM} add -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
```

`tailwind.config.js` content array must include `.vue` files:

```js
content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
darkMode: "class",
```

**tsconfig adjustments** — add to `tsconfig.app.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```

**Verification**

```bash
npx vue-tsc --noEmit
${PM} run dev          # starts on http://localhost:5173
```

---

### Nuxt 4

**Scaffold**

```bash
# npm
npx nuxi@latest init ${PROJECT_NAME} --no-install --package-manager npm

# pnpm
pnpm dlx nuxi@latest init ${PROJECT_NAME} --no-install --package-manager pnpm

# yarn
yarn dlx nuxi@latest init ${PROJECT_NAME} --no-install --package-manager yarn

# bun
bunx nuxi@latest init ${PROJECT_NAME} --no-install --package-manager bun
```

**Post-scaffold cleanup**

```bash
cd ${PROJECT_NAME}
${PM} install

rm -f app.vue pages/index.vue
rm -rf components/NuxtWelcome.vue
mkdir -p pages components/ui assets/styles utils

cat > assets/styles/globals.css << 'EOF'
@import "./tokens.css";
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-font-smoothing: antialiased; }
EOF

cat > app.vue << 'EOF'
<script setup lang="ts">
useHead({ htmlAttrs: { class: "light" } });
</script>
<template>
  <NuxtLayout><NuxtPage /></NuxtLayout>
</template>
EOF
```

> **Nuxt 4 app directory:** if `nuxi init` placed source under `app/`, all
> paths above shift to `app/pages/`, `app/components/`, `app/assets/`, etc.
> Confirm the layout after scaffolding before running these commands.

**Route stubs**

```bash
cat > pages/index.vue << 'EOF'
<script setup lang="ts">
await navigateTo("/library", { replace: true });
</script>
EOF

mkdir -p pages/library
touch pages/library/index.vue pages/library/inputs.vue \
      pages/library/display.vue pages/library/feedback.vue \
      pages/library/navigation.vue pages/library/overlay.vue \
      "pages/library/data-viz.vue"

mkdir -p layouts

cat > layouts/default.vue << 'EOF'
<script setup lang="ts"></script>
<template>
  <div class="flex min-h-screen bg-background text-foreground">
    <slot />
  </div>
</template>
EOF
```

**Tailwind v4 adjustments**

```bash
${PM} add -D @nuxtjs/tailwindcss@${NUXT_TW_VERSION} tailwindcss@${TW_VERSION}
```

`nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  compatibilityDate: "2025-01-01",
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss"],
  tailwindcss: { cssPath: "~/assets/styles/globals.css" },
  css: ["~/assets/styles/globals.css"],
});
```

Prepend to `assets/styles/globals.css`:

```css
@import "tailwindcss";
@import "./tokens.css";
```

**Tailwind v3 adjustments** (only if user chose v3)

```bash
${PM} add -D @nuxtjs/tailwindcss tailwindcss@3 postcss autoprefixer
```

Add `configPath: "tailwind.config.js"` to `tailwindcss` key in `nuxt.config.ts`.
Create `tailwind.config.js` with content paths covering `components/`, `layouts/`,
`pages/`, `app.vue`, and `app/**/*`.

**tsconfig adjustments**

```json
{
  "extends": "./.nuxt/tsconfig.json",
  "compilerOptions": { "strict": true, "noUncheckedIndexedAccess": true }
}
```

**Verification**

```bash
npx nuxi prepare          # generates .nuxt/ type declarations
npx vue-tsc --noEmit
${PM} run dev             # starts on http://localhost:3000
```

---

### SvelteKit (Svelte 5)

**Scaffold**

```bash
# npx
npx sv@latest create ${PROJECT_NAME} --template minimal --types ts --no-add-ons

# pnpm
pnpm dlx sv@latest create ${PROJECT_NAME} --template minimal --types ts --no-add-ons

# yarn
yarn dlx sv@latest create ${PROJECT_NAME} --template minimal --types ts --no-add-ons

# bun
bunx sv@latest create ${PROJECT_NAME} --template minimal --types ts --no-add-ons

# JavaScript variant: omit --types ts
```

**Post-scaffold cleanup**

```bash
cd ${PROJECT_NAME}
${PM} install

${PM} add -D eslint eslint-plugin-svelte prettier prettier-plugin-svelte \
           prettier-plugin-perfectionist globals

mkdir -p src/lib/components/ui src/lib/styles src/lib/utils

cat > src/lib/styles/globals.css << 'EOF'
@import "./tokens.css";
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-font-smoothing: antialiased; }
EOF

cat > .prettierrc.json << 'EOF'
{
  "plugins": ["prettier-plugin-svelte", "prettier-plugin-perfectionist"],
  "overrides": [{ "files": "*.svelte", "options": { "parser": "svelte" } }]
}
EOF

cat > eslint.config.js << 'EOF'
import js from "@eslint/js";
import svelte from "eslint-plugin-svelte";
import globals from "globals";

export default [
  js.configs.recommended,
  ...svelte.configs["flat/recommended"],
  { languageOptions: { globals: { ...globals.browser, ...globals.node } } },
  { ignores: [".svelte-kit/", "build/"] },
];
EOF
```

**Root layout and SSR disable**

```bash
cat > src/routes/+layout.svelte << 'EOF'
<script lang="ts">
  import "$lib/styles/globals.css";
  import type { Snippet } from "svelte";
  let { children }: { children: Snippet } = $props();
</script>

<div class="flex min-h-screen bg-background text-foreground">
  {@render children()}
</div>
EOF

cat > src/routes/+layout.ts << 'EOF'
export const prerender = false;
export const ssr = false;
EOF
```

**Route stubs**

```bash
cat > src/routes/+page.svelte << 'EOF'
<script lang="ts">
  import { goto } from "$app/navigation";
  goto("/library", { replaceState: true });
</script>
EOF

mkdir -p src/routes/library/inputs src/routes/library/display \
         src/routes/library/feedback src/routes/library/navigation \
         src/routes/library/overlay "src/routes/library/data-viz"

touch src/routes/library/+page.svelte

cat > src/routes/library/+layout.svelte << 'EOF'
<script lang="ts">
  import type { Snippet } from "svelte";
  let { children }: { children: Snippet } = $props();
</script>
<div class="flex min-h-screen bg-background text-foreground">
  {@render children()}
</div>
EOF

for dir in inputs display feedback navigation overlay data-viz; do
  touch "src/routes/library/$dir/+page.svelte"
done
```

**Tailwind v4 adjustments**

```bash
${PM} add -D tailwindcss@${TW_VERSION} @tailwindcss/vite@${TW_VITE_VERSION}
```

`vite.config.ts`:

```ts
import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

// sveltekit() must come before tailwindcss()
export default defineConfig({
  plugins: [sveltekit(), tailwindcss()],
});
```

Prepend to `src/lib/styles/globals.css`:

```css
@import "tailwindcss";
@import "./tokens.css";
```

**Tailwind v3 adjustments** (only if user chose v3)

```bash
${PM} add -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
```

`tailwind.config.js` content must include `.svelte` files:

```js
content: ["./src/**/*.{html,js,ts,svelte}"],
darkMode: "class",
```

**tsconfig adjustments**

```json
{
  "extends": "./.svelte-kit/tsconfig.json",
  "compilerOptions": { "strict": true, "noUncheckedIndexedAccess": true }
}
```

**Verification**

```bash
npx svelte-kit sync
npx svelte-check --tsconfig ./tsconfig.json
${PM} run dev             # starts on http://localhost:5173
```

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

### 5a — Locate sibling skill

```bash
bash scripts/locate_ui_ux_pro_max.sh
# Prints absolute path on success (exit 0)
# Prints error to stderr and exits 1 if not found
```

Store the result as `UI_SKILL_PATH`. If exit 1, proceed to the fallback path.

### 5b — Install 28 components

**If sibling skill found** — for each of the 28 components:

1. Find the source using the name-mapping table in
   `references/ui-library/ui-ux-pro-max-bridge.md`.
2. Adapt to the target framework using
   `references/ui-library/framework-adapters/<choice>-adapter.md`:
   - **React** — JSX, hooks, `React.forwardRef`, `cn()` for class merging
   - **Vue** — SFC `<script setup>`, `defineProps`, `defineEmits`, `v-model`
   - **Svelte 5** — `$props()` rune, snippets (`{@render children()}`), `$state()`
3. Replace any hard-coded color values with CSS variable tokens from Phase 4.
4. Write the adapted file to:

| Framework | Destination |
|---|---|
| Next.js / React + Vite | `src/components/ui/<ComponentName>.tsx` |
| Vue 3 / Nuxt 4 | `src/components/ui/<ComponentName>.vue` |
| SvelteKit | `src/lib/components/ui/<ComponentName>.svelte` |

**If sibling skill not found** — use implementations from
`references/ui-library/custom-tailwind.md`. These are minimal Tailwind-only
variants with no external dependencies. Write them to the same destinations.

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

### 6a — Install layout templates

Copy from `assets/showcase-templates/<framework>/` and place in the project:

| Framework | Template files | Destination |
|---|---|---|
| Next.js | `react/layout.tsx.template`, `react/sidebar.tsx.template` | `src/app/library/layout.tsx`, `src/components/Sidebar.tsx` |
| React + Vite | `react/layout.tsx.template`, `react/sidebar.tsx.template` | `src/components/LibraryLayout.tsx`, `src/components/Sidebar.tsx` |
| Vue 3 / Nuxt 4 | `vue/AppLayout.vue.template`, `vue/Sidebar.vue.template` | `src/components/AppLayout.vue`, `src/components/Sidebar.vue` |
| SvelteKit | `svelte/+layout.svelte.template` | `src/routes/library/+layout.svelte` |

Replace all `{{PLACEHOLDER}}` tokens in every copied file:

| Token | Value |
|---|---|
| `{{PROJECT_NAME}}` | User's project name |
| `{{COLOR_PRESET}}` | Selected preset label (e.g. `"Modern Slate"`) |
| `{{NEUTRAL_VAR}}` | `--color-neutral` |
| `{{ACCENT_VAR}}` | `--color-accent` |
| `{{IMPORT_ALIAS}}` | `@/` for React/Vue/Next.js; `$lib/` for SvelteKit |

### 6b — Install category page templates

Copy the six category templates and write them to the routes established in
Phase 3:

| Category | React destination | Vue destination | Svelte destination |
|---|---|---|---|
| Inputs | `src/pages/Inputs.tsx` | `src/views/InputsView.vue` | `src/routes/library/inputs/+page.svelte` |
| Display | `src/pages/Display.tsx` | `src/views/DisplayView.vue` | `src/routes/library/display/+page.svelte` |
| Feedback | `src/pages/Feedback.tsx` | `src/views/FeedbackView.vue` | `src/routes/library/feedback/+page.svelte` |
| Navigation | `src/pages/Navigation.tsx` | `src/views/NavigationView.vue` | `src/routes/library/navigation/+page.svelte` |
| Overlay | `src/pages/Overlay.tsx` | `src/views/OverlayView.vue` | `src/routes/library/overlay/+page.svelte` |
| Data viz | `src/pages/DataViz.tsx` | `src/views/DataVizView.vue` | `src/routes/library/data-viz/+page.svelte` |

> For Next.js, templates go to `src/app/library/<category>/page.tsx` (not `src/pages/`).

### 6c — Install /library landing page

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
