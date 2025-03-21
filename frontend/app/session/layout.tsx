'use client';

import Header from '@/components/ui/Header';

export default function SessionLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <div className="flex-grow px-4 py-10 sm:px-6 lg:px-8">
        {children}
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