# Theming — CSS Variable Tokens & Dark Mode Strategy

## Table of contents

1. [Token architecture](#1-token-architecture)
2. [Token hierarchy](#2-token-hierarchy)
3. [CSS variable reference](#3-css-variable-reference)
4. [Light theme — :root block](#4-light-theme--root-block)
5. [Dark theme — .dark block](#5-dark-theme--dark-block)
6. [Tailwind @theme integration](#6-tailwind-theme-integration)
7. [Dark mode strategy](#7-dark-mode-strategy)
8. [FOUC prevention](#8-fouc-prevention)
9. [Custom color integration](#9-custom-color-integration)
10. [Verification checklist](#10-verification-checklist)

---

## 1. Token architecture

The theme system uses a three-layer token architecture:

```
Layer 1 — Palette tokens (@theme block)
  └── Raw color scales: --color-neutral-50 … --color-neutral-950
                          --color-accent-50   … --color-accent-950

Layer 2 — Semantic tokens (:root / .dark)
  └── Purposeful aliases: --background, --foreground, --primary, etc.

Layer 3 — Component tokens (component CSS)
  └── Inherit from Layer 2 via var(--semantic-token)
```

Palette tokens are static and compile-time. Semantic tokens are runtime-swappable via theme class. Components only ever reference Layer 2; they never reference Layer 1 directly.

---

## 2. Token hierarchy

| Layer | Location | Purpose | Swappable at runtime? |
|---|---|---|---|
| Palette | `@theme {}` in `tokens.css` | Raw 50–950 OKLCH scales | No (compile-time) |
| Semantic | `:root {}` / `.dark {}` in `tokens.css` | Purpose-driven aliases | Yes — via theme class |
| Component | Inline `var(--token)` in component classes | Component coloring | Yes — inherits from semantic |

Palette tokens live in `@theme` so Tailwind v4 generates utility classes (`bg-neutral-500`, `text-accent-600`). Semantic tokens live in regular CSS blocks so they can be swapped without rebuilding the Tailwind pipeline.

---

## 3. CSS variable reference

All semantic tokens declared in both `:root` (light) and `.dark` (dark).

### Surface tokens

| Token | Light value | Dark value | Usage |
|---|---|---|---|
| `--background` | `var(--color-neutral-50)` | `var(--color-neutral-950)` | Page background |
| `--foreground` | `var(--color-neutral-950)` | `var(--color-neutral-50)` | Primary text |
| `--surface` | `var(--color-neutral-100)` | `var(--color-neutral-900)` | Cards, panels |
| `--muted` | `var(--color-neutral-300)` | `var(--color-neutral-600)` | Secondary text, placeholders |
| `--muted-foreground` | `var(--color-neutral-500)` | `var(--color-neutral-400)` | Muted label text |

### Border tokens

| Token | Light value | Dark value | Usage |
|---|---|---|---|
| `--border` | `var(--color-neutral-200)` | `var(--color-neutral-800)` | Default borders |
| `--input` | `var(--color-neutral-200)` | `var(--color-neutral-800)` | Input field borders |
| `--ring` | `var(--color-accent-400)` | `var(--color-accent-400)` | Focus ring (static) |

### Primary / accent tokens

| Token | Light value | Dark value | Usage |
|---|---|---|---|
| `--primary` | `var(--color-accent-500)` | `var(--color-accent-400)` | Primary actions |
| `--primary-foreground` | `var(--color-neutral-50)` | `var(--color-neutral-950)` | Text on primary |
| `--secondary` | `var(--color-neutral-200)` | `var(--color-neutral-700)` | Secondary actions |
| `--secondary-foreground` | `var(--color-neutral-900)` | `var(--color-neutral-50)` | Text on secondary |
| `--accent` | `var(--color-neutral-100)` | `var(--color-neutral-800)` | Hover / emphasis surfaces |
| `--accent-foreground` | `var(--color-neutral-900)` | `var(--color-neutral-50)` | Text on accent |

### Destructive / destructive-foreground

| Token | Light value | Dark value | Usage |
|---|---|---|---|
| `--destructive` | `var(--color-neutral-900)` | `var(--color-neutral-800)` | Destructive actions |
| `--destructive-foreground` | `var(--color-neutral-50)` | `var(--color-neutral-50)` | Text on destructive |

### Component-specific tokens

| Token | Light value | Dark value | Usage |
|---|---|---|---|
| `--card` | `var(--color-neutral-50)` | `var(--color-neutral-900)` | Card background |
| `--card-foreground` | `var(--color-neutral-950)` | `var(--color-neutral-50)` | Card text |
| `--popover` | `var(--color-neutral-50)` | `var(--color-neutral-900)` | Popover / dropdown bg |
| `--popover-foreground` | `var(--color-neutral-950)` | `var(--color-neutral-50)` | Popover text |
| `--border` | `var(--color-neutral-200)` | `var(--color-neutral-800)` | Card / popover borders |
| `--radius` | `var(--radius-md)` | `var(--radius-md)` | Border radius (static) |

---

## 4. Light theme — :root block

```css
:root {
  /* Surface */
  --background: var(--color-neutral-50);
  --foreground: var(--color-neutral-950);
  --surface: var(--color-neutral-100);
  --muted: var(--color-neutral-300);
  --muted-foreground: var(--color-neutral-500);

  /* Borders */
  --border: var(--color-neutral-200);
  --input: var(--color-neutral-200);
  --ring: var(--color-accent-400);

  /* Primary / Accent */
  --primary: var(--color-accent-500);
  --primary-foreground: var(--color-neutral-50);
  --secondary: var(--color-neutral-200);
  --secondary-foreground: var(--color-neutral-900);
  --accent: var(--color-neutral-100);
  --accent-foreground: var(--color-neutral-900);

  /* Destructive */
  --destructive: var(--color-neutral-900);
  --destructive-foreground: var(--color-neutral-50);

  /* Component */
  --card: var(--color-neutral-50);
  --card-foreground: var(--color-neutral-950);
  --popover: var(--color-neutral-50);
  --popover-foreground: var(--color-neutral-950);

  /* Radius */
  --radius: var(--radius-md);
}
```

---

## 5. Dark theme — .dark block

```css
.dark {
  /* Surface */
  --background: var(--color-neutral-950);
  --foreground: var(--color-neutral-50);
  --surface: var(--color-neutral-900);
  --muted: var(--color-neutral-600);
  --muted-foreground: var(--color-neutral-400);

  /* Borders */
  --border: var(--color-neutral-800);
  --input: var(--color-neutral-800);
  --ring: var(--color-accent-400);

  /* Primary / Accent */
  --primary: var(--color-accent-400);
  --primary-foreground: var(--color-neutral-950);
  --secondary: var(--color-neutral-700);
  --secondary-foreground: var(--color-neutral-50);
  --accent: var(--color-neutral-800);
  --accent-foreground: var(--color-neutral-50);

  /* Destructive */
  --destructive: var(--color-neutral-800);
  --destructive-foreground: var(--color-neutral-50);

  /* Component */
  --card: var(--color-neutral-900);
  --card-foreground: var(--color-neutral-50);
  --popover: var(--color-neutral-900);
  --popover-foreground: var(--color-neutral-50);
}
```

---

## 6. Tailwind @theme integration

Expose semantic tokens as Tailwind utilities by adding them to the `@theme` block. This lets components use `bg-background` instead of `bg-[var(--background)]`.

```css
@theme {
  /* Palette scale tokens — generated by generate_palette.py */
  --color-neutral-50: oklch(97% 0.01 265);
  --color-neutral-100: oklch(93% 0.03 265);
  /* … 50–950 … */
  --color-neutral-950: oklch(15% 0.05 265);
  --color-accent-50: oklch(97% 0.01 265);
  /* … 50–950 … */
  --color-accent-950: oklch(15% 0.05 265);

  /* Semantic aliases — these generate bg-background, text-foreground, etc. */
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-surface: var(--surface);
  --color-muted: var(--color-neutral-300);
  --color-muted-foreground: var(--color-neutral-500);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-accent: var(--color-neutral-100);
  --color-accent-foreground: var(--color-neutral-900);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
}
```

The chain resolves as: `bg-background` → `var(--color-background)` → `var(--background)` → `:root { --background: var(--color-neutral-50) }` (light) or `.dark { --background: var(--color-neutral-950) }` (dark).

---

## 7. Dark mode strategy

### Class-based toggle (v4 built-in)

Tailwind v4 automatically handles `.dark` variant. No config entry required.

**Activation:** Apply `.dark` class to `<html>` via ThemeProvider. All `dark:` prefixed utilities activate when an ancestor has `.dark`.

```css
/* Component using semantic token — no dark: variant needed */
<div class="bg-background text-foreground">…</div>

/* Component using raw scale — use dark: variant */
<div class="bg-neutral-100 dark:bg-neutral-900">…</div>
```

**ThemeProvider behavior:**
1. On mount, read `localStorage.getItem('theme')`.
2. If null, fall back to `window.matchMedia('(prefers-color-scheme: dark)')`.
3. Apply `"dark"` or `""` to `document.documentElement.classList`.
4. Re-read on `storage` event (cross-tab sync).

**System preference sync:** The ThemeProvider watches `matchMedia` for system preference changes and updates the class accordingly, unless the user has explicitly set a preference (stored in localStorage).

### Per-framework injection point

| Framework | ThemeProvider file | Inject in |
|---|---|---|
| Next.js | `src/components/ThemeProvider.tsx` | `src/app/layout.tsx` |
| React + Vite | `src/components/ThemeProvider.tsx` | `src/App.tsx` / `src/main.tsx` |
| Vue / Nuxt | `src/plugins/theme-provider.ts` | `nuxt.config.ts` plugin / `main.ts` |
| SvelteKit | `src/lib/theme-provider.ts` | `src/routes/+layout.svelte` |

---

## 8. FOUC prevention

Flash of unstyled content occurs when the browser renders the page before the ThemeProvider JavaScript executes. Prevention requires an inline script in `<head>` that runs synchronously before any CSS is parsed.

### Inline script (universal)

Add this as the first child of `<head>` in the root layout (or equivalent):

```html
<script>
  (function () {
    var stored = localStorage.getItem('theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var theme = stored || (prefersDark ? 'dark' : 'light');
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    }
  })();
</script>
```

This script runs before the body is rendered, ensuring `<html class="dark">` (or not) is already set before CSS custom properties are evaluated.

For Next.js App Router, add to `src/app/layout.tsx` inside `<head>` via `children` in a `<Script>` component with `strategy="beforeInteractive"`.

For React + Vite / Vue / SvelteKit, add the inline `<script>` tag directly to the HTML template.

---

## 9. Custom color integration

When the user picks "Custom" and provides hex or OKLCH values, `generate_palette.py` generates the full 50–950 scale from the supplied base colors. The output format is identical to a preset, so no additional theming steps are needed.

Input: one neutral + one accent (hex or OKLCH). Output: full OKLCH scale for each, written into the `@theme` block.

If the user provides OKLCH values directly, use them as-is. If hex is provided, convert to OKLCH before generating the scale.

The scale generation algorithm:
1. Take the 500 value (user-provided or interpolated).
2. Generate 50–400 by decreasing lightness.
3. Generate 600–950 by increasing lightness and decreasing chroma.
4. Cap chroma at `0.2` for very light values (50–100) to avoid过饱和.
5. Target 15 steps total: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950.

---

## 10. Verification checklist

- [ ] `:root` and `.dark` blocks both declare all semantic tokens
- [ ] `@theme` includes semantic token aliases (`--color-background`, etc.)
- [ ] Inline FOUC-prevention script is present in `<head>`
- [ ] ThemeProvider reads localStorage first, then `prefers-color-scheme`
- [ ] ThemeProvider watches `storage` and `matchMedia` events
- [ ] All components use semantic tokens (no hardcoded palette values in component classes)
- [ ] `generate_palette.py` produces the same scale for preset and custom inputs
- [ ] `verify_contrast.py` passes for both light and dark in all foreground/background pairs