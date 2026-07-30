"use client";

import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Navbar } from "./navbar";
import { SideNav } from "./side-nav";

const APP_ROUTES = ["/dashboard", "/leaderboard", "/notifications", "/admin", "/organization", "/wellbeing"];

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isAppShell = APP_ROUTES.some((route) => pathname?.startsWith(route));

  return (
    <div className={cn("min-h-screen bg-background text-foreground")}>
      <Navbar />
      {isAppShell && <SideNav />}
      <div className={cn(isAppShell && "md:pl-64")}>{children}</div>
    </div>
  );
}
