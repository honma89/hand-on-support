"use client";

import { use } from "react";
import { Calendar, MapPin, Trophy, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
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
    return <main className="container py-8 text-muted-foreground">Loading event…</main>;
  }

  if (!event) {
    return <main className="container py-8 text-destructive">Event not found.</main>;
  }

  const isFull = event.spots_remaining !== null && event.spots_remaining <= 0;

  return (
    <main className="container max-w-3xl py-8">
      <div className="mb-2 inline-flex rounded-full bg-secondary px-2 py-0.5 text-xs font-medium text-secondary-foreground">
        {event.category}
      </div>
      <h1 className="mb-4 text-3xl font-bold">{event.title}</h1>

      <div className="mb-6 grid gap-3 text-sm text-muted-foreground sm:grid-cols-2">
        <div className="flex items-center gap-2">
          <Calendar className="h-4 w-4 shrink-0" />
          {formatDateRange(event.start_datetime, event.end_datetime)}
        </div>
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 shrink-0" />
          {event.dzongkhag}
          {event.location_detail ? ` — ${event.location_detail}` : ""}
        </div>
        <div className="flex items-center gap-2 font-medium text-accent-foreground">
          <Trophy className="h-4 w-4 shrink-0" />
          {event.points_reward} points on completion
        </div>
        <div className="flex items-center gap-2">
          <Users className="h-4 w-4 shrink-0" />
          {event.capacity
            ? `${event.registered_count} / ${event.capacity} registered`
            : `${event.registered_count} registered`}
        </div>
      </div>

      <Card className="mb-6">
        <CardContent className="whitespace-pre-line pt-6 text-sm leading-relaxed">
          {event.description}
        </CardContent>
      </Card>

      {!user && (
        <p className="text-sm text-muted-foreground">Log in to register for this event.</p>
      )}

      {user && !myRegistration && (
        <Button
          size="lg"
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
        <div className="flex items-center gap-3">
          <span className="rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
            {myRegistration.status === "waitlisted" ? "You're on the waitlist" : "You're registered"}
          </span>
          <Button
            variant="outline"
            onClick={() => cancelMutation.mutate()}
            disabled={cancelMutation.isPending}
          >
            {cancelMutation.isPending ? "Cancelling…" : "Cancel registration"}
          </Button>
        </div>
      )}
    </main>
  );
}
