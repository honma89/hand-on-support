import { NextRequest, NextResponse } from "next/server";
import { jwtVerify } from "jose";

/**
 * Route access rules. Checked in order; the first matching prefix wins.
 *
 * "public"          - anyone, logged in or not
 * "authenticated"    - any logged-in role (volunteer/organizer/admin)
 * "admin"            - role === "admin" only
 * "organizer"        - role === "organizer" or "admin"
 *
 * NOTE: this is a UX-layer gate only. The backend's require_admin /
 * require_organizer_or_admin dependencies remain the authoritative
 * enforcement for every actual API call -- this just stops the wrong
 * page shell from rendering (or a wrong role from even seeing the
 * navigation for a page it can't use) before that happens.
 */
const PUBLIC_PREFIXES = ["/", "/events", "/organization", "/about", "/login", "/register"];
const AUTHENTICATED_PREFIXES = ["/leaderboard", "/dashboard", "/notifications", "/wellbeing"];
const ADMIN_PREFIXES = ["/admin"];
const ORGANIZER_PREFIXES = ["/organizer"];

type Role = "volunteer" | "organizer" | "admin";

function matchesPrefix(pathname: string, prefixes: string[]): boolean {
  return prefixes.some((prefix) => {
    if (prefix === "/") return pathname === "/";
    return pathname === prefix || pathname.startsWith(`${prefix}/`);
  });
}

async function getRoleFromToken(token: string | undefined): Promise<Role | null> {
  if (!token) return null;
  const secret = process.env.JWT_SECRET_KEY;
  if (!secret) {
    // Misconfigured deployment -- fail closed (treat as unauthenticated)
    // rather than trusting an unverifiable token.
    console.error("middleware: JWT_SECRET_KEY is not set; treating all requests as unauthenticated.");
    return null;
  }
  try {
    const { payload } = await jwtVerify(token, new TextEncoder().encode(secret), {
      algorithms: ["HS256"],
    });
    if (payload.type !== "access") return null;
    return (payload.role as Role) ?? null;
  } catch {
    // Expired, malformed, or invalid signature -- treat as logged out.
    return null;
  }
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Public routes never need the cookie at all.
  if (matchesPrefix(pathname, PUBLIC_PREFIXES)) {
    return NextResponse.next();
  }

  const role = await getRoleFromToken(request.cookies.get("access_token")?.value);

  if (!role) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  if (matchesPrefix(pathname, ADMIN_PREFIXES) && role !== "admin") {
    const homeUrl = new URL("/", request.url);
    homeUrl.searchParams.set("error", "unauthorized");
    return NextResponse.redirect(homeUrl);
  }

  if (matchesPrefix(pathname, ORGANIZER_PREFIXES) && role !== "organizer" && role !== "admin") {
    const homeUrl = new URL("/", request.url);
    homeUrl.searchParams.set("error", "unauthorized");
    return NextResponse.redirect(homeUrl);
  }

  if (matchesPrefix(pathname, AUTHENTICATED_PREFIXES)) {
    // Any logged-in role is fine -- already confirmed role !== null above.
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  // Only run on actual navigable page routes. Excludes:
  // - /api/*        -- proxied straight to FastAPI, which enforces its
  //                    own auth independently; intercepting these here
  //                    would break every API call, including anonymous
  //                    public browsing (e.g. GET /api/v1/events).
  // - _next/*        -- framework internals
  // - static assets  -- images/icons/etc, never need gating
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|webp|ico)$).*)"],
};
