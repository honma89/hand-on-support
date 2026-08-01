"use client";

import Link from "next/link";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useCoordinationEvents, useUpdateEvent } from "@/lib/hooks/use-events";
import { EventStatusBadge } from "@/components/events/event-status-badge";
import { ConfirmDialog } from "@/components/common/confirm-dialog";
import { EmptyState } from "@/components/common/empty-state";
import { EventRowListSkeleton } from "@/components/common/loading-skeletons";
import { toast } from "@/lib/hooks/use-toast";
import type { EventPublic, EventStatus } from "@/lib/types";

// Organizers can publish/unpublish/cancel their own events, same as
// admins can on the Manage Events page -- the backend already allows
// this (an organizer manages any event where event.organizer_id ===
// their own id), this just surfaces the controls here too, using the
// same ConfirmDialog + toast pattern as the admin page for consistency.
function MyEventStatusControls({ event }: { event: EventPublic }) {
  const updateEvent = useUpdateEvent(event.id);

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
    <div className="flex flex-wrap items-center gap-xs">
      {/* Publishing a draft is non-destructive -- no confirmation needed. */}
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

      {/* Unpublish IS disruptive (hides it from volunteers) -- confirm. */}
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

      {/* Cancelling is the most destructive action -- confirm firmly. */}
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
    </div>
  );
}

export default function OrganizerDashboardPage() {
  const { data: user } = useCurrentUser();
  const { data: events, isLoading, isError } = useCoordinationEvents();

  const myEvents = events?.filter((e) => e.organizer_id === user?.id) ?? [];
  const otherPublished = events?.filter((e) => e.organizer_id !== user?.id) ?? [];

  return (
    <main className="min-h-screen bg-background px-margin-mobile py-xl md:px-margin-desktop">
      <div className="mx-auto max-w-5xl">
        <div className="mb-lg flex flex-wrap items-center justify-between gap-sm">
          <div>
            <h1 className="mb-xs font-display-lg text-headline-lg text-on-surface md:text-display-lg">
              Organizer Dashboard
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant">
              Manage your own events, and see what everyone else has published for coordination.
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

        {/* Loading: real skeleton UI instead of "Loading…" text. */}
        {isLoading && <EventRowListSkeleton />}

        {isError && (
          <EmptyState
            variant="error"
            title="Could not load your events"
            description="Something went wrong reaching the server. Check your connection and try again."
          />
        )}

        {!isLoading && !isError && (
          <>
            <section className="mb-xl">
              <h2 className="mb-sm font-headline-md text-headline-md text-on-surface">My Events</h2>

              {myEvents.length === 0 ? (
                <EmptyState
                  icon="event_note"
                  title="No events yet"
                  description="Create your first event to start coordinating volunteers across your dzongkhag."
                  action={
                    <Link
                      href="/organizer/events/new"
                      className="btn-primary inline-flex items-center gap-xs rounded-full px-md py-sm"
                    >
                      <span aria-hidden="true" className="material-symbols-outlined text-lg">
                        add_circle
                      </span>
                      Create Event
                    </Link>
                  }
                />
              ) : (
                <div className="grid gap-gutter">
                  {myEvents.map((event) => (
                    <div
                      key={event.id}
                      className="glass-card flex flex-wrap items-center justify-between gap-md rounded-xl p-md shadow-ambient shadow-ambient-hover transition-shadow"
                    >
                      <div>
                        <div className="mb-xs flex flex-wrap items-center gap-sm">
                          <p className="font-headline-md text-headline-md text-on-surface">
                            {event.title}
                          </p>
                          <EventStatusBadge status={event.status} />
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
                      <div className="flex shrink-0 flex-wrap items-center gap-xs">
                        <MyEventStatusControls event={event} />
                        <Link
                          href={`/organizer/events/${event.id}/attendance`}
                          className="btn-secondary inline-flex shrink-0 items-center gap-xs rounded-full px-md py-sm"
                        >
                          <span aria-hidden="true" className="material-symbols-outlined text-lg">
                            how_to_reg
                          </span>
                          Manage attendance
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section>
              <h2 className="mb-sm font-headline-md text-headline-md text-on-surface">
                Published by Other Organizers
              </h2>
              <p className="mb-sm font-body-md text-sm text-on-surface-variant">
                Read-only, for coordination -- you can&apos;t edit or manage these.
              </p>

              {otherPublished.length === 0 ? (
                <EmptyState
                  icon="groups"
                  title="Nothing published elsewhere"
                  description="When other organizers publish events, they'll show up here so you can coordinate."
                />
              ) : (
                <div className="grid gap-gutter">
                  {otherPublished.map((event) => (
                    <Link
                      key={event.id}
                      href={`/events/${event.id}`}
                      className="glass-card flex flex-wrap items-center justify-between gap-md rounded-xl p-md opacity-90 shadow-ambient"
                    >
                      <div>
                        <p className="font-headline-md text-headline-md text-on-surface">
                          {event.title}
                        </p>
                        <p className="font-body-md text-sm text-on-surface-variant">
                          {new Date(event.start_datetime).toLocaleString(undefined, {
                            dateStyle: "medium",
                            timeStyle: "short",
                          })}{" "}
                          · {event.dzongkhag}
                        </p>
                      </div>
                      <span
                        className="material-symbols-outlined text-on-surface-variant"
                        aria-hidden="true"
                      >
                        chevron_right
                      </span>
                    </Link>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </div>
    </main>
  );
}
