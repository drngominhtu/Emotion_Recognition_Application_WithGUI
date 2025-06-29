"""
Emotion information panel
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class EmotionPanel:
    """Panel displaying emotion information and history"""
    
    def __init__(self, parent_frame, emotion_var, confidence_var):
        self.parent_frame = parent_frame
        self.emotion_var = emotion_var
        self.confidence_var = confidence_var
        
        self.setup_emotion_panel()
    
    def setup_emotion_panel(self):
        """Setup emotion information panel"""
        # Emotion info frame - positioned in content area, right side
        self.info_frame = ttk.LabelFrame(
            self.parent_frame, 
            text="Thông tin cảm xúc", 
            padding="10"
        )
        self.info_frame.grid(
            row=1, column=1, 
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=(0, 5), pady=(0, 5)
        )
        
        # Current emotion display
        emotion_display_frame = ttk.Frame(self.info_frame)
        emotion_display_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            emotion_display_frame, 
            text="Cảm xúc hiện tại:", 
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W)
        
        self.emotion_label = ttk.Label(
            emotion_display_frame, 
            textvariable=self.emotion_var, 
            font=("Arial", 18, "bold"), 
            foreground="blue"
        )
        self.emotion_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Confidence display
        confidence_frame = ttk.Frame(self.info_frame)
        confidence_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            confidence_frame, 
            text="Độ tin cậy:", 
            font=("Arial", 11, "bold")
        ).pack(anchor=tk.W)
        
        self.confidence_label = ttk.Label(
            confidence_frame, 
            textvariable=self.confidence_var, 
            font=("Arial", 14, "bold"),
            foreground="green"
        )
        self.confidence_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Emotion history section
        history_label_frame = ttk.Frame(self.info_frame)
        history_label_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            history_label_frame, 
            text="Lịch sử cảm xúc:", 
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT)
        
        # Clear history button
        ttk.Button(
            history_label_frame,
            text="Xóa",
            width=8,
            command=self.clear_history
        ).pack(side=tk.RIGHT)
        
        self.setup_history_section()
        
        # Configure grid weights
        self.info_frame.pack_propagate(False)

    def setup_history_section(self):
        """Setup emotion history text area"""
        history_frame = ttk.Frame(self.info_frame)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget with scrollbar
        self.history_text = tk.Text(
            history_frame, 
            height=12, 
            width=35,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="white",
            fg="black"
        )
        
        scrollbar = ttk.Scrollbar(
            history_frame, 
            orient=tk.VERTICAL, 
            command=self.history_text.yview
        )
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add initial message
        self.history_text.insert(tk.END, "Chưa có dữ liệu cảm xúc...\n")
        self.history_text.config(state=tk.DISABLED)
    
    def update_emotion_info(self, emotion, confidence):
        """Update emotion information and add to history"""
        # Update current emotion display
        self.emotion_var.set(emotion.title())
        self.confidence_var.set(f"{confidence:.1%}")
        
        # Update label colors based on confidence
        if confidence > 0.8:
            self.confidence_label.configure(foreground="green")
        elif confidence > 0.6:
            self.confidence_label.configure(foreground="orange")
        else:
            self.confidence_label.configure(foreground="red")
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {emotion.title()} ({confidence:.1%})\n"
        
        self.history_text.config(state=tk.NORMAL)
        
        # Clear initial message if still there
        content = self.history_text.get("1.0", tk.END).strip()
        if content == "Chưa có dữ liệu cảm xúc...":
            self.history_text.delete("1.0", tk.END)
        
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        
        # Keep only last 100 entries
        lines = self.history_text.get("1.0", tk.END).split('\n')
        if len(lines) > 100:
            self.history_text.delete("1.0", "2.0")
        
        self.history_text.config(state=tk.DISABLED)
    
    def clear_history(self):
        """Clear emotion history"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        self.history_text.insert(tk.END, "Lịch sử đã được xóa...\n")
        self.history_text.config(state=tk.DISABLED)
