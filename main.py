"""
Main application file for Emotion Recognition App
Ứng dụng nhận dạng cảm xúc khuôn mặt realtime
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import sys
import os
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import application modules
from models.model_manager import ModelManager
from gui.main_window import MainWindow
from gui.control_panel import ControlPanel
from gui.video_display import VideoDisplay
from gui.emotion_panel import EmotionPanel
from utils.camera_handler import CameraHandler
from utils.video_recorder import VideoRecorder
from utils.logger import EmotionLogger
import config

class EmotionRecognitionApp:
    """Main application class"""
    
    def __init__(self):
        # Initialize Tkinter root
        self.root = tk.Tk()
        
        # Initialize components
        self.model_manager = ModelManager()
        self.camera_handler = CameraHandler()
        self.video_recorder = VideoRecorder()
        self.emotion_logger = EmotionLogger()
        
        # Initialize GUI
        self.setup_gui()
        
        # Initialize models
        self.initialize_models()
        
        # Application state
        self.is_streaming = False
        
    def setup_gui(self):
        """Setup the graphical user interface"""
        # Main window
        self.main_window = MainWindow(self.root)
        main_frame = self.main_window.get_main_frame()
        
        # Configure main frame grid for 3-section layout
        main_frame.grid_rowconfigure(0, weight=0)  # Control panel (fixed height)
        main_frame.grid_rowconfigure(1, weight=1)  # Content area (expandable)
        main_frame.grid_columnconfigure(0, weight=2)  # Left side (video) - wider
        main_frame.grid_columnconfigure(1, weight=1)  # Right side (emotion panel)
        
        # 1. Control Panel - Top row, spanning both columns
        self.control_panel = ControlPanel(
            main_frame,
            self.main_window.model_var,
            self.main_window.status_var
        )
        # Place control panel at top, spanning full width
        # Control panel will handle its own grid placement
        
        # 2. Video Display - Left side of content area
        self.video_display = VideoDisplay(main_frame)
        # Video display will handle its own grid placement
        
        # 3. Emotion Panel - Right side of content area  
        self.emotion_panel = EmotionPanel(
            main_frame,
            self.main_window.emotion_var,
            self.main_window.confidence_var
        )
        # Emotion panel will handle its own grid placement
        
        # Set button commands
        self.control_panel.set_button_commands(
            self.toggle_stream,
            self.toggle_recording
        )
        
        # Pass model manager to control panel for status window
        self.control_panel.set_model_manager(self.model_manager)
    
    def initialize_models(self):
        """Initialize emotion detection models"""
        available_models = self.model_manager.get_available_models()
        
        if not available_models:
            messagebox.showwarning(
                "Cảnh báo",
                "Không có model nào khả dụng! Vui lòng cài đặt FER hoặc DeepFace."
            )
            available_models = ["Không có model"]
        
        self.control_panel.update_model_list(available_models)
    
    def toggle_stream(self):
        """Toggle video streaming on/off"""
        if not self.is_streaming:
            self.start_stream()
        else:
            self.stop_stream()
    
    def start_stream(self):
        """Start video streaming"""
        # Check if model is selected
        selected_model = self.main_window.model_var.get()
        if not selected_model or selected_model == "Không có model":
            messagebox.showerror("Lỗi", "Vui lòng chọn model nhận dạng!")
            return
        
        # Start camera
        if not self.camera_handler.start_camera(config.CAMERA_INDEX):
            messagebox.showerror("Lỗi", "Không thể mở camera!")
            return
        
        # Start streaming
        if self.camera_handler.start_streaming(self.process_frame):
            self.is_streaming = True
            self.control_panel.update_start_button("Dừng")
            self.main_window.status_var.set("Đang stream...")
        else:
            messagebox.showerror("Lỗi", "Không thể bắt đầu stream!")
    
    def stop_stream(self):
        """Stop video streaming"""
        self.is_streaming = False
        self.camera_handler.stop_streaming()
        self.camera_handler.stop_camera()
        
        self.control_panel.update_start_button("Bắt đầu")
        self.main_window.status_var.set("Đã dừng")
        
        # Stop recording if active
        if self.video_recorder.is_recording_active():
            self.stop_recording()
    
    def toggle_recording(self):
        """Toggle video recording on/off"""
        if not self.video_recorder.is_recording_active():
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start video recording"""
        if not self.is_streaming:
            messagebox.showwarning("Cảnh báo", "Vui lòng bắt đầu stream trước khi ghi!")
            return
        
        # Ask for save location with more format options
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            initialvalue=self.video_recorder.get_default_filename(),
            filetypes=config.SUPPORTED_VIDEO_FORMATS,
            title="Chọn vị trí lưu video"
        )
        
        if filename:
            if self.video_recorder.start_recording(
                filename, 
                config.DEFAULT_FPS, 
                (config.FRAME_WIDTH, config.FRAME_HEIGHT)
            ):
                self.control_panel.update_record_button("Dừng ghi")
                
                # Start logging
                session_name = os.path.splitext(os.path.basename(filename))[0]
                self.emotion_logger.start_logging(session_name)
                
                # Update status with recording info
                import os
                import time
                file_size_mb = 0
                folder_path = os.path.dirname(filename)
                file_name = os.path.basename(filename)
                file_ext = os.path.splitext(filename)[1].upper()
                
                self.main_window.status_var.set(f"REC Đang ghi {file_ext} - {file_name}")
                
                # Show recording info dialog
                self.show_recording_info(filename)
                
                # Start recording timer
                self.recording_start_time = time.time()
                self.update_recording_status()
            else:
                messagebox.showerror("Lỗi", "Không thể bắt đầu ghi video!")
    
    def stop_recording(self):
        """Stop video recording"""
        if self.video_recorder.is_recording_active():
            recording_duration = time.time() - self.recording_start_time if hasattr(self, 'recording_start_time') else 0
            saved_file = self.video_recorder.get_current_filename()
            
            self.video_recorder.stop_recording()
            
            # Stop logging and get summary
            log_summary = self.emotion_logger.stop_logging()
            
            self.control_panel.update_record_button("Ghi hình")
            
            # Show completion info with log details
            self.show_recording_completed(saved_file, recording_duration, log_summary)
        
        if self.is_streaming:
            self.main_window.status_var.set("Đang stream...")
        else:
            self.main_window.status_var.set("Sẵn sàng")
    
    def update_recording_status(self):
        """Update recording status periodically"""
        if self.video_recorder.is_recording_active():
            import time
            duration = time.time() - self.recording_start_time if hasattr(self, 'recording_start_time') else 0
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            
            # Get file size
            current_file = self.video_recorder.get_current_filename()
            file_size = self.get_file_size_mb(current_file)
            
            status_text = f"REC {minutes:02d}:{seconds:02d} - {file_size:.1f}MB"
            self.main_window.status_var.set(status_text)
            
            # Schedule next update
            self.root.after(1000, self.update_recording_status)
    
    def show_recording_info(self, filename):
        """Show recording information dialog"""
        import os
        import time
        
        folder_path = os.path.dirname(filename)
        file_name = os.path.basename(filename)
        file_ext = os.path.splitext(filename)[1].upper()
        
        info_text = f"""BẮT ĐẦU GHI HÌNH

Thư mục: {folder_path}
Tên file: {file_name}
Định dạng: {file_ext}
FPS: {config.DEFAULT_FPS}
Độ phân giải: {config.FRAME_WIDTH}x{config.FRAME_HEIGHT}

LOGGING:
Log folder: output/
CSV data: Có
JSON data: Có
Summary: Có

Thời gian bắt đầu: {time.strftime('%H:%M:%S')}

Nhấn "Dừng ghi" để kết thúc"""
        
        messagebox.showinfo("Thông tin ghi hình", info_text)
    
    def show_recording_completed(self, filename, duration, log_summary):
        """Show recording completion dialog"""
        import os
        
        if not filename or not os.path.exists(filename):
            messagebox.showwarning("Cảnh báo", "File không tồn tại!")
            return
        
        file_size = self.get_file_size_mb(filename)
        folder_path = os.path.dirname(filename)
        file_name = os.path.basename(filename)
        
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        
        # Add log summary to completion message
        log_info = ""
        if log_summary:
            total_records = log_summary.get('total_records', 0)
            most_common = log_summary.get('most_common_emotion', 'N/A')
            avg_confidence = log_summary.get('confidence_stats', {}).get('average', 0)
            log_info = f"""
LOG SUMMARY:
Số bản ghi: {total_records}
Cảm xúc chính: {most_common}
Độ tin cậy TB: {avg_confidence:.2%}
"""
        
        completion_text = f"""GHI HÌNH HOÀN TẤT

FILE VIDEO:
Tên: {file_name}
Vị trí: {folder_path}
Thời lượng: {minutes:02d}:{seconds:02d}
Kích thước: {file_size:.1f}MB
{log_info}
FILES LOG:
Vị trí: output/
- CSV data file
- JSON data file  
- Text summary file

Bạn có muốn mở thư mục output?"""
        
        result = messagebox.askyesno("Ghi hình hoàn tất", completion_text)
        if result:
            self.open_file_location("output")
    
    def get_file_size_mb(self, filename):
        """Get file size in MB"""
        try:
            import os
            if os.path.exists(filename):
                size_bytes = os.path.getsize(filename)
                return size_bytes / (1024 * 1024)
        except:
            pass
        return 0.0
    
    def open_file_location(self, folder_path):
        """Open file location in explorer"""
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                subprocess.run(['explorer', folder_path])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', folder_path])
            else:  # Linux
                subprocess.run(['xdg-open', folder_path])
        except Exception as e:
            print(f"Could not open folder: {e}")

    def process_frame(self, frame):
        """Process each video frame"""
        # Get selected model
        selected_model = self.main_window.model_var.get()
        
        # Detect emotion
        emotion, confidence, faces = self.model_manager.detect_emotion(selected_model, frame)
        
        # Log emotion data if logging is active
        if self.emotion_logger.is_active():
            self.emotion_logger.log_emotion(emotion, confidence, selected_model, len(faces))
        
        # Draw face rectangles and emotion labels
        frame_with_annotations = self.camera_handler.draw_face_rectangles(
            frame.copy(), faces, emotion, confidence
        )
        
        # Update GUI in main thread
        self.root.after(0, self.update_gui, emotion, confidence, frame_with_annotations)
        
        # Record frame if recording
        if self.video_recorder.is_recording_active():
            self.video_recorder.write_frame(frame_with_annotations)
    
    def update_gui(self, emotion, confidence, frame):
        """Update GUI with new emotion data and video frame"""
        # Update emotion information
        self.emotion_panel.update_emotion_info(emotion, confidence)
        
        # Update video display
        img_tk = self.camera_handler.frame_to_tkinter(frame)
        self.video_display.update_frame(img_tk)
    
    def run(self):
        """Run the application"""
        try:
            print("Đang khởi động ứng dụng nhận dạng cảm xúc...")
            print(f"Models khả dụng: {self.model_manager.get_available_models()}")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Ứng dụng đã được dừng bởi người dùng")
        except Exception as e:
            print(f"Lỗi ứng dụng: {e}")
            messagebox.showerror("Lỗi", f"Lỗi ứng dụng: {str(e)}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources before exit"""
        if self.is_streaming:
            self.stop_stream()
        if self.video_recorder.is_recording_active():
            self.stop_recording()
        if self.emotion_logger.is_active():
            self.emotion_logger.stop_logging()

def main():
    """Main entry point"""
    print("=" * 50)
    print("EMOTION RECOGNITION APP")
    print("Ứng dụng nhận dạng cảm xúc khuôn mặt")
    print("=" * 50)
    
    try:
        app = EmotionRecognitionApp()
        app.run()
    except Exception as e:
        print(f"Lỗi khởi động ứng dụng: {e}")
        messagebox.showerror("Lỗi", f"Không thể khởi động ứng dụng: {str(e)}")

if __name__ == "__main__":
    main()
    main()
