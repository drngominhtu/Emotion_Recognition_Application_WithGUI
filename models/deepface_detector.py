"""
DeepFace model implementation for emotion detection
"""
from typing import Tuple, List
from .base_detector import EmotionDetector

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False

class DeepFaceDetector(EmotionDetector):
    """DeepFace model for emotion detection"""
    
    def __init__(self, backend="VGG-Face"):
        self.backend = backend
        self.model_name = f"DeepFace - {backend}"
    
    def detect_emotion(self, frame) -> Tuple[str, float, List[Tuple[int, int, int, int]]]:
        """Detect emotion using DeepFace"""
        if not self.is_available():
            return "Model không khả dụng", 0.0, []
        
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], 
                                    enforce_detection=False, silent=True)
            
            if isinstance(result, list):
                result = result[0]
            
            dominant_emotion = result['dominant_emotion']
            confidence = result['emotion'][dominant_emotion] / 100.0
            
            # Get face region
            region = result.get('region', {})
            if region:
                x, y, w, h = region['x'], region['y'], region['w'], region['h']
                faces = [(x, y, x + w, y + h)]
            else:
                faces = []
            
            return dominant_emotion, confidence, faces
        except Exception as e:
            print(f"DeepFace Error: {e}")
            return "Lỗi", 0.0, []
    
    def is_available(self) -> bool:
        """Check if DeepFace is available"""
        return DEEPFACE_AVAILABLE
    
    def get_model_name(self) -> str:
        """Get model name"""
        return self.model_name
