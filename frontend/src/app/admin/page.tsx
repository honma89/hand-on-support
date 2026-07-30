"use client";

import { useAdminDashboard } from "@/lib/hooks/use-rewards";

const statCards = [
  { key: "total_users" as const, label: "Total Users", icon: "group" },
  { key: "total_volunteers" as const, label: "Volunteers", icon: "volunteer_activism" },
  { key: "total_events" as const, label: "Total Events", icon: "event" },
  { key: "upcoming_events" as const, label: "Upcoming Events", icon: "upcoming" },
  { key: "total_registrations" as const, label: "Registrations", icon: "how_to_reg" },
  { key: "total_attendance_present" as const, label: "Attendance (Present)", icon: "task_alt" },
  { key: "total_points_awarded" as const, label: "Points Awarded", icon: "stars" },
  { key: "total_badges_awarded" as const, label: "Badges Awarded", icon: "military_tech" },
];

export default function AdminDashboardPage() {
  const { data: stats, isLoading, isError } = useAdminDashboard();

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-7xl mx-auto">
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-lg">
          Admin Dashboard
        </h1>

        {isLoading && <p className="text-on-surface-variant font-body-md text-body-md">Loading stats…</p>}
        {isError && (
          <p className="text-error font-body-md text-body-md">
            Could not load dashboard stats. Admin access is required.
          </p>
        )}

        {stats && (
          <div className="grid gap-gutter sm:grid-cols-2 lg:grid-cols-4">
            {statCards.map(({ key, label, icon }) => (
              <div key={key} className="glass-card rounded-xl p-md shadow-ambient shadow-ambient-hover transition-shadow">
                <div className="flex items-center justify-between mb-sm">
                  <p className="font-label-md text-label-md text-on-surface-variant">{label}</p>
                  <span className="material-symbols-outlined text-on-surface-variant text-xl">{icon}</span>
                </div>
                <p className="font-headline-lg text-headline-lg text-on-surface">{stats[key]}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
