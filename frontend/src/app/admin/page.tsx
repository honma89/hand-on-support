"use client";

import {
  Award,
  Calendar,
  CheckCircle2,
  ClipboardList,
  Trophy,
  Users,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAdminDashboard } from "@/lib/hooks/use-rewards";

const statCards = [
  { key: "total_users" as const, label: "Total Users", icon: Users },
  { key: "total_volunteers" as const, label: "Volunteers", icon: Users },
  { key: "total_events" as const, label: "Total Events", icon: Calendar },
  { key: "upcoming_events" as const, label: "Upcoming Events", icon: Calendar },
  { key: "total_registrations" as const, label: "Registrations", icon: ClipboardList },
  { key: "total_attendance_present" as const, label: "Attendance (Present)", icon: CheckCircle2 },
  { key: "total_points_awarded" as const, label: "Points Awarded", icon: Trophy },
  { key: "total_badges_awarded" as const, label: "Badges Awarded", icon: Award },
];

export default function AdminDashboardPage() {
  const { data: stats, isLoading, isError } = useAdminDashboard();

  return (
    <main className="container py-8">
      <h1 className="mb-6 text-3xl font-bold">Admin Dashboard</h1>

      {isLoading && <p className="text-muted-foreground">Loading stats…</p>}
      {isError && (
        <p className="text-destructive">
          Could not load dashboard stats. Admin access is required.
        </p>
      )}

      {stats && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {statCards.map(({ key, label, icon: Icon }) => (
            <Card key={key}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
                <Icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent className="text-2xl font-bold">{stats[key]}</CardContent>
            </Card>
          ))}
        </div>
      )}
    </main>
  );
}
