#!/usr/bin/env bash
# Locate the ui-ux-pro-max skill directory on disk.
# Searches sibling directories, Claude skills dirs, and parent paths.
# Usage: ./locate_ui_ux_pro_max.sh
# Output: absolute path to the skill directory (stdout)
# Exit: 0 if found, 1 if not found

set -euo pipefail

SKILL_NAMES=(
  "ui-ux-pro-max"
  "wizard-ui-ux-pro-max"
  "ui-ux-pro-max-skill"
  "wizard-ui-ux-pro-max-skill"
)

SEARCH_DIRS=()

# 1. Parent of this skill's root directory (sibling resolution).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
SEARCH_DIRS+=("$(dirname "$SKILL_ROOT")")

# 2. Standard Claude Code skill directories.
SEARCH_DIRS+=(
  "$HOME/.claude/skills"
  "$HOME/.config/claude/skills"
  "$HOME/Library/Application Support/Claude/skills"
)

# 3. Parent chain from CWD (3 levels up).
d="$PWD"
for _ in 1 2 3; do
  d="$(dirname "$d")"
  SEARCH_DIRS+=("$d")
done

for base in "${SEARCH_DIRS[@]}"; do
  [[ -d "$base" ]] || continue
  for name in "${SKILL_NAMES[@]}"; do
    if [[ -d "$base/$name" ]]; then
      echo "$base/$name"
      exit 0
    fi
  done
done

printf 'ui-ux-pro-max skill not found.\n' >&2
printf 'Searched:\n' >&2
for base in "${SEARCH_DIRS[@]}"; do
  printf '  %s\n' "$base" >&2
done
exit 1
