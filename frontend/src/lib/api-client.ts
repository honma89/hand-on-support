import axios from "axios";

/**
 * Shared HTTP client for all requests to the FastAPI backend.
 *
 * baseURL is "/api" (not the FastAPI origin directly) so the browser
 * always calls same-origin. In Docker Compose, Nginx forwards /api/*
 * to the backend container; in local dev, next.config.ts rewrites do
 * the same. This is what keeps the auth cookie flow (Module 1) simple
 * -- no cross-origin cookie gymnastics.
 *
 * withCredentials: true ensures HttpOnly auth cookies are sent/received.
 */
export const apiClient = axios.create({
  baseURL: "/api/v1",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});
