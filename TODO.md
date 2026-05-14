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
- [ ] `references/component-catalog.md` — all 28 components (name, category, deps, props interface, source mapping)
- [ ] `references/showcase-layout.md` — sidebar nav, header, category routing, CodeBlock utility
- [ ] `references/portability.md` — notes for non-Claude agents, tested agent list

## 4. Assets — color system
- [ ] Write `scripts/generate_palette.py` first (OKLCH algorithm)
- [ ] Generate `assets/color-presets.json` using the same algorithm (8 presets + custom slot, OKLCH 50–950 scales, light/dark CSS var mappings)

## 5. Assets — showcase templates
- [ ] `assets/showcase-templates/react/layout.tsx.template`
- [ ] `assets/showcase-templates/react/sidebar.tsx.template`
- [ ] `assets/showcase-templates/react/inputs.tsx.template`
- [ ] `assets/showcase-templates/react/display.tsx.template`
- [ ] `assets/showcase-templates/react/feedback.tsx.template`
- [ ] `assets/showcase-templates/react/navigation.tsx.template`
- [ ] `assets/showcase-templates/react/overlay.tsx.template`
- [ ] `assets/showcase-templates/react/data-viz.tsx.template`
- [ ] `assets/showcase-templates/vue/AppLayout.vue.template`
- [ ] `assets/showcase-templates/vue/Sidebar.vue.template`
- [ ] `assets/showcase-templates/vue/pages/` — 6 category page templates
- [ ] `assets/showcase-templates/svelte/+layout.svelte.template`
- [ ] `assets/showcase-templates/svelte/routes/` — 6 category route templates

## 6. Assets — theme providers
- [ ] `assets/theme-provider/react.tsx` — localStorage + prefers-color-scheme + FOUC prevention
- [ ] `assets/theme-provider/vue.ts`
- [ ] `assets/theme-provider/svelte.ts`

## 7. Assets — misc
- [ ] `assets/snippet-template.txt` — collapsible code-snippet block format

## 8. Scripts
- [ ] `scripts/check_versions.sh` — query npm registry for latest versions
- [ ] `scripts/generate_palette.py` — hex/OKLCH → 50–950 scale
- [ ] `scripts/verify_contrast.py` — WCAG AA gate
- [ ] `scripts/detect_package_manager.sh` — pnpm/yarn/npm/bun detection
- [ ] `scripts/locate_ui_ux_pro_max.sh` — find sibling skill on disk
- [ ] Validate all `.sh` files with `bash -n`
- [ ] Validate all `.py` files with `python -m py_compile`

## 9. Workflow doc
- [ ] Write `workflow.md` — detailed playbook with verbatim commands for all 7 phases

## 10. End-to-end validation (simulated runs)
- [ ] **Run 1:** Next.js 15 + TS + Tailwind v4 + Modern Slate — dev server starts, all 6 routes render, theme toggle works, WCAG AA passes
- [ ] **Run 2:** Vue 3.5 + TS + Tailwind v4 + Custom hex `#0ea5e9` / `#f59e0b` — same checks
- [ ] **Run 3:** SvelteKit + TS + Tailwind v4 + Monochrome — same checks

## 11. Portability check
- [ ] Confirm `SKILL.md` contains no Claude-specific syntax (`<*>` tags, internal tool names)
- [ ] Confirm `AGENTS.md` contains no Claude-specific syntax
- [ ] Confirm all actions are shell commands or file edits executable by a generic agent
