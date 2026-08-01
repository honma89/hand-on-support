"use client";

import {
  ToastProvider,
  ToastViewport,
  Toast,
  ToastTitle,
  ToastDescription,
  ToastClose,
} from "@/components/ui/toast";
import { useToastStore } from "@/lib/hooks/use-toast";

/**
 * Mount this once, near the root (see app/layout.tsx). It subscribes to
 * the toast store and renders each active toast. Everything else in the
 * app just calls `toast()` / `toast.error()` — no context wiring needed
 * at the call site.
 */
export function Toaster() {
  const { toasts, dismiss } = useToastStore();

  return (
    <ToastProvider swipeDirection="right">
      {toasts.map(({ id, title, description, variant, duration }) => (
        <Toast
          key={id}
          variant={variant}
          duration={duration}
          // Remove from the store once Radix finishes closing (whether by
          // timeout, swipe, or the close button).
          onOpenChange={(open) => {
            if (!open) dismiss(id);
          }}
        >
          <div className="flex-1 pr-md">
            <ToastTitle>{title}</ToastTitle>
            {description && <ToastDescription>{description}</ToastDescription>}
          </div>
          <ToastClose />
        </Toast>
      ))}
      <ToastViewport />
    </ToastProvider>
  );
}
