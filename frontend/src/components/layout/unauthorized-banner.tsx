"use client";

import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";

function UnauthorizedBannerInner() {
  const searchParams = useSearchParams();
  const [dismissed, setDismissed] = useState(false);
  const isUnauthorized = searchParams.get("error") === "unauthorized";

  if (!isUnauthorized || dismissed) return null;

  return (
    <div className="bg-destructive/10 border-b border-destructive/20 px-4 py-3">
      <div className="container mx-auto flex items-center justify-between gap-4">
        <p className="text-sm text-destructive">
          You don&apos;t have permission to view that page.
        </p>
        <button
          onClick={() => setDismissed(true)}
          className="text-sm text-destructive underline-offset-4 hover:underline"
          aria-label="Dismiss"
        >
          Dismiss
        </button>
      </div>
    </div>
  );
}

export function UnauthorizedBanner() {
  return (
    <Suspense fallback={null}>
      <UnauthorizedBannerInner />
    </Suspense>
  );
}
