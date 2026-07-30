These two migrations (`17d747ed40f3` initial_migration -> `11131b566373`
rename_password_column) were the original migration chain from the
`tashi-feature`/main org-schema branch before it was rebased onto the
async core's `e74810f03c36` baseline via `f3a91c7b2e4d`. They are superseded
and archived here (not deleted) purely for reference. Leaving them in
`alembic/versions/` causes Alembic to see two unrelated heads and refuse
to run `alembic upgrade head`.
