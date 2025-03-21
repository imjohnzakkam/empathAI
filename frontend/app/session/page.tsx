'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { v4 as uuidv4 } from 'uuid';

export default function SessionRedirectPage() {
  const router = useRouter();
  
  // Generate a new UUID and redirect to the session page
  useEffect(() => {
    const sessionId = uuidv4();
    router.push(`/session/${sessionId}`);
  }, [router]);

  // Show a loading message while redirecting
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Creating your therapy session...</h1>
        <div className="flex justify-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-indigo-600 animate-bounce"></div>
          <div className="w-3 h-3 rounded-full bg-indigo-600 animate-bounce delay-100"></div>
          <div className="w-3 h-3 rounded-full bg-indigo-600 animate-bounce delay-200"></div>
        </div>
      </div>
    </div>
  );
} 