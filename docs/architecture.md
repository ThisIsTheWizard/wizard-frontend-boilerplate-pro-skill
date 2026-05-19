# Architecture — Three-Location Pattern

The skill content lives in three locations that serve different purposes. Only
one of them — `src/` — is the source you edit. The other two follow automatically.

## The three locations

| Location | Role | Can you delete it? |
|---|---|---|
| **`src/wizard-frontend-boilerplate-pro/`** | **Source of truth.** All skill files (SKILL.md, references, assets, scripts) live here. This is the only place you edit. | ❌ Never — this is the canonical source. |
| **`.claude/skills/wizard-frontend-boilerplate-pro/`** | Symlink consumed by Claude Code and compatible agents. Points to `src/`. No content of its own. | ❌ Never — agents won't find the skill without it. Recreate with: `ln -s ../../src/wizard-frontend-boilerplate-pro .claude/skills/wizard-frontend-boilerplate-pro` |
| _(future)_ **`cli/assets/`** | Bundled copy for an npm CLI installer. Synced from `src/` before every release. | ❌ Never once it exists — delete only the `cli/` subtree, not `src/`. |

## Why three locations?

Each location serves a **different consumer**:

- **`src/`** — humans and agents editing the skill itself.
- **`.claude/skills/`** — Claude Code's skill loader; it scans this path at startup.
- **`cli/assets/`** — the npm package bundles assets at build time; it cannot follow symlinks across user machines.

## Recommended workflow

1. All changes go into **`src/wizard-frontend-boilerplate-pro/`** only.
2. The `.claude/skills/` symlink follows automatically — no sync needed.
3. Before publishing a CLI release, run:
   ```bash
   cp -r src/wizard-frontend-boilerplate-pro/assets/*   cli/assets/assets/
   cp -r src/wizard-frontend-boilerplate-pro/scripts/*  cli/assets/scripts/
   cp -r src/wizard-frontend-boilerplate-pro/references/* cli/assets/references/
   ```
4. Commit `cli/assets/` changes and tag the release.

## Directory tree

```
wizard-frontend-boilerplate-pro-skill/
├── src/
│   └── wizard-frontend-boilerplate-pro/   ← edit here
│       ├── SKILL.md
│       ├── AGENTS.md
│       ├── workflow.md
│       ├── references/
│       │   ├── frameworks/
│       │   ├── tailwind/
│       │   ├── ui-library/
│       │   ├── theming.md
│       │   ├── component-catalog.md
│       │   ├── showcase-layout.md
│       │   └── portability.md
│       ├── assets/
│       │   ├── color-presets.json
│       │   ├── showcase-templates/
│       │   └── theme-provider/
│       └── scripts/
│           ├── check_versions.sh
│           ├── detect_package_manager.sh
│           ├── generate_palette.py
│           ├── locate_ui_ux_pro_max.sh
│           └── verify_contrast.py
├── .claude/
│   └── skills/
│       └── wizard-frontend-boilerplate-pro → ../../src/wizard-frontend-boilerplate-pro
├── docs/                                  ← developer documentation
├── .github/workflows/                     ← CI
├── skill.json
├── CLAUDE.md
└── README.md
```

## Restoring the symlink

If the `.claude/skills/` symlink is accidentally removed:

```bash
ln -s ../../src/wizard-frontend-boilerplate-pro \
  .claude/skills/wizard-frontend-boilerplate-pro
```

## Cross-platform and symlink-unsupported environments

**Windows (native git without symlinks enabled)**

Git on Windows requires Developer Mode or the `core.symlinks=true` setting to
check out symlinks correctly. If the symlink resolves as a plain text file
containing the target path, recreate it manually:

```powershell
# PowerShell (run as administrator, or in Developer Mode)
cmd /c mklink /D .claude\skills\wizard-frontend-boilerplate-pro ..\..\src\wizard-frontend-boilerplate-pro
```

Or enable symlinks globally and re-clone:

```bash
git config --global core.symlinks true
```

**WSL (Windows Subsystem for Linux)**

Inside a WSL terminal the `ln -s` command works normally. Use the standard
Unix form:

```bash
ln -s ../../src/wizard-frontend-boilerplate-pro \
  .claude/skills/wizard-frontend-boilerplate-pro
```

**Git clients that do not support symlinks (e.g. some CI agents)**

Copy the source directory instead of symlinking:

```bash
cp -r src/wizard-frontend-boilerplate-pro \
  .claude/skills/wizard-frontend-boilerplate-pro
```

Note: the copy will not automatically track future edits to `src/`. Run the
copy command again after making changes if symlinks are unavailable.

**Verification**

Regardless of method, verify the skill resolves correctly:

```bash
# Should print the path to SKILL.md (not a raw symlink path string)
cat .claude/skills/wizard-frontend-boilerplate-pro/SKILL.md | head -5
```
