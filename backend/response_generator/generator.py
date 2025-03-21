import logging
import random
import json
import os
from pathlib import Path
import requests
from typing import Dict, List, Optional, Union, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Provider Options
LLM_PROVIDERS = {
    "openai": "OpenAI API (requires key)",
    "huggingface": "HuggingFace Inference API (free tier available)",
    "ollama": "Ollama (local deployment)",
    "together_ai": "Together.ai (free tier available)",
    "google": "Google Gemini API (free tier available)",
    "anthropic": "Anthropic Claude (requires key)",
    "deepseek": "Deepseek API (requires key)",
    "openrouter": "OpenRouter API (access to multiple models)",
}

class ResponseGenerator:
    """
    Generates empathetic therapeutic responses based on detected emotions
    and recommended therapeutic techniques.
    """
    
    def __init__(self, templates_path=None, llm_provider=None, llm_model=None, api_key=None):
        """
        Initialize the response generator.
        
        Args:
            templates_path: Path to response templates file (optional)
            llm_provider: LLM provider to use (optional, defaults to template-based if None)
            llm_model: Specific LLM model to use (optional)
            api_key: API key for the LLM provider (optional)
        """
        self.logger = logging.getLogger(__name__)
        
        # Load response templates (for fallback)
        if templates_path and os.path.exists(templates_path):
            self.load_templates(templates_path)
        else:
            self.templates = self._create_default_templates()
            self.logger.info("Using default response templates")
        
        # LLM configuration
        self.llm_provider = llm_provider or os.getenv("LLM_PROVIDER")
        self.llm_model = llm_model or os.getenv("LLM_MODEL")
        self.api_key = api_key or os.getenv(f"{self.llm_provider.upper()}_API_KEY") if self.llm_provider else None
        
        # Check if LLM is properly configured
        self.use_llm = self.llm_provider is not None
        if self.use_llm:
            self.logger.info(f"Using {self.llm_provider} LLM for response generation")
        else:
            self.logger.info("Using template-based response generation (no LLM configured)")
    
    def _create_default_templates(self):
        """
        Create default response templates for different emotions and techniques.
        
        Returns:
            Dictionary of templates
        """
        templates = {
            # Emotion-specific greeting templates
            "greeting": {
                "anger": [
                    "I notice you seem frustrated right now.",
                    "It sounds like you're feeling angry about this situation.",
                    "I can sense some frustration in what you're expressing."
                ],
                "fear": [
                    "I notice you seem anxious or worried.",
                    "It sounds like this situation is causing you some fear.",
                    "I can tell you're feeling apprehensive about this."
                ],
                "sadness": [
                    "I notice you seem to be feeling down right now.",
                    "It sounds like you're going through a difficult time.",
                    "I can sense some sadness in what you're sharing."
                ],
                "joy": [
                    "I notice you're feeling positive about this!",
                    "It sounds like things are going well for you.",
                    "I can sense the enthusiasm in what you're sharing."
                ],
                "surprise": [
                    "This seems to have caught you off guard.",
                    "It sounds like this was unexpected for you.",
                    "I can tell you weren't anticipating this development."
                ],
                "disgust": [
                    "I notice this situation seems troubling to you.",
                    "It sounds like you're having a strong negative reaction to this.",
                    "I can tell this is something you find difficult to accept."
                ],
                "neutral": [
                    "I hear what you're saying.",
                    "Thank you for sharing this with me.",
                    "I understand what you're expressing."
                ]
            },
            
            # Validation templates
            "validation": {
                "anger": [
                    "It's completely natural to feel angry in this situation.",
                    "Your frustration makes a lot of sense given what you've described.",
                    "Many people would feel similarly in your position."
                ],
                "fear": [
                    "It's understandable to feel anxious about this.",
                    "This kind of worry is a natural response to uncertainty.",
                    "Your concerns are valid given what you're facing."
                ],
                "sadness": [
                    "It's okay to feel sad about this - it's a natural response.",
                    "What you're feeling is a normal reaction to loss or disappointment.",
                    "Many people would feel down in this situation."
                ],
                "joy": [
                    "It's wonderful that you're feeling good about this!",
                    "You have every reason to feel happy about this accomplishment.",
                    "Your positive feelings are well-deserved."
                ],
                "surprise": [
                    "It's natural to feel taken aback by unexpected changes.",
                    "Surprise can be disorienting, and that's completely normal.",
                    "It makes sense that you didn't see this coming."
                ],
                "disgust": [
                    "It's understandable to have such a strong reaction to this.",
                    "Many people would find this situation challenging.",
                    "Your response is a natural reaction to something that conflicts with your values."
                ],
                "neutral": [
                    "Thank you for sharing your perspective.",
                    "I appreciate you explaining how you see this situation.",
                    "It's helpful to understand your point of view."
                ]
            },
            
            # Technique introduction templates
            "technique_intro": [
                "Something that might help in this situation is {technique_name}.",
                "Many people find that {technique_name} can be beneficial when feeling this way.",
                "One approach that could be helpful is {technique_name}.",
                "Have you ever tried {technique_name}? It might be helpful.",
                "I'd like to suggest trying {technique_name}."
            ],
            
            # Technique description templates
            "technique_description": {
                "deep_breathing": [
                    "Take a slow, deep breath in through your nose for 4 counts, hold for 2, and exhale through your mouth for 6 counts. Repeat this several times while focusing on your breath.",
                    "Find a comfortable position and practice breathing deeply into your abdomen. Breathe in slowly through your nose, and out through your mouth, making your exhale longer than your inhale."
                ],
                "mindfulness": [
                    "Take a moment to notice five things you can see, four things you can touch, three things you can hear, two things you can smell, and one thing you can taste. This can help ground you in the present moment.",
                    "Set aside a few minutes to focus entirely on the present moment. Notice your surroundings, your bodily sensations, and your thoughts without judgment."
                ],
                "cognitive_reframing": [
                    "Consider if there might be another way to look at this situation. What would you say to a friend facing the same circumstances?",
                    "Try to identify any thought patterns that might be making you feel worse. Ask yourself if there's evidence for these thoughts, or if there might be a more balanced perspective."
                ],
                "gratitude": [
                    "Try taking a moment to think of three things you're grateful for today, no matter how small they might seem.",
                    "Consider keeping a gratitude journal where you write down a few things you appreciate each day. This can help shift focus toward positive aspects of your life."
                ],
                "progressive_relaxation": [
                    "Try tensing and then relaxing each muscle group in your body, starting from your toes and working up to your head. Hold the tension for 5 seconds before releasing.",
                    "Find a quiet place where you can lie down comfortably. Tense each muscle group for a few seconds, then release and notice the sensation of relaxation."
                ],
                "journal_writing": [
                    "Writing about your feelings can sometimes help process them. Try spending 10-15 minutes writing freely about your thoughts and emotions without worrying about grammar or structure.",
                    "Consider keeping a journal where you can express your thoughts and track patterns in your emotions over time."
                ],
                "positive_affirmation": [
                    "Try creating a simple, positive statement about yourself that you can repeat when you need encouragement, such as 'I am capable of handling challenges' or 'I am worthy of respect and care.'",
                    "Choose an affirmation that feels meaningful to you and repeat it to yourself several times, especially when facing difficult moments."
                ],
                "social_connection": [
                    "Consider reaching out to someone you trust to share how you're feeling. Even a brief conversation can sometimes help provide perspective.",
                    "Think about a supportive person in your life. How might connecting with them help you navigate this situation?"
                ],
                "physical_exercise": [
                    "Even a short walk or some gentle stretching can help shift your emotional state through the release of endorphins.",
                    "Consider engaging in some form of physical movement that you enjoy, whether that's dancing, yoga, running, or anything else that gets your body moving."
                ],
                "visualization": [
                    "Take a few minutes to close your eyes and imagine a peaceful place where you feel safe and calm. Notice the details in this place using all your senses.",
                    "Try visualizing yourself successfully navigating this challenge. What would that look like? How would you feel?"
                ]
            },
            
            # Follow-up question templates
            "follow_up": [
                "How does that suggestion sound to you?",
                "Would you be willing to try this approach?",
                "Does this resonate with what you're experiencing?",
                "What are your thoughts about this suggestion?",
                "Would you like to explore more techniques like this?"
            ],
            
            # Closing templates
            "closing": [
                "Remember that experiencing emotions is part of being human. Be gentle with yourself as you navigate this.",
                "I'm here to support you through this process whenever you need to talk.",
                "Take the time you need to process these feelings. Emotional well-being is a journey.",
                "Remember that seeking support is a sign of strength, not weakness.",
                "I hope these suggestions provide some help. Please let me know if there's anything else I can do to support you."
            ]
        }
        
        return templates
    
    def load_templates(self, path):
        """
        Load response templates from a file.
        
        Args:
            path: Path to templates file (JSON format)
        """
        try:
            with open(path, 'r') as f:
                self.templates = json.load(f)
            self.logger.info(f"Loaded response templates from {path}")
        except Exception as e:
            self.logger.error(f"Error loading templates: {str(e)}")
            self.templates = self._create_default_templates()
            self.logger.info("Created default templates as fallback")
    
    def _select_primary_emotion(self, emotions):
        """
        Select the primary emotion from the emotions dictionary.
        
        Args:
            emotions: Dictionary of emotions and their scores
            
        Returns:
            The emotion with the highest score
        """
        if not emotions:
            return "neutral"
            
        # Find emotion with highest score
        primary_emotion = max(emotions.items(), key=lambda x: x[1])
        
        # Map to our template categories
        emotion_name = primary_emotion[0].lower()
        
        # Map similar emotions to our template categories
        emotion_mapping = {
            "angry": "anger",
            "fury": "anger",
            "furious": "anger",
            "mad": "anger",
            "irritated": "anger",
            
            "anxious": "fear",
            "nervous": "fear",
            "worried": "fear",
            "scared": "fear",
            "terrified": "fear",
            "apprehensive": "fear",
            "stress": "fear",
            "stressed": "fear",
            
            "sad": "sadness",
            "depressed": "sadness",
            "unhappy": "sadness",
            "miserable": "sadness",
            "down": "sadness",
            "blue": "sadness",
            "grief": "sadness",
            "grieving": "sadness",
            
            "happy": "joy",
            "excited": "joy",
            "delighted": "joy",
            "pleased": "joy",
            "content": "joy",
            "joyful": "joy",
            
            "surprised": "surprise",
            "shocked": "surprise",
            "astonished": "surprise",
            "amazed": "surprise",
            
            "disgusted": "disgust",
            "repulsed": "disgust",
            "revolted": "disgust",
            
            "ok": "neutral",
            "okay": "neutral",
            "fine": "neutral",
            "calm": "neutral"
        }
        
        # Map to standard emotion categories
        if emotion_name in emotion_mapping:
            emotion_name = emotion_mapping[emotion_name]
            
        # If we don't have templates for this emotion, fall back to neutral
        if emotion_name not in self.templates["greeting"]:
            emotion_name = "neutral"
            
        return emotion_name
    
    def _get_technique_info(self, technique_id):
        """
        Get readable name and description for a technique ID.
        
        Args:
            technique_id: The technique identifier
            
        Returns:
            Tuple of (name, description)
        """
        # Default mappings in case we don't have specific data
        technique_names = {
            "deep_breathing": "Deep Breathing",
            "mindfulness": "Mindfulness Practice",
            "cognitive_reframing": "Cognitive Reframing",
            "gratitude": "Gratitude Practice",
            "progressive_relaxation": "Progressive Muscle Relaxation",
            "journal_writing": "Expressive Journal Writing",
            "positive_affirmation": "Positive Affirmations",
            "social_connection": "Social Connection",
            "physical_exercise": "Physical Activity",
            "visualization": "Positive Visualization"
        }
        
        # Get name from mapping or capitalize the ID if not found
        name = technique_names.get(
            technique_id, 
            technique_id.replace('_', ' ').title()
        )
        
        return name
    
    def _generate_with_openai(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using OpenAI API.
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            import openai
            
            # Set API key
            openai.api_key = self.api_key
            
            # Format emotions for prompt
            emotion_text = ", ".join([f"{emotion}: {score:.2f}" for emotion, score in emotions.items()])
            
            # Format techniques for prompt
            technique_text = ", ".join([self._get_technique_info(t) for t in techniques])
            
            # Construct system message
            system_message = f"""You are an empathetic AI therapeutic assistant. 
            Respond to the user's message with empathy, validation, and helpful suggestions.
            The user's primary emotions have been detected as: {emotion_text}
            Recommended therapeutic techniques: {technique_text}
            
            Your response should:
            1. Acknowledge and validate the user's emotions
            2. Offer 1-2 suggested techniques or approaches that might help
            3. End with a thoughtful question to continue the conversation
            
            Be warm, supportive, and professional. Avoid being overly cheerful for negative emotions.
            Keep your response concise (100-200 words).
            """
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=self.llm_model or "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": text}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error generating response with OpenAI: {str(e)}")
            return self._generate_with_templates(text, emotions, techniques)
    
    def _generate_with_huggingface(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using HuggingFace Inference API.
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            # Format emotions for prompt
            emotion_text = ", ".join([f"{emotion}: {score:.2f}" for emotion, score in emotions.items()])
            
            # Format techniques for prompt
            technique_text = ", ".join([self._get_technique_info(t) for t in techniques])
            
            # Construct prompt
            prompt = f"""You are an empathetic AI therapeutic assistant. 
            The user's message is: '{text}'
            Their primary emotions have been detected as: {emotion_text}
            Recommended therapeutic techniques: {technique_text}
            
            Respond with empathy, validation, and helpful suggestions. Your response should:
            1. Acknowledge and validate the user's emotions
            2. Offer 1-2 suggested techniques that might help
            3. End with a thoughtful question
            
            Your response:"""
            
            # API endpoint
            API_URL = f"https://api-inference.huggingface.co/models/{self.llm_model or 'mistralai/Mistral-7B-Instruct-v0.2'}"
            
            # Call HuggingFace API
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {"inputs": prompt, "parameters": {"max_length": 300, "temperature": 0.7}}
            
            response = requests.post(API_URL, headers=headers, json=payload)
            response_json = response.json()
            
            # Extract generated text
            if isinstance(response_json, list):
                return response_json[0].get("generated_text", "").replace(prompt, "").strip()
            else:
                return response_json.get("generated_text", "").replace(prompt, "").strip()
                
        except Exception as e:
            self.logger.error(f"Error generating response with HuggingFace: {str(e)}")
            return self._generate_with_templates(text, emotions, techniques)
    
    def _generate_with_ollama(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using local Ollama deployment.
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            # Format emotions for prompt
            emotion_text = ", ".join([f"{emotion}: {score:.2f}" for emotion, score in emotions.items()])
            
            # Format techniques for prompt
            technique_text = ", ".join([self._get_technique_info(t) for t in techniques])
            
            # Construct prompt
            prompt = f"""You are an empathetic AI therapeutic assistant. 
            The user's message is: '{text}'
            Their primary emotions have been detected as: {emotion_text}
            Recommended therapeutic techniques: {technique_text}
            
            Respond with empathy, validation, and helpful suggestions. Your response should:
            1. Acknowledge and validate the user's emotions
            2. Offer 1-2 suggested techniques that might help
            3. End with a thoughtful question
            
            Your response:"""
            
            # Ollama API endpoint (typically local)
            OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
            
            # Call Ollama API
            payload = {
                "model": self.llm_model or "llama2",
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(OLLAMA_API_URL, json=payload)
            response_json = response.json()
            
            return response_json.get("response", "").strip()
                
        except Exception as e:
            self.logger.error(f"Error generating response with Ollama: {str(e)}")
            return self._generate_with_templates(text, emotions, techniques)
    
    def _generate_with_together_ai(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using Together.ai API.
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            # Format emotions and techniques for prompt
            emotion_text = ", ".join([f"{emotion}: {score:.2f}" for emotion, score in emotions.items()])
            technique_text = ", ".join([self._get_technique_info(t) for t in techniques])
            
            # Construct prompt
            prompt = f"""<|im_start|>system
You are an empathetic AI therapeutic assistant. 
Respond to the user's message with empathy, validation, and helpful suggestions.
The user's primary emotions have been detected as: {emotion_text}
Recommended therapeutic techniques: {technique_text}

Your response should:
1. Acknowledge and validate the user's emotions
2. Offer 1-2 suggested techniques or approaches that might help
3. End with a thoughtful question to continue the conversation

Be warm, supportive, and professional. Avoid being overly cheerful for negative emotions.
Keep your response concise (100-200 words).<|im_end|>
<|im_start|>user
{text}<|im_end|>
<|im_start|>assistant
"""
            
            # API endpoint
            API_URL = "https://api.together.xyz/v1/completions"
            
            # Call Together.ai API
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "model": self.llm_model or "mistralai/Mistral-7B-Instruct-v0.2",
                "prompt": prompt,
                "max_tokens": 300,
                "temperature": 0.7,
                "stop": ["<|im_end|>"]
            }
            
            response = requests.post(API_URL, headers=headers, json=payload)
            response_json = response.json()
            
            return response_json.get("choices", [{}])[0].get("text", "").strip()
                
        except Exception as e:
            self.logger.error(f"Error generating response with Together.ai: {str(e)}")
            return self._generate_with_templates(text, emotions, techniques)
    
    def _generate_with_google(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using Google Gemini API.
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            import google.generativeai as genai
            
            # Configure the API
            genai.configure(api_key=self.api_key)
            
            # Format emotions and techniques for prompt
            emotion_text = ", ".join([f"{emotion}: {score:.2f}" for emotion, score in emotions.items()])
            technique_text = ", ".join([self._get_technique_info(t) for t in techniques])
            
            # Create the model
            model = genai.GenerativeModel(self.llm_model or 'gemini-pro')
            
            # Construct prompt
            prompt = f"""You are an empathetic AI therapeutic assistant. 
            The user's message is: '{text}'
            Their primary emotions have been detected as: {emotion_text}
            Recommended therapeutic techniques: {technique_text}
            
            Respond with empathy, validation, and helpful suggestions. Your response should:
            1. Acknowledge and validate the user's emotions
            2. Offer 1-2 suggested techniques that might help
            3. End with a thoughtful question"""
            
            # Generate content
            response = model.generate_content(prompt)
            
            return response.text.strip()
                
        except Exception as e:
            self.logger.error(f"Error generating response with Google Gemini: {str(e)}")
            return self._generate_with_templates(text, emotions, techniques)
    
    def _generate_with_anthropic(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using Anthropic Claude API.
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            import anthropic
            
            # Initialize client
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Format emotions and techniques for prompt
            emotion_text = ", ".join([f"{emotion}: {score:.2f}" for emotion, score in emotions.items()])
            technique_text = ", ".join([self._get_technique_info(t) for t in techniques])
            
            # Create system prompt
            system_prompt = f"""You are an empathetic AI therapeutic assistant. 
            Respond to the user's message with empathy, validation, and helpful suggestions.
            The user's primary emotions have been detected as: {emotion_text}
            Recommended therapeutic techniques: {technique_text}
            
            Your response should:
            1. Acknowledge and validate the user's emotions
            2. Offer 1-2 suggested techniques or approaches that might help
            3. End with a thoughtful question to continue the conversation
            
            Be warm, supportive, and professional. Avoid being overly cheerful for negative emotions.
            Keep your response concise (100-200 words)."""
            
            # Call Anthropic API
            message = client.messages.create(
                model=self.llm_model or "claude-3-sonnet-20240229",
                max_tokens=300,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": text}
                ]
            )
            
            return message.content[0].text
                
        except Exception as e:
            self.logger.error(f"Error generating response with Anthropic Claude: {str(e)}")
            return self._generate_with_templates(text, emotions, techniques)
    
    def _generate_with_deepseek(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using Deepseek's API.
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            # Format emotions and techniques for prompt
            emotion_text = ", ".join([f"{emotion}: {score:.2f}" for emotion, score in emotions.items()])
            technique_text = ", ".join([self._get_technique_info(t) for t in techniques])
            
            # Construct prompt for Deepseek
            messages = [
                {
                    "role": "system", 
                    "content": f"""You are an empathetic AI therapeutic assistant. 
                    Respond to the user's message with empathy, validation, and helpful suggestions.
                    The user's primary emotions have been detected as: {emotion_text}
                    Recommended therapeutic techniques: {technique_text}
                    
                    Your response should:
                    1. Acknowledge and validate the user's emotions
                    2. Offer 1-2 suggested techniques or approaches that might help
                    3. End with a thoughtful question to continue the conversation
                    
                    Be warm, supportive, and professional. Avoid being overly cheerful for negative emotions.
                    Keep your response concise (100-200 words)."""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            
            # Define headers for API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Set up API endpoint and payload
            api_url = "https://api.deepseek.com/v1/chat/completions"
            payload = {
                "model": self.llm_model or "deepseek-chat",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 300
            }
            
            # Make API call
            response = requests.post(api_url, json=payload, headers=headers)
            
            # Check for successful response
            if response.status_code == 200:
                response_json = response.json()
                return response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                self.logger.error(f"Error from Deepseek API: {response.status_code} - {response.text}")
                return self._generate_with_templates(text, emotions, techniques)
                
        except Exception as e:
            self.logger.error(f"Error generating response with Deepseek: {str(e)}")
            return self._generate_with_templates(text, emotions, techniques)
    
    def _generate_with_openrouter(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using OpenRouter API.
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            # Format emotions and techniques for prompt
            emotion_text = ", ".join([f"{emotion}: {score:.2f}" for emotion, score in emotions.items()])
            technique_text = ", ".join([self._get_technique_info(t) for t in techniques])
            
            # Construct prompt
            messages = [
                {
                    "role": "system", 
                    "content": f"""You are an empathetic AI therapeutic assistant. 
                    Respond to the user's message with empathy, validation, and helpful suggestions.
                    The user's primary emotions have been detected as: {emotion_text}
                    Recommended therapeutic techniques: {technique_text}
                    
                    Your response should:
                    1. Acknowledge and validate the user's emotions
                    2. Offer 1-2 suggested techniques or approaches that might help
                    3. End with a thoughtful question to continue the conversation
                    
                    Be warm, supportive, and professional. Avoid being overly cheerful for negative emotions.
                    Keep your response concise (100-200 words)."""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            
            # Define headers for API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Set up API endpoint and payload
            api_url = "https://openrouter.ai/api/v1/chat/completions"
            payload = {
                "model": self.llm_model or "deepseek/deepseek-chat:free",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 300
            }
            
            # Make API call
            response = requests.post(api_url, json=payload, headers=headers)
            
            # Check for successful response
            if response.status_code == 200:
                response_json = response.json()
                return response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                self.logger.error(f"Error from OpenRouter API: {response.status_code} - {response.text}")
                return self._generate_with_templates(text, emotions, techniques)
                
        except Exception as e:
            self.logger.error(f"Error generating response with OpenRouter: {str(e)}")
            return self._generate_with_templates(text, emotions, techniques)
    
    def _generate_with_templates(self, text: str, emotions: Dict[str, float], techniques: List[str]) -> str:
        """
        Generate a response using templates (original method, used as fallback).
        
        Args:
            text: User's input text
            emotions: Detected emotions
            techniques: Recommended therapeutic techniques
            
        Returns:
            Generated response
        """
        try:
            # Select primary emotion to respond to
            primary_emotion = self._select_primary_emotion(emotions)
            
            # Build response components
            response_parts = []
            
            # Add emotion-specific greeting
            if primary_emotion in self.templates["greeting"]:
                greeting = random.choice(self.templates["greeting"][primary_emotion])
                response_parts.append(greeting)
            else:
                greeting = random.choice(self.templates["greeting"]["neutral"])
                response_parts.append(greeting)
            
            # Add validation based on emotion
            if primary_emotion in self.templates["validation"]:
                validation = random.choice(self.templates["validation"][primary_emotion])
                response_parts.append(validation)
            
            # Add technique suggestions (max 2)
            if techniques:
                for i, technique_id in enumerate(techniques[:2]):
                    # Only add conjunction for second technique
                    if i == 1:
                        response_parts.append("Additionally,")
                    
                    # Get technique name
                    technique_name = self._get_technique_info(technique_id)
                    
                    # Add technique introduction
                    intro_template = random.choice(self.templates["technique_intro"])
                    intro = intro_template.format(technique_name=technique_name)
                    response_parts.append(intro)
                    
                    # Add technique description if available
                    if technique_id in self.templates["technique_description"]:
                        description = random.choice(self.templates["technique_description"][technique_id])
                        response_parts.append(description)
            
            # Add follow-up question
            follow_up = random.choice(self.templates["follow_up"])
            response_parts.append(follow_up)
            
            # Add closing remark
            closing = random.choice(self.templates["closing"])
            response_parts.append(closing)
            
            # Join all parts into a cohesive response
            full_response = " ".join(response_parts)
            
            return full_response
            
        except Exception as e:
            self.logger.error(f"Error generating response with templates: {str(e)}")
            return "I understand you're sharing something important with me. Could you tell me more about how you're feeling right now?"
    
    def generate(self, text, emotions, techniques, user_id=None, session_id=None):
        """
        Generate an empathetic response based on detected emotions and recommended techniques.
        
        Args:
            text: The user's input text
            emotions: Dictionary of emotions and their scores
            techniques: List of recommended technique IDs
            user_id: User identifier for personalization (optional)
            session_id: Session identifier for context (optional)
            
        Returns:
            Generated response text
        """
        try:
            # Use LLM if configured, otherwise fall back to templates
            if self.use_llm:
                # Call the appropriate LLM provider
                if self.llm_provider == "openai":
                    return self._generate_with_openai(text, emotions, techniques)
                elif self.llm_provider == "huggingface":
                    return self._generate_with_huggingface(text, emotions, techniques)
                elif self.llm_provider == "ollama":
                    return self._generate_with_ollama(text, emotions, techniques)
                elif self.llm_provider == "together_ai":
                    return self._generate_with_together_ai(text, emotions, techniques)
                elif self.llm_provider == "google":
                    return self._generate_with_google(text, emotions, techniques)
                elif self.llm_provider == "anthropic":
                    return self._generate_with_anthropic(text, emotions, techniques)
                elif self.llm_provider == "deepseek":
                    return self._generate_with_deepseek(text, emotions, techniques)
                elif self.llm_provider == "openrouter":
                    return self._generate_with_openrouter(text, emotions, techniques)
                else:
                    self.logger.warning(f"Unknown LLM provider: {self.llm_provider}, falling back to templates")
                    return self._generate_with_templates(text, emotions, techniques)
            else:
                # Use template-based approach
                return self._generate_with_templates(text, emotions, techniques)
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return "I understand you're sharing something important with me. Could you tell me more about how you're feeling right now?" 

    @staticmethod
    def get_available_providers():
        """
        Returns information about available LLM providers.
        
        Returns:
            Dictionary of provider information
        """
        return LLM_PROVIDERS 

    def generate_response(self, text, emotions, techniques=None, user_id=None, session_id=None):
        """
        Alias for the generate method to maintain backward compatibility with updated API endpoints.
        
        Args:
            text: User message text
            emotions: Dictionary of detected emotions
            techniques: Optional therapeutic techniques to incorporate
            user_id: Optional user ID
            session_id: Optional session ID
            
        Returns:
            Generated therapeutic response text
        """
        if not techniques:
            # If techniques aren't provided, get them from the knowledge graph
            from knowledge_graph.graph import TherapeuticKnowledgeGraph
            knowledge_graph = TherapeuticKnowledgeGraph()
            techniques = knowledge_graph.get_techniques_for_emotions(emotions)
            
        return self.generate(text, emotions, techniques, user_id, session_id) 