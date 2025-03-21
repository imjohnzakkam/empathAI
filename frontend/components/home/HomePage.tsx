'use client';

import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { debounce } from 'lodash';
import EmotionVisualizer from '../emotion/EmotionVisualizer';

interface HomePageProps {
  onStartSession: () => void;
}

const HomePage: React.FC<HomePageProps> = ({ onStartSession }) => {
  const [demoText, setDemoText] = useState<string>('');
  const [emotions, setEmotions] = useState<Record<string, number>>({
    "neutral": 0.9,
    "calm": 0.1
  });
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  // Debounced function for real-time emotion analysis
  const analyzeEmotions = useRef(
    debounce(async (text: string) => {
      if (!text.trim()) {
        setEmotions({
          "neutral": 0.9,
          "calm": 0.1
        });
        setIsAnalyzing(false);
        return;
      }
      
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await axios.post(`${apiUrl}/analyze/text/emotions`, {
          text: text.trim()
        });
        
        setEmotions(response.data.detected_emotions);
      } catch (error) {
        console.error('Error analyzing emotions:', error);
        // Fall back to default emotions if the analysis fails
        setEmotions({
          "neutral": 0.9,
          "calm": 0.1
        });
      }
      
      setIsAnalyzing(false);
    }, 500)
  ).current;
  
  // Handle text input change for real-time emotion analysis
  const handleDemoTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value;
    setDemoText(text);
    
    // Analyze emotions in real-time
    if (text.trim()) {
      setIsAnalyzing(true);
      analyzeEmotions(text);
    } else {
      setEmotions({
        "neutral": 0.9,
        "calm": 0.1
      });
    }
  };

  return (
    <motion.div 
      className="max-w-3xl mx-auto text-center"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
        <span className="block">Welcome to</span>
        <span className="block text-indigo-600">EmpathAI</span>
      </h1>
      <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
        An advanced AI therapeutic support system that understands your emotions through facial expressions, voice tone, and language.
      </p>
      <div className="mt-10">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="btn-primary text-lg px-8 py-3"
          onClick={onStartSession}
        >
          Start Therapy Session
        </motion.button>
      </div>

      <div className="mt-20 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <div className="card">
          <div className="h-12 w-12 rounded-md bg-indigo-500 flex items-center justify-center mx-auto">
            <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="mt-5 text-lg font-medium text-gray-900 text-center">Visual Emotion Recognition</h3>
          <p className="mt-2 text-sm text-gray-500">
            Advanced computer vision algorithms detect emotions from your facial expressions in real-time.
          </p>
        </div>

        <div className="card">
          <div className="h-12 w-12 rounded-md bg-indigo-500 flex items-center justify-center mx-auto">
            <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </div>
          <h3 className="mt-5 text-lg font-medium text-gray-900 text-center">Voice Tone Analysis</h3>
          <p className="mt-2 text-sm text-gray-500">
            Sophisticated audio processing identifies emotional cues in your voice during conversation.
          </p>
        </div>

        <div className="card">
          <div className="h-12 w-12 rounded-md bg-indigo-500 flex items-center justify-center mx-auto">
            <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <h3 className="mt-5 text-lg font-medium text-gray-900 text-center">Natural Language Processing</h3>
          <p className="mt-2 text-sm text-gray-500">
            Advanced NLP models understand the emotional context of your messages to provide personalized responses.
          </p>
        </div>
      </div>

      {/* Demo section */}
      <div className="mt-20">
        <h2 className="text-2xl font-bold text-gray-900">Try the Emotion Analyzer</h2>
        <p className="mt-3 text-gray-500">
          Type a message below to see how our AI detects emotions in real-time
        </p>
        
        <div className="mt-6 max-w-xl mx-auto">
          <textarea
            value={demoText}
            onChange={handleDemoTextChange}
            placeholder="How are you feeling today? Type something to analyze emotions..."
            className="w-full h-24 p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
          
          <div className="mt-6 h-96 bg-white rounded-lg shadow-sm overflow-hidden">
            <EmotionVisualizer emotions={emotions} isLoading={isAnalyzing} />
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default HomePage; 