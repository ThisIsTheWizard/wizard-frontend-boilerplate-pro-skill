#!/usr/bin/env python3
"""
validate_templates.py — verify that every expected showcase template file exists.

Checks that each framework-family × UI-library combination has the required
layout, sidebar, and six category page files. Exits 1 if any are missing.

Usage:
  python3 validate_templates.py [--templates-dir <path>]
  python3 validate_templates.py --help

Options:
  --templates-dir  Path to the showcase-templates directory.
                   Default: ../assets/showcase-templates relative to this script.
  --quiet          Only print failures and the final summary.
  -h, --help       Show this help.

Exit code: 0 if all expected files exist, 1 if any are missing.
"""
from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Expected structure per framework family
# ---------------------------------------------------------------------------

REACT_LAYOUT_FILES = [
    "layout.tsx.template",
    "sidebar.tsx.template",
]
REACT_PAGE_FILES = [
    "data-viz.tsx.template",
    "display.tsx.template",
    "feedback.tsx.template",
    "inputs.tsx.template",
    "navigation.tsx.template",
    "overlay.tsx.template",
]

VUE_LAYOUT_FILES = [
    "AppLayout.vue.template",
    "Sidebar.vue.template",
]
VUE_PAGE_FILES = [
    "data-viz.vue.template",
    "display.vue.template",
    "feedback.vue.template",
    "inputs.vue.template",
    "navigation.vue.template",
    "overlay.vue.template",
]

SVELTE_LAYOUT_FILES = [
    "+layout.svelte.template",
    "Sidebar.svelte.template",
]
SVELTE_ROUTE_DIRS = [
    "data-viz",
    "display",
    "feedback",
    "inputs",
    "navigation",
    "overlay",
]
SVELTE_ROUTE_FILE = "+page.svelte.template"

# ---------------------------------------------------------------------------
# Matrix: (directory-name, family, ui-library)
# ---------------------------------------------------------------------------

EXPECTED_DIRS: list[tuple[str, str, str]] = [
    # React / Next.js
    ("react",             "react",   "custom"),
    ("react-shadcn",      "react",   "shadcn"),
    ("react-mui",         "react",   "mui"),
    ("react-bootstrap",   "react",   "bootstrap"),
    ("react-daisy",       "react",   "daisy"),
    ("react-chakra",      "react",   "chakra"),
    ("react-mantine",     "react",   "mantine"),
    ("react-antd",        "react",   "antd"),
    ("react-heroui",      "react",   "heroui"),
    ("react-headlessui",  "react",   "headlessui"),
    # Vue / Nuxt
    ("vue",               "vue",     "custom"),
    ("vue-shadcn",        "vue",     "shadcn"),
    ("vue-bootstrap",     "vue",     "bootstrap"),
    ("vue-daisy",         "vue",     "daisy"),
    ("vue-vuetify",       "vue",     "vuetify"),
    ("vue-primevue",      "vue",     "primevue"),
    ("vue-elementplus",   "vue",     "elementplus"),
    ("vue-headlessui",    "vue",     "headlessui"),
    # SvelteKit
    ("svelte",            "svelte",  "custom"),
    ("svelte-shadcn",     "svelte",  "shadcn"),
    ("svelte-bootstrap",  "svelte",  "bootstrap"),
    ("svelte-daisy",      "svelte",  "daisy"),
]


def _check_react(base: Path, dir_name: str, quiet: bool) -> list[str]:
    missing: list[str] = []
    for f in REACT_LAYOUT_FILES:
        p = base / dir_name / f
        if not p.exists():
            missing.append(str(p.relative_to(base.parent.parent)))
    for f in REACT_PAGE_FILES:
        p = base / dir_name / f
        if not p.exists():
            missing.append(str(p.relative_to(base.parent.parent)))
    return missing


def _check_vue(base: Path, dir_name: str, quiet: bool) -> list[str]:
    missing: list[str] = []
    for f in VUE_LAYOUT_FILES:
        p = base / dir_name / f
        if not p.exists():
            missing.append(str(p.relative_to(base.parent.parent)))
    pages_dir = base / dir_name / "pages"
    for f in VUE_PAGE_FILES:
        p = pages_dir / f
        if not p.exists():
            missing.append(str(p.relative_to(base.parent.parent)))
    return missing


def _check_svelte(base: Path, dir_name: str, quiet: bool) -> list[str]:
    missing: list[str] = []
    for f in SVELTE_LAYOUT_FILES:
        p = base / dir_name / f
        if not p.exists():
            missing.append(str(p.relative_to(base.parent.parent)))
    routes_dir = base / dir_name / "routes"
    for cat in SVELTE_ROUTE_DIRS:
        p = routes_dir / cat / SVELTE_ROUTE_FILE
        if not p.exists():
            missing.append(str(p.relative_to(base.parent.parent)))
    return missing


_GREEN = "\033[32m"
_RED   = "\033[31m"
_RST   = "\033[0m"


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    quiet = False
    templates_dir: Path | None = None

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--quiet":
            quiet = True
        elif arg == "--templates-dir":
            i += 1
            if i >= len(argv):
                print("Error: --templates-dir requires a path", file=sys.stderr)
                return 1
            templates_dir = Path(argv[i])
        elif arg.startswith("--"):
            print(f"Error: unknown option {arg!r}", file=sys.stderr)
            return 1
        i += 1

    if templates_dir is None:
        templates_dir = Path(__file__).parent.parent / "assets" / "showcase-templates"

    if not templates_dir.exists():
        print(f"Error: templates directory not found: {templates_dir}", file=sys.stderr)
        return 1

    total_missing: list[str] = []
    total_checked = 0

    checkers = {"react": _check_react, "vue": _check_vue, "svelte": _check_svelte}

    for dir_name, family, _lib in EXPECTED_DIRS:
        checker = checkers.get(family)
        if checker is None:
            continue
        missing = checker(templates_dir, dir_name, quiet)
        total_checked += 1
        if missing:
            total_missing.extend(missing)
            if not quiet:
                print(f"{_RED}MISSING{_RST}  {dir_name}/  ({len(missing)} file(s))")
                for m in missing:
                    print(f"  - {m}")
        else:
            if not quiet:
                print(f"{_GREEN}OK{_RST}       {dir_name}/")

    bar = "=" * 60
    print(f"\n{bar}")
    if not total_missing:
        print(f"All {total_checked} template directories complete.")
    else:
        print(f"{len(total_missing)} missing file(s) across {total_checked} template directories.")
        for m in total_missing:
            print(f"  MISSING  {m}")
    print(bar)

    return 0 if not total_missing else 1


if __name__ == "__main__":
    sys.exit(main())
