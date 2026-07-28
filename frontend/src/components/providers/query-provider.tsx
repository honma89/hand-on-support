"use client";

import { useState } from "react";
import {
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";

export function QueryProvider({ children }: { children: React.ReactNode }) {
  // Created inside useState so each browser session gets its own client
  // instance (avoids sharing cached data across users during SSR).
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 30 * 1000,
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
