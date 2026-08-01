"use client";

import Link from "next/link";
import { useAllEventsAdmin, useUpdateEvent } from "@/lib/hooks/use-events";
import { EventStatusBadge } from "@/components/events/event-status-badge";
import { ConfirmDialog } from "@/components/common/confirm-dialog";
import { EmptyState } from "@/components/common/empty-state";
import { EventRowListSkeleton } from "@/components/common/loading-skeletons";
import { toast } from "@/lib/hooks/use-toast";
import type { EventPublic, EventStatus } from "@/lib/types";

function EventRow({ event }: { event: EventPublic }) {
  const updateEvent = useUpdateEvent(event.id);

  // Central status mutation. Errors now surface as a toast (consistent
  // everywhere) instead of ad-hoc inline text; success is confirmed too.
  const setStatus = async (status: EventStatus, successMsg: string) => {
    try {
      await updateEvent.mutateAsync({ status });
      toast.success(successMsg, event.title);
    } catch (err) {
      toast.error(err, "Could not update the event.");
      throw err; // rethrow so ConfirmDialog keeps its dialog open
    }
  };

  return (
    <div className="glass-card flex flex-wrap items-center justify-between gap-md rounded-xl p-md shadow-ambient">
      <div>
        <div className="mb-xs flex flex-wrap items-center gap-sm">
          <p className="font-headline-md text-headline-md text-on-surface">{event.title}</p>
          <EventStatusBadge status={event.status} />
        </div>
        <p className="font-body-md text-sm text-on-surface-variant">
          {new Date(event.start_datetime).toLocaleString(undefined, {
            dateStyle: "medium",
            timeStyle: "short",
          })}{" "}
          · {event.dzongkhag} · {event.category}
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-xs">
        {/* Publishing a draft is non-destructive — no confirmation needed. */}
        {event.status === "draft" && (
          <button
            onClick={() => void setStatus("published", "Event published")}
            disabled={updateEvent.isPending}
            className="btn-primary inline-flex items-center gap-xs rounded-full px-md py-sm text-sm"
          >
            <span aria-hidden="true" className="material-symbols-outlined text-lg">
              publish
            </span>
            Publish
          </button>
        )}

        {/* Unpublish IS disruptive (hides it from volunteers) — confirm. */}
        {event.status === "published" && (
          <ConfirmDialog
            title="Unpublish this event?"
            description="It will be hidden from volunteers and move back to draft. Anyone already registered keeps their spot, but new sign-ups will pause until you publish again."
            confirmLabel="Unpublish"
            cancelLabel="Keep published"
            icon="unpublished"
            onConfirm={() => setStatus("draft", "Event unpublished")}
            trigger={
              <button
                disabled={updateEvent.isPending}
                className="btn-secondary inline-flex items-center gap-xs rounded-full px-md py-sm text-sm"
              >
                <span aria-hidden="true" className="material-symbols-outlined text-lg">
                  unpublished
                </span>
                Unpublish
              </button>
            }
          />
        )}

        {/* Cancelling is the most destructive action — confirm firmly. */}
        {(event.status === "draft" || event.status === "published") && (
          <ConfirmDialog
            title="Cancel this event?"
            description="Registered volunteers will be notified and the event will be marked cancelled. This can't be undone."
            confirmLabel="Yes, cancel event"
            cancelLabel="Keep event"
            icon="cancel"
            onConfirm={() => setStatus("cancelled", "Event cancelled")}
            trigger={
              <button
                disabled={updateEvent.isPending}
                className="inline-flex items-center gap-xs rounded-full px-md py-sm text-sm text-error transition-colors hover:bg-error/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              >
                <span aria-hidden="true" className="material-symbols-outlined text-lg">
                  cancel
                </span>
                Cancel
              </button>
            }
          />
        )}

        <Link
          href={`/organizer/events/${event.id}/attendance`}
          className="inline-flex items-center gap-xs rounded-full px-md py-sm text-sm text-on-surface-variant transition-colors hover:bg-surface-container"
        >
          <span aria-hidden="true" className="material-symbols-outlined text-lg">
            how_to_reg
          </span>
          Attendance
        </Link>
        <Link
          href={`/events/${event.id}`}
          className="inline-flex items-center gap-xs rounded-full px-md py-sm text-sm text-on-surface-variant transition-colors hover:bg-surface-container"
        >
          <span aria-hidden="true" className="material-symbols-outlined text-lg">
            visibility
          </span>
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
      <div className="mx-auto max-w-5xl">
        <div className="mb-lg flex flex-wrap items-center justify-between gap-sm">
          <div>
            <Link
              href="/admin"
              className="mb-xs inline-flex items-center gap-xs font-label-md text-label-md text-on-surface-variant hover:text-primary"
            >
              <span aria-hidden="true" className="material-symbols-outlined text-lg">
                arrow_back
              </span>
              Back to dashboard
            </Link>
            <h1 className="font-display-lg text-headline-lg text-on-surface md:text-display-lg">
              Manage Events
            </h1>
            <p className="mt-xs font-body-md text-body-md text-on-surface-variant">
              All events across every organizer, including drafts that aren&apos;t visible to
              volunteers yet.
            </p>
          </div>
          <Link
            href="/organizer/events/new"
            className="btn-primary inline-flex items-center gap-xs rounded-full px-md py-sm"
          >
            <span aria-hidden="true" className="material-symbols-outlined text-lg">
              add_circle
            </span>
            Create Event
          </Link>
        </div>

        {isLoading && <EventRowListSkeleton />}

        {isError && (
          <EmptyState
            variant="error"
            title="Couldn't load events"
            description="Admin access is required, or the server is unreachable. Try refreshing the page."
          />
        )}

        {events && events.length === 0 && !isLoading && (
          <EmptyState
            icon="event_note"
            title="No events created yet"
            description="Once you or another organizer creates an event, it'll show up here for management."
            action={
              <Link
                href="/organizer/events/new"
                className="btn-primary inline-flex items-center gap-xs rounded-full px-md py-sm"
              >
                <span aria-hidden="true" className="material-symbols-outlined text-lg">
                  add_circle
                </span>
                Create the first event
              </Link>
            }
          />
        )}

        {events && events.length > 0 && (
          <div className="grid gap-gutter">
            {events.map((event) => (
              <EventRow key={event.id} event={event} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
