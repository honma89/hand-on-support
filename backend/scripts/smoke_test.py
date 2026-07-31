"""
One-off smoke test (not part of the permanent test suite) run manually to
verify the full request lifecycle across every module works against a real
Postgres database. Exercises: register -> login -> create badge (admin) ->
create+publish event (admin) -> register for event -> mark attendance
(auto-awards points + badge) -> check balance -> check leaderboard ->
check notifications -> check admin dashboard -> check analytics.
"""
import asyncio
import uuid

import httpx

from app.main import app

async def main():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        unique = uuid.uuid4().hex[:8]

        # --- Register admin (first user promoted manually below via SQL is
        # unrealistic in prod, but for this smoke test we register two
        # users and manually flip one to ADMIN via direct DB access) ---
        admin_email = f"admin_{unique}@handonsupport.bt"
        vol_email = f"vol_{unique}@handonsupport.bt"

        r = await client.post(
            "/api/v1/auth/register",
            json={"email": admin_email, "password": "AdminPass123", "full_name": "Admin User"},
        )
        assert r.status_code == 201, r.text
        admin_cookies = r.cookies
        admin_id = r.json()["user"]["id"]
        print("✓ Admin registered:", admin_email)

        r = await client.post(
            "/api/v1/auth/register",
            json={"email": vol_email, "password": "VolPass123", "full_name": "Volunteer User"},
        )
        assert r.status_code == 201, r.text
        vol_cookies = r.cookies
        vol_id = r.json()["user"]["id"]
        print("✓ Volunteer registered:", vol_email)

        # Promote admin_id to ADMIN and ORGANIZER-capable directly via DB
        # (bootstrapping problem: no one can call admin endpoints yet).
        from sqlalchemy import update
        from app.db.session import AsyncSessionLocal
        from app.models.user import User
        from app.models.enums import UserRole

        async with AsyncSessionLocal() as session:
            await session.execute(
                update(User).where(User.id == uuid.UUID(admin_id)).values(role=UserRole.ADMIN)
            )
            await session.commit()
        print("✓ Promoted admin user to ADMIN role")

        # Re-login to get a fresh access token reflecting the new role
        r = await client.post("/api/v1/auth/login", json={"email": admin_email, "password": "AdminPass123"})
        assert r.status_code == 200, r.text
        admin_cookies = r.cookies

        # --- Admin creates a badge ---
        r = await client.post(
            "/api/v1/badges",
            json={
                "name": f"First Steps {unique}",
                "description": "Attend your first event",
                "icon": "🌱",
                "criteria_type": "events_attended",
                "criteria_value": 1,
            },
            cookies=admin_cookies,
        )
        assert r.status_code == 201, r.text
        print("✓ Badge created:", r.json()["name"])

        # --- Admin creates + publishes an event ---
        r = await client.post(
            "/api/v1/events",
            json={
                "title": f"River Cleanup {unique}",
                "description": "Community river cleanup in Thimphu",
                "category": "Environment",
                "dzongkhag": "Thimphu",
                "start_datetime": "2026-08-15T09:00:00Z",
                "end_datetime": "2026-08-15T13:00:00Z",
                "capacity": 20,
                "points_reward": 25,
            },
            cookies=admin_cookies,
        )
        assert r.status_code == 201, r.text
        event_id = r.json()["id"]
        print("✓ Event created:", r.json()["title"])

        r = await client.patch(
            f"/api/v1/events/{event_id}", json={"status": "published"}, cookies=admin_cookies
        )
        assert r.status_code == 200, r.text
        print("✓ Event published")

        # --- Volunteer registers ---
        r = await client.post(f"/api/v1/events/{event_id}/register", cookies=vol_cookies)
        assert r.status_code == 201, r.text
        assert r.json()["status"] == "registered"
        print("✓ Volunteer registered for event")

        # --- Admin marks attendance PRESENT (should award points + badge) ---
        r = await client.post(
            f"/api/v1/events/{event_id}/attendance",
            json={"user_id": vol_id, "status": "present"},
            cookies=admin_cookies,
        )
        assert r.status_code == 201, r.text
        assert r.json()["points_awarded"] is True
        print("✓ Attendance marked PRESENT, points awarded")

        # --- Check volunteer point balance ---
        r = await client.get("/api/v1/points/me/balance", cookies=vol_cookies)
        assert r.status_code == 200, r.text
        assert r.json()["balance"] == 25, r.json()
        print("✓ Point balance correct:", r.json()["balance"])

        # --- Check badge was auto-awarded ---
        r = await client.get("/api/v1/badges/me", cookies=vol_cookies)
        assert r.status_code == 200, r.text
        assert len(r.json()) >= 1
        print("✓ Badge auto-awarded:", r.json()[0]["badge"]["name"])

        # --- Check leaderboard ---
        r = await client.get("/api/v1/leaderboard", cookies=vol_cookies)
        assert r.status_code == 200, r.text
        assert any(e["user_id"] == vol_id for e in r.json())
        print("✓ Leaderboard includes volunteer")

        # --- Check notifications ---
        r = await client.get("/api/v1/notifications", cookies=vol_cookies)
        assert r.status_code == 200, r.text
        assert len(r.json()) >= 3  # registration confirmed, points awarded, badge earned
        print(f"✓ Notifications generated: {len(r.json())} notifications")

        # --- Admin dashboard ---
        r = await client.get("/api/v1/admin/dashboard", cookies=admin_cookies)
        assert r.status_code == 200, r.text
        print("✓ Admin dashboard:", r.json())

        # --- Analytics ---
        r = await client.get("/api/v1/analytics/attendance-rate", cookies=admin_cookies)
        assert r.status_code == 200, r.text
        print("✓ Analytics attendance rate:", r.json())

        r = await client.get("/api/v1/analytics/events-by-category", cookies=admin_cookies)
        assert r.status_code == 200, r.text
        print("✓ Analytics events by category:", r.json())

        print("\nALL SMOKE TESTS PASSED")

if __name__ == "__main__":
    asyncio.run(main())
