# ui-ux-pro-max-skill — Integration Bridge

This document is the contract between the boilerplate skill and the sibling
`ui-ux-pro-max-skill`. It covers how to locate the skill, read its component
catalog, map source files to the 28 catalog entries, and adapt them per
framework. Includes a graceful fallback for when the sibling is absent.

---

## 1. Locating ui-ux-pro-max-skill

Run `scripts/locate_ui_ux_pro_max.sh` from the project working directory.
The script searches in order:

1. `~/.claude/skills/ui-ux-pro-max-skill/`
2. `~/skills/ui-ux-pro-max-skill/`
3. `/mnt/skills/ui-ux-pro-max-skill/`
4. Current working directory and all subdirectories (BFS, max depth 4)

The script prints the absolute path on success and exits 0. On failure it
exits 1 and prints nothing.

If the script fails, fall back to `references/ui-library/custom-tailwind.md`
and do not block progress.

---

## 2. Reading the component catalog

Once located, the sibling skill has a component catalog at:

```
<ui-ux-pro-max-path>/references/component-catalog.md
```

Read this file to discover all available source components. Each entry lists:
- Component name
- Category (Inputs / Display / Feedback / Navigation / Overlay / Data viz)
- Peer dependencies (e.g. Recharts for Chart)
- Props interface summary
- Source file path within the sibling skill

---

## 3. Name mapping table

Map each of the 28 boilerplate components to the sibling skill's source files.

| Boilerplate name | Sibling source (relative to `<ui-ux-pro-max-path>/`) | Category |
|---|---|---|
| Button | `src/components/ui/button.tsx` | Inputs |
| Input | `src/components/ui/input.tsx` | Inputs |
| Textarea | `src/components/ui/textarea.tsx` | Inputs |
| Select | `src/components/ui/select.tsx` | Inputs |
| Checkbox | `src/components/ui/checkbox.tsx` | Inputs |
| RadioGroup | `src/components/ui/radio-group.tsx` | Inputs |
| Switch | `src/components/ui/switch.tsx` | Inputs |
| Card | `src/components/ui/card.tsx` | Display |
| Badge | `src/components/ui/badge.tsx` | Display |
| Avatar | `src/components/ui/avatar.tsx` | Display |
| Separator | `src/components/ui/separator.tsx` | Display |
| Skeleton | `src/components/ui/skeleton.tsx` | Display |
| Table | `src/components/ui/table.tsx` | Display |
| Alert | `src/components/ui/alert.tsx` | Feedback |
| Toast | `src/components/ui/toast.tsx` | Feedback |
| Progress | `src/components/ui/progress.tsx` | Feedback |
| Tooltip | `src/components/ui/tooltip.tsx` | Feedback |
| Dialog | `src/components/ui/dialog.tsx` | Feedback |
| Tabs | `src/components/ui/tabs.tsx` | Navigation |
| Breadcrumb | `src/components/ui/breadcrumb.tsx` | Navigation |
| Pagination | `src/components/ui/pagination.tsx` | Navigation |
| NavigationMenu | `src/components/ui/navigation-menu.tsx` | Navigation |
| Popover | `src/components/ui/popover.tsx` | Overlay |
| DropdownMenu | `src/components/ui/dropdown-menu.tsx` | Overlay |
| Sheet | `src/components/ui/sheet.tsx` | Overlay |
| Chart | `src/components/ui/chart.tsx` | Data viz |
| DataTable | `src/components/ui/data-table.tsx` | Data viz |
| Calendar | `src/components/ui/calendar.tsx` | Data viz |

> If a source file is not found at the expected path, check the sibling's
> component-catalog.md for actual file names and adjust accordingly. Sibling
> updates may rename files.

---

## 4. Adaptation rules per framework

For each component, read the source file and adapt it to the target framework
using the corresponding adapter reference.

### Step-by-step adaptation

1. **Read source** — read the sibling's `.tsx` source file.
2. **Apply framework adapter** — consult
   `references/ui-library/framework-adapters/<choice>-adapter.md` for the
   transformation rules specific to the target framework.
3. **Replace color values** — any hardcoded color hex/OKLCH values in the
   source must be replaced with the CSS variable tokens generated in Phase 4:
   - `bg-slate-50` → `bg-background`
   - `text-slate-900` → `text-foreground`
   - `border-slate-200` → `border-border`
   - `text-indigo-500` → `text-primary` (primary token, not accent scale)
4. **Write adapted file** — write to the boilerplate project's component path:
   - Next.js / React + Vite: `src/components/ui/<Name>.tsx`
   - Vue / Nuxt: `src/components/ui/<Name>.vue`
   - SvelteKit: `src/lib/components/ui/<Name>.svelte`

---

## 5. Peer dependencies

Some components require external libraries. Install these after adapting the
component, before the showcase routes:

| Component | Peer dependency | Registry name |
|---|---|---|
| Chart | Recharts | `recharts` |
| DataTable | TanStack Table | `@tanstack/react-table` (React) / `vue-tables-2` (Vue) / `$tanstack/table-core` (Svelte) |
| Calendar | date-fns | `date-fns` |
| Toast | Sonner (React), Vue Toast, Svelte Toast | `sonner` / `vue-toastification` / `svelte-sonner` |

The peer dependency name varies by framework — consult the framework adapter
reference.

---

## 6. Graceful fallback

If `locate_ui_ux_pro_max.sh` exits 1, do not block progress. Fall back to
`references/ui-library/custom-tailwind.md`, which contains standalone
implementations of all 28 components using only Tailwind utility classes and
no external dependencies.

The fallback components:
- Have no peer dependencies (Chart uses SVG mock, Calendar uses raw date calc)
- Do not use Recharts, TanStack, or date-fns
- Cover the full props surface of the catalog entries
- Are framework-agnostic (written in common patterns, adapted per-framework
  via the adapter references before writing)

The output quality is lower than the sibling-sourced version, but the skill
remains fully functional and portable.

---

## 7. Search paths in SKILL.md

When writing the adaptation instructions in SKILL.md, use these tokens:

```
SIBLING_SKILL_PATH=$(scripts/locate_ui_ux_pro_max.sh)
```

If the command succeeds, `$SIBLING_SKILL_PATH` holds the absolute path. Use
it to construct the full source file path:

```bash
SIBLING_COMPONENT="$SIBLING_SKILL_PATH/src/components/ui/<Name>.tsx"
```

If the command fails, fall back as described in section 6.