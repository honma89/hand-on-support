export type UserRole = "volunteer" | "organizer" | "admin";

export interface User {
  id: string;
  email: string;
  full_name: string;
  phone_number: string | null;
  role: UserRole;
  is_active: boolean;
  dzongkhag: string | null;
  bio: string | null;
  avatar_url: string | null;
  skills: string | null;
  created_at: string;
}

export type EventStatus = "draft" | "published" | "cancelled" | "completed";

export interface EventPublic {
  id: string;
  title: string;
  description: string;
  category: string;
  dzongkhag: string;
  location_detail: string | null;
  start_datetime: string;
  end_datetime: string;
  capacity: number | null;
  points_reward: number;
  status: EventStatus;
  image_url: string | null;
  organizer_id: string;
  created_at: string;
}

export interface EventDetail extends EventPublic {
  registered_count: number;
  spots_remaining: number | null;
}

export type RegistrationStatus = "registered" | "waitlisted" | "cancelled";

export interface RegistrationWithEvent {
  id: string;
  event_id: string;
  user_id: string;
  status: RegistrationStatus;
  created_at: string;
  event: EventPublic;
}

export interface PointBalance {
  user_id: string;
  balance: number;
}

export interface PointTransaction {
  id: string;
  user_id: string;
  event_id: string | null;
  amount: number;
  type: "earned" | "redeemed" | "adjustment" | "bonus";
  description: string;
  created_at: string;
}

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  full_name: string;
  avatar_url: string | null;
  dzongkhag: string | null;
  total_points: number;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  criteria_type: "events_attended" | "points_earned";
  criteria_value: number;
}

export interface UserBadge {
  id: string;
  badge_id: string;
  awarded_at: string;
  badge: Badge;
}

export interface NotificationItem {
  id: string;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  related_entity_id: string | null;
  created_at: string;
}

export interface DashboardStats {
  total_users: number;
  total_volunteers: number;
  total_organizers: number;
  total_events: number;
  published_events: number;
  upcoming_events: number;
  total_registrations: number;
  total_attendance_present: number;
  total_points_awarded: number;
  total_badges_awarded: number;
}
