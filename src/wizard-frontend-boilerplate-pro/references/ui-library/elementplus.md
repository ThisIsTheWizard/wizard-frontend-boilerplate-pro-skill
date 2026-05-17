# Element Plus — Integration Reference

## Overview

Element Plus is a Vue 3 UI component library — the official successor to Element UI. It ships 70+ components with full TypeScript support, a CSS variable-based token system, and built-in dark mode.

- **Package**: `element-plus`
- **Version**: v2.x
- **Framework support**: Vue 3.x / Nuxt 3+ — **no React or Svelte package**
- **Components**: 70+ covering form inputs, data display, navigation, feedback, and overlay patterns

## Install

```bash
npm install element-plus
```

Icon library (separate package):

```bash
npm install @element-plus/icons-vue
```

## Auto-import setup (recommended)

Auto-import avoids bundling unused components and handles tree-shaking automatically.

```bash
npm install -D unplugin-vue-components unplugin-auto-import
```

```ts
// vite.config.ts
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
});
```

> **TypeScript**: Add the generated declaration files to `tsconfig.json`:
>
> ```json
> {
>   "include": ["auto-imports.d.ts", "components.d.ts"]
> }
> ```

## Manual full import (alternative)

```ts
// main.ts
import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import App from "./App.vue";

const app = createApp(App);
app.use(ElementPlus);
app.mount("#app");
```

> For manual tree-shaking per component:
> ```ts
> import { ElButton } from "element-plus";
> import "element-plus/es/components/button/style/css";
> ```

## Dark mode bridge

Element Plus dark mode is triggered by adding `class="dark"` to `<html>` — compatible with the skill's `ThemeProvider` composable, which already toggles that class.

Include dark mode styles by importing the dark theme CSS:

```ts
// main.ts — import after the default CSS
import "element-plus/theme-chalk/dark/css-vars.css";
```

Or import both at once:

```ts
import "element-plus/dist/index.css";
```

(The full dist CSS includes dark mode variable overrides.)

## CSS variable bridge

Map skill tokens to Element Plus CSS variables in your `globals.css` or a dedicated token bridge file:

```css
:root {
  --el-color-primary:       var(--color-accent-500);
  --el-color-primary-dark-2: var(--color-accent-600);
  --el-color-primary-light-3: var(--color-accent-400);
  --el-bg-color:            var(--background);
  --el-text-color-primary:  var(--foreground);
  --el-border-color:        var(--border);
}
```

| Skill token | Element Plus var |
|---|---|
| `--color-accent-500` | `--el-color-primary` |
| `--color-accent-600` | `--el-color-primary-dark-2` |
| `--color-accent-400` | `--el-color-primary-light-3` |
| `--background` | `--el-bg-color` |
| `--foreground` | `--el-text-color-primary` |
| `--border` | `--el-border-color` |

## SCSS variable override strategy

For build-time token replacement (deeper integration):

```scss
// styles/element-vars.scss
@forward 'element-plus/theme-chalk/src/common/var.scss' with (
  $--el-color-primary: #3b82f6
);
```

Then in `vite.config.ts`:

```ts
css: {
  preprocessorOptions: {
    scss: {
      additionalData: `@use "@/styles/element-vars.scss" as *;`,
    },
  },
},
```

## Vue-only constraint

Element Plus has no React or Svelte package. For React projects use HeroUI, shadcn/ui, or Ant Design. For SvelteKit use DaisyUI or a custom Tailwind approach.

## Nuxt integration

Use the official Nuxt module:

```bash
npm install -D @element-plus/nuxt
```

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ["@element-plus/nuxt"],
});
```

## Component map (Element Plus v2)

### Inputs

| Skill slot | Element Plus component | Key props |
|---|---|---|
| Button | `<el-button>` | `type` (primary/success/warning/danger/info), `plain`, `round`, `circle`, `disabled`, `loading` |
| Input | `<el-input>` | `v-model`, `placeholder`, `type`, `clearable`, `show-password`, `disabled` |
| Textarea | `<el-input type="textarea">` | `:rows`, `autosize` (object `{ minRows, maxRows }`) |
| Select | `<el-select>` + `<el-option>` | `v-model`, `filterable`, `clearable`, `placeholder` |
| Checkbox | `<el-checkbox>` | `v-model`, `label`, `disabled`; `<el-checkbox-group>` for multi-value |
| RadioGroup | `<el-radio-group>` + `<el-radio>` | `v-model` on group, `value` on each radio |
| Switch | `<el-switch>` | `v-model`, `active-color`, `inactive-color`, `active-text`, `inactive-text` |

### Display

| Skill slot | Element Plus component | Key props |
|---|---|---|
| Card | `<el-card>` | `header` slot or `header` prop, `shadow` (always/hover/never) |
| Badge | `<el-badge>` | `:value`, `type` (primary/success/warning/danger/info), `is-dot`, `max` |
| Avatar | `<el-avatar>` | `:size` (number or sm/md/lg), `shape` (circle/square), `src`, `icon` |
| Separator/Divider | `<el-divider>` | `direction` (horizontal/vertical), `content-position` (left/center/right) |
| Skeleton | `<el-skeleton>` | `:rows`, `animated`, `loading` |
| Table | `<el-table>` + `<el-table-column>` | `v-loading`, `sortable`, `stripe`, `border`, `highlight-current-row` |

### Feedback

| Skill slot | Element Plus component | Notes |
|---|---|---|
| Alert | `<el-alert>` | `title`, `type` (success/warning/info/error), `description`, `closable`, `show-icon` |
| Toast | `ElMessage(...)` composable | `ElMessage.success/warning/error/info(text)` or `ElMessage({ message, type, duration })` |
| Progress | `<el-progress>` | `:percentage`, `type` (line/circle/dashboard), `status` (success/exception/warning) |
| Tooltip | `<el-tooltip>` | `content`, `placement`, `effect` (dark/light) |
| Dialog | `<el-dialog>` | `v-model`, `title`, `width`, `:before-close` |

### Navigation

| Skill slot | Element Plus component | Key props |
|---|---|---|
| Tabs | `<el-tabs>` + `<el-tab-pane>` | `v-model`, `type` (card/border-card), `label`, `name` |
| Breadcrumb | `<el-breadcrumb>` + `<el-breadcrumb-item>` | `:to` (router-link), `separator` |
| Pagination | `<el-pagination>` | `v-model:current-page`, `:page-size`, `:total`, `layout` |
| NavigationMenu | `<el-menu>` + `<el-menu-item>` + `<el-sub-menu>` | `mode` (horizontal/vertical), `router`, `default-active` |

### Overlay

| Skill slot | Element Plus component | Key props |
|---|---|---|
| Popover | `<el-popover>` | `trigger` (click/hover/focus), `content`, `placement`, `title`, `width` |
| DropdownMenu | `<el-dropdown>` + `<el-dropdown-menu>` + `<el-dropdown-item>` | `@command`, `trigger`, `placement` |
| Sheet/Drawer | `<el-drawer>` | `v-model`, `title`, `direction` (ltr/rtl/ttb/btt), `size` |

### Data viz

| Skill slot | Element Plus component | Notes |
|---|---|---|
| Chart | `vue-echarts` + `echarts` | Element Plus has no native chart — `vue-echarts` is the canonical pairing |
| DataTable | `<el-table>` with sort and filter | Use `sortable` on columns + `@sort-change` on table |
| Calendar | `<el-date-picker>` | `type` (date/daterange/month/year), `v-model`, `inline` for inline display |

## Key API snippets

### ElMessage toast

```ts
// Import even with auto-import (it's a function, not a component)
import { ElMessage } from "element-plus";

ElMessage.success("Profile saved successfully.");
ElMessage.warning("Unsaved changes detected.");
ElMessage.error("Something went wrong.");
ElMessage({
  message: "Custom toast",
  type: "info",
  duration: 3000,
  showClose: true,
});
```

### el-table with sortable columns

```vue
<el-table :data="tableData" stripe border @sort-change="handleSortChange">
  <el-table-column prop="name" label="Name" sortable />
  <el-table-column prop="email" label="Email" sortable />
  <el-table-column prop="role" label="Role" />
</el-table>
```

### el-dialog with v-model

```vue
<script setup lang="ts">
import { ref } from "vue";
const visible = ref(false);
</script>

<template>
  <el-button @click="visible = true">Open dialog</el-button>
  <el-dialog v-model="visible" title="Confirm action" width="28rem">
    <p>This action cannot be undone.</p>
    <template #footer>
      <el-button @click="visible = false">Cancel</el-button>
      <el-button type="primary" @click="visible = false">Confirm</el-button>
    </template>
  </el-dialog>
</template>
```

### el-form with validation

```vue
<script setup lang="ts">
import { reactive, ref } from "vue";
import type { FormInstance, FormRules } from "element-plus";

const formRef = ref<FormInstance>();
const form = reactive({ email: "", name: "" });
const rules: FormRules = {
  email: [{ required: true, type: "email", message: "Valid email required", trigger: "blur" }],
  name:  [{ required: true, min: 2, message: "Name must be at least 2 characters", trigger: "blur" }],
};

async function handleSubmit() {
  await formRef.value?.validate();
  // submit...
}
</script>

<template>
  <el-form ref="formRef" :model="form" :rules="rules" label-width="auto">
    <el-form-item label="Name" prop="name">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item label="Email" prop="email">
      <el-input v-model="form.email" type="email" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="handleSubmit">Submit</el-button>
    </el-form-item>
  </el-form>
</template>
```

## Gotchas

- **Auto-import TypeScript declarations** — add `auto-imports.d.ts` and `components.d.ts` to `tsconfig.json` `include` array or you'll get type errors.
- **`ElMessage` and `ElNotification` must be imported separately** — they are functions, not components, so unplugin-vue-components won't auto-import them. Always `import { ElMessage } from "element-plus"` explicitly.
- **Full CSS import includes dark styles** — `element-plus/dist/index.css` includes dark mode variable overrides; the `dark` class on `<html>` activates them.
- **Tree-shaking with manual imports** — import both the component and its style: `import { ElButton } from "element-plus"` + `import "element-plus/es/components/button/style/css"`.
- **Icon library is separate** — `npm install @element-plus/icons-vue` and register icons globally or import per-use.
- **`vue-echarts` + `echarts`** is the canonical chart pairing for Element Plus projects. Install with `npm install vue-echarts echarts`.
- **`el-select` filterable + remote** — for remote search, add `:remote="true"` + `:remote-method="myFn"` + `loading` state to `el-select`.
- **`el-pagination` layout** — control which controls appear with the `layout` prop: e.g. `"total, prev, pager, next, jumper"`.
