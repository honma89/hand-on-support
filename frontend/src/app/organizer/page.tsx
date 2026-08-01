"use client";

import { useState } from "react";
import Link from "next/link";
import { isAxiosError } from "axios";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useCoordinationEvents, useUpdateEvent } from "@/lib/hooks/use-events";
import type { EventPublic, EventStatus } from "@/lib/types";

const STATUS_STYLES: Record<EventStatus, string> = {
  draft: "bg-outline-variant/40 text-on-surface-variant",
  published: "bg-primary-container text-on-primary-container",
  cancelled: "bg-error/10 text-error",
  completed: "bg-secondary-container text-secondary",
};

// Organizers can publish/unpublish/cancel their own events, same as
// admins can -- the backend already allows this (an organizer manages
// any event where event.organizer_id === their own id), this just
// surfaces the controls here too.
function MyEventStatusControls({ event }: { event: EventPublic }) {
  const updateEvent = useUpdateEvent(event.id);
  const [error, setError] = useState<string | null>(null);

  const setStatus = async (status: EventStatus) => {
    setError(null);
    try {
      await updateEvent.mutateAsync({ status });
    } catch (err) {
      setError(
        isAxiosError(err)
          ? (err.response?.data?.detail as string | undefined) ?? "Could not update the event."
          : "Could not update the event.",
      );
    }
  };

  return (
    <div className="flex items-center gap-xs flex-wrap">
      {event.status === "draft" && (
        <button
          onClick={() => setStatus("published")}
          disabled={updateEvent.isPending}
          className="btn-primary rounded-full px-md py-sm inline-flex items-center gap-xs text-sm"
        >
          <span className="material-symbols-outlined text-lg">publish</span>
          Publish
        </button>
      )}
      {event.status === "published" && (
        <button
          onClick={() => setStatus("draft")}
          disabled={updateEvent.isPending}
          className="btn-secondary rounded-full px-md py-sm inline-flex items-center gap-xs text-sm"
        >
          <span className="material-symbols-outlined text-lg">unpublished</span>
          Unpublish
        </button>
      )}
      {(event.status === "draft" || event.status === "published") && (
        <button
          onClick={() => setStatus("cancelled")}
          disabled={updateEvent.isPending}
          className="rounded-full px-md py-sm inline-flex items-center gap-xs text-sm text-error hover:bg-error/10 transition-colors"
        >
          <span className="material-symbols-outlined text-lg">cancel</span>
          Cancel
        </button>
      )}
      {error && <p className="text-sm text-error basis-full">{error}</p>}
    </div>
  );
}

export default function OrganizerDashboardPage() {
  const { data: user } = useCurrentUser();
  const { data: events, isLoading, isError } = useCoordinationEvents();

  const myEvents = events?.filter((e) => e.organizer_id === user?.id) ?? [];
  const otherPublished = events?.filter((e) => e.organizer_id !== user?.id) ?? [];

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-lg flex-wrap gap-sm">
          <div>
            <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-xs">
              Organizer Dashboard
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant">
              Manage your own events, and see what everyone else has published for coordination.
            </p>
          </div>
          <Link
            href="/organizer/events/new"
            className="btn-primary rounded-full px-md py-sm inline-flex items-center gap-xs"
          >
            <span className="material-symbols-outlined text-lg">add_circle</span>
            Create Event
          </Link>
        </div>

        {isLoading && (
          <p className="text-on-surface-variant font-body-md text-body-md">Loading events…</p>
        )}
        {isError && (
          <p className="text-error font-body-md text-body-md">Could not load events. Try refreshing.</p>
        )}

        <section className="mb-xl">
          <h2 className="font-headline-md text-headline-md text-on-surface mb-sm">My Events</h2>
          {myEvents.length === 0 && !isLoading && (
            <p className="text-on-surface-variant font-body-md text-body-md">
              You haven&apos;t created any events yet.
            </p>
          )}
          <div className="grid gap-gutter">
            {myEvents.map((event) => (
              <div
                key={event.id}
                className="glass-card rounded-xl p-md shadow-ambient shadow-ambient-hover transition-shadow flex items-center justify-between gap-md flex-wrap"
              >
                <div>
                  <div className="flex items-center gap-sm mb-xs flex-wrap">
                    <p className="font-headline-md text-headline-md text-on-surface">{event.title}</p>
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
                {/* Manage controls only ever render here, inside "My Events" --
                    events in "Published by other organizers" below never get
                    these controls, since this section is filtered to
                    event.organizer_id === user.id. */}
                <div className="flex items-center gap-xs flex-wrap shrink-0">
                  <MyEventStatusControls event={event} />
                  <Link
                    href={`/organizer/events/${event.id}/attendance`}
                    className="btn-secondary rounded-full px-md py-sm inline-flex items-center gap-xs shrink-0"
                  >
                    <span className="material-symbols-outlined text-lg">how_to_reg</span>
                    Manage attendance
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section>
          <h2 className="font-headline-md text-headline-md text-on-surface mb-sm">
            Published by Other Organizers
          </h2>
          <p className="font-body-md text-sm text-on-surface-variant mb-sm">
            Read-only, for coordination -- you can&apos;t edit or manage these.
          </p>
          {otherPublished.length === 0 && !isLoading && (
            <p className="text-on-surface-variant font-body-md text-body-md">
              No other published events right now.
            </p>
          )}
          <div className="grid gap-gutter">
            {otherPublished.map((event) => (
              <Link
                key={event.id}
                href={`/events/${event.id}`}
                className="glass-card rounded-xl p-md shadow-ambient flex items-center justify-between gap-md flex-wrap opacity-90"
              >
                <div>
                  <p className="font-headline-md text-headline-md text-on-surface">{event.title}</p>
                  <p className="font-body-md text-sm text-on-surface-variant">
                    {new Date(event.start_datetime).toLocaleString(undefined, {
                      dateStyle: "medium",
                      timeStyle: "short",
                    })}{" "}
                    · {event.dzongkhag}
                  </p>
                </div>
                <span className="material-symbols-outlined text-on-surface-variant">chevron_right</span>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
