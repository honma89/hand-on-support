import { cn } from "@/lib/utils";

export interface EmptyStateProps {
  /** Material Symbols Outlined ligature shown in the halo. */
  icon?: string;
  title: string;
  description?: string;
  /** Optional call-to-action (e.g. a <Button> or <Link>). */
  action?: React.ReactNode;
  /** Renders the error-toned variant for failed loads. */
  variant?: "default" | "error";
  className?: string;
}

/**
 * A friendly, consistent empty / error state.
 *
 * Replaces the scattered one-line "No events yet" / "Could not load"
 * paragraphs with a single centred pattern: an icon in a soft brand
 * halo, a headline, supporting copy, and an optional action. Warm and
 * civic-minded rather than clinical, matching the "Bhutanese Youth
 * Empowerment" tone.
 */
export function EmptyState({
  icon = "inbox",
  title,
  description,
  action,
  variant = "default",
  className,
}: EmptyStateProps) {
  const isError = variant === "error";

  return (
    <div
      role={isError ? "alert" : "status"}
      className={cn(
        "flex flex-col items-center justify-center rounded-xl border border-dashed px-md py-lg text-center",
        isError ? "border-error/30 bg-error/5" : "border-outline-variant bg-surface-container-low",
        className,
      )}
    >
      <span
        aria-hidden="true"
        className={cn(
          "mb-sm flex h-16 w-16 items-center justify-center rounded-full",
          isError ? "bg-error/10 text-error" : "bg-primary-container/40 text-on-primary-container",
        )}
      >
        <span className="material-symbols-outlined text-4xl leading-none">
          {isError ? "error" : icon}
        </span>
      </span>
      <h3 className="font-headline-md text-headline-md text-on-surface text-balance">{title}</h3>
      {description && (
        <p className="mt-xs max-w-md font-body-md text-body-md text-on-surface-variant text-pretty">
          {description}
        </p>
      )}
      {action && <div className="mt-md">{action}</div>}
    </div>
  );
}
