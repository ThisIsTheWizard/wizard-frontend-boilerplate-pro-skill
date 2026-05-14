# SvelteKit — Scaffold Reference (Svelte 5)

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
| SvelteKit | `@sveltejs/kit` |
| Svelte | `svelte` |
| Vite adapter | `@sveltejs/adapter-auto` |
| Vite | `vite` |
| `@sveltejs/vite-plugin-svelte` | `@sveltejs/vite-plugin-svelte` |
| TypeScript | `typescript` |

> SvelteKit bundles Vite and its own Svelte plugin — do not install them
> separately. The versions above are resolved for display only; `sv create`
> manages the actual pinned versions in the generated `package.json`.

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
> ships a first-class Vite plugin (`@tailwindcss/vite`) that works with
> SvelteKit's Vite build — add it to `vite.config.ts` alongside the Svelte
> plugin. Do not mix `@tailwindcss/postcss` with the Vite plugin.

---

## 2. Scaffold command

Use `sv` — the official SvelteKit CLI introduced with Svelte 5 — with explicit
flags for a non-interactive, reproducible scaffold.

**TypeScript project (default)**

```bash
npx sv@latest create <project-name> --template minimal --types ts --no-add-ons
```

**JavaScript project**

```bash
npx sv@latest create <project-name> --template minimal --no-add-ons
```

> `--template minimal` produces the smallest possible scaffold — a root layout,
> a home page, and no demo content. Do not use `--template demo`; it adds
> sample routes and components that conflict with the showcase structure.

> `--types ts` adds TypeScript support: `tsconfig.json`, `.svelte-check` config,
> and `lang="ts"` on all generated `<script>` blocks.

> `--no-add-ons` skips the interactive add-on picker (ESLint, Prettier, etc.).
> The boilerplate skill installs its own ESLint + Prettier config in the cleanup
> step below, matching the configuration used across all three frameworks.

> pnpm / yarn / bun syntax — replace `npx sv@latest` with the appropriate
> runner:

```bash
# pnpm
pnpm dlx sv@latest create <project-name> --template minimal --types ts --no-add-ons

# yarn
yarn dlx sv@latest create <project-name> --template minimal --types ts --no-add-ons

# bun
bunx sv@latest create <project-name> --template minimal --types ts --no-add-ons
```

> `sv create` does not accept a `--package-manager` flag — it detects the
> active package manager from the environment. Run the command with the
> intended package manager's runner (e.g. `pnpm dlx`) so the generated
> lock file matches the rest of the project.

---

## 3. CLI flag matrix

| User choice | Action |
|---|---|
| TypeScript (default) | `--types ts` |
| JavaScript | _(omit `--types ts`)_ |
| Specific SvelteKit version | After scaffold, update `@sveltejs/kit` in `package.json` and reinstall |
| Package manager | Use the corresponding runner (`npx` / `pnpm dlx` / `yarn dlx` / `bunx`) |

---

## 4. Post-scaffold cleanup

After `sv create` exits, install dependencies, add linting tooling, and remove
the minimal demo content.

```bash
cd <project-name>

# Install base deps first
<package-manager> install

# Install ESLint + Prettier (matching other framework scaffolds)
<package-manager> add -D \
  eslint \
  eslint-plugin-svelte \
  prettier \
  prettier-plugin-svelte \
  prettier-plugin-perfectionist \
  globals

# Stub out the home page (content added in Phase 6)
cat > src/routes/+page.svelte << 'EOF'
<script lang="ts">
</script>
EOF

# Stub out the root layout (Phase 6 installs the full version)
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

# Create directory layout expected by showcase templates
mkdir -p src/lib/components/ui
mkdir -p src/lib/styles
mkdir -p src/lib/utils
```

Create `eslint.config.js`:

```js
import js from "@eslint/js";
import svelte from "eslint-plugin-svelte";
import globals from "globals";

export default [
  js.configs.recommended,
  ...svelte.configs["flat/recommended"],
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
    },
  },
  {
    ignores: [".svelte-kit/", "build/"],
  },
];
```

Create `.prettierrc.json`:

```json
{
  "plugins": ["prettier-plugin-svelte", "prettier-plugin-perfectionist"],
  "overrides": [
    {
      "files": "*.svelte",
      "options": { "parser": "svelte" }
    }
  ]
}
```

Create the global stylesheet that imports tokens (written in Phase 4):

```bash
cat > src/lib/styles/globals.css << 'EOF'
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

> The `@import "tailwindcss"` directive is prepended to this file in step 6
> once Tailwind is installed — do not add it here.

---

## 5. Routing setup

SvelteKit uses **file-based routing** with a `+page.svelte` / `+layout.svelte`
convention — no router config is needed. Create the six showcase routes now;
Phase 6 populates their content from `assets/showcase-templates/svelte/`.

```bash
# Home route already exists at src/routes/+page.svelte

# Create the six category routes
mkdir -p src/routes/inputs
mkdir -p src/routes/display
mkdir -p src/routes/feedback
mkdir -p src/routes/navigation
mkdir -p src/routes/overlay
mkdir -p "src/routes/data-viz"

touch src/routes/inputs/+page.svelte
touch src/routes/display/+page.svelte
touch src/routes/feedback/+page.svelte
touch src/routes/navigation/+page.svelte
touch src/routes/overlay/+page.svelte
touch "src/routes/data-viz/+page.svelte"
```

The resulting URL structure:

| File | URL |
|---|---|
| `src/routes/+page.svelte` | `/` |
| `src/routes/inputs/+page.svelte` | `/inputs` |
| `src/routes/display/+page.svelte` | `/display` |
| `src/routes/feedback/+page.svelte` | `/feedback` |
| `src/routes/navigation/+page.svelte` | `/navigation` |
| `src/routes/overlay/+page.svelte` | `/overlay` |
| `src/routes/data-viz/+page.svelte` | `/data-viz` |

Create a `+layout.ts` at the root to disable prerendering — required so the
theme provider's `localStorage` access works on the initial SSR request:

```bash
cat > src/routes/+layout.ts << 'EOF'
export const prerender = false;
export const ssr = false;
EOF
```

> Setting `ssr = false` makes SvelteKit render entirely on the client (SPA
> mode). This avoids a `localStorage is not defined` error during server-side
> rendering before the theme provider hydrates. If the user later needs SSR,
> remove this file and update the theme provider to use `$effect` only.

> Phase 6 replaces the root `+layout.svelte` stub with the full Sidebar +
> Header layout shell.

---

## 6. Tailwind integration

### v4 (default)

Install the Vite plugin:

```bash
<package-manager> add -D tailwindcss@<resolved-version> @tailwindcss/vite@<resolved-version>
```

Update `vite.config.ts` to add the Tailwind plugin alongside the Svelte plugin:

```ts
import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit(), tailwindcss()],
});
```

> Plugin order matters: `sveltekit()` must come before `tailwindcss()`.
> Swapping the order can cause Svelte component styles to be emitted after
> Tailwind utilities, producing specificity conflicts.

Prepend the v4 import to `src/lib/styles/globals.css`:

```css
@import "tailwindcss";
@import "./tokens.css";
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
  content: ["./src/**/*.{html,js,ts,svelte}"],
  darkMode: "class",
  theme: { extend: {} },
  plugins: [],
};
```

> The `content` glob must include `.svelte` files.

SvelteKit's Vite build picks up `postcss.config.js` automatically — no
additional `vite.config.ts` change is needed for v3.

Replace the top of `src/lib/styles/globals.css` with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
@import "./tokens.css";
```

Full v3 setup: `references/tailwind/v3-setup.md`.

---

## 7. Expected directory structure

After scaffold + cleanup + Phase 4 setup:

```
<project-name>/
├── static/
│   └── favicon.png
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ui/                  # 28 components — Phase 5
│   │   │   │   └── ...
│   │   │   ├── CodeBlock.svelte     # Phase 5c utility
│   │   │   ├── Sidebar.svelte       # Phase 6
│   │   │   └── Header.svelte        # Phase 6
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   └── tokens.css           # Phase 4
│   │   ├── utils/
│   │   │   └── utils.ts             # cn() helper
│   │   └── index.ts                 # barrel export
│   └── routes/
│       ├── +layout.svelte           # Sidebar + Header shell
│       ├── +layout.ts               # ssr = false, prerender = false
│       ├── +page.svelte             # home
│       ├── inputs/
│       │   └── +page.svelte
│       ├── display/
│       │   └── +page.svelte
│       ├── feedback/
│       │   └── +page.svelte
│       ├── navigation/
│       │   └── +page.svelte
│       ├── overlay/
│       │   └── +page.svelte
│       └── data-viz/
│           └── +page.svelte
├── vite.config.ts
├── svelte.config.js
├── tsconfig.json
├── eslint.config.js
├── .prettierrc.json
└── package.json
```

> SvelteKit resolves `$lib` to `src/lib/` automatically — no `vite.config.ts`
> alias needed. Import components as
> `import Button from "$lib/components/ui/Button.svelte"`.

> The `src/lib/index.ts` barrel is optional but useful for re-exporting utility
> functions shared across routes (e.g. `cn()`).

---

## 8. tsconfig adjustments

`sv create --types ts` generates a `tsconfig.json` that extends SvelteKit's
auto-generated `.svelte-kit/tsconfig.json`. Do not flatten this — SvelteKit
regenerates the base config on every `svelte-kit sync` / dev server start.

Add stricter options on top of the SvelteKit base:

```json
{
  "extends": "./.svelte-kit/tsconfig.json",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```

> The `$lib` path alias, Svelte component type declarations, and all SvelteKit
> route type stubs are injected by `.svelte-kit/tsconfig.json`. Do not redefine
> `paths` or `types` manually. Running `<package-manager> run dev` (or
> `npx svelte-kit sync`) must happen before `svelte-check` so `.svelte-kit/`
> is populated.

> Svelte 5 ships improved TypeScript integration: component props typed via
> `$props()` runes are fully inferred, and snippets carry the `Snippet<[T]>`
> generic type. Use `svelte-check` (bundled by `sv create --types ts`) as the
> type-checker for `.svelte` files rather than plain `tsc`.

---

## 9. Verification

Before advancing to Phase 4:

```bash
# Sync SvelteKit type declarations first
npx svelte-kit sync

# TypeScript + Svelte check (TS projects only)
npx svelte-check --tsconfig ./tsconfig.json

# Dev server smoke test
<package-manager> run dev
```

Expected output:
- `svelte-kit sync` exits 0 and creates `.svelte-kit/`.
- `svelte-check` exits 0 with 0 errors and 0 warnings.
- Vite reports `Local: http://localhost:5173/` (SvelteKit defaults to 5173).
- Browser shows a blank page — the demo content was cleared in step 4.

> If `svelte-check` reports errors inside `.svelte-kit/` generated types,
> ignore them. Errors in files under `src/` are not ignorable.

> SvelteKit defaults to port **5173** (same as Vite). Add
> `server: { port: 3000 }` to `vite.config.ts` if the user wants a consistent
> port across all frameworks.

> `sv create` may prompt to install the `sv` package if it is not already
> cached. Accept the prompt — it only downloads the CLI, not the project
> dependencies.
