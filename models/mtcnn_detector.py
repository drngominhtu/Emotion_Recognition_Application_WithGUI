"""
MTCNN face detection with emotion classification
"""
import cv2
import numpy as np
from typing import Tuple, List
from .base_detector import EmotionDetector

try:
    from facenet_pytorch import MTCNN
    import torch
    MTCNN_AVAILABLE = True
except ImportError:
    MTCNN_AVAILABLE = False

class MTCNNDetector(EmotionDetector):
    """MTCNN for precise face detection with basic emotion classification"""
    
    def __init__(self):
        self.mtcnn = None
        
        if MTCNN_AVAILABLE:
            try:
                # Initialize MTCNN
                device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                self.mtcnn = MTCNN(
                    image_size=160,
                    margin=0,
                    min_face_size=20,
                    thresholds=[0.6, 0.7, 0.7],
                    factor=0.709,
                    post_process=False,
                    device=device
                )
                
            except Exception as e:
                print(f"Lỗi khởi tạo MTCNN: {e}")
                self.mtcnn = None
    
    def detect_emotion(self, frame) -> Tuple[str, float, List[Tuple[int, int, int, int]]]:
        """Detect emotion using MTCNN + basic classification"""
        if not self.is_available():
            return "Model không khả dụng", 0.0, []
        
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces and landmarks
            boxes, probs, landmarks = self.mtcnn.detect(rgb_frame, landmarks=True)
            
            if boxes is not None and len(boxes) > 0:
                faces = []
                
                for box in boxes:
                    x1, y1, x2, y2 = box.astype(int)
                    faces.append((x1, y1, x2, y2))
                
                # Use landmarks for emotion detection if available
                if landmarks is not None and len(landmarks) > 0:
                    emotion, confidence = self._landmark_based_emotion(landmarks[0])
                else:
                    emotion, confidence = self._face_geometry_emotion(frame, faces[0])
                
                return emotion, confidence, faces
            
            return "Không phát hiện", 0.0, []
            
        except Exception as e:
            print(f"MTCNN Error: {e}")
            return "Lỗi", 0.0, []
    
    def _landmark_based_emotion(self, landmarks):
        """Emotion detection based on facial landmarks"""
        try:
            # landmarks shape: [5, 2] for 5 key points
            # Points: left_eye, right_eye, nose, left_mouth, right_mouth
            
            left_eye = landmarks[0]
            right_eye = landmarks[1]
            nose = landmarks[2]
            left_mouth = landmarks[3]
            right_mouth = landmarks[4]
            
            # Calculate distances and ratios
            eye_distance = np.linalg.norm(left_eye - right_eye)
            mouth_width = np.linalg.norm(left_mouth - right_mouth)
            
            # Eye-mouth distance
            eye_center = (left_eye + right_eye) / 2
            mouth_center = (left_mouth + right_mouth) / 2
            eye_mouth_distance = np.linalg.norm(eye_center - mouth_center)
            
            # Simple ratios for emotion classification
            mouth_eye_ratio = mouth_width / eye_distance if eye_distance > 0 else 0
            face_length_ratio = eye_mouth_distance / eye_distance if eye_distance > 0 else 0
            
            # Basic emotion classification based on ratios
            if mouth_eye_ratio > 0.8:
                return 'happy', 0.75
            elif mouth_eye_ratio < 0.5:
                return 'sad', 0.7
            elif face_length_ratio > 2.0:
                return 'surprise', 0.8
            elif face_length_ratio < 1.5:
                return 'angry', 0.65
            else:
                return 'neutral', 0.6
                
        except Exception as e:
            print(f"Landmark emotion detection error: {e}")
            return 'neutral', 0.5
    
    def _face_geometry_emotion(self, frame, face_coords):
        """Fallback emotion detection based on face geometry"""
        try:
            x1, y1, x2, y2 = face_coords
            face_roi = frame[y1:y2, x1:x2]
            
            # Convert to grayscale
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            
            # Apply edge detection to find facial features
            edges = cv2.Canny(gray_face, 50, 150)
            
            # Count edges in different regions
            h, w = edges.shape
            upper_edges = np.sum(edges[:h//3, :])
            middle_edges = np.sum(edges[h//3:2*h//3, :])
            lower_edges = np.sum(edges[2*h//3:, :])
            
            total_edges = upper_edges + middle_edges + lower_edges
            
            if total_edges == 0:
                return 'neutral', 0.5
            
            # Emotion based on edge distribution
            lower_ratio = lower_edges / total_edges
            upper_ratio = upper_edges / total_edges
            
            if lower_ratio > 0.4:
                return 'happy', 0.7
            elif upper_ratio > 0.5:
                return 'surprise', 0.6
            elif middle_edges > upper_edges and middle_edges > lower_edges:
                return 'angry', 0.65
            else:
                return 'neutral', 0.6
                
        except Exception as e:
            print(f"Face geometry emotion error: {e}")
            return 'neutral', 0.5
    
    def is_available(self) -> bool:
        """Check if MTCNN is available"""
        return MTCNN_AVAILABLE and self.mtcnn is not None
    
    def get_model_name(self) -> str:
        """Get model name"""
        return "MTCNN + Landmarks"
