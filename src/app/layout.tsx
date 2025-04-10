import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { ViewTransitions } from "next-view-transitions";
import type { Metadata } from "next";
import { Analytics } from "@vercel/analytics/react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Sandon Lai",
  description: "Sandon Lai's personal website",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ViewTransitions>
      <html lang="en">
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[#1b1b1b] max-w-2xl mx-auto px-4 selection:bg-sky-300 selection:text-sky-900`}
        >
          <Header />
          {children}
          <Footer />
          <Analytics />
        </body>
      </html>
    </ViewTransitions>
  );
}
