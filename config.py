"""
Configuration settings for the application
"""

# Application settings
APP_NAME = "Nhận dạng cảm xúc khuôn mặt - Realtime"
APP_VERSION = "1.0.0"

# Window settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Video settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30
FRAME_DELAY = 0.03  # 1/FPS for ~30 FPS

# Recording settings
DEFAULT_CODEC = 'XVID'
DEFAULT_FPS = 20.0

# Video recording settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Supported video formats for recording
SUPPORTED_VIDEO_FORMATS = [
    ("MP4 files", "*.mp4"),
    ("AVI files", "*.avi"), 
    ("MOV files", "*.mov"),
    ("MKV files", "*.mkv"),
    ("All files", "*.*")
]

# Video encoding settings
VIDEO_CODECS = {
    'mp4': 'mp4v',
    'avi': 'XVID',
    'mov': 'mp4v',
    'mkv': 'XVID'
}

# GUI settings
CONTROL_PANEL_PADDING = "5"
MAIN_FRAME_PADDING = "10"
EMOTION_HISTORY_HEIGHT = 15
EMOTION_HISTORY_WIDTH = 30
MAX_HISTORY_ENTRIES = 100

# Font settings
DEFAULT_FONT = ("Arial", 12)
EMOTION_FONT = ("Arial", 16)
CONFIDENCE_FONT = ("Arial", 14)
BOLD_FONT = ("Arial", 12, "bold")

# Colors
PRIMARY_COLOR = "blue"
SUCCESS_COLOR = "green"
ERROR_COLOR = "red"
WARNING_COLOR = "orange"

# Emotion mapping (for display in Vietnamese)
EMOTION_TRANSLATIONS = {
    "happy": "Vui vẻ",
    "sad": "Buồn",
    "angry": "Tức giận",
    "fear": "Sợ hãi",
    "surprise": "Ngạc nhiên",
    "neutral": "Bình thường",
    "disgust": "Ghê tởm"
}

# Model information
MODEL_INFO = {
    "FER (Fast)": {
        "description": "Fast Emotion Recognition - Nhanh nhất, phù hợp realtime",
        "accuracy": "Medium",
        "speed": "Very Fast"
    },
    "DeepFace - VGG-Face": {
        "description": "DeepFace với VGG-Face backend - Độ chính xác cao",
        "accuracy": "High",
        "speed": "Slow"
    },
    "DeepFace - Facenet": {
        "description": "DeepFace với Facenet backend - Cân bằng tốc độ và độ chính xác",
        "accuracy": "High",
        "speed": "Medium"
    },
    "DeepFace - OpenFace": {
        "description": "DeepFace với OpenFace backend - Model nhẹ",
        "accuracy": "Medium",
        "speed": "Fast"
    },
    "MediaPipe + Heuristics": {
        "description": "MediaPipe face detection với emotion heuristics",
        "accuracy": "Medium",
        "speed": "Fast"
    },
    "MTCNN + Landmarks": {
        "description": "MTCNN face detection với facial landmarks",
        "accuracy": "Medium-High",
        "speed": "Medium"
    },
    "Dlib + 68 Landmarks": {
        "description": "Dlib với 68 facial landmarks - Rất chính xác",
        "accuracy": "High",
        "speed": "Medium"
    },
    "Dlib + HOG Features": {
        "description": "Dlib với HOG features - Fallback khi không có landmarks",
        "accuracy": "Medium",
        "speed": "Fast"
    },
    "Simple CNN": {
        "description": "CNN đơn giản - Experimental",
        "accuracy": "Medium",
        "speed": "Fast"
    },
    "OpenCV Basic": {
        "description": "OpenCV face detection cơ bản - Fallback",
        "accuracy": "Low",
        "speed": "Very Fast"
    }
}
