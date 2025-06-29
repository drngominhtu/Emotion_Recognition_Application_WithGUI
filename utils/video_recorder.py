"""
Video recorder for saving emotion recognition sessions
"""
import cv2
from datetime import datetime
from typing import Optional

class VideoRecorder:
    """Handle video recording functionality"""
    
    def __init__(self):
        self.video_writer: Optional[cv2.VideoWriter] = None
        self.is_recording = False
        self.output_filename = ""
        self.recording_start_time = None
        self.frame_count = 0
    
    def start_recording(self, filename: str, fps: float = 20.0, frame_size: tuple = (640, 480)) -> bool:
        """Start video recording"""
        try:
            # Determine codec based on file extension
            ext = filename.lower().split('.')[-1]
            if ext == 'mp4':
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            elif ext == 'avi':
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
            elif ext == 'mov':
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            else:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
            
            self.video_writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)
            
            if self.video_writer.isOpened():
                self.is_recording = True
                self.output_filename = filename
                self.recording_start_time = datetime.now()
                self.frame_count = 0
                print(f"Bắt đầu ghi video: {filename}")
                return True
            else:
                print(f"Không thể tạo video writer cho: {filename}")
                return False
                
        except Exception as e:
            print(f"Error starting recording: {e}")
            return False
    
    def stop_recording(self):
        """Stop video recording"""
        if self.is_recording:
            recording_duration = datetime.now() - self.recording_start_time if self.recording_start_time else None
            
            print(f"Dừng ghi video: {self.output_filename}")
            if recording_duration:
                print(f"Thời lượng: {recording_duration}")
            print(f"Số frame: {self.frame_count}")
        
        self.is_recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        
        self.recording_start_time = None
        self.frame_count = 0
    
    def write_frame(self, frame):
        """Write a frame to the video file"""
        if self.is_recording and self.video_writer:
            self.video_writer.write(frame)
            self.frame_count += 1
    
    def get_default_filename(self) -> str:
        """Generate default filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"emotion_recording_{timestamp}.mp4"
    
    def get_current_filename(self) -> str:
        """Get current recording filename"""
        return self.output_filename
    
    def get_recording_info(self) -> dict:
        """Get current recording information"""
        if not self.is_recording:
            return {}
        
        duration = datetime.now() - self.recording_start_time if self.recording_start_time else None
        
        return {
            'filename': self.output_filename,
            'start_time': self.recording_start_time,
            'duration': duration,
            'frame_count': self.frame_count,
            'is_recording': self.is_recording
        }
    
    def is_recording_active(self) -> bool:
        """Check if recording is currently active"""
        return self.is_recording
