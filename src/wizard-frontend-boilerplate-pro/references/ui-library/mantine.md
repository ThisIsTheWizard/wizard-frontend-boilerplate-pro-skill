# Mantine v7 Integration Reference

## Overview

Mantine v7 is a React-only component library with a native CSS variables engine, full dark-mode support, and a rich built-in component set. It ships as `@mantine/core` with optional packages for notifications, dates, forms, and charts.

**React only.** Mantine has no official Vue or Svelte port. Select `mantine` only when `FRAMEWORK` is `nextjs` or `react-vite`.

---

## Install

```bash
npm install @mantine/core @mantine/hooks
```

For notifications (Toast slot):

```bash
npm install @mantine/notifications
```

For data viz extras:

```bash
npm install recharts react-day-picker @tanstack/react-table
```

---

## Required CSS imports

Add both style imports to the root layout **before** any custom CSS. Mantine's styles must load first so per-component overrides work.

`app/layout.tsx` (Next.js App Router) or `src/main.tsx` (Vite):

```ts
import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css"; // only if using notifications
```

---

## Root layout wiring (Next.js App Router)

`app/layout.tsx`:

```tsx
import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";

import { ColorSchemeScript, MantineProvider } from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import type { ReactNode } from "react";

import { mantineTheme } from "@/lib/mantineTheme";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        {/* Prevents FOUC on first load — must be in <head> */}
        <ColorSchemeScript defaultColorScheme="auto" />
      </head>
      <body>
        <MantineProvider theme={mantineTheme}>
          <Notifications />
          {children}
        </MantineProvider>
      </body>
    </html>
  );
}
```

> The skill's `ThemeProvider` (from `assets/theme-provider/react.tsx`) drives the `.dark` class on `<html>`. The library layout template bridges this into Mantine's `forceColorScheme` prop — see `assets/showcase-templates/react-mantine/layout.tsx.template`.

---

## Theme bridge — `createTheme()` mapping

Mantine v7 resolves all colour tokens via CSS variables at render time, making the bridge straightforward. Pass CSS variable references as colour scale values; the browser resolves them against the active theme.

### `src/lib/mantineTheme.ts`

```ts
import { createTheme, type MantineColorsTuple } from "@mantine/core";

const brandColors: MantineColorsTuple = [
  "var(--color-accent-50)",
  "var(--color-accent-100)",
  "var(--color-accent-200)",
  "var(--color-accent-300)",
  "var(--color-accent-400)",
  "var(--color-accent-500)",
  "var(--color-accent-600)",
  "var(--color-accent-700)",
  "var(--color-accent-800)",
  "var(--color-accent-900)",
];

export const mantineTheme = createTheme({
  colors: {
    brand: brandColors,
  },
  primaryColor: "brand",
  primaryShade: { dark: 4, light: 5 },
  defaultRadius: "md",
  fontFamily: "inherit",
});
```

> `MantineColorsTuple` requires exactly 10 values (indices 0–9). Index 5 is treated as the primary shade in light mode; index 4 in dark mode — matching the `primaryShade` config above.

---

## Dark mode bridge

Mantine's `MantineProvider` accepts a `forceColorScheme` prop (`"light"` | `"dark"`). Bridge the skill's `useTheme()` hook by passing the current theme:

```tsx
// Inside the library layout (app/library/layout.tsx)
"use client";

import { MantineProvider } from "@mantine/core";
import { useTheme } from "@/components/ThemeProvider";

export default function LibraryLayout({ children }) {
  const { theme } = useTheme();

  return (
    <MantineProvider theme={mantineTheme} forceColorScheme={theme}>
      {children}
    </MantineProvider>
  );
}
```

> The `forceColorScheme` prop overrides Mantine's internal `colorScheme` state, keeping it in sync with the skill's `.dark` class mechanism. Components respond to this prop immediately without requiring `useComputedColorScheme` or manual class reads.

---

## Token mapping table

| Skill CSS token | Mantine equivalent | Notes |
|---|---|---|
| `--color-accent-500` | `brand.5` | Primary action colour |
| `--color-accent-100` | `brand.1` | Subtle backgrounds |
| `--background` | N/A | Use inline `style` or CSS vars on container |
| `--surface` | N/A | Use inline `style` on `Card`, `Paper` |
| `--foreground` | N/A | Mantine manages text colours via `colorScheme` |
| `--muted-foreground` | `dimmed` prop on `Text` | `<Text c="dimmed">` |
| `--border` | N/A | Use inline `style` on `Divider` or containers |
| `--destructive` | `red.6` | `color="red"` on error-state components |

> Mantine manages most semantic colours internally via its own CSS variable system. The brand colour is the key integration point — everything else falls through to Mantine's defaults, which adapt correctly to `forceColorScheme`.

---

## Component coverage map

| Skill slot | Mantine v7 equivalent | Package |
|---|---|---|
| Button | `Button` with `variant` | `@mantine/core` |
| Input + Label | `TextInput` | `@mantine/core` |
| Textarea | `Textarea` | `@mantine/core` |
| Select | `Select` | `@mantine/core` |
| Checkbox | `Checkbox` | `@mantine/core` |
| RadioGroup | `Radio.Group` + `Radio` | `@mantine/core` |
| Switch | `Switch` | `@mantine/core` |
| Card | `Card` + `Card.Section` | `@mantine/core` |
| Badge | `Badge` | `@mantine/core` |
| Avatar | `Avatar` | `@mantine/core` |
| Separator | `Divider` | `@mantine/core` |
| Skeleton | `Skeleton` | `@mantine/core` |
| Table | `Table` + sub-components | `@mantine/core` |
| Alert | `Alert` | `@mantine/core` |
| Toast | `notifications.show()` + `<Notifications />` | `@mantine/notifications` |
| Progress | `Progress` | `@mantine/core` |
| Tooltip | `Tooltip` | `@mantine/core` |
| Dialog | `Modal` | `@mantine/core` |
| Tabs | `Tabs` + sub-components | `@mantine/core` |
| Breadcrumb | `Breadcrumbs` + `Anchor` | `@mantine/core` |
| Pagination | `Pagination` | `@mantine/core` |
| NavigationMenu | `NavLink` + custom layout | `@mantine/core` |
| Popover | `Popover` + sub-components | `@mantine/core` |
| DropdownMenu | `Menu` + sub-components | `@mantine/core` |
| Sheet | `Drawer` with `position="right"` | `@mantine/core` |
| Chart | recharts directly | `recharts` |
| DataTable | Mantine `Table` + TanStack Table | `@mantine/core` + `@tanstack/react-table` |
| Calendar | `react-day-picker` | `react-day-picker` |

---

## Notification (Toast) setup

Mantine uses a notification system from `@mantine/notifications`:

```tsx
// 1. Mount <Notifications /> once in root layout (inside MantineProvider)
import { Notifications } from "@mantine/notifications";

// 2. Trigger from any component
import { notifications } from "@mantine/notifications";

notifications.show({
  title: "Success",
  message: "Your changes have been saved.",
  color: "green",
});
```

---

## Peer deps per component category

| Category | Extra install |
|---|---|
| Notifications / Toast | `npm install @mantine/notifications` |
| Charts (recharts) | `npm install recharts` |
| DataTable (sort) | `npm install @tanstack/react-table` |
| Calendar | `npm install react-day-picker` |

---

## Graceful fallback

If Mantine installation fails (network issues, version conflicts), fall back to `references/ui-library/custom-tailwind.md`. The `/library` route structure and sidebar navigation are unchanged — only the component implementations differ.
