import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CuraPulse AI | Grounded Healthcare Intelligence",
  description:
    "Explore trusted, literature-grounded clinical knowledge with the CuraPulse AI assistant.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
