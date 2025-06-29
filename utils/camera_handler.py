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
        self._lock = threading.Lock()
        self.available_cameras = []
        
    def detect_available_cameras(self) -> list:
        """Detect all available cameras"""
        available_cameras = []
        
        # Test camera indices 0-9
        for index in range(10):
            try:
                cap = cv2.VideoCapture(index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        # Get camera info
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        
                        camera_info = {
                            'index': index,
                            'name': f"Camera {index}",
                            'resolution': f"{width}x{height}",
                            'fps': fps,
                            'type': 'USB/Built-in'
                        }
                        available_cameras.append(camera_info)
                        print(f"Found camera {index}: {width}x{height} @ {fps}fps")
                cap.release()
            except Exception as e:
                pass
        
        # Test IP camera or file paths if needed
        self.available_cameras = available_cameras
        return available_cameras
    
    def start_camera(self, camera_input) -> bool:
        """Start camera capture with flexible input"""
        try:
            with self._lock:
                # Release existing camera first
                if self.cap is not None:
                    self.cap.release()
                    self.cap = None
                
                # Determine camera input type
                camera_index = self._parse_camera_input(camera_input)
                
                # Try to open camera with different backends
                backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
                
                for backend in backends:
                    try:
                        if isinstance(camera_index, str):
                            # File path or IP camera
                            self.cap = cv2.VideoCapture(camera_index)
                        else:
                            # Camera index
                            self.cap = cv2.VideoCapture(camera_index, backend)
                            
                        if self.cap.isOpened():
                            # Set camera properties for stability
                            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                            if isinstance(camera_index, int):
                                self.cap.set(cv2.CAP_PROP_FPS, 30)
                                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                            
                            # Test reading a frame
                            ret, frame = self.cap.read()
                            if ret and frame is not None:
                                print(f"Camera opened successfully: {camera_input} with backend: {backend}")
                                return True
                            else:
                                self.cap.release()
                                self.cap = None
                    except Exception as e:
                        print(f"Failed to open camera {camera_input} with backend {backend}: {e}")
                        if self.cap:
                            self.cap.release()
                            self.cap = None
                
                return False
                
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
    
    def _parse_camera_input(self, camera_input):
        """Parse different types of camera input"""
        if isinstance(camera_input, int):
            return camera_input
        
        if isinstance(camera_input, str):
            # Check if it's a number string
            if camera_input.isdigit():
                return int(camera_input)
            
            # Check if it's a file path
            if any(camera_input.endswith(ext) for ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']):
                return camera_input
            
            # Check if it's an IP camera URL
            if camera_input.startswith(('http://', 'https://', 'rtsp://', 'rtmp://')):
                return camera_input
            
            # Try to extract number from string like "Camera 0"
            import re
            match = re.search(r'(\d+)', camera_input)
            if match:
                return int(match.group(1))
        
        # Default to camera 0
        return 0
    
    def get_camera_info(self) -> dict:
        """Get current camera information"""
        if not self.cap or not self.cap.isOpened():
            return {}
        
        try:
            info = {
                'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'fps': self.cap.get(cv2.CAP_PROP_FPS),
                'brightness': self.cap.get(cv2.CAP_PROP_BRIGHTNESS),
                'contrast': self.cap.get(cv2.CAP_PROP_CONTRAST),
                'saturation': self.cap.get(cv2.CAP_PROP_SATURATION),
            }
            return info
        except Exception as e:
            print(f"Error getting camera info: {e}")
            return {}
    
    def set_camera_property(self, property_name: str, value: float) -> bool:
        """Set camera property"""
        if not self.cap or not self.cap.isOpened():
            return False
        
        try:
            property_map = {
                'brightness': cv2.CAP_PROP_BRIGHTNESS,
                'contrast': cv2.CAP_PROP_CONTRAST,
                'saturation': cv2.CAP_PROP_SATURATION,
                'hue': cv2.CAP_PROP_HUE,
                'gain': cv2.CAP_PROP_GAIN,
                'exposure': cv2.CAP_PROP_EXPOSURE,
                'width': cv2.CAP_PROP_FRAME_WIDTH,
                'height': cv2.CAP_PROP_FRAME_HEIGHT,
                'fps': cv2.CAP_PROP_FPS,
            }
            
            if property_name in property_map:
                return self.cap.set(property_map[property_name], value)
            
            return False
        except Exception as e:
            print(f"Error setting camera property {property_name}: {e}")
            return False
    
    def stop_camera(self):
        """Stop camera capture"""
        try:
            with self._lock:
                self.is_streaming = False
                
                # Wait for thread to finish
                if self.video_thread and self.video_thread.is_alive():
                    self.video_thread.join(timeout=2.0)
                
                # Release camera
                if self.cap:
                    try:
                        self.cap.release()
                    except Exception as e:
                        print(f"Error releasing camera: {e}")
                    finally:
                        self.cap = None
                
                # Force garbage collection
                import gc
                gc.collect()
                
        except Exception as e:
            print(f"Error stopping camera: {e}")
    
    def start_streaming(self, frame_callback: Callable):
        """Start video streaming with callback for each frame"""
        if not self.cap or not self.cap.isOpened():
            return False
        
        try:
            self.is_streaming = True
            self.frame_callback = frame_callback
            
            # Start video processing thread
            self.video_thread = threading.Thread(target=self._process_video, daemon=True)
            self.video_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Error starting streaming: {e}")
            return False
    
    def stop_streaming(self):
        """Stop video streaming"""
        try:
            self.is_streaming = False
            
            # Wait for thread to finish with timeout
            if self.video_thread and self.video_thread.is_alive():
                self.video_thread.join(timeout=2.0)
                if self.video_thread.is_alive():
                    print("Warning: Video thread did not stop gracefully")
            
        except Exception as e:
            print(f"Error stopping streaming: {e}")
    
    def _process_video(self):
        """Main video processing loop"""
        frame_count = 0
        last_error_time = 0
        error_count = 0
        
        while self.is_streaming:
            try:
                # Check if camera is still valid
                if not self.cap or not self.cap.isOpened():
                    print("Camera connection lost")
                    break
                
                # Try to read frame with timeout
                ret, frame = self.cap.read()
                
                if not ret or frame is None:
                    # Handle read error
                    current_time = time.time()
                    if current_time - last_error_time > 1.0:  # Reset error count every second
                        error_count = 0
                    
                    error_count += 1
                    last_error_time = current_time
                    
                    if error_count > 5:  # Too many consecutive errors
                        print("Too many camera read errors, stopping stream")
                        break
                    
                    time.sleep(0.1)  # Wait before retry
                    continue
                
                # Reset error count on successful read
                error_count = 0
                
                # Resize frame for better performance
                try:
                    frame = cv2.resize(frame, (640, 480))
                except Exception as e:
                    print(f"Error resizing frame: {e}")
                    continue
                
                # Call callback with frame
                if self.frame_callback and self.is_streaming:
                    try:
                        self.frame_callback(frame)
                    except Exception as e:
                        print(f"Error in frame callback: {e}")
                
                frame_count += 1
                
                # Control frame rate
                time.sleep(0.03)  # ~30 FPS
                
            except Exception as e:
                print(f"Error in video processing loop: {e}")
                time.sleep(0.1)  # Prevent tight error loop
                
                # Break if too many errors
                error_count += 1
                if error_count > 10:
                    print("Too many processing errors, stopping stream")
                    break
        
        print(f"Video processing stopped. Processed {frame_count} frames.")
    
    @staticmethod
    def frame_to_tkinter(frame):
        """Convert OpenCV frame to Tkinter PhotoImage"""
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error converting frame to tkinter: {e}")
            return None
    
    @staticmethod
    def draw_face_rectangles(frame, faces, emotion=None, confidence=None):
        """Draw rectangles around detected faces with emotion labels"""
        try:
            for (x1, y1, x2, y2) in faces:
                # Draw rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw emotion label if provided
                if emotion and confidence is not None:
                    label = f"{emotion}: {confidence:.1%}"
                    cv2.putText(frame, label, (x1, y1 - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            return frame
        except Exception as e:
            print(f"Error drawing face rectangles: {e}")
            return frame
