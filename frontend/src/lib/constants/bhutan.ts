/**
 * Shared Bhutan-specific constants and event-category theming.
 *
 * Centralised here so the events filter bar, event cards and any future
 * surfaces all agree on the same district list and the same category
 * colours/icons — instead of each component inventing its own.
 *
 * All colours reference design-system tokens (primary / secondary /
 * tertiary + their containers). No raw hex is used anywhere.
 */

/** Bhutan's 20 dzongkhags (districts), alphabetical. */
export const DZONGKHAGS = [
  "Bumthang",
  "Chhukha",
  "Dagana",
  "Gasa",
  "Haa",
  "Lhuentse",
  "Mongar",
  "Paro",
  "Pemagatshel",
  "Punakha",
  "Samdrup Jongkhar",
  "Samtse",
  "Sarpang",
  "Thimphu",
  "Trashigang",
  "Trashiyangtse",
  "Trongsa",
  "Tsirang",
  "Wangdue Phodrang",
  "Zhemgang",
] as const;

export type Dzongkhag = (typeof DZONGKHAGS)[number];

/**
 * Visual theme for an event category.
 *
 * - `icon`     Material Symbols Outlined ligature (matches the icon set
 *              already used across the app via <span className="material-symbols-outlined">).
 * - `gradient` Tailwind gradient classes used for the image *fallback*
 *              surface, built only from design-system container tokens.
 * - `onGradient` Foreground colour that reads well on that gradient.
 */
export interface CategoryTheme {
  icon: string;
  gradient: string;
  onGradient: string;
}

/**
 * Known categories mapped to a distinct token-based theme. Keys are the
 * canonical category strings; lookups are case-insensitive (see
 * getCategoryTheme). Colours rotate through the three brand hues so a
 * list of mixed categories stays visually varied but on-brand.
 */
export const CATEGORY_THEMES: Record<string, CategoryTheme> = {
  environment: {
    icon: "eco",
    gradient: "bg-gradient-to-br from-tertiary-container to-tertiary",
    onGradient: "text-on-tertiary",
  },
  education: {
    icon: "school",
    gradient: "bg-gradient-to-br from-primary-container to-primary",
    onGradient: "text-on-primary",
  },
  health: {
    icon: "health_and_safety",
    gradient: "bg-gradient-to-br from-secondary-container to-secondary",
    onGradient: "text-on-secondary",
  },
  community: {
    icon: "diversity_3",
    gradient: "bg-gradient-to-br from-primary-fixed to-primary-fixed-dim",
    onGradient: "text-on-primary-fixed",
  },
  culture: {
    icon: "temple_buddhist",
    gradient: "bg-gradient-to-br from-secondary-fixed to-secondary-fixed-dim",
    onGradient: "text-on-secondary-fixed",
  },
  "disaster relief": {
    icon: "emergency",
    gradient: "bg-gradient-to-br from-secondary-container to-secondary",
    onGradient: "text-on-secondary",
  },
  sports: {
    icon: "sports_soccer",
    gradient: "bg-gradient-to-br from-tertiary-fixed to-tertiary-fixed-dim",
    onGradient: "text-on-tertiary-fixed",
  },
};

/** Fallback theme for any category we don't have an explicit mapping for. */
export const DEFAULT_CATEGORY_THEME: CategoryTheme = {
  icon: "volunteer_activism",
  gradient: "bg-gradient-to-br from-primary-container to-secondary-container",
  onGradient: "text-on-primary-container",
};

/**
 * Resolve the theme for a category string. Matching is case-insensitive
 * and also tries a loose "contains" match so "Environmental Cleanup"
 * still resolves to the "environment" theme. Falls back to a neutral
 * brand gradient when nothing matches.
 */
export function getCategoryTheme(category: string | null | undefined): CategoryTheme {
  if (!category) return DEFAULT_CATEGORY_THEME;
  const key = category.trim().toLowerCase();
  if (CATEGORY_THEMES[key]) return CATEGORY_THEMES[key];
  const partial = Object.keys(CATEGORY_THEMES).find(
    (k) => key.includes(k) || k.includes(key),
  );
  return partial ? CATEGORY_THEMES[partial] : DEFAULT_CATEGORY_THEME;
}

/** Categories offered in the filter bar. Extend freely — themes fall back gracefully. */
export const EVENT_CATEGORIES = [
  "Environment",
  "Education",
  "Health",
  "Community",
  "Culture",
  "Disaster Relief",
  "Sports",
] as const;
