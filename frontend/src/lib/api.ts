import axios from 'axios';

// Define API base URL - would be set in environment variables in production
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Initialize axios instance with base config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for API responses
export interface EmotionAnalysisResponse {
  detected_emotions: {
    [key: string]: number;
  };
  response_text: string;
  suggested_techniques: string[];
  confidence_score: number;
}

// API functions
export const analyzeText = async (text: string, userId?: string, sessionId?: string) => {
  const response = await api.post<EmotionAnalysisResponse>('/analyze/text', {
    text,
    user_id: userId,
    session_id: sessionId,
  });
  return response.data;
};

export const analyzeImage = async (
  imageData: string, 
  text?: string,
  userId?: string, 
  sessionId?: string
) => {
  // Convert base64 image to file
  const blob = await fetch(imageData).then(res => res.blob());
  const file = new File([blob], 'webcam-image.jpg', { type: 'image/jpeg' });

  const formData = new FormData();
  formData.append('image', file);
  
  if (text) formData.append('text', text);
  if (userId) formData.append('user_id', userId);
  if (sessionId) formData.append('session_id', sessionId);

  const response = await api.post<EmotionAnalysisResponse>('/analyze/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const analyzeAudio = async (
  audioBlob: Blob,
  text?: string,
  userId?: string,
  sessionId?: string
) => {
  const file = new File([audioBlob], 'audio-recording.wav', { type: 'audio/wav' });
  
  const formData = new FormData();
  formData.append('audio', file);
  
  if (text) formData.append('text', text);
  if (userId) formData.append('user_id', userId);
  if (sessionId) formData.append('session_id', sessionId);

  const response = await api.post<EmotionAnalysisResponse>('/analyze/audio', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const analyzeMultimodal = async (
  text: string,
  imageData?: string,
  audioBlob?: Blob,
  userId?: string,
  sessionId?: string
) => {
  const formData = new FormData();
  formData.append('text', text);
  
  if (imageData) {
    const blob = await fetch(imageData).then(res => res.blob());
    const file = new File([blob], 'webcam-image.jpg', { type: 'image/jpeg' });
    formData.append('image', file);
  }
  
  if (audioBlob) {
    const file = new File([audioBlob], 'audio-recording.wav', { type: 'audio/wav' });
    formData.append('audio', file);
  }
  
  if (userId) formData.append('user_id', userId);
  if (sessionId) formData.append('session_id', sessionId);

  const response = await api.post<EmotionAnalysisResponse>('/analyze/multimodal', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export default api; 