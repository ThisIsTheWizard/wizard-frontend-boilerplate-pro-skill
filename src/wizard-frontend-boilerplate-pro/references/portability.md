# Portability

Notes for running this skill on agents other than Claude Code. Covers
prerequisites, entry-point conventions, known per-agent behaviour, and a
tested-agent compatibility table.

## Table of Contents

- [Design principles](#design-principles)
- [Prerequisites](#prerequisites)
- [Entry points](#entry-points)
- [What agents must be able to do](#what-agents-must-be-able-to-do)
- [What agents must NOT need](#what-agents-must-not-need)
- [Tested agents](#tested-agents)
- [Per-agent notes](#per-agent-notes)
- [Portability checklist](#portability-checklist)

---

## Design principles

The skill is intentionally constrained to the lowest common denominator of
agent capabilities:

1. **Plain CommonMark only** — no agent-specific tags, directives, XML, or
   tool-call syntax anywhere in the markdown.
2. **Shell + Python only** — every action in every phase is either a shell
   command or a file write. No agent SDK calls, no HTTP requests from the
   skill itself.
3. **No pip installs** — all Python scripts use the standard library only
   (`math`, `json`, `subprocess`, `sys`, `pathlib`). An agent needs only
   `python3` on PATH.
4. **No assumptions about the agent's tool set** — the skill gives shell
   commands to run, not instructions like "search the web" or "use your
   browser tool".
5. **Stateless scripts** — every script in `scripts/` is idempotent and can
   be re-run safely.

---

## Prerequisites

The machine running the agent must have:

| Requirement | Minimum version | Notes |
|---|---|---|
| `bash` | 3.2+ | macOS ships 3.2; Linux ships 5.x |
| `python3` | 3.9+ | stdlib only — no pip needed |
| `node` | 18 LTS+ | Required for all framework scaffolds |
| `npm` | 9+ | Baseline package manager |
| `curl` | any | Used by `check_versions.sh` to query npm registry |
| `git` | 2.x+ | Required by some framework CLIs |

Optional but improves output quality:

| Optional | Purpose |
|---|---|
| `pnpm` | Faster installs; detected by `detect_package_manager.sh` |
| `bun` | Fastest installs; also detected |
| `yarn` | Detected if present |
| `ui-ux-pro-max-skill` | Higher-quality component source; fallback is built-in |

---

## Entry points

Different agents look for different filenames:

| Agent / convention | File to read |
|---|---|
| Claude Code (`/skills/`) | `SKILL.md` |
| AGENTS.md convention (Codex, OpenCode) | `AGENTS.md` → redirects to `SKILL.md` |
| Direct invocation | `SKILL.md` |

`AGENTS.md` contains a single line pointing to `SKILL.md`. Any agent that
opens it will be immediately redirected. This means the skill works with both
conventions without duplicating content.

---

## What agents must be able to do

The minimum capability set required to run this skill end-to-end:

- **Read files** — read any file in the skill directory and the target project.
- **Write files** — write and overwrite files in the target project directory.
- **Execute shell commands** — run `bash`, `python3`, `npm`/`pnpm`/`yarn`/`bun`,
  and framework CLIs (`npx`, `bunx`, etc.).
- **Follow sequential instructions** — execute the phases in order,
  waiting for each command to complete before the next.
- **Ask the user questions** — Phase 1 is an interactive interview (5
  questions); the agent must be able to prompt the user and capture answers.
- **Present formatted output** — the color preset table in Phase 1 and the
  compatibility table in Phase 2 are markdown tables; the agent should render
  or display them clearly.

---

## What agents must NOT need

The following capabilities are explicitly **not required**:

- **Web browsing / search** — version resolution uses `check_versions.sh`
  which calls `curl` directly; no agent-level browser tool needed.
- **Image rendering** — no screenshots, no canvas, no visual preview tools.
- **Database access** — nothing persists outside the project directory and
  `localStorage` in the user's browser.
- **Agent-to-agent calls** — locating `ui-ux-pro-max-skill` is a shell `find`
  operation, not an inter-agent API call.
- **Authenticated API access** — npm registry queries are unauthenticated.
- **Claude-specific features** — no `<tool_use>`, no thinking blocks, no
  `bash` tool syntax. Only plain shell.

---

## Tested agents

| Agent | Entry point used | Phases tested | Status |
|---|---|---|---|
| **Claude Code** (CLI) | `SKILL.md` | 1–7 | Full pass |
| **Claude.ai** (web) | `SKILL.md` | 1–7 | Full pass |
| **Codex** (OpenAI) | `AGENTS.md` | 1–7 | Full pass |
| **Cursor Agent** | `SKILL.md` | 1–7 | Full pass |
| **OpenCode** | `AGENTS.md` | 1–7 | Full pass |
| **Gemini CLI** | `SKILL.md` | 1–7 | Full pass |

"Full pass" means: all six interview questions answered, dev server started,
all six `/library/*` routes rendered, theme toggle functional.

---

## Per-agent notes

### Claude Code (CLI)

- Place the skill directory at `~/.claude/skills/wizard-frontend-boilerplate-pro/`
  or any path registered in Claude Code's skills config.
- The skill triggers automatically on phrases matching the frontmatter
  `description` field in `SKILL.md`.
- Shell commands run in the agent's bash tool; no extra setup needed.
- `locate_ui_ux_pro_max.sh` searches `~/.claude/skills/` first, which is the
  standard install location for sibling skills.

### Claude.ai (web)

- Upload the skill directory as a Project file, or paste `SKILL.md` content
  as a Project instruction.
- The agent does not have a native shell tool in the web UI; instruct it to
  output all commands as a bash script for the user to run, then paste back
  the output.
- Alternatively, use the Claude.ai desktop app with computer use enabled for
  full shell access.

### Codex (OpenAI)

- Drop the skill directory in the repo root or a `skills/` subdirectory.
- Codex reads `AGENTS.md` first; the redirect to `SKILL.md` works as-is.
- Codex can execute shell commands natively in its sandbox; all scripts run
  without modification.
- Known limitation: Codex may time out on very long `npm install` runs. If
  this happens, split Phase 7 into two steps: install dependencies first,
  then run the build.

### Cursor Agent

- Open the skill directory in a Cursor workspace alongside the target project.
- Reference `SKILL.md` in the agent's system prompt or via `@SKILL.md`.
- Cursor's terminal integration executes shell commands directly.
- The `locate_ui_ux_pro_max.sh` search covers `~/skills/` and the workspace
  root; place sibling skills in one of those locations.

### OpenCode

- OpenCode reads `AGENTS.md` by convention when placed at the repo root.
- The single-line redirect in `AGENTS.md` is sufficient; no additional config.
- All shell commands work in OpenCode's integrated terminal runner.

### Gemini CLI

- Pass `SKILL.md` as the initial context file:
  `gemini -f path/to/SKILL.md "scaffold a new Next.js app"`.
- Gemini CLI executes bash via its built-in shell tool; no modifications needed.
- The `generate_palette.py` script uses only `math` and `json`; no issues with
  Gemini's Python sandbox.
- Known limitation: Gemini CLI streams output line-by-line; long tables in
  Phase 1 and Phase 2 may be split across multiple assistant turns. This is
  cosmetic only and does not affect correctness.

---

## Portability checklist

Run this checklist before shipping a new version of the skill:

- [ ] `SKILL.md` contains no `<*>` tags (XML/HTML angle-bracket syntax).
- [ ] `SKILL.md` contains no internal tool names (`bash_tool`, `computer_use`,
      `str_replace_editor`, etc.).
- [ ] `AGENTS.md` contains no `<*>` tags or internal tool names.
- [ ] All `.sh` scripts pass `bash -n scripts/*.sh` with zero errors.
- [ ] All `.py` scripts pass `python3 -m py_compile scripts/*.py` with zero errors.
- [ ] No script imports a third-party package (`import requests`, `import numpy`, etc.).
- [ ] Every phase action is either a shell command or a file write — no
      instructions that assume agent-specific capabilities.
- [ ] The `references/` directory contains no agent-specific syntax.
- [ ] `assets/` templates contain no agent-specific syntax.
