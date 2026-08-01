import { Skeleton } from "@/components/ui/skeleton";

/**
 * Loading skeletons that mirror the real layouts so the page doesn't
 * jump when data arrives. Each list wrapper carries the loading
 * semantics (role="status" + aria-busy); the inner blocks are
 * decorative.
 */

/** Mirrors <EventCard>: media block + category tag + title + meta rows. */
export function EventCardSkeleton() {
  return (
    <div className="flex h-full flex-col overflow-hidden rounded-xl bg-surface shadow-ambient">
      <Skeleton className="h-44 w-full rounded-none" />
      <div className="flex flex-grow flex-col gap-sm p-md">
        <Skeleton className="h-6 w-24 rounded-full" />
        <Skeleton className="h-6 w-4/5" />
        <Skeleton className="h-6 w-3/5" />
        <div className="mt-auto flex flex-col gap-xs pt-sm">
          <Skeleton className="h-5 w-1/2" />
          <Skeleton className="h-5 w-1/3" />
        </div>
      </div>
    </div>
  );
}

/** Grid of card skeletons for the public events list / dashboards. */
export function EventCardGridSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div
      role="status"
      aria-busy="true"
      aria-label="Loading events"
      className="grid gap-gutter sm:grid-cols-2 lg:grid-cols-3"
    >
      <span className="sr-only">Loading events…</span>
      {Array.from({ length: count }).map((_, i) => (
        <EventCardSkeleton key={i} />
      ))}
    </div>
  );
}

/** Mirrors the admin/organizer management row (title + status + meta + actions). */
export function EventRowSkeleton() {
  return (
    <div className="glass-card flex flex-wrap items-center justify-between gap-md rounded-xl p-md shadow-ambient">
      <div className="flex flex-col gap-xs">
        <div className="flex items-center gap-sm">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-6 w-20 rounded-full" />
        </div>
        <Skeleton className="h-4 w-64" />
      </div>
      <div className="flex gap-xs">
        <Skeleton className="h-10 w-28 rounded-full" />
        <Skeleton className="h-10 w-24 rounded-full" />
      </div>
    </div>
  );
}

/** Stacked management rows for the admin events / organizer dashboard. */
export function EventRowListSkeleton({ count = 4 }: { count?: number }) {
  return (
    <div role="status" aria-busy="true" aria-label="Loading events" className="grid gap-gutter">
      <span className="sr-only">Loading events…</span>
      {Array.from({ length: count }).map((_, i) => (
        <EventRowSkeleton key={i} />
      ))}
    </div>
  );
}
