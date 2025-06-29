"""
Video display component
"""
import tkinter as tk
from tkinter import ttk

class VideoDisplay:
    """Video stream display component"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_video_display()
    
    def setup_video_display(self):
        """Setup video display layout"""
        # Video frame - positioned in content area, left side
        self.video_frame = ttk.LabelFrame(
            self.parent_frame, 
            text="Video Stream", 
            padding="10"
        )
        self.video_frame.grid(
            row=1, column=0, 
            sticky=(tk.W, tk.E, tk.N, tk.S), 
            padx=(5, 10), pady=(0, 5)
        )
        
        # Video label for displaying frames with placeholder
        self.video_label = ttk.Label(
            self.video_frame,
            text="Camera chưa được khởi động\n\nNhấn 'Bắt đầu' để bắt đầu stream",
            font=("Arial", 12),
            background="lightgray",
            anchor="center",
            justify="center"
        )
        self.video_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Configure grid weights for proper resizing
        self.video_frame.columnconfigure(0, weight=1)
        self.video_frame.rowconfigure(0, weight=1)
    
    def update_frame(self, img_tk):
        """Update video frame"""
        self.video_label.configure(image=img_tk)
        self.video_label.image = img_tk
