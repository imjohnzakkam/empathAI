'use client';

import { useState } from 'react';
import Header from '@/components/ui/Header';
import HomePage from '@/components/home/HomePage';
import TherapyContainer from '@/components/therapy/TherapyContainer';

export default function Home() {
  const [sessionActive, setSessionActive] = useState<boolean>(false);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <div className="flex-grow px-4 py-10 sm:px-6 lg:px-8">
        {!sessionActive ? (
          <HomePage onStartSession={() => setSessionActive(true)} />
        ) : (
          <TherapyContainer setSessionActive={setSessionActive} />
        )}
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
