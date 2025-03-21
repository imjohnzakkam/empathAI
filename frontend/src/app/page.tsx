'use client';

import { useState } from 'react';
import Header from '@/components/ui/Header';
import TherapySession from '@/components/therapy/TherapySession';
import EmotionVisualizer from '@/components/emotion/EmotionVisualizer';
import { motion } from 'framer-motion';

export default function Home() {
  const [sessionActive, setSessionActive] = useState<boolean>(false);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <div className="flex-grow px-4 py-10 sm:px-6 lg:px-8">
        {!sessionActive ? (
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
                onClick={() => setSessionActive(true)}
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
          </motion.div>
        ) : (
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <TherapySession setSessionActive={setSessionActive} />
              </div>
              <div className="lg:col-span-1">
                <EmotionVisualizer />
              </div>
            </div>
          </div>
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