"use client";

import Link from "next/link";
import { useEvents } from "@/lib/hooks/use-events";

function formatEventDate(iso: string) {
  const d = new Date(iso);
  return {
    month: d.toLocaleDateString("en-US", { month: "short" }).toUpperCase(),
    day: d.toLocaleDateString("en-US", { day: "2-digit" }),
  };
}

export default function EventsPage() {
  const { data: events, isLoading, isError } = useEvents();

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-7xl mx-auto">
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-xs">
          Upcoming Opportunities
        </h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant mb-lg">
          Find a community service event near you and start earning Point Bank rewards.
        </p>

        {isLoading && <p className="text-on-surface-variant font-body-md text-body-md">Loading events…</p>}
        {isError && <p className="text-error font-body-md text-body-md">Could not load events. Please try again.</p>}
        {events && events.length === 0 && (
          <p className="text-on-surface-variant font-body-md text-body-md">
            No upcoming events right now — check back soon.
          </p>
        )}

        <div className="grid gap-gutter sm:grid-cols-2 lg:grid-cols-3">
          {events?.map((event) => {
            const { month, day } = formatEventDate(event.start_datetime);
            return (
              <Link key={event.id} href={`/events/${event.id}`}>
                <div className="bg-surface rounded-xl shadow-ambient shadow-ambient-hover overflow-hidden flex flex-col h-full transition-all duration-300">
                  <div className="h-40 relative bg-gradient-to-br from-primary-container to-secondary-container flex items-center justify-center">
                    <span className="material-symbols-outlined text-white/80 text-5xl">
                      volunteer_activism
                    </span>
                    <div className="absolute top-sm right-sm bg-surface px-sm py-xs rounded-md shadow-sm flex flex-col items-center">
                      <span className="font-label-md text-label-md text-secondary">{month}</span>
                      <span className="font-headline-md text-headline-md text-on-surface leading-none">
                        {day}
                      </span>
                    </div>
                  </div>
                  <div className="p-md flex flex-col gap-sm flex-grow">
                    <span className="bg-secondary-container/10 text-secondary px-sm py-xs rounded-full font-label-md text-label-md w-fit">
                      {event.category}
                    </span>
                    <h3 className="font-headline-md text-headline-md text-on-surface line-clamp-2">
                      {event.title}
                    </h3>
                    <div className="flex items-center gap-xs text-on-surface-variant font-body-md text-body-md mt-auto pt-sm">
                      <span className="material-symbols-outlined text-lg">location_on</span>
                      <span>{event.dzongkhag}</span>
                    </div>
                    <div className="flex items-center gap-xs text-primary font-label-md text-label-md">
                      <span className="material-symbols-outlined text-lg">stars</span>
                      {event.points_reward} points
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </main>
  );
}
