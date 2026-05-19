# Contributing to Wizard Frontend Boilerplate Pro

Thanks for wanting to improve the skill! This guide covers the four most common
contribution types: adding a color preset, adding a UI library, adding a
framework, and fixing a bug in an existing template or reference file.

> **Maintainer?** See [docs/development.md](docs/development.md) for additional
> sections covering the theme provider contract, `color-presets.json` regeneration,
> and the release process.

All skill content lives in `src/wizard-frontend-boilerplate-pro/`. The
`.claude/skills/wizard-frontend-boilerplate-pro/` entry is a symlink — never
edit files there.

## Before you start

Clone the repo and verify the validation suite passes:

```bash
git clone https://github.com/ThisIsTheWizard/wizard-frontend-boilerplate-pro-skill.git
cd wizard-frontend-boilerplate-pro-skill

# Shell script syntax
bash -n src/wizard-frontend-boilerplate-pro/scripts/check_versions.sh
bash -n src/wizard-frontend-boilerplate-pro/scripts/detect_package_manager.sh

# Python syntax
python3 -m py_compile src/wizard-frontend-boilerplate-pro/scripts/generate_palette.py
python3 -m py_compile src/wizard-frontend-boilerplate-pro/scripts/verify_contrast.py

# WCAG AA gate (must print no failures)
python3 src/wizard-frontend-boilerplate-pro/scripts/verify_contrast.py \
  src/wizard-frontend-boilerplate-pro/assets/color-presets.json --quiet
```

---

## Adding a color preset

Color presets are named pairs of a neutral and an accent seed color, each
generating an 11-stop OKLCH scale (50–950). Every preset must pass WCAG AA
contrast before it can be merged.

**Steps:**

1. Pick two hex seeds — one for the neutral base, one for the accent.
2. Add a `(name, neutral_hex, accent_hex)` tuple to the `PRESETS` list in
   `src/wizard-frontend-boilerplate-pro/scripts/generate_palette.py`.
3. Regenerate `color-presets.json`:
   ```bash
   python3 src/wizard-frontend-boilerplate-pro/scripts/generate_palette.py \
     --emit-presets-json \
     > src/wizard-frontend-boilerplate-pro/assets/color-presets.json
   ```
4. Confirm the new preset passes WCAG AA:
   ```bash
   python3 src/wizard-frontend-boilerplate-pro/scripts/verify_contrast.py \
     src/wizard-frontend-boilerplate-pro/assets/color-presets.json --quiet
   ```
   Fix failures by adjusting the seed lightness until all stops pass.
5. Add the preset row to the Q4 table in `SKILL.md` and `workflow.md`.
6. Add a tagline (one sentence describing who/what it suits) to the README
   color presets table.

**Checklist before opening a PR:**
- [ ] `color-presets.json` regenerated and committed
- [ ] WCAG AA gate passes (exit 0)
- [ ] Preset appears in `SKILL.md` Q4 table
- [ ] Preset appears in `workflow.md` Q4 list
- [ ] Tagline added to README

---

## Adding a UI library

Adding a new UI library involves a reference file, showcase templates for every
compatible framework family, and entries in the interview tables.

**Steps:**

1. **Reference file** — create
   `src/wizard-frontend-boilerplate-pro/references/ui-library/<name>.md`.
   Follow the structure of an existing reference (e.g. `shadcn.md` for a
   Tailwind-based library, `mui.md` for a CSS-in-JS library). The file must cover:
   - Package install command
   - Provider / plugin wiring per compatible framework
   - Theming bridge to the CSS variable tokens from Phase 4
   - Per-component install commands (if applicable)
   - Peer dependencies

2. **Component catalog mapping** — add a column for the new library to the
   Library Component Mapping table in
   `src/wizard-frontend-boilerplate-pro/references/component-catalog.md`.
   Map each of the 28 catalog slots to its native library equivalent.

3. **Showcase templates** — create one template directory per compatible
   framework family:
   - React/Next: `assets/showcase-templates/react-<name>/` with
     `layout.tsx.template`, `sidebar.tsx.template`, and six category templates
     (`inputs`, `display`, `feedback`, `navigation`, `overlay`, `data-viz`)
   - Vue/Nuxt: `assets/showcase-templates/vue-<name>/` with
     `AppLayout.vue.template`, `Sidebar.vue.template`, and `pages/<category>.vue.template`
   - SvelteKit: `assets/showcase-templates/svelte-<name>/` with
     `+layout.svelte.template`, `Sidebar.svelte.template`, and
     `routes/<category>/+page.svelte.template`

   Each category template must render all components in that category, each with
   a heading, one-sentence description, live example, and `<CodeBlock>` toggle.
   Use `{{PLACEHOLDER}}` tokens for project-specific values (see `workflow.md`
   Phase 6b for the full token list).

4. **Interview tables** — add the library to:
   - The Q2 compatibility table in `SKILL.md`
   - The Q2 list in `workflow.md`
   - The `UI_LIB = named library` branch in Phase 5 of both files
   - The template folder mapping table in Phase 6 of `workflow.md`

5. **Tailwind gotchas** — if the library has a known Tailwind v4 conflict, add
   an entry to `references/tailwind/per-framework-gotchas.md`.

**Checklist before opening a PR:**
- [ ] Reference file created and complete
- [ ] Component catalog mapping added (all 28 slots)
- [ ] Showcase templates created for every compatible framework family
- [ ] All category page templates present (inputs, display, feedback, navigation, overlay, data-viz)
- [ ] `SKILL.md` Q2 table and Phase 5/6 updated
- [ ] `workflow.md` Q2 list and Phase 5/6 updated
- [ ] Tailwind gotchas entry added if applicable
- [ ] Version noted in README version compatibility matrix

---

## Adding a framework

Adding a framework means a new scaffold reference, theme provider, showcase
templates, and interview entries.

**Steps:**

1. **Scaffold reference** — create
   `src/wizard-frontend-boilerplate-pro/references/frameworks/<name>.md`.
   Cover: CLI scaffold command (with flags for language and router mode),
   post-scaffold cleanup, Tailwind v4 + v3 setup, tsconfig adjustments,
   expected directory structure, and an initial smoke test.

2. **Theme provider** — add
   `src/wizard-frontend-boilerplate-pro/assets/theme-provider/<name>.ts|tsx`.
   The provider must:
   - Read `localStorage.getItem('theme')` on mount
   - Fall back to `prefers-color-scheme` when absent
   - Toggle the `dark` class on `<html>`
   - Expose `toggleTheme()` for the Header component

3. **Showcase templates** — create
   `assets/showcase-templates/<name>/` with a layout, sidebar, and all six
   category page templates. Choose `<name>` to match the framework family
   key used in `SKILL.md` Phase 6 (`react`, `vue`, or `svelte`; introduce a
   new key if the framework family is genuinely different).

4. **Interview tables** — add the framework to:
   - Q1 in `SKILL.md` and `workflow.md`
   - The version-resolution table in `workflow.md` Phase 2b
   - The framework family mapping in `SKILL.md` and `workflow.md` Phase 6
   - The destination paths in Phase 5b and 6b

5. **Version matrix** — add a row to the version compatibility table in README.

6. **Portability note** — once tested end-to-end with at least two agents, add
   the framework to `references/portability.md`.

---

## Fixing a bug in a template or reference file

Reference files in `references/` and templates in `assets/showcase-templates/`
are plain Markdown and template text — edit them directly. No regeneration step
is needed.

After editing a template, trace through Phase 6 of `workflow.md` to verify:
- All `{{PLACEHOLDER}}` tokens are still handled
- Import paths use the correct alias (`@/` for React/Vue/Next, `$lib/` for SvelteKit)
- The component renders without a build error (mentally check imports and props)

After editing a reference file, check the phase that reads it (listed in the
Reference Index at the bottom of `SKILL.md`) to ensure the new instructions
remain consistent with the phase's inputs and outputs.

---

## Code quality

All `.ts`, `.tsx`, `.vue`, and `.svelte` files must pass ESLint, Prettier, and
`prettier-plugin-perfectionist` (import sorting). Template files (`.template`)
are exempt from linting but should follow the same style conventions.

---

## Opening a pull request

1. Fork the repo, create a branch from `master`.
2. Run the full validation suite (top of this file) — all checks must pass.
3. Open a PR with a clear title and a short description of what you added/fixed.
4. Link any relevant issue.

Questions? Open an issue and tag it `question`.
