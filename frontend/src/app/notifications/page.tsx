"use client";

import { useQueryClient } from "@tanstack/react-query";
import { Bell } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
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
    <main className="container max-w-2xl py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Notifications</h1>
        <Button variant="outline" size="sm" onClick={markAllRead}>
          Mark all read
        </Button>
      </div>

      {isLoading && <p className="text-muted-foreground">Loading notifications…</p>}

      <div className="space-y-2">
        {notifications?.map((n) => (
          <Card
            key={n.id}
            className={cn("cursor-pointer", !n.is_read && "border-primary/50 bg-primary/5")}
            onClick={() => !n.is_read && markRead(n.id)}
          >
            <CardContent className="flex items-start gap-3 py-4">
              <Bell className={cn("mt-0.5 h-4 w-4 shrink-0", n.is_read ? "text-muted-foreground" : "text-primary")} />
              <div className="flex-1">
                <p className="font-medium">{n.title}</p>
                <p className="text-sm text-muted-foreground">{n.message}</p>
                <p className="mt-1 text-xs text-muted-foreground">{timeAgo(n.created_at)}</p>
              </div>
            </CardContent>
          </Card>
        ))}
        {notifications && notifications.length === 0 && (
          <p className="text-sm text-muted-foreground">You&apos;re all caught up.</p>
        )}
      </div>
    </main>
  );
}
