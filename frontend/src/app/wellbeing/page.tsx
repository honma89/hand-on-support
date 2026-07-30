const wellbeingCards = [
  {
    title: "Spiritual Guidance",
    icon: "self_improvement",
    desc: "Connect with monastic mentors and quiet reflection spaces to find calm and perspective between volunteer shifts.",
    image:
      "https://images.unsplash.com/photo-1716783184813-e34403516ada?w=1000&q=80&auto=format&fit=crop",
    cta: "Request a session",
    href: "/wellbeing/spiritual-guidance",
  },
  {
    title: "Group Hiking",
    icon: "hiking",
    desc: "Join fellow volunteers on scenic trails across the dzongkhags — a chance to unwind, connect, and recharge together.",
    image:
      "https://images.unsplash.com/photo-1689825422854-8e3083c2fb82?w=1000&q=80&auto=format&fit=crop",
    cta: "See upcoming hikes",
    href: "/events?category=hiking",
  },
  {
    title: "Mental Wellness",
    icon: "psychology",
    desc: "Confidential counseling, guided breathing exercises, and peer support circles for volunteers who need someone to talk to.",
    image:
      "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=1000&q=80&auto=format&fit=crop",
    cta: "Get support",
    href: "/wellbeing/mental-wellness",
  },
];

export default function WellbeingPage() {
  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-5xl mx-auto">
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-xs text-center">
          Wellbeing
        </h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant mb-xl text-center max-w-2xl mx-auto">
          Volunteering asks a lot of you. These programs exist so you have somewhere to turn when
          you need rest, community, or a moment of stillness.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-md">
          {wellbeingCards.map((card) => (
            <div
              key={card.title}
              className="glass-card rounded-xl overflow-hidden shadow-ambient shadow-ambient-hover transition-shadow flex flex-col"
            >
              <div className="relative h-44 w-full">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={card.image}
                  alt={card.title}
                  className="h-full w-full object-cover"
                />
                <div className="absolute bottom-3 left-3 w-11 h-11 rounded-full bg-primary-container/90 flex items-center justify-center shadow-ambient">
                  <span className="material-symbols-outlined text-primary text-2xl">
                    {card.icon}
                  </span>
                </div>
              </div>

              <div className="p-md flex flex-col flex-1">
                <p className="font-headline-md text-headline-md text-on-surface mb-xs">
                  {card.title}
                </p>
                <p className="font-body-md text-sm text-on-surface-variant mb-md flex-1">
                  {card.desc}
                </p>
                <a
                  href={card.href}
                  className="btn-primary rounded-full px-md py-sm text-center font-label-md text-label-md inline-flex items-center justify-center gap-xs"
                >
                  {card.cta}
                  <span className="material-symbols-outlined text-lg">arrow_forward</span>
                </a>
              </div>
            </div>
          ))}
        </div>

        <p className="text-center font-body-md text-sm text-on-surface-variant mt-xl">
          Need something not listed here?{" "}
          <a href="/notifications" className="text-primary font-semibold hover:underline">
            Reach out to your program coordinator
          </a>
          .
        </p>
      </div>
    </main>
  );
}
