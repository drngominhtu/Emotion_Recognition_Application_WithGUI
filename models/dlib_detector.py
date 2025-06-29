"""
Dlib face detection with HOG features and emotion classification
"""
import cv2
import numpy as np
from typing import Tuple, List
from .base_detector import EmotionDetector

try:
    import dlib
    DLIB_AVAILABLE = True
except ImportError:
    DLIB_AVAILABLE = False

class DlibDetector(EmotionDetector):
    """Dlib HOG face detector with emotion classification"""
    
    def __init__(self):
        self.face_detector = None
        self.shape_predictor = None
        
        if DLIB_AVAILABLE:
            try:
                # Initialize Dlib face detector
                self.face_detector = dlib.get_frontal_face_detector()
                
                # Try to load shape predictor (68 landmarks)
                # Note: This requires downloading shape_predictor_68_face_landmarks.dat
                try:
                    self.shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
                except:
                    print("Shape predictor not found. Using basic face detection only.")
                    self.shape_predictor = None
                
            except Exception as e:
                print(f"Lỗi khởi tạo Dlib: {e}")
                self.face_detector = None
    
    def detect_emotion(self, frame) -> Tuple[str, float, List[Tuple[int, int, int, int]]]:
        """Detect emotion using Dlib"""
        if not self.is_available():
            return "Model không khả dụng", 0.0, []
        
        try:
            # Convert to grayscale for Dlib
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces_dlib = self.face_detector(gray)
            
            if len(faces_dlib) > 0:
                faces = []
                
                for face in faces_dlib:
                    x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
                    faces.append((x1, y1, x2, y2))
                
                # Use landmarks if available
                if self.shape_predictor is not None:
                    emotion, confidence = self._landmark_emotion_detection(gray, faces_dlib[0])
                else:
                    emotion, confidence = self._hog_based_emotion(gray, faces[0])
                
                return emotion, confidence, faces
            
            return "Không phát hiện", 0.0, []
            
        except Exception as e:
            print(f"Dlib Error: {e}")
            return "Lỗi", 0.0, []
    
    def _landmark_emotion_detection(self, gray, face_rect):
        """Emotion detection using 68 facial landmarks"""
        try:
            # Get landmarks
            landmarks = self.shape_predictor(gray, face_rect)
            
            # Convert to numpy array
            points = np.array([[p.x, p.y] for p in landmarks.parts()])
            
            # Key facial regions (based on 68-point model)
            # Mouth: points 48-67
            # Eyes: left (36-41), right (42-47)
            # Eyebrows: left (17-21), right (22-26)
            
            mouth_points = points[48:68]
            left_eye_points = points[36:42]
            right_eye_points = points[42:48]
            left_eyebrow = points[17:22]
            right_eyebrow = points[22:27]
            
            # Calculate features
            mouth_width = np.linalg.norm(mouth_points[6] - mouth_points[12])  # corner to corner
            mouth_height = np.linalg.norm(mouth_points[3] - mouth_points[9])   # top to bottom
            
            left_eye_width = np.linalg.norm(left_eye_points[0] - left_eye_points[3])
            right_eye_width = np.linalg.norm(right_eye_points[0] - right_eye_points[3])
            
            # Calculate ratios
            mouth_aspect_ratio = mouth_height / mouth_width if mouth_width > 0 else 0
            avg_eye_width = (left_eye_width + right_eye_width) / 2
            mouth_eye_ratio = mouth_width / avg_eye_width if avg_eye_width > 0 else 0
            
            # Eyebrow position relative to eyes
            left_eyebrow_height = np.mean(left_eyebrow[:, 1]) - np.mean(left_eye_points[:, 1])
            right_eyebrow_height = np.mean(right_eyebrow[:, 1]) - np.mean(right_eye_points[:, 1])
            avg_eyebrow_height = (left_eyebrow_height + right_eyebrow_height) / 2
            
            # Emotion classification based on facial ratios
            if mouth_aspect_ratio > 0.3 and mouth_eye_ratio > 0.8:
                return 'happy', 0.8
            elif mouth_aspect_ratio < 0.1 and avg_eyebrow_height < -5:
                return 'sad', 0.75
            elif avg_eyebrow_height < -10 and mouth_aspect_ratio < 0.2:
                return 'angry', 0.7
            elif mouth_aspect_ratio > 0.4:
                return 'surprise', 0.8
            elif mouth_aspect_ratio < 0.15:
                return 'disgust', 0.6
            else:
                return 'neutral', 0.65
                
        except Exception as e:
            print(f"Landmark emotion detection error: {e}")
            return 'neutral', 0.5
    
    def _hog_based_emotion(self, gray, face_coords):
        """Basic emotion detection using HOG features"""
        try:
            x1, y1, x2, y2 = face_coords
            face_roi = gray[y1:y2, x1:x2]
            
            # Resize face to standard size
            face_resized = cv2.resize(face_roi, (64, 64))
            
            # Calculate HOG features
            from skimage.feature import hog
            
            hog_features = hog(
                face_resized,
                orientations=9,
                pixels_per_cell=(8, 8),
                cells_per_block=(2, 2),
                visualize=False
            )
            
            # Simple classification based on HOG feature statistics
            feature_mean = np.mean(hog_features)
            feature_std = np.std(hog_features)
            feature_max = np.max(hog_features)
            
            # Basic emotion classification based on feature statistics
            if feature_mean > 0.1 and feature_std > 0.05:
                return 'happy', 0.7
            elif feature_mean < 0.05 and feature_std < 0.03:
                return 'sad', 0.65
            elif feature_max > 0.5:
                return 'surprise', 0.7
            elif feature_std > 0.08:
                return 'angry', 0.6
            else:
                return 'neutral', 0.6
                
        except Exception as e:
            print(f"HOG emotion detection error: {e}")
            return 'neutral', 0.5
    
    def is_available(self) -> bool:
        """Check if Dlib is available"""
        return DLIB_AVAILABLE and self.face_detector is not None
    
    def get_model_name(self) -> str:
        """Get model name"""
        if self.shape_predictor is not None:
            return "Dlib + 68 Landmarks"
        else:
            return "Dlib + HOG Features"
