# shadcn/ui Integration Reference

## Overview

shadcn/ui is a collection of copy-paste components built on Radix UI primitives and styled with Tailwind CSS. The CLI installs component source files directly into `src/components/ui/`, giving full ownership. No runtime dependency on a separate package — components live in your repo.

## Framework support

| Framework | CLI package | Constraint |
|---|---|---|
| Next.js 15 / React 19 | `shadcn` (official) | React only |
| Vue 3.5 / Nuxt 4 | `shadcn-vue` (community) | Vue only |
| SvelteKit / Svelte 5 | `shadcn-svelte` (community) | Svelte only |

## CSS variable compatibility

shadcn/ui uses the same CSS variable naming convention as this skill's token system. No bridge is needed — `shadcn init` writes the same variables the token system already declares.

| Token | Used by both | Role |
|---|---|---|
| `--background` | ✓ | Page background |
| `--foreground` | ✓ | Primary text |
| `--card` / `--card-foreground` | ✓ | Card surface |
| `--popover` / `--popover-foreground` | ✓ | Floating elements |
| `--primary` / `--primary-foreground` | ✓ | Brand colour |
| `--secondary` / `--secondary-foreground` | ✓ | Secondary actions |
| `--muted` / `--muted-foreground` | ✓ | Subdued content |
| `--accent` / `--accent-foreground` | ✓ | Hover states |
| `--destructive` / `--destructive-foreground` | ✓ | Error states |
| `--border` | ✓ | Borders |
| `--input` | ✓ | Input borders |
| `--ring` | ✓ | Focus rings |
| `--radius` | ✓ | Border radius |
| `--chart-1` … `--chart-5` | shadcn only | Generated from palette by `generate_palette.py` |

When `shadcn init` asks **"Use CSS variables for theming?"**, answer **Yes**. The generated block will slot directly into the skill's `globals.css` without conflicts.

## Init commands

### React / Next.js
```bash
npx shadcn@latest init
```
Prompts: TypeScript → Yes, style → Default, base color → (match your primary), CSS variables → Yes, tailwind config path → (auto-detected), components alias → `@/components`, utils alias → `@/lib/utils`.

### Vue 3 / Nuxt
```bash
npx shadcn-vue@latest init
```

### SvelteKit
```bash
npx shadcn-svelte@latest init
```

## Adding all 28 components

### React / Next.js
```bash
npx shadcn@latest add \
  button input textarea select label checkbox radio-group switch \
  card badge avatar separator skeleton table \
  alert sonner progress tooltip dialog \
  tabs breadcrumb pagination navigation-menu \
  popover dropdown-menu sheet \
  chart calendar
```
> `DataTable` is a recipe, not a direct add. Follow https://ui.shadcn.com/docs/components/data-table — it installs the shadcn `Table` plus a TanStack Table wrapper you write once.

### Vue 3 / Nuxt
```bash
npx shadcn-vue@latest add \
  button input textarea select label checkbox radio-group switch \
  card badge avatar separator skeleton table \
  alert sonner progress tooltip dialog \
  tabs breadcrumb pagination navigation-menu \
  popover dropdown-menu sheet \
  chart calendar
```

### SvelteKit
```bash
npx shadcn-svelte@latest add \
  button input textarea select label checkbox radio-group switch \
  card badge avatar separator skeleton table \
  alert sonner progress tooltip dialog \
  tabs breadcrumb pagination navigation-menu \
  popover dropdown-menu sheet \
  chart calendar
```

## Per-framework API notes

### React (native shadcn)

**Import path:** `@/components/ui/<component>`  
**`cn()` utility:** `@/lib/utils`

Key API differences from the `custom-tailwind` fallback:

| Component | shadcn API |
|---|---|
| `Input` | No built-in `label`/`helperText` — compose with `Label` from `@/components/ui/label` |
| `Select` | Sub-components: `Select`, `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectItem` |
| `Checkbox` | No built-in `label` — pair `<Checkbox id="x" />` with `<Label htmlFor="x">` |
| `RadioGroup` | `RadioGroup` + `RadioGroupItem` + `Label` — no `options` array prop |
| `Switch` | No built-in `label` — pair with `<Label>` |
| `Avatar` | Sub-components: `Avatar`, `AvatarImage`, `AvatarFallback` — no `src`/`fallback` top-level props |
| `Progress` | Only `value` prop — no `label` or `indeterminate` |
| `Alert` | Variants: `default`, `destructive` — add `success`/`warning` variants via CVA if needed |
| `Tooltip` | Requires `TooltipProvider` wrapper (place in root layout) |

### Vue (shadcn-vue)

**Import path:** `@/components/ui/<component>`  
**`cn()` utility:** `@/lib/utils`

Component APIs mirror the React version, adapted for Vue template syntax. `v-model` is supported on form components. `TooltipProvider` wrapper required.

### Svelte (shadcn-svelte)

**Import path:** `$lib/components/ui/<component>`  
Uses Svelte 5 runes syntax (`$state`, `$props`). Sub-component APIs identical to React. `TooltipProvider` wrapper required.

## Peer deps by category

### Inputs

| Component | Radix primitive |
|---|---|
| Button | — |
| Input, Textarea | — |
| Label | `@radix-ui/react-label` |
| Select | `@radix-ui/react-select` |
| Checkbox | `@radix-ui/react-checkbox` |
| RadioGroup | `@radix-ui/react-radio-group` |
| Switch | `@radix-ui/react-switch` |

### Display

| Component | Radix primitive |
|---|---|
| Card, Badge, Skeleton, Table | — |
| Avatar | `@radix-ui/react-avatar` |
| Separator | `@radix-ui/react-separator` |

### Feedback

| Component | Radix primitive / package |
|---|---|
| Alert | — |
| Toast | `sonner` |
| Progress | `@radix-ui/react-progress` |
| Tooltip | `@radix-ui/react-tooltip` |
| Dialog | `@radix-ui/react-dialog` |

### Navigation

| Component | Radix primitive |
|---|---|
| Tabs | `@radix-ui/react-tabs` |
| Breadcrumb, Pagination | — |
| NavigationMenu | `@radix-ui/react-navigation-menu` |

### Overlay

| Component | Radix primitive |
|---|---|
| Popover | `@radix-ui/react-popover` |
| DropdownMenu | `@radix-ui/react-dropdown-menu` |
| Sheet | `@radix-ui/react-dialog` |

### Data viz

| Component | Package |
|---|---|
| Chart | `recharts` |
| DataTable | `@tanstack/react-table` |
| Calendar | `react-day-picker`, `date-fns` |

## Graceful fallback

If `shadcn init` is unavailable or fails, fall back to `references/ui-library/custom-tailwind.md`. The import paths (`@/components/ui/*`) are identical — no page template changes required.
