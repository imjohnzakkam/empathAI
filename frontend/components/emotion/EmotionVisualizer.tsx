'use client';

import { motion } from 'framer-motion';

interface EmotionData {
  emotion: string;
  percentage: number;
  color: string;
}

// Map of emotions to their corresponding colors
const EMOTION_COLORS: Record<string, string> = {
  happy: '#10B981',
  joy: '#10B981',
  sad: '#6B7280',
  sadness: '#6B7280',
  angry: '#EF4444',
  anger: '#EF4444',
  disgust: '#8B5CF6',
  fear: '#7C3AED',
  surprised: '#F59E0B',
  surprise: '#F59E0B',
  neutral: '#4F46E5',
  calm: '#4F46E5',
};

interface EmotionVisualizerProps {
  // Pass in the raw emotions from the API
  emotions?: Record<string, number>;
  // Optional flag to show the mock data instead
  useMockData?: boolean;
  // Show loading state
  isLoading?: boolean;
}

const EmotionVisualizer = ({
  emotions: rawEmotions,
  useMockData = false,
  isLoading = false,
}: EmotionVisualizerProps) => {
  // Set default emotions
  const defaultEmotions: EmotionData[] = [
    { emotion: 'Neutral', percentage: 65, color: '#4F46E5' },
    { emotion: 'Happy', percentage: 15, color: '#10B981' },
    { emotion: 'Sad', percentage: 10, color: '#6B7280' },
    { emotion: 'Angry', percentage: 5, color: '#EF4444' },
    { emotion: 'Surprised', percentage: 5, color: '#F59E0B' },
  ];
  
  // Format the raw emotions for display
  const formatEmotions = (rawData?: Record<string, number>): EmotionData[] => {
    console.log("Formatting emotions from:", rawData);
    
    if (!rawData || Object.keys(rawData).length === 0) {
      console.log("No valid emotion data, using defaults");
      return defaultEmotions;
    }
    
    try {
      const formatted = Object.entries(rawData)
        .map(([emotion, value]) => {
          console.log(`Processing emotion: ${emotion} with value: ${value}`);
          return {
            emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1), // Capitalize
            percentage: Math.round(value * 100),
            color: EMOTION_COLORS[emotion.toLowerCase()] || '#4F46E5',
          };
        })
        .sort((a, b) => b.percentage - a.percentage)
        .slice(0, 5);
      
      console.log("Formatted emotions:", formatted);
      return formatted.length > 0 ? formatted : defaultEmotions;
    } catch (error) {
      console.error("Error formatting emotions:", error);
      return defaultEmotions;
    }
  };
  
  // Get the current emotions to display
  const displayEmotions = useMockData ? defaultEmotions : formatEmotions(rawEmotions);
  
  // Determine the dominant emotion
  const dominantEmotion = displayEmotions[0]?.emotion || 'Neutral';
  
  // Get therapy tips based on the dominant emotion
  const getTherapyTips = (emotion: string): string[] => {
    const emotionTips: Record<string, string[]> = {
      Neutral: [
        'Practice regular mindfulness meditation',
        'Set goals for personal growth',
        'Engage in activities that bring you peace'
      ],
      Happy: [
        'Journal about what brought you joy today',
        'Share your positive feelings with others',
        'Build on this energy to tackle challenges'
      ],
      Sad: [
        'Allow yourself to feel without judgment',
        'Connect with a supportive friend or family member',
        'Try gentle physical activity like walking'
      ],
      Angry: [
        'Take deep breaths to calm your nervous system',
        'Try counting to 10 before responding',
        'Channel the energy into productive activities'
      ],
      Fear: [
        'Ground yourself by naming 5 things you can see',
        'Challenge catastrophic thinking patterns',
        'Practice progressive muscle relaxation'
      ],
      Surprised: [
        'Take a moment to process the unexpected',
        'Consider different perspectives of the situation',
        'Adapt your plans as needed'
      ],
      Disgust: [
        'Identify the specific trigger for your feeling',
        'Practice acceptance of uncomfortable emotions',
        'Reframe your thinking about the situation'
      ]
    };
    
    return emotionTips[emotion] || emotionTips['Neutral'];
  };
  
  const therapyTips = getTherapyTips(dominantEmotion);
  
  const getEmotionIcon = (emotion: string) => {
    switch (emotion.toLowerCase()) {
      case 'happy':
      case 'joy':
        return '😊';
      case 'sad':
      case 'sadness':
        return '😢';
      case 'angry':
      case 'anger':
        return '😠';
      case 'surprised':
      case 'surprise':
        return '😲';
      case 'fear':
        return '😨';
      case 'disgust':
        return '🤢';
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
        
        {isLoading ? (
          <div className="flex justify-center items-center h-40">
            <div className="flex space-x-2">
              <div className="w-2 h-2 rounded-full bg-indigo-600 animate-bounce"></div>
              <div className="w-2 h-2 rounded-full bg-indigo-600 animate-bounce delay-100"></div>
              <div className="w-2 h-2 rounded-full bg-indigo-600 animate-bounce delay-200"></div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {displayEmotions.map((emotion) => (
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
        )}
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