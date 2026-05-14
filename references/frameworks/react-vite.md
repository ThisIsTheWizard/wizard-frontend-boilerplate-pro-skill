# React + Vite — Scaffold Reference

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
| Vite | `vite` |
| React | `react` |
| React DOM | `react-dom` |
| React Router | `react-router-dom` |
| TypeScript | `typescript` |
| `@types/react` | `@types/react` |
| `@types/react-dom` | `@types/react-dom` |
| `@vitejs/plugin-react` | `@vitejs/plugin-react` |

**Tailwind v4 (default)**

| Package | Registry name |
|---|---|
| Tailwind CSS | `tailwindcss` |
| Vite plugin | `@tailwindcss/vite` |

**Tailwind v3 (fallback)**

| Package | Registry name |
|---|---|
| Tailwind CSS | `tailwindcss` (v3 tag: `tailwindcss@3`) |
| PostCSS | `postcss` |
| Autoprefixer | `autoprefixer` |

> Gotchas: see `references/tailwind/per-framework-gotchas.md`. Tailwind v4
> ships a first-class Vite plugin (`@tailwindcss/vite`) that replaces the
> PostCSS integration — do not mix `@tailwindcss/postcss` with the Vite plugin.

---

## 2. Scaffold command

Use `create vite` with `--template` flags so the scaffold is non-interactive
and reproducible.

**TypeScript project (default)**

```bash
npm create vite@<resolved-version> <project-name> -- --template react-ts
```

**JavaScript project**

```bash
npm create vite@<resolved-version> <project-name> -- --template react
```

> Vite's `create` command requires the double `--` separator before template
> flags when invoked via `npm create`. With pnpm or yarn the syntax differs:

```bash
# pnpm
pnpm create vite@<resolved-version> <project-name> --template react-ts

# yarn
yarn create vite@<resolved-version> <project-name> --template react-ts

# bun
bun create vite@<resolved-version> <project-name> --template react-ts
```

> Vite does not scaffold Tailwind, ESLint, or a router. All three are added
> manually in the steps below.

---

## 3. CLI flag matrix

| User choice | Template flag |
|---|---|
| TypeScript | `react-ts` (default) |
| JavaScript | `react` |

> Vite does not offer App Router / Pages Router distinctions — routing is
> added via React Router in the post-scaffold step.

---

## 4. Post-scaffold cleanup

After scaffolding, install dependencies and remove the Vite demo content.

```bash
cd <project-name>

# Install base deps first so subsequent commands resolve correctly
<package-manager> install

# Remove Vite demo files
rm -f src/App.tsx src/App.js        # replaced by showcase root component
rm -f src/App.css                   # replaced by tokens.css
rm -f src/index.css                 # replaced by globals.css
rm -f src/assets/react.svg
rm -f public/vite.svg

# Create directory layout expected by showcase templates
mkdir -p src/components/ui
mkdir -p src/pages
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

Update `src/main.tsx` (or `src/main.jsx`) to import the global stylesheet:

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

---

## 5. Routing setup

React + Vite has no built-in router. Install React Router and wire up the six
showcase routes.

```bash
<package-manager> add react-router-dom@<resolved-version>
```

Create `src/App.tsx` with a `BrowserRouter` wrapping the showcase layout:

```tsx
import { BrowserRouter, Route, Routes } from "react-router-dom";
import RootLayout from "./components/RootLayout";
import Home from "./pages/Home";
import InputsPage from "./pages/Inputs";
import DisplayPage from "./pages/Display";
import FeedbackPage from "./pages/Feedback";
import NavigationPage from "./pages/Navigation";
import OverlayPage from "./pages/Overlay";
import DataVizPage from "./pages/DataViz";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RootLayout />}>
          <Route index element={<Home />} />
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

`RootLayout` renders `<Sidebar />`, `<Header />`, and `<Outlet />`. It is
installed from `assets/showcase-templates/react/layout.tsx.template` in Phase 6.

---

## 6. Tailwind integration

### v4 (default)

Install the Vite plugin:

```bash
<package-manager> add -D tailwindcss@<resolved-version> @tailwindcss/vite@<resolved-version>
```

Update `vite.config.ts`:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

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
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: { extend: {} },
  plugins: [],
};
```

Replace globals.css imports with:

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
│   │   ├── CodeBlock.tsx        # Phase 5c utility
│   │   ├── RootLayout.tsx       # wraps Sidebar + Header + Outlet
│   │   ├── Sidebar.tsx          # Phase 6
│   │   └── Header.tsx           # Phase 6
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Inputs.tsx
│   │   ├── Display.tsx
│   │   ├── Feedback.tsx
│   │   ├── Navigation.tsx
│   │   ├── Overlay.tsx
│   │   └── DataViz.tsx
│   ├── styles/
│   │   └── tokens.css           # Phase 4
│   ├── lib/
│   │   └── utils.ts             # cn() helper
│   ├── globals.css
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── vite.config.ts
├── tsconfig.json                # TS projects only
├── tsconfig.node.json           # TS projects only
└── package.json
```

---

## 8. tsconfig adjustments

Vite's `react-ts` template generates a split `tsconfig.json` /
`tsconfig.node.json`. Apply these changes to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Then add the alias to `vite.config.ts` so Vite resolves it at build time:

```ts
import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

> The `@/` alias keeps showcase template import paths identical to the
> Next.js variant, so templates ship a single set of import statements.

---

## 9. Verification

Before advancing to Phase 4:

```bash
# TypeScript check (TS projects only)
npx tsc --noEmit

# Dev server smoke test
<package-manager> run dev
```

Expected output:
- `tsc --noEmit` exits 0.
- Vite reports `Local: http://localhost:5173/` (default Vite port).
- Browser shows a blank page or the Vite default — both are fine at this stage.

> Note: React + Vite defaults to port **5173**, not 3000. Adjust any
> port-specific instructions in Phase 7 accordingly. To align with the
> other frameworks, add `server: { port: 3000 }` to `vite.config.ts`
> if the user prefers a consistent port.
