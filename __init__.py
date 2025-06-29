"""
Emotion Recognition App Package
Ứng dụng nhận dạng cảm xúc khuôn mặt realtime

Version: 1.0.0
Author: AI Assistant
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"

# Import main components for easy access
from .main import EmotionRecognitionApp, main
from .models.model_manager import ModelManager
from .utils.camera_handler import CameraHandler
from .utils.video_recorder import VideoRecorder

__all__ = [
    'EmotionRecognitionApp',
    'main',
    'ModelManager', 
    'CameraHandler',
    'VideoRecorder'
]
