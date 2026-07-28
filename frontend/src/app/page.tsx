"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";

interface HealthResponse {
  status: string;
  app: string;
  env: string;
}

export default function HomePage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      // Health check lives at /api/health (outside the /v1 prefix),
      // so we call axios directly instead of the apiClient instance.
      const res = await fetch("/api/health");
      if (!res.ok) throw new Error("API unreachable");
      return (await res.json()) as HealthResponse;
    },
  });

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center">
      <h1 className="text-3xl font-bold text-primary">Hand On Support</h1>
      <p className="text-muted-foreground max-w-md">
        Volunteer management &amp; the Point Bank rewards system for
        Bhutan&apos;s community service network.
      </p>

      <div className="rounded-lg border border-border bg-card px-4 py-3 text-sm">
        {isLoading && <span>Checking API connection…</span>}
        {isError && (
          <span className="text-destructive">
            Could not reach the backend API.
          </span>
        )}
        {data && (
          <span className="text-primary">
            ✓ Connected to {data.app} ({data.env})
          </span>
        )}
      </div>
    </main>
  );
}
