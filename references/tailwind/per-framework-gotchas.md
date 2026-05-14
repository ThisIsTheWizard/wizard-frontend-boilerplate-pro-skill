# Tailwind per-Framework Gotchas

Known incompatibilities, version constraints, and edge cases when pairing
Tailwind v3/v4 with each supported framework.

---

## Next.js

### v4 — `@tailwindcss/postcss` required

`create-next-app --tailwind` generates `postcss.config.mjs` with `tailwindcss`
as the plugin. For v4, replace it with `@tailwindcss/postcss`:

```js
plugins: { "@tailwindcss/postcss": {} }
```

The `tailwindcss` package as a direct PostCSS plugin is v3-only.

### v4 — Delete `tailwind.config.ts`

Next.js 15 + Tailwind v4 uses CSS-first configuration. A
`tailwind.config.ts` at the project root does nothing in v4 but can mislead
debugging. Delete it.

### v4 — `@import "tailwindcss"` before other imports

In `globals.css`, place `@import "tailwindcss"` before any other import
(including tokens). Out-of-order causes the v4 parser to miss classes.

### Turbopack

Turbopack (enabled via `--turbopack`) has known Tailwind v4 scan issues in
Next.js 15 early releases. Disable it with `--no-turbopack` unless the user
requests it.

---

## React + Vite

### v4 — Use `@tailwindcss/vite`, not PostCSS

Do not install `@tailwindcss/postcss` for Vite projects. The v4 integration for
Vite is `@tailwindcss/vite`:

```ts
import tailwindcss from "@tailwindcss/vite";
export default defineConfig({ plugins: [tailwindcss()] });
```

Mixing PostCSS with the Vite plugin produces double-processing and crashes.

### v4 — Plugin order matters

`tailwindcss()` must come before `react()` in the plugins array so CSS is
transformed before React's HMR layer runs.

### v3 — `transform`, `filter`, `backdrop-filter`

If using `transform`, `filter`, or `backdrop-filter` utilities in v3, the bare
classes must be present on the same element:

```html
<div class="transform filter backdrop-blur ...">
  <!-- both transform and filter must be bare classes -->
</div>
```

---

## Vue + Vite

### v4 — Use `@tailwindcss/vite`

Same constraint as React + Vite. Use the Vite plugin, not PostCSS.

### v4 — Confirm `@/` alias in `vite.config.ts`

`create-vue` generates the `@/` alias using `path.resolve(__dirname, "./src")`.
Verify it is present before Phase 6; some versions of `create-vue` omit it.

### v3 — Content glob must include `.vue`

v3's content scanner does not include `.vue` files by default. The content array
must explicitly list `**/*.vue`:

```js
content: ["./index.html", "./src/**/*.{vue,js,ts}"]
```

---

## Nuxt

### v4 — `@nuxtjs/tailwindcss` module

Nuxt 4 uses the `@nuxtjs/tailwindcss` module for Tailwind v4 integration. The
module accepts `tailwindcss` v4 as a peer. Confirm the module version in the
npm registry before scaffolding — this area evolves quickly.

```ts
export default defineNuxtConfig({
  modules: ["@nuxtjs/tailwindcss"],
  tailwindcss: { cssPath: "~/assets/styles/globals.css" },
});
```

### v4 — No `tailwind.config.ts`

When using `@nuxtjs/tailwindcss` in v4 mode, design tokens live in CSS
(`@theme` block) rather than `tailwind.config.ts`. The module handles config
internally.

### v3 — PostCSS via `nuxt.config.ts`

Do not create a standalone `postcss.config.mjs` for Nuxt v3. Configure PostCSS
in `nuxt.config.ts`:

```ts
postcss: {
  plugins: { tailwindcss: {}, autoprefixer: {} },
}
```

---

## SvelteKit

### v4 — Plugin order in `vite.config.ts`

`tailwindcss()` must come after `sveltekit()`:

```ts
plugins: [sveltekit(), tailwindcss()]
```

Reversing the order causes Tailwind to emit utilities after Svelte's scoping
layer, breaking specificity.

### v3 — `content` must include `.svelte`

```js
content: ["./src/**/*.{html,js,ts,svelte}"]
```

---

## Version compatibility matrix

| Framework | Tailwind v4 | Tailwind v3 |
|---|---|---|
| Next.js 15 | Yes — `@tailwindcss/postcss` | Yes |
| Next.js 14 | Yes — `@tailwindcss/postcss` | Yes |
| React + Vite | Yes — `@tailwindcss/vite` | Yes |
| Vue 3.5+ | Yes — `@tailwindcss/vite` | Yes |
| Nuxt 4 | Yes — `@nuxtjs/tailwindcss` | Yes |
| SvelteKit | Yes — `@tailwindcss/vite` | Yes |

As of mid-2025, all listed framework versions are compatible with v4.
Check npm registry for the latest compatibility status before scaffolding if
the user is on an older framework version.