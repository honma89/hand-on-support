export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-[calc(100vh-5rem)] flex items-center justify-center py-lg px-margin-mobile md:px-margin-desktop bg-background">
      {children}
    </div>
  );
}
