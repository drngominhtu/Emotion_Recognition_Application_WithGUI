"""
Simple CNN model for emotion recognition
"""
import cv2
import numpy as np
from typing import Tuple, List
from .base_detector import EmotionDetector

try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

class SimpleCNNDetector(EmotionDetector):
    """Simple CNN model for emotion detection"""
    
    def __init__(self):
        self.face_cascade = None
        self.model = None
        
        if TENSORFLOW_AVAILABLE:
            try:
                # Initialize face detector
                self.face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                )
                
                # Create simple CNN model
                self.model = self._create_simple_model()
                
            except Exception as e:
                print(f"Lỗi khởi tạo Simple CNN: {e}")
                self.face_cascade = None
                self.model = None
    
    def _create_simple_model(self):
        """Create a simple CNN model for emotion classification"""
        try:
            model = keras.Sequential([
                keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
                keras.layers.MaxPooling2D((2, 2)),
                keras.layers.Conv2D(64, (3, 3), activation='relu'),
                keras.layers.MaxPooling2D((2, 2)),
                keras.layers.Conv2D(64, (3, 3), activation='relu'),
                keras.layers.Flatten(),
                keras.layers.Dense(64, activation='relu'),
                keras.layers.Dropout(0.5),
                keras.layers.Dense(7, activation='softmax')  # 7 emotions
            ])
            
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            # Initialize with random weights (in practice, you'd load pre-trained weights)
            return model
            
        except Exception as e:
            print(f"Error creating CNN model: {e}")
            return None
    
    def detect_emotion(self, frame) -> Tuple[str, float, List[Tuple[int, int, int, int]]]:
        """Detect emotion using simple CNN"""
        if not self.is_available():
            return "Model không khả dụng", 0.0, []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                face_list = []
                for (x, y, w, h) in faces:
                    face_list.append((x, y, x + w, y + h))
                
                # Get first face for emotion detection
                x, y, w, h = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                
                # Predict emotion
                emotion, confidence = self._predict_emotion(face_roi)
                
                return emotion, confidence, face_list
            
            return "Không phát hiện", 0.0, []
            
        except Exception as e:
            print(f"Simple CNN Error: {e}")
            return "Lỗi", 0.0, []
    
    def _predict_emotion(self, face_roi):
        """Predict emotion using CNN model"""
        try:
            # Preprocess face
            face_resized = cv2.resize(face_roi, (48, 48))
            face_normalized = face_resized / 255.0
            face_expanded = np.expand_dims(face_normalized, axis=0)
            face_expanded = np.expand_dims(face_expanded, axis=-1)
            
            # Predict
            predictions = self.model.predict(face_expanded, verbose=0)
            
            # Emotion labels
            emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
            
            # Get prediction
            emotion_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][emotion_idx])
            emotion = emotions[emotion_idx]
            
            return emotion, confidence
            
        except Exception as e:
            print(f"CNN prediction error: {e}")
            # Fallback to simple heuristics
            return self._simple_heuristic_emotion(face_roi)
    
    def _simple_heuristic_emotion(self, face_roi):
        """Simple emotion detection based on pixel intensity patterns"""
        try:
            h, w = face_roi.shape
            
            # Divide face into regions
            upper_region = face_roi[:h//3, :]
            middle_region = face_roi[h//3:2*h//3, :]
            lower_region = face_roi[2*h//3:, :]
            
            # Calculate regional statistics
            upper_mean = np.mean(upper_region)
            middle_mean = np.mean(middle_region)
            lower_mean = np.mean(lower_region)
            
            upper_std = np.std(upper_region)
            lower_std = np.std(lower_region)
            
            # Simple emotion classification
            if lower_mean > middle_mean * 1.1 and lower_std > 20:
                return 'happy', 0.6
            elif upper_mean < middle_mean * 0.9:
                return 'sad', 0.55
            elif upper_std > 30 and lower_std > 25:
                return 'surprise', 0.6
            elif upper_std > 35:
                return 'angry', 0.55
            else:
                return 'neutral', 0.7
                
        except Exception as e:
            print(f"Heuristic emotion error: {e}")
            return 'neutral', 0.5
    
    def is_available(self) -> bool:
        """Check if Simple CNN is available"""
        return TENSORFLOW_AVAILABLE and self.face_cascade is not None and self.model is not None
    
    def get_model_name(self) -> str:
        """Get model name"""
        return "Simple CNN"
