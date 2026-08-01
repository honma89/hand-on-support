"use client";

import { useMemo, useState } from "react";
import { useEvents } from "@/lib/hooks/use-events";
import { EventCard } from "@/components/events/event-card";
import {
  EventsFilterBar,
  EMPTY_EVENT_FILTERS,
  type EventFilters,
} from "@/components/events/events-filter-bar";
import { EventCardGridSkeleton } from "@/components/common/loading-skeletons";
import { EmptyState } from "@/components/common/empty-state";

export default function EventsPage() {
  const { data: events, isLoading, isError } = useEvents();
  const [filters, setFilters] = useState<EventFilters>(EMPTY_EVENT_FILTERS);

  // Client-side filtering keeps this instant + offline-friendly. Swap to
  // server params (useEvents({ category, dzongkhag })) if the dataset
  // ever grows beyond a single page.
  const filtered = useMemo(() => {
    if (!events) return [];
    const now = Date.now();
    const q = filters.query.trim().toLowerCase();
    return events.filter((e) => {
      if (q && !e.title.toLowerCase().includes(q)) return false;
      if (filters.category && e.category !== filters.category) return false;
      if (filters.dzongkhag && e.dzongkhag !== filters.dzongkhag) return false;
      if (filters.upcomingOnly && new Date(e.start_datetime).getTime() < now) return false;
      return true;
    });
  }, [events, filters]);

  const hasActiveFilters =
    Boolean(filters.query || filters.category || filters.dzongkhag) || filters.upcomingOnly;

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="mx-auto max-w-7xl">
        <h1 className="mb-xs font-display-lg text-headline-lg text-on-surface md:text-display-lg text-balance">
          Upcoming Opportunities
        </h1>
        <p className="mb-lg font-body-lg text-body-lg text-on-surface-variant text-pretty">
          Find a community service event near you and start earning Point Bank rewards.
        </p>

        <div className="mb-lg">
          <EventsFilterBar value={filters} onChange={setFilters} />
        </div>

        {/* Loading: skeleton grid matching the real card layout. */}
        {isLoading && <EventCardGridSkeleton />}

        {/* Error: friendly, retry-able empty state. */}
        {isError && (
          <EmptyState
            variant="error"
            title="We couldn't load events"
            description="Something went wrong reaching the server. Please check your connection and try again."
          />
        )}

        {/* Loaded but nothing matches. Distinguish "no events at all" from
            "no events for these filters" so the CTA makes sense. */}
        {events && filtered.length === 0 && !isLoading && (
          <EmptyState
            icon={hasActiveFilters ? "search_off" : "event_busy"}
            title={hasActiveFilters ? "No matching events" : "No upcoming events yet"}
            description={
              hasActiveFilters
                ? "Try widening your filters — a different district or category might have openings."
                : "There are no opportunities posted right now. Check back soon — new events are added regularly."
            }
          />
        )}

        {filtered.length > 0 && (
          <div className="grid gap-gutter sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((event) => (
              // Public list: every event is already published, so hide the
              // status pill to keep the card clean.
              <EventCard key={event.id} event={event} showStatus={false} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
