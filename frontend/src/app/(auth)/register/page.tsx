"use client";

import { useState } from "react";
import Link from "next/link";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";
import { apiClient } from "@/lib/api-client";
import { useRegister } from "@/lib/hooks/use-auth";

const registerSchema = z.object({
  full_name: z.string().min(2, "Enter your full name"),
  email: z.string().email("Enter a valid email address"),
  phone_number: z.string().optional(),
  password: z.string().min(8, "Password must be at least 8 characters"),
  dzongkhag: z.string().optional(),
  bio: z.string().optional(),
  agree: z.literal(true, {
    errorMap: () => ({ message: "You must accept the declaration to continue" }),
  }),
});

type RegisterForm = z.infer<typeof registerSchema>;

const dzongkhags = [
  "Thimphu",
  "Paro",
  "Punakha",
  "Wangdue Phodrang",
  "Bumthang",
  "Trongsa",
  "Mongar",
  "Trashigang",
  "Samdrup Jongkhar",
  "Chukha",
  "Haa",
  "Gasa",
  "Other",
];

const steps = [
  { key: "personal", label: "Personal Info", icon: "person" },
  { key: "address", label: "Address", icon: "location_on" },
  { key: "declaration", label: "Declaration", icon: "task_alt" },
] as const;

export default function RegisterPage() {
  const registerUser = useRegister();
  const [step, setStep] = useState(0);
  const {
    register,
    handleSubmit,
    trigger,
    formState: { errors },
  } = useForm<RegisterForm>({ resolver: zodResolver(registerSchema), mode: "onTouched" });

  const stepFields: Record<number, (keyof RegisterForm)[]> = {
    0: ["full_name", "email", "phone_number", "password"],
    1: ["dzongkhag", "bio"],
    2: ["agree"],
  };

  const goNext = async () => {
    const valid = await trigger(stepFields[step]);
    if (valid) setStep((s) => Math.min(s + 1, steps.length - 1));
  };

  const goBack = () => setStep((s) => Math.max(s - 1, 0));

  const onSubmit = handleSubmit(async (data) => {
    await registerUser.mutateAsync({
      email: data.email,
      password: data.password,
      full_name: data.full_name,
      phone_number: data.phone_number || undefined,
    });
    // Registration only accepts core auth fields; address/bio are saved as
    // a follow-up profile update once the session cookie is set.
    if (data.dzongkhag || data.bio) {
      await apiClient.put("/users/me", {
        dzongkhag: data.dzongkhag || undefined,
        bio: data.bio || undefined,
      });
    }
  });

  return (
    <div className="bg-surface-container-lowest rounded-xl shadow-ambient max-w-2xl w-full p-md md:p-lg border border-outline-variant">
      <div className="text-center mb-lg">
        <span className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-container text-on-primary-container mb-md">
          <span className="material-symbols-outlined text-3xl">volunteer_activism</span>
        </span>
        <h1 className="font-display-lg text-headline-lg text-on-surface mb-base">
          Join the Movement
        </h1>
        <p className="font-body-md text-body-md text-on-surface-variant">
          Register as a volunteer and start making an impact in Bhutan.
        </p>
      </div>

      {/* Progress indicator */}
      <div className="flex items-center justify-center gap-xs mb-lg">
        {steps.map((s, i) => (
          <div key={s.key} className="flex items-center gap-xs">
            <div
              className={cn(
                "flex items-center justify-center w-9 h-9 rounded-full font-label-md text-label-md transition-colors",
                i < step && "bg-primary-container text-on-primary-container",
                i === step && "bg-primary text-primary-foreground",
                i > step && "bg-surface-container text-on-surface-variant",
              )}
            >
              {i < step ? (
                <span className="material-symbols-outlined text-lg">check</span>
              ) : (
                <span className="material-symbols-outlined text-lg">{s.icon}</span>
              )}
            </div>
            <span
              className={cn(
                "hidden sm:block font-label-md text-label-md",
                i === step ? "text-on-surface" : "text-on-surface-variant",
              )}
            >
              {s.label}
            </span>
            {i < steps.length - 1 && (
              <div className={cn("w-6 sm:w-10 h-0.5 mx-xs", i < step ? "bg-primary-container" : "bg-surface-variant")} />
            )}
          </div>
        ))}
      </div>

      <form onSubmit={onSubmit} className="space-y-md">
        {step === 0 && (
          <div className="space-y-md">
            <div className="space-y-xs">
              <Label htmlFor="full_name">Full name</Label>
              <Input id="full_name" placeholder="Tashi Wangmo" {...register("full_name")} />
              {errors.full_name && <p className="text-sm text-error">{errors.full_name.message}</p>}
            </div>
            <div className="space-y-xs">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="you@example.com" {...register("email")} />
              {errors.email && <p className="text-sm text-error">{errors.email.message}</p>}
            </div>
            <div className="space-y-xs">
              <Label htmlFor="phone_number">Phone number (optional)</Label>
              <Input id="phone_number" placeholder="17123456" {...register("phone_number")} />
            </div>
            <div className="space-y-xs">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" {...register("password")} />
              {errors.password && <p className="text-sm text-error">{errors.password.message}</p>}
            </div>
          </div>
        )}

        {step === 1 && (
          <div className="space-y-md">
            <div className="space-y-xs">
              <Label htmlFor="dzongkhag">Dzongkhag (optional)</Label>
              <select
                id="dzongkhag"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-on-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                {...register("dzongkhag")}
              >
                <option value="">Select your dzongkhag</option>
                {dzongkhags.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>
            <div className="space-y-xs">
              <Label htmlFor="bio">A little about you (optional)</Label>
              <textarea
                id="bio"
                rows={4}
                placeholder="Tell us what causes you care about…"
                className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-on-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                {...register("bio")}
              />
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-md">
            <div className="rounded-lg border border-outline-variant bg-background p-md font-body-md text-body-md text-on-surface-variant leading-relaxed">
              By joining Hand On Support, I confirm the information I&apos;ve provided is accurate,
              and I agree to conduct myself respectfully at all community events, follow event
              organizer instructions, and represent the movement&apos;s values of unity and
              compassion.
            </div>
            <label className="flex items-start gap-sm cursor-pointer">
              <input type="checkbox" className="mt-1 h-4 w-4" {...register("agree")} />
              <span className="font-body-md text-body-md text-on-surface">
                I have read and agree to the declaration above.
              </span>
            </label>
            {errors.agree && <p className="text-sm text-error">{errors.agree.message}</p>}

            {registerUser.isError && (
              <p className="text-sm text-error">
                Could not create your account. That email may already be registered.
              </p>
            )}
          </div>
        )}

        <div className="flex items-center justify-between pt-md border-t border-surface-variant mt-lg">
          {step > 0 ? (
            <Button type="button" variant="outline" onClick={goBack}>
              Back
            </Button>
          ) : (
            <Link href="/login" className="font-label-md text-label-md text-on-surface-variant hover:text-primary">
              Already have an account?
            </Link>
          )}

          {step < steps.length - 1 ? (
            <Button type="button" onClick={goNext}>
              Next Step
              <span className="material-symbols-outlined text-sm ml-1">arrow_forward</span>
            </Button>
          ) : (
            <Button type="submit" disabled={registerUser.isPending}>
              {registerUser.isPending ? "Creating account…" : "Create account"}
            </Button>
          )}
        </div>
      </form>
    </div>
  );
}
