import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { User, UserRole } from "@/lib/types";

export function useUsers(params?: { offset?: number; limit?: number }) {
  return useQuery({
    queryKey: ["admin", "users", params],
    queryFn: async () =>
      (
        await apiClient.get<User[]>("/users", {
          params: { offset: 0, limit: 200, ...params },
        })
      ).data,
  });
}

export interface AdminUserUpdateInput {
  role?: UserRole;
  is_active?: boolean;
}

export function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ userId, data }: { userId: string; data: AdminUserUpdateInput }) =>
      (await apiClient.put<User>(`/users/${userId}`, data)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
      queryClient.invalidateQueries({ queryKey: ["admin", "dashboard"] });
    },
  });
}
