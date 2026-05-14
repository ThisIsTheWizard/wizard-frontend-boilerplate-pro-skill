# CLAUDE.md — `wizard-frontend-boilerplate-pro` Skill

## Session convention

Each session completes **exactly one TODO item** from `TODO.md`. Do not move to the next item unless the user explicitly starts a new session for it.

Examples:
- Session A → TODO item 3.1 only
- Session B → TODO item 3.2 only

Mark the item `[x]` in `TODO.md` when complete.

## Code quality

All generated code files (`.js`, `.ts`, `.tsx`, `.vue`, `.svelte`) must pass:

- **ESLint** — for linting
- **Prettier** — for formatting
- **prettier-plugin-perfectionist** — for import/property sorting

Apply these consistently. Do not leave files that would fail any of these checks.

## Reference files

- `PLAN.md` — architecture decisions and full skill structure (source of truth)
- `TODO.md` — ordered build checklist, one item per session
