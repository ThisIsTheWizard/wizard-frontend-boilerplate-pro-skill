# Vuetify — Integration Reference

Vuetify is a Material Design component library for Vue 3 with 80+ components, a built-in theme system, and comprehensive typography/spacing scales.

## Install

```bash
npm install vuetify @mdi/font
```

## Setup (main.ts)

```ts
import { createApp } from "vue";
import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import App from "./App.vue";

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "light",
    themes: {
      light: {
        colors: {
          primary: "#3b82f6",
          secondary: "#6b7280",
          error: "#ef4444",
          warning: "#f59e0b",
          info: "#0ea5e9",
          success: "#10b981",
          surface: "#ffffff",
          background: "#f9fafb",
        },
      },
      dark: {
        colors: {
          primary: "#60a5fa",
          secondary: "#9ca3af",
          error: "#f87171",
          warning: "#fbbf24",
          info: "#38bdf8",
          success: "#34d399",
          surface: "#1e293b",
          background: "#0f172a",
        },
      },
    },
  },
});

const app = createApp(App);
app.use(vuetify);
app.mount("#app");
```

## Dark mode bridge

Vuetify manages its own theme system independently from the skill's CSS variable approach. In `AppLayout.vue`, sync the two systems via a watcher:

```ts
import { watch } from "vue";
import { useTheme as useVuetifyTheme } from "vuetify";
import { useTheme } from "@/composables/useTheme";

const { theme } = useTheme();
const vuetifyTheme = useVuetifyTheme();
watch(theme, (val) => {
  vuetifyTheme.global.name.value = val === "dark" ? "dark" : "light";
}, { immediate: true });
```

## Tree-shaking (optional)

Instead of importing all components, use the Vuetify Vite plugin:

```bash
npm install -D vite-plugin-vuetify
```

```ts
// vite.config.ts
import vuetify from "vite-plugin-vuetify";

export default {
  plugins: [
    vuetify({ autoImport: true }),
  ],
};
```

Then remove the `* as components` import and let the plugin handle it.

## Component map (Vuetify 3)

### Inputs

| Component | Key props |
|---|---|
| `<v-btn>` | `color`, `variant` (flat/outlined/text/tonal/elevated/plain), `size` (x-small/small/default/large/x-large), `disabled`, `block` |
| `<v-text-field>` | `v-model`, `label`, `variant` (outlined/filled/underlined/solo/plain), `type`, `disabled`, `error-messages` |
| `<v-textarea>` | `v-model`, `label`, `rows`, `variant`, `auto-grow` |
| `<v-select>` | `v-model`, `label`, `:items`, `item-title`, `item-value`, `variant` |
| `<v-checkbox>` | `v-model`, `label`, `color`, `hide-details` |
| `<v-radio-group>` + `<v-radio>` | `<v-radio-group v-model="val">` wraps `<v-radio :value="x" label="…">` |
| `<v-switch>` | `v-model`, `label`, `color`, `hide-details` |

### Display

| Component | Key props |
|---|---|
| `<v-card>` + `<v-card-title>` + `<v-card-subtitle>` + `<v-card-text>` + `<v-card-actions>` | `elevation`, `variant` (elevated/flat/outlined/tonal/text), `rounded` |
| `<v-chip>` | `color`, `variant` (elevated/flat/outlined/text/tonal), `closable`, `label` |
| `<v-avatar>` | `color`, `image`, `size`, `rounded` |
| `<v-divider>` | `vertical`, `thickness`, `color`, `opacity` |
| `<v-skeleton-loader>` | `type` (card/list-item/avatar/text/image/table), `loading` |
| `<v-table>` | `density` (default/comfortable/compact), `fixed-header`, `height` — use standard HTML `thead`/`tbody` inside |
| `<v-data-table>` | `:headers`, `:items`, `v-model:sort-by`, `items-per-page` |

### Feedback

| Component | Key props |
|---|---|
| `<v-alert>` | `type` (success/info/warning/error), `variant`, `title`, `text`, `closable`, `prominent` |
| `<v-snackbar>` | `v-model`, `color`, `timeout`, `location`, `multi-line` |
| `<v-progress-linear>` | `:model-value` (0–100), `color`, `indeterminate`, `height` |
| `<v-tooltip>` | Wrap trigger in `#activator="{ props }"` slot, provide `text` prop or default slot |
| `<v-dialog>` | `v-model`, `max-width`, `persistent` — use `#activator="{ props }"` or external `v-model` |

### Navigation

| Component | Key props |
|---|---|
| `<v-tabs>` + `<v-tab>` + `<v-window>` + `<v-window-item>` | `v-model` on `<v-tabs>`, `:value` on each `<v-tab>` and `<v-window-item>` |
| `<v-breadcrumbs>` | `:items` array with `{ title, href, disabled }` |
| `<v-pagination>` | `v-model`, `:length`, `:total-visible`, `rounded` |
| `<v-app-bar>` / Menubar pattern | Use `<v-menu>` + `<v-list>` + `<v-list-item>` for dropdown nav items |

### Overlay

| Component | Key props |
|---|---|
| `<v-menu>` | Use `#activator="{ props }"` slot, `close-on-content-click` (true for menus, false for popover) |
| `<v-list>` + `<v-list-item>` | Inside `<v-menu>` for dropdown items; `value`, `title`, `prepend-icon` |
| `<v-navigation-drawer>` | `v-model`, `location` (left/right), `temporary`, `width` |

### Data viz

Vuetify does not ship a chart component. Use Chart.js directly:

```bash
npm install chart.js vue-chartjs
```

```vue
<script setup lang="ts">
import { Line } from "vue-chartjs";
import {
  CategoryScale, Chart as ChartJS, Legend, LinearScale,
  LineElement, PointElement, Title, Tooltip,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const data = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  datasets: [{ borderColor: "#3b82f6", data: [65, 59, 80, 81, 56, 72], label: "Sessions" }],
};
const options = { responsive: true };
</script>

<template>
  <Line :data="data" :options="options" />
</template>
```

For the calendar, use Vuetify Labs' `<v-date-picker>`:

```ts
import { VDatePicker } from "vuetify/labs/VDatePicker";
// register in createVuetify components or import manually
```

```vue
<v-date-picker v-model="selectedDate" />
```

## CSS var bridge

Vuetify uses its own internal SCSS-based token system and generates CSS custom properties like `--v-theme-primary`. The skill's `--color-accent-*` tokens can be aligned by hardcoding a representative hex in the theme config colors (as shown in the setup above). For full dynamic sync at runtime, override Vuetify's color tokens in `:root` using JS after mount:

```ts
// Optional: full runtime sync (advanced)
watch(() => cssVarValue("--color-accent-500"), (hex) => {
  document.documentElement.style.setProperty("--v-theme-primary", hexToRgb(hex));
});
```

For most projects the static color values in the theme config are sufficient.

## Vuetify-specific layout note

Vuetify's `<v-app>` wrapper is required at the root for theme injection to work. Wrap your app root with it:

```vue
<template>
  <v-app :theme="vuetifyTheme">
    <slot />
  </v-app>
</template>
```

The skill's `AppLayout.vue` does NOT use `<v-app>` — add it at the page/router-view level or in `App.vue`.

## Gotchas

- Vuetify imports `vuetify/styles` globally — this adds ~100 KB of base CSS. Use `vite-plugin-vuetify` with tree-shaking to reduce this.
- `<v-data-table>` with sorting requires `:headers` items to have `sortable: true`.
- `<v-tooltip>` requires the activator pattern — it does not work with the older `activator` string prop in Vuetify 3.
- `<v-navigation-drawer>` with `temporary` closes on outside click; without `temporary` it is persistent.
- MDI icons require the `@mdi/font` CSS import. Alternatively use `mdi-svg` for tree-shakeable SVG icons.
- `VDatePicker` is in Vuetify Labs and must be opted into — it may have breaking API changes.
