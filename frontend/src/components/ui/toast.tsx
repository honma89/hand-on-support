"use client";

import * as React from "react";
import * as ToastPrimitive from "@radix-ui/react-toast";
import { cn } from "@/lib/utils";
import type { ToastVariant } from "@/lib/hooks/use-toast";

/**
 * Styled Radix Toast primitives. Radix gives us the accessibility for
 * free: an `aria-live` region, swipe-to-dismiss, hotkey focus (F8), and
 * pause-on-hover. We only add design-system styling here.
 */
export const ToastProvider = ToastPrimitive.Provider;

export const ToastViewport = React.forwardRef<
  React.ElementRef<typeof ToastPrimitive.Viewport>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitive.Viewport>
>(({ className, ...props }, ref) => (
  <ToastPrimitive.Viewport
    ref={ref}
    className={cn(
      // Mobile-first: full-width stack pinned to the bottom; on larger
      // screens it moves to the top-right corner.
      "fixed bottom-0 left-0 right-0 z-[100] flex max-h-screen w-full flex-col gap-sm p-md sm:bottom-auto sm:left-auto sm:right-0 sm:top-0 sm:max-w-sm",
      className,
    )}
    {...props}
  />
));
ToastViewport.displayName = ToastPrimitive.Viewport.displayName;

/** Per-variant accent: colored left border + icon halo, neutral body. */
const VARIANT_CONFIG: Record<ToastVariant, { icon: string; accent: string; iconWrap: string }> = {
  success: {
    icon: "check_circle",
    accent: "border-l-tertiary",
    iconWrap: "bg-tertiary-container/50 text-on-tertiary-container",
  },
  error: {
    icon: "error",
    accent: "border-l-error",
    iconWrap: "bg-error/10 text-error",
  },
  info: {
    icon: "info",
    accent: "border-l-primary-container",
    iconWrap: "bg-primary-container/40 text-on-primary-container",
  },
};

export interface ToastProps
  extends React.ComponentPropsWithoutRef<typeof ToastPrimitive.Root> {
  variant?: ToastVariant;
}

export const Toast = React.forwardRef<
  React.ElementRef<typeof ToastPrimitive.Root>,
  ToastProps
>(({ className, variant = "info", ...props }, ref) => {
  const config = VARIANT_CONFIG[variant];
  return (
    <ToastPrimitive.Root
      ref={ref}
      className={cn(
        "group pointer-events-auto relative flex items-start gap-sm overflow-hidden rounded-xl border border-l-4 border-outline-variant bg-surface-container-lowest p-md shadow-ambient-hover",
        // Enter/exit + swipe animations (tailwindcss-animate).
        "data-[state=open]:animate-in data-[state=closed]:animate-out data-[swipe=end]:animate-out",
        "data-[state=open]:slide-in-from-bottom-2 sm:data-[state=open]:slide-in-from-right-full",
        "data-[state=closed]:fade-out-80 data-[swipe=end]:fade-out-80",
        "data-[swipe=move]:translate-x-[var(--radix-toast-swipe-move-x)] data-[swipe=move]:transition-none data-[swipe=cancel]:translate-x-0 data-[swipe=cancel]:transition-transform",
        config.accent,
        className,
      )}
      {...props}
    >
      <span
        aria-hidden="true"
        className={cn(
          "mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full",
          config.iconWrap,
        )}
      >
        <span className="material-symbols-outlined text-xl leading-none">{config.icon}</span>
      </span>
      {props.children}
    </ToastPrimitive.Root>
  );
});
Toast.displayName = ToastPrimitive.Root.displayName;

export const ToastTitle = React.forwardRef<
  React.ElementRef<typeof ToastPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitive.Title>
>(({ className, ...props }, ref) => (
  <ToastPrimitive.Title
    ref={ref}
    className={cn("font-label-md text-label-md text-on-surface", className)}
    {...props}
  />
));
ToastTitle.displayName = ToastPrimitive.Title.displayName;

export const ToastDescription = React.forwardRef<
  React.ElementRef<typeof ToastPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitive.Description>
>(({ className, ...props }, ref) => (
  <ToastPrimitive.Description
    ref={ref}
    className={cn("mt-0.5 font-body-md text-sm text-on-surface-variant", className)}
    {...props}
  />
));
ToastDescription.displayName = ToastPrimitive.Description.displayName;

export const ToastClose = React.forwardRef<
  React.ElementRef<typeof ToastPrimitive.Close>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitive.Close>
>(({ className, ...props }, ref) => (
  <ToastPrimitive.Close
    ref={ref}
    aria-label="Dismiss notification"
    className={cn(
      "absolute right-2 top-2 rounded-full p-1 text-on-surface-variant/70 transition-colors hover:bg-surface-container hover:text-on-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
      className,
    )}
    toast-close=""
    {...props}
  >
    <span aria-hidden="true" className="material-symbols-outlined text-lg leading-none">
      close
    </span>
  </ToastPrimitive.Close>
));
ToastClose.displayName = ToastPrimitive.Close.displayName;
