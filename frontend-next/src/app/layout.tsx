import type { Metadata } from "next";
import "./globals.css";
import "./mobile.css";
import { AppShell } from "./app-shell";
import { GlassFilter } from "@/components/glass-filter";
import { LangProvider } from "@/lib/language";

export const metadata: Metadata = {
  title: "Trinetra Agro AI \u2014 Vision Beyond the Fields",
  description:
    "AI-powered agricultural intelligence platform for Indian farmers. Crop recommendations, disease detection, market forecasting, and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased" suppressHydrationWarning>
      <head>
        <style>{`
          @keyframes bgScroll {
            from { background-position: center bottom; }
            to { background-position: center top; }
          }
        `}</style>
      </head>
      <body className="min-h-screen font-sans" style={{
        fontFamily: "Inter, system-ui, sans-serif",
      }}>
        <GlassFilter />
        <LangProvider>
          <AppShell>{children}</AppShell>
        </LangProvider>
      </body>
    </html>
  );
}
