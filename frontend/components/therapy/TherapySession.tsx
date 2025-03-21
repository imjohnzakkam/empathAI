'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaMicrophone, FaMicrophoneSlash, FaPaperPlane, FaArrowLeft } from 'react-icons/fa';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { debounce } from 'lodash';
import EmotionVisualizer from '../emotion/EmotionVisualizer';

interface Message {
    id: string;
    text: string;
    sender: 'user' | 'ai';
    emotions?: Record<string, number>;
}

interface TextAnalysisPayload {
    text: string;
    session_id?: string;
}

interface LLMConfig {
    current_provider: string | null;
    current_model: string | null;
    is_using_llm: boolean;
}

interface TherapySessionProps {
    setSessionActive: (active: boolean) => void;
    onEmotionsUpdate?: (emotions: Record<string, number>) => void;
    onAnalyzingStateChange?: (isAnalyzing: boolean) => void;
    sessionId?: string;
}

const TherapySession: React.FC<TherapySessionProps> = ({ 
    setSessionActive,
    onEmotionsUpdate,
    onAnalyzingStateChange,
    sessionId
}) => {
    const [messages, setMessages] = useState<Message[]>([
        { id: '1', text: "Hello, I'm your empathetic AI assistant. How are you feeling today?", sender: 'ai' }
    ]);
    const [inputText, setInputText] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
    const [loading, setLoading] = useState(false);
    const [llmConfig, setLlmConfig] = useState<LLMConfig | null>(null);
    const [currentEmotions, setCurrentEmotions] = useState<Record<string, number>>({
        "neutral": 0.9,
        "calm": 0.1
    });
    const [isAnalyzingEmotions, setIsAnalyzingEmotions] = useState(false);
    
    const audioRecorderRef = useRef<MediaRecorder | null>(null);
    const audioChunksRef = useRef<BlobPart[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    
    // Auto-scroll to the latest message
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);
    
    // Update parent component with emotion state changes
    useEffect(() => {
        if (onEmotionsUpdate) {
            console.log("Sending emotions update to parent:", currentEmotions);
            onEmotionsUpdate(currentEmotions);
        }
    }, [currentEmotions, onEmotionsUpdate]);
    
    useEffect(() => {
        if (onAnalyzingStateChange) {
            onAnalyzingStateChange(isAnalyzingEmotions);
        }
    }, [isAnalyzingEmotions, onAnalyzingStateChange]);
    
    // Fetch LLM configuration
    useEffect(() => {
        const fetchLLMConfig = async () => {
            try {
                const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
                const response = await axios.get(`${apiUrl}/llm/config`);
                setLlmConfig(response.data);
            } catch (error) {
                console.error('Error fetching LLM config:', error);
            }
        };
        
        fetchLLMConfig();
    }, []);
    
    // Debounced function for real-time emotion analysis
    // eslint-disable-next-line react-hooks/exhaustive-deps
    const analyzeEmotions = useRef(
        debounce(async (text: string) => {
            if (!text.trim()) {
                const defaultEmotions = {
                    "neutral": 0.9,
                    "calm": 0.1
                };
                console.log("Setting default emotions due to empty text:", defaultEmotions);
                setCurrentEmotions(defaultEmotions);
                setIsAnalyzingEmotions(false);
                return;
            }
            
            try {
                console.log("Analyzing emotions for text:", text.trim().substring(0, 50) + "...");
                const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
                const response = await axios.post(`${apiUrl}/analyze/text/emotions`, {
                    text: text.trim()
                });
                
                console.log("Received emotion analysis response:", response.data);
                
                if (response.data && response.data.detected_emotions) {
                    const detectedEmotions = response.data.detected_emotions;
                    console.log("Setting detected emotions:", detectedEmotions);
                    
                    // Force update by creating a new object
                    const newEmotions = { ...detectedEmotions };
                    
                    // Ensure we have at least one emotion
                    if (Object.keys(newEmotions).length === 0) {
                        newEmotions.neutral = 1.0;
                    }
                    
                    setCurrentEmotions(newEmotions);
                } else {
                    console.warn("Invalid emotion data from API:", response.data);
                    // Fall back to default emotions if the analysis fails
                    setCurrentEmotions({
                        "neutral": 0.9,
                        "calm": 0.1
                    });
                }
            } catch (error) {
                console.error("Error analyzing emotions:", error);
                // Fall back to default emotions if the analysis fails
                setCurrentEmotions({
                    "neutral": 0.9,
                    "calm": 0.1
                });
            }
            
            setIsAnalyzingEmotions(false);
        }, 500)
    ).current;
    
    // Handle text input change for real-time emotion analysis
    const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const text = e.target.value;
        setInputText(text);
        
        // Analyze emotions in real-time
        if (text.trim()) {
            setIsAnalyzingEmotions(true);
            analyzeEmotions(text);
        } else {
            setCurrentEmotions({
                "neutral": 0.9,
                "calm": 0.1
            });
        }
    };
    
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
                // Add session ID if available
                if (sessionId) {
                    formData.append('session_id', sessionId);
                }
                
                response = await axios.post(`${apiUrl}/analyze/audio`, formData);
                setAudioBlob(null);
            } else {
                // Send just text
                const payload: TextAnalysisPayload = {
                    text: inputText.trim()
                };
                
                // Add session ID if available
                if (sessionId) {
                    payload.session_id = sessionId;
                }
                
                response = await axios.post(`${apiUrl}/analyze/text`, payload);
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
    
    // Log session ID on component mount
    useEffect(() => {
        if (sessionId) {
            console.log(`Therapy session initialized with ID: ${sessionId}`);
            
            // Here you could load previous messages if this is a returning session
            // For example:
            // loadPreviousMessages(sessionId);
        }
    }, [sessionId]);
    
    return (
        <div className="flex flex-col h-full bg-gray-50">
            {/* Header */}
            <div className="flex items-center p-4 bg-gradient-to-r from-purple-600 to-indigo-700 text-white">
                <button className="mr-4" onClick={() => setSessionActive(false)}>
                    <FaArrowLeft size={20} />
                </button>
                <h1 className="text-xl font-bold">EmpathAI Therapy Session</h1>
                {llmConfig && llmConfig.is_using_llm && (
                    <div className="ml-auto text-xs bg-indigo-800 px-2 py-1 rounded">
                        Powered by: {llmConfig.current_provider?.toUpperCase()} • {llmConfig.current_model}
                    </div>
                )}
            </div>
            
            {/* Main content area with chat */}
            <div className="flex-1 overflow-hidden flex">
                {/* Chat area - reduced width on desktop */}
                <div className="h-full overflow-y-auto p-4 space-y-4 w-full md:w-2/3">
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
                                {message.sender === 'user' ? (
                                    message.text
                                ) : (
                                    <div className="prose prose-sm max-w-none prose-headings:text-indigo-800 prose-a:text-indigo-600">
                                        <ReactMarkdown 
                                            remarkPlugins={[remarkGfm]}
                                            components={{
                                                // Override styling for specific markdown elements
                                                a: (props) => <a {...props} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer" />,
                                                p: (props) => <p {...props} className="mb-2" />,
                                                ul: (props) => <ul {...props} className="list-disc ml-4 mb-2" />,
                                                ol: (props) => <ol {...props} className="list-decimal ml-4 mb-2" />,
                                                h1: (props) => <h1 {...props} className="text-lg font-bold mb-2" />,
                                                h2: (props) => <h2 {...props} className="text-md font-bold mb-2" />,
                                                h3: (props) => <h3 {...props} className="font-bold mb-1" />,
                                                code: (props) => <code {...props} className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded" />,
                                                pre: (props) => <pre {...props} className="bg-gray-100 dark:bg-gray-800 p-2 rounded overflow-x-auto mb-2" />
                                            }}
                                        >
                                            {message.text}
                                        </ReactMarkdown>
                                    </div>
                                )}
                                
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
                    
                    {/* Emotion visualizer for mobile view - shown only on small screens */}
                    <div className="md:hidden mt-4">
                        <EmotionVisualizer 
                            emotions={currentEmotions} 
                            isLoading={isAnalyzingEmotions}
                        />
                    </div>
                </div>
                
                {/* Emotions panel - shown only on desktop */}
                <div className="hidden md:block w-1/3 h-full border-l border-gray-200 bg-white overflow-auto">
                    <EmotionVisualizer 
                        emotions={currentEmotions} 
                        isLoading={isAnalyzingEmotions}
                    />
                </div>
            </div>
            
            {/* Input area */}
            <div className="p-4 border-t border-gray-200 bg-white">
                {/* Test buttons for debugging */}
                {/* <div className="flex mb-2 gap-2 justify-end">
                    <button 
                        onClick={() => setCurrentEmotions({ "happy": 0.8, "surprised": 0.2 })}
                        className="bg-green-500 text-white px-2 py-1 text-xs rounded"
                    >
                        Test Happy
                    </button>
                    <button 
                        onClick={() => setCurrentEmotions({ "sad": 0.7, "fear": 0.3 })}
                        className="bg-blue-500 text-white px-2 py-1 text-xs rounded"
                    >
                        Test Sad
                    </button>
                    <button 
                        onClick={() => setCurrentEmotions({ "angry": 0.9, "disgust": 0.1 })}
                        className="bg-red-500 text-white px-2 py-1 text-xs rounded"
                    >
                        Test Angry
                    </button>
                </div> */}
                
                <div className="flex items-center space-x-2">
                    <button 
                        onClick={toggleRecording}
                        className={`p-3 rounded-full ${isRecording ? 'bg-red-500' : 'bg-gray-200'}`}
                    >
                        {isRecording ? <FaMicrophoneSlash color="white" /> : <FaMicrophone />}
                    </button>
                    
                    <textarea 
                        value={inputText}
                        onChange={handleTextChange}
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
                                ? 'bg-gray-200' 
                                : 'bg-indigo-600 hover:bg-indigo-700'
                        }`}
                    >
                        <FaPaperPlane color={loading || (!inputText.trim() && !audioBlob) ? 'gray' : 'white'} />
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