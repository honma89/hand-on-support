import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type {
  AttendanceStatus,
  EventDetail,
  EventPublic,
  EventStatus,
  RegistrationWithEvent,
  RegistrationWithUser,
} from "@/lib/types";

export interface EventCreateInput {
  title: string;
  description: string;
  category: string;
  dzongkhag: string;
  location_detail?: string;
  start_datetime: string;
  end_datetime: string;
  capacity?: number;
  points_reward: number;
  status: EventStatus;
  image_url?: string;
  location_id?: string;
}


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

export function useCreateEvent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: EventCreateInput) =>
      (await apiClient.post<EventPublic>("/events", data)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["events"] });
      queryClient.invalidateQueries({ queryKey: ["admin", "dashboard"] });
    },
  });
}

export function useUpdateEvent(eventId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<EventCreateInput>) =>
      (await apiClient.patch<EventPublic>(`/events/${eventId}`, data)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["events"] });
      queryClient.invalidateQueries({ queryKey: ["admin", "dashboard"] });
    },
  });
}

export function useAllEventsAdmin() {
  return useQuery({
    queryKey: ["events", "admin", "all"],
    queryFn: async () =>
      (
        await apiClient.get<EventPublic[]>("/events", {
          params: { limit: 100 },
        })
      ).data,
  });
}

export function useOrganizerEvents(organizerId: string | undefined) {
  return useQuery({
    queryKey: ["events", "organizer", organizerId],
    queryFn: async () =>
      (
        await apiClient.get<EventPublic[]>("/events", {
          params: { organizer_id: organizerId, limit: 100 },
        })
      ).data,
    enabled: !!organizerId,
  });
}

export function useEventRegistrations(eventId: string) {
  return useQuery({
    queryKey: ["events", eventId, "registrations"],
    queryFn: async () =>
      (await apiClient.get<RegistrationWithUser[]>(`/events/${eventId}/registrations`)).data,
    enabled: !!eventId,
  });
}

export function useMarkBulkAttendance(eventId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (records: { user_id: string; status: AttendanceStatus }[]) =>
      (
        await apiClient.post(`/events/${eventId}/attendance/bulk`, { records })
      ).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["events", eventId] });
      queryClient.invalidateQueries({ queryKey: ["admin", "dashboard"] });
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
