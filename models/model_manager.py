"""
Model manager to handle all emotion detection models
"""
from typing import List, Dict
from .base_detector import EmotionDetector
from .fer_detector import FERDetector
from .deepface_detector import DeepFaceDetector
from .opencv_detector import OpenCVDetector
from .mediapipe_detector import MediaPipeTransformersDetector
from .mtcnn_detector import MTCNNDetector
from .dlib_detector import DlibDetector
from .simple_cnn_detector import SimpleCNNDetector

class ModelManager:
    """Manager class for all emotion detection models"""
    
    def __init__(self):
        self.models: Dict[str, EmotionDetector] = {}
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize all available models"""
        # FER model
        fer_model = FERDetector()
        if fer_model.is_available():
            self.models[fer_model.get_model_name()] = fer_model
        
        # DeepFace models
        deepface_backends = ["VGG-Face", "Facenet", "OpenFace"]
        for backend in deepface_backends:
            deepface_model = DeepFaceDetector(backend)
            if deepface_model.is_available():
                self.models[deepface_model.get_model_name()] = deepface_model
        
        # MediaPipe + Transformers model
        mediapipe_model = MediaPipeTransformersDetector()
        if mediapipe_model.is_available():
            self.models[mediapipe_model.get_model_name()] = mediapipe_model
        
        # MTCNN model
        mtcnn_model = MTCNNDetector()
        if mtcnn_model.is_available():
            self.models[mtcnn_model.get_model_name()] = mtcnn_model
        
        # Dlib model
        dlib_model = DlibDetector()
        if dlib_model.is_available():
            self.models[dlib_model.get_model_name()] = dlib_model
        
        # Simple CNN model
        cnn_model = SimpleCNNDetector()
        if cnn_model.is_available():
            self.models[cnn_model.get_model_name()] = cnn_model
        
        # OpenCV fallback (always add this last)
        opencv_model = OpenCVDetector()
        if opencv_model.is_available():
            self.models[opencv_model.get_model_name()] = opencv_model
    
    def get_available_models(self) -> List[str]:
        """Get list of available model names"""
        return list(self.models.keys())
    
    def get_model(self, model_name: str) -> EmotionDetector:
        """Get a specific model by name"""
        return self.models.get(model_name)
    
    def detect_emotion(self, model_name: str, frame):
        """Detect emotion using specified model"""
        model = self.get_model(model_name)
        if model:
            return model.detect_emotion(frame)
        else:
            return "Model không tồn tại", 0.0, []
