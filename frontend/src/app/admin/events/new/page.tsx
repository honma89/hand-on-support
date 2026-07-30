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
import { useCreateEvent } from "@/lib/hooks/use-events";

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

const eventSchema = z
  .object({
    title: z
      .string()
      .min(3, "Title must be at least 3 characters")
      .max(200, "Title must be at most 200 characters"),
    description: z.string().min(1, "Description is required"),
    category: z.string().min(1, "Category is required").max(100),
    dzongkhag: z.string().min(1, "Dzongkhag is required"),
    location_detail: z.string().optional(),
    start_datetime: z.string().min(1, "Start date and time is required"),
    end_datetime: z.string().min(1, "End date and time is required"),
    capacity: z.preprocess(
      (val) => (val === "" || val === undefined ? undefined : Number(val)),
      z.number().int().positive("Capacity must be a positive number").optional(),
    ),
    points_reward: z.preprocess(
      (val) => (val === "" || val === undefined ? 10 : Number(val)),
      z.number().int().min(0, "Points reward cannot be negative"),
    ),
    status: z.enum(["draft", "published"]),
    image_url: z.union([z.string().url("Enter a valid URL"), z.literal("")]).optional(),
  })
  .refine((data) => new Date(data.end_datetime) > new Date(data.start_datetime), {
    message: "End date/time must be after the start date/time",
    path: ["end_datetime"],
  });

type EventForm = z.infer<typeof eventSchema>;

export default function NewEventPage() {
  const router = useRouter();
  const createEvent = useCreateEvent();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<EventForm>({
    resolver: zodResolver(eventSchema),
    defaultValues: { status: "draft", points_reward: 10 },
  });

  const onSubmit = handleSubmit(async (data) => {
    await createEvent.mutateAsync({
      title: data.title,
      description: data.description,
      category: data.category,
      dzongkhag: data.dzongkhag,
      location_detail: data.location_detail || undefined,
      start_datetime: new Date(data.start_datetime).toISOString(),
      end_datetime: new Date(data.end_datetime).toISOString(),
      capacity: data.capacity,
      points_reward: data.points_reward,
      status: data.status,
      image_url: data.image_url || undefined,
    });
    router.push("/admin");
  });

  const serverError = isAxiosError(createEvent.error)
    ? (createEvent.error.response?.data?.detail as string | undefined)
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
          Create Event
        </h1>

        <form onSubmit={onSubmit} className="glass-card rounded-xl p-md md:p-lg shadow-ambient space-y-md">
          <div className="space-y-xs">
            <Label htmlFor="title">Title</Label>
            <Input id="title" placeholder="Riverside Cleanup Drive" {...register("title")} />
            {errors.title && <p className="text-sm text-error">{errors.title.message}</p>}
          </div>

          <div className="space-y-xs">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              rows={4}
              placeholder="Describe what volunteers will be doing…"
              {...register("description")}
            />
            {errors.description && (
              <p className="text-sm text-error">{errors.description.message}</p>
            )}
          </div>

          <div className="grid gap-md sm:grid-cols-2">
            <div className="space-y-xs">
              <Label htmlFor="category">Category</Label>
              <Input id="category" placeholder="Environment" {...register("category")} />
              {errors.category && <p className="text-sm text-error">{errors.category.message}</p>}
            </div>

            <div className="space-y-xs">
              <Label htmlFor="dzongkhag">Dzongkhag</Label>
              <Select id="dzongkhag" defaultValue="" {...register("dzongkhag")}>
                <option value="" disabled>
                  Select a dzongkhag
                </option>
                {dzongkhags.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </Select>
              {errors.dzongkhag && <p className="text-sm text-error">{errors.dzongkhag.message}</p>}
            </div>
          </div>

          <div className="space-y-xs">
            <Label htmlFor="location_detail">Location detail (optional)</Label>
            <Input
              id="location_detail"
              placeholder="Near Changlimithang Stadium"
              {...register("location_detail")}
            />
          </div>

          <div className="grid gap-md sm:grid-cols-2">
            <div className="space-y-xs">
              <Label htmlFor="start_datetime">Start date &amp; time</Label>
              <Input id="start_datetime" type="datetime-local" {...register("start_datetime")} />
              {errors.start_datetime && (
                <p className="text-sm text-error">{errors.start_datetime.message}</p>
              )}
            </div>

            <div className="space-y-xs">
              <Label htmlFor="end_datetime">End date &amp; time</Label>
              <Input id="end_datetime" type="datetime-local" {...register("end_datetime")} />
              {errors.end_datetime && (
                <p className="text-sm text-error">{errors.end_datetime.message}</p>
              )}
            </div>
          </div>

          <div className="grid gap-md sm:grid-cols-3">
            <div className="space-y-xs">
              <Label htmlFor="capacity">Capacity (optional)</Label>
              <Input id="capacity" type="number" min={1} placeholder="Unlimited" {...register("capacity")} />
              {errors.capacity && <p className="text-sm text-error">{errors.capacity.message}</p>}
            </div>

            <div className="space-y-xs">
              <Label htmlFor="points_reward">Points reward</Label>
              <Input id="points_reward" type="number" min={0} {...register("points_reward")} />
              {errors.points_reward && (
                <p className="text-sm text-error">{errors.points_reward.message}</p>
              )}
            </div>

            <div className="space-y-xs">
              <Label htmlFor="status">Status</Label>
              <Select id="status" {...register("status")}>
                <option value="draft">Draft</option>
                <option value="published">Published</option>
              </Select>
            </div>
          </div>

          <div className="space-y-xs">
            <Label htmlFor="image_url">Image URL (optional)</Label>
            <Input id="image_url" placeholder="https://…" {...register("image_url")} />
            {errors.image_url && <p className="text-sm text-error">{errors.image_url.message}</p>}
          </div>

          {createEvent.isError && (
            <p className="text-sm text-error">
              {serverError || "Could not create the event. Please check the form and try again."}
            </p>
          )}

          <div className="flex items-center gap-sm pt-xs">
            <Button type="submit" disabled={createEvent.isPending}>
              {createEvent.isPending ? "Creating…" : "Create event"}
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
