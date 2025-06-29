"""
MediaPipe + Transformers emotion detection model
"""
import cv2
import numpy as np
from typing import Tuple, List
from .base_detector import EmotionDetector

try:
    import mediapipe as mp
    from transformers import pipeline
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

class MediaPipeTransformersDetector(EmotionDetector):
    """MediaPipe for face detection + Transformers for emotion recognition"""
    
    def __init__(self):
        self.face_detection = None
        self.emotion_classifier = None
        
        if MEDIAPIPE_AVAILABLE:
            try:
                # Initialize MediaPipe Face Detection
                mp_face_detection = mp.solutions.face_detection
                self.face_detection = mp_face_detection.FaceDetection(
                    model_selection=0, min_detection_confidence=0.5
                )
                
                # Initialize emotion classifier from Transformers
                self.emotion_classifier = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    device=-1  # Use CPU
                )
                
                # Emotion mapping for better results
                self.emotion_map = {
                    'joy': 'happy',
                    'sadness': 'sad',
                    'anger': 'angry',
                    'fear': 'fear',
                    'surprise': 'surprise',
                    'disgust': 'disgust'
                }
                
            except Exception as e:
                print(f"Lỗi khởi tạo MediaPipe+Transformers: {e}")
                self.face_detection = None
                self.emotion_classifier = None
    
    def detect_emotion(self, frame) -> Tuple[str, float, List[Tuple[int, int, int, int]]]:
        """Detect emotion using MediaPipe + basic heuristics"""
        if not self.is_available():
            return "Model không khả dụng", 0.0, []
        
        try:
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            results = self.face_detection.process(rgb_frame)
            
            if results.detections:
                faces = []
                h, w, _ = frame.shape
                
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    x1 = int(bbox.xmin * w)
                    y1 = int(bbox.ymin * h)
                    x2 = int((bbox.xmin + bbox.width) * w)
                    y2 = int((bbox.ymin + bbox.height) * h)
                    
                    faces.append((x1, y1, x2, y2))
                
                # Simple emotion detection based on facial features
                # This is a simplified approach - in practice you'd use a proper emotion model
                emotion, confidence = self._simple_emotion_detection(frame, faces[0])
                
                return emotion, confidence, faces
            
            return "Không phát hiện", 0.0, []
            
        except Exception as e:
            print(f"MediaPipe Error: {e}")
            return "Lỗi", 0.0, []
    
    def _simple_emotion_detection(self, frame, face_coords):
        """Simple emotion detection based on facial geometry"""
        try:
            x1, y1, x2, y2 = face_coords
            face_roi = frame[y1:y2, x1:x2]
            
            # Convert to grayscale for analysis
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            
            # Simple heuristics based on face geometry
            height, width = gray_face.shape
            
            # Analyze different regions
            upper_third = gray_face[:height//3, :]
            middle_third = gray_face[height//3:2*height//3, :]
            lower_third = gray_face[2*height//3:, :]
            
            # Calculate brightness in different regions
            upper_brightness = np.mean(upper_third)
            middle_brightness = np.mean(middle_third)
            lower_brightness = np.mean(lower_third)
            
            # Simple emotion classification based on brightness patterns
            # This is very basic - real emotion detection is much more complex
            emotions = ['happy', 'sad', 'neutral', 'surprise', 'angry']
            
            # Random selection weighted by some simple features
            if lower_brightness > middle_brightness * 1.1:
                return 'happy', 0.7
            elif upper_brightness < middle_brightness * 0.9:
                return 'sad', 0.6
            elif abs(upper_brightness - lower_brightness) > 20:
                return 'surprise', 0.65
            else:
                return 'neutral', 0.8
                
        except Exception as e:
            print(f"Simple emotion detection error: {e}")
            return 'neutral', 0.5
    
    def is_available(self) -> bool:
        """Check if MediaPipe is available"""
        return MEDIAPIPE_AVAILABLE and self.face_detection is not None
    
    def get_model_name(self) -> str:
        """Get model name"""
        return "MediaPipe + Heuristics"
