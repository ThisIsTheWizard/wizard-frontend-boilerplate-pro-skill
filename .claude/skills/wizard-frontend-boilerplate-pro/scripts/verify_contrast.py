#!/usr/bin/env python3
"""
verify_contrast.py — WCAG AA contrast gate for wizard-frontend-boilerplate-pro palettes.

Verifies that the semantic token color pairs produced by the theme system meet
WCAG 2.1 AA contrast requirements (4.5:1 normal text, 3:1 UI components / large text).

Usage:
  python verify_contrast.py [options] [<color-presets.json>]
  python verify_contrast.py [options] <fg_color> <bg_color>

Positional:
  color-presets.json  Path to presets file (default: ../assets/color-presets.json
                      relative to this script).
  fg_color / bg_color Direct hex or oklch() color pair for a quick spot-check.

Options:
  --level normal      WCAG AA threshold: 4.5:1 for text (default)
  --level large       WCAG AA threshold: 3:1 for large text / UI components
  --level aaa         WCAG AAA threshold: 7:1
  --only <preset>     Check only the named preset (case-insensitive)
  --quiet             Only print failures and the final summary
  -h, --help          Show this help

Exit code: 0 if all checks pass, 1 if any fail.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Color conversion: OKLCH -> WCAG relative luminance
# ---------------------------------------------------------------------------


def _parse_oklch_str(s: str) -> tuple[float, float, float]:
    m = re.match(
        r"oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)\s*\)",
        s.strip(),
        re.IGNORECASE,
    )
    if not m:
        raise ValueError(f"Cannot parse OKLCH string: {s!r}")
    L = float(m.group(1))
    if m.group(2) == "%":
        L /= 100.0
    return L, float(m.group(3)), float(m.group(4))


def _hex_to_linear_rgb(hex_color: str) -> tuple[float, float, float]:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    if len(h) != 6:
        raise ValueError(f"Invalid hex color: {hex_color!r}")

    def _expand(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return (
        _expand(int(h[0:2], 16) / 255.0),
        _expand(int(h[2:4], 16) / 255.0),
        _expand(int(h[4:6], 16) / 255.0),
    )


def oklch_to_luminance(L: float, C: float, H_deg: float) -> float:
    """OKLCH (L in [0,1], C, H in degrees) -> WCAG relative luminance."""
    H = math.radians(H_deg)
    a = C * math.cos(H)
    b = C * math.sin(H)

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_**3
    m = m_**3
    s = s_**3

    r = max(0.0, min(1.0, +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s))
    g = max(0.0, min(1.0, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s))
    b_lin = max(0.0, min(1.0, -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s))

    return 0.2126 * r + 0.7152 * g + 0.0722 * b_lin


def parse_color_to_luminance(s: str) -> float:
    """Accept hex or oklch() string, return WCAG relative luminance."""
    s = s.strip()
    if s.startswith("#"):
        r, g, b = _hex_to_linear_rgb(s)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    if re.match(r"oklch\s*\(", s, re.IGNORECASE):
        return oklch_to_luminance(*_parse_oklch_str(s))
    raise ValueError(f"Unrecognized color: {s!r}. Use #rrggbb or oklch(L% C H).")


def contrast_ratio(lum1: float, lum2: float) -> float:
    hi, lo = (lum1, lum2) if lum1 >= lum2 else (lum2, lum1)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------------------
# Semantic token pair definitions
# Derived from emit_semantic_css() in generate_palette.py.
# Each tuple: (label, mode, fg_scale, fg_stop, bg_scale, bg_stop)
# ---------------------------------------------------------------------------

SEMANTIC_PAIRS = [
    # Light mode
    ("light / foreground on background",       "light", "neutral", "950", "neutral", "50"),
    ("light / muted-fg on background",         "light", "neutral", "500", "neutral", "50"),
    ("light / muted-fg on surface",            "light", "neutral", "500", "neutral", "100"),
    ("light / primary-fg on primary",          "light", "neutral",  "50", "accent",  "500"),
    ("light / secondary-fg on secondary",      "light", "neutral", "900", "neutral", "200"),
    ("light / accent-fg on accent",            "light", "neutral", "900", "neutral", "100"),
    ("light / destructive-fg on destructive",  "light", "neutral",  "50", "neutral", "900"),
    ("light / card-fg on card",                "light", "neutral", "950", "neutral",  "50"),
    # Dark mode
    ("dark / foreground on background",        "dark",  "neutral",  "50", "neutral", "950"),
    ("dark / muted-fg on background",          "dark",  "neutral", "400", "neutral", "950"),
    ("dark / muted-fg on surface",             "dark",  "neutral", "400", "neutral", "900"),
    ("dark / primary-fg on primary",           "dark",  "neutral", "950", "accent",  "400"),
    ("dark / secondary-fg on secondary",       "dark",  "neutral",  "50", "neutral", "700"),
    ("dark / accent-fg on accent",             "dark",  "neutral",  "50", "neutral", "800"),
    ("dark / destructive-fg on destructive",   "dark",  "neutral",  "50", "neutral", "800"),
    ("dark / card-fg on card",                 "dark",  "neutral",  "50", "neutral", "900"),
]

# These pairs carry secondary/decorative text — 3:1 (AA large/UI) is the correct bar.
_LARGE_TEXT_LABELS = frozenset({
    "light / muted-fg on background",
    "light / muted-fg on surface",
    "light / accent-fg on accent",
    "dark / muted-fg on background",
    "dark / muted-fg on surface",
    "dark / accent-fg on accent",
})


# ---------------------------------------------------------------------------
# Checking logic
# ---------------------------------------------------------------------------


class CheckResult(NamedTuple):
    label: str
    fg_color: str
    bg_color: str
    ratio: float
    threshold: float
    passed: bool


def check_pair(label: str, fg_color: str, bg_color: str, level: str) -> CheckResult:
    fg_lum = parse_color_to_luminance(fg_color)
    bg_lum = parse_color_to_luminance(bg_color)
    ratio = contrast_ratio(fg_lum, bg_lum)

    if level == "aaa":
        threshold = 7.0
    elif level == "large":
        threshold = 3.0
    else:
        threshold = 3.0 if label in _LARGE_TEXT_LABELS else 4.5

    return CheckResult(
        label=label,
        fg_color=fg_color,
        bg_color=bg_color,
        ratio=round(ratio, 2),
        threshold=threshold,
        passed=ratio >= threshold,
    )


def check_preset(preset: dict, level: str) -> list[CheckResult]:
    neutral = preset.get("neutral", {}).get("scale", {})
    accent = preset.get("accent", {}).get("scale", {})
    results: list[CheckResult] = []
    for label, _mode, fg_scale, fg_stop, bg_scale, bg_stop in SEMANTIC_PAIRS:
        fg_src = neutral if fg_scale == "neutral" else accent
        bg_src = neutral if bg_scale == "neutral" else accent
        fg_color = fg_src.get(fg_stop, "")
        bg_color = bg_src.get(bg_stop, "")
        if not fg_color or not bg_color:
            continue
        results.append(check_pair(label, fg_color, bg_color, level))
    return results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

_RED = "\033[31m"
_GRN = "\033[32m"
_RST = "\033[0m"


def _tag(passed: bool) -> str:
    return f"{_GRN}PASS{_RST}" if passed else f"{_RED}FAIL{_RST}"


def print_results(preset_name: str, results: list[CheckResult], quiet: bool) -> int:
    failures = [r for r in results if not r.passed]
    if not quiet:
        print(f"\n  Preset: {preset_name}")
        print(f"  {'Label':<48}  {'Ratio':>7}  {'Min':>5}  Result")
        print(f"  {'-'*48}  {'-------':>7}  {'---':>5}  ------")
        for r in results:
            print(f"  {r.label:<48}  {r.ratio:>6.2f}:1  {r.threshold:>4.1f}:1  {_tag(r.passed)}")
    elif failures:
        print(f"\n  Preset: {preset_name} -- {len(failures)} failure(s)")
        for r in failures:
            print(f"  FAIL  {r.label}  {r.ratio:.2f}:1 < {r.threshold:.1f}:1")
    return len(failures)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _default_presets_path() -> Path:
    return Path(__file__).parent.parent / "assets" / "color-presets.json"


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    level = "normal"
    only: str | None = None
    quiet = False
    positional: list[str] = []

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--level":
            i += 1
            if i >= len(argv):
                print("Error: --level requires a value (normal | large | aaa)", file=sys.stderr)
                return 1
            level = argv[i]
            if level not in ("normal", "large", "aaa"):
                print(f"Error: unknown level {level!r}", file=sys.stderr)
                return 1
        elif arg == "--only":
            i += 1
            if i >= len(argv):
                print("Error: --only requires a preset name", file=sys.stderr)
                return 1
            only = argv[i]
        elif arg == "--quiet":
            quiet = True
        elif arg.startswith("--"):
            print(f"Error: unknown option {arg!r}", file=sys.stderr)
            return 1
        else:
            positional.append(arg)
        i += 1

    # Direct pair mode: verify_contrast.py <fg> <bg>
    if len(positional) == 2 and not positional[0].endswith(".json"):
        try:
            result = check_pair("custom pair", positional[0], positional[1], level)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        tag = "PASS" if result.passed else "FAIL"
        print(f"{tag}  ratio={result.ratio:.2f}:1  threshold={result.threshold:.1f}:1")
        return 0 if result.passed else 1

    # Presets file mode
    presets_path = Path(positional[0]) if positional else _default_presets_path()
    if not presets_path.exists():
        print(f"Error: presets file not found: {presets_path}", file=sys.stderr)
        return 1

    try:
        with open(presets_path) as f:
            presets: list[dict] = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Error reading {presets_path}: {exc}", file=sys.stderr)
        return 1

    total_failures = 0
    checked = 0
    for preset in presets:
        name = preset.get("name", "?")
        if only and name.lower() != only.lower():
            continue
        if not preset.get("neutral", {}).get("scale"):
            continue  # skip the Custom slot which has an empty scale
        results = check_preset(preset, level)
        total_failures += print_results(name, results, quiet)
        checked += 1

    if checked == 0:
        print("No presets matched.", file=sys.stderr)
        return 1

    level_label = "AAA" if level == "aaa" else "AA"
    bar = "=" * 60
    print(f"\n{bar}")
    if total_failures == 0:
        print(f"All {checked} preset(s) passed WCAG {level_label} ({level}).")
    else:
        print(f"{total_failures} failure(s) across {checked} preset(s) [WCAG {level_label} / {level}].")
    print(bar)

    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
