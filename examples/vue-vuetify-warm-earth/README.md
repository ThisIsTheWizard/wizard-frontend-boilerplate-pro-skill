# Example: Warm Earth · Vue 3 · Vuetify

A grounded, content-friendly admin panel — great for editorial tools and
data-heavy dashboards.

## Prompt

```
New Vue 3 app — Warm Earth theme, Vuetify, TypeScript, call it "earth-admin"
```

## Interview answers

| Question | Answer |
|---|---|
| Framework | Vue 3 |
| UI library | Vuetify |
| Language | TypeScript |
| Color theme | Warm Earth (stone neutral + amber accent) |
| Project name | earth-admin |
| Package manager | *(auto-detected)* |
| Tailwind version | none *(Vuetify uses its own CSS system)* |

## What gets generated

```
earth-admin/
├── src/
│   ├── main.ts                     # createApp + Vuetify plugin mount
│   ├── App.vue                     # Root component
│   ├── plugins/
│   │   ├── vuetify.ts              # createVuetify with Warm Earth token bridge
│   │   └── theme-provider.ts       # localStorage + prefers-color-scheme
│   ├── router/
│   │   └── index.ts                # Vue Router 4 routes
│   ├── components/
│   │   ├── AppLayout.vue           # Sidebar + header wrapper
│   │   ├── Sidebar.vue
│   │   ├── CodeBlock.vue
│   │   └── ui/                     # 28 Vuetify-backed components
│   │       ├── Button.vue
│   │       ├── Input.vue
│   │       └── ... (26 more)
│   ├── views/
│   │   ├── LibraryView.vue         # /library landing
│   │   ├── InputsView.vue
│   │   ├── DisplayView.vue
│   │   ├── FeedbackView.vue
│   │   ├── NavigationView.vue
│   │   ├── OverlayView.vue
│   │   └── DataVizView.vue
│   └── styles/
│       └── tokens.css              # OKLCH Warm Earth semantic tokens
├── vite.config.ts
└── tsconfig.json
```

## Vuetify theme bridge

The Vuetify theme is wired to the OKLCH tokens so light/dark switching works
through both the CSS variable system and Vuetify's `useTheme()`:

```ts
// src/plugins/vuetify.ts
import { createVuetify } from "vuetify";

export default createVuetify({
  theme: {
    defaultTheme: "warmEarthLight",
    themes: {
      warmEarthLight: {
        dark: false,
        colors: {
          background: "#fafaf9",   // neutral-50
          surface:    "#f5f5f4",   // neutral-100
          primary:    "#d97706",   // amber-600
          secondary:  "#78716c",   // stone-500
          error:      "#dc2626",
        },
      },
      warmEarthDark: {
        dark: true,
        colors: {
          background: "#1c1917",   // neutral-950
          surface:    "#292524",   // neutral-900
          primary:    "#fbbf24",   // amber-400
          secondary:  "#a8a29e",   // stone-400
          error:      "#f87171",
        },
      },
    },
  },
});
```

## Key packages installed

```json
{
  "dependencies": {
    "vue": "^3.5.0",
    "vue-router": "^4.4.0",
    "vuetify": "^3.7.0",
    "@mdi/font": "^7.4.0"
  },
  "devDependencies": {
    "vite": "^6.0.0",
    "vite-plugin-vuetify": "^2.0.0",
    "typescript": "^5.6.0",
    "vue-tsc": "^2.1.0"
  }
}
```
