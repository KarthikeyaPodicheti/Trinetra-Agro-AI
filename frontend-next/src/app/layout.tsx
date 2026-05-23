import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "./app-shell";

export const metadata: Metadata = {
  title: "Trinetra Agro AI — Vision Beyond the Fields",
  description:
    "AI-powered agricultural intelligence platform for Indian farmers. Crop recommendations, disease detection, market forecasting, and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-screen font-sans" style={{ fontFamily: "Inter, system-ui, sans-serif" }}>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
