export interface Emotion {
  name: string;
  color: string;
  icon: string;
  description: string;
}

export const emotionColors = {
  happy: '#10B981', // green
  sad: '#6B7280', // gray
  angry: '#EF4444', // red
  disgust: '#8B5CF6', // purple
  fear: '#7C3AED', // violet
  surprise: '#F59E0B', // amber
  neutral: '#4F46E5', // indigo
};

export const emotions: Record<string, Emotion> = {
  happy: {
    name: 'Happy',
    color: emotionColors.happy,
    icon: '😊',
    description: 'Feeling joy, contentment, or satisfaction'
  },
  sad: {
    name: 'Sad',
    color: emotionColors.sad,
    icon: '😢',
    description: 'Feeling sorrow, unhappiness, or grief'
  },
  angry: {
    name: 'Angry',
    color: emotionColors.angry,
    icon: '😠',
    description: 'Feeling displeasure, hostility, or annoyance'
  },
  disgust: {
    name: 'Disgust',
    color: emotionColors.disgust,
    icon: '🤢',
    description: 'Feeling repulsion or profound disapproval'
  },
  fear: {
    name: 'Fear',
    color: emotionColors.fear,
    icon: '😨',
    description: 'Feeling anxiety, worry, or dread'
  },
  surprise: {
    name: 'Surprised',
    color: emotionColors.surprise,
    icon: '😲',
    description: 'Feeling astonishment or wonder'
  },
  neutral: {
    name: 'Neutral',
    color: emotionColors.neutral,
    icon: '😐',
    description: 'Feeling balanced, calm, or emotionally stable'
  }
};

export interface TherapyTechnique {
  id: string;
  name: string;
  description: string;
  forEmotions: string[];
  steps: string[];
}

export const therapyTechniques: TherapyTechnique[] = [
  {
    id: 'deep-breathing',
    name: 'Deep Breathing Exercise',
    description: 'A simple technique to reduce stress and anxiety by controlling your breath',
    forEmotions: ['angry', 'fear', 'sad', 'disgust'],
    steps: [
      'Find a comfortable position and close your eyes',
      'Breathe in slowly through your nose for a count of 4',
      'Hold your breath for a count of 2',
      'Exhale slowly through your mouth for a count of 6',
      'Repeat for 5-10 cycles'
    ]
  },
  {
    id: 'gratitude-practice',
    name: 'Gratitude Practice',
    description: 'Focusing on things you are grateful for to improve mood and perspective',
    forEmotions: ['sad', 'angry', 'disgust'],
    steps: [
      'Take a moment to reflect on your day',
      'Identify three things you are grateful for, no matter how small',
      'For each item, consider why you are grateful for it',
      'Notice how acknowledging these positives affects your mood'
    ]
  },
  {
    id: 'grounding-54321',
    name: '5-4-3-2-1 Grounding Technique',
    description: 'A sensory awareness exercise to manage anxiety and bring focus to the present',
    forEmotions: ['fear', 'angry', 'sad'],
    steps: [
      'Acknowledge 5 things you can see',
      'Acknowledge 4 things you can touch/feel',
      'Acknowledge 3 things you can hear',
      'Acknowledge 2 things you can smell',
      'Acknowledge 1 thing you can taste'
    ]
  },
  {
    id: 'positive-reframing',
    name: 'Positive Reframing',
    description: 'Changing perspective by finding the positive aspects in challenging situations',
    forEmotions: ['sad', 'fear', 'angry', 'disgust'],
    steps: [
      'Identify a negative thought or situation',
      'Challenge the thought: Is it entirely true? Are you seeing the whole picture?',
      'Find a more balanced or positive interpretation',
      'Focus on what you have learned or how you have grown from the experience'
    ]
  }
];

/**
 * Gets therapy techniques appropriate for a given emotion
 */
export const getTechniquesForEmotion = (emotionName: string): TherapyTechnique[] => {
  const emotion = emotionName.toLowerCase();
  return therapyTechniques.filter(technique => 
    technique.forEmotions.includes(emotion)
  );
};

/**
 * Formats emotion data from API response for visualization
 */
export const formatEmotionData = (emotions: Record<string, number>) => {
  return Object.entries(emotions).map(([emotion, value]) => {
    const normalizedEmotion = emotion.toLowerCase();
    // Get color from our defined colors or use neutral as fallback
    const color = normalizedEmotion in emotionColors 
      ? emotionColors[normalizedEmotion as keyof typeof emotionColors] 
      : emotionColors.neutral;
    
    return {
      emotion: emotion,
      percentage: Math.round(value * 100),
      color: color
    };
  });
};

/**
 * Gets the dominant emotion from a set of emotions
 */
export const getDominantEmotion = (emotions: Record<string, number>): string => {
  let maxScore = 0;
  let dominant = 'neutral';
  
  Object.entries(emotions).forEach(([emotion, score]) => {
    if (score > maxScore) {
      maxScore = score;
      dominant = emotion;
    }
  });
  
  return dominant;
}; 