# Example: Ocean · SvelteKit · DaisyUI

A cool, data-focused starter built on Svelte 5 runes — perfect for developer
tools, dashboards, and data-heavy UIs.

## Prompt

```
SvelteKit app with DaisyUI and the Ocean color preset, call it "ocean-kit"
```

## Interview answers

| Question | Answer |
|---|---|
| Framework | SvelteKit (Svelte 5) |
| UI library | DaisyUI |
| Language | TypeScript |
| Color theme | Ocean (slate neutral + cyan accent) |
| Project name | ocean-kit |
| Package manager | *(auto-detected)* |
| Tailwind version | v4 *(DaisyUI 4 supports Tailwind v4)* |

## What gets generated

```
ocean-kit/
├── src/
│   ├── app.html                    # FOUC-prevention script in <head>
│   ├── lib/
│   │   ├── theme-provider.ts       # $state-based theme store (Svelte 5)
│   │   ├── utils/
│   │   │   └── utils.ts            # cn() helper
│   │   ├── styles/
│   │   │   └── tokens.css          # OKLCH Ocean palette + semantic tokens
│   │   └── components/
│   │       ├── ui/                 # 28 DaisyUI-backed components
│   │       │   ├── Button.svelte
│   │       │   ├── Input.svelte
│   │       │   └── ... (26 more)
│   │       └── CodeBlock.svelte
│   └── routes/
│       ├── +layout.svelte          # Root layout, initTheme() call
│       ├── +page.svelte            # Redirects to /library
│       └── library/
│           ├── +layout.svelte      # Sidebar + Header
│           ├── +page.svelte        # /library landing
│           ├── inputs/+page.svelte
│           ├── display/+page.svelte
│           ├── feedback/+page.svelte
│           ├── navigation/+page.svelte
│           ├── overlay/+page.svelte
│           └── data-viz/+page.svelte
├── tailwind.config.ts              # DaisyUI plugin wired to Ocean tokens
└── tsconfig.json
```

## DaisyUI theme bridge

DaisyUI's CSS variable system is mapped to the Ocean OKLCH tokens so the
built-in `data-theme` attribute and the custom `dark` class work in sync:

```css
/* src/lib/styles/tokens.css */
[data-theme="ocean-light"],
:root {
  --color-background:  oklch(98.4% 0.003 222.0);
  --color-foreground:  oklch(12.9% 0.026 222.0);
  --color-accent:      oklch(55.4% 0.163 213.0);  /* cyan-500 */

  /* DaisyUI semantic bridge */
  --p:  55.4% 0.163 213.0;   /* primary → ocean accent */
  --pf: 98.4% 0.003 222.0;   /* primary-focus */
  --pc: 98.4% 0.003 222.0;   /* primary-content */
  --b1: 98.4% 0.003 222.0;   /* base-100 */
  --b2: 96.8% 0.006 222.0;   /* base-200 */
  --b3: 92.9% 0.012 222.0;   /* base-300 */
  --bc: 12.9% 0.026 222.0;   /* base-content */
}

[data-theme="ocean-dark"] {
  --b1: 12.9% 0.026 222.0;
  --b2: 20.8% 0.030 222.0;
  --b3: 27.9% 0.035 222.0;
  --bc: 98.4% 0.003 222.0;
  --p:  70.5% 0.158 213.0;   /* cyan-400 for dark mode */
}
```

## Svelte 5 theme provider

The theme provider uses runes instead of stores:

```ts
// src/lib/theme-provider.ts
let theme = $state<"light" | "dark">("light");

export function initTheme() {
  const stored = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  theme = (stored as "light" | "dark") ?? (prefersDark ? "dark" : "light");
  applyTheme(theme);
}

export function toggleTheme() {
  theme = theme === "light" ? "dark" : "light";
  localStorage.setItem("theme", theme);
  applyTheme(theme);
}

function applyTheme(t: "light" | "dark") {
  document.documentElement.setAttribute("data-theme", `ocean-${t}`);
  document.documentElement.classList.toggle("dark", t === "dark");
}

export { theme };
```

## Key packages installed

```json
{
  "dependencies": {
    "daisyui": "^4.12.0"
  },
  "devDependencies": {
    "@sveltejs/kit": "^2.7.0",
    "svelte": "^5.0.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/vite": "^4.0.0",
    "typescript": "^5.6.0",
    "svelte-check": "^4.0.0"
  }
}
```
