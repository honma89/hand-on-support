"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useUnreadNotificationCount } from "@/lib/hooks/use-rewards";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: "dashboard" },
  { href: "/leaderboard", label: "Leaderboard", icon: "military_tech" },
  { href: "/notifications", label: "Notifications", icon: "notifications" },
  { href: "/organization", label: "Organization", icon: "account_tree" },
  { href: "/wellbeing", label: "Wellbeing", icon: "self_improvement" },
];

export function SideNav() {
  const pathname = usePathname();
  const { data: user } = useCurrentUser();
  const { data: unreadCount } = useUnreadNotificationCount();

  return (
    <aside className="hidden md:flex flex-col fixed left-0 top-20 bottom-0 w-64 border-r border-outline-variant bg-surface-container-lowest p-md gap-xs overflow-y-auto">
      {navItems.map((item) => {
        const active = pathname === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center gap-sm px-sm py-sm rounded-xl font-label-md text-label-md transition-colors",
              active
                ? "bg-primary-container text-on-primary-container"
                : "text-on-surface-variant hover:bg-surface-container",
            )}
          >
            <span className="material-symbols-outlined text-xl">{item.icon}</span>
            {item.label}
            {item.href === "/notifications" && !!unreadCount && (
              <span className="ml-auto flex h-5 w-5 items-center justify-center rounded-full bg-secondary text-[10px] text-secondary-foreground">
                {unreadCount}
              </span>
            )}
          </Link>
        );
      })}

      {user?.role === "admin" && (
        <Link
          href="/admin"
          className={cn(
            "flex items-center gap-sm px-sm py-sm rounded-xl font-label-md text-label-md transition-colors mt-md pt-md border-t border-outline-variant",
            pathname === "/admin"
              ? "bg-primary-container text-on-primary-container"
              : "text-on-surface-variant hover:bg-surface-container",
          )}
        >
          <span className="material-symbols-outlined text-xl">admin_panel_settings</span>
          Admin
        </Link>
      )}
    </aside>
  );
}
