import { cn } from "@/lib/utils";

/**
 * Low-level shimmer block. Everything else (card skeletons, row
 * skeletons) is composed from this. Uses `animate-pulse` from
 * tailwindcss-animate and a neutral surface token so it blends into
 * any page background.
 *
 * `aria-hidden` because skeletons are decorative — the *container*
 * should own the loading semantics (see the composed skeletons, which
 * set role="status" / aria-busy on their wrapper).
 */
export function Skeleton({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      aria-hidden="true"
      className={cn("animate-pulse rounded-md bg-surface-container-high", className)}
      {...props}
    />
  );
}
