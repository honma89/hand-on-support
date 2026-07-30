"use client";

import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Navbar } from "./navbar";

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isAppShell = ["/dashboard", "/leaderboard", "/notifications", "/admin"].some((route) =>
    pathname?.startsWith(route),
  );

  return (
    <div className={cn("min-h-screen bg-background text-foreground", isAppShell && "md:pl-72")}>
      <Navbar />
      {children}
    </div>
  );
}
