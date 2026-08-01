"use client";

import * as React from "react";
import { isAxiosError } from "axios";

/**
 * A tiny toast store (no extra dependency) inspired by the shadcn/ui
 * pattern. `toast()` can be called from anywhere — event handlers,
 * mutation callbacks, plain functions — and the <Toaster /> mounted in
 * the layout renders the results.
 *
 * Usage:
 *   toast.success("Event published");
 *   toast.error(err, "Couldn't publish the event");
 *   toast({ title: "Saved", description: "Draft updated", variant: "info" });
 */

export type ToastVariant = "success" | "error" | "info";

export interface ToastData {
  id: string;
  title: string;
  description?: string;
  variant: ToastVariant;
  duration?: number;
}

type ToastInput = Omit<ToastData, "id" | "variant"> & { variant?: ToastVariant };

const DEFAULT_DURATION = 5000;

let count = 0;
const genId = () => `toast-${++count}`;

// --- Minimal external store -------------------------------------------------
let toasts: ToastData[] = [];
const listeners = new Set<(t: ToastData[]) => void>();

function emit() {
  for (const listener of listeners) listener(toasts);
}

function addToast(input: ToastInput): string {
  const id = genId();
  const next: ToastData = {
    duration: DEFAULT_DURATION,
    variant: "info",
    ...input,
    id,
  };
  toasts = [next, ...toasts].slice(0, 4); // cap concurrent toasts so a burst of errors can't bury the UI
  emit();
  return id;
}

export function dismissToast(id: string) {
  toasts = toasts.filter((t) => t.id !== id);
  emit();
}

/**
 * Pull a human-readable message out of an unknown error. Handles axios
 * errors (FastAPI's `detail`), plain Errors, and strings — so callers
 * can pass whatever a `catch` block gives them.
 */
export function getErrorMessage(error: unknown, fallback = "Something went wrong. Please try again."): string {
  if (isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg as string;
    return error.message || fallback;
  }
  if (error instanceof Error && error.message) return error.message;
  if (typeof error === "string") return error;
  return fallback;
}

// --- Public `toast` API -----------------------------------------------------
interface ToastFn {
  (input: ToastInput): string;
  success: (title: string, description?: string) => string;
  info: (title: string, description?: string) => string;
  /** Accepts a title string OR an unknown error (message is extracted). */
  error: (titleOrError: string | unknown, description?: string) => string;
}

export const toast = ((input: ToastInput) => addToast(input)) as ToastFn;

toast.success = (title, description) => addToast({ title, description, variant: "success" });
toast.info = (title, description) => addToast({ title, description, variant: "info" });
toast.error = (titleOrError, description) => {
  const title = typeof titleOrError === "string" ? titleOrError : "Something went wrong";
  const desc =
    typeof titleOrError === "string" ? description : (description ?? getErrorMessage(titleOrError));
  return addToast({ title, description: desc, variant: "error" });
};

/** Subscribe to the toast store. Used by <Toaster />. */
export function useToastStore() {
  const [state, setState] = React.useState<ToastData[]>(toasts);
  React.useEffect(() => {
    listeners.add(setState);
    return () => {
      listeners.delete(setState);
    };
  }, []);
  return { toasts: state, dismiss: dismissToast };
}
