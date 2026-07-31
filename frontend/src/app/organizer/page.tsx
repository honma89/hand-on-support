"use client";

import Link from "next/link";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useOrganizerEvents } from "@/lib/hooks/use-events";
import type { EventStatus } from "@/lib/types";

const STATUS_STYLES: Record<EventStatus, string> = {
  draft: "bg-outline-variant/40 text-on-surface-variant",
  published: "bg-primary-container text-on-primary-container",
  cancelled: "bg-error/10 text-error",
  completed: "bg-secondary-container text-secondary",
};

export default function OrganizerDashboardPage() {
  const { data: user } = useCurrentUser();
  const { data: events, isLoading, isError } = useOrganizerEvents(user?.id);

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-lg flex-wrap gap-sm">
          <div>
            <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-xs">
              My Events
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant">
              Events you organize, including drafts not yet published.
            </p>
          </div>
          <Link
            href="/admin/events/new"
            className="btn-primary rounded-full px-md py-sm inline-flex items-center gap-xs"
          >
            <span className="material-symbols-outlined text-lg">add_circle</span>
            Create Event
          </Link>
        </div>

        {isLoading && (
          <p className="text-on-surface-variant font-body-md text-body-md">Loading your events…</p>
        )}
        {isError && (
          <p className="text-error font-body-md text-body-md">
            Could not load your events. Try refreshing.
          </p>
        )}
        {events && events.length === 0 && (
          <p className="text-on-surface-variant font-body-md text-body-md">
            You haven&apos;t created any events yet.
          </p>
        )}

        <div className="grid gap-gutter">
          {events?.map((event) => (
            <div
              key={event.id}
              className="glass-card rounded-xl p-md shadow-ambient shadow-ambient-hover transition-shadow flex items-center justify-between gap-md flex-wrap"
            >
              <div>
                <div className="flex items-center gap-sm mb-xs flex-wrap">
                  <p className="font-headline-md text-headline-md text-on-surface">
                    {event.title}
                  </p>
                  <span
                    className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ${STATUS_STYLES[event.status]}`}
                  >
                    {event.status}
                  </span>
                </div>
                <p className="font-body-md text-sm text-on-surface-variant">
                  {new Date(event.start_datetime).toLocaleString(undefined, {
                    dateStyle: "medium",
                    timeStyle: "short",
                  })}{" "}
                  · {event.dzongkhag}
                </p>
              </div>
              <Link
                href={`/organizer/events/${event.id}/attendance`}
                className="btn-secondary rounded-full px-md py-sm inline-flex items-center gap-xs shrink-0"
              >
                <span className="material-symbols-outlined text-lg">how_to_reg</span>
                Manage attendance
              </Link>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
