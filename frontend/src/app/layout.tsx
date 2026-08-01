import type { Metadata } from "next";
import { Inter, Montserrat } from "next/font/google";
import "./globals.css";
import { QueryProvider } from "@/components/providers/query-provider";
import { Toaster } from "@/components/providers/toast-provider";
import { Shell } from "@/components/layout/shell";
import { UnauthorizedBanner } from "@/components/layout/unauthorized-banner";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-body",
  display: "swap",
  weight: ["400", "500", "600"],
});

const montserrat = Montserrat({
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
  weight: ["400", "600", "700"],
});

export const metadata: Metadata = {
  title: "Hand On Support | Volunteer Management, Bhutan",
  description:
    "Connect volunteers with community service opportunities across Bhutan and earn rewards through the Point Bank.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${inter.variable} ${montserrat.variable}`}>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased min-h-screen bg-background text-foreground">
        <QueryProvider>
          <Shell>
            <UnauthorizedBanner />
            {children}
          </Shell>
          {/* Global toast outlet — any component can call `toast()` and it
              renders here. Mounted inside QueryProvider so mutation
              callbacks can fire toasts freely. */}
          <Toaster />
        </QueryProvider>
      </body>
    </html>
  );
}
