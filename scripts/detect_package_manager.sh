#!/usr/bin/env bash
# Detect the package manager for a project directory.
# Usage: ./detect_package_manager.sh [<directory>]
# Output: one of bun | pnpm | yarn | npm
# Exit: 0 always (falls back to npm)

set -euo pipefail

_detect() {
  local dir="${1:-$PWD}"

  # Lockfiles are the most reliable signal — they reflect the last tool used.
  [[ -f "$dir/bun.lockb"         ]] && echo "bun"  && return
  [[ -f "$dir/pnpm-lock.yaml"    ]] && echo "pnpm" && return
  [[ -f "$dir/yarn.lock"         ]] && echo "yarn" && return
  [[ -f "$dir/package-lock.json" ]] && echo "npm"  && return

  # package.json "packageManager" field (corepack convention).
  if [[ -f "$dir/package.json" ]] && command -v python3 &>/dev/null; then
    local pm_field
    pm_field=$(python3 -c "
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    pm = d.get('packageManager', '')
    if pm:
        print(pm.split('@')[0].strip())
except Exception:
    pass
" "$dir/package.json" 2>/dev/null) || true
    if [[ -n "$pm_field" ]]; then
      echo "$pm_field"
      return
    fi
  fi

  # PATH availability — last resort.
  command -v bun  &>/dev/null && echo "bun"  && return
  command -v pnpm &>/dev/null && echo "pnpm" && return
  command -v yarn &>/dev/null && echo "yarn" && return
  echo "npm"
}

_detect "${1:-$PWD}"
