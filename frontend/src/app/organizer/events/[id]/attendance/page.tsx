"use client";

import { use, useState } from "react";
import Link from "next/link";
import { useEvent } from "@/lib/hooks/use-events";
import { useEventRegistrations, useMarkBulkAttendance } from "@/lib/hooks/use-events";
import { Button } from "@/components/ui/button";
import type { AttendanceStatus } from "@/lib/types";

export default function EventAttendancePage({ params }: { params: Promise<{ id: string }> }) {
  const { id: eventId } = use(params);
  const { data: event } = useEvent(eventId);
  const { data: registrations, isLoading, isError } = useEventRegistrations(eventId);
  const markAttendance = useMarkBulkAttendance(eventId);

  const [marks, setMarks] = useState<Record<string, AttendanceStatus>>({});

  const setMark = (userId: string, status: AttendanceStatus) =>
    setMarks((prev) => ({ ...prev, [userId]: status }));

  const handleSave = () => {
    const records = Object.entries(marks).map(([user_id, status]) => ({ user_id, status }));
    if (records.length === 0) return;
    markAttendance.mutate(records);
  };

  const registeredOnly = registrations?.filter((r) => r.status === "registered") ?? [];

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-3xl mx-auto">
        <Link
          href="/organizer"
          className="font-body-md text-sm text-primary hover:underline mb-md inline-flex items-center gap-xs"
        >
          <span className="material-symbols-outlined text-lg">arrow_back</span>
          My Events
        </Link>

        <h1 className="font-display-lg text-headline-lg text-on-surface mb-xs">
          {event?.title ?? "Mark Attendance"}
        </h1>
        <p className="font-body-md text-body-md text-on-surface-variant mb-lg">
          Mark who showed up. Present volunteers automatically receive this event&apos;s points.
        </p>

        {isLoading && (
          <p className="text-on-surface-variant font-body-md text-body-md">Loading registrants…</p>
        )}
        {isError && (
          <p className="text-error font-body-md text-body-md">
            Could not load registrants for this event. You may only manage events you organize.
          </p>
        )}
        {registrations && registeredOnly.length === 0 && (
          <p className="text-on-surface-variant font-body-md text-body-md">
            No registered volunteers for this event yet.
          </p>
        )}

        {registeredOnly.length > 0 && (
          <div className="glass-card rounded-xl p-md shadow-ambient overflow-x-auto mb-md">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-outline/30">
                  <th className="pb-sm font-label-md text-label-md text-on-surface-variant">
                    Volunteer
                  </th>
                  <th className="pb-sm font-label-md text-label-md text-on-surface-variant text-right">
                    Attendance
                  </th>
                </tr>
              </thead>
              <tbody>
                {registeredOnly.map((reg) => {
                  const current = marks[reg.user_id];
                  return (
                    <tr key={reg.id} className="border-b border-outline/20 last:border-0">
                      <td className="py-sm pr-md">
                        <p className="font-label-md text-label-md text-on-surface">
                          {reg.user.full_name}
                        </p>
                        <p className="font-body-md text-sm text-on-surface-variant">
                          {reg.user.email}
                        </p>
                      </td>
                      <td className="py-sm text-right">
                        <div className="inline-flex gap-xs">
                          <Button
                            type="button"
                            size="sm"
                            variant={current === "present" ? "default" : "outline"}
                            onClick={() => setMark(reg.user_id, "present")}
                          >
                            Present
                          </Button>
                          <Button
                            type="button"
                            size="sm"
                            variant={current === "absent" ? "destructive" : "outline"}
                            onClick={() => setMark(reg.user_id, "absent")}
                          >
                            Absent
                          </Button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {registeredOnly.length > 0 && (
          <div className="flex items-center gap-sm">
            <Button
              onClick={handleSave}
              disabled={Object.keys(marks).length === 0 || markAttendance.isPending}
            >
              {markAttendance.isPending ? "Saving…" : "Save Attendance"}
            </Button>
            {markAttendance.isSuccess && (
              <span className="font-body-md text-sm text-primary">Attendance saved.</span>
            )}
            {markAttendance.isError && (
              <span className="font-body-md text-sm text-error">
                Could not save attendance. Try again.
              </span>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
