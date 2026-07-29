"use client";

import Link from "next/link";
import { Calendar, Trophy } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useMyRegistrations } from "@/lib/hooks/use-events";
import { useMyBadges, usePointBalance, usePointHistory } from "@/lib/hooks/use-rewards";

export default function DashboardPage() {
  const { data: user } = useCurrentUser();
  const { data: balance } = usePointBalance();
  const { data: history } = usePointHistory();
  const { data: badges } = useMyBadges();
  const { data: registrations } = useMyRegistrations();

  const upcoming = registrations?.filter(
    (r) => r.status !== "cancelled" && new Date(r.event.start_datetime) >= new Date(),
  );

  return (
    <main className="container py-8">
      <h1 className="mb-6 text-3xl font-bold">Welcome back{user ? `, ${user.full_name}` : ""}</h1>

      <div className="mb-8 grid gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Point Bank Balance
            </CardTitle>
          </CardHeader>
          <CardContent className="flex items-center gap-2 text-3xl font-bold text-primary">
            <Trophy className="h-7 w-7" />
            {balance?.balance ?? "—"}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">Badges Earned</CardTitle>
          </CardHeader>
          <CardContent className="text-3xl font-bold">{badges?.length ?? "—"}</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Upcoming Events
            </CardTitle>
          </CardHeader>
          <CardContent className="text-3xl font-bold">{upcoming?.length ?? "—"}</CardContent>
        </Card>
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <section>
          <h2 className="mb-3 text-xl font-semibold">Your Upcoming Events</h2>
          {upcoming && upcoming.length === 0 && (
            <p className="text-sm text-muted-foreground">
              No upcoming events yet.{" "}
              <Link href="/events" className="text-primary underline-offset-4 hover:underline">
                Browse opportunities
              </Link>
              .
            </p>
          )}
          <div className="space-y-3">
            {upcoming?.map((r) => (
              <Link key={r.id} href={`/events/${r.event_id}`}>
                <Card className="hover:shadow-md">
                  <CardContent className="flex items-center gap-3 pt-6">
                    <Calendar className="h-5 w-5 shrink-0 text-primary" />
                    <div>
                      <p className="font-medium">{r.event.title}</p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(r.event.start_datetime).toLocaleDateString()} ·{" "}
                        {r.status === "waitlisted" ? "Waitlisted" : "Registered"}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </section>

        <section>
          <h2 className="mb-3 text-xl font-semibold">Recent Point Activity</h2>
          <div className="space-y-2">
            {history?.slice(0, 8).map((t) => (
              <div
                key={t.id}
                className="flex items-center justify-between rounded-md border border-border px-4 py-2 text-sm"
              >
                <span>{t.description}</span>
                <span className={t.amount >= 0 ? "font-semibold text-primary" : "font-semibold text-destructive"}>
                  {t.amount >= 0 ? "+" : ""}
                  {t.amount}
                </span>
              </div>
            ))}
            {history && history.length === 0 && (
              <p className="text-sm text-muted-foreground">
                No point activity yet — attend an event to start earning.
              </p>
            )}
          </div>
        </section>
      </div>
    </main>
  );
}
