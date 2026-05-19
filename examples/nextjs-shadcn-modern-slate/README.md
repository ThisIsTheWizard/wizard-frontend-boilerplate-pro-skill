# Example: Modern Slate · Next.js · shadcn/ui

A clean, professional SaaS starter — the most common stack combination.

## Prompt

```
Create a Modern Slate Next.js app with shadcn/ui called "my-dashboard"
```

## Interview answers

| Question | Answer |
|---|---|
| Framework | Next.js (App Router) |
| UI library | shadcn/ui |
| Language | TypeScript |
| Color theme | Modern Slate (slate neutral + indigo accent) |
| Project name | my-dashboard |
| Package manager | *(auto-detected)* |
| Tailwind version | v4 *(auto-selected)* |

## What gets generated

```
my-dashboard/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout with ThemeProvider + FOUC script
│   │   ├── page.tsx                # Redirects to /library
│   │   └── library/
│   │       ├── layout.tsx          # Sidebar + header wrapper
│   │       ├── page.tsx            # /library landing with 6 category cards
│   │       ├── inputs/page.tsx
│   │       ├── display/page.tsx
│   │       ├── feedback/page.tsx
│   │       ├── navigation/page.tsx
│   │       ├── overlay/page.tsx
│   │       └── data-viz/page.tsx
│   ├── components/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   ├── ThemeProvider.tsx
│   │   ├── CodeBlock.tsx
│   │   └── ui/                     # 28 shadcn/ui components
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       └── ... (26 more)
│   ├── lib/
│   │   └── utils.ts                # cn() helper (clsx + tailwind-merge)
│   └── styles/
│       └── tokens.css              # OKLCH Modern Slate palette + semantic tokens
├── components.json                 # shadcn/ui config
├── tailwind.config.ts
└── tsconfig.json
```

## Color tokens (light mode excerpt)

```css
:root {
  --color-background:    oklch(98.4% 0.003 257.4);
  --color-foreground:    oklch(12.9% 0.026 257.4);
  --color-surface:       oklch(96.8% 0.006 257.4);
  --color-muted:         oklch(92.9% 0.012 257.4);
  --color-muted-fg:      oklch(55.4% 0.041 257.4);
  --color-accent:        oklch(55.4% 0.204 277.1);   /* indigo-500 */
  --color-accent-fg:     oklch(98.4% 0.013 277.1);
  --color-primary:       oklch(44.6% 0.042 257.4);
  --color-primary-fg:    oklch(98.4% 0.003 257.4);
  --radius:              0.5rem;
}
```

## Showcase routes

| Route | Components shown |
|---|---|
| `/library/inputs` | Button (6 variants), Input, Textarea, Select, Checkbox, RadioGroup, Switch |
| `/library/display` | Card, Badge (5 variants), Avatar, Separator, Skeleton, Table |
| `/library/feedback` | Alert (3 variants), Toast, Progress, Tooltip, Dialog |
| `/library/navigation` | Tabs, Breadcrumb, Pagination, NavigationMenu |
| `/library/overlay` | Popover, DropdownMenu, Sheet |
| `/library/data-viz` | Chart (Recharts), DataTable, Calendar |

## Key packages installed

```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@radix-ui/react-*": "latest",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.5.0",
    "recharts": "^2.13.0",
    "lucide-react": "^0.460.0"
  },
  "devDependencies": {
    "tailwindcss": "^4.0.0",
    "@tailwindcss/postcss": "^4.0.0",
    "typescript": "^5.6.0"
  }
}
```
