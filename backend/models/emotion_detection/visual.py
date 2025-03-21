import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
from pathlib import Path
import logging

class VisualEmotionDetector:
    """
    Class for detecting emotions from facial expressions using computer vision.
    Uses a pre-trained CNN model to classify emotions from face images.
    """
    
    # Emotion mapping
    EMOTIONS = {
        0: "angry",
        1: "disgust",
        2: "fear",
        3: "happy",
        4: "sad",
        5: "surprise",
        6: "neutral"
    }
    
    def __init__(self, model_path=None):
        """
        Initialize the emotion detector with pre-trained models.
        
        Args:
            model_path: Path to a pre-trained emotion detection model (optional)
        """
        self.logger = logging.getLogger(__name__)
        self.confidence = 0.0
        
        # Load face detection model
        model_dir = Path(__file__).parent / "pretrained"
        face_cascade_path = str(model_dir / "haarcascade_frontalface_default.xml")
        
        # Check if model exists, if not use OpenCV's default
        if not os.path.exists(face_cascade_path):
            model_dir.mkdir(parents=True, exist_ok=True)
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.logger.info("Using OpenCV's default face detection model")
        else:
            self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
            self.logger.info(f"Loaded face detection model from {face_cascade_path}")
        
        # Initialize emotion model
        # In a real implementation, you would load a pre-trained model
        # Here we'll simulate the model for demonstration purposes
        self.model = self._create_mock_model() if model_path is None else load_model(model_path)
        self.logger.info("Emotion detection model initialized")
    
    def _create_mock_model(self):
        """Creates a simple mock model for demonstration purposes"""
        class MockModel:
            def predict(self, image):
                # Mock prediction - returns random emotion probabilities
                # In a real implementation, this would be a trained neural network
                return np.random.rand(1, 7)
        return MockModel()
    
    def preprocess_image(self, image):
        """
        Preprocess an image for emotion detection.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Preprocessed image suitable for the model
        """
        # Convert PIL image to numpy if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
            
        # Convert to grayscale if it's color
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
            
        # Resize to model input size
        resized = cv2.resize(gray, (48, 48))
        
        # Normalize pixel values
        normalized = resized / 255.0
        
        # Expand dimensions for model input
        return np.expand_dims(np.expand_dims(normalized, -1), 0)
    
    def detect_faces(self, image):
        """
        Detect faces in an image.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            List of face regions (x, y, w, h)
        """
        # Convert PIL image to numpy if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
            
        # Convert to grayscale if it's color
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
            
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return faces
    
    def detect_emotions(self, image):
        """
        Detect emotions from facial expressions in an image.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Dictionary of emotions and their confidence scores
        """
        # Detect faces
        faces = self.detect_faces(image)
        
        # If no faces detected, return neutral with low confidence
        if len(faces) == 0:
            self.confidence = 0.1
            return {"neutral": 0.5}
        
        # Process the largest face
        face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = face
        
        # Extract face region
        if isinstance(image, Image.Image):
            image = np.array(image)
            
        if len(image.shape) == 3 and image.shape[2] == 3:
            face_img = image[y:y+h, x:x+w]
        else:
            face_img = image[y:y+h, x:x+w]
            
        # Preprocess for model
        processed_img = self.preprocess_image(face_img)
        
        # Get emotion predictions
        predictions = self.model.predict(processed_img)[0]
        
        # Convert to dictionary
        emotions = {self.EMOTIONS[i]: float(score) for i, score in enumerate(predictions)}
        
        # Set confidence as the highest emotion score
        self.confidence = float(max(predictions))
        
        return emotions
    
    def get_confidence(self):
        """Return the confidence score of the last prediction"""
        return self.confidence 