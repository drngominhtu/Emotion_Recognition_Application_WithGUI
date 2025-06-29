"""
Base class for emotion detection models
"""
from abc import ABC, abstractmethod
from typing import Tuple, List

class EmotionDetector(ABC):
    """Abstract base class for emotion detection models"""
    
    @abstractmethod
    def detect_emotion(self, frame) -> Tuple[str, float, List[Tuple[int, int, int, int]]]:
        """
        Detect emotion in a frame
        
        Args:
            frame: Input image frame
            
        Returns:
            Tuple of (emotion_name, confidence, face_coordinates)
            face_coordinates is list of (x1, y1, x2, y2) tuples
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the model is available for use"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get the display name of the model"""
        pass
