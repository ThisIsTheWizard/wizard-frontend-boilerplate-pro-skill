# Material UI Integration Reference

## Overview

Material UI (MUI) is a comprehensive React component library implementing Google's Material Design. All components are self-contained; no CLI copy-paste step is required. MUI ships its own styling engine (Emotion) and theming system (`createTheme` / `ThemeProvider`), which requires a bridge layer to align with the skill's CSS variable token system.

**React only.** MUI has no official Vue or Svelte port. Select `mui` only when `FRAMEWORK` is `nextjs` or `react-vite`.

---

## Install

### React / Vite

```bash
npm install @mui/material @emotion/react @emotion/styled
```

### Next.js 15 (App Router + SSR)

```bash
npm install @mui/material @emotion/react @emotion/styled @mui/material-nextjs @emotion/cache
```

> `@mui/material-nextjs` patches `AppRouterCacheProvider`, which prevents Emotion from injecting duplicate style tags during streaming SSR. Place it once in the root layout.

---

## Root layout wiring (Next.js App Router)

`app/layout.tsx`:

```tsx
import { AppRouterCacheProvider } from "@mui/material-nextjs/v15-appRouter";
import type { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppRouterCacheProvider>
          {children}
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
```

> The skill's `ThemeProvider` (from `assets/theme-provider/react.tsx`) must be nested inside `AppRouterCacheProvider` but outside the page content. Place it in the library layout template — see `assets/showcase-templates/react-mui/layout.tsx.template`.

---

## Theme bridge — `createTheme()` mapping

MUI's styling engine does not resolve CSS variables at theme-creation time; you must pass resolved color values. The bridge reads the skill's semantic token values (which are OKLCH) from the compiled stylesheet via a CSS-level trick: attach a temporary element, read its `background-color`, and pass the RGB/hex result to `createTheme`.

For most projects, providing mode-appropriate fallback values is sufficient. Customise once to match the active preset.

### `src/lib/muiTheme.ts`

```ts
import { createTheme } from "@mui/material/styles";

function readCssVar(varName: string, fallback: string): string {
  if (typeof window === "undefined") return fallback;
  const el = document.createElement("div");
  el.style.cssText = `position:absolute;visibility:hidden;background-color:var(${varName})`;
  document.body.appendChild(el);
  const value = getComputedStyle(el).backgroundColor;
  document.body.removeChild(el);
  return value || fallback;
}

export function buildMuiTheme(mode: "dark" | "light") {
  return createTheme({
    palette: {
      mode,
      primary: {
        main: readCssVar(
          "--color-accent-500",
          mode === "dark" ? "#818cf8" : "#4f46e5",
        ),
        contrastText: "#ffffff",
      },
      background: {
        default: readCssVar(
          "--background",
          mode === "dark" ? "#0a0a0a" : "#fafafa",
        ),
        paper: readCssVar(
          "--surface",
          mode === "dark" ? "#171717" : "#ffffff",
        ),
      },
      text: {
        primary: readCssVar(
          "--foreground",
          mode === "dark" ? "#fafafa" : "#0a0a0a",
        ),
        secondary: readCssVar(
          "--muted-foreground",
          mode === "dark" ? "#a3a3a3" : "#737373",
        ),
      },
      divider: readCssVar(
        "--border",
        mode === "dark" ? "#262626" : "#e5e5e5",
      ),
      error: {
        main: readCssVar("--destructive", "#ef4444"),
      },
    },
    shape: { borderRadius: 8 },
    typography: {
      fontFamily: "inherit",
      button: { textTransform: "none" },
    },
    components: {
      MuiButton: {
        defaultProps: { disableElevation: true },
      },
      MuiAppBar: {
        defaultProps: { elevation: 0 },
      },
      MuiCard: {
        defaultProps: { elevation: 0 },
        styleOverrides: {
          root: {
            border: "1px solid",
            borderColor: "var(--border)",
          },
        },
      },
    },
  });
}
```

> `readCssVar` runs client-side only. Use `useMemo` in the layout component and re-run when `mode` changes.

---

## Token mapping table

| Skill CSS token | MUI palette key | Notes |
|---|---|---|
| `--color-accent-500` | `palette.primary.main` | Brand colour |
| `--background` | `palette.background.default` | Page background |
| `--surface` | `palette.background.paper` | Cards, drawers |
| `--foreground` | `palette.text.primary` | Body text |
| `--muted-foreground` | `palette.text.secondary` | Secondary text |
| `--border` | `palette.divider` | Dividers, outlines |
| `--destructive` | `palette.error.main` | Error state |
| `--radius` | `shape.borderRadius` | Mapped as number (px) |

---

## Dark mode

The skill's `useTheme()` hook manages `light`/`dark` state and the `.dark` class on `<html>`. The MUI layout template reads `theme` from `useTheme()`, maps it to MUI's `mode`, and rebuilds the MUI theme via `useMemo`. `CssBaseline` from MUI applies `palette.background.default` to `<body>`.

```tsx
const { theme } = useTheme();
const mode = theme === "dark" ? "dark" : "light";
const muiTheme = useMemo(() => buildMuiTheme(mode), [mode]);

return (
  <ThemeProvider theme={muiTheme}>
    <CssBaseline />
    {children}
  </ThemeProvider>
);
```

---

## Component coverage map

| Skill slot | shadcn equivalent | MUI equivalent | Package |
|---|---|---|---|
| Button | `Button` | `Button` | `@mui/material` |
| Input | `Input` + `Label` | `TextField` | `@mui/material` |
| Textarea | `Textarea` | `TextField multiline` | `@mui/material` |
| Select | `Select` sub-components | `TextField select` or `Select` + `MenuItem` | `@mui/material` |
| Checkbox | `Checkbox` + `Label` | `FormControlLabel` + `Checkbox` | `@mui/material` |
| RadioGroup | `RadioGroup` + `RadioGroupItem` | `RadioGroup` + `FormControlLabel` + `Radio` | `@mui/material` |
| Switch | `Switch` + `Label` | `FormControlLabel` + `Switch` | `@mui/material` |
| Card | `Card` sub-components | `Card`, `CardHeader`, `CardContent`, `CardActions` | `@mui/material` |
| Badge | `Badge` | `Chip` | `@mui/material` |
| Avatar | `Avatar` sub-components | `Avatar` | `@mui/material` |
| Separator | `Separator` | `Divider` | `@mui/material` |
| Skeleton | `Skeleton` | `Skeleton` | `@mui/material` |
| Table | `Table` sub-components | `Table`, `TableHead`, `TableBody`, `TableRow`, `TableCell` | `@mui/material` |
| Alert | `Alert` + `AlertTitle` | `Alert` + `AlertTitle` | `@mui/material` |
| Toast | `sonner` | `Snackbar` + `Alert` | `@mui/material` |
| Progress | `Progress` | `LinearProgress` | `@mui/material` |
| Tooltip | `Tooltip` sub-components | `Tooltip` | `@mui/material` |
| Dialog | `Dialog` sub-components | `Dialog`, `DialogTitle`, `DialogContent`, `DialogActions` | `@mui/material` |
| Tabs | `Tabs` + `TabsList` + `TabsTrigger` | `Tabs` + `Tab` | `@mui/material` |
| Breadcrumb | `Breadcrumb` sub-components | `Breadcrumbs` + `Link` | `@mui/material` |
| Pagination | `Pagination` sub-components | `Pagination` | `@mui/material` |
| NavigationMenu | `NavigationMenu` sub-components | `AppBar` + `Toolbar` + `Button` | `@mui/material` |
| Popover | `Popover` sub-components | `Popover` | `@mui/material` |
| DropdownMenu | `DropdownMenu` sub-components | `Menu` + `MenuItem` | `@mui/material` |
| Sheet | `Sheet` sub-components | `Drawer` (anchor="right") | `@mui/material` |
| Chart | `ChartContainer` (recharts) | recharts directly | `recharts` |
| DataTable | `DataTable` (TanStack) | MUI `Table` or `DataGrid` | `@mui/material` / `@mui/x-data-grid` |
| Calendar | `Calendar` (react-day-picker) | `DateCalendar` | `@mui/x-date-pickers` + `date-fns` |

> **`@mui/x-data-grid`** and **`@mui/x-date-pickers`** are separate packages from MUI X. Install as needed:
> ```bash
> npm install @mui/x-data-grid @mui/x-date-pickers date-fns
> ```

---

## No-Tailwind note

MUI manages all component styling via Emotion internally. Tailwind utility classes are **not** applied to MUI components — use the `sx` prop or `styled()` instead. Tailwind utility classes remain available for non-MUI layout wrappers (flexbox, grid, spacing on container divs).

---

## Graceful fallback

If MUI installation fails (network issues, version conflicts), fall back to `references/ui-library/custom-tailwind.md`. The page templates will differ, but the `/library` route structure and sidebar navigation are unchanged.
