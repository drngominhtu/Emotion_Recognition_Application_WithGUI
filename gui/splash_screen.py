"""
Splash screen with logo for application startup
"""
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import threading
import time

class SplashScreen:
    """Splash screen displayed during application startup"""
    
    def __init__(self, duration=3):
        self.duration = duration
        self.splash = tk.Tk()
        self.splash.withdraw()  # Hide initially
        
        self.setup_splash()
        
    def setup_splash(self):
        """Setup splash screen"""
        # Configure window
        self.splash.title("Loading...")
        self.splash.overrideredirect(True)  # Remove title bar
        self.splash.configure(bg='white')
        
        # Get screen dimensions
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        # Splash dimensions
        splash_width = 400
        splash_height = 300
        
        # Center splash
        x = (screen_width // 2) - (splash_width // 2)
        y = (screen_height // 2) - (splash_height // 2)
        
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(self.splash, bg='white', padx=40, pady=40)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo
        self.add_logo(main_frame)
        
        # App title
        title_label = tk.Label(
            main_frame,
            text="Emotion Recognition App",
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="AI-Powered Facial Emotion Detection",
            font=("Arial", 11),
            bg='white',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Đang khởi tạo...")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg='white',
            fg='#95a5a6'
        )
        status_label.pack()
        
        # Version
        version_label = tk.Label(
            main_frame,
            text="v1.0.0",
            font=("Arial", 8),
            bg='white',
            fg='#bdc3c7'
        )
        version_label.pack(side=tk.BOTTOM, anchor=tk.SE)
    
    def add_logo(self, parent):
        """Add logo to splash screen"""
        try:
            logo_path = os.path.join("img_logo", "logo.png")
            if os.path.exists(logo_path):
                # Load and display logo - width 3x longer
                img = Image.open(logo_path)
                img = img.resize((300, 100), Image.Resampling.LANCZOS)  # 300 = 100 * 3
                logo_photo = ImageTk.PhotoImage(img)
                
                logo_label = tk.Label(parent, image=logo_photo, bg='white')
                logo_label.image = logo_photo  # Keep reference
                logo_label.pack()
            else:
                # Fallback emoji
                logo_label = tk.Label(
                    parent,
                    text="🎭",
                    font=("Arial", 64),
                    bg='white'
                )
                logo_label.pack()
                
        except Exception as e:
            print(f"Error loading logo in splash: {e}")
            # Fallback emoji
            logo_label = tk.Label(
                parent,
                text="🎭",
                font=("Arial", 64),
                bg='white'
            )
            logo_label.pack()
    
    def show(self, status_updates=None):
        """Show splash screen with optional status updates"""
        self.splash.deiconify()  # Show window
        self.splash.lift()
        self.splash.attributes('-topmost', True)
        
        # Start progress animation
        self.progress.start(10)
        
        # Update status if provided
        if status_updates:
            self._animate_status(status_updates)
        
        # Auto close after duration
        self.splash.after(self.duration * 1000, self.close)
        
        # Start main loop
        self.splash.mainloop()
    
    def _animate_status(self, status_updates):
        """Animate status updates"""
        def update_status():
            for i, status in enumerate(status_updates):
                self.splash.after(i * 500, lambda s=status: self.status_var.set(s))
        
        threading.Thread(target=update_status, daemon=True).start()
    
    def close(self):
        """Close splash screen"""
        try:
            self.progress.stop()
            self.splash.destroy()
        except:
            pass
    
    def update_status(self, status):
        """Update status text"""
        self.status_var.set(status)
        self.splash.update()

# Usage function
def show_splash_screen():
    """Show splash screen with loading sequence"""
    status_updates = [
        "Đang khởi tạo...",
        "Đang tải models AI...",
        "Đang kiểm tra camera...",
        "Đang chuẩn bị giao diện...",
        "Hoàn tất!"
    ]
    
    splash = SplashScreen(duration=4)
    splash.show(status_updates)
