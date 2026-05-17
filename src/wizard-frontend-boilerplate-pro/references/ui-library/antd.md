# Ant Design v5 Integration Reference

## Overview

Ant Design v5 is a React-only component library providing an enterprise-grade design system with hundreds of components and a CSS-in-JS token engine via `ConfigProvider`.

**React only.** Ant Design has no official Vue or Svelte port. Select `antd` only when `FRAMEWORK` is `nextjs` or `react-vite`.

---

## Install

```bash
npm install antd @ant-design/icons
```

For Next.js App Router SSR cache (prevents CSS-in-JS flash on first load):

```bash
npm install @ant-design/nextjs-registry
```

For data viz extras:

```bash
npm install recharts
```

> DataTable sorting is built into antd's `Table` component — no `@tanstack/react-table` needed.
> DatePicker uses `dayjs` which antd bundles internally — no extra install needed.

---

## Next.js App Router setup

Ant Design uses CSS-in-JS which requires a server-side style cache to prevent FOUC.

`app/layout.tsx`:

```tsx
import { AntdRegistry } from "@ant-design/nextjs-registry";
import type { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AntdRegistry>{children}</AntdRegistry>
      </body>
    </html>
  );
}
```

The library layout (`app/library/layout.tsx`) wraps content in `ConfigProvider` — see `assets/showcase-templates/react-antd/layout.tsx.template`.

---

## ConfigProvider — theme token bridge

Ant Design v5 design tokens are passed to `ConfigProvider`. The skill's active accent colour is read from the CSS variable at mount time and passed as `colorPrimary`.

### Reading the accent colour

```ts
function useAccentColor(fallback = "#0ea5e9"): string {
  const [color, setColor] = useState(fallback);

  useEffect(() => {
    const value = getComputedStyle(document.documentElement)
      .getPropertyValue("--color-accent-500")
      .trim();
    if (value) setColor(value);
  }, []);

  return color;
}
```

### Full `app/library/layout.tsx`

```tsx
"use client";

import { useEffect, useState } from "react";
import type { ReactNode } from "react";

import { ConfigProvider, theme as antdTheme } from "antd";

import { useTheme } from "@/components/ThemeProvider";

function useAccentColor(fallback = "#0ea5e9"): string {
  const [color, setColor] = useState(fallback);

  useEffect(() => {
    const value = getComputedStyle(document.documentElement)
      .getPropertyValue("--color-accent-500")
      .trim();
    if (value) setColor(value);
  }, []);

  return color;
}

export default function LibraryLayout({ children }: { children: ReactNode }) {
  const { theme } = useTheme();
  const primaryColor = useAccentColor();

  return (
    <ConfigProvider
      theme={{
        algorithm:
          theme === "dark"
            ? antdTheme.darkAlgorithm
            : antdTheme.defaultAlgorithm,
        token: {
          borderRadius: 6,
          colorPrimary: primaryColor,
        },
      }}
    >
      {children}
    </ConfigProvider>
  );
}
```

---

## Dark mode bridge

Ant Design's `ConfigProvider` switches between light and dark via the `algorithm` token:

| Mode | Algorithm |
|---|---|
| Light | `theme.defaultAlgorithm` |
| Dark | `theme.darkAlgorithm` |

The skill's `ThemeProvider` drives the `.dark` class on `<html>`. Bridge it by reading `theme` from `useTheme()` and passing the matching algorithm to `ConfigProvider`.

> Unlike Mantine (`forceColorScheme`) or MUI (`mode`), antd uses an algorithm function rather than a named mode string.

---

## Token mapping table

| Skill CSS token | Ant Design token | Notes |
|---|---|---|
| `--color-accent-500` (hex) | `colorPrimary` | Read at mount with `getComputedStyle` |
| `--background` | `colorBgLayout` | Managed by `algorithm` |
| `--surface` | `colorBgContainer` | Managed by `algorithm` |
| `--foreground` | `colorText` | Managed by `algorithm` |
| `--muted-foreground` | `colorTextSecondary` | Use `<Typography.Text type="secondary">` |
| `--border` | `colorBorder` | Managed by `algorithm` |
| `--destructive` | `colorError` | Use `danger` prop on Button; `type="error"` on Alert |

> Ant Design manages most semantic colours internally via its token system. Only `colorPrimary` needs explicit bridging — everything else adapts when the algorithm switches.

---

## Component coverage map

| Skill slot | Ant Design equivalent | Package |
|---|---|---|
| Button | `Button` with `type` prop | `antd` |
| Input + Label | `Typography.Text` label + `Input` | `antd` |
| Textarea | `Input.TextArea` | `antd` |
| Select | `Select` with `options` | `antd` |
| Checkbox | `Checkbox` | `antd` |
| RadioGroup | `Radio.Group` + `Radio` | `antd` |
| Switch | `Switch` | `antd` |
| Card | `Card` | `antd` |
| Badge / Tag | `Tag` (labels) + `Badge` (count overlay) | `antd` |
| Avatar | `Avatar` | `antd` |
| Separator | `Divider` | `antd` |
| Skeleton | `Skeleton` | `antd` |
| Table | `Table` with `columns` + `dataSource` | `antd` |
| Alert | `Alert` with `type` | `antd` |
| Toast | `message.success/error/warning/info()` | `antd` |
| Progress | `Progress` | `antd` |
| Tooltip | `Tooltip` | `antd` |
| Dialog | `Modal` | `antd` |
| Tabs | `Tabs` with `items` array | `antd` |
| Breadcrumb | `Breadcrumb` with `items` array | `antd` |
| Pagination | `Pagination` | `antd` |
| NavigationMenu | `Menu` with `mode="inline"` | `antd` |
| Popover | `Popover` | `antd` |
| DropdownMenu | `Dropdown` with `menu.items` | `antd` |
| Sheet | `Drawer` with `placement="right"` | `antd` |
| Chart | recharts directly | `recharts` |
| DataTable | `Table` with `sorter` in columns | `antd` (built-in sorting) |
| Calendar | `DatePicker` | `antd` (dayjs bundled) |

---

## Toast (message) setup

Ant Design's `message` API uses a static method pattern. For full ConfigProvider theming (including dark mode), use `App.useApp()`:

```tsx
// Option 1: static (simpler, sufficient for most cases)
import { message } from "antd";
message.success("Saved successfully.");

// Option 2: hook (recommended for full ConfigProvider colour support)
// Wrap content in <App> inside ConfigProvider:
import { App } from "antd";

function MyComponent() {
  const { message } = App.useApp();
  message.success("Saved successfully.");
}
```

---

## Key v5 API differences from v4

| v4 prop | v5 replacement |
|---|---|
| `visible` on Modal/Drawer | `open` |
| `Select` option children | `options` array prop |
| `Tabs` with `TabPane` children | `Tabs` with `items` array |
| `Breadcrumb` with `Item` children | `Breadcrumb` with `items` array |
| `Table` `dataSource` row key `key` field | `rowKey` prop or `key` field |

---

## Peer deps per component category

| Category | Extra install |
|---|---|
| Next.js SSR cache | `npm install @ant-design/nextjs-registry` |
| Icons | `npm install @ant-design/icons` |
| Charts | `npm install recharts` |
| DataTable sorting | built-in (no extra package) |
| DatePicker / Calendar | built-in (dayjs bundled with antd) |

---

## Graceful fallback

If Ant Design installation fails (network issues, version conflicts), fall back to `references/ui-library/custom-tailwind.md`. The `/library` route structure and sidebar navigation are unchanged — only the component implementations differ.
