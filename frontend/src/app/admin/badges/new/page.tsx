"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { isAxiosError } from "axios";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { useCreateBadge } from "@/lib/hooks/use-rewards";

const criteriaTypes = [
  { value: "events_attended", label: "Events attended (count of present attendance)" },
  { value: "points_earned", label: "Points earned (lifetime point balance)" },
] as const;

const badgeSchema = z.object({
  name: z.string().min(1, "Name is required").max(100, "Name is too long"),
  description: z.string().min(1, "Description is required"),
  icon: z.string().min(1, "Pick an icon or emoji"),
  criteria_type: z.enum(["events_attended", "points_earned"]),
  criteria_value: z.preprocess(
    (val) => (val === "" || val === undefined ? undefined : Number(val)),
    z.number().int().positive("Threshold must be a positive number"),
  ),
});

type BadgeForm = z.infer<typeof badgeSchema>;

export default function NewBadgePage() {
  const router = useRouter();
  const createBadge = useCreateBadge();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<BadgeForm>({
    resolver: zodResolver(badgeSchema),
    defaultValues: { icon: "🏅", criteria_type: "events_attended" },
  });

  const onSubmit = handleSubmit(async (data) => {
    await createBadge.mutateAsync(data);
    router.push("/admin/badges");
  });

  const serverError = isAxiosError(createBadge.error)
    ? (createBadge.error.response?.data?.detail as string | undefined)
    : undefined;

  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-2xl mx-auto">
        <Link
          href="/admin"
          className="inline-flex items-center gap-xs font-label-md text-label-md text-on-surface-variant hover:text-primary mb-md"
        >
          <span className="material-symbols-outlined text-lg">arrow_back</span>
          Back to dashboard
        </Link>

        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-lg">
          Create Badge
        </h1>

        <form onSubmit={onSubmit} className="glass-card rounded-xl p-md md:p-lg shadow-ambient space-y-md">
          <div className="grid gap-md sm:grid-cols-[80px_1fr]">
            <div className="space-y-xs">
              <Label htmlFor="icon">Icon</Label>
              <Input id="icon" className="text-center text-xl" maxLength={4} {...register("icon")} />
              {errors.icon && <p className="text-sm text-error">{errors.icon.message}</p>}
            </div>

            <div className="space-y-xs">
              <Label htmlFor="name">Name</Label>
              <Input id="name" placeholder="Community Champion" {...register("name")} />
              {errors.name && <p className="text-sm text-error">{errors.name.message}</p>}
            </div>
          </div>

          <div className="space-y-xs">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              rows={3}
              placeholder="Awarded for consistently showing up and making an impact…"
              {...register("description")}
            />
            {errors.description && (
              <p className="text-sm text-error">{errors.description.message}</p>
            )}
          </div>

          <div className="grid gap-md sm:grid-cols-2">
            <div className="space-y-xs">
              <Label htmlFor="criteria_type">Criteria type</Label>
              <Select id="criteria_type" {...register("criteria_type")}>
                {criteriaTypes.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label}
                  </option>
                ))}
              </Select>
            </div>

            <div className="space-y-xs">
              <Label htmlFor="criteria_value">Threshold</Label>
              <Input
                id="criteria_value"
                type="number"
                min={1}
                placeholder="e.g. 5"
                {...register("criteria_value")}
              />
              {errors.criteria_value && (
                <p className="text-sm text-error">{errors.criteria_value.message}</p>
              )}
            </div>
          </div>

          {createBadge.isError && (
            <p className="text-sm text-error">
              {serverError || "Could not create the badge. Please check the form and try again."}
            </p>
          )}

          <div className="flex items-center gap-sm pt-xs">
            <Button type="submit" disabled={createBadge.isPending}>
              {createBadge.isPending ? "Creating…" : "Create badge"}
            </Button>
            <Link href="/admin" className="font-label-md text-label-md text-on-surface-variant hover:text-primary">
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </main>
  );
}
