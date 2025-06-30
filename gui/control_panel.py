"""
Control panel GUI components
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import config
except ImportError:
    config = None

class ControlPanel:
    """Control panel with model selection and action buttons"""
    
    def __init__(self, parent_frame, model_var, status_var):
        self.parent_frame = parent_frame
        self.model_var = model_var
        self.status_var = status_var
        
        self.setup_control_panel()
    
    def setup_control_panel(self):
        """Setup control panel layout"""
        # Control panel frame - spans full width at top
        self.control_frame = ttk.LabelFrame(
            self.parent_frame, 
            text="Điều khiển", 
            padding="10"
        )
        self.control_frame.grid(
            row=0, column=0, columnspan=2,
            sticky=(tk.W, tk.E), 
            padx=5, pady=(5, 10)
        )
        
        # Configure grid for horizontal layout
        self.control_frame.columnconfigure(1, weight=1)
        self.control_frame.columnconfigure(3, weight=1)
        
        # Row 1: Model selection and camera
        ttk.Label(self.control_frame, text="Model:").grid(
            row=0, column=0, padx=(0, 5), sticky=tk.W
        )
        
        self.model_combo = ttk.Combobox(
            self.control_frame, 
            textvariable=self.model_var,
            state="readonly",
            width=25
        )
        self.model_combo.grid(row=0, column=1, padx=(0, 20), sticky=tk.W)
        self.model_combo.bind("<<ComboboxSelected>>", self.on_model_selected)
        
        # Camera selection with more options
        ttk.Label(self.control_frame, text="Camera:").grid(
            row=0, column=2, padx=(0, 5), sticky=tk.W
        )
        
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.camera_var,
            width=20,
            values=self._get_default_camera_options()
        )
        self.camera_combo.grid(row=0, column=3, padx=(0, 20), sticky=tk.W)
        self.camera_combo.set("Camera 0 (Mặc định)")
        
        # Camera detect button
        detect_btn = ttk.Button(
            self.control_frame,
            text="Tìm Camera",
            width=10,
            command=self.detect_cameras
        )
        detect_btn.grid(row=0, column=4, padx=(0, 10))

        # Row 2: Action buttons
        button_frame = ttk.Frame(self.control_frame)
        button_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0), sticky=tk.W)
        
        self.start_btn = ttk.Button(
            button_frame, 
            text="Bắt đầu", 
            width=12
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.record_btn = ttk.Button(
            button_frame, 
            text="Ghi hình", 
            width=12
        )
        self.record_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Model info button
        self.info_btn = ttk.Button(
            button_frame,
            text="Info",
            width=8,
            command=self.show_model_info
        )
        self.info_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Model status button
        self.status_btn = ttk.Button(
            button_frame,
            text="Models",
            width=10,
            command=self.show_model_status
        )
        self.status_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # About button with logo
        self.about_btn = ttk.Button(
            button_frame,
            text="About",
            width=8,
            command=self.show_about
        )
        self.about_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Status display
        status_frame = ttk.Frame(self.control_frame)
        status_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(status_frame, text="Trạng thái:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        status_label = ttk.Label(status_frame, textvariable=self.status_var, font=("Arial", 9))
        status_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def update_model_list(self, models):
        """Update available models in dropdown"""
        self.model_combo['values'] = models
        if models:
            self.model_combo.set(models[0])
    
    def set_button_commands(self, start_command, record_command):
        """Set button command callbacks"""
        self.start_btn.config(command=start_command)
        self.record_btn.config(command=record_command)
    
    def update_start_button(self, text):
        """Update start button text"""
        self.start_btn.config(text=text)
    
    def update_record_button(self, text):
        """Update record button text"""
        self.record_btn.config(text=text)
        
        # Change button color based on recording state
        if "Dừng" in text:
            self.record_btn.configure(style="Recording.TButton")
            # Create recording style if not exists
            style = ttk.Style()
            style.configure("Recording.TButton", foreground="red")
        else:
            self.record_btn.configure(style="TButton")
    
    def on_model_selected(self, event=None):
        """Handle model selection change"""
        selected_model = self.model_var.get()
        if selected_model and config and hasattr(config, 'MODEL_INFO'):
            model_info = config.MODEL_INFO.get(selected_model, {})
            accuracy = model_info.get('accuracy', 'Unknown')
            speed = model_info.get('speed', 'Unknown')
            
            # Update status with model info
            status_text = f"Model: {accuracy} accuracy, {speed} speed"
            self.status_var.set(status_text)
    
    def show_model_info(self):
        """Show detailed information about the selected model"""
        selected_model = self.model_var.get()
        if not selected_model:
            messagebox.showinfo("Thông tin", "Vui lòng chọn một model!")
            return
        
        if config and hasattr(config, 'MODEL_INFO'):
            model_info = config.MODEL_INFO.get(selected_model, {})
            description = model_info.get('description', 'Không có mô tả')
            accuracy = model_info.get('accuracy', 'Unknown')
            speed = model_info.get('speed', 'Unknown')
            
            info_text = f"""Model: {selected_model}

Mô tả: {description}

Đặc điểm:
• Độ chính xác: {accuracy}
• Tốc độ: {speed}

{self._get_model_requirements(selected_model)}"""
            
            messagebox.showinfo("Thông tin Model", info_text)
        else:
            messagebox.showinfo("Thông tin", f"Model được chọn: {selected_model}")
    
    def _get_model_requirements(self, model_name):
        """Get installation requirements for specific model"""
        requirements = {
            "FER (Fast)": "Cài đặt: pip install fer",
            "DeepFace - VGG-Face": "Cài đặt: pip install deepface",
            "DeepFace - Facenet": "Cài đặt: pip install deepface",
            "DeepFace - OpenFace": "Cài đặt: pip install deepface",
            "MediaPipe + Heuristics": "Cài đặt: pip install mediapipe transformers",
            "MTCNN + Landmarks": "Cài đặt: pip install facenet-pytorch torch",
            "Dlib + 68 Landmarks": "Cài đặt: pip install dlib + download landmarks file",
            "Dlib + HOG Features": "Cài đặt: pip install dlib",
            "Simple CNN": "Cài đặt: pip install tensorflow",
            "OpenCV Basic": "Đã có sẵn - không cần cài thêm"
        }
        
        return requirements.get(model_name, "Yêu cầu: Không rõ")
    
    def show_install_info(self):
        """Show installation instructions for all models"""
        install_text = """HƯỚNG DẪN CÀI ĐẶT MODELS

Để có thêm models nhận dạng cảm xúc, cài đặt:

Cài đặt cơ bản:
pip install fer deepface

Cài đặt đầy đủ (tất cả models):
pip install fer deepface mediapipe transformers facenet-pytorch torch dlib tensorflow

Hoặc từ file requirements:
pip install -r requirements.txt

Dành cho Python 3.8:
pip install -r requirements38.txt

Lưu ý:
• Một số model cần download weights lần đầu
• Dlib cần Visual C++ trên Windows  
• Models AI sẽ chậm hơn OpenCV Basic

Sau khi cài xong, khởi động lại ứng dụng để load models mới."""
        
        messagebox.showinfo("Cài đặt Models", install_text)
    
    def show_model_status(self):
        """Show model status window"""
        try:
            from .model_status_window import ModelStatusWindow
            # We need to get model_manager from parent
            # This will be set by the main app
            if hasattr(self, 'model_manager'):
                status_window = ModelStatusWindow(self.parent_frame.winfo_toplevel(), self.model_manager)
                status_window.show()
            else:
                self.show_install_info()  # Fallback to simple info
        except ImportError:
            self.show_install_info()  # Fallback if import fails
    
    def show_output_folder(self):
        """Show output folder with logs"""
        try:
            import subprocess
            import platform
            
            output_folder = "output"
            if not os.path.exists(output_folder):
                messagebox.showinfo("Thông báo", "Chưa có folder output. Bắt đầu ghi hình để tạo log!")
                return
            
            if platform.system() == "Windows":
                subprocess.run(['explorer', os.path.abspath(output_folder)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', os.path.abspath(output_folder)])
            else:  # Linux
                subprocess.run(['xdg-open', os.path.abspath(output_folder)])
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở folder: {e}")
    
    def set_model_manager(self, model_manager):
        """Set the model manager for status window"""
        self.model_manager = model_manager
        
        # Add output folder button to the button frame
        try:
            # Find the button frame
            for child in self.control_frame.winfo_children():
                if isinstance(child, ttk.Frame):
                    # This should be our button frame
                    output_btn = ttk.Button(
                        child,
                        text="Logs",
                        width=8,
                        command=self.show_output_folder
                    )
                    output_btn.pack(side=tk.LEFT, padx=(0, 10))
                    break
        except Exception as e:
            print(f"Error adding logs button: {e}")
    
    def _get_default_camera_options(self):
        """Get default camera options"""
        return [
            "Camera 0 (Mặc định)",
            "Camera 1", 
            "Camera 2",
            "Camera 3",
            "Nhập đường dẫn...",
            "IP Camera...",
            "Video File..."
        ]
    
    def detect_cameras(self):
        """Detect available cameras"""
        try:
            # Import camera handler if available
            if hasattr(self, 'camera_handler'):
                cameras = self.camera_handler.detect_available_cameras()
            else:
                # Fallback detection
                cameras = self._fallback_camera_detection()
            
            if cameras:
                camera_options = []
                for cam in cameras:
                    option = f"Camera {cam['index']} ({cam['resolution']})"
                    camera_options.append(option)
                
                # Add special options
                camera_options.extend([
                    "---",
                    "Nhập đường dẫn...",
                    "IP Camera...", 
                    "Video File..."
                ])
                
                # Update combo box
                self.camera_combo['values'] = camera_options
                
                messagebox.showinfo("Tìm Camera", f"Tìm thấy {len(cameras)} camera(s)")
            else:
                messagebox.showwarning("Tìm Camera", "Không tìm thấy camera nào!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm camera: {e}")
    
    def _fallback_camera_detection(self):
        """Fallback camera detection without camera handler"""
        import cv2
        cameras = []
        
        for i in range(5):
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        cameras.append({
                            'index': i,
                            'resolution': f"{width}x{height}"
                        })
                cap.release()
            except:
                pass
        
        return cameras
    
    def on_camera_selected(self, event=None):
        """Handle camera selection"""
        selection = self.camera_var.get()
        
        if selection == "Nhập đường dẫn...":
            self._input_custom_path()
        elif selection == "IP Camera...":
            self._input_ip_camera()
        elif selection == "Video File...":
            self._select_video_file()
    
    def _input_custom_path(self):
        """Input custom camera path"""
        from tkinter import simpledialog
        
        path = simpledialog.askstring(
            "Đường dẫn Camera",
            "Nhập đường dẫn camera:\n\n"
            "Ví dụ:\n"
            "• 0, 1, 2... (Camera index)\n"
            "• /dev/video0 (Linux)\n"
            "• rtsp://192.168.1.100:554/stream\n"
            "• http://192.168.1.100:8080/video\n"
            "• C:/path/to/video.mp4"
        )
        
        if path:
            self.camera_var.set(path)
    
    def _input_ip_camera(self):
        """Input IP camera URL"""
        from tkinter import simpledialog
        
        # Show dialog for IP camera
        dialog = IPCameraDialog(self.control_frame)
        if dialog.result:
            self.camera_var.set(dialog.result)
    
    def _select_video_file(self):
        """Select video file"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Chọn file video",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.camera_var.set(file_path)
    
    def set_camera_handler(self, camera_handler):
        """Set camera handler for detection"""
        self.camera_handler = camera_handler
        
        # Bind camera selection event
        self.camera_combo.bind("<<ComboboxSelected>>", self.on_camera_selected)
    
    def show_about(self):
        """Show about dialog"""
        try:
            from .about_dialog import AboutDialog
            AboutDialog(self.control_frame.winfo_toplevel())
        except ImportError as e:
            messagebox.showinfo(
                "About",
                "Emotion Recognition App v1.0.0\n\n"
                "Ứng dụng nhận dạng cảm xúc khuôn mặt realtime\n"
                "Sử dụng AI và Computer Vision"
            )
