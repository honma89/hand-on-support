"use client";

import { useState } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { getCategoryTheme } from "@/lib/constants/bhutan";
import { EventStatusBadge } from "@/components/events/event-status-badge";
import type { EventPublic } from "@/lib/types";

function formatDateChip(iso: string) {
  const d = new Date(iso);
  return {
    month: d.toLocaleDateString("en-US", { month: "short" }).toUpperCase(),
    day: d.toLocaleDateString("en-US", { day: "2-digit" }),
  };
}

/**
 * The media/header area of an event card.
 *
 * Priority:
 *   1. Show the organizer's real `image_url` when present *and* it loads.
 *   2. If there's no URL — or it fails to load — fall back to a
 *      category-themed gradient with the category icon.
 *
 * The fallback is derived from the event category so the wall of cards
 * still reads as varied and intentional rather than "broken image".
 */
function EventCardMedia({ event, showStatus }: { event: EventPublic; showStatus: boolean }) {
  // Track load failures so a dead URL degrades to the gradient instead
  // of showing a broken-image glyph.
  const [imageFailed, setImageFailed] = useState(false);
  const theme = getCategoryTheme(event.category);
  const { month, day } = formatDateChip(event.start_datetime);
  const hasImage = Boolean(event.image_url) && !imageFailed;

  return (
    <div className="relative h-44 w-full overflow-hidden">
      {hasImage ? (
        <>
          {/* Real photo. crossOrigin kept anonymous in case the card is
              ever painted to a canvas (share images, etc.). */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={event.image_url as string}
            alt={`${event.title} event photo`}
            loading="lazy"
            crossOrigin="anonymous"
            onError={() => setImageFailed(true)}
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
          {/* Subtle scrim keeps the floating chips legible over any photo. */}
          <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-black/25 via-transparent to-transparent" />
        </>
      ) : (
        <div
          className={cn(
            "flex h-full w-full items-center justify-center",
            theme.gradient,
          )}
        >
          <span
            aria-hidden="true"
            className={cn("material-symbols-outlined text-6xl opacity-90", theme.onGradient)}
          >
            {theme.icon}
          </span>
        </div>
      )}

      {/* Status pill — top-left. */}
      {showStatus && (
        <div className="absolute left-sm top-sm">
          <EventStatusBadge status={event.status} onImage={hasImage} />
        </div>
      )}

      {/* Date chip — top-right, mirrors the original design. */}
      <div className="absolute right-sm top-sm flex flex-col items-center rounded-md bg-surface px-sm py-xs shadow-ambient">
        <span className="font-label-md text-label-md text-secondary">{month}</span>
        <span className="font-headline-md text-headline-md leading-none text-on-surface">{day}</span>
      </div>
    </div>
  );
}

export interface EventCardProps {
  event: EventPublic;
  /**
   * Show the status pill over the media. Defaults to true so admin /
   * organizer surfaces get status at a glance; a purely public list can
   * pass `false` if every event is already known to be published.
   */
  showStatus?: boolean;
  /** Override the destination; defaults to the public event detail page. */
  href?: string;
  className?: string;
}

/**
 * The canonical event card. Composable and link-wrapped:
 *
 *   {events.map((e) => <EventCard key={e.id} event={e} />)}
 *
 * `group` on the root enables the image zoom-on-hover in EventCardMedia.
 */
export function EventCard({ event, showStatus = true, href, className }: EventCardProps) {
  const theme = getCategoryTheme(event.category);

  return (
    <Link
      href={href ?? `/events/${event.id}`}
      className={cn(
        "group flex h-full flex-col overflow-hidden rounded-xl bg-surface shadow-ambient shadow-ambient-hover transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
        className,
      )}
    >
      <EventCardMedia event={event} showStatus={showStatus} />

      <div className="flex flex-grow flex-col gap-sm p-md">
        {/* Category tag, themed to match the fallback gradient family. */}
        <span className="inline-flex w-fit items-center gap-1 rounded-full bg-secondary-container/10 px-sm py-xs font-label-md text-label-md text-secondary">
          <span aria-hidden="true" className="material-symbols-outlined text-base leading-none">
            {theme.icon}
          </span>
          {event.category}
        </span>

        <h3 className="line-clamp-2 font-headline-md text-headline-md text-on-surface text-pretty">
          {event.title}
        </h3>

        <div className="mt-auto flex items-center gap-xs pt-sm font-body-md text-body-md text-on-surface-variant">
          <span aria-hidden="true" className="material-symbols-outlined text-lg">
            location_on
          </span>
          <span className="truncate">{event.dzongkhag}</span>
        </div>

        <div className="flex items-center gap-xs font-label-md text-label-md text-primary">
          <span aria-hidden="true" className="material-symbols-outlined text-lg">
            stars
          </span>
          {event.points_reward} points
        </div>
      </div>
    </Link>
  );
}
