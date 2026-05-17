# TODO — `wizard-frontend-boilerplate-pro` Skill Build

## 1. Directory structure
- [x] Create full directory tree as defined in PLAN.md

## 2. Entry points
- [x] Write `SKILL.md` (≤400 lines, 7-phase workflow, references point to detail files)
- [x] Write `AGENTS.md` (one-line redirect to SKILL.md)

## 3. Reference files (`references/`)
- [x] `references/frameworks/nextjs.md` — create-next-app, App Router setup
- [x] `references/frameworks/react-vite.md`
- [x] `references/frameworks/vue.md` — Vue 3.5+
- [x] `references/frameworks/nuxt.md` — Nuxt 4
- [x] `references/frameworks/svelte-kit.md` — Svelte 5
- [x] All frontend app should have home page (/) redirected to /library page and components showcase will be shown in /library page. Update plan, existing created files and plan for next.
- [x] `references/tailwind/v4-setup.md` — @tailwindcss/postcss, @theme
- [x] `references/tailwind/v3-setup.md` — fallback
- [x] `references/tailwind/per-framework-gotchas.md`
- [X] `references/ui-library/ui-ux-pro-max-bridge.md` — integration contract, search paths, name-mapping table, per-framework adaptation rules, graceful fallback section
- [x] `references/ui-library/custom-tailwind.md` — standalone fallback component implementations
- [x] `references/ui-library/framework-adapters/react-adapter.md`
- [x] `references/ui-library/framework-adapters/vue-adapter.md`
- [x] `references/ui-library/framework-adapters/svelte-adapter.md`
- [x] `references/theming.md` — CSS var tokens, dark mode strategy
- [x] `references/component-catalog.md` — all 28 components (name, category, deps, props interface, source mapping)
- [x] `references/showcase-layout.md` — sidebar nav, header, category routing, CodeBlock utility
- [x] `references/portability.md` — notes for non-Claude agents, tested agent list

## 4. Assets — color system
- [x] Write `scripts/generate_palette.py` first (OKLCH algorithm)
- [x] Generate `assets/color-presets.json` using the same algorithm (8 presets + custom slot, OKLCH 50–950 scales, light/dark CSS var mappings)

## 5. Assets — showcase templates
- [x] `assets/showcase-templates/react/layout.tsx.template`
- [x] `assets/showcase-templates/react/sidebar.tsx.template`
- [x] `assets/showcase-templates/react/inputs.tsx.template`
- [x] `assets/showcase-templates/react/display.tsx.template`
- [x] `assets/showcase-templates/react/feedback.tsx.template`
- [x] `assets/showcase-templates/react/navigation.tsx.template`
- [x] `assets/showcase-templates/react/overlay.tsx.template`
- [x] `assets/showcase-templates/react/data-viz.tsx.template`
- [x] `assets/showcase-templates/vue/AppLayout.vue.template`
- [x] `assets/showcase-templates/vue/Sidebar.vue.template`
- [x] `assets/showcase-templates/vue/pages/` — 6 category page templates
- [x] `assets/showcase-templates/svelte/+layout.svelte.template`
- [x] `assets/showcase-templates/svelte/routes/` — 6 category route templates

## 6. Assets — theme providers
- [x] `assets/theme-provider/react.tsx` — localStorage + prefers-color-scheme + FOUC prevention
- [x] `assets/theme-provider/vue.ts`
- [x] `assets/theme-provider/svelte.ts`

## 7. Assets — misc
- [x] `assets/snippet-template.txt` — collapsible code-snippet block format

## 8. Scripts
- [x] `scripts/check_versions.sh` — query npm registry for latest versions
- [x] `scripts/generate_palette.py` — hex/OKLCH → 50–950 scale
- [x] `scripts/verify_contrast.py` — WCAG AA gate
- [x] `scripts/detect_package_manager.sh` — pnpm/yarn/npm/bun detection
- [x] `scripts/locate_ui_ux_pro_max.sh` — find sibling skill on disk
- [x] Validate all `.sh` files with `bash -n`
- [x] Validate all `.py` files with `python -m py_compile`

## 9. Workflow doc
- [x] Write `workflow.md` — detailed playbook with verbatim commands for all 7 phases

## 10. Public distribution files
- [x] Write `skill.json` — root manifest (name, version, owner, plugins array)
- [x] Write `.claude-plugin/plugin.json` — Claude Code plugin metadata (keywords, category, capabilities)
- [x] Write `.claude-plugin/marketplace.json` — marketplace distribution entry
- [x] Write `README.md` — public-facing repo documentation (distinct from `SKILL.md`)
- [x] Add `LICENSE` — MIT license
- [x] Create `.claude/skills/wizard-frontend-boilerplate-pro/` entry point (symlink or copy of `SKILL.md`)

## 11. End-to-end validation (simulated runs)
- [x] **Run 1:** Next.js 15 + TS + Tailwind v4 + Modern Slate — dev server starts, all 6 routes render, theme toggle works, WCAG AA passes
- [x] **Run 2:** Vue 3.5 + TS + Tailwind v4 + Custom hex `#0ea5e9` / `#f59e0b` — same checks
- [x] **Run 3:** SvelteKit + TS + Tailwind v4 + Monochrome — same checks

## 12. Portability check
- [x] Confirm `SKILL.md` contains no Claude-specific syntax (`<*>` tags, internal tool names)
- [x] Confirm `AGENTS.md` contains no Claude-specific syntax
- [x] Confirm all actions are shell commands or file edits executable by a generic agent

## 13. Multi-library infrastructure — UI_LIB selection
- [x] Update `SKILL.md` Phase 1 to add Q8 `UI_LIB` selection question with framework compatibility filter
- [x] Update `SKILL.md` Phase 5 to route to `references/ui-library/<UI_LIB>.md` when `UI_LIB != custom`
- [x] Update `SKILL.md` Phase 6 to use `assets/showcase-templates/<framework>-<UI_LIB>/` when `UI_LIB != custom`
- [x] Update `SKILL.md` Reference index table with new `references/ui-library/<library>.md` entries
- [x] Update `workflow.md` Phase 1 to add Q8 (UI library) with compatibility table
- [x] Update `workflow.md` Phase 5 to add `UI_LIB` routing block replacing binary skill-found/custom logic
- [x] Update `workflow.md` Phase 6 to resolve template folder by `UI_LIB`
- [x] Add library component mapping table to `references/component-catalog.md`

## 14. shadcn/ui — reference file
- [x] Write `references/ui-library/shadcn.md`
  - CLI init (`npx shadcn@latest init`), component add commands
  - Theming: CSS var 1:1 mapping to existing token system
  - Per-framework notes: React (native), Vue (shadcn-vue), Svelte (shadcn-svelte)
  - Peer deps per component

## 15. shadcn/ui — showcase templates
- [x] `assets/showcase-templates/react-shadcn/` — layout + sidebar + 6 category pages (8 files)
- [x] `assets/showcase-templates/vue-shadcn/` — 8 files
- [x] `assets/showcase-templates/svelte-shadcn/` — 8 files

## 16. Material UI — reference file
- [x] Write `references/ui-library/mui.md`
  - `@mui/material`, `@emotion/react`, `@emotion/styled` install
  - `createTheme()` bridge mapping existing CSS tokens to MUI palette/typography
  - Next.js App Router SSR cache (`@mui/material-nextjs`) setup
  - React-only constraint documented

## 17. Material UI — showcase templates
- [x] `assets/showcase-templates/react-mui/` — 8 files using MUI native components

## 18. Bootstrap — reference file
- [x] Write `references/ui-library/bootstrap.md`
  - npm install: `react-bootstrap` / `bootstrap-vue-next` / svelte approach
  - SCSS variable override strategy for theming bridge
  - CDN alternative for prototyping

## 19. Bootstrap — showcase templates
- [x] `assets/showcase-templates/react-bootstrap/` — 8 files
- [x] `assets/showcase-templates/vue-bootstrap/` — 8 files
- [x] `assets/showcase-templates/svelte-bootstrap/` — 8 files

## 20. DaisyUI — reference file + templates
- [x] Write `references/ui-library/daisy.md` (Tailwind plugin, minimal bridge needed)
- [x] `assets/showcase-templates/react-daisy/` — 8 files
- [x] `assets/showcase-templates/vue-daisy/` — 8 files
- [x] `assets/showcase-templates/svelte-daisy/` — 8 files

## 21. Chakra UI — reference file + templates
- [x] Write `references/ui-library/chakra.md` — `ChakraProvider` setup, token-to-CSS-var bridge
- [x] `assets/showcase-templates/react-chakra/` — 8 files

## 22. Mantine — reference file + templates
- [x] Write `references/ui-library/mantine.md` — `MantineProvider`, CSS variables mode, theming
- [x] `assets/showcase-templates/react-mantine/` — 8 files

## 23. Ant Design — reference file + templates
- [x] Write `references/ui-library/antd.md` — `ConfigProvider` theme tokens, Next.js App Router notes
- [x] `assets/showcase-templates/react-antd/` — 8 files

## 24. PrimeVue — reference file + templates
- [ ] Write `references/ui-library/primevue.md` — plugin setup, PrimeVue theming presets
- [ ] `assets/showcase-templates/vue-primevue/` — 8 files

## 25. Vuetify — reference file + templates
- [ ] Write `references/ui-library/vuetify.md` — `createVuetify`, blueprint, CSS var bridge
- [ ] `assets/showcase-templates/vue-vuetify/` — 8 files

## 27. Headless UI — reference file + templates
- [ ] Write `references/ui-library/headlessui.md`
  - `@headlessui/react` (React) and `@headlessui/vue` (Vue) install + wiring
  - Component coverage map (which of the 28 slots are native vs custom Tailwind)
  - Tailwind pairing — always installed, pairs with existing token system
- [ ] `assets/showcase-templates/react-headlessui/` — 8 files
- [ ] `assets/showcase-templates/vue-headlessui/` — 8 files

## 28. NextUI / HeroUI — reference file + templates
- [ ] Write `references/ui-library/heroui.md`
  - `@heroui/react` install, `HeroUIProvider` wiring, Tailwind config
  - Theming bridge: map existing CSS variable tokens to HeroUI theme config
  - React/Next.js only constraint noted
- [ ] `assets/showcase-templates/react-heroui/` — 8 files

## 29. Element Plus — reference file + templates
- [ ] Write `references/ui-library/elementplus.md`
  - `element-plus` install, auto-import setup (`unplugin-vue-components`)
  - SCSS variable override strategy for theming bridge to CSS tokens
  - Vue/Nuxt only constraint noted; echarts pairing for Chart slot
- [ ] `assets/showcase-templates/vue-elementplus/` — 8 files

## 26. Multi-library end-to-end validation
- [ ] Simulated run: Next.js + shadcn/ui — all 6 routes render, dark mode works
- [ ] Simulated run: Next.js + MUI — theme bridge verified, SSR no flash
- [ ] Simulated run: Vue + Bootstrap — all routes render, responsive
- [ ] Confirm Phase 1 menu hides Vue-incompatible libraries when Vue is selected
- [ ] Confirm existing `custom` path still works unchanged
