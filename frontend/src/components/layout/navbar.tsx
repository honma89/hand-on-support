"use client";

import Link from "next/link";
import { Bell, LogOut, Trophy } from "lucide-react";
import { Button, buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useCurrentUser, useLogout } from "@/lib/hooks/use-auth";
import { usePointBalance, useUnreadNotificationCount } from "@/lib/hooks/use-rewards";

export function Navbar() {
  const { data: user } = useCurrentUser();
  const { data: balance } = usePointBalance();
  const { data: unreadCount } = useUnreadNotificationCount();
  const logout = useLogout();

  return (
    <header className="sticky top-0 z-10 border-b border-border bg-background/95 backdrop-blur">
      <div className="container flex h-16 items-center justify-between">
        <Link href="/" className="text-lg font-bold text-primary">
          Hand On Support
        </Link>

        <nav className="hidden items-center gap-6 text-sm font-medium md:flex">
          <Link href="/events" className="hover:text-primary">
            Events
          </Link>
          <Link href="/leaderboard" className="hover:text-primary">
            Leaderboard
          </Link>
          {user && (
            <Link href="/dashboard" className="hover:text-primary">
              Dashboard
            </Link>
          )}
          {user?.role === "admin" && (
            <Link href="/admin" className="hover:text-primary">
              Admin
            </Link>
          )}
        </nav>

        <div className="flex items-center gap-3">
          {user ? (
            <>
              {balance !== undefined && (
                <div className="flex items-center gap-1 rounded-full bg-accent/20 px-3 py-1 text-sm font-semibold text-accent-foreground">
                  <Trophy className="h-4 w-4" />
                  {balance.balance}
                </div>
              )}
              <Link href="/notifications" className="relative rounded-full p-2 hover:bg-secondary">
                <Bell className="h-5 w-5" />
                {!!unreadCount && (
                  <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-destructive text-[10px] text-destructive-foreground">
                    {unreadCount}
                  </span>
                )}
              </Link>
              <Button variant="ghost" size="icon" onClick={() => logout.mutate()} title="Log out">
                <LogOut className="h-4 w-4" />
              </Button>
            </>
          ) : (
            <>
              <Link href="/login" className={cn(buttonVariants({ variant: "ghost" }))}>
                Log in
              </Link>
              <Link href="/register" className={cn(buttonVariants({ variant: "default" }))}>
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
