const values = [
  {
    icon: "diversity_3",
    title: "Community First",
    desc: "Every program starts with what dzongkhags and gewogs actually need, not what's easiest to run.",
  },
  {
    icon: "verified",
    title: "Transparent Impact",
    desc: "Hours, attendance, and points are tracked openly through the Point Bank so contributions are always visible.",
  },
  {
    icon: "self_improvement",
    title: "Volunteer Wellbeing",
    desc: "Spiritual guidance, group hikes, and mental wellness support exist because sustainable service starts with sustainable volunteers.",
  },
];

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-background px-margin-mobile md:px-margin-desktop py-xl">
      <div className="max-w-4xl mx-auto">
        <h1 className="font-display-lg text-headline-lg md:text-display-lg text-on-surface mb-xs text-center">
          About Hand On Support
        </h1>
        <p className="font-body-lg text-body-lg text-on-surface-variant mb-xl text-center max-w-2xl mx-auto">
          We connect volunteers across Bhutan with community service opportunities, and recognize
          every hour given through a transparent, gamified rewards system.
        </p>

        <div className="glass-card rounded-xl p-lg shadow-ambient mb-xl">
          <p className="font-headline-md text-headline-md text-on-surface mb-sm">Our mission</p>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Hand On Support exists to make it simple for anyone in Bhutan to find a meaningful way
            to serve their community — and to make sure that service is recognized. From
            riverside cleanups in Thimphu to donation drives in remote gewogs, we coordinate
            events, track attendance, and reward volunteers with points, badges, and public
            recognition through the Point Bank.
          </p>
        </div>

        <p className="font-headline-md text-headline-md text-on-surface mb-md text-center">
          What we stand for
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-md mb-xl">
          {values.map((value) => (
            <div
              key={value.title}
              className="glass-card rounded-xl p-md shadow-ambient shadow-ambient-hover transition-shadow"
            >
              <div className="w-11 h-11 rounded-full bg-primary-container flex items-center justify-center mb-sm">
                <span className="material-symbols-outlined text-primary text-2xl">
                  {value.icon}
                </span>
              </div>
              <p className="font-headline-md text-headline-md text-on-surface mb-xs">
                {value.title}
              </p>
              <p className="font-body-md text-sm text-on-surface-variant">{value.desc}</p>
            </div>
          ))}
        </div>

        <div className="text-center">
          <p className="font-body-md text-body-md text-on-surface-variant mb-sm">
            Curious how we&apos;re organized, or ready to find your first event?
          </p>
          <div className="flex items-center justify-center gap-sm flex-wrap">
            <a
              href="/organization"
              className="btn-secondary rounded-full px-md py-sm inline-flex items-center gap-xs"
            >
              <span className="material-symbols-outlined text-lg">account_tree</span>
              See our structure
            </a>
            <a
              href="/events"
              className="btn-primary rounded-full px-md py-sm inline-flex items-center gap-xs"
            >
              <span className="material-symbols-outlined text-lg">event</span>
              Browse events
            </a>
          </div>
        </div>
      </div>
    </main>
  );
}
