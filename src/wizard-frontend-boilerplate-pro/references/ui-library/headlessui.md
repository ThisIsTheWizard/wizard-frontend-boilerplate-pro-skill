# Headless UI Integration Reference

## Overview

Headless UI is a set of completely unstyled, fully accessible UI primitives for React and Vue. It provides the interaction logic and ARIA semantics for complex components (Dialog, Listbox, Menu, Popover, RadioGroup, Switch, Tabs, etc.) while leaving all visual styling to you. Every component in this skill uses Tailwind CSS for styling — Headless UI always pairs with the project's existing Tailwind token system.

**Packages:**
- React: `@headlessui/react` v2 (React 18+)
- Vue: `@headlessui/vue` v1 (Vue 3.x)

Headless UI has no Svelte package — SvelteKit projects fall back to `references/ui-library/custom-tailwind.md`.

## Framework support

| Framework | Package | Version | Notes |
|-----------|---------|---------|-------|
| Next.js 15 / React 19 | `@headlessui/react` | v2.x | Full support; works in Client Components |
| React + Vite | `@headlessui/react` | v2.x | Full support |
| Vue 3.5 / Nuxt 4 | `@headlessui/vue` | v1.x | Full support |
| SvelteKit | — | — | No package; use `custom-tailwind.md` fallback |

## Install

### React

```bash
npm install @headlessui/react
```

No Tailwind plugin needed — Headless UI is behaviour-only; all styling is Tailwind utilities.

### Vue

```bash
npm install @headlessui/vue
```

## Theming bridge

Headless UI components accept `className` (React) / `class` (Vue) — they render standard HTML elements with the classes you provide. There is no internal theme system to bridge; the existing skill token system (`--background`, `--foreground`, `--primary`, etc.) is used directly via Tailwind utility classes.

Dark mode works automatically through the skill's `data-theme` / `class="dark"` toggle because all classes reference CSS custom properties.

## CSS variable integration

Because Headless UI components only add ARIA and interaction, all token usage follows the same pattern as `custom-tailwind.md`:

```tsx
// Dialog backdrop uses bg-black/50 (no token), panel uses token-aware classes
<DialogPanel className="bg-surface border border-border rounded-xl p-6 shadow-xl" />

// Menu item active state
<MenuItem className="data-[focus]:bg-accent data-[focus]:text-foreground" />

// Switch thumb uses translate for on/off
<Switch className="data-[checked]:bg-primary bg-muted-foreground/30" />
```

## Component coverage map

| Skill slot       | Headless UI approach (React)                                           | Headless UI approach (Vue) |
|------------------|------------------------------------------------------------------------|----------------------------|
| Button           | plain `<button>` + Tailwind                                            | plain `<button>` + Tailwind |
| Input            | `<Input>` (v2 Field primitive) or plain `<input>` + Tailwind          | plain `<input>` + Tailwind |
| Textarea         | `<Textarea>` (v2 Field primitive) or plain `<textarea>` + Tailwind    | plain `<textarea>` + Tailwind |
| Select           | `Listbox` (accessible dropdown select)                                 | `Listbox` |
| Checkbox         | `Checkbox` (v2)                                                        | plain `<input type="checkbox">` + Tailwind |
| RadioGroup       | `RadioGroup` + `Radio`                                                 | `RadioGroup` + `RadioGroupOption` |
| Switch           | `Switch`                                                               | `Switch` |
| Card             | plain `<div>` + Tailwind                                               | plain `<div>` + Tailwind |
| Badge            | plain `<span>` + Tailwind                                             | plain `<span>` + Tailwind |
| Avatar           | plain `<div>` + Tailwind                                              | plain `<div>` + Tailwind |
| Separator        | plain `<hr>` + Tailwind                                               | plain `<hr>` + Tailwind |
| Skeleton         | plain `<div>` + Tailwind + `animate-pulse`                            | plain `<div>` + Tailwind + `animate-pulse` |
| Table            | plain `<table>` + Tailwind                                            | plain `<table>` + Tailwind |
| Alert            | plain `<div role="alert">` + Tailwind                                 | plain `<div role="alert">` + Tailwind |
| Toast            | manual `useState` queue + `Transition`                                | manual `ref` queue + `TransitionRoot` |
| Progress         | plain `<div>` + Tailwind                                              | plain `<div>` + Tailwind |
| Tooltip          | `Popover` (CSS-positioned hover variant)                              | `Popover` |
| Dialog/Modal     | `Dialog` + `DialogPanel` + `DialogBackdrop`                           | `Dialog` + `DialogPanel` |
| Tabs             | `TabGroup` + `TabList` + `Tab` + `TabPanels` + `TabPanel`            | `TabGroup` + `TabList` + `Tab` + `TabPanels` + `TabPanel` |
| Breadcrumb       | plain `<nav aria-label="breadcrumb">` + Tailwind                     | plain `<nav aria-label="breadcrumb">` + Tailwind |
| Pagination       | plain button group + Tailwind                                         | plain button group + Tailwind |
| NavigationMenu   | plain `<nav>` + Tailwind                                              | plain `<nav>` + Tailwind |
| Popover          | `Popover` + `PopoverButton` + `PopoverPanel`                          | `Popover` + `PopoverButton` + `PopoverPanel` |
| DropdownMenu     | `Menu` + `MenuButton` + `MenuItems` + `MenuItem`                      | `Menu` + `MenuButton` + `MenuItems` + `MenuItem` |
| Sheet/Drawer     | `Dialog` + `DialogPanel` (slide-in variant via `translate-x`)         | `Dialog` + `DialogPanel` (slide-in) |
| Chart            | recharts (no HUI primitive)                                           | vue-chartjs (no HUI primitive) |
| DataTable        | plain `<table>` + sort state                                          | plain `<table>` + sort state |
| Calendar         | plain calendar grid + Tailwind                                        | plain calendar grid + Tailwind |

## React API quick-reference (@headlessui/react v2)

### Field primitives

```tsx
import { Field, Label, Description, Input, Textarea, Select } from "@headlessui/react";

<Field>
  <Label className="text-sm font-medium text-foreground">Email</Label>
  <Description className="text-sm text-muted-foreground">We'll never share it.</Description>
  <Input
    className="mt-1 w-full rounded-md border border-border bg-background px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring"
    type="email"
  />
</Field>
```

### Listbox (Select)

```tsx
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from "@headlessui/react";

<Listbox value={selected} onChange={setSelected}>
  <ListboxButton className="relative w-full rounded-md border border-border bg-background px-3 py-2 text-left text-sm">
    {selected}
  </ListboxButton>
  <ListboxOptions
    anchor="bottom"
    className="z-50 w-[var(--button-width)] rounded-md border border-border bg-surface shadow-lg [--anchor-gap:4px]"
  >
    {options.map((opt) => (
      <ListboxOption
        key={opt}
        value={opt}
        className="cursor-pointer px-3 py-2 text-sm data-[focus]:bg-accent data-[focus]:text-foreground"
      >
        {opt}
      </ListboxOption>
    ))}
  </ListboxOptions>
</Listbox>
```

### RadioGroup

```tsx
import { Radio, RadioGroup } from "@headlessui/react";

<RadioGroup value={plan} onChange={setPlan}>
  {plans.map((p) => (
    <Radio
      key={p}
      value={p}
      className="flex cursor-pointer items-center gap-2 data-[checked]:text-primary"
    >
      <span className="flex h-4 w-4 items-center justify-center rounded-full border border-border data-[checked]:border-primary">
        <span className="hidden h-2 w-2 rounded-full bg-primary data-[checked]:block" />
      </span>
      {p}
    </Radio>
  ))}
</RadioGroup>
```

### Switch

```tsx
import { Switch } from "@headlessui/react";

<Switch
  checked={enabled}
  onChange={setEnabled}
  className="relative inline-flex h-6 w-11 items-center rounded-full bg-muted-foreground/30 transition data-[checked]:bg-primary"
>
  <span className="inline-block h-4 w-4 translate-x-1 rounded-full bg-white transition data-[checked]:translate-x-6" />
</Switch>
```

### Checkbox (v2)

```tsx
import { Checkbox } from "@headlessui/react";

<Checkbox
  checked={checked}
  onChange={setChecked}
  className="flex h-4 w-4 items-center justify-center rounded border border-border data-[checked]:border-primary data-[checked]:bg-primary"
>
  <svg className="hidden h-3 w-3 text-white data-[checked]:block" viewBox="0 0 12 12" fill="currentColor">
    <path d="M10 3L5 8.5 2.5 6" stroke="currentColor" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
</Checkbox>
```

### Dialog

```tsx
import { Dialog, DialogBackdrop, DialogPanel, DialogTitle } from "@headlessui/react";

<Dialog open={open} onClose={setOpen}>
  <DialogBackdrop className="fixed inset-0 z-40 bg-black/50" />
  <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
    <DialogPanel className="w-full max-w-md rounded-xl border border-border bg-surface p-6 shadow-xl">
      <DialogTitle className="text-lg font-semibold text-foreground">Title</DialogTitle>
    </DialogPanel>
  </div>
</Dialog>
```

### Menu (DropdownMenu)

```tsx
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/react";

<Menu as="div" className="relative">
  <MenuButton className="rounded-md border border-border px-3 py-1.5 text-sm">Options</MenuButton>
  <MenuItems
    anchor="bottom end"
    className="z-50 min-w-32 rounded-md border border-border bg-surface p-1 shadow-lg [--anchor-gap:4px]"
  >
    <MenuItem as="button" className="block w-full rounded px-3 py-1.5 text-left text-sm data-[focus]:bg-accent">
      Edit
    </MenuItem>
    <MenuItem as="button" className="block w-full rounded px-3 py-1.5 text-left text-sm text-destructive data-[focus]:bg-accent">
      Delete
    </MenuItem>
  </MenuItems>
</Menu>
```

### Popover

```tsx
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/react";

<Popover className="relative">
  <PopoverButton className="rounded-md border border-border px-3 py-1.5 text-sm">Info</PopoverButton>
  <PopoverPanel
    anchor="bottom"
    className="z-50 w-56 rounded-md border border-border bg-surface p-3 shadow-lg text-sm [--anchor-gap:4px]"
  >
    Popover content here.
  </PopoverPanel>
</Popover>
```

### Tabs

```tsx
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from "@headlessui/react";

<TabGroup>
  <TabList className="flex gap-1 rounded-lg bg-muted p-1">
    {tabs.map((t) => (
      <Tab
        key={t}
        className="rounded-md px-3 py-1.5 text-sm font-medium text-muted-foreground transition data-[selected]:bg-background data-[selected]:text-foreground data-[selected]:shadow-sm"
      >
        {t}
      </Tab>
    ))}
  </TabList>
  <TabPanels className="mt-4">
    {tabs.map((t) => (
      <TabPanel key={t}>{t} content</TabPanel>
    ))}
  </TabPanels>
</TabGroup>
```

## Vue API quick-reference (@headlessui/vue v1)

### Listbox

```vue
<script setup lang="ts">
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from "@headlessui/vue";
import { ref } from "vue";

const selected = ref("Next.js");
const options = ["Next.js", "Remix", "Astro", "SvelteKit"];
</script>

<template>
  <Listbox v-model="selected">
    <div class="relative">
      <ListboxButton class="relative w-full rounded-md border border-border bg-background px-3 py-2 text-left text-sm">
        {{ selected }}
      </ListboxButton>
      <ListboxOptions class="absolute z-50 mt-1 w-full rounded-md border border-border bg-surface shadow-lg">
        <ListboxOption
          v-for="opt in options"
          :key="opt"
          :value="opt"
          v-slot="{ active }"
          class="cursor-pointer"
        >
          <span :class="['block px-3 py-2 text-sm', active ? 'bg-accent text-foreground' : 'text-foreground']">
            {{ opt }}
          </span>
        </ListboxOption>
      </ListboxOptions>
    </div>
  </Listbox>
</template>
```

### RadioGroup

```vue
<script setup lang="ts">
import { RadioGroup, RadioGroupOption } from "@headlessui/vue";
import { ref } from "vue";

const plan = ref("Free");
const plans = ["Free", "Pro", "Enterprise"];
</script>

<template>
  <RadioGroup v-model="plan">
    <RadioGroupOption
      v-for="p in plans"
      :key="p"
      :value="p"
      v-slot="{ checked }"
      class="cursor-pointer"
    >
      <div class="flex items-center gap-2 py-1">
        <span :class="['flex h-4 w-4 items-center justify-center rounded-full border', checked ? 'border-primary' : 'border-border']">
          <span v-if="checked" class="h-2 w-2 rounded-full bg-primary" />
        </span>
        <span class="text-sm text-foreground">{{ p }}</span>
      </div>
    </RadioGroupOption>
  </RadioGroup>
</template>
```

### Switch

```vue
<script setup lang="ts">
import { Switch } from "@headlessui/vue";
import { ref } from "vue";

const enabled = ref(false);
</script>

<template>
  <Switch
    v-model="enabled"
    :class="['relative inline-flex h-6 w-11 items-center rounded-full transition', enabled ? 'bg-primary' : 'bg-muted-foreground/30']"
  >
    <span :class="['inline-block h-4 w-4 rounded-full bg-white transition', enabled ? 'translate-x-6' : 'translate-x-1']" />
  </Switch>
</template>
```

### Dialog

```vue
<script setup lang="ts">
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from "@headlessui/vue";
import { ref } from "vue";

const open = ref(false);
</script>

<template>
  <TransitionRoot :show="open" as="template">
    <Dialog @close="open = false">
      <TransitionChild
        enter="ease-out duration-200" enter-from="opacity-0" enter-to="opacity-100"
        leave="ease-in duration-150" leave-from="opacity-100" leave-to="opacity-0"
      >
        <div class="fixed inset-0 z-40 bg-black/50" />
      </TransitionChild>
      <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <TransitionChild
          enter="ease-out duration-200" enter-from="opacity-0 scale-95" enter-to="opacity-100 scale-100"
          leave="ease-in duration-150" leave-from="opacity-100 scale-100" leave-to="opacity-0 scale-95"
        >
          <DialogPanel class="w-full max-w-md rounded-xl border border-border bg-surface p-6 shadow-xl">
            <DialogTitle class="text-lg font-semibold text-foreground">Title</DialogTitle>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
```

### Menu (DropdownMenu)

```vue
<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
</script>

<template>
  <Menu as="div" class="relative">
    <MenuButton class="rounded-md border border-border px-3 py-1.5 text-sm">Options</MenuButton>
    <MenuItems class="absolute right-0 z-50 mt-1 min-w-32 rounded-md border border-border bg-surface p-1 shadow-lg">
      <MenuItem v-slot="{ active }">
        <button :class="['block w-full rounded px-3 py-1.5 text-left text-sm', active ? 'bg-accent' : '']">
          Edit
        </button>
      </MenuItem>
      <MenuItem v-slot="{ active }">
        <button :class="['block w-full rounded px-3 py-1.5 text-left text-sm text-destructive', active ? 'bg-accent' : '']">
          Delete
        </button>
      </MenuItem>
    </MenuItems>
  </Menu>
</template>
```

### Tabs

```vue
<script setup lang="ts">
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from "@headlessui/vue";

const tabs = ["Account", "Billing", "Security"];
</script>

<template>
  <TabGroup>
    <TabList class="flex gap-1 rounded-lg bg-muted p-1">
      <Tab
        v-for="tab in tabs"
        :key="tab"
        v-slot="{ selected }"
        class="focus:outline-none"
      >
        <span :class="['block rounded-md px-3 py-1.5 text-sm font-medium transition', selected ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground']">
          {{ tab }}
        </span>
      </Tab>
    </TabList>
    <TabPanels class="mt-4">
      <TabPanel v-for="tab in tabs" :key="tab">{{ tab }} content</TabPanel>
    </TabPanels>
  </TabGroup>
</template>
```

## Peer dependencies

| Skill slot       | React peer dep                    | Vue peer dep |
|------------------|-----------------------------------|--------------|
| Select           | none (Listbox built-in)           | none (Listbox built-in) |
| Checkbox         | none (Checkbox built-in v2)       | none (native `<input>`) |
| RadioGroup       | none (built-in)                   | none (built-in) |
| Switch           | none (built-in)                   | none (built-in) |
| Dialog / Sheet   | none (built-in)                   | none (built-in) |
| Menu             | none (built-in)                   | none (built-in) |
| Popover          | none (built-in)                   | none (built-in) |
| Tabs             | none (built-in)                   | none (built-in) |
| Chart            | `recharts` + `@types/recharts`    | `vue-chartjs` + `chart.js` |
| Calendar         | `react-day-picker`                | custom grid |

## Tailwind coexistence

Headless UI requires no Tailwind plugin. Components accept any Tailwind class via `className`/`class`. The `data-[state]` modifiers (`data-[checked]`, `data-[selected]`, `data-[focus]`, `data-[open]`, `data-[active]`) are the primary mechanism for styling interactive states.

In Tailwind v4 projects the `@variant` directive can create reusable state shorthands:

```css
/* globals.css */
@variant hfocus (&[data-focus]);
@variant hchecked (&[data-checked]);
@variant hselected (&[data-selected]);
```

## Graceful fallback

If `@headlessui/react` or `@headlessui/vue` installation fails, replace each headless component with plain HTML equivalents from `references/ui-library/custom-tailwind.md`. The `/library` route structure and sidebar navigation remain unchanged — only the component implementations differ.
