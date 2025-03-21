import logging
import re
import os
from pathlib import Path
from collections import Counter
import json

# Using langchain for improved text analysis
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class EmotionAnalysisResult(BaseModel):
    emotions: Dict[str, float] = Field(description="Emotions detected with confidence scores")
    dominant_emotion: str = Field(description="The most dominant emotion detected")
    explanation: str = Field(description="Brief explanation of the emotional analysis")

class TextEmotionAnalyzer:
    """
    Class for analyzing emotions from text input using LangChain.
    """
    
    # Emotion categories
    EMOTIONS = ["anger", "disgust", "fear", "joy", "sadness", "surprise", "neutral"]
    
    # Simple emotion keyword dictionary for fallback
    EMOTION_KEYWORDS = {
        "anger": ["angry", "mad", "furious", "annoyed", "irritated", "enraged", "frustrated"],
        "disgust": ["disgusted", "gross", "revolting", "repulsed", "sickened", "appalled"],
        "fear": ["afraid", "scared", "terrified", "anxious", "worried", "frightened", "nervous"],
        "joy": ["happy", "joyful", "delighted", "pleased", "glad", "excited", "thrilled", "content"],
        "sadness": ["sad", "depressed", "unhappy", "miserable", "gloomy", "heartbroken", "upset"],
        "surprise": ["surprised", "shocked", "astonished", "amazed", "stunned", "speechless"],
        "neutral": ["okay", "fine", "neutral", "indifferent", "balanced", "stable"]
    }
    
    def __init__(self):
        """
        Initialize the text emotion analyzer with LangChain components.
        """
        self.logger = logging.getLogger(__name__)
        self.confidence = 0.0
        
        # Check if OpenAI API key is available
        self.openai_available = "OPENAI_API_KEY" in os.environ
        
        if self.openai_available:
            # Initialize LangChain components
            self.initialize_langchain()
        else:
            self.logger.warning("OpenAI API key not found. Falling back to keyword-based analysis.")
            
    def initialize_langchain(self):
        """Initialize LangChain components for emotion analysis"""
        # Create output parser
        self.parser = PydanticOutputParser(pydantic_object=EmotionAnalysisResult)
        
        # Create prompt template
        template = """
        Analyze the emotional content of the following text and determine the emotions present.
        
        Text: {text}
        
        Identify the emotions present in the text from this list: {emotions}.
        Assign a confidence score (0.0-1.0) to each detected emotion.
        
        {format_instructions}
        """
        
        self.prompt = PromptTemplate(
            input_variables=["text", "emotions"],
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
    
    def _keyword_based_analysis(self, text):
        """
        Analyze text using keyword matching as a fallback method.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary of emotions and their confidence scores
        """
        text = text.lower()
        
        # Count occurrences of emotion keywords
        emotion_counts = {emotion: 0 for emotion in self.EMOTIONS}
        
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            for keyword in keywords:
                # Match whole words
                matches = re.findall(r'\b' + keyword + r'\b', text)
                emotion_counts[emotion] += len(matches)
        
        # If no emotions were detected, default to neutral
        if sum(emotion_counts.values()) == 0:
            emotion_counts["neutral"] = 1
        
        # Normalize to get confidence values
        total_counts = sum(emotion_counts.values())
        if total_counts > 0:
            emotion_scores = {emotion: count / total_counts for emotion, count in emotion_counts.items()}
        else:
            emotion_scores = {emotion: 0.0 for emotion in self.EMOTIONS}
            emotion_scores["neutral"] = 1.0
            
        return emotion_scores
            
    def analyze(self, text):
        """
        Analyze the emotional content of text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with detected emotions and their confidence scores
        """
        if not text.strip():
            # Empty text, return neutral
            self.confidence = 1.0
            return {"neutral": 1.0}
        
        try:
            if self.openai_available:
                # Use LangChain for analysis
                result = self.chain.run(text=text, emotions=", ".join(self.EMOTIONS))
                parsed_result = self.parser.parse(result)
                self.confidence = max(parsed_result.emotions.values()) if parsed_result.emotions else 0.5
                return parsed_result.emotions
            else:
                # Fallback to keyword-based analysis
                emotion_scores = self._keyword_based_analysis(text)
                self.confidence = max(emotion_scores.values())
                return emotion_scores
                
        except Exception as e:
            self.logger.error(f"Error in text emotion analysis: {e}")
            # Fallback to simple keyword analysis
            emotion_scores = self._keyword_based_analysis(text)
            self.confidence = 0.5  # Lower confidence for fallback
            return emotion_scores
    
    def get_confidence(self):
        """
        Return the confidence level of the last analysis.
        
        Returns:
            Float value representing confidence (0.0-1.0)
        """
        return self.confidence 