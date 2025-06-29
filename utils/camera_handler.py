"""
Camera handler for video capture and processing
"""
import cv2
import threading
import time
from typing import Callable, Optional
from PIL import Image, ImageTk

class CameraHandler:
    """Handle camera operations and video processing"""
    
    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_streaming = False
        self.video_thread: Optional[threading.Thread] = None
        self.frame_callback: Optional[Callable] = None
        
    def start_camera(self, camera_index=0) -> bool:
        """Start camera capture"""
        try:
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                return False
            return True
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
    
    def stop_camera(self):
        """Stop camera capture"""
        self.is_streaming = False
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def start_streaming(self, frame_callback: Callable):
        """Start video streaming with callback for each frame"""
        if not self.cap or not self.cap.isOpened():
            return False
        
        self.is_streaming = True
        self.frame_callback = frame_callback
        
        # Start video processing thread
        self.video_thread = threading.Thread(target=self._process_video)
        self.video_thread.daemon = True
        self.video_thread.start()
        
        return True
    
    def stop_streaming(self):
        """Stop video streaming"""
        self.is_streaming = False
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join(timeout=1.0)
    
    def _process_video(self):
        """Main video processing loop"""
        while self.is_streaming and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Resize frame for better performance
            frame = cv2.resize(frame, (640, 480))
            
            # Call callback with frame
            if self.frame_callback:
                self.frame_callback(frame)
            
            # Small delay to prevent high CPU usage
            time.sleep(0.03)  # ~30 FPS
    
    @staticmethod
    def frame_to_tkinter(frame):
        """Convert OpenCV frame to Tkinter PhotoImage"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        return ImageTk.PhotoImage(img)
    
    @staticmethod
    def draw_face_rectangles(frame, faces, emotion=None, confidence=None):
        """Draw rectangles around detected faces with emotion labels"""
        for (x1, y1, x2, y2) in faces:
            # Draw rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw emotion label if provided
            if emotion and confidence is not None:
                label = f"{emotion}: {confidence:.2%}"
                cv2.putText(frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame
