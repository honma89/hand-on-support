import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // In local (non-Docker) dev, proxy /api/* straight to FastAPI so the
  // browser only ever talks to http://localhost:3000. In the Docker
  // Compose topology, Nginx handles this routing instead and this
  // rewrite simply won't be hit (Nginx intercepts /api/* first).
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.INTERNAL_API_URL ?? "http://localhost:8000"}/api/:path*`,
      },
      {
        source: "/uploads/:path*",
        destination: `${process.env.INTERNAL_API_URL ?? "http://localhost:8000"}/uploads/:path*`,
      },
    ];
  },
};

export default nextConfig;
