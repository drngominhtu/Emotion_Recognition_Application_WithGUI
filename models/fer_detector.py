"""
FER (Facial Emotion Recognition) model implementation
"""
import cv2
from typing import Tuple, List
from .base_detector import EmotionDetector

try:
    from fer import FER
    FER_AVAILABLE = True
except ImportError:
    FER_AVAILABLE = False

class FERDetector(EmotionDetector):
    """FER model for emotion detection"""
    
    def __init__(self):
        self.detector = None
        if FER_AVAILABLE:
            try:
                self.detector = FER(mtcnn=True)
            except Exception as e:
                print(f"Lỗi khởi tạo FER: {e}")
                self.detector = None
    
    def detect_emotion(self, frame) -> Tuple[str, float, List[Tuple[int, int, int, int]]]:
        """Detect emotion using FER"""
        if not self.is_available():
            return "Model không khả dụng", 0.0, []
        
        try:
            emotions = self.detector.detect_emotions(frame)
            if emotions:
                emotion_dict = emotions[0]['emotions']
                dominant_emotion = max(emotion_dict, key=emotion_dict.get)
                confidence = emotion_dict[dominant_emotion]
                
                # Get face coordinates for drawing rectangle
                box = emotions[0]['box']
                faces = [(box[0], box[1], box[0] + box[2], box[1] + box[3])]
                
                return dominant_emotion, confidence, faces
            return "Không phát hiện", 0.0, []
        except Exception as e:
            print(f"FER Error: {e}")
            return "Lỗi", 0.0, []
    
    def is_available(self) -> bool:
        """Check if FER is available"""
        return FER_AVAILABLE and self.detector is not None
    
    def get_model_name(self) -> str:
        """Get model name"""
        return "FER (Fast)"
