const divisions = [
  { name: "Finance", icon: "account_balance", desc: "Budgeting, grants, and financial transparency." },
  { name: "Wellness", icon: "self_improvement", desc: "Mental health and community wellbeing programs." },
  { name: "Communications", icon: "campaign", desc: "Outreach, media, and public storytelling." },
  { name: "Volunteer Ops", icon: "groups", desc: "Recruitment, training, and event coordination." },
  { name: "Digital & Data", icon: "database", desc: "Point Bank systems and platform engineering." },
  { name: "Community Relations", icon: "diversity_3", desc: "Local dzongkhag partnerships and liaison work." },
];

export default function OrganizationPage() {
  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-5xl mx-auto">
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-xs text-center">
          Organization Structure
        </h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant mb-xl text-center max-w-2xl mx-auto">
          A clear, accountable leadership structure supporting every volunteer and community
          initiative.
        </p>

        {/* Tree layout */}
        <div className="flex flex-col items-center gap-md">
          {/* Root: Leadership */}
          <div className="glass-card rounded-xl px-lg py-md shadow-ambient flex items-center gap-sm">
            <span className="material-symbols-outlined text-primary text-3xl">star</span>
            <div>
              <p className="font-headline-md text-headline-md text-on-surface">Executive Leadership</p>
              <p className="font-body-md text-sm text-on-surface-variant">Board & Director</p>
            </div>
          </div>

          {/* Connector */}
          <div className="w-0.5 h-8 bg-outline-variant" />

          {/* Divisions row */}
          <div className="w-full">
            <div className="relative">
              <div className="hidden md:block absolute top-0 left-[8.33%] right-[8.33%] h-0.5 bg-outline-variant" />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-md pt-md">
                {divisions.map((d) => (
                  <div key={d.name} className="flex flex-col items-center">
                    <div className="hidden md:block w-0.5 h-4 bg-outline-variant -mt-md mb-0" />
                    <div className="glass-card rounded-xl p-md shadow-ambient shadow-ambient-hover transition-shadow w-full text-center">
                      <div className="w-14 h-14 mx-auto rounded-full bg-primary-container/20 flex items-center justify-center mb-sm">
                        <span className="material-symbols-outlined text-primary text-2xl">{d.icon}</span>
                      </div>
                      <p className="font-headline-md text-headline-md text-on-surface mb-xs">{d.name}</p>
                      <p className="font-body-md text-sm text-on-surface-variant">{d.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <p className="text-center font-body-md text-sm text-on-surface-variant mt-xl">
          Interested in leading a division near you?{" "}
          <a href="/register" className="text-primary font-semibold hover:underline">
            Join the movement
          </a>
          .
        </p>
      </div>
    </main>
  );
}
