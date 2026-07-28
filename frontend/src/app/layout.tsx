import type { Metadata } from "next";
import "./globals.css";
import { QueryProvider } from "@/components/providers/query-provider";

export const metadata: Metadata = {
  title: "Hand On Support | Volunteer Management, Bhutan",
  description:
    "Connect volunteers with community service opportunities across Bhutan and earn rewards through the Point Bank.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen">
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
