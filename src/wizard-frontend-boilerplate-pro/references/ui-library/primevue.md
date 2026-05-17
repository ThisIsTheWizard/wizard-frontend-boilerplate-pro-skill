# PrimeVue — Integration Reference

PrimeVue is a comprehensive Vue UI component library with 90+ components, a theming system based on design tokens, and first-class dark mode support.

## Install

```bash
npm install primevue @primevue/themes
```

## Setup (main.ts)

```ts
import { createApp } from "vue";
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura";
import { definePreset } from "@primevue/themes";
import ToastService from "primevue/toastservice";
import Tooltip from "primevue/tooltip";
import App from "./App.vue";

const MyPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: "var(--color-accent-50)",
      100: "var(--color-accent-100)",
      200: "var(--color-accent-200)",
      300: "var(--color-accent-300)",
      400: "var(--color-accent-400)",
      500: "var(--color-accent-500)",
      600: "var(--color-accent-600)",
      700: "var(--color-accent-700)",
      800: "var(--color-accent-800)",
      900: "var(--color-accent-900)",
      950: "var(--color-accent-950)",
    },
  },
});

const app = createApp(App);
app.use(PrimeVue, {
  theme: {
    preset: MyPreset,
    options: { darkModeSelector: ".dark" },
  },
});
app.use(ToastService);
app.directive("tooltip", Tooltip);
app.mount("#app");
```

## Dark mode bridge

PrimeVue reads `darkModeSelector: '.dark'`. The skill's `ThemeProvider` composable toggles `.dark` on `<html>`, so dark mode works automatically with no extra wiring.

## Component import style

Two options — pick one per project:

**Option A — Manual imports (recommended for tree-shaking):**
```ts
import Button from "primevue/button";
import InputText from "primevue/inputtext";
```

**Option B — Auto-import via unplugin:**
```bash
npm install -D unplugin-vue-components
```
```ts
// vite.config.ts
import Components from "unplugin-vue-components/vite";
import { PrimeVueResolver } from "@primevue/auto-import-resolver";

export default {
  plugins: [
    Components({ resolvers: [PrimeVueResolver()] }),
  ],
};
```

## Component map (PrimeVue v4)

### Inputs

| Component | Import path | Key props |
|---|---|---|
| `<Button>` | `primevue/button` | `severity` (primary/secondary/danger/contrast), `outlined`, `text`, `size`, `disabled` |
| `<InputText>` | `primevue/inputtext` | `v-model`, `placeholder`, `invalid`, `disabled` |
| `<Textarea>` | `primevue/textarea` | `v-model`, `rows`, `autoResize` |
| `<Select>` | `primevue/select` | `:options`, `optionLabel`, `optionValue`, `v-model`, `placeholder` |
| `<Checkbox>` | `primevue/checkbox` | `v-model`, `binary`, `inputId`, `value` |
| `<RadioButton>` | `primevue/radiobutton` | `v-model`, `value`, `inputId` |
| `<ToggleSwitch>` | `primevue/toggleswitch` | `v-model`, `disabled` |

### Display

| Component | Import path | Key props |
|---|---|---|
| `<Card>` | `primevue/card` | slots: `#title`, `#subtitle`, `#content`, `#footer` |
| `<Tag>` | `primevue/tag` | `severity` (primary/success/info/warn/danger/secondary/contrast), `value`, `rounded` |
| `<Avatar>` | `primevue/avatar` | `label`, `image`, `shape` (circle/square), `size` |
| `<Divider>` | `primevue/divider` | `layout` (horizontal/vertical), `type` (solid/dashed/dotted) |
| `<Skeleton>` | `primevue/skeleton` | `width`, `height`, `shape` (rectangle/circle), `borderRadius` |
| `<DataTable>` | `primevue/datatable` | `:value`, `sortField`, `sortOrder`, `paginator`, `:rows` |
| `<Column>` | `primevue/column` | `field`, `header`, `sortable` |

### Feedback

| Component | Import path | Key props / notes |
|---|---|---|
| `<Message>` | `primevue/message` | `severity` (info/success/warn/error), `closable` |
| `<Toast>` + `useToast()` | `primevue/toast` + `primevue/usetoast` | `toast.add({ severity, summary, detail, life })` — requires `ToastService` plugin |
| `<ProgressBar>` | `primevue/progressbar` | `:value` (0–100), `mode` (determinate/indeterminate) |
| `v-tooltip` directive | registered globally via `primevue/tooltip` | `v-tooltip.top="'Text'"`, positions: top/bottom/left/right |
| `<Dialog>` | `primevue/dialog` | `v-model:visible`, `header`, `modal`, `closable` |

### Navigation

| Component | Import path | Key props |
|---|---|---|
| `<Tabs>` + `<TabList>` + `<Tab>` + `<TabPanels>` + `<TabPanel>` | `primevue/tabs` | `v-model:value` on `<Tabs>`, `value` on each `<Tab>` and `<TabPanel>` |
| `<Breadcrumb>` | `primevue/breadcrumb` | `:model` array with `{ label, url }`, `:home` item |
| `<Paginator>` | `primevue/paginator` | `:rows`, `:totalRecords`, `v-model:first` |
| `<Menubar>` | `primevue/menubar` | `:model` array with nested `items` |

### Overlay

| Component | Import path | Key props |
|---|---|---|
| `<Popover>` | `primevue/popover` | ref + `.toggle(event)` — non-modal anchored panel |
| `<Menu>` | `primevue/menu` | ref + `.toggle(event)`, `:model` array with `{ label, command }` |
| `<Drawer>` | `primevue/drawer` | `v-model:visible`, `position` (left/right/top/bottom), `header` |

### Data viz

| Component | Import path | Key props |
|---|---|---|
| `<Chart>` | `primevue/chart` | `type` (bar/line/pie/doughnut), `:data`, `:options` — wraps Chart.js |
| `<DataTable>` (sortable) | `primevue/datatable` | `sortField`, `sortOrder`, `@sort`, `removableSort` |
| `<DatePicker>` | `primevue/datepicker` | `v-model`, `inline`, `showTime`, `selectionMode` |

## CSS var bridge

PrimeVue's Aura preset uses its own design tokens. Map them to the skill's accent palette in `definePreset`:

```ts
const MyPreset = definePreset(Aura, {
  semantic: {
    primary: {
      500: "var(--color-accent-500)", // interactive default
      600: "var(--color-accent-600)", // hover
      // add 50–950 for full range
    },
  },
});
```

Surface/background colors from PrimeVue's semantic layer (`surface-0` through `surface-900`) will continue to use Aura defaults unless overridden. For full alignment, also remap `colorScheme.light.surface` and `colorScheme.dark.surface`.

## Theming tips

- Use `pt` (passthrough) prop on any component to inject raw HTML attributes and classes without fighting the default styles.
- Use `unstyled: true` in the PrimeVue config for a headless mode where you style everything yourself.
- PrimeVue's CSS layer is `@layer primevue` — Tailwind's `@layer utilities` wins by default.

## Gotchas

- `<Select>` replaces the old `<Dropdown>` from PrimeVue v3. Do not use `<Dropdown>`.
- `<Tabs>` with sub-components replaces the old `<TabView>`/`<TabPanel>` pattern from v3.
- `<Popover>` replaces `<OverlayPanel>` from v3.
- `<ToggleSwitch>` replaces `<InputSwitch>` from v3.
- `<DatePicker>` replaces `<Calendar>` from v3.
- Toast requires `app.use(ToastService)` and `<Toast />` in the component tree before `useToast()` works.
- The `v-tooltip` directive must be registered globally (`app.directive("tooltip", Tooltip)`) or per-component.
