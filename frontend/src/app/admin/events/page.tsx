"use client";

import { useState } from "react";
import Link from "next/link";
import { isAxiosError } from "axios";
import { useAllEventsAdmin, useUpdateEvent } from "@/lib/hooks/use-events";
import type { EventPublic, EventStatus } from "@/lib/types";

const STATUS_STYLES: Record<EventStatus, string> = {
  draft: "bg-outline-variant/40 text-on-surface-variant",
  published: "bg-primary-container text-on-primary-container",
  cancelled: "bg-error/10 text-error",
  completed: "bg-secondary-container text-secondary",
};

function EventRow({ event }: { event: EventPublic }) {
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
    <div className="glass-card rounded-xl p-md shadow-ambient flex items-center justify-between gap-md flex-wrap">
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
          · {event.dzongkhag} · {event.category}
        </p>
        {error && <p className="text-sm text-error mt-xs">{error}</p>}
      </div>

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
        <Link
          href={`/organizer/events/${event.id}/attendance`}
          className="rounded-full px-md py-sm inline-flex items-center gap-xs text-sm text-on-surface-variant hover:bg-surface-container transition-colors"
        >
          <span className="material-symbols-outlined text-lg">how_to_reg</span>
          Attendance
        </Link>
        <Link
          href={`/events/${event.id}`}
          className="rounded-full px-md py-sm inline-flex items-center gap-xs text-sm text-on-surface-variant hover:bg-surface-container transition-colors"
        >
          <span className="material-symbols-outlined text-lg">visibility</span>
          View
        </Link>
      </div>
    </div>
  );
}

export default function AdminEventsPage() {
  const { data: events, isLoading, isError } = useAllEventsAdmin();

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-lg flex-wrap gap-sm">
          <div>
            <Link
              href="/admin"
              className="inline-flex items-center gap-xs font-label-md text-label-md text-on-surface-variant hover:text-primary mb-xs"
            >
              <span className="material-symbols-outlined text-lg">arrow_back</span>
              Back to dashboard
            </Link>
            <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface">
              Manage Events
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant mt-xs">
              All events across every organizer, including drafts that aren&apos;t visible to
              volunteers yet.
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

        {isLoading && <p className="text-on-surface-variant font-body-md text-body-md">Loading events…</p>}
        {isError && (
          <p className="text-error font-body-md text-body-md">
            Could not load events. Admin access is required.
          </p>
        )}
        {events && events.length === 0 && (
          <p className="text-on-surface-variant font-body-md text-body-md">
            No events created yet.
          </p>
        )}

        <div className="grid gap-gutter">
          {events?.map((event) => (
            <EventRow key={event.id} event={event} />
          ))}
        </div>
      </div>
    </main>
  );
}
