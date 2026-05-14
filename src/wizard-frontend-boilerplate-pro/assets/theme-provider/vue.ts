import { readonly, ref } from "vue";

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

const theme = ref<Theme>(
  typeof window !== "undefined"
    ? ((localStorage.getItem(STORAGE_KEY) as Theme | null) ?? "system")
    : "system",
);

function setTheme(next: Theme): void {
  if (typeof window !== "undefined") localStorage.setItem(STORAGE_KEY, next);
  theme.value = next;
  applyTheme(next);
}

function toggleTheme(): void {
  const resolved = theme.value === "system" ? getSystemTheme() : theme.value;
  setTheme(resolved === "dark" ? "light" : "dark");
}

if (typeof window !== "undefined") {
  applyTheme(theme.value);

  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", () => {
      if (theme.value === "system") applyTheme("system");
    });

  window.addEventListener("storage", (e: StorageEvent) => {
    if (e.key === STORAGE_KEY) {
      theme.value = (e.newValue as Theme | null) ?? "system";
      applyTheme(theme.value);
    }
  });
}

export function useTheme() {
  return {
    setTheme,
    theme: readonly(theme),
    toggleTheme,
  };
}

/**
 * Paste into <head> before any CSS to prevent flash of unstyled content.
 * Nuxt: add via useHead({ script: [{ innerHTML: fouc, tagPosition: 'head' }] }).
 * Vue + Vite: add as an inline <script> in index.html.
 */
export const fouc =
  "(function(){" +
  "var s=localStorage.getItem('theme');" +
  "var d=window.matchMedia('(prefers-color-scheme: dark)').matches;" +
  "var t=s||(d?'dark':'light');" +
  "if(t==='dark'){document.documentElement.classList.add('dark')}" +
  "})();";
