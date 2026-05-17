# Chakra UI v3 Integration Reference

## Overview

Chakra UI v3 is a React-only component library with a built-in design system. It ships a single unified package (`@chakra-ui/react`) that includes all components, theming utilities, and a CSS-in-JS engine. No CLI copy-paste step is required; components are installed and used directly.

**React only.** Chakra UI has no official Vue or Svelte port. Select `chakra` only when `FRAMEWORK` is `nextjs` or `react-vite`.

---

## Install

```bash
npm install @chakra-ui/react
```

> Chakra UI v3 is a single-package install. No separate Emotion or theme package is required — the new version uses its own CSS engine.

---

## Root layout wiring (Next.js App Router)

`app/layout.tsx`:

```tsx
import { ChakraProvider } from "@chakra-ui/react";
import type { ReactNode } from "react";

import { chakraSystem } from "@/lib/chakraSystem";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ChakraProvider value={chakraSystem}>
          {children}
        </ChakraProvider>
      </body>
    </html>
  );
}
```

> The skill's `ThemeProvider` (from `assets/theme-provider/react.tsx`) must be nested inside `ChakraProvider`. Place it in the library layout template — see `assets/showcase-templates/react-chakra/layout.tsx.template`.

---

## Theme bridge — `createSystem()` / `defineConfig()` mapping

Chakra UI v3 introduces a new theming API based on `createSystem` and `defineConfig`. The bridge maps the skill's CSS variable token system directly to Chakra design tokens. Because Chakra v3 supports CSS variable values in token definitions, no runtime DOM reading is required — the tokens resolve at render time using the browser's computed style.

### `src/lib/chakraSystem.ts`

```ts
import {
  createSystem,
  defaultConfig,
  defineConfig,
} from "@chakra-ui/react";

export const chakraSystem = createSystem(
  defaultConfig,
  defineConfig({
    globalCss: {
      body: {
        bg: "var(--background)",
        color: "var(--foreground)",
      },
    },
    theme: {
      semanticTokens: {
        colors: {
          "chakra-body-bg": { value: "var(--background)" },
          "chakra-body-text": { value: "var(--foreground)" },
          "chakra-border-color": { value: "var(--border)" },
          "chakra-subtle-bg": { value: "var(--surface)" },
          "chakra-subtle-text": { value: "var(--muted-foreground)" },
        },
      },
      tokens: {
        colors: {
          brand: {
            50: { value: "var(--color-accent-50)" },
            100: { value: "var(--color-accent-100)" },
            200: { value: "var(--color-accent-200)" },
            300: { value: "var(--color-accent-300)" },
            400: { value: "var(--color-accent-400)" },
            500: { value: "var(--color-accent-500)" },
            600: { value: "var(--color-accent-600)" },
            700: { value: "var(--color-accent-700)" },
            800: { value: "var(--color-accent-800)" },
            900: { value: "var(--color-accent-900)" },
            950: { value: "var(--color-accent-950)" },
          },
        },
      },
    },
  }),
);
```

> Use `colorPalette="brand"` on Chakra components to apply the brand colour. The token bridge keeps the palette in sync with the active skill preset automatically.

---

## Token mapping table

| Skill CSS token | Chakra semantic token | Notes |
|---|---|---|
| `--color-accent-500` | `brand.500` (via token) | Brand colour via `colorPalette="brand"` |
| `--background` | `chakra-body-bg` | Page background |
| `--surface` | `chakra-subtle-bg` | Cards, drawers |
| `--foreground` | `chakra-body-text` | Body text |
| `--muted-foreground` | `chakra-subtle-text` | Secondary text |
| `--border` | `chakra-border-color` | Dividers, outlines |
| `--destructive` | `red.500` (fallback) | Error state — no semantic token mapping |
| `--radius` | Not directly mapped | Use inline `borderRadius` on components |

---

## Dark mode

Chakra UI v3 integrates with a `ColorModeProvider` for dark/light mode switching. The skill's `useTheme()` hook manages the `.dark` class on `<html>`. Because the Chakra token bridge maps all colours to CSS variables, the `.dark` class automatically switches the resolved values — Chakra components stay in sync without requiring an explicit `colorMode` prop.

For projects that want Chakra's built-in colour mode utilities:

```tsx
// In layout.tsx — the forcedTheme approach keeps Chakra in sync with the skill's theme state
import { useTheme } from "@/components/ThemeProvider";

const { theme } = useTheme();

// Pass forcedTheme to ColorModeProvider if using Chakra's useColorMode hook internally
// Otherwise, the .dark class on <html> is sufficient via CSS variable resolution.
```

> The skill's CSS variables switch on `.dark` automatically. The Chakra system reads those variables at render time, so no `colorMode` prop is needed on individual components.

---

## Component coverage map

| Skill slot | Chakra v3 equivalent | Package |
|---|---|---|
| Button | `Button` with `colorPalette` | `@chakra-ui/react` |
| Input + Label | `Field.Root` + `Input` | `@chakra-ui/react` |
| Textarea | `Field.Root` + `Textarea` | `@chakra-ui/react` |
| Select | `Select.Root` + sub-components | `@chakra-ui/react` |
| Checkbox | `Checkbox.Root` + sub-components | `@chakra-ui/react` |
| RadioGroup | `RadioGroup.Root` + sub-components | `@chakra-ui/react` |
| Switch | `Switch.Root` + sub-components | `@chakra-ui/react` |
| Card | `Card.Root` + sub-components | `@chakra-ui/react` |
| Badge | `Badge` | `@chakra-ui/react` |
| Avatar | `Avatar.Root` + sub-components | `@chakra-ui/react` |
| Separator | `Separator` | `@chakra-ui/react` |
| Skeleton | `Skeleton` | `@chakra-ui/react` |
| Table | `Table.Root` + sub-components | `@chakra-ui/react` |
| Alert | `Alert.Root` + sub-components | `@chakra-ui/react` |
| Toast | `Toaster` + `createToaster` | `@chakra-ui/react` |
| Progress | `Progress.Root` + sub-components | `@chakra-ui/react` |
| Tooltip | `Tooltip.Root` + sub-components | `@chakra-ui/react` |
| Dialog | `Dialog.Root` + sub-components | `@chakra-ui/react` |
| Tabs | `Tabs.Root` + sub-components | `@chakra-ui/react` |
| Breadcrumb | `Breadcrumb.Root` + sub-components | `@chakra-ui/react` |
| Pagination | `Pagination.Root` + sub-components | `@chakra-ui/react` |
| NavigationMenu | `Box` + `Button` (custom header) | `@chakra-ui/react` |
| Popover | `Popover.Root` + sub-components | `@chakra-ui/react` |
| DropdownMenu | `Menu.Root` + sub-components | `@chakra-ui/react` |
| Sheet | `Drawer.Root` (placement="end") + sub-components | `@chakra-ui/react` |
| Chart | recharts directly | `recharts` |
| DataTable | Chakra `Table` + TanStack Table | `@chakra-ui/react` + `@tanstack/react-table` |
| Calendar | `react-day-picker` | `react-day-picker` |

> **recharts** and **react-day-picker** require separate installs:
> ```bash
> npm install recharts react-day-picker
> ```
> **@tanstack/react-table** for the sortable DataTable:
> ```bash
> npm install @tanstack/react-table
> ```

---

## Compound component API note

Chakra UI v3 uses a compound component API for most complex components (e.g. `Select.Root`, `Select.Trigger`, `Select.Content`, `Select.Item`). This is similar to shadcn/ui's pattern and differs from MUI's monolithic component approach. Each sub-component has a specific role and must be composed in the documented order.

---

## Graceful fallback

If Chakra UI installation fails (network issues, version conflicts), fall back to `references/ui-library/custom-tailwind.md`. The page templates will differ, but the `/library` route structure and sidebar navigation are unchanged.
