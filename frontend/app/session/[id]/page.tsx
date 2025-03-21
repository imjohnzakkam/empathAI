'use client';

import { useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { v4 as uuidv4 } from 'uuid';
import TherapySession from '@/components/therapy/TherapySession';

export default function SessionPage() {
  const router = useRouter();
  const params = useParams();
  const sessionId = params.id as string;
  
  // Validate that the session ID is a valid UUID
  useEffect(() => {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(sessionId)) {
      console.error('Invalid session ID');
      router.push('/');
    }
  }, [sessionId, router]);
  
  const handleEndSession = () => {
    router.push('/');
  };

  return (
    <div className="h-screen max-w-6xl mx-auto">
      <TherapySession 
        sessionId={sessionId}
        setSessionActive={() => handleEndSession()} 
      />
    </div>
  );
} 