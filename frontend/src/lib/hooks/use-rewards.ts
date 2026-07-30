import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type {
  Badge,
  DashboardStats,
  LeaderboardEntry,
  NotificationItem,
  PointBalance,
  PointTransaction,
  UserBadge,
} from "@/lib/types";

export function usePointBalance() {
  return useQuery({
    queryKey: ["points", "balance"],
    queryFn: async () => (await apiClient.get<PointBalance>("/points/me/balance")).data,
  });
}

export function usePointHistory() {
  return useQuery({
    queryKey: ["points", "history"],
    queryFn: async () =>
      (await apiClient.get<PointTransaction[]>("/points/me/history")).data,
  });
}

export function useLeaderboard(scope: "all_time" | "monthly" | "weekly" = "all_time") {
  return useQuery({
    queryKey: ["leaderboard", scope],
    queryFn: async () =>
      (await apiClient.get<LeaderboardEntry[]>("/leaderboard", { params: { scope } })).data,
  });
}

export function useAllBadges() {
  return useQuery({
    queryKey: ["badges", "all"],
    queryFn: async () => (await apiClient.get<Badge[]>("/badges")).data,
  });
}

export function useMyBadges() {
  return useQuery({
    queryKey: ["badges", "me"],
    queryFn: async () => (await apiClient.get<UserBadge[]>("/badges/me")).data,
  });
}

export function useMyNotifications() {
  return useQuery({
    queryKey: ["notifications"],
    queryFn: async () => (await apiClient.get<NotificationItem[]>("/notifications")).data,
    refetchInterval: 30_000,
  });
}

export function useUnreadNotificationCount() {
  return useQuery({
    queryKey: ["notifications", "unread-count"],
    queryFn: async () =>
      (await apiClient.get<{ unread_count: number }>("/notifications/unread-count")).data
        .unread_count,
    refetchInterval: 30_000,
  });
}

export function useAdminDashboard() {
  return useQuery({
    queryKey: ["admin", "dashboard"],
    queryFn: async () => (await apiClient.get<DashboardStats>("/admin/dashboard")).data,
  });
}
