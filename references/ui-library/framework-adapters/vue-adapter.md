# Vue 3 — Framework Adapter

Patterns and rules for adapting the 28 components into idiomatic Vue 3 Single File
Components (SFC) with `<script setup>` and the Composition API.

---

## 1. File structure

Write all components to `src/components/ui/<Name>.vue`. TypeScript is enabled
by default via `lang="ts"`.

Each component follows the `<script setup>` + `<template>` + `<style>` structure:

```vue
<script setup lang="ts">
import { computed } from "vue";
import { cn } from "@/lib/utils";

interface Props {
  variant?: "default" | "outline" | "ghost" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {
  variant: "default",
  size: "default",
});

const classes = computed(() =>
  cn(
    "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
    props.variant === "destructive" && "bg-red-500 text-white",
    props.variant === "outline" && "border border-input bg-background",
    props.variant === "ghost" && "hover:bg-surface",
    props.variant === "default" && "bg-primary text-primary-foreground",
    props.size === "sm" && "h-9 px-3",
    props.size === "lg" && "h-11 px-8",
    props.size === "icon" && "h-10 w-10",
    props.class
  )
);
</script>

<template>
  <button :class="classes" v-bind="$attrs">
    <slot />
  </button>
</template>
```

---

## 2. Props definition

Use TypeScript interfaces with `withDefaults(defineProps<Props>(), {})`.
Never use `defineProps` with runtime options (`defineProps({ ... })`) — the
type-based form gives better IDE support and catches runtime-only errors.

```ts
interface Props {
  modelValue?: boolean;
  label?: string;
  disabled?: boolean;
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  disabled: false,
});
```

Emits are defined with `defineEmits`:

```ts
const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "change", value: string): void;
}>();
```

---

## 3. `v-bind="$attrs"` — attribute inheritance

Use `v-bind="$attrs"` on the root element to spread all attributes (id, data-,
aria-, etc.) without explicitly listing each one. This replaces React's
`{...props}` spread.

Do not use `v-bind="props"` — that spreads only declared props, not the
additional attributes. Always use `$attrs` on the root element.

```vue
<template>
  <button :class="classes" v-bind="$attrs">
    <slot />
  </button>
</template>
```

---

## 4. Slots

Use the `<slot />` element for content projection. Named slots use the
standard Vue syntax:

```vue
<template>
  <div>
    <header><slot name="header" /></header>
    <main><slot /></main>
    <footer><slot name="footer" /></footer>
  </div>
</template>
```

---

## 5. `v-model` support

For components that participate in `v-model`, use `defineModel()` (Vue 3.5+)
for two-way binding:

```vue
<script setup lang="ts">
const modelValue = defineModel<boolean>({ default: false });
</script>

<template>
  <input type="checkbox" v-model="modelValue" />
</template>
```

For Vue < 3.5, use `props` + `emit("update:modelValue", value)` manually.

---

## 6. Compound components

Components with sub-parts (Card, Dialog, Select, etc.) are written as separate
SFCs that are composed in a parent:

```
src/components/ui/Card.vue        — root card
src/components/ui/CardHeader.vue  — header slot wrapper
src/components/ui/CardTitle.vue   — title slot wrapper
src/components/ui/CardContent.vue  — content slot wrapper
src/components/ui/CardFooter.vue   — footer slot wrapper
```

Each file uses `<script setup lang="ts">` and exports only a default component.
Use `defineEmits` for any events the sub-component raises.

---

## 7. cn() utility

Create `src/lib/utils.ts` as a plain TypeScript module (not a `.vue` file):

```ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Import it in Vue components:

```ts
import { cn } from "@/lib/utils";
```

---

## 8. Event handling

Native events are bound with `@eventname` in templates:

```vue
<template>
  <input @input="onInput" @change="onChange" />
</template>
```

Custom events are emitted with `emit()`:

```ts
const emit = defineEmits<{ (e: "select", value: string): void }>();

function handleSelect(value: string) {
  emit("select", value);
}
```

---

## 9. Color token usage

All components use semantic CSS variable tokens:

- `bg-background`, `text-foreground`, `border-border`
- `bg-primary`, `text-primary-foreground`
- `text-muted`, `bg-surface`

Use `cn()` to combine semantic tokens with layout/spacing classes.

---

## 10. Accessibility

- Use semantic HTML (`<button>`, `<nav>`, `<main>`) instead of `<div>` with
  click handlers.
- Bind `aria-` attributes with Vue's `:attr` binding:

```vue
<button :aria-pressed="active" :aria-label="label" @click="toggle">
```

- Add `type="button"` to prevent form submission on icon buttons.
- Use `role` only when semantic HTML is insufficient.