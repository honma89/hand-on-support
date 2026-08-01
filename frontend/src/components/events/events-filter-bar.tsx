"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import {
  Sheet,
  SheetTrigger,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
  SheetFooter,
  SheetClose,
} from "@/components/ui/sheet";
import { DZONGKHAGS, EVENT_CATEGORIES } from "@/lib/constants/bhutan";

/** The full filter state owned by the parent page. */
export interface EventFilters {
  /** Free-text title search. */
  query: string;
  /** Selected category, or "" for all. */
  category: string;
  /** Selected dzongkhag, or "" for all. */
  dzongkhag: string;
  /** Only show events that haven't started yet. */
  upcomingOnly: boolean;
}

export const EMPTY_EVENT_FILTERS: EventFilters = {
  query: "",
  category: "",
  dzongkhag: "",
  upcomingOnly: false,
};

/** Count of *facet* filters active (search is surfaced separately). */
function countActive(f: EventFilters) {
  return [f.category, f.dzongkhag].filter(Boolean).length + (f.upcomingOnly ? 1 : 0);
}

interface FieldProps {
  value: EventFilters;
  onChange: (next: EventFilters) => void;
}

/** Accessible pill toggle for the upcoming-only switch. */
function UpcomingToggle({ value, onChange }: FieldProps) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={value.upcomingOnly}
      aria-label="Show upcoming events only"
      onClick={() => onChange({ ...value, upcomingOnly: !value.upcomingOnly })}
      className={cn(
        "inline-flex h-11 items-center gap-xs whitespace-nowrap rounded-full border px-4 font-label-md text-label-md transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
        value.upcomingOnly
          ? "border-primary-container bg-primary-container text-on-primary-container"
          : "border-outline bg-surface text-on-surface-variant hover:bg-surface-container",
      )}
    >
      <span aria-hidden="true" className="material-symbols-outlined text-lg">
        {value.upcomingOnly ? "event_available" : "event"}
      </span>
      Upcoming only
    </button>
  );
}

/** The category + dzongkhag + toggle controls, reused inline and in the sheet. */
function FilterFields({ value, onChange, stacked }: FieldProps & { stacked?: boolean }) {
  return (
    <div className={cn("flex gap-sm", stacked ? "flex-col" : "items-center")}>
      <label className={cn("flex flex-col gap-xs", stacked && "w-full")}>
        <span className="sr-only">Category</span>
        <Select
          aria-label="Filter by category"
          value={value.category}
          onChange={(e) => onChange({ ...value, category: e.target.value })}
          className={cn(!stacked && "h-11 w-auto min-w-40 py-0")}
        >
          <option value="">All categories</option>
          {EVENT_CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </Select>
      </label>

      <label className={cn("flex flex-col gap-xs", stacked && "w-full")}>
        <span className="sr-only">Dzongkhag</span>
        <Select
          aria-label="Filter by dzongkhag (district)"
          value={value.dzongkhag}
          onChange={(e) => onChange({ ...value, dzongkhag: e.target.value })}
          className={cn(!stacked && "h-11 w-auto min-w-40 py-0")}
        >
          <option value="">All districts</option>
          {DZONGKHAGS.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </Select>
      </label>

      <UpcomingToggle value={value} onChange={onChange} />
    </div>
  );
}

export interface EventsFilterBarProps {
  value: EventFilters;
  onChange: (next: EventFilters) => void;
  className?: string;
}

/**
 * A single, unified control bar for browsing events.
 *
 * - Desktop (md+): search box + facet controls sit together in one
 *   glass-card row so it reads as one instrument, not three orphaned
 *   dropdowns.
 * - Mobile: only the search box + a "Filters" button show; the facets
 *   collapse into a bottom sheet with a live active-filter count and a
 *   Reset action, so a phone screen stays uncluttered.
 *
 * Fully controlled — the parent owns `value` and passes `onChange`.
 */
export function EventsFilterBar({ value, onChange, className }: EventsFilterBarProps) {
  const [sheetOpen, setSheetOpen] = useState(false);
  const activeCount = countActive(value);

  const reset = () => onChange({ ...EMPTY_EVENT_FILTERS, query: value.query });

  return (
    <div className={cn("glass-card rounded-xl p-sm shadow-ambient", className)}>
      <div className="flex items-center gap-sm">
        {/* Search — always visible, full-width on mobile. */}
        <div className="relative flex-1">
          <span
            aria-hidden="true"
            className="material-symbols-outlined pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant"
          >
            search
          </span>
          <Input
            type="search"
            aria-label="Search events by title"
            placeholder="Search events…"
            value={value.query}
            onChange={(e) => onChange({ ...value, query: e.target.value })}
            className="h-11 border-transparent bg-surface-container-low pl-11"
          />
        </div>

        {/* Desktop: inline facets. */}
        <div className="hidden items-center gap-sm md:flex">
          <FilterFields value={value} onChange={onChange} />
          {activeCount > 0 && (
            <button
              type="button"
              onClick={reset}
              className="inline-flex h-11 items-center gap-xs whitespace-nowrap rounded-full px-3 font-label-md text-label-md text-on-surface-variant transition-colors hover:bg-surface-container focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <span aria-hidden="true" className="material-symbols-outlined text-lg">
                restart_alt
              </span>
              Reset
            </button>
          )}
        </div>

        {/* Mobile: a single Filters button that opens the sheet. */}
        <div className="md:hidden">
          <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
            <SheetTrigger
              className="relative inline-flex h-11 items-center gap-xs whitespace-nowrap rounded-full border border-outline bg-surface px-4 font-label-md text-label-md text-on-surface transition-colors hover:bg-surface-container focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              aria-label={`Filters${activeCount ? `, ${activeCount} active` : ""}`}
            >
              <span aria-hidden="true" className="material-symbols-outlined text-lg">
                tune
              </span>
              Filters
              {activeCount > 0 && (
                <span className="ml-1 inline-flex h-5 min-w-5 items-center justify-center rounded-full bg-primary-container px-1 font-label-md text-xs text-on-primary-container">
                  {activeCount}
                </span>
              )}
            </SheetTrigger>

            <SheetContent side="bottom" className="max-h-[85vh]">
              <SheetHeader>
                <SheetTitle>Filter events</SheetTitle>
                <SheetDescription>
                  Narrow opportunities by category, district, or timing.
                </SheetDescription>
              </SheetHeader>

              <div className="overflow-y-auto py-sm">
                <FilterFields value={value} onChange={onChange} stacked />
              </div>

              <SheetFooter>
                <button
                  type="button"
                  onClick={reset}
                  disabled={activeCount === 0}
                  className="inline-flex h-11 items-center justify-center gap-xs rounded-full px-6 font-label-md text-label-md text-on-surface-variant transition-colors hover:bg-surface-container disabled:opacity-40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                >
                  Reset
                </button>
                <SheetClose className="inline-flex h-11 items-center justify-center rounded-full bg-primary-container px-6 font-label-md text-label-md text-on-primary-container transition-colors hover:bg-primary-fixed-dim focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
                  Show results
                </SheetClose>
              </SheetFooter>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </div>
  );
}
