'use client';

import React from 'react';
import TherapySession from './TherapySession';

interface TherapyContainerProps {
  setSessionActive: (active: boolean) => void;
}

const TherapyContainer: React.FC<TherapyContainerProps> = ({ setSessionActive }) => {
  return (
    <div className="h-screen max-w-6xl mx-auto">
      {/* TherapySession now contains the EmotionVisualizer component directly */}
      <TherapySession setSessionActive={setSessionActive} />
    </div>
  );
};

export default TherapyContainer; 