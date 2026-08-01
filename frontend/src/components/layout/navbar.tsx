"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bell, LogOut, Menu, Trophy, X } from "lucide-react";
import { Button, buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useCurrentUser, useLogout } from "@/lib/hooks/use-auth";
import { usePointBalance, useUnreadNotificationCount } from "@/lib/hooks/use-rewards";

const mobileLinks = [
  { href: "/events", label: "Events", authOnly: false },
  { href: "/leaderboard", label: "Leaderboard", authOnly: false },
  { href: "/organization", label: "Organization", authOnly: false },
  { href: "/about", label: "About Us", authOnly: false },
  { href: "/dashboard", label: "Dashboard", authOnly: true },
  { href: "/notifications", label: "Notifications", authOnly: true },
  { href: "/wellbeing", label: "Wellbeing", authOnly: true },
];

export function Navbar() {
  const { data: user } = useCurrentUser();
  const { data: balance } = usePointBalance();
  const { data: unreadCount } = useUnreadNotificationCount();
  const logout = useLogout();
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-30 border-b border-border/60 bg-background/95 backdrop-blur-sm shadow-sm">
      <div className="container mx-auto flex h-20 items-center justify-between gap-4 px-4 md:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary-container text-on-primary-container font-bold">
            H
          </div>
          <Link href="/" className="text-xl font-bold tracking-tight text-primary">
            Hand On Support
          </Link>
        </div>

        <nav className="hidden items-center gap-6 text-sm font-semibold text-on-surface-variant md:flex">
          <Link href="/events" className="transition hover:text-primary">
            Events
          </Link>
          <Link href="/leaderboard" className="transition hover:text-primary">
            Leaderboard
          </Link>
          <Link href="/organization" className="transition hover:text-primary">
            Organization
          </Link>
          <Link href="/about" className="transition hover:text-primary">
            About Us
          </Link>
          {user && (
            <Link href="/dashboard" className="transition hover:text-primary">
              Dashboard
            </Link>
          )}
          {user && (
            <Link href="/wellbeing" className="transition hover:text-primary">
              Wellbeing
            </Link>
          )}
          {user?.role === "organizer" && (
            <Link href="/organizer" className="transition hover:text-primary">
              My Events
            </Link>
          )}
          {user?.role === "admin" && (
            <Link href="/admin" className="transition hover:text-primary">
              Admin
            </Link>
          )}
        </nav>

        <div className="flex items-center gap-2 md:gap-3">
          {user ? (
            <>
              {balance !== undefined && (
                <div className="hidden sm:flex items-center gap-2 rounded-full bg-secondary-container/10 px-3 py-2 text-sm font-semibold text-secondary">
                  <Trophy className="h-4 w-4" />
                  {balance.balance}
                </div>
              )}
              <Link
                href="/notifications"
                className="relative flex h-11 w-11 items-center justify-center rounded-full bg-surface border border-surface-variant transition hover:border-secondary-container hover:bg-secondary-container/10"
              >
                <Bell className="h-5 w-5 text-on-surface-variant" />
                {!!unreadCount && (
                  <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-secondary text-on-secondary text-[10px] font-semibold">
                    {unreadCount}
                  </span>
                )}
              </Link>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => logout.mutate()}
                title="Log out"
                className="hidden md:inline-flex"
              >
                <LogOut className="h-4 w-4 text-on-surface-variant" />
              </Button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className={cn(
                  buttonVariants({ variant: "ghost", size: "default" }),
                  "hidden sm:inline-flex rounded-full px-4 py-2",
                )}
              >
                Log in
              </Link>
              <Link
                href="/register"
                className={cn(buttonVariants({ variant: "default", size: "default" }), "rounded-full px-5 py-2")}
              >
                Sign up
              </Link>
            </>
          )}

          <button
            className="flex h-11 w-11 items-center justify-center rounded-full border border-surface-variant md:hidden"
            onClick={() => setMenuOpen((v) => !v)}
            aria-label="Toggle menu"
          >
            {menuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {menuOpen && (
        <nav className="md:hidden border-t border-border/60 bg-background px-4 py-3 flex flex-col gap-1">
          {mobileLinks
            .filter((l) => !l.authOnly || !!user)
            .map((l) => (
              <Link
                key={l.href}
                href={l.href}
                onClick={() => setMenuOpen(false)}
                className={cn(
                  "rounded-lg px-3 py-3 text-sm font-semibold transition",
                  pathname === l.href
                    ? "bg-primary-container text-on-primary-container"
                    : "text-on-surface-variant hover:bg-surface-container",
                )}
              >
                {l.label}
              </Link>
            ))}

          {user?.role === "organizer" && (
            <Link
              href="/organizer"
              onClick={() => setMenuOpen(false)}
              className={cn(
                "rounded-lg px-3 py-3 text-sm font-semibold transition",
                pathname.startsWith("/organizer")
                  ? "bg-primary-container text-on-primary-container"
                  : "text-on-surface-variant hover:bg-surface-container",
              )}
            >
              My Events
            </Link>
          )}

          {user?.role === "admin" && (
            <Link
              href="/admin"
              onClick={() => setMenuOpen(false)}
              className={cn(
                "rounded-lg px-3 py-3 text-sm font-semibold transition",
                pathname.startsWith("/admin")
                  ? "bg-primary-container text-on-primary-container"
                  : "text-on-surface-variant hover:bg-surface-container",
              )}
            >
              Admin
            </Link>
          )}

          {user ? (
            <>
              {balance !== undefined && (
                <div className="flex items-center gap-2 px-3 py-2 text-sm font-semibold text-secondary sm:hidden">
                  <Trophy className="h-4 w-4" />
                  {balance.balance} points
                </div>
              )}
              <button
                onClick={() => {
                  setMenuOpen(false);
                  logout.mutate();
                }}
                className="text-left rounded-lg px-3 py-3 text-sm font-semibold text-on-surface-variant hover:bg-surface-container transition"
              >
                Log out
              </button>
            </>
          ) : (
            <Link
              href="/login"
              onClick={() => setMenuOpen(false)}
              className="rounded-lg px-3 py-3 text-sm font-semibold text-on-surface-variant hover:bg-surface-container transition"
            >
              Log in
            </Link>
          )}
        </nav>
      )}
    </header>
  );
}
