"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useLeaderboard } from "@/lib/hooks/use-rewards";

const scopes = [
  { value: "all_time", label: "All Time" },
  { value: "monthly", label: "This Month" },
  { value: "weekly", label: "This Week" },
] as const;

const medalColors = ["text-primary-fixed-dim", "text-outline", "text-secondary"];

export default function LeaderboardPage() {
  const [scope, setScope] = useState<(typeof scopes)[number]["value"]>("all_time");
  const { data: entries, isLoading } = useLeaderboard(scope);

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-2xl mx-auto">
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-xs">
          Leaderboard
        </h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant mb-lg">
          Top volunteers across Bhutan, ranked by Point Bank earnings.
        </p>

        <div className="flex gap-sm mb-lg">
          {scopes.map((s) => (
            <Button
              key={s.value}
              variant={scope === s.value ? "default" : "outline"}
              size="sm"
              className="rounded-full"
              onClick={() => setScope(s.value)}
            >
              {s.label}
            </Button>
          ))}
        </div>

        {isLoading && <p className="text-on-surface-variant font-body-md text-body-md">Loading rankings…</p>}

        <div className="space-y-sm">
          {entries?.map((entry) => (
            <div
              key={entry.user_id}
              className="glass-card rounded-xl flex items-center gap-md p-sm shadow-ambient"
            >
              <div className="flex w-8 items-center justify-center font-headline-md text-headline-md">
                {entry.rank <= 3 ? (
                  <span className={cn("material-symbols-outlined text-2xl", medalColors[entry.rank - 1])}>
                    workspace_premium
                  </span>
                ) : (
                  <span className="text-on-surface-variant text-lg">{entry.rank}</span>
                )}
              </div>
              <div className="flex-1">
                <p className="font-label-md text-label-md text-on-surface">{entry.full_name}</p>
                {entry.dzongkhag && (
                  <p className="font-body-md text-xs text-on-surface-variant">{entry.dzongkhag}</p>
                )}
              </div>
              <div className="font-headline-md text-headline-md text-primary">{entry.total_points} pts</div>
            </div>
          ))}
          {entries && entries.length === 0 && (
            <p className="font-body-md text-body-md text-on-surface-variant">
              No rankings yet for this period.
            </p>
          )}
        </div>
      </div>
    </main>
  );
}
