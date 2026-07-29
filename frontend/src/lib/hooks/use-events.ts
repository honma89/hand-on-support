import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { EventDetail, EventPublic, RegistrationWithEvent } from "@/lib/types";

export function useEvents(params?: { category?: string; dzongkhag?: string }) {
  return useQuery({
    queryKey: ["events", params],
    queryFn: async () =>
      (
        await apiClient.get<EventPublic[]>("/events", {
          params: { status: "published", upcoming_only: true, ...params },
        })
      ).data,
  });
}

export function useEvent(eventId: string) {
  return useQuery({
    queryKey: ["events", eventId],
    queryFn: async () => (await apiClient.get<EventDetail>(`/events/${eventId}`)).data,
    enabled: !!eventId,
  });
}

export function useMyRegistrations() {
  return useQuery({
    queryKey: ["registrations", "me"],
    queryFn: async () =>
      (await apiClient.get<RegistrationWithEvent[]>("/registrations/me")).data,
  });
}

export function useRegisterForEvent(eventId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => apiClient.post(`/events/${eventId}/register`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["events", eventId] });
      queryClient.invalidateQueries({ queryKey: ["registrations", "me"] });
    },
  });
}

export function useCancelRegistration(eventId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => apiClient.delete(`/events/${eventId}/register`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["events", eventId] });
      queryClient.invalidateQueries({ queryKey: ["registrations", "me"] });
    },
  });
}
