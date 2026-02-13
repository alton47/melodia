import type { Metadata } from "next";
import { Figtree } from "next/font/google";
import Sidebar from "@/components/Sidebar"; // Ensure this path matches your file location
import "./globals.css";

const figtree = Figtree({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Melodia",
  description: "A Spotify clone..",
  icons: {
    icon: [
      {
        url: "/favicon.svg",
        type: "image/svg+xml",
      },
    ],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${figtree.className} antialiased`}>
        <Sidebar>{children}</Sidebar>
      </body>
    </html>
  );
}
