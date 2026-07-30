"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { useEvents } from "@/lib/hooks/use-events";

interface HealthResponse {
  status: string;
  app: string;
  env: string;
}

function formatEventDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "2-digit" });
}

export default function HomePage() {
  const { data } = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      // Health check lives at /api/health (outside the /v1 prefix),
      // so we call apiClient's underlying fetch directly instead of the
      // versioned apiClient instance.
      const res = await fetch("/api/health");
      if (!res.ok) throw new Error("API unreachable");
      return (await res.json()) as HealthResponse;
    },
  });
  const { data: events } = useEvents();
  const featured = events?.slice(0, 3) ?? [];

  return (
    <main className="min-h-screen bg-background text-foreground">
      <section className="relative overflow-hidden bg-surface py-20">
        <div className="absolute inset-x-0 top-0 h-2/3 bg-gradient-to-b from-primary-container/15 to-transparent" />
        <div className="container mx-auto grid gap-12 px-4 md:grid-cols-[minmax(420px,1fr)_minmax(420px,560px)] md:items-center">
          <div className="space-y-6 py-12">
            <div className="inline-flex items-center gap-2 rounded-full border border-primary-container/40 bg-primary-container/10 px-4 py-2 text-sm font-semibold text-primary">
              Community first
            </div>
            <h1 className="max-w-3xl text-5xl font-bold leading-tight text-on-surface md:text-6xl">
              Empowering Bhutanese youth to lead change.
            </h1>
            <p className="max-w-2xl text-lg leading-8 text-on-surface-variant">
              Join a grassroots movement dedicated to building a brighter future through action, unity, and compassion. Our volunteer platform connects changemakers with meaningful events while tracking impact through the Point Bank.
            </p>
            <div className="flex flex-col gap-4 sm:flex-row">
              <a href="/register" className="btn-primary inline-flex items-center justify-center px-8 py-3 shadow-ambient">
                Join Us
              </a>
              <a href="/events" className="btn-secondary inline-flex items-center justify-center px-8 py-3 rounded-full">
                View Campaigns
              </a>
            </div>
          </div>

          <div className="rounded-[32px] bg-white p-8 shadow-ambient">
            <div className="grid gap-4">
              <div className="rounded-3xl border border-outline-variant bg-surface p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-on-surface">Our Mission</h2>
                <p className="mt-3 text-base leading-7 text-on-surface-variant">
                  Fostering unity and compassion through grassroots initiatives that empower the next generation.
                </p>
              </div>

              <div className="rounded-3xl bg-surface p-6 shadow-ambient hover:shadow-ambient-hover transition-shadow">
                <span className="inline-flex rounded-full bg-primary-container/20 px-3 py-1 text-sm font-semibold text-primary">Action</span>
                <h3 className="mt-4 text-xl font-semibold text-on-surface">Environmental Stewardship</h3>
                <p className="mt-2 text-sm leading-7 text-on-surface-variant">
                  Leading local initiatives to preserve and protect our natural heritage for future generations.
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-3xl bg-primary-container p-6 text-on-primary-container shadow-ambient">
                  <h3 className="text-xl font-semibold">Unity</h3>
                  <p className="mt-2 text-sm leading-7 text-primary-fixed">Building strong, resilient community networks across regions.</p>
                </div>
                <div className="rounded-3xl bg-surface p-6 shadow-ambient">
                  <h3 className="text-xl font-semibold text-on-surface">Compassion</h3>
                  <p className="mt-2 text-sm leading-7 text-on-surface-variant">Providing hands-on support to those who need it most.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-background py-20">
        <div className="container mx-auto px-4">
          <div className="flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
            <div>
              <h2 className="text-3xl font-bold text-on-surface">Upcoming Events</h2>
              <p className="mt-3 max-w-xl text-base leading-7 text-on-surface-variant">
                Get involved in local campaigns and volunteer opportunities.
              </p>
            </div>
            <a href="/events" className="font-semibold text-primary transition hover:text-primary-fixed">
              View Full Calendar →
            </a>
          </div>

          {featured.length === 0 && (
            <p className="mt-10 text-on-surface-variant">
              No events scheduled yet — check back soon.
            </p>
          )}

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {featured.map((event) => (
              <a
                key={event.id}
                href={`/events/${event.id}`}
                className="group overflow-hidden rounded-[28px] bg-white shadow-ambient transition hover:shadow-ambient-hover"
              >
                <div className="h-52 bg-gradient-to-br from-primary-container/40 to-secondary-container/30" />
                <div className="p-6">
                  <div className="mb-4 inline-flex rounded-full bg-secondary-container/10 px-3 py-1 text-xs font-semibold text-secondary">
                    {event.category}
                  </div>
                  <h3 className="text-xl font-semibold text-on-surface">{event.title}</h3>
                  <p className="mt-3 text-sm leading-6 text-on-surface-variant">{event.dzongkhag}</p>
                  <span className="mt-5 inline-flex text-sm font-semibold text-primary">
                    {formatEventDate(event.start_datetime)}
                  </span>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
