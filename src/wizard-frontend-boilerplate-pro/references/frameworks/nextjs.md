# Next.js — Scaffold Reference

## Table of contents

1. [Package list for version resolution](#1-package-list-for-version-resolution)
2. [Scaffold command](#2-scaffold-command)
3. [CLI flag matrix](#3-cli-flag-matrix)
4. [Post-scaffold cleanup](#4-post-scaffold-cleanup)
5. [Tailwind integration](#5-tailwind-integration)
6. [Expected directory structure](#6-expected-directory-structure)
7. [tsconfig adjustments](#7-tsconfig-adjustments)
8. [Verification](#8-verification)

---

## 1. Package list for version resolution

Pass these names to `scripts/check_versions.sh` during Phase 2. The script
queries the npm registry and returns the latest stable version for each.

**Core**

| Package | Registry name |
|---|---|
| Next.js | `next` |
| React | `react` |
| React DOM | `react-dom` |
| TypeScript | `typescript` |
| `@types/react` | `@types/react` |
| `@types/react-dom` | `@types/react-dom` |
| `@types/node` | `@types/node` |

**Tailwind v4 (default)**

| Package | Registry name |
|---|---|
| Tailwind CSS | `tailwindcss` |
| PostCSS plugin | `@tailwindcss/postcss` |
| PostCSS | `postcss` |

**Tailwind v3 (fallback — only if user chose v3)**

| Package | Registry name |
|---|---|
| Tailwind CSS | `tailwindcss` (v3 tag: `tailwindcss@3`) |
| PostCSS | `postcss` |
| Autoprefixer | `autoprefixer` |

> Gotchas: see `references/tailwind/per-framework-gotchas.md` before
> defaulting to v4. As of Next.js 15 the `@tailwindcss/postcss` adapter is
> the correct v4 integration path; the legacy `tailwind.config.js` approach
> is v3 only.

---

## 2. Scaffold command

Use `create-next-app` with the flags derived from the user's answers. Do not
run `npx create-next-app` interactively — always pass all flags non-interactively
so the scaffold is reproducible and works in headless environments.

**TypeScript project (default)**

```bash
npx create-next-app@<resolved-version> <project-name> \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --yes
```

**JavaScript project**

```bash
npx create-next-app@<resolved-version> <project-name> \
  --js \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --yes
```

> `--tailwind` lets `create-next-app` install its own initial Tailwind config.
> The boilerplate skill will overwrite that config in Phase 4 with the
> generated palette. Do not skip `--tailwind` — it wires up PostCSS correctly.

> `--app` selects the App Router. The Pages Router is not supported by this skill.

> `--src-dir` places all application code under `src/`, which is required for
> the showcase template paths to resolve correctly.

---

## 3. CLI flag matrix

| User choice | Flags to add/change |
|---|---|
| TypeScript | `--typescript` (default) |
| JavaScript | `--js` (replaces `--typescript`) |
| With ESLint | `--eslint` (always include) |
| App Router | `--app` (always include) |
| src/ directory | `--src-dir` (always include) |
| Specific version | Replace `@<resolved-version>` with `@<user-version>` |

---

## 4. Post-scaffold cleanup

After `create-next-app` exits, remove the demo content that ships with every
fresh scaffold. These files are replaced by the showcase templates in Phase 6.

```bash
# Remove boilerplate demo files
rm -f src/app/page.tsx          # replaced by redirect below
rm -f src/app/globals.css       # replaced by tokens.css import
rm -rf public/next.svg
rm -rf public/vercel.svg

# Remove default favicon (keep only if the user wants it)
# rm -f public/favicon.ico
```

Create a clean global stylesheet that only imports tokens:

```bash
cat > src/app/globals.css << 'EOF'
@import "../styles/tokens.css";

@layer base {
  * {
    box-sizing: border-box;
  }
  html {
    -webkit-font-smoothing: antialiased;
  }
}
EOF
```

Create the styles directory for Phase 4:

```bash
mkdir -p src/styles
```

Write the home page that redirects to `/library`:

```bash
cat > src/app/page.tsx << 'EOF'
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/library");
}
EOF
```

Create the `/library` route group and its stub pages (Phase 6 fills in content):

```bash
mkdir -p src/app/library/inputs
mkdir -p src/app/library/display
mkdir -p src/app/library/feedback
mkdir -p src/app/library/navigation
mkdir -p src/app/library/overlay
mkdir -p "src/app/library/data-viz"

# Library landing page
cat > src/app/library/page.tsx << 'EOF'
export default function LibraryPage() {
  return null;
}
EOF

# Category page stubs (Phase 6 installs full content)
for dir in inputs display feedback navigation overlay data-viz; do
  echo 'export default function Page() { return null; }' > "src/app/library/$dir/page.tsx"
done
```

---

## 5. Tailwind integration

### v4 (default)

`create-next-app --tailwind` installs `tailwindcss` and writes a
`postcss.config.mjs`. For v4 the PostCSS plugin package must be
`@tailwindcss/postcss`, not `tailwindcss` directly.

Overwrite `postcss.config.mjs`:

```js
/** @type {import('postcss').Config} */
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
```

Remove `tailwind.config.ts` or `tailwind.config.js` if `create-next-app`
generated one — v4 uses a CSS-first `@theme` block instead.

Add the v4 import to `src/app/globals.css` **before** the tokens import:

```css
@import "tailwindcss";
@import "../styles/tokens.css";
```

Full v4 setup: `references/tailwind/v4-setup.md`.

### v3 (fallback)

Keep the generated `tailwind.config.ts`. Ensure `content` includes:

```ts
content: [
  "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
],
```

Replace the globals.css imports with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
@import "../styles/tokens.css";
```

Full v3 setup: `references/tailwind/v3-setup.md`.

---

## 6. Expected directory structure

After scaffold + cleanup + Phase 4 setup, the project should look like:

```
<project-name>/
├── public/
│   └── favicon.ico
├── src/
│   ├── app/
│   │   ├── library/             # showcase section — added in Phase 6
│   │   │   ├── layout.tsx       # sidebar + header layout for /library/*
│   │   │   ├── page.tsx         # /library landing with category links
│   │   │   ├── inputs/
│   │   │   │   └── page.tsx
│   │   │   ├── display/
│   │   │   │   └── page.tsx
│   │   │   ├── feedback/
│   │   │   │   └── page.tsx
│   │   │   ├── navigation/
│   │   │   │   └── page.tsx
│   │   │   ├── overlay/
│   │   │   │   └── page.tsx
│   │   │   └── data-viz/
│   │   │       └── page.tsx
│   │   ├── layout.tsx           # root layout with ThemeProvider only
│   │   ├── page.tsx             # redirects to /library
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                  # 28 components installed in Phase 5
│   │   │   └── ...
│   │   ├── CodeBlock.tsx        # Phase 5c utility
│   │   ├── Sidebar.tsx          # Phase 6
│   │   └── Header.tsx           # Phase 6
│   ├── styles/
│   │   └── tokens.css           # generated in Phase 4
│   └── lib/
│       └── utils.ts             # cn() helper (clsx + tailwind-merge)
├── next.config.ts
├── postcss.config.mjs
├── tsconfig.json                # TypeScript projects only
└── package.json
```

`src/app/layout.tsx` is the root layout — it mounts the `ThemeProvider` and
sets `<html lang="en">` but does **not** render the Sidebar. The Sidebar lives
in `src/app/library/layout.tsx` so it only appears on `/library/*` routes, not
on the redirect page at `/`.

---

## 7. tsconfig adjustments

`create-next-app` generates a reasonable `tsconfig.json`. Make the following
adjustments for strict correctness:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

- `noUncheckedIndexedAccess` prevents silent `undefined` bugs when indexing
  arrays — important for the component showcase where dynamic data indexing
  is common.
- The `paths` alias must match the `--import-alias "@/*"` flag used at
  scaffold time; `create-next-app` should already set this correctly.

---

## 8. Verification

Before advancing to Phase 4, confirm the scaffold is healthy:

```bash
cd <project-name>

# TypeScript check (TS projects only)
npx tsc --noEmit

# Dev server smoke test
# pnpm dev | yarn dev | npm run dev | bun dev
<package-manager> dev
```

Expected output:
- `tsc --noEmit` exits 0 with no errors.
- Dev server starts and reports `ready` on `http://localhost:3000`.
- Browser shows the default Next.js page (or blank page after cleanup — both are fine).

If `tsc` reports errors in auto-generated files (`next-env.d.ts`, etc.), ignore
them — they resolve after the first `next build`. Errors in files you wrote are
not ignorable.
