'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface EmotionData {
  emotion: string;
  percentage: number;
  color: string;
}

const EmotionVisualizer = () => {
  const [emotions, setEmotions] = useState<EmotionData[]>([
    { emotion: 'Neutral', percentage: 65, color: '#4F46E5' },
    { emotion: 'Happy', percentage: 15, color: '#10B981' },
    { emotion: 'Sad', percentage: 10, color: '#6B7280' },
    { emotion: 'Angry', percentage: 5, color: '#EF4444' },
    { emotion: 'Surprised', percentage: 5, color: '#F59E0B' },
  ]);
  
  const [dominantEmotion, setDominantEmotion] = useState<string>('Neutral');
  const [therapyTips, setTherapyTips] = useState<string[]>([
    'Take deep breaths to calm your nervous system',
    'Try mindfulness meditation for 5 minutes',
    'Express your feelings through creative outlets'
  ]);

  // In a real implementation, this would update based on API responses
  useEffect(() => {
    const timer = setInterval(() => {
      const mockEmotion: EmotionData[] = [
        { 
          emotion: 'Neutral', 
          percentage: Math.floor(Math.random() * 30) + 45, 
          color: '#4F46E5' 
        },
        { 
          emotion: 'Happy', 
          percentage: Math.floor(Math.random() * 20) + 5, 
          color: '#10B981' 
        },
        { 
          emotion: 'Sad', 
          percentage: Math.floor(Math.random() * 15) + 5, 
          color: '#6B7280' 
        },
        { 
          emotion: 'Angry', 
          percentage: Math.floor(Math.random() * 10), 
          color: '#EF4444' 
        },
        { 
          emotion: 'Surprised', 
          percentage: Math.floor(Math.random() * 10), 
          color: '#F59E0B' 
        },
      ];

      // Normalize to ensure total is 100%
      const total = mockEmotion.reduce((acc, curr) => acc + curr.percentage, 0);
      const normalizedEmotions = mockEmotion.map(emotion => ({
        ...emotion,
        percentage: Math.round((emotion.percentage / total) * 100)
      }));

      setEmotions(normalizedEmotions);
      
      // Update dominant emotion
      const dominant = normalizedEmotions.reduce((prev, current) => 
        (prev.percentage > current.percentage) ? prev : current
      );
      setDominantEmotion(dominant.emotion);
      
    }, 3000); // Update every 3 seconds
    
    return () => clearInterval(timer);
  }, []);

  const getEmotionIcon = (emotion: string) => {
    switch (emotion.toLowerCase()) {
      case 'happy':
        return '😊';
      case 'sad':
        return '😢';
      case 'angry':
        return '😠';
      case 'surprised':
        return '😲';
      case 'neutral':
      default:
        return '😐';
    }
  };

  return (
    <div className="flex flex-col h-full card">
      <div className="p-4 border-b">
        <h2 className="text-xl font-semibold text-gray-900">Emotion Analysis</h2>
        <p className="text-sm text-gray-500 mt-1">Real-time emotional state detection</p>
      </div>
      
      <div className="p-4">
        <div className="flex items-center justify-center mb-6">
          <motion.div 
            className="text-6xl"
            key={dominantEmotion}
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          >
            {getEmotionIcon(dominantEmotion)}
          </motion.div>
        </div>
        
        <h3 className="text-center text-lg font-medium text-gray-900 mb-4">
          Dominant Emotion: <span className="font-bold">{dominantEmotion}</span>
        </h3>
        
        <div className="space-y-4">
          {emotions.map((emotion) => (
            <div key={emotion.emotion} className="space-y-1">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">
                  {emotion.emotion}
                </span>
                <span className="text-sm font-medium text-gray-900">
                  {emotion.percentage}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <motion.div
                  className="h-2.5 rounded-full"
                  style={{ backgroundColor: emotion.color }}
                  initial={{ width: 0 }}
                  animate={{ width: `${emotion.percentage}%` }}
                  transition={{ duration: 1 }}
                ></motion.div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="mt-6 p-4 border-t">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Suggested Techniques</h3>
        <ul className="space-y-2">
          {therapyTips.map((tip, index) => (
            <motion.li 
              key={index}
              className="flex items-start"
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <span className="inline-flex items-center justify-center w-6 h-6 mr-2 bg-indigo-100 text-indigo-800 rounded-full flex-shrink-0">
                {index + 1}
              </span>
              <span className="text-gray-700">{tip}</span>
            </motion.li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default EmotionVisualizer; 