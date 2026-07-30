"use client";

import Link from "next/link";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRegister } from "@/lib/hooks/use-auth";

const registerSchema = z.object({
  full_name: z.string().min(2, "Enter your full name"),
  email: z.string().email("Enter a valid email address"),
  phone_number: z.string().optional(),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type RegisterForm = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const registerUser = useRegister();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>({ resolver: zodResolver(registerSchema) });

  return (
    <main className="min-h-screen bg-background py-16 px-4 text-foreground sm:px-6 lg:px-8">
      <div className="container mx-auto grid gap-12 lg:grid-cols-[1fr_420px] lg:items-center">
        <section className="space-y-6">
          <span className="inline-flex rounded-full bg-primary-container/15 px-4 py-2 text-sm font-semibold text-primary">
            Start your journey
          </span>
          <h1 className="max-w-3xl text-4xl font-bold leading-tight text-on-surface sm:text-5xl">
            Become a volunteer with Hand On Support.
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-on-surface-variant">
            Create an account to discover meaningful events, earn Point Bank rewards, and help strengthen Bhutan&apos;s local communities.
          </p>
        </section>

        <section className="rounded-[32px] border border-outline-variant bg-white p-8 shadow-ambient">
          <div className="mb-8 space-y-2 text-center">
            <h2 className="text-2xl font-semibold text-on-surface">Create your account</h2>
            <p className="text-sm leading-6 text-on-surface-variant">
              Secure your profile and start volunteering today.
            </p>
          </div>

          <form className="space-y-5" onSubmit={handleSubmit((data) => registerUser.mutate(data))}>
            <div className="space-y-2">
              <Label htmlFor="full_name">Full name</Label>
              <Input id="full_name" placeholder="Tashi Wangmo" {...register("full_name")} />
              {errors.full_name && (
                <p className="text-sm text-destructive">{errors.full_name.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="you@example.com" {...register("email")} />
              {errors.email && <p className="text-sm text-destructive">{errors.email.message}</p>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone_number">Phone number (optional)</Label>
              <Input id="phone_number" placeholder="17123456" {...register("phone_number")} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" {...register("password")} />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>

            {registerUser.isError && (
              <p className="text-sm text-destructive">
                Could not create your account. That email may already be registered.
              </p>
            )}

            <Button type="submit" className="w-full rounded-full py-3" disabled={registerUser.isPending}>
              {registerUser.isPending ? "Creating account…" : "Create account"}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-on-surface-variant">
            Already have an account?{
}
