# HeroUI — Integration Reference

## Overview

HeroUI (formerly NextUI) is a React-only UI component library built on top of React Aria and Tailwind CSS. It ships components with built-in accessibility, motion, and theming out of the box.

- **Package**: `@heroui/react` (monorepo — each component is also its own scoped package)
- **Version**: v2.x
- **Foundation**: React Aria (WAI-ARIA) + Tailwind CSS v3/v4
- **Framework support**: React 18+ / Next.js — **no Vue or Svelte package**

## Install

```bash
npm install @heroui/react framer-motion
```

`framer-motion` is a **required peer dependency** — installation will fail or components will error at runtime without it.

## Tailwind config

HeroUI ships a `heroui()` Tailwind plugin. Register it and add the dist paths to `content`:

```ts
// tailwind.config.ts
import { heroui } from "@heroui/react";
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    // Required — HeroUI theme dist contains utility classes
    "./node_modules/@heroui/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  plugins: [heroui()],
};

export default config;
```

## Provider setup (Next.js App Router)

Create `app/providers.tsx` as a Client Component:

```tsx
// app/providers.tsx
"use client";

import { useRouter } from "next/navigation";
import { HeroUIProvider } from "@heroui/react";
import type { ReactNode } from "react";

export function Providers({ children }: { children: ReactNode }) {
  const router = useRouter();

  return (
    // className="h-full" prevents layout shifts
    // navigate prop enables HeroUI Link components to use Next.js router
    <HeroUIProvider className="h-full" navigate={router.push}>
      {children}
    </HeroUIProvider>
  );
}
```

Then wrap your root layout:

```tsx
// app/layout.tsx
import { Providers } from "./providers";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Dark mode bridge

HeroUI reads the `dark` class on `<html>`. The skill's `ThemeProvider` toggles `className="dark"` on `<html>`, so dark mode works automatically — no extra configuration needed.

Ensure the `<html>` tag does **not** suppress the class during SSR. The `HeroUIProvider` must receive `className="h-full"` to avoid layout issues in App Router.

## CSS variable bridge

HeroUI has its own design token system. Map the skill's `--color-accent-*` palette to HeroUI's `primary` color scale via the `theme` prop on `HeroUIProvider`:

```tsx
import { HeroUIProvider } from "@heroui/react";

// Map skill accent tokens to HeroUI primary scale
const heroTheme = {
  extend: {
    colors: {
      primary: {
        50:  "hsl(var(--color-accent-50) / <alpha-value>)",
        100: "hsl(var(--color-accent-100) / <alpha-value>)",
        200: "hsl(var(--color-accent-200) / <alpha-value>)",
        300: "hsl(var(--color-accent-300) / <alpha-value>)",
        400: "hsl(var(--color-accent-400) / <alpha-value>)",
        500: "hsl(var(--color-accent-500) / <alpha-value>)",
        600: "hsl(var(--color-accent-600) / <alpha-value>)",
        700: "hsl(var(--color-accent-700) / <alpha-value>)",
        800: "hsl(var(--color-accent-800) / <alpha-value>)",
        900: "hsl(var(--color-accent-900) / <alpha-value>)",
        DEFAULT: "hsl(var(--color-accent-500) / <alpha-value>)",
        foreground: "#ffffff",
      },
    },
  },
};

<HeroUIProvider theme={heroTheme}>
  {children}
</HeroUIProvider>
```

## React-only constraint

HeroUI has no Vue or Svelte package. For Vue projects use PrimeVue, Element Plus, or Vuetify. For SvelteKit use DaisyUI or a custom Tailwind approach.

## Component map

| Skill slot | HeroUI component | Import path |
|---|---|---|
| Button | `<Button>` | `@heroui/button` |
| Input | `<Input>` | `@heroui/input` |
| Textarea | `<Textarea>` | `@heroui/input` |
| Select | `<Select>` + `<SelectItem>` | `@heroui/select` |
| Checkbox | `<Checkbox>` | `@heroui/checkbox` |
| RadioGroup | `<RadioGroup>` + `<Radio>` | `@heroui/radio` |
| Switch | `<Switch>` | `@heroui/switch` |
| Card | `<Card>` + `<CardHeader>` + `<CardBody>` + `<CardFooter>` | `@heroui/card` |
| Badge | `<Badge>` | `@heroui/badge` |
| Avatar | `<Avatar>` | `@heroui/avatar` |
| Separator/Divider | `<Divider>` | `@heroui/divider` |
| Skeleton | `<Skeleton>` | `@heroui/skeleton` |
| Table | `<Table>` + `<TableHeader>` + `<TableColumn>` + `<TableBody>` + `<TableRow>` + `<TableCell>` | `@heroui/table` |
| Alert | plain `<div role="alert">` + Tailwind | — |
| Toast | state-managed queue + Tailwind | — |
| Progress | `<Progress>` | `@heroui/progress` |
| Tooltip | `<Tooltip>` | `@heroui/tooltip` |
| Dialog/Modal | `<Modal>` + `<ModalContent>` + `<ModalHeader>` + `<ModalBody>` + `<ModalFooter>` | `@heroui/modal` |
| Tabs | `<Tabs>` + `<Tab>` | `@heroui/tabs` |
| Breadcrumb | `<Breadcrumbs>` + `<BreadcrumbItem>` | `@heroui/breadcrumbs` |
| Pagination | `<Pagination>` | `@heroui/pagination` |
| NavigationMenu | `<Navbar>` + `<NavbarContent>` + `<NavbarItem>` | `@heroui/navbar` |
| Popover | `<Popover>` + `<PopoverTrigger>` + `<PopoverContent>` | `@heroui/popover` |
| DropdownMenu | `<Dropdown>` + `<DropdownTrigger>` + `<DropdownMenu>` + `<DropdownItem>` | `@heroui/dropdown` |
| Sheet/Drawer | `<Drawer>` + `<DrawerContent>` + `<DrawerHeader>` + `<DrawerBody>` + `<DrawerFooter>` | `@heroui/drawer` |
| Chart | `recharts` (no native HeroUI chart) | `recharts` |
| DataTable | `<Table>` with sort state | `@heroui/table` |
| Calendar | `<Calendar>` or `<DatePicker>` | `@heroui/date-picker` |

> **Note**: All components are also re-exported from `@heroui/react` — importing from there instead of individual packages is simpler and works equally well.

## Key API snippets

### Button variants

```tsx
import { Button } from "@heroui/react";

// color prop, not variant
<Button color="primary">Primary</Button>
<Button color="primary" variant="bordered">Bordered</Button>
<Button color="primary" variant="light">Light</Button>
<Button color="primary" variant="flat">Flat</Button>
<Button color="primary" variant="ghost">Ghost</Button>
<Button color="danger">Danger</Button>
<Button isDisabled>Disabled</Button>
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
<Button isLoading>Loading</Button>
```

### Input with validation

```tsx
import { Input } from "@heroui/react";

<Input
  label="Email"
  placeholder="you@example.com"
  type="email"
  isInvalid={!!error}
  errorMessage={error}
  description="We'll never share your email."
/>
```

### Select

```tsx
import { Select, SelectItem } from "@heroui/react";

const frameworks = ["Next.js", "Remix", "Astro", "SvelteKit"];

<Select label="Framework" placeholder="Select a framework">
  {frameworks.map((fw) => (
    <SelectItem key={fw}>{fw}</SelectItem>
  ))}
</Select>
```

### Checkbox

```tsx
import { Checkbox } from "@heroui/react";

<Checkbox defaultSelected color="primary">
  Accept terms and conditions
</Checkbox>
```

### RadioGroup

```tsx
import { Radio, RadioGroup } from "@heroui/react";

<RadioGroup label="Plan" color="primary" defaultValue="free">
  <Radio value="free">Free</Radio>
  <Radio value="pro">Pro</Radio>
  <Radio value="enterprise">Enterprise</Radio>
</RadioGroup>
```

### Switch

```tsx
import { Switch } from "@heroui/react";

<Switch defaultSelected color="primary">
  Email notifications
</Switch>
```

### Modal

```tsx
import { useDisclosure, Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button } from "@heroui/react";

export function Example() {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <>
      <Button onPress={onOpen}>Open Modal</Button>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalContent>
          <ModalHeader>Delete project?</ModalHeader>
          <ModalBody>
            <p>This action cannot be undone.</p>
          </ModalBody>
          <ModalFooter>
            <Button variant="light" onPress={onClose}>Cancel</Button>
            <Button color="danger" onPress={onClose}>Delete</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}
```

### Tabs

```tsx
import { Tabs, Tab } from "@heroui/react";

<Tabs color="primary" aria-label="Settings tabs">
  <Tab key="account" title="Account">Account content</Tab>
  <Tab key="billing" title="Billing">Billing content</Tab>
  <Tab key="security" title="Security">Security content</Tab>
</Tabs>
```

### Dropdown

```tsx
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem, Button } from "@heroui/react";

<Dropdown>
  <DropdownTrigger>
    <Button variant="bordered">Options</Button>
  </DropdownTrigger>
  <DropdownMenu aria-label="Actions">
    <DropdownItem key="profile">Profile</DropdownItem>
    <DropdownItem key="settings">Settings</DropdownItem>
    <DropdownItem key="logout" color="danger" className="text-danger">
      Sign out
    </DropdownItem>
  </DropdownMenu>
</Dropdown>
```

### Tooltip

```tsx
import { Tooltip, Button } from "@heroui/react";

<Tooltip content="This is a tooltip" color="primary">
  <Button variant="bordered">Hover me</Button>
</Tooltip>
```

## Gotchas

- **framer-motion is required** — `npm install framer-motion` alongside `@heroui/react` or components will throw at runtime.
- **Each component is its own scoped package** (`@heroui/button`, `@heroui/input`, etc.) — use `@heroui/react` to import everything from one place.
- **`HeroUIProvider` must be a Client Component** in Next.js App Router — wrap it in a `"use client"` file and import that from the server root layout.
- **Tailwind content path is required** — add `./node_modules/@heroui/theme/dist/**/*.{js,ts,jsx,tsx}` to `content` or utility classes will be purged.
- **`color` prop, not `variant`** — HeroUI uses `color="primary"` for colour variants. `variant` controls shape/style (filled, bordered, light, flat, ghost, shadow).
- **Size values** — `"sm"`, `"md"`, `"lg"` only. No `"xs"` or `"xl"`.
- **`useDisclosure`** — the canonical hook for controlling Modal, Popover, and Dropdown open state. Import from `@heroui/react`.
- **Drawer** is available in `@heroui/drawer` (v2.6+). For older versions use Modal with `placement="bottom"` or a custom slide-in Dialog.
