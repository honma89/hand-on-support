"use client";

import { useState } from "react";
import { Trophy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { useLeaderboard } from "@/lib/hooks/use-rewards";

const scopes = [
  { value: "all_time", label: "All Time" },
  { value: "monthly", label: "This Month" },
  { value: "weekly", label: "This Week" },
] as const;

const medalColors = ["text-yellow-500", "text-gray-400", "text-amber-700"];

export default function LeaderboardPage() {
  const [scope, setScope] = useState<(typeof scopes)[number]["value"]>("all_time");
  const { data: entries, isLoading } = useLeaderboard(scope);

  return (
    <main className="container max-w-2xl py-8">
      <h1 className="mb-1 text-3xl font-bold">Leaderboard</h1>
      <p className="mb-6 text-muted-foreground">
        Top volunteers across Bhutan, ranked by Point Bank earnings.
      </p>

      <div className="mb-6 flex gap-2">
        {scopes.map((s) => (
          <Button
            key={s.value}
            variant={scope === s.value ? "default" : "outline"}
            size="sm"
            onClick={() => setScope(s.value)}
          >
            {s.label}
          </Button>
        ))}
      </div>

      {isLoading && <p className="text-muted-foreground">Loading rankings…</p>}

      <div className="space-y-2">
        {entries?.map((entry) => (
          <Card key={entry.user_id}>
            <CardContent className="flex items-center gap-4 py-3">
              <div className="flex w-8 items-center justify-center font-bold">
                {entry.rank <= 3 ? (
                  <Trophy className={cn("h-5 w-5", medalColors[entry.rank - 1])} />
                ) : (
                  <span className="text-muted-foreground">{entry.rank}</span>
                )}
              </div>
              <div className="flex-1">
                <p className="font-medium">{entry.full_name}</p>
                {entry.dzongkhag && (
                  <p className="text-xs text-muted-foreground">{entry.dzongkhag}</p>
                )}
              </div>
              <div className="font-bold text-primary">{entry.total_points} pts</div>
            </CardContent>
          </Card>
        ))}
        {entries && entries.length === 0 && (
          <p className="text-sm text-muted-foreground">No rankings yet for this period.</p>
        )}
      </div>
    </main>
  );
}
