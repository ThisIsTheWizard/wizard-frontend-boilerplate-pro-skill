# Wizard Frontend Boilerplate Pro

A comprehensive skill for scaffolding production-ready frontend applications with themed component showcases, design tokens, and light/dark theming.

## Overview

This skill enables you to quickly scaffold frontend projects using Next.js, React + Vite, Vue 3, Nuxt 4, or SvelteKit. Each scaffolded project includes:

- **28 pre-built UI components** across 6 categories (inputs, display, feedback, navigation, overlay, data-viz)
- **Automatic color palette generation** using OKLCH algorithm (50-950 scales)
- **Light/dark theme support** with FOUC prevention
- **Tailwind v4 support** with @theme directive
- **Component showcase** with collapsible code snippets
- **WCAG AA compliant** color contrast

## Supported Frameworks

| Framework | Version | Router |
|-----------|---------|--------|
| Next.js | 15+ | App Router |
| React + Vite | Latest | React Router |
| Vue | 3.5+ | Vue Router |
| Nuxt | 4 | Nuxt Router |
| SvelteKit | Svelte 5 | SvelteKit Router |

## Quick Start

```bash
# Using opencode
opencode skill wizard-frontend-boilerplate-pro
```

The skill will interview you through 6 questions:

1. **Framework** - Choose from Next.js, React + Vite, Vue, Nuxt, or SvelteKit
2. **Version** - Latest stable, specific version, or LTS
3. **Language** - TypeScript (default) or JavaScript
4. **Tailwind version** - v4 (default) or v3
5. **Color theme** - Modern Slate, Custom hex, or Preset colors
6. **Package manager** - pnpm, yarn, npm, or bun

## Features

### 7-Phase Scaffolding Workflow

1. **Interview** - Gather project requirements
2. **Version Resolution** - Query npm registry for latest versions
3. **Scaffold** - Create framework-specific project structure
4. **Color Palette** - Generate OKLCH-based color scales
5. **Components** - Install 28 UI components
6. **Showcase** - Build sidebar navigation with code snippets
7. **Verification** - End-to-end validation with WCAG AA checks

### Color System

- **8 preset palettes**: Modern Slate, Ocean Blue, Forest Green, Sunset Orange, Royal Purple, Rose Pink, Monochrome, Custom
- **OKLCH algorithm**: 50-950 lightness scales
- **Light/dark mappings**: Automatic CSS variable generation

### Component Categories

- **Inputs**: Button, Input, Select, Checkbox, Radio, Toggle, Slider, Textarea
- **Display**: Badge, Card, Avatar, Tag, List, Table, Timeline
- **Feedback**: Alert, Toast, Progress, Skeleton, Empty, Spinner
- **Navigation**: Navbar, Tabs, Breadcrumb, Pagination, Sidebar
- **Overlay**: Modal, Drawer, Popover, Tooltip, Dropdown
- **Data Viz**: Chart, Bar, Line, Pie, Area

## Integration with ui-ux-pro-max

This skill pairs with `ui-ux-pro-max` skill for enhanced UI/UX recommendations:

- Style guidelines (glassmorphism, minimalism, brutalism, etc.)
- Color palette suggestions
- Typography pairings
- Accessibility compliance

## Directory Structure

```
wizard-frontend-boilerplate-pro/
├── SKILL.md              # Main skill definition
├── workflow.md           # Detailed playbook
├── references/          # Framework-specific guides
│   ├── frameworks/      # Next.js, React, Vue, Nuxt, Svelte
│   ├── tailwind/        # v4 setup, v3 fallback, per-framework gotchas
│   ├── ui-library/      # Component integration, adapters
│   ├── theming.md       # CSS variables, dark mode strategy
│   ├── component-catalog.md
│   └── showcase-layout.md
├── assets/
│   ├── color-presets.json
│   ├── showcase-templates/  # Per-framework templates
│   └── theme-provider/       # React, Vue, Svelte providers
├── scripts/
│   ├── generate_palette.py   # OKLCH color scale generator
│   ├── verify_contrast.py    # WCAG AA validation
│   ├── check_versions.sh     # npm version queries
│   └── detect_package_manager.sh
└── .claude-plugin/      # Distribution files
    ├── plugin.json
    └── marketplace.json
```

## Requirements

- Node.js 24+
- Any AI agent CLI (Aider, Claude, Claude Code, Codex, Continue, Cursor, Gemini, Gemini CLI, Opencode, Tabby, Windsurf)
- Python 3.10+ (for color palette generation scripts)

## License

MIT

## Contributing

Contributions are welcome! Please open an issue or submit a PR on GitHub.