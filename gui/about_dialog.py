"""
About dialog with logo and application information
"""
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class AboutDialog:
    """About dialog showing application information and logo"""
    
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("About - Emotion Recognition App")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
        self.center_dialog()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_dialog(self):
        """Setup dialog components"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo section
        self.add_logo_section(main_frame)
        
        # App info section
        self.add_app_info_section(main_frame)
        
        # Credits section
        self.add_credits_section(main_frame)
        
        # Close button
        ttk.Button(
            main_frame,
            text="Đóng",
            command=self.dialog.destroy,
            width=15
        ).pack(pady=(20, 0))
    
    def add_logo_section(self, parent):
        """Add logo section"""
        logo_frame = ttk.Frame(parent)
        logo_frame.pack(fill=tk.X, pady=(0, 20))
        
        try:
            logo_path = os.path.join("img_logo", "logo.png")
            if os.path.exists(logo_path):
                # Load and display logo - width 3x longer
                img = Image.open(logo_path)
                img = img.resize((384, 128), Image.Resampling.LANCZOS)  # 384 = 128 * 3
                logo_photo = ImageTk.PhotoImage(img)
                
                logo_label = ttk.Label(logo_frame, image=logo_photo)
                logo_label.image = logo_photo  # Keep reference
                logo_label.pack()
            else:
                # Fallback text
                ttk.Label(
                    logo_frame,
                    text="🎭",
                    font=("Arial", 48)
                ).pack()
                
        except Exception as e:
            print(f"Error loading logo in about dialog: {e}")
            # Fallback text
            ttk.Label(
                logo_frame,
                text="🎭",
                font=("Arial", 48)
            ).pack()
    
    def add_app_info_section(self, parent):
        """Add application information"""
        info_frame = ttk.LabelFrame(parent, text="Thông tin ứng dụng", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        app_info = [
            ("Tên ứng dụng:", "Emotion Recognition App"),
            ("Phiên bản:", "1.0.0"),
            ("Mô tả:", "Ứng dụng nhận dạng cảm xúc khuôn mặt realtime"),
            ("Ngôn ngữ:", "Python 3.8+"),
            ("Framework:", "Tkinter + OpenCV + AI Models"),
            ("Tác giả:", "Your Name"),
            ("Ngày phát hành:", "2024")
        ]
        
        for i, (label, value) in enumerate(app_info):
            row_frame = ttk.Frame(info_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(
                row_frame,
                text=label,
                font=("Arial", 9, "bold"),
                width=15,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            ttk.Label(
                row_frame,
                text=value,
                font=("Arial", 9),
                anchor=tk.W
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def add_credits_section(self, parent):
        """Add credits section"""
        credits_frame = ttk.LabelFrame(parent, text="Credits & Libraries", padding="10")
        credits_frame.pack(fill=tk.X, pady=(0, 15))
        
        credits_text = """• OpenCV - Computer Vision
• TensorFlow/PyTorch - Deep Learning
• FER - Facial Emotion Recognition
• DeepFace - Face Analysis
• MediaPipe - Face Detection
• Dlib - Facial Landmarks
• Pillow - Image Processing
• Tkinter - GUI Framework

Cảm ơn tất cả các thư viện mã nguồn mở!"""
        
        credits_label = ttk.Label(
            credits_frame,
            text=credits_text,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        credits_label.pack(anchor=tk.W)
    
    def center_dialog(self):
        """Center dialog on screen"""
        self.dialog.update_idletasks()
        
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
