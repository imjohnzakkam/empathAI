'use client';

import Header from '@/components/ui/Header';
import HomePage from '@/components/home/HomePage';

/**
 * Home page component for EmpathAI
 * 
 * This page displays the landing content with information about EmpathAI
 * and a demo of the emotion analysis feature.
 * 
 * When the user clicks "Start Therapy Session", the HomePage component
 * will generate a new UUID and redirect to /session/{uuid} using Next.js
 * dynamic routing. This creates a unique, shareable URL for each therapy session.
 */
export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <div className="flex-grow px-4 py-10 sm:px-6 lg:px-8">
        <HomePage />
      </div>

      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-6 px-4 overflow-hidden sm:px-6 lg:px-8">
          <p className="text-center text-gray-400 text-sm">
            &copy; {new Date().getFullYear()} EmpathAI. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
