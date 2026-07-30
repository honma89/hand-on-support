"use client";

import Link from "next/link";
import { Calendar, MapPin, Trophy } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useEvents } from "@/lib/hooks/use-events";

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export default function EventsPage() {
  const { data: events, isLoading, isError } = useEvents();

  return (
    <main className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Upcoming Opportunities</h1>
        <p className="text-muted-foreground">
          Find a community service event near you and start earning Point Bank rewards.
        </p>
      </div>

      {isLoading && <p className="text-muted-foreground">Loading events…</p>}
      {isError && <p className="text-destructive">Could not load events. Please try again.</p>}

      {events && events.length === 0 && (
        <p className="text-muted-foreground">No upcoming events right now — check back soon.</p>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {events?.map((event) => (
          <Link key={event.id} href={`/events/${event.id}`}>
            <Card className="h-full transition-shadow hover:shadow-md">
              <CardHeader>
                <div className="mb-1 inline-flex w-fit rounded-full bg-secondary px-2 py-0.5 text-xs font-medium text-secondary-foreground">
                  {event.category}
                </div>
                <CardTitle className="line-clamp-2">{event.title}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 shrink-0" />
                  {formatDate(event.start_datetime)}
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 shrink-0" />
                  {event.dzongkhag}
                </div>
                <div className="flex items-center gap-2 font-medium text-accent-foreground">
                  <Trophy className="h-4 w-4 shrink-0" />
                  {event.points_reward} points
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </main>
  );
}
