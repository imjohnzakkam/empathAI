'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaMicrophone, FaMicrophoneSlash, FaPaperPlane, FaArrowLeft } from 'react-icons/fa';
import axios from 'axios';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  emotions?: Record<string, number>;
}

interface TherapySessionProps {
  setSessionActive: (active: boolean) => void;
}

const TherapySession: React.FC<TherapySessionProps> = ({ setSessionActive }) => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', text: "Hello, I'm your empathetic AI assistant. How are you feeling today?", sender: 'ai' }
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [loading, setLoading] = useState(false);
  
  const audioRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<BlobPart[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Handle recording start/stop
  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording
      audioRecorderRef.current?.stop();
      setIsRecording(false);
    } else {
      try {
        // Start new recording
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        
        recorder.ondataavailable = (e) => {
          audioChunksRef.current.push(e.data);
        };
        
        recorder.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
          setAudioBlob(audioBlob);
          audioChunksRef.current = [];
          
          // Stop all tracks on the stream to release the microphone
          stream.getTracks().forEach(track => track.stop());
        };
        
        audioRecorderRef.current = recorder;
        audioChunksRef.current = [];
        recorder.start();
        setIsRecording(true);
      } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Could not access your microphone. Please check permissions.');
      }
    }
  };
  
  // Send user message and get AI response
  const sendMessage = async () => {
    if ((!inputText.trim() && !audioBlob) || loading) return;
    
    const newMessage: Message = {
      id: Date.now().toString(),
      text: inputText.trim(),
      sender: 'user'
    };
    
    setMessages(prev => [...prev, newMessage]);
    setInputText('');
    setLoading(true);
    
    try {
      let response;
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      if (audioBlob) {
        // Send both audio and text (if available)
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'recording.wav');
        if (inputText.trim()) {
          formData.append('text', inputText.trim());
        }
        
        response = await axios.post(`${apiUrl}/analyze/audio`, formData);
        setAudioBlob(null);
      } else {
        // Send just text
        response = await axios.post(`${apiUrl}/analyze/text`, {
          text: inputText.trim()
        });
      }
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.response_text,
        sender: 'ai',
        emotions: response.data.detected_emotions
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error getting response:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, I couldn't process your message. Please try again.",
        sender: 'ai'
      };
      setMessages(prev => [...prev, errorMessage]);
    }
    
    setLoading(false);
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };
  
  return (
    <div className="flex flex-col h-[calc(100vh-200px)] card">
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center">
          <button 
            onClick={() => setSessionActive(false)}
            className="mr-4 text-gray-500 hover:text-gray-700"
          >
            <FaArrowLeft />
          </button>
          <h2 className="text-xl font-semibold text-gray-900">Therapy Session</h2>
        </div>
      </div>

      <div className="flex-grow overflow-y-auto p-4 space-y-4">
        {messages.map(message => (
          <div 
            key={message.id} 
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`max-w-xs md:max-w-md rounded-lg p-3 ${
                message.sender === 'user' 
                  ? 'bg-indigo-600 text-white rounded-br-none' 
                  : 'bg-white shadow rounded-bl-none'
              }`}
            >
              {message.text}
              
              {/* Display emotions if available */}
              {message.emotions && (
                <div className="mt-2 pt-2 border-t border-indigo-200 text-xs text-indigo-200">
                  <div className="font-semibold">Detected emotions:</div>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {Object.entries(message.emotions)
                      .sort((a, b) => b[1] - a[1])
                      .slice(0, 3)
                      .map(([emotion, score]) => (
                        <span 
                          key={emotion} 
                          className="px-2 py-1 rounded-full bg-indigo-700"
                        >
                          {emotion}: {Math.round(score * 100)}%
                        </span>
                      ))
                    }
                  </div>
                </div>
              )}
            </motion.div>
          </div>
        ))}
        <div ref={messagesEndRef} />
        
        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-start">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-white shadow rounded-lg p-3"
            >
              <div className="flex space-x-2">
                <div className="w-2 h-2 rounded-full bg-indigo-600 animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-indigo-600 animate-bounce delay-100"></div>
                <div className="w-2 h-2 rounded-full bg-indigo-600 animate-bounce delay-200"></div>
              </div>
            </motion.div>
          </div>
        )}
      </div>
      
      <div className="p-4 border-t">
        <div className="flex items-center space-x-2">
          <button 
            onClick={toggleRecording}
            className={`p-3 rounded-full ${isRecording ? 'bg-red-500 text-white' : 'bg-gray-200 text-gray-600'}`}
          >
            {isRecording ? <FaMicrophoneSlash /> : <FaMicrophone />}
          </button>
          
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            rows={1}
          />
          
          <button 
            onClick={sendMessage}
            disabled={loading || (!inputText.trim() && !audioBlob)}
            className={`p-3 rounded-full ${
              loading || (!inputText.trim() && !audioBlob) 
                ? 'bg-gray-200 text-gray-400' 
                : 'bg-indigo-600 text-white hover:bg-indigo-700'
            }`}
          >
            <FaPaperPlane />
          </button>
        </div>
        
        {audioBlob && (
          <div className="mt-2 p-2 bg-green-100 text-green-800 rounded-lg text-sm">
            Audio recording ready to send! {inputText.trim() && '(Will be sent with your text)'}
          </div>
        )}
      </div>
    </div>
  );
};

export default TherapySession; 