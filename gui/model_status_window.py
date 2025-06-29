"""
Model status window to show which models are available
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ModelStatusWindow:
    """Window showing status of all emotion recognition models"""
    
    def __init__(self, parent, model_manager):
        self.parent = parent
        self.model_manager = model_manager
        self.window = None
    
    def show(self):
        """Show the model status window"""
        if self.window:
            self.window.lift()
            return
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Trạng thái Models")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # Make window modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        self.setup_window()
        
        # Center window
        self.center_window()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
    
    def setup_window(self):
        """Setup the window content"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Trạng thái Models Nhận dạng Cảm xúc",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create treeview for model status
        columns = ("Model", "Status", "Requirements")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("Model", text="Model")
        self.tree.heading("Status", text="Trạng thái")
        self.tree.heading("Requirements", text="Yêu cầu cài đặt")
        
        self.tree.column("Model", width=200)
        self.tree.column("Status", width=100)
        self.tree.column("Requirements", width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate tree
        self.populate_tree()
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Refresh button
        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_status
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Install guide button
        ttk.Button(
            button_frame,
            text="Hướng dẫn cài đặt",
            command=self.show_install_guide
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        ttk.Button(
            button_frame,
            text="Đóng",
            command=self.close_window
        ).pack(side=tk.RIGHT)
    
    def populate_tree(self):
        """Populate the tree with model status"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Model definitions
        models_info = [
            ("FER (Fast)", "fer", "pip install fer"),
            ("DeepFace - VGG-Face", "deepface", "pip install deepface"),
            ("DeepFace - Facenet", "deepface", "pip install deepface"),
            ("DeepFace - OpenFace", "deepface", "pip install deepface"),
            ("MediaPipe + Heuristics", "mediapipe", "pip install mediapipe transformers"),
            ("MTCNN + Landmarks", "facenet-pytorch", "pip install facenet-pytorch torch"),
            ("Dlib + 68 Landmarks", "dlib", "pip install dlib"),
            ("Simple CNN", "tensorflow", "pip install tensorflow"),
            ("OpenCV Basic", "opencv-python", "Có sẵn")
        ]
        
        available_models = self.model_manager.get_available_models()
        
        for model_name, requirement, install_cmd in models_info:
            # Check if model is available
            is_available = any(model_name in available for available in available_models)
            
            status = "Có sẵn" if is_available else "Chưa cài"
            status_tag = "available" if is_available else "unavailable"
            
            self.tree.insert("", tk.END, values=(model_name, status, install_cmd), tags=(status_tag,))
        
        # Configure tags
        self.tree.tag_configure("available", background="#d4edda", foreground="#155724")
        self.tree.tag_configure("unavailable", background="#f8d7da", foreground="#721c24")
    
    def refresh_status(self):
        """Refresh model status"""
        # Reinitialize model manager
        try:
            from models.model_manager import ModelManager
            self.model_manager = ModelManager()
            self.populate_tree()
        except Exception as e:
            print(f"Error refreshing models: {e}")
    
    def show_install_guide(self):
        """Show detailed installation guide"""
        guide_text = """HƯỚNG DẪN CÀI ĐẶT CHI TIẾT

CÀI ĐẶT CƠ BẢN (khuyến nghị):
pip install fer deepface

CÀI ĐẶT ĐẦY ĐỦ:
pip install fer deepface mediapipe transformers facenet-pytorch torch dlib tensorflow

CÀI ĐẶT TỪNG MODEL:

FER (Fast, nhẹ):
pip install fer

DeepFace (chính xác cao):
pip install deepface

MediaPipe (Google):
pip install mediapipe transformers

MTCNN (PyTorch):
pip install facenet-pytorch torch

Dlib (landmarks):
pip install dlib
# Cần Visual C++ trên Windows

TensorFlow CNN:
pip install tensorflow

LƯU Ý:
• Khởi động lại ứng dụng sau khi cài
• Một số model cần download weights lần đầu
• Dlib cần thêm file landmarks (tùy chọn)
• Models AI sẽ chậm hơn OpenCV"""
        
        # Create guide window
        guide_window = tk.Toplevel(self.window)
        guide_window.title("Hướng dẫn cài đặt")
        guide_window.geometry("500x600")
        guide_window.resizable(False, False)
        
        # Make modal
        guide_window.transient(self.window)
        guide_window.grab_set()
        
        # Text widget with scrollbar
        frame = ttk.Frame(guide_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar_guide = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar_guide.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_guide.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert("1.0", guide_text)
        text_widget.configure(state="disabled")
        
        # Close button
        ttk.Button(
            guide_window,
            text="Đóng",
            command=guide_window.destroy
        ).pack(pady=10)
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def close_window(self):
        """Close the window"""
        if self.window:
            self.window.grab_release()
            self.window.destroy()
            self.window = None
