import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";
import type { User } from "@/lib/types";

interface AuthResponse {
  access_token: string;
  user: User;
}

export function useCurrentUser() {
  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: async () => (await apiClient.get<User>("/auth/me")).data,
    retry: false,
  });
}

export function useLogin() {
  const queryClient = useQueryClient();
  const router = useRouter();
  return useMutation({
    mutationFn: async (data: { email: string; password: string }) =>
      (await apiClient.post<AuthResponse>("/auth/login", data)).data,
    onSuccess: (data) => {
      queryClient.setQueryData(["auth", "me"], data.user);
      router.push("/dashboard");
    },
  });
}

export function useRegister() {
  const queryClient = useQueryClient();
  const router = useRouter();
  return useMutation({
    mutationFn: async (data: {
      email: string;
      password: string;
      full_name: string;
      phone_number?: string;
    }) => (await apiClient.post<AuthResponse>("/auth/register", data)).data,
    onSuccess: (data) => {
      queryClient.setQueryData(["auth", "me"], data.user);
      router.push("/dashboard");
    },
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  const router = useRouter();
  return useMutation({
    mutationFn: async () => apiClient.post("/auth/logout"),
    onSuccess: () => {
      queryClient.setQueryData(["auth", "me"], null);
      queryClient.clear();
      router.push("/login");
    },
  });
}
