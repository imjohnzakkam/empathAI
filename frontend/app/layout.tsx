import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "EmpathAI - Therapeutic AI Assistant",
  description: "Advanced AI system that combines visual emotion recognition, voice tone analysis, and natural language processing to provide personalized therapeutic support.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main className="min-h-screen bg-gradient-to-b from-blue-50 to-indigo-100">
          {children}
        </main>
      </body>
    </html>
  );
}
