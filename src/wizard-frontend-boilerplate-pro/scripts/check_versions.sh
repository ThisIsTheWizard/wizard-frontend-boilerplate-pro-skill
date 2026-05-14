#!/usr/bin/env bash
# Query the npm registry for the latest versions of key frontend packages.
# Usage: ./check_versions.sh [--json]
# Requires: curl, python3

set -uo pipefail

REGISTRY="https://registry.npmjs.org"
TIMEOUT=10
FORMAT="table"

PACKAGES=(
  "next" "react" "react-dom"
  "vue" "nuxt"
  "@sveltejs/kit" "svelte"
  "tailwindcss" "@tailwindcss/vite" "@tailwindcss/postcss"
  "typescript" "vite" "@vitejs/plugin-react" "@vitejs/plugin-vue"
  "eslint" "prettier" "prettier-plugin-tailwindcss"
)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) FORMAT="json" ;;
    -h|--help) printf 'Usage: %s [--json]\n' "$(basename "$0")"; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; exit 1 ;;
  esac
  shift
done

_fetch() {
  local pkg="$1" version="ERROR"
  local enc="${pkg//@/%40}"; enc="${enc//\//%2F}"
  local body
  if body=$(curl -sf --max-time "$TIMEOUT" "$REGISTRY/$enc/latest" 2>/dev/null); then
    version=$(
      printf '%s' "$body" | python3 -c \
        "import json,sys; print(json.load(sys.stdin).get('version','ERROR'))" 2>/dev/null
    ) || version="ERROR"
  fi
  printf '%s\t%s\n' "$pkg" "$version"
}

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

for pkg in "${PACKAGES[@]}"; do
  _fetch "$pkg" > "$WORKDIR/${pkg//[^A-Za-z0-9._-]/_}" &
done
wait

declare -a ROWS=()
for pkg in "${PACKAGES[@]}"; do
  ROWS+=("$(cat "$WORKDIR/${pkg//[^A-Za-z0-9._-]/_}" 2>/dev/null || printf '%s\tERROR\n' "$pkg")")
done

if [[ "$FORMAT" == "json" ]]; then
  printf '%s\n' "${ROWS[@]}" | python3 -c "
import json, sys
out = {}
for line in sys.stdin:
    pkg, _, ver = line.rstrip('\n').partition('\t')
    if pkg:
        out[pkg] = ver or 'ERROR'
print(json.dumps(out, indent=2))
"
else
  printf '%-42s  %s\n' 'Package' 'Latest'
  printf '%-42s  %s\n' '-------' '------'
  for row in "${ROWS[@]}"; do
    printf '%-42s  %s\n' "${row%%$'\t'*}" "${row##*$'\t'}"
  done
fi
