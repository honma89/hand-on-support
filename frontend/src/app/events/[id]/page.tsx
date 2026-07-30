"use client";

import { use } from "react";
import { Button } from "@/components/ui/button";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import {
  useCancelRegistration,
  useEvent,
  useMyRegistrations,
  useRegisterForEvent,
} from "@/lib/hooks/use-events";

function formatDateRange(startIso: string, endIso: string) {
  const start = new Date(startIso);
  const end = new Date(endIso);
  const dateStr = start.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
  const timeStr = `${start.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" })} – ${end.toLocaleTimeString(
    "en-US",
    { hour: "numeric", minute: "2-digit" },
  )}`;
  return `${dateStr} · ${timeStr}`;
}

export default function EventDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { data: event, isLoading } = useEvent(id);
  const { data: user } = useCurrentUser();
  const { data: myRegistrations } = useMyRegistrations();
  const registerMutation = useRegisterForEvent(id);
  const cancelMutation = useCancelRegistration(id);

  const myRegistration = myRegistrations?.find((r) => r.event_id === id && r.status !== "cancelled");

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
        <p className="text-on-surface-variant font-body-md text-body-md">Loading event…</p>
      </main>
    );
  }

  if (!event) {
    return (
      <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
        <p className="text-error font-body-md text-body-md">Event not found.</p>
      </main>
    );
  }

  const isFull = event.spots_remaining !== null && event.spots_remaining <= 0;

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-3xl mx-auto">
        <span className="inline-flex bg-secondary-container/10 text-secondary px-sm py-xs rounded-full font-label-md text-label-md mb-sm">
          {event.category}
        </span>
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-md">
          {event.title}
        </h1>

        <div className="grid gap-sm sm:grid-cols-2 mb-lg font-body-md text-body-md text-on-surface-variant">
          <div className="flex items-center gap-xs">
            <span className="material-symbols-outlined text-lg">calendar_month</span>
            {formatDateRange(event.start_datetime, event.end_datetime)}
          </div>
          <div className="flex items-center gap-xs">
            <span className="material-symbols-outlined text-lg">location_on</span>
            {event.dzongkhag}
            {event.location_detail ? ` — ${event.location_detail}` : ""}
          </div>
          <div className="flex items-center gap-xs text-primary font-label-md text-label-md">
            <span className="material-symbols-outlined text-lg">stars</span>
            {event.points_reward} points on completion
          </div>
          <div className="flex items-center gap-xs">
            <span className="material-symbols-outlined text-lg">group</span>
            {event.capacity
              ? `${event.registered_count} / ${event.capacity} registered`
              : `${event.registered_count} registered`}
          </div>
        </div>

        <div className="glass-card rounded-xl p-md mb-lg">
          <p className="font-body-md text-body-md text-on-surface-variant whitespace-pre-line leading-relaxed">
            {event.description}
          </p>
        </div>

        {!user && (
          <p className="font-body-md text-body-md text-on-surface-variant">
            Log in to register for this event.
          </p>
        )}

        {user && !myRegistration && (
          <Button
            size="lg"
            className="rounded-full"
            onClick={() => registerMutation.mutate()}
            disabled={registerMutation.isPending}
          >
            {registerMutation.isPending
              ? "Registering…"
              : isFull
                ? "Join waitlist"
                : "Register for this event"}
          </Button>
        )}

        {user && myRegistration && (
          <div className="flex items-center gap-sm">
            <span className="rounded-full bg-primary-container/20 px-sm py-xs font-label-md text-label-md text-primary">
              {myRegistration.status === "waitlisted" ? "You're on the waitlist" : "You're registered"}
            </span>
            <Button
              variant="outline"
              className="rounded-full"
              onClick={() => cancelMutation.mutate()}
              disabled={cancelMutation.isPending}
            >
              {cancelMutation.isPending ? "Cancelling…" : "Cancel registration"}
            </Button>
          </div>
        )}
      </div>
    </main>
  );
}
