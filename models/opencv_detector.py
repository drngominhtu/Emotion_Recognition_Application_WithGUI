"""
OpenCV basic face detection (fallback when no emotion models available)
"""
import cv2
from typing import Tuple, List
from .base_detector import EmotionDetector

class OpenCVDetector(EmotionDetector):
    """Basic OpenCV face detector (no emotion recognition)"""
    
    def __init__(self):
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.available = True
        except Exception as e:
            print(f"OpenCV Error: {e}")
            self.available = False
    
    def detect_emotion(self, frame) -> Tuple[str, float, List[Tuple[int, int, int, int]]]:
        """Basic face detection with OpenCV (no emotion recognition)"""
        if not self.is_available():
            return "Model không khả dụng", 0.0, []
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            face_list = []
            for (x, y, w, h) in faces:
                face_list.append((x, y, x + w, y + h))
            
            if len(face_list) > 0:
                return "Phát hiện khuôn mặt", 1.0, face_list
            else:
                return "Không phát hiện", 0.0, []
        except Exception as e:
            print(f"OpenCV Error: {e}")
            return "Lỗi", 0.0, []
    
    def is_available(self) -> bool:
        """Check if OpenCV is available"""
        return self.available
    
    def get_model_name(self) -> str:
        """Get model name"""
        return "OpenCV Basic"
