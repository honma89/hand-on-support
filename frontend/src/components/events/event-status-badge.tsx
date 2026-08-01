import { cn } from "@/lib/utils";
import type { EventStatus } from "@/lib/types";

/**
 * Single source of truth for how each event status looks.
 *
 * Previously this map was duplicated inline in the admin and organizer
 * pages; centralising it here keeps every status pill consistent and
 * uses only design-system tokens (no raw hex).
 */
const STATUS_CONFIG: Record<EventStatus, { label: string; className: string; icon: string }> = {
  draft: {
    label: "Draft",
    icon: "edit_note",
    className: "bg-outline-variant/40 text-on-surface-variant",
  },
  published: {
    label: "Published",
    icon: "public",
    className: "bg-primary-container text-on-primary-container",
  },
  cancelled: {
    label: "Cancelled",
    icon: "cancel",
    className: "bg-error/10 text-error",
  },
  completed: {
    label: "Completed",
    icon: "task_alt",
    className: "bg-secondary-container text-secondary-foreground",
  },
};

export interface EventStatusBadgeProps {
  status: EventStatus;
  /** Hide the leading icon (e.g. in very tight rows). Defaults to false. */
  hideIcon?: boolean;
  /** Render on a translucent surface, e.g. floating over a card image. */
  onImage?: boolean;
  className?: string;
}

/**
 * A small, accessible status pill. Uses `aria-label` so screen readers
 * announce the status explicitly (the visual text is already clear, but
 * this keeps intent obvious when composed inside other controls).
 */
export function EventStatusBadge({
  status,
  hideIcon = false,
  onImage = false,
  className,
}: EventStatusBadgeProps) {
  const config = STATUS_CONFIG[status];

  return (
    <span
      aria-label={`Status: ${config.label}`}
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-3 py-1 font-label-md text-label-md capitalize",
        config.className,
        // When floating over an image, add a subtle backdrop so the pill
        // stays legible regardless of the photo behind it.
        onImage && "shadow-ambient backdrop-blur-sm",
        className,
      )}
    >
      {!hideIcon && (
        <span aria-hidden="true" className="material-symbols-outlined text-base leading-none">
          {config.icon}
        </span>
      )}
      {config.label}
    </span>
  );
}
