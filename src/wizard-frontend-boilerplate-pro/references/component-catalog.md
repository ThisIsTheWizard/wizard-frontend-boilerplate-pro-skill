# Component Catalog

All 28 showcase components plus the `CodeBlock` utility component (29 total).
Each entry lists: category, peer dependencies, accessibility requirements,
props interface, and the source mapping in `ui-ux-pro-max-skill`.

## Table of Contents

- [Inputs (7)](#inputs)
- [Display (6)](#display)
- [Feedback (5)](#feedback)
- [Navigation (4)](#navigation)
- [Overlay (3)](#overlay)
- [Data viz (3)](#data-viz)
- [Utility (1)](#utility)

---

## Inputs

### Button

| Field | Value |
|---|---|
| Category | Inputs |
| Peer deps | none |
| Source | `src/components/ui/button.tsx` |

**Accessibility:** `role="button"`, keyboard-focusable, `aria-disabled` when disabled, `aria-pressed` for toggle variant.

**Props:**

```ts
interface ButtonProps {
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
  size?: "default" | "sm" | "lg" | "icon";
  disabled?: boolean;
  loading?: boolean;
  asChild?: boolean; // React only — renders child element with button styles
  onClick?: (e: MouseEvent) => void;
  children: ReactNode;
  className?: string;
}
```

---

### Input

| Field | Value |
|---|---|
| Category | Inputs |
| Peer deps | none |
| Source | `src/components/ui/input.tsx` |

**Accessibility:** `<label>` association via `htmlFor`/`id`, `aria-invalid` on error, `aria-describedby` for helper text.

**Props:**

```ts
interface InputProps extends HTMLInputAttributes {
  label?: string;
  error?: string;
  helperText?: string;
  className?: string;
}
```

---

### Textarea

| Field | Value |
|---|---|
| Category | Inputs |
| Peer deps | none |
| Source | `src/components/ui/textarea.tsx` |

**Accessibility:** Same as `Input`. Supports `rows` and auto-resize variant.

**Props:**

```ts
interface TextareaProps extends HTMLTextareaAttributes {
  label?: string;
  error?: string;
  helperText?: string;
  autoResize?: boolean;
  className?: string;
}
```

---

### Select

| Field | Value |
|---|---|
| Category | Inputs |
| Peer deps | none |
| Source | `src/components/ui/select.tsx` |

**Accessibility:** ARIA listbox pattern, `aria-expanded`, `aria-activedescendant`, keyboard navigation (arrows, Enter, Escape).

**Props:**

```ts
interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

interface SelectProps {
  options: SelectOption[];
  value?: string;
  defaultValue?: string;
  placeholder?: string;
  disabled?: boolean;
  label?: string;
  error?: string;
  onChange?: (value: string) => void;
  className?: string;
}
```

---

### Checkbox

| Field | Value |
|---|---|
| Category | Inputs |
| Peer deps | none |
| Source | `src/components/ui/checkbox.tsx` |

**Accessibility:** `role="checkbox"`, `aria-checked` (true/false/mixed for indeterminate), keyboard-focusable.

**Props:**

```ts
interface CheckboxProps {
  checked?: boolean;
  defaultChecked?: boolean;
  indeterminate?: boolean;
  disabled?: boolean;
  label?: string;
  id?: string;
  onCheckedChange?: (checked: boolean) => void;
  className?: string;
}
```

---

### RadioGroup

| Field | Value |
|---|---|
| Category | Inputs |
| Peer deps | none |
| Source | `src/components/ui/radio-group.tsx` |

**Accessibility:** `role="radiogroup"` on the container, `role="radio"` on each item, arrow-key navigation within group.

**Props:**

```ts
interface RadioOption {
  value: string;
  label: string;
  disabled?: boolean;
}

interface RadioGroupProps {
  options: RadioOption[];
  value?: string;
  defaultValue?: string;
  orientation?: "horizontal" | "vertical";
  label?: string;
  onValueChange?: (value: string) => void;
  className?: string;
}
```

---

### Switch

| Field | Value |
|---|---|
| Category | Inputs |
| Peer deps | none |
| Source | `src/components/ui/switch.tsx` |

**Accessibility:** `role="switch"`, `aria-checked`, toggle on Space/Enter.

**Props:**

```ts
interface SwitchProps {
  checked?: boolean;
  defaultChecked?: boolean;
  disabled?: boolean;
  label?: string;
  id?: string;
  onCheckedChange?: (checked: boolean) => void;
  className?: string;
}
```

---

## Display

### Card

| Field | Value |
|---|---|
| Category | Display |
| Peer deps | none |
| Source | `src/components/ui/card.tsx` |

**Accessibility:** Semantic `<article>` or `<section>` when containing meaningful content; otherwise `<div>`.

**Props:**

```ts
interface CardProps {
  children: ReactNode;
  className?: string;
}

interface CardHeaderProps { children: ReactNode; className?: string; }
interface CardTitleProps { children: ReactNode; className?: string; }
interface CardDescriptionProps { children: ReactNode; className?: string; }
interface CardContentProps { children: ReactNode; className?: string; }
interface CardFooterProps { children: ReactNode; className?: string; }
```

Sub-components exported: `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`.

---

### Badge

| Field | Value |
|---|---|
| Category | Display |
| Peer deps | none |
| Source | `src/components/ui/badge.tsx` |

**Accessibility:** Use `aria-label` when badge communicates status not conveyed by text alone.

**Props:**

```ts
interface BadgeProps {
  variant?: "default" | "secondary" | "destructive" | "outline";
  children: ReactNode;
  className?: string;
}
```

---

### Avatar

| Field | Value |
|---|---|
| Category | Display |
| Peer deps | none |
| Source | `src/components/ui/avatar.tsx` |

**Accessibility:** `<img>` with `alt` text; fallback initials marked `aria-hidden="true"` when image loads.

**Props:**

```ts
interface AvatarProps {
  src?: string;
  alt?: string;
  fallback?: string;
  size?: "sm" | "default" | "lg";
  className?: string;
}
```

---

### Separator

| Field | Value |
|---|---|
| Category | Display |
| Peer deps | none |
| Source | `src/components/ui/separator.tsx` |

**Accessibility:** `role="separator"`, `aria-orientation`.

**Props:**

```ts
interface SeparatorProps {
  orientation?: "horizontal" | "vertical";
  decorative?: boolean;
  className?: string;
}
```

---

### Skeleton

| Field | Value |
|---|---|
| Category | Display |
| Peer deps | none |
| Source | `src/components/ui/skeleton.tsx` |

**Accessibility:** Wrap in a container with `aria-busy="true"` and `aria-label="Loading…"` while content is pending.

**Props:**

```ts
interface SkeletonProps {
  className?: string;
}
```

Usage note: compose multiple `<Skeleton>` elements to mimic the expected content shape.

---

### Table

| Field | Value |
|---|---|
| Category | Display |
| Peer deps | none |
| Source | `src/components/ui/table.tsx` |

**Accessibility:** `<table>` with `<caption>` or `aria-label`, `scope="col"` on `<th>` elements.

**Props:**

```ts
interface TableProps { children: ReactNode; className?: string; }
interface TableHeaderProps { children: ReactNode; className?: string; }
interface TableBodyProps { children: ReactNode; className?: string; }
interface TableFooterProps { children: ReactNode; className?: string; }
interface TableRowProps { children: ReactNode; className?: string; }
interface TableHeadProps { children: ReactNode; className?: string; }
interface TableCellProps { children: ReactNode; colSpan?: number; className?: string; }
interface TableCaptionProps { children: ReactNode; className?: string; }
```

Sub-components exported: `Table`, `TableHeader`, `TableBody`, `TableFooter`, `TableRow`, `TableHead`, `TableCell`, `TableCaption`.

---

## Feedback

### Alert

| Field | Value |
|---|---|
| Category | Feedback |
| Peer deps | none |
| Source | `src/components/ui/alert.tsx` |

**Accessibility:** `role="alert"` for urgent messages; `role="status"` for informational. Screen readers announce immediately.

**Props:**

```ts
interface AlertProps {
  variant?: "default" | "destructive" | "warning" | "success";
  title?: string;
  children: ReactNode;
  icon?: ReactNode;
  className?: string;
}
```

Sub-components exported: `Alert`, `AlertTitle`, `AlertDescription`.

---

### Toast

| Field | Value |
|---|---|
| Category | Feedback |
| Peer deps | `sonner` (React/Svelte) · `vue-toastification` (Vue/Nuxt) |
| Source | `src/components/ui/toast.tsx` |

**Accessibility:** `role="status"` or `role="alert"`, `aria-live="polite"` or `"assertive"`. Auto-dismiss must be pausable on hover/focus.

**Props:**

```ts
interface ToastOptions {
  title?: string;
  description?: string;
  variant?: "default" | "success" | "error" | "warning";
  duration?: number;
  action?: { label: string; onClick: () => void };
}

// Usage via imperative API:
// toast(message, options)
// toast.success(message)
// toast.error(message)
```

**Framework peer deps:**

| Framework | Package |
|---|---|
| React / Next.js | `sonner` |
| Vue / Nuxt | `vue-toastification` |
| SvelteKit | `svelte-sonner` |

---

### Progress

| Field | Value |
|---|---|
| Category | Feedback |
| Peer deps | none |
| Source | `src/components/ui/progress.tsx` |

**Accessibility:** `role="progressbar"`, `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"`, `aria-label`.

**Props:**

```ts
interface ProgressProps {
  value?: number;
  max?: number;
  indeterminate?: boolean;
  label?: string;
  className?: string;
}
```

---

### Tooltip

| Field | Value |
|---|---|
| Category | Feedback |
| Peer deps | none |
| Source | `src/components/ui/tooltip.tsx` |

**Accessibility:** `role="tooltip"`, triggered element has `aria-describedby` pointing to tooltip content. Appears on hover AND focus.

**Props:**

```ts
interface TooltipProps {
  content: ReactNode;
  side?: "top" | "right" | "bottom" | "left";
  delay?: number;
  children: ReactNode;
  className?: string;
}
```

---

### Dialog

| Field | Value |
|---|---|
| Category | Feedback |
| Peer deps | none |
| Source | `src/components/ui/dialog.tsx` |

**Accessibility:** `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to title, focus trap while open, Escape closes, focus returns to trigger on close.

**Props:**

```ts
interface DialogProps {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: ReactNode;
}

interface DialogContentProps {
  children: ReactNode;
  className?: string;
}

interface DialogTitleProps { children: ReactNode; className?: string; }
interface DialogDescriptionProps { children: ReactNode; className?: string; }
interface DialogFooterProps { children: ReactNode; className?: string; }
```

Sub-components: `Dialog`, `DialogTrigger`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogDescription`, `DialogFooter`, `DialogClose`.

---

## Navigation

### Tabs

| Field | Value |
|---|---|
| Category | Navigation |
| Peer deps | none |
| Source | `src/components/ui/tabs.tsx` |

**Accessibility:** ARIA tab pattern — `role="tablist"`, `role="tab"`, `role="tabpanel"`, arrow-key navigation, `aria-selected`, `aria-controls`.

**Props:**

```ts
interface TabsProps {
  value?: string;
  defaultValue?: string;
  orientation?: "horizontal" | "vertical";
  onValueChange?: (value: string) => void;
  children: ReactNode;
  className?: string;
}

interface TabsListProps { children: ReactNode; className?: string; }
interface TabsTriggerProps { value: string; disabled?: boolean; children: ReactNode; className?: string; }
interface TabsContentProps { value: string; children: ReactNode; className?: string; }
```

Sub-components: `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent`.

---

### Breadcrumb

| Field | Value |
|---|---|
| Category | Navigation |
| Peer deps | none |
| Source | `src/components/ui/breadcrumb.tsx` |

**Accessibility:** `<nav aria-label="Breadcrumb">`, `<ol>` list, last item has `aria-current="page"`.

**Props:**

```ts
interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  separator?: ReactNode;
  className?: string;
}
```

Sub-components: `Breadcrumb`, `BreadcrumbList`, `BreadcrumbItem`, `BreadcrumbLink`, `BreadcrumbPage`, `BreadcrumbSeparator`.

---

### Pagination

| Field | Value |
|---|---|
| Category | Navigation |
| Peer deps | none |
| Source | `src/components/ui/pagination.tsx` |

**Accessibility:** `<nav aria-label="Pagination">`, current page has `aria-current="page"`, prev/next have `aria-label`.

**Props:**

```ts
interface PaginationProps {
  currentPage: number;
  totalPages: number;
  siblingCount?: number;
  onPageChange?: (page: number) => void;
  className?: string;
}
```

Sub-components: `Pagination`, `PaginationContent`, `PaginationItem`, `PaginationLink`, `PaginationPrevious`, `PaginationNext`, `PaginationEllipsis`.

---

### NavigationMenu

| Field | Value |
|---|---|
| Category | Navigation |
| Peer deps | none |
| Source | `src/components/ui/navigation-menu.tsx` |

**Accessibility:** `role="navigation"`, `role="menubar"` on the root, `role="menuitem"` on items, `aria-haspopup` on items with submenus, arrow-key navigation.

**Props:**

```ts
interface NavigationMenuItem {
  label: string;
  href?: string;
  children?: NavigationMenuItem[];
}

interface NavigationMenuProps {
  items: NavigationMenuItem[];
  className?: string;
}
```

Sub-components: `NavigationMenu`, `NavigationMenuList`, `NavigationMenuItem`, `NavigationMenuTrigger`, `NavigationMenuContent`, `NavigationMenuLink`, `NavigationMenuIndicator`, `NavigationMenuViewport`.

---

## Overlay

### Popover

| Field | Value |
|---|---|
| Category | Overlay |
| Peer deps | none |
| Source | `src/components/ui/popover.tsx` |

**Accessibility:** `role="dialog"` or `role="tooltip"` depending on content, `aria-haspopup`, Escape closes, focus management inside when interactive.

**Props:**

```ts
interface PopoverProps {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: ReactNode;
}

interface PopoverContentProps {
  side?: "top" | "right" | "bottom" | "left";
  align?: "start" | "center" | "end";
  sideOffset?: number;
  children: ReactNode;
  className?: string;
}
```

Sub-components: `Popover`, `PopoverTrigger`, `PopoverContent`.

---

### DropdownMenu

| Field | Value |
|---|---|
| Category | Overlay |
| Peer deps | none |
| Source | `src/components/ui/dropdown-menu.tsx` |

**Accessibility:** `role="menu"`, `role="menuitem"`, `role="menuitemcheckbox"`, `role="menuitemradio"`, arrow navigation, Escape closes, focus returns to trigger.

**Props:**

```ts
interface DropdownMenuProps {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: ReactNode;
}

interface DropdownMenuItemProps {
  disabled?: boolean;
  onSelect?: () => void;
  children: ReactNode;
  className?: string;
}
```

Sub-components: `DropdownMenu`, `DropdownMenuTrigger`, `DropdownMenuContent`, `DropdownMenuItem`, `DropdownMenuCheckboxItem`, `DropdownMenuRadioItem`, `DropdownMenuLabel`, `DropdownMenuSeparator`, `DropdownMenuShortcut`, `DropdownMenuSub`, `DropdownMenuSubTrigger`, `DropdownMenuSubContent`.

---

### Sheet

| Field | Value |
|---|---|
| Category | Overlay |
| Peer deps | none |
| Source | `src/components/ui/sheet.tsx` |

**Accessibility:** `role="dialog"`, `aria-modal="true"`, focus trap, Escape closes, focus returns to trigger. Overlay has `aria-hidden="true"`.

**Props:**

```ts
interface SheetProps {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: ReactNode;
}

interface SheetContentProps {
  side?: "top" | "right" | "bottom" | "left";
  children: ReactNode;
  className?: string;
}
```

Sub-components: `Sheet`, `SheetTrigger`, `SheetClose`, `SheetContent`, `SheetHeader`, `SheetFooter`, `SheetTitle`, `SheetDescription`.

---

## Data viz

### Chart

| Field | Value |
|---|---|
| Category | Data viz |
| Peer deps | `recharts` |
| Source | `src/components/ui/chart.tsx` |

**Accessibility:** `role="img"` on the chart container, `aria-label` summarizing data, fallback `<table>` with the same data for screen readers.

**Props:**

```ts
interface ChartConfig {
  [key: string]: { label: string; color?: string };
}

interface ChartContainerProps {
  config: ChartConfig;
  children: ReactNode;
  className?: string;
}

interface ChartTooltipContentProps {
  active?: boolean;
  payload?: Array<{ name: string; value: number; color: string }>;
  label?: string;
  hideLabel?: boolean;
  className?: string;
}
```

Sub-components: `ChartContainer`, `ChartTooltip`, `ChartTooltipContent`, `ChartLegend`, `ChartLegendContent`.

Wraps Recharts primitives (`LineChart`, `BarChart`, `PieChart`, etc.) with consistent theming via CSS variable tokens.

---

### DataTable

| Field | Value |
|---|---|
| Category | Data viz |
| Peer deps | `@tanstack/react-table` (React/Next.js) · `@tanstack/vue-table` (Vue/Nuxt) · `@tanstack/svelte-table` (SvelteKit) |
| Source | `src/components/ui/data-table.tsx` |

**Accessibility:** `<table>` with `<caption>`, `scope="col"` on headers, `aria-sort` on sortable columns.

**Props:**

```ts
interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  filterColumn?: string;
  filterPlaceholder?: string;
  pageSize?: number;
  className?: string;
}
```

Includes built-in: column visibility toggle, column sorting, global filter input, pagination controls.

**Framework peer deps:**

| Framework | Package |
|---|---|
| React / Next.js | `@tanstack/react-table` |
| Vue / Nuxt | `@tanstack/vue-table` |
| SvelteKit | `@tanstack/svelte-table` |

---

### Calendar

| Field | Value |
|---|---|
| Category | Data viz |
| Peer deps | `date-fns` |
| Source | `src/components/ui/calendar.tsx` |

**Accessibility:** `role="grid"` on the calendar, `aria-label` on the month/year header, `aria-selected` on selected date, arrow-key navigation between dates.

**Props:**

```ts
interface CalendarProps {
  mode?: "single" | "range" | "multiple";
  selected?: Date | Date[] | { from: Date; to?: Date };
  defaultSelected?: Date;
  onSelect?: (date: Date | undefined) => void;
  disabled?: (date: Date) => boolean;
  fromDate?: Date;
  toDate?: Date;
  locale?: Locale; // date-fns Locale
  weekStartsOn?: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  showOutsideDays?: boolean;
  className?: string;
}
```

---

## Utility

### CodeBlock

| Field | Value |
|---|---|
| Category | Utility (showcase-only) |
| Peer deps | none |
| Source | built-in (not sourced from `ui-ux-pro-max-skill`) |

**Accessibility:** `<pre><code>` with `role="region"` and `aria-label="Code snippet"`, copy button has `aria-label="Copy code"` that updates to `"Copied!"` on success.

**Props:**

```ts
interface CodeBlockProps {
  code: string;
  language?: string;
  filename?: string;
  collapsible?: boolean;
  defaultOpen?: boolean;
  className?: string;
}
```

Used exclusively in showcase routes to wrap every component example. Not part of the 28 components installed into user projects — installed alongside them for the `/library/*` routes only.

---

## Summary table

| # | Name | Category | Peer deps |
|---|---|---|---|
| 1 | Button | Inputs | — |
| 2 | Input | Inputs | — |
| 3 | Textarea | Inputs | — |
| 4 | Select | Inputs | — |
| 5 | Checkbox | Inputs | — |
| 6 | RadioGroup | Inputs | — |
| 7 | Switch | Inputs | — |
| 8 | Card | Display | — |
| 9 | Badge | Display | — |
| 10 | Avatar | Display | — |
| 11 | Separator | Display | — |
| 12 | Skeleton | Display | — |
| 13 | Table | Display | — |
| 14 | Alert | Feedback | — |
| 15 | Toast | Feedback | sonner / vue-toastification / svelte-sonner |
| 16 | Progress | Feedback | — |
| 17 | Tooltip | Feedback | — |
| 18 | Dialog | Feedback | — |
| 19 | Tabs | Navigation | — |
| 20 | Breadcrumb | Navigation | — |
| 21 | Pagination | Navigation | — |
| 22 | NavigationMenu | Navigation | — |
| 23 | Popover | Overlay | — |
| 24 | DropdownMenu | Overlay | — |
| 25 | Sheet | Overlay | — |
| 26 | Chart | Data viz | recharts |
| 27 | DataTable | Data viz | @tanstack/{react,vue,svelte}-table |
| 28 | Calendar | Data viz | date-fns |

---

## Library component mapping

How each of the 28 catalog components maps to native components in every supported UI library. Use this table when `UI_LIB` is set to a named library in Phase 5.

Abbreviations: **custom** = hand-written thin wrapper; **n/a** = no native equivalent, compose from primitives; **—** = same name as catalog.

### Inputs

| Catalog component | shadcn/ui | Material UI | Bootstrap | DaisyUI | Chakra UI | Mantine | Ant Design | PrimeVue | Vuetify |
|---|---|---|---|---|---|---|---|---|---|
| Button | `Button` | `Button` | `Button` | `.btn` | `Button` | `Button` | `Button` | `Button` | `v-btn` |
| Input | `Input` | `TextField` | `Form.Control` | `.input` | `Input` | `TextInput` | `Input` | `InputText` | `v-text-field` |
| Textarea | `Textarea` | `TextField multiline` | `Form.Control as="textarea"` | `.textarea` | `Textarea` | `Textarea` | `Input.TextArea` | `Textarea` | `v-textarea` |
| Select | `Select` | `Select` + `MenuItem` | `Form.Select` | `.select` | `NativeSelect` / `Select` | `Select` | `Select` | `Select` | `v-select` |
| Checkbox | `Checkbox` | `Checkbox` | `Form.Check type="checkbox"` | `.checkbox` | `Checkbox` | `Checkbox` | `Checkbox` | `Checkbox` | `v-checkbox` |
| RadioGroup | `RadioGroup` | `RadioGroup` + `Radio` | `Form.Check type="radio"` | `.radio` | `RadioGroup` + `Radio` | `Radio.Group` + `Radio` | `Radio.Group` | `RadioButton` | `v-radio-group` + `v-radio` |
| Switch | `Switch` | `Switch` | `Form.Check type="switch"` | `.toggle` | `Switch` | `Switch` | `Switch` | `ToggleSwitch` | `v-switch` |

### Display

| Catalog component | shadcn/ui | Material UI | Bootstrap | DaisyUI | Chakra UI | Mantine | Ant Design | PrimeVue | Vuetify |
|---|---|---|---|---|---|---|---|---|---|
| Card | `Card` | `Card` + `CardContent` | `Card` | `.card` | `Card` | `Card` | `Card` | `Card` | `v-card` |
| Badge | `Badge` | `Chip` | `Badge` | `.badge` | `Badge` | `Badge` | `Tag` / `Badge` | `Tag` / `Badge` | `v-chip` / `v-badge` |
| Avatar | `Avatar` | `Avatar` | custom | `.avatar` | `Avatar` | `Avatar` | `Avatar` | `Avatar` | `v-avatar` |
| Separator | `Separator` | `Divider` | `<hr>` / custom | `.divider` | `Divider` | `Divider` | `Divider` | `Divider` | `v-divider` |
| Skeleton | `Skeleton` | `Skeleton` | `Placeholder` | `.skeleton` | `Skeleton` | `Skeleton` | `Skeleton` | `Skeleton` | `v-skeleton-loader` |
| Table | `Table` | `Table` + sub-components | `Table` | `.table` | `Table` | `Table` | `Table` | `DataTable` (basic) | `v-table` |

### Feedback

| Catalog component | shadcn/ui | Material UI | Bootstrap | DaisyUI | Chakra UI | Mantine | Ant Design | PrimeVue | Vuetify |
|---|---|---|---|---|---|---|---|---|---|
| Alert | `Alert` | `Alert` | `Alert` | `.alert` | `Alert` | `Alert` | `Alert` | `Message` | `v-alert` |
| Toast | `Sonner` (sonner) | `Snackbar` | `Toast` + `ToastContainer` | `.toast` | `Toaster` / `useToast` | `notifications` (@mantine/notifications) | `message` / `notification` | `Toast` | `v-snackbar` |
| Progress | `Progress` | `LinearProgress` | `ProgressBar` | `.progress` | `Progress` | `Progress` | `Progress` | `ProgressBar` | `v-progress-linear` |
| Tooltip | `Tooltip` | `Tooltip` | `Tooltip` (overlay) | `.tooltip` | `Tooltip` | `Tooltip` | `Tooltip` | `Tooltip` (directive) | `v-tooltip` |
| Dialog | `Dialog` | `Dialog` | `Modal` | `.modal` | `Dialog` / `Modal` | `Modal` / `Dialog` | `Modal` | `Dialog` | `v-dialog` |

### Navigation

| Catalog component | shadcn/ui | Material UI | Bootstrap | DaisyUI | Chakra UI | Mantine | Ant Design | PrimeVue | Vuetify |
|---|---|---|---|---|---|---|---|---|---|
| Tabs | `Tabs` | `Tabs` + `Tab` | `Tabs` + `Tab` | `.tabs` | `Tabs` | `Tabs` | `Tabs` | `Tabs` + `TabList` | `v-tabs` + `v-tab` |
| Breadcrumb | `Breadcrumb` | `Breadcrumbs` | `Breadcrumb` | `.breadcrumbs` | `Breadcrumb` | `Breadcrumbs` | `Breadcrumb` | `Breadcrumb` | `v-breadcrumbs` |
| Pagination | `Pagination` | `Pagination` | `Pagination` | `.join` + `.btn` | custom | `Pagination` | `Pagination` | `Paginator` | `v-pagination` |
| NavigationMenu | `NavigationMenu` | `Menu` + `MenuItem` | `Navbar` + `Nav` | `.menu` | custom | `NavLink` + custom | `Menu` | `Menubar` / `Menu` | `v-navigation-drawer` + `v-list` |

### Overlay

| Catalog component | shadcn/ui | Material UI | Bootstrap | DaisyUI | Chakra UI | Mantine | Ant Design | PrimeVue | Vuetify |
|---|---|---|---|---|---|---|---|---|---|
| Popover | `Popover` | `Popover` | `Popover` (overlay) | `.dropdown` (anchored) | `Popover` | `Popover` | `Popover` | `Popover` | `v-menu` (anchored) |
| DropdownMenu | `DropdownMenu` | `Menu` + `MenuItem` | `Dropdown` | `.dropdown` | `Menu` | `Menu` | `Dropdown` | `Menu` / `TieredMenu` | `v-menu` |
| Sheet | `Sheet` | `Drawer` | custom | `.drawer` | `Drawer` | `Drawer` | `Drawer` | `Drawer` | `v-navigation-drawer` |

### Data viz

| Catalog component | shadcn/ui | Material UI | Bootstrap | DaisyUI | Chakra UI | Mantine | Ant Design | PrimeVue | Vuetify |
|---|---|---|---|---|---|---|---|---|---|
| Chart | `ChartContainer` (recharts) | recharts (no native) | recharts | recharts | recharts | `@mantine/charts` | `@ant-design/charts` | `Chart` (Chart.js) | recharts |
| DataTable | custom (TanStack Table) | `DataGrid` (@mui/x-data-grid) | custom (TanStack Table) | custom (TanStack Table) | custom (TanStack Table) | `@mantine/datatable` | `Table` (built-in) | `DataTable` (built-in) | `v-data-table` |
| Calendar | `Calendar` (react-day-picker) | `DateCalendar` (@mui/x-date-pickers) | custom / react-datepicker | custom | custom | `Calendar` (@mantine/dates) | `Calendar` / `DatePicker` | `DatePicker` / `Calendar` | `v-date-picker` |

### Notes

- **shadcn/ui** components are installed one at a time via `npx shadcn@latest add <name>`. See `references/ui-library/shadcn.md` for the full add-command list.
- **Material UI** `DataGrid` requires the separate `@mui/x-data-grid` package. `DateCalendar` requires `@mui/x-date-pickers` and a date adapter (`date-fns` or `dayjs`).
- **Bootstrap** has no native Avatar, Sheet (Drawer), or NavigationMenu equivalent — write thin wrappers for those slots.
- **DaisyUI** components are utility classes applied to standard HTML elements or framework components. No import — just apply the class. See `references/ui-library/daisy.md` for class→component mapping.
- **Chakra UI** v3 renamed several components from v2. Always check the v3 docs. Pagination is not built-in; compose from `HStack` + `Button`.
- **PrimeVue** `DataTable` is full-featured (sort, filter, pagination built-in) and covers both the `Table` and `DataTable` catalog slots.
- **Vuetify** `v-data-table` also covers the basic `Table` slot if needed. Chart support requires recharts or a third-party Chart.js integration.
