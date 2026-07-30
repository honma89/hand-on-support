"use client";

import { useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/lib/api-client";
import { cn } from "@/lib/utils";
import { useMyNotifications } from "@/lib/hooks/use-rewards";

function timeAgo(iso: string) {
  const diffMs = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export default function NotificationsPage() {
  const { data: notifications, isLoading } = useMyNotifications();
  const queryClient = useQueryClient();

  const markAllRead = async () => {
    await apiClient.post("/notifications/read-all");
    queryClient.invalidateQueries({ queryKey: ["notifications"] });
  };

  const markRead = async (id: string) => {
    await apiClient.post(`/notifications/${id}/read`);
    queryClient.invalidateQueries({ queryKey: ["notifications"] });
  };

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-lg">
          <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface">
            Notifications
          </h1>
          <Button variant="outline" size="sm" className="rounded-full" onClick={markAllRead}>
            Mark all read
          </Button>
        </div>

        {isLoading && <p className="text-on-surface-variant font-body-md text-body-md">Loading notifications…</p>}

        <div className="space-y-sm">
          {notifications?.map((n) => (
            <div
              key={n.id}
              className={cn(
                "glass-card rounded-xl p-md cursor-pointer flex items-start gap-sm shadow-ambient",
                !n.is_read && "border-l-4 border-primary-container",
              )}
              onClick={() => !n.is_read && markRead(n.id)}
            >
              <span
                className={cn(
                  "material-symbols-outlined mt-0.5",
                  n.is_read ? "text-on-surface-variant" : "text-primary",
                )}
              >
                notifications
              </span>
              <div className="flex-1">
                <p className="font-label-md text-label-md text-on-surface">{n.title}</p>
                <p className="font-body-md text-body-md text-on-surface-variant">{n.message}</p>
                <p className="font-body-md text-xs text-on-surface-variant mt-xs">{timeAgo(n.created_at)}</p>
              </div>
            </div>
          ))}
          {notifications && notifications.length === 0 && (
            <p className="font-body-md text-body-md text-on-surface-variant">You&apos;re all caught up.</p>
          )}
        </div>
      </div>
    </main>
  );
}
