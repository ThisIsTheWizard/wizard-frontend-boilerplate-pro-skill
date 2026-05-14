# SvelteKit / Svelte 5 — Framework Adapter

Patterns and rules for adapting the 28 components into idiomatic Svelte 5 SFCs
using runes (`$props`, `$state`, `$derived`, `$effect`) and snippets.

---

## 1. File structure

Write all components to `src/lib/components/ui/<Name>.svelte`. TypeScript is
enabled by default via `lang="ts"`.

Each component uses Svelte 5 runes syntax:

```svelte
<script lang="ts">
  import { cn } from "$lib/utils";

  interface Props {
    variant?: "default" | "outline" | "ghost" | "destructive";
    size?: "default" | "sm" | "lg" | "icon";
    class?: string;
    children?: import("svelte").Snippet;
  }

  let {
    variant = "default",
    size = "default",
    class: className = "",
    children,
  }: Props = $props();

  const classes = $derived(cn(
    "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
    variant === "destructive" && "bg-red-500 text-white",
    variant === "outline" && "border border-input bg-background",
    variant === "ghost" && "hover:bg-surface",
    variant === "default" && "bg-primary text-primary-foreground",
    size === "sm" && "h-9 px-3",
    size === "lg" && "h-11 px-8",
    size === "icon" && "h-10 w-10",
    className
  ));
</script>

<template>
  <button class={classes} v-bind="$attrs">
    {@render children?.()}
  </button>
</template>
```

---

## 2. Props with `$props()`

Use `let { ... }: Props = $props()` with destructuring. Required props are
listed without defaults; optional ones have defaults.

```svelte
<script lang="ts">
  interface Props {
    label: string;
    disabled?: boolean;
    class?: string;
  }

  let { label, disabled = false, class: className = "" }: Props = $props();
</script>
```

---

## 3. Reactive state with `$state()`

```svelte
<script lang="ts">
  let open = $state(false);
  let count = $state(0);
</script>
```

---

## 4. Derived values with `$derived()`

```svelte
<script lang="ts">
  let variant = $state("default");
  const classes = $derived(cn("rounded-md", variant === "outline" && "border"));
</script>
```

---

## 5. Effects with `$effect()`

```svelte
<script lang="ts">
  interface Props {
    value: string;
  }
  let { value }: Props = $props();

  $effect(() => {
    console.log("value changed to", value);
  });
</script>
```

---

## 6. Snippets (rendering children)

Svelte 5 uses `{@render snippet()}` to render children. Import `Snippet` type
from "svelte":

```svelte
<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();
</script>

<template>
  <div>
    {@render children?.()}
  </div>
</template>
```

---

## 7. Event handlers

Use standard HTML event attributes in templates:

```svelte
<template>
  <button @click={handleClick} @keydown={handleKeydown}>
    Click me
  </button>
</template>

<script lang="ts">
  function handleClick(e: MouseEvent) {
    console.log("clicked", e.target);
  }
</script>
```

For two-way binding, use `$bindable()`:

```svelte
<script lang="ts">
  interface Props {
    checked?: boolean;
    onchange?: (checked: boolean) => void;
  }

  let { checked = $bindable(false), onchange }: Props = $props();
</script>

<template>
  <input type="checkbox" bind:checked onchange={() => onchange?.(checked)} />
</template>
```

---

## 8. Compound components

Components with sub-parts (Card, Dialog, etc.) are separate `.svelte` files:

```
src/lib/components/ui/Button.svelte
src/lib/components/ui/Card.svelte
src/lib/components/ui/CardHeader.svelte
src/lib/components/ui/CardTitle.svelte
```

Import and compose in the parent page or layout file. Each component uses
`$props()` and `$derived()` independently.

---

## 9. `cn()` utility

Create `src/lib/utils/utils.ts`:

```ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Export it from `src/lib/index.ts` for convenient access:

```ts
export { cn } from "./utils/utils";
```

Import it in Svelte components:

```svelte
<script lang="ts">
  import { cn } from "$lib";
</script>
```

---

## 10. Color token usage

All components use semantic CSS variable tokens:

- `bg-background`, `text-foreground`, `border-border`
- `bg-primary`, `text-primary-foreground`
- `text-muted`, `bg-surface`

Use `$derived(cn(...))` to combine tokens with layout classes.

---

## 11. Accessibility

- Use semantic HTML elements (`<button>`, `<nav>`, etc.) instead of clickable `<div>`.
- Add `aria-` attributes directly in templates:

```svelte
<button aria-label="Close" aria-expanded={open} @click={() => open = false}>
```

- For icon-only buttons, always add `aria-label`.
- Bind keyboard events with `@keydown`:

```svelte
<div role="dialog" @keydown={(e) => e.key === "Escape" && close()} />
```

---

## 12. SSR considerations

Because SvelteKit uses SSR by default, avoid browser-only APIs at the top level.
Use `$effect()` for any code that must run only in the browser:

```svelte
<script lang="ts">
  $effect(() => {
    // Browser-only: localStorage, window, etc.
    const theme = localStorage.getItem("theme");
  });
</script>
```

If SSR causes issues, add `export const ssr = false` and `export const prerender = false`
to the `+layout.ts` file at the route group level, as described in the
SvelteKit scaffold reference (`references/frameworks/svelte-kit.md`).