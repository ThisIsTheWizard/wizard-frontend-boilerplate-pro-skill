# React — Framework Adapter

Patterns and rules for adapting the 28 components from the ui-ux-pro-max-skill
(or from custom-tailwind.md fallback) into idiomatic React JSX.

---

## 1. File structure

Write all components to `src/components/ui/<Name>.tsx`. TypeScript is used
by default; omit `type` props on function signatures for JS projects.

Each file exports a single default component plus named types where needed:

```tsx
import * as React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
  asChild?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", asChild, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn("inline-flex items-center justify-center", className)}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
```

---

## 2. Ref forwarding

All components that render native elements use `React.forwardRef`. This allows
parent components (or Radix primitives) to access the underlying DOM node.

```tsx
export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        ref={ref}
        className={cn("flex h-10 w-full rounded-md border", className)}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";
```

---

## 3. Compound components (Slots pattern)

Components with sub-parts (Card, Dialog, Select, DropdownMenu, Popover, Sheet)
use the Slots pattern via Radix or headless UI:

```tsx
import * as React from "react";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}
export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("rounded-lg border bg-card", className)} {...props} />
  )
);
Card.displayName = "Card";

export const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
);
CardHeader.displayName = "CardHeader";

export const CardTitle = React.forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
  )
);
CardTitle.displayName = "CardTitle";

// ... etc.
```

---

## 4. Slot merging (cn utility)

Use `clsx` + `tailwind-merge` via a `cn()` helper to merge class names:

```ts
// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Import `cn` at the top of every component file. Never use `clsx` or `classnames`
directly — the merged output from `cn` handles Tailwind arbitrary value conflicts.

---

## 5. Event handlers

Native event handlers are spread directly via `{...props}` on native elements.
For custom callbacks, type them with React's event types:

```tsx
onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
```

---

## 6. Polymorphic components (asChild / component prop)

For components that wrap a different HTML tag or component (Button, Badge, etc.),
implement an `asChild` prop using `@radix-ui/react-slot`:

```tsx
import { Slot } from "@radix-ui/react-slot";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, asChild, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return <Comp ref={ref} className={cn(className)} {...props} />;
  }
);
```

---

## 7. Conditional classes

Use ternary chains inside `cn()` for variant/size props. Never use template
literals outside `cn()`:

```tsx
className={cn(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  variant === "destructive" && "bg-red-500 text-white",
  variant === "outline" && "border border-input bg-background",
  variant === "ghost" && "hover:bg-surface",
  variant === "default" && "bg-primary text-primary-foreground",
  size === "sm" && "h-9 px-3",
  size === "lg" && "h-11 px-8",
  size === "icon" && "h-10 w-10",
  className
)}
```

---

## 8. Server component awareness

For Next.js App Router, mark client-only components with `"use client"` at the
top when they use hooks, refs, or browser APIs. Server components use plain
exported functions without hooks.

---

## 9. Color token usage

All components use semantic CSS variable tokens, never raw palette scale values:

- `bg-background` — not `bg-neutral-50` directly
- `text-foreground` — not `text-neutral-950`
- `border-border` — not `border-neutral-200`
- `bg-primary` / `text-primary-foreground` — primary accent token
- `text-muted` — muted semantic token

The `cn()` call merges `className` last so user overrides always win.

---

## 10. Accessibility

Every component includes proper ARIA attributes and keyboard navigation:

- `role`, `aria-` attributes on interactive elements
- `aria-label` when an icon-only button has no visible text
- `aria-expanded` for collapsible components (Accordion, Disclosure)
- `aria-selected` for listbox/tab options
- Focus ring via `focus-visible:ring-2 focus-visible:ring-primary`