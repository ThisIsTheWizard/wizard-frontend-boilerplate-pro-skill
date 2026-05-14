#!/usr/bin/env python3
"""
generate_palette.py — OKLCH palette generator for wizard-frontend-boilerplate-pro.

Generates 50–950 OKLCH color scales from a hex or OKLCH seed color.
The seed is treated as the 500-stop anchor; all other stops are derived by
applying fixed perceptual-lightness targets (calibrated from Tailwind CSS v4
OKLCH palettes) while preserving the seed's hue and scaling its chroma.

Usage:
  python generate_palette.py <neutral> <accent>
  python generate_palette.py --preset <name>
  python generate_palette.py --list-presets
  python generate_palette.py --emit-presets-json

Arguments:
  neutral   Hex (#rrggbb / #rgb) or CSS oklch(L% C H) — neutral scale seed
  accent    Hex or CSS oklch(L% C H) — accent scale seed

Options:
  --format css            Emit @theme CSS block (default)
  --format json           Emit JSON { neutral: {...}, accent: {...} }
  --preset <name>         Use a built-in named preset
  --list-presets          Print available preset names and exit
  --emit-presets-json     Write full color-presets.json to stdout

Examples:
  python generate_palette.py "#64748b" "#6366f1"
  python generate_palette.py "oklch(50% 0.12 265)" "oklch(55% 0.25 241)"
  python generate_palette.py --preset "Modern Slate"
  python generate_palette.py --emit-presets-json > assets/color-presets.json
"""

from __future__ import annotations

import json
import math
import re
import sys

# ---------------------------------------------------------------------------
# Color conversion  (stdlib only — no pip required)
# ---------------------------------------------------------------------------


def _gamma_expand(c: float) -> float:
    """sRGB component → linear light."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_oklch(hex_color: str) -> tuple[float, float, float]:
    """Convert #rrggbb / #rgb hex to OKLCH (L 0–1, C, H°)."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    if len(h) != 6:
        raise ValueError(f"Invalid hex color: {hex_color!r}")

    r = _gamma_expand(int(h[0:2], 16) / 255.0)
    g = _gamma_expand(int(h[2:4], 16) / 255.0)
    b = _gamma_expand(int(h[4:6], 16) / 255.0)

    # Linear sRGB → LMS  (Björn Ottosson, 2020)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_ = l ** (1.0 / 3.0)
    m_ = m ** (1.0 / 3.0)
    s_ = s ** (1.0 / 3.0)

    # LMS' → OKLab
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b_ok = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    # OKLab → OKLCH
    C = math.sqrt(a * a + b_ok * b_ok)
    H = math.degrees(math.atan2(b_ok, a)) % 360.0

    return L, C, H


def parse_oklch_str(s: str) -> tuple[float, float, float]:
    """Parse 'oklch(L% C H)' or 'oklch(L C H)' → (L 0–1, C, H°)."""
    m = re.match(
        r"oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)\s*\)",
        s.strip(),
        re.IGNORECASE,
    )
    if not m:
        raise ValueError(
            f"Cannot parse OKLCH string: {s!r}\n"
            "Expected format: oklch(50% 0.12 265) or oklch(0.5 0.12 265)"
        )
    L = float(m.group(1))
    if m.group(2) == "%":
        L /= 100.0
    return L, float(m.group(3)), float(m.group(4))


def parse_color(s: str) -> tuple[float, float, float]:
    """Accept hex or oklch() string → (L 0–1, C, H°)."""
    s = s.strip()
    if s.startswith("#"):
        return hex_to_oklch(s)
    if re.match(r"oklch\s*\(", s, re.IGNORECASE):
        return parse_oklch_str(s)
    raise ValueError(
        f"Unrecognized color format: {s!r}\n"
        "Use #rrggbb hex or oklch(L% C H) CSS syntax."
    )


# ---------------------------------------------------------------------------
# Scale generation
# ---------------------------------------------------------------------------

# Perceptual lightness (L) targets per stop.
# Calibrated from Tailwind CSS v4 OKLCH Slate palette (low-chroma reference).
_STOP_L: dict[int, float] = {
    50: 0.984,
    100: 0.968,
    200: 0.929,
    300: 0.869,
    400: 0.705,
    500: 0.554,
    600: 0.446,
    700: 0.372,
    800: 0.279,
    900: 0.208,
    950: 0.129,
}

# Chroma multiplier per stop (fraction of the seed's chroma).
# Chroma peaks just above 500, tapers to near-zero at the light end,
# and decreases gradually at the dark end.
_STOP_C_FACTOR: dict[int, float] = {
    50: 0.065,
    100: 0.150,
    200: 0.285,
    300: 0.490,
    400: 0.775,
    500: 1.000,
    600: 1.020,
    700: 0.970,
    800: 0.860,
    900: 0.740,
    950: 0.650,
}

# Hard chroma ceiling for the lightest stops to prevent over-saturation.
_LIGHT_CHROMA_CAP: float = 0.020

_STOPS: list[int] = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]


def generate_scale(
    seed_L: float,
    seed_C: float,
    seed_H: float,
) -> dict[int, tuple[float, float, float]]:
    """
    Build an 11-stop OKLCH scale from a seed color.

    The seed is interpreted as the 500-stop anchor.  Lightness for each stop
    is taken from _STOP_L (fixed reference ramp); chroma is scaled relative to
    seed_C using _STOP_C_FACTOR; hue is held constant at seed_H.

    For achromatic seeds (C ≈ 0) the result is a neutral grayscale scale.
    """
    scale: dict[int, tuple[float, float, float]] = {}
    for stop in _STOPS:
        L = _STOP_L[stop]
        C = seed_C * _STOP_C_FACTOR[stop]
        if stop in (50, 100):
            C = min(C, _LIGHT_CHROMA_CAP)
        scale[stop] = (round(L, 4), round(C, 4), round(seed_H, 2))
    return scale


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------


def _fmt(L: float, C: float, H: float) -> str:
    """Format an OKLCH triple as a CSS oklch() string."""
    return f"oklch({L * 100:.1f}% {C:.3f} {H:.1f})"


def scale_to_css_vars(scale: dict[int, tuple[float, float, float]], name: str) -> list[str]:
    """Return --color-<name>-<stop> CSS custom-property lines."""
    return [f"  --color-{name}-{stop}: {_fmt(*scale[stop])};" for stop in _STOPS]


def scale_to_dict(scale: dict[int, tuple[float, float, float]]) -> dict[str, str]:
    """Return {stop: oklch_string} JSON-serialisable dict."""
    return {str(stop): _fmt(*scale[stop]) for stop in _STOPS}


def emit_css_theme(
    neutral_scale: dict[int, tuple[float, float, float]],
    accent_scale: dict[int, tuple[float, float, float]],
) -> str:
    """Emit a @theme block containing both neutral and accent palette scales."""
    lines = ["@theme {"]
    lines += scale_to_css_vars(neutral_scale, "neutral")
    lines.append("")
    lines += scale_to_css_vars(accent_scale, "accent")
    lines.append("}")
    return "\n".join(lines)


def emit_semantic_css() -> str:
    """Emit the static :root (light) and .dark semantic token blocks.

    These blocks alias the generated palette scale vars to purpose-driven
    semantic tokens.  The structure is identical for every preset; only the
    underlying palette scale values change.
    """
    return """\
:root {
  /* Surface */
  --background: var(--color-neutral-50);
  --foreground: var(--color-neutral-950);
  --surface: var(--color-neutral-100);
  --muted: var(--color-neutral-300);
  --muted-foreground: var(--color-neutral-500);

  /* Borders */
  --border: var(--color-neutral-200);
  --input: var(--color-neutral-200);
  --ring: var(--color-accent-400);

  /* Primary / Accent */
  --primary: var(--color-accent-600);
  --primary-foreground: var(--color-neutral-50);
  --secondary: var(--color-neutral-200);
  --secondary-foreground: var(--color-neutral-900);
  --accent: var(--color-neutral-100);
  --accent-foreground: var(--color-neutral-900);

  /* Destructive */
  --destructive: var(--color-neutral-900);
  --destructive-foreground: var(--color-neutral-50);

  /* Component */
  --card: var(--color-neutral-50);
  --card-foreground: var(--color-neutral-950);
  --popover: var(--color-neutral-50);
  --popover-foreground: var(--color-neutral-950);

  /* Radius */
  --radius: var(--radius-md);
}

.dark {
  /* Surface */
  --background: var(--color-neutral-950);
  --foreground: var(--color-neutral-50);
  --surface: var(--color-neutral-900);
  --muted: var(--color-neutral-600);
  --muted-foreground: var(--color-neutral-400);

  /* Borders */
  --border: var(--color-neutral-800);
  --input: var(--color-neutral-800);
  --ring: var(--color-accent-400);

  /* Primary / Accent */
  --primary: var(--color-accent-400);
  --primary-foreground: var(--color-neutral-950);
  --secondary: var(--color-neutral-700);
  --secondary-foreground: var(--color-neutral-50);
  --accent: var(--color-neutral-800);
  --accent-foreground: var(--color-neutral-50);

  /* Destructive */
  --destructive: var(--color-neutral-800);
  --destructive-foreground: var(--color-neutral-50);

  /* Component */
  --card: var(--color-neutral-900);
  --card-foreground: var(--color-neutral-50);
  --popover: var(--color-neutral-900);
  --popover-foreground: var(--color-neutral-50);
}"""


def emit_tokens_css(
    neutral_scale: dict[int, tuple[float, float, float]],
    accent_scale: dict[int, tuple[float, float, float]],
) -> str:
    """Emit a complete tokens.css file: @theme palette + semantic :root/.dark."""
    return emit_css_theme(neutral_scale, accent_scale) + "\n\n" + emit_semantic_css()


# ---------------------------------------------------------------------------
# Built-in presets
# ---------------------------------------------------------------------------

# (name, neutral_500_hex, accent_500_hex)
# Seed hex values are the Tailwind CSS 500-stop for each palette family.
PRESETS: list[tuple[str, str, str]] = [
    ("Modern Slate", "#64748b", "#6366f1"),
    ("Warm Earth", "#78716c", "#f59e0b"),
    ("Fresh Mint", "#71717a", "#10b981"),
    ("Royal", "#6b7280", "#8b5cf6"),
    ("Sunset", "#78716c", "#f43f5e"),
    ("Ocean", "#64748b", "#06b6d4"),
    ("Forest", "#71717a", "#22c55e"),
    ("Monochrome", "#737373", "#737373"),
]


def _preset_lookup(name: str) -> tuple[str, str]:
    """Return (neutral_hex, accent_hex) for a preset name (case-insensitive)."""
    for preset_name, neutral, accent in PRESETS:
        if preset_name.lower() == name.lower():
            return neutral, accent
    available = ", ".join(f'"{p[0]}"' for p in PRESETS)
    raise ValueError(f"Unknown preset {name!r}. Available: {available}")


def build_preset_entry(name: str, neutral_hex: str, accent_hex: str) -> dict:
    """Build a single color-presets.json entry from seed hex values."""
    nL, nC, nH = hex_to_oklch(neutral_hex)
    aL, aC, aH = hex_to_oklch(accent_hex)

    neutral_scale = generate_scale(nL, nC, nH)
    accent_scale = generate_scale(aL, aC, aH)

    return {
        "name": name,
        "neutral": {
            "seed": neutral_hex,
            "hue": round(nH, 1),
            "scale": scale_to_dict(neutral_scale),
        },
        "accent": {
            "seed": accent_hex,
            "hue": round(aH, 1),
            "scale": scale_to_dict(accent_scale),
        },
        "monochrome": neutral_hex == accent_hex,
        "css": emit_css_theme(neutral_scale, accent_scale),
        "tokens_css": emit_tokens_css(neutral_scale, accent_scale),
    }


def emit_presets_json() -> str:
    """Generate the full color-presets.json content (8 presets + custom slot)."""
    entries: list[dict] = [
        build_preset_entry(name, neutral, accent)
        for name, neutral, accent in PRESETS
    ]
    entries.append(
        {
            "name": "Custom",
            "neutral": {"seed": None, "hue": None, "scale": {}},
            "accent": {"seed": None, "hue": None, "scale": {}},
            "monochrome": False,
            "css": "",
            "tokens_css": "",
            "note": (
                "Generated at runtime — run: "
                "python generate_palette.py <neutral_hex> <accent_hex>"
            ),
        }
    )
    return json.dumps(entries, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _usage_error(msg: str) -> int:
    print(f"Error: {msg}", file=sys.stderr)
    print("Run with --help for usage.", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    if argv[0] == "--list-presets":
        for name, neutral, accent in PRESETS:
            print(f"  {name:<20}  neutral={neutral}  accent={accent}")
        return 0

    if argv[0] == "--emit-presets-json":
        print(emit_presets_json())
        return 0

    fmt = "css"
    preset_name: str | None = None
    positional: list[str] = []

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--format":
            i += 1
            if i >= len(argv):
                return _usage_error("--format requires a value (css | json)")
            fmt = argv[i]
        elif arg == "--preset":
            i += 1
            if i >= len(argv):
                return _usage_error("--preset requires a name")
            preset_name = argv[i]
        elif arg.startswith("--"):
            return _usage_error(f"Unknown option: {arg!r}")
        else:
            positional.append(arg)
        i += 1

    try:
        if preset_name is not None:
            neutral_seed, accent_seed = _preset_lookup(preset_name)
        elif len(positional) >= 2:
            neutral_seed, accent_seed = positional[0], positional[1]
        elif len(positional) == 1:
            neutral_seed = accent_seed = positional[0]
        else:
            return _usage_error(
                "Provide two color seeds (<neutral> <accent>) or use --preset <name>."
            )

        nL, nC, nH = parse_color(neutral_seed)
        aL, aC, aH = parse_color(accent_seed)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    neutral_scale = generate_scale(nL, nC, nH)
    accent_scale = generate_scale(aL, aC, aH)

    if fmt == "css":
        print(emit_tokens_css(neutral_scale, accent_scale))
    elif fmt == "json":
        print(
            json.dumps(
                {
                    "neutral": scale_to_dict(neutral_scale),
                    "accent": scale_to_dict(accent_scale),
                },
                indent=2,
            )
        )
    else:
        return _usage_error(f"Unknown format: {fmt!r}. Use 'css' or 'json'.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
