"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import {
  AlertDialog,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogAction,
  AlertDialogCancel,
} from "@/components/ui/alert-dialog";

export interface ConfirmDialogProps {
  /** Dialog heading, e.g. "Cancel this event?". */
  title: string;
  /** Supporting copy explaining the consequence. */
  description: string;
  /** Confirm button label. Defaults to "Confirm". */
  confirmLabel?: string;
  /** Cancel button label. Defaults to "Keep it". */
  cancelLabel?: string;
  /** Material Symbols ligature shown in the header halo. */
  icon?: string;
  /**
   * "destructive" (default) paints the confirm button in the error tone
   * for irreversible actions; "default" uses the primary tone for
   * benign confirmations.
   */
  tone?: "destructive" | "default";
  /**
   * Runs when the user confirms. May be async — while the returned
   * promise is pending the confirm button shows a spinner and the
   * dialog stays open. Throwing keeps the dialog open (surface the
   * error via a toast in the caller); resolving closes it.
   */
  onConfirm: () => void | Promise<void>;

  /* --- Uncontrolled usage: pass a trigger and we manage open state. --- */
  trigger?: React.ReactNode;

  /* --- Controlled usage: drive open state yourself. --- */
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

/**
 * Reusable "are you sure?" gate for destructive actions (Cancel event,
 * Unpublish, Delete). Built on the accessible AlertDialog primitive.
 *
 * Two ways to use it:
 *
 * 1. Trigger mode — wrap the button that starts the action:
 *
 *      <ConfirmDialog
 *        title="Cancel this event?"
 *        description="Registered volunteers will be notified. This can't be undone."
 *        confirmLabel="Yes, cancel event"
 *        onConfirm={() => cancelEvent.mutateAsync()}
 *        trigger={<Button variant="outline">Cancel event</Button>}
 *      />
 *
 * 2. Controlled mode — drive `open`/`onOpenChange` from your own state.
 */
export function ConfirmDialog({
  title,
  description,
  confirmLabel = "Confirm",
  cancelLabel = "Keep it",
  icon = "warning",
  tone = "destructive",
  onConfirm,
  trigger,
  open: controlledOpen,
  onOpenChange: controlledOnOpenChange,
}: ConfirmDialogProps) {
  // Support both controlled and uncontrolled open state.
  const [internalOpen, setInternalOpen] = useState(false);
  const isControlled = controlledOpen !== undefined;
  const open = isControlled ? controlledOpen : internalOpen;
  const setOpen = isControlled ? (controlledOnOpenChange ?? (() => {})) : setInternalOpen;

  const [pending, setPending] = useState(false);
  const isDestructive = tone === "destructive";

  const handleConfirm = async () => {
    try {
      setPending(true);
      await onConfirm();
      setOpen(false);
    } catch {
      // Leave the dialog open so the user can retry; the caller is
      // responsible for surfacing the failure (e.g. a toast).
    } finally {
      setPending(false);
    }
  };

  return (
    <AlertDialog open={open} onOpenChange={pending ? undefined : setOpen}>
      {trigger && <AlertDialogTrigger asChild>{trigger}</AlertDialogTrigger>}

      <AlertDialogContent>
        <AlertDialogHeader>
          <span
            aria-hidden="true"
            className={cn(
              "flex h-12 w-12 items-center justify-center rounded-full",
              isDestructive ? "bg-error/10 text-error" : "bg-primary-container/40 text-on-primary-container",
            )}
          >
            <span className="material-symbols-outlined text-2xl leading-none">{icon}</span>
          </span>
          <AlertDialogTitle>{title}</AlertDialogTitle>
          <AlertDialogDescription>{description}</AlertDialogDescription>
        </AlertDialogHeader>

        <AlertDialogFooter>
          {/* preventDefault lets us control closing ourselves after the
              (possibly async) confirm resolves. */}
          <AlertDialogCancel
            disabled={pending}
            className="inline-flex h-11 items-center justify-center rounded-full border border-outline bg-transparent px-6 font-label-md text-label-md text-on-surface transition-colors hover:bg-surface-container focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
          >
            {cancelLabel}
          </AlertDialogCancel>
          <AlertDialogAction
            onClick={(e) => {
              e.preventDefault();
              void handleConfirm();
            }}
            disabled={pending}
            className={cn(
              "inline-flex h-11 items-center justify-center gap-xs rounded-full px-6 font-label-md text-label-md transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-70",
              isDestructive
                ? "bg-error text-on-error hover:bg-error/90"
                : "bg-primary-container text-on-primary-container hover:bg-primary-fixed-dim",
            )}
          >
            {pending && (
              <span
                aria-hidden="true"
                className="material-symbols-outlined animate-spin text-lg leading-none"
              >
                progress_activity
              </span>
            )}
            {pending ? "Working…" : confirmLabel}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
