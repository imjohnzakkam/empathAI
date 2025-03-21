from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import base64
import io
import numpy as np
import json
import os
import soundfile as sf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules from our project
from models.emotion_detection.audio import AudioEmotionAnalyzer
from models.emotion_detection.text import TextEmotionAnalyzer
from knowledge_graph.graph import TherapeuticKnowledgeGraph
from response_generator.generator import ResponseGenerator

# Initialize FastAPI app
app = FastAPI(
    title="EmpathAI API",
    description="API for the EmpathAI therapy assistant system",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000", "*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
audio_analyzer = AudioEmotionAnalyzer()
text_analyzer = TextEmotionAnalyzer()
knowledge_graph = TherapeuticKnowledgeGraph()

# Get LLM configuration from environment variables
llm_provider = os.getenv("LLM_PROVIDER")
llm_model = os.getenv("LLM_MODEL")

# Initialize response generator with LLM configuration if available
response_generator = ResponseGenerator(llm_provider=llm_provider, llm_model=llm_model)

# Data models
class TextInput(BaseModel):
    text: str
    session_id: Optional[str] = None

class TextAnalysisResponse(BaseModel):
    detected_emotions: Dict[str, float]
    response_text: str
    session_id: Optional[str] = None

class EmotionAnalysisResponse(BaseModel):
    detected_emotions: Dict[str, float]
    session_id: Optional[str] = None

class MultimodalResponse(BaseModel):
    detected_emotions: dict
    response_text: str

class LLMConfigResponse(BaseModel):
    current_provider: Optional[str] = None
    current_model: Optional[str] = None
    available_providers: Dict[str, str]
    is_using_llm: bool

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"status": "ok", "message": "EmpathAI API is running"}

@app.get("/llm/config", response_model=LLMConfigResponse)
async def get_llm_config():
    """Get current LLM configuration"""
    return {
        "current_provider": response_generator.llm_provider,
        "current_model": response_generator.llm_model,
        "available_providers": ResponseGenerator.get_available_providers(),
        "is_using_llm": response_generator.use_llm
    }

@app.post("/analyze/text", response_model=TextAnalysisResponse)
async def analyze_text(input_data: TextInput):
    try:
        # Analyze emotions in text
        emotions = text_analyzer.analyze(input_data.text)
        
        # Generate response using the emotion analysis
        response = response_generator.generate_response(input_data.text, emotions)
        
        return {
            "detected_emotions": emotions,
            "response_text": response,
            "session_id": input_data.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")

@app.post("/analyze/text/emotions", response_model=EmotionAnalysisResponse)
async def analyze_text_emotions(input_data: TextInput):
    try:
        # Only analyze emotions in text
        emotions = text_analyzer.analyze(input_data.text)
        
        return {
            "detected_emotions": emotions,
            "session_id": input_data.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing emotions in text: {str(e)}")

@app.post("/analyze/audio", response_model=TextAnalysisResponse)
async def analyze_audio(
    audio_file: UploadFile = File(...),
    text: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None)
):
    """
    Analyze emotions in an audio recording and generate a therapeutic response.
    
    Args:
        audio_file: Audio recording
        text: Text content (optional)
        session_id: Session ID (optional)
        
    Returns:
        Detected emotions and therapeutic response
    """
    try:
        # Read audio file
        audio_content = await audio_file.read()
        audio_buffer = io.BytesIO(audio_content)
        audio_array, sample_rate = sf.read(audio_buffer)
        
        # Analyze audio emotions
        audio_emotions = audio_analyzer.analyze_audio(audio_array, sample_rate)
        
        # If text is provided, also analyze text emotions
        if text:
            text_emotions = text_analyzer.analyze(text)
            
            # Combine audio and text emotions
            combined_emotions = {}
            for emotion in set(list(audio_emotions.keys()) + list(text_emotions.keys())):
                audio_score = audio_emotions.get(emotion, 0)
                text_score = text_emotions.get(emotion, 0)
                # Weight text emotions more heavily (0.7) than audio (0.3)
                combined_emotions[emotion] = 0.3 * audio_score + 0.7 * text_score
        else:
            combined_emotions = audio_emotions
        
        # Generate response using the emotion analysis
        response = response_generator.generate_response(text or "", combined_emotions)
        
        return {
            "detected_emotions": combined_emotions,
            "response_text": response,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.post("/analyze/multimodal", response_model=MultimodalResponse)
async def analyze_multimodal(
    text: str = Form(...),
    audio_file: Optional[UploadFile] = File(None),
    user_id: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None)
):
    """
    Analyze emotions from multiple modalities and generate a therapeutic response.
    
    Args:
        text: Text content
        audio_file: Audio recording (optional)
        user_id: User ID (optional)
        session_id: Session ID (optional)
        
    Returns:
        Detected emotions and therapeutic response
    """
    if not text:
        raise HTTPException(status_code=400, detail="Text content is required")
    
    # Analyze text emotions
    text_emotions = text_analyzer.analyze(text)
    combined_emotions = text_emotions
    
    # If audio is provided, combine with audio emotions
    if audio_file:
        audio_bytes = await audio_file.read()
        
        try:
            with io.BytesIO(audio_bytes) as audio_io:
                audio_array, sample_rate = sf.read(audio_io)
                
            audio_emotions = audio_analyzer.analyze_audio(audio_array, sample_rate)
            
            # Combine text and audio emotions
            for emotion in audio_emotions:
                if emotion in combined_emotions:
                    # Weight text emotions more heavily (0.7) than audio (0.3)
                    combined_emotions[emotion] = 0.7 * combined_emotions[emotion] + 0.3 * audio_emotions[emotion]
                else:
                    combined_emotions[emotion] = 0.3 * audio_emotions[emotion]
        except Exception as e:
            # Log but continue with just text analysis
            print(f"Error processing audio: {str(e)}")
    
    # Get recommended therapeutic techniques
    recommended_techniques = knowledge_graph.get_techniques_for_emotions(combined_emotions)
    
    # Generate response
    response = response_generator.generate(
        text,
        combined_emotions,
        recommended_techniques,
        user_id,
        session_id
    )
    
    return {
        "detected_emotions": combined_emotions,
        "response_text": response
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=True) 