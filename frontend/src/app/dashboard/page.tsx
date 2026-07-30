"use client";

import Link from "next/link";
import { useCurrentUser } from "@/lib/hooks/use-auth";
import { useMyRegistrations } from "@/lib/hooks/use-events";
import {
  useLeaderboard,
  useMyBadges,
  usePointBalance,
  usePointHistory,
} from "@/lib/hooks/use-rewards";

const POINTS_PER_LEVEL = 200;

function levelInfo(points: number) {
  const level = Math.floor(points / POINTS_PER_LEVEL) + 1;
  const intoLevel = points % POINTS_PER_LEVEL;
  const percent = Math.round((intoLevel / POINTS_PER_LEVEL) * 100);
  return { level, percent, pointsToNext: POINTS_PER_LEVEL - intoLevel };
}

export default function DashboardPage() {
  const { data: user } = useCurrentUser();
  const { data: balance } = usePointBalance();
  const { data: history } = usePointHistory();
  const { data: badges } = useMyBadges();
  const { data: registrations } = useMyRegistrations();
  const { data: leaderboard } = useLeaderboard("all_time");

  const upcoming = registrations?.filter(
    (r) => r.status !== "cancelled" && new Date(r.event.start_datetime) >= new Date(),
  );

  const points = balance?.balance ?? 0;
  const { level, percent, pointsToNext } = levelInfo(points);
  const myRank = leaderboard?.find((e) => e.user_id === user?.id);
  const topThree = leaderboard?.slice(0, 3) ?? [];

  return (
    <div className="p-margin-mobile md:p-margin-desktop min-h-screen max-w-7xl mx-auto">
      <header className="mb-lg">
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-primary">
          Point Bank
        </h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant mt-xs">
          {user ? `Welcome back, ${user.full_name.split(" ")[0]}.` : "Track your impact and achievements."}
        </p>
      </header>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-gutter mb-gutter">
        <div className="glass-card rounded-xl p-md flex items-center justify-between shadow-ambient shadow-ambient-hover transition-shadow">
          <div>
            <p className="font-label-md text-label-md text-on-surface-variant">Total Points</p>
            <h3 className="font-headline-lg text-headline-lg text-primary mt-xs">{points}</h3>
          </div>
          <div className="w-14 h-14 rounded-full bg-primary-container flex items-center justify-center">
            <span className="material-symbols-outlined text-on-primary-container text-3xl">stars</span>
          </div>
        </div>

        <div className="glass-card rounded-xl p-md flex items-center justify-between shadow-ambient shadow-ambient-hover transition-shadow">
          <div>
            <p className="font-label-md text-label-md text-on-surface-variant">Upcoming Events</p>
            <h3 className="font-headline-lg text-headline-lg text-secondary mt-xs">
              {upcoming?.length ?? 0}
            </h3>
          </div>
          <div className="w-14 h-14 rounded-full bg-secondary-container/20 flex items-center justify-center">
            <span className="material-symbols-outlined text-secondary text-3xl">event</span>
          </div>
        </div>

        <div className="glass-card rounded-xl p-md flex items-center justify-between shadow-ambient shadow-ambient-hover transition-shadow">
          <div>
            <p className="font-label-md text-label-md text-on-surface-variant">Badges Earned</p>
            <h3 className="font-headline-lg text-headline-lg text-tertiary mt-xs">
              {badges?.length ?? 0}
            </h3>
          </div>
          <div className="w-14 h-14 rounded-full bg-tertiary-container/20 flex items-center justify-center">
            <span className="material-symbols-outlined text-tertiary text-3xl">military_tech</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        {/* Left column */}
        <div className="lg:col-span-8 flex flex-col gap-gutter">
          <div className="glass-card rounded-xl p-md">
            <div className="flex justify-between items-end mb-sm">
              <div>
                <h4 className="font-headline-md text-headline-md text-on-surface">
                  Level {level}: Community Volunteer
                </h4>
                <p className="font-body-md text-body-md text-on-surface-variant mt-xs">
                  {pointsToNext} points to Level {level + 1}
                </p>
              </div>
              <span className="font-label-md text-label-md text-secondary">{percent}%</span>
            </div>
            <div className="w-full bg-surface-variant rounded-full h-4 overflow-hidden">
              <div
                className="bg-secondary-container h-4 rounded-full transition-all duration-500"
                style={{ width: `${percent}%` }}
              />
            </div>
          </div>

          <div className="glass-card rounded-xl p-md">
            <h4 className="font-headline-md text-headline-md text-on-surface mb-md">Recent Badges</h4>
            {badges && badges.length === 0 && (
              <p className="font-body-md text-body-md text-on-surface-variant">
                No badges yet — attend an event to start earning them.
              </p>
            )}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-sm">
              {badges?.slice(0, 4).map((ub) => (
                <div
                  key={ub.id}
                  className="flex flex-col items-center text-center p-sm bg-surface rounded-lg border border-outline-variant hover:border-primary-container transition-colors"
                >
                  <div className="w-14 h-14 rounded-full bg-primary-container flex items-center justify-center mb-xs text-2xl">
                    {ub.badge.icon}
                  </div>
                  <span className="font-label-md text-label-md text-on-surface">{ub.badge.name}</span>
                </div>
              ))}
              {badges && badges.length < 4 && (
                <div className="flex flex-col items-center justify-center text-center p-sm bg-surface-variant/30 rounded-lg border border-dashed border-outline-variant opacity-60">
                  <span className="material-symbols-outlined text-on-surface-variant text-3xl mb-xs">lock</span>
                  <span className="font-label-md text-label-md text-on-surface-variant">Next Badge</span>
                </div>
              )}
            </div>
          </div>

          <div className="glass-card rounded-xl p-md flex-1">
            <h4 className="font-headline-md text-headline-md text-on-surface mb-md">Activity History</h4>
            <div className="flex flex-col divide-y divide-outline-variant/40">
              {history && history.length === 0 && (
                <p className="font-body-md text-body-md text-on-surface-variant py-sm">
                  No point activity yet.
                </p>
              )}
              {history?.slice(0, 8).map((t) => (
                <div
                  key={t.id}
                  className="flex items-center justify-between py-sm hover:bg-surface rounded-lg transition-colors px-xs"
                >
                  <div className="flex items-center gap-sm">
                    <div className="w-10 h-10 rounded-full bg-surface-variant/50 flex items-center justify-center">
                      <span className="material-symbols-outlined text-on-surface-variant text-lg">
                        {t.amount >= 0 ? "redeem" : "shopping_cart"}
                      </span>
                    </div>
                    <div>
                      <p className="font-label-md text-label-md text-on-surface">{t.description}</p>
                      <p className="font-body-md text-sm text-on-surface-variant">
                        {new Date(t.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <span
                    className={`font-label-md text-label-md px-3 py-1 rounded-full ${
                      t.amount >= 0 ? "text-primary bg-primary-container/20" : "text-secondary bg-secondary-container/10"
                    }`}
                  >
                    {t.amount >= 0 ? "+" : ""}
                    {t.amount} pts
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right column: Leaderboard */}
        <div className="lg:col-span-4 flex flex-col gap-gutter">
          <div className="rounded-xl p-md bg-gradient-to-br from-primary-container to-primary-fixed relative overflow-hidden shadow-ambient">
            <span className="material-symbols-outlined absolute top-sm right-sm text-6xl opacity-20 text-on-primary-container">
              workspace_premium
            </span>
            <div className="relative z-10">
              <span className="font-label-md text-label-md text-on-primary-container bg-white/50 px-2 py-1 rounded-md mb-md inline-block">
                Your Standing
              </span>
              <h4 className="font-headline-md text-headline-md text-on-primary-container mb-sm">
                {myRank ? `Rank #${myRank.rank}` : "Not ranked yet"}
              </h4>
              <p className="font-body-md text-sm text-on-primary-container">
                {myRank
                  ? `You have ${myRank.total_points} points. Keep volunteering to climb the leaderboard!`
                  : "Attend an event to start earning points and appear on the leaderboard."}
              </p>
            </div>
          </div>

          <div className="glass-card rounded-xl p-md flex-1">
            <div className="flex justify-between items-center mb-md">
              <h4 className="font-headline-md text-headline-md text-on-surface">Top Volunteers</h4>
              <span className="material-symbols-outlined text-secondary">local_fire_department</span>
            </div>
            <div className="flex flex-col gap-xs">
              {topThree.map((entry) => (
                <div
                  key={entry.user_id}
                  className="flex items-center justify-between p-sm bg-surface rounded-lg"
                >
                  <div className="flex items-center gap-sm">
                    <span className="font-headline-md text-headline-md text-primary-fixed-dim w-6 text-center">
                      {entry.rank}
                    </span>
                    <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center font-label-md text-label-md text-on-surface-variant">
                      {entry.full_name.charAt(0)}
                    </div>
                    <span className="font-label-md text-label-md text-on-surface">{entry.full_name}</span>
                  </div>
                  <span className="font-label-md text-label-md text-on-surface-variant">
                    {entry.total_points}
                  </span>
                </div>
              ))}
              {topThree.length === 0 && (
                <p className="font-body-md text-body-md text-on-surface-variant">No rankings yet.</p>
              )}
            </div>
            <Link
              href="/leaderboard"
              className="block w-full mt-md py-sm text-center font-label-md text-label-md text-secondary hover:underline"
            >
              View Full Leaderboard
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
