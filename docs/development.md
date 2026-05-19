# Development Guide

How to extend, maintain, and validate the `wizard-frontend-boilerplate-pro` skill.
All paths below are relative to the repo root. All edits go into `src/wizard-frontend-boilerplate-pro/`.

> **Contributing?** See [CONTRIBUTING.md](../CONTRIBUTING.md) instead — it covers the same
> recipes with contributor-focused checklists and PR instructions. This file adds the
> maintainer-only sections: theme provider contract, `color-presets.json` regeneration,
> and the release process.

---

## Validation scripts

Run these from the repo root before every commit:

```bash
# Syntax-check all shell scripts
bash -n src/wizard-frontend-boilerplate-pro/scripts/check_versions.sh
bash -n src/wizard-frontend-boilerplate-pro/scripts/detect_package_manager.sh
bash -n src/wizard-frontend-boilerplate-pro/scripts/locate_ui_ux_pro_max.sh

# Syntax-check Python scripts
python3 -m py_compile src/wizard-frontend-boilerplate-pro/scripts/generate_palette.py
python3 -m py_compile src/wizard-frontend-boilerplate-pro/scripts/verify_contrast.py
python3 -m py_compile src/wizard-frontend-boilerplate-pro/scripts/validate_templates.py

# WCAG AA gate — all 8 presets must pass
python3 src/wizard-frontend-boilerplate-pro/scripts/verify_contrast.py \
  src/wizard-frontend-boilerplate-pro/assets/color-presets.json --quiet

# Template coverage — all expected showcase template files present
python3 src/wizard-frontend-boilerplate-pro/scripts/validate_templates.py --quiet
```

CI runs the same commands on every push (see `.github/workflows/python-ci.yml`).
The full compat matrix (Python 3.10–3.13, Ubuntu + macOS) runs via
`.github/workflows/compat-matrix.yml`.

---

## Adding a color preset

1. Add a `(name, neutral_hex, accent_hex)` tuple to `PRESETS` in
   `src/wizard-frontend-boilerplate-pro/scripts/generate_palette.py`.
2. Regenerate `color-presets.json`:
   ```bash
   python3 src/wizard-frontend-boilerplate-pro/scripts/generate_palette.py \
     --emit-presets-json \
     > src/wizard-frontend-boilerplate-pro/assets/color-presets.json
   ```
3. Rerun the WCAG gate to confirm the new preset passes.
4. Add the preset to the table in `src/wizard-frontend-boilerplate-pro/SKILL.md` (Phase 1, Q5).
5. Add it to the `workflow.md` Q5 list as well.

---

## Updating a reference file

Reference files in `src/wizard-frontend-boilerplate-pro/references/` are plain
Markdown. Edit them directly. No regeneration step is needed.

Key references and what they govern:

| File | What changes here |
|---|---|
| `references/frameworks/<fw>.md` | Scaffold commands, post-cleanup steps, directory structure |
| `references/tailwind/v4-setup.md` | PostCSS / Vite plugin install commands |
| `references/tailwind/per-framework-gotchas.md` | Known v4 incompatibilities |
| `references/ui-library/ui-ux-pro-max-bridge.md` | Name-mapping table, search paths for sibling skill |
| `references/ui-library/custom-tailwind.md` | Standalone fallback component implementations |
| `references/component-catalog.md` | Props interfaces, peer deps, source mappings |
| `references/showcase-layout.md` | Sidebar nav, header, CodeBlock, route structure |
| `references/theming.md` | CSS var token contract |

---

## Updating showcase templates

Templates live in `src/wizard-frontend-boilerplate-pro/assets/showcase-templates/`.
They use `{{PLACEHOLDER}}` tokens replaced at install time (see `workflow.md` Phase 6 for the full token list).

After editing a template, do a quick mental trace through Phase 6 of `workflow.md` to verify all placeholders are still handled.

---

## Updating theme providers

Providers are in `src/wizard-frontend-boilerplate-pro/assets/theme-provider/`.
Each provider must:
- Read `localStorage.getItem('theme')` on mount.
- Fall back to `prefers-color-scheme` when no stored value exists.
- Toggle the `dark` class on `<html>`.
- Expose a `toggleTheme()` / `setTheme()` function for the Header component.

After editing a provider, trace through Phase 4c and Phase 7f of `workflow.md` to verify FOUC prevention still works.

---

## Adding a new framework

1. Create `src/wizard-frontend-boilerplate-pro/references/frameworks/<name>.md`
   following the structure of an existing reference (package list, scaffold command,
   CLI flag matrix, cleanup steps, directory structure, tsconfig, verification).
2. Add showcase templates under `src/wizard-frontend-boilerplate-pro/assets/showcase-templates/<name>/`.
3. Add a theme provider to `src/wizard-frontend-boilerplate-pro/assets/theme-provider/`.
4. Add the framework to the Q1 list in `SKILL.md` and `workflow.md`.
5. Add it to the version-resolution table in `workflow.md` Phase 2b.
6. Add it to `references/portability.md` once tested end-to-end.

---

## Regenerating color-presets.json

The presets JSON embeds pre-computed `tokens_css` strings for each preset. It must be
regenerated whenever `generate_palette.py` changes the output format or semantic token
mapping:

```bash
python3 src/wizard-frontend-boilerplate-pro/scripts/generate_palette.py \
  --emit-presets-json \
  > src/wizard-frontend-boilerplate-pro/assets/color-presets.json
```

---

## Releasing

1. Run all validation scripts (see top of this file).
2. Bump `version` in `skill.json` and `.claude-plugin/plugin.json`.
3. Commit and push.
4. Tag: `git tag v<version> && git push --tags`.
