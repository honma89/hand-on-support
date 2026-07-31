"use client";

import Link from "next/link";
import { useAllBadges } from "@/lib/hooks/use-rewards";

const criteriaLabel: Record<string, (value: number) => string> = {
  events_attended: (v) => `Attend ${v} event${v === 1 ? "" : "s"}`,
  points_earned: (v) => `Earn ${v} lifetime points`,
};

export default function AdminBadgesPage() {
  const { data: badges, isLoading, isError } = useAllBadges();

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-lg flex-wrap gap-sm">
          <div>
            <Link
              href="/admin"
              className="inline-flex items-center gap-xs font-label-md text-label-md text-on-surface-variant hover:text-primary mb-xs"
            >
              <span className="material-symbols-outlined text-lg">arrow_back</span>
              Back to dashboard
            </Link>
            <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface">
              Manage Badges
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant mt-xs">
              Badge templates volunteers automatically earn when they meet the criteria.
            </p>
          </div>
          <Link
            href="/admin/badges/new"
            className="btn-primary rounded-full px-md py-sm inline-flex items-center gap-xs"
          >
            <span className="material-symbols-outlined text-lg">add_circle</span>
            Create Badge
          </Link>
        </div>

        {isLoading && <p className="text-on-surface-variant font-body-md text-body-md">Loading badges…</p>}
        {isError && (
          <p className="text-error font-body-md text-body-md">Could not load badges.</p>
        )}
        {badges && badges.length === 0 && (
          <p className="text-on-surface-variant font-body-md text-body-md">
            No badges created yet — badges are how volunteers get automatically rewarded for
            milestones like attending events or earning points.
          </p>
        )}

        <div className="grid gap-gutter sm:grid-cols-2">
          {badges?.map((badge) => (
            <div key={badge.id} className="glass-card rounded-xl p-md shadow-ambient flex items-start gap-sm">
              <div className="w-14 h-14 rounded-full bg-primary-container flex items-center justify-center text-2xl shrink-0">
                {badge.icon}
              </div>
              <div>
                <p className="font-headline-md text-headline-md text-on-surface">{badge.name}</p>
                <p className="font-body-md text-sm text-on-surface-variant mt-xs">
                  {badge.description}
                </p>
                <p className="font-label-md text-label-md text-primary mt-sm">
                  {criteriaLabel[badge.criteria_type]?.(badge.criteria_value) ??
                    `${badge.criteria_type}: ${badge.criteria_value}`}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
