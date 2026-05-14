import { writable } from "svelte/store";

type Theme = "dark" | "light" | "system";

const STORAGE_KEY = "theme";

function getSystemTheme(): "dark" | "light" {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function applyTheme(theme: Theme): void {
  if (typeof document === "undefined") return;
  const resolved = theme === "system" ? getSystemTheme() : theme;
  document.documentElement.classList.toggle("dark", resolved === "dark");
}

const stored =
  typeof window !== "undefined"
    ? (localStorage.getItem(STORAGE_KEY) as Theme | null)
    : null;

const { set, subscribe, update } = writable<Theme>(stored ?? "system");

if (typeof window !== "undefined") {
  applyTheme(stored ?? "system");

  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", () => {
      update((current) => {
        if (current === "system") applyTheme("system");
        return current;
      });
    });

  window.addEventListener("storage", (e: StorageEvent) => {
    if (e.key === STORAGE_KEY) {
      const next = (e.newValue as Theme | null) ?? "system";
      set(next);
      applyTheme(next);
    }
  });
}

export function setTheme(next: Theme): void {
  if (typeof window !== "undefined") localStorage.setItem(STORAGE_KEY, next);
  set(next);
  applyTheme(next);
}

export function toggleTheme(): void {
  update((current) => {
    const resolved = current === "system" ? getSystemTheme() : current;
    const next: Theme = resolved === "dark" ? "light" : "dark";
    if (typeof window !== "undefined") localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);
    return next;
  });
}

/** Readable store — use as `$theme` in Svelte components. */
export const theme = { subscribe };

/**
 * Paste into <head> before any CSS to prevent flash of unstyled content.
 * SvelteKit: add inside <svelte:head> in src/routes/+layout.svelte using
 * a {@html fouc} expression wrapped in a <script> tag.
 */
export const fouc =
  "(function(){" +
  "var s=localStorage.getItem('theme');" +
  "var d=window.matchMedia('(prefers-color-scheme: dark)').matches;" +
  "var t=s||(d?'dark':'light');" +
  "if(t==='dark'){document.documentElement.classList.add('dark')}" +
  "})();";
