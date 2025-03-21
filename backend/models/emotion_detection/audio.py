import numpy as np
import librosa
import soundfile as sf
import io
import logging
from pathlib import Path
import os
import json
from typing import Dict, List, Optional

# Import LangChain components
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class AudioFeatures(BaseModel):
    """Features extracted from audio for emotion analysis"""
    mfcc_mean: List[float] = Field(description="Mean MFCC features")
    spectral_contrast_mean: List[float] = Field(description="Mean spectral contrast")
    chroma_mean: List[float] = Field(description="Mean chroma features")
    tempo: float = Field(description="Tempo of the audio")
    energy: float = Field(description="Energy level in the audio")

class AudioEmotionResult(BaseModel):
    emotions: Dict[str, float] = Field(description="Emotions detected with confidence scores")
    dominant_emotion: str = Field(description="The most dominant emotion detected")
    explanation: str = Field(description="Brief explanation of the emotional analysis")

class AudioEmotionAnalyzer:
    """
    Class for analyzing emotions from audio recordings using feature extraction
    and LangChain for analysis.
    """
    
    # Emotion labels
    EMOTIONS = ["angry", "calm", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
    
    def __init__(self):
        """
        Initialize the audio emotion analyzer.
        """
        self.logger = logging.getLogger(__name__)
        self.confidence = 0.0
        
        # Check if OpenAI API key is available
        self.openai_available = "OPENAI_API_KEY" in os.environ
        
        if self.openai_available:
            # Initialize LangChain components
            self.initialize_langchain()
        else:
            self.logger.warning("OpenAI API key not found. Falling back to rule-based analysis.")
    
    def initialize_langchain(self):
        """Initialize LangChain components for audio emotion analysis"""
        # Create output parser
        self.parser = PydanticOutputParser(pydantic_object=AudioEmotionResult)
        
        # Create prompt template
        template = """
        Analyze the audio features provided and determine the emotions present.
        
        Audio Features:
        - MFCC (Mel-frequency cepstral coefficients): {mfcc}
        - Spectral Contrast: {spectral_contrast}
        - Chroma: {chroma}
        - Tempo: {tempo}
        - Energy: {energy}
        
        Based on these features:
        - Higher energy and tempo often correlate with active emotions like anger or happiness
        - Lower energy often correlates with sadness or calmness
        - Spectral contrast helps distinguish between speech characteristics
        
        Identify the emotions present in the audio from this list: {emotions}.
        Assign a confidence score (0.0-1.0) to each detected emotion.
        
        {format_instructions}
        """
        
        self.prompt = PromptTemplate(
            input_variables=["mfcc", "spectral_contrast", "chroma", "tempo", "energy", "emotions"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
            template=template,
        )
        
        # Initialize LLM and chain
        try:
            self.llm = OpenAI(temperature=0)
            self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        except Exception as e:
            self.logger.error(f"Error initializing LangChain: {e}")
            self.openai_available = False
        
    def extract_features(self, audio_data, sample_rate=22050):
        """
        Extract audio features for emotion analysis.
        
        Args:
            audio_data: Audio data as a numpy array
            sample_rate: Sampling rate of the audio
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Handle mono/stereo conversion
        if len(audio_data.shape) > 1 and audio_data.shape[1] > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Extract MFCCs (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfccs, axis=1).tolist()
        
        # Extract spectral contrast
        spectral_contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sample_rate)
        features['spectral_contrast_mean'] = np.mean(spectral_contrast, axis=1).tolist()
        
        # Extract chroma features
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=sample_rate)
        features['chroma_mean'] = np.mean(chroma, axis=1).tolist()
        
        # Extract tempo
        onset_env = librosa.onset.onset_strength(y=audio_data, sr=sample_rate)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sample_rate)
        features['tempo'] = float(tempo[0])
        
        # Calculate energy
        features['energy'] = float(np.mean(np.abs(audio_data)))
        
        return features
    
    def rule_based_analysis(self, features):
        """
        Simple rule-based analysis of audio features as a fallback.
        
        Args:
            features: Dictionary of audio features
            
        Returns:
            Dictionary of emotion scores
        """
        # Default scores
        emotion_scores = {emotion: 0.1 for emotion in self.EMOTIONS}
        
        # Energy-based rules
        energy = features['energy']
        if energy > 0.1:
            emotion_scores['angry'] += 0.3
            emotion_scores['happy'] += 0.3
        else:
            emotion_scores['sad'] += 0.3
            emotion_scores['calm'] += 0.3
        
        # Tempo-based rules
        tempo = features['tempo']
        if tempo > 120:
            emotion_scores['happy'] += 0.2
            emotion_scores['surprise'] += 0.2
        elif tempo < 80:
            emotion_scores['sad'] += 0.2
            emotion_scores['calm'] += 0.2
        
        # Normalize scores
        total = sum(emotion_scores.values())
        emotion_scores = {k: v/total for k, v in emotion_scores.items()}
        
        return emotion_scores
    
    def analyze_audio(self, audio_data, sample_rate=22050):
        """
        Analyze emotions in audio data.
        
        Args:
            audio_data: Audio data as numpy array
            sample_rate: Sampling rate of the audio
            
        Returns:
            Dictionary of emotions and their confidence scores
        """
        try:
            # Extract features
            features = self.extract_features(audio_data, sample_rate)
            
            if self.openai_available:
                # Use LangChain for analysis
                result = self.chain.run(
                    mfcc=str(features['mfcc_mean']),
                    spectral_contrast=str(features['spectral_contrast_mean']),
                    chroma=str(features['chroma_mean']),
                    tempo=str(features['tempo']),
                    energy=str(features['energy']),
                    emotions=", ".join(self.EMOTIONS)
                )
                
                parsed_result = self.parser.parse(result)
                self.confidence = max(parsed_result.emotions.values()) if parsed_result.emotions else 0.5
                return parsed_result.emotions
            else:
                # Fallback to rule-based analysis
                emotion_scores = self.rule_based_analysis(features)
                self.confidence = max(emotion_scores.values())
                return emotion_scores
                
        except Exception as e:
            self.logger.error(f"Error in audio emotion analysis: {e}")
            # Return neutral as fallback
            self.confidence = 0.5
            return {"neutral": 1.0}
    
    def get_confidence(self):
        """
        Return the confidence level of the last analysis.
        
        Returns:
            Float value representing confidence (0.0-1.0)
        """
        return self.confidence 