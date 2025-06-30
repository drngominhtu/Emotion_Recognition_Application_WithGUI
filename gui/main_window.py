"""
Main application window GUI components
"""
import tkinter as tk
from tkinter import ttk

class MainWindow:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_variables()
        self.setup_layout()
    
    def setup_window(self):
        """Configure main window"""
        self.root.title("Nhận dạng cảm xúc khuôn mặt - Realtime")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set window icon
        self.set_window_icon()
        
        # Center window on screen
        self.center_window()
    
    def set_window_icon(self):
        """Set window icon from logo"""
        try:
            import os
            from PIL import Image, ImageTk
            
            logo_path = os.path.join("img_logo", "logo.png")
            if os.path.exists(logo_path):
                # Load and resize logo for window icon - maintain aspect ratio
                img = Image.open(logo_path)
                img = img.resize((96, 32), Image.Resampling.LANCZOS)  # 96 = 32 * 3
                icon = ImageTk.PhotoImage(img)
                
                # Set as window icon
                self.root.iconphoto(True, icon)
                print("Logo set as window icon")
            else:
                print(f"Logo not found at: {logo_path}")
                
        except Exception as e:
            print(f"Error setting window icon: {e}")

        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        
        width = 1200
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_variables(self):
        """Create tkinter variables"""
        self.model_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Sẵn sàng")
        self.emotion_var = tk.StringVar(value="Chưa phát hiện")
        self.confidence_var = tk.StringVar(value="0%")
    
    def setup_layout(self):
        """Setup main layout"""
        # Main frame with better padding
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add logo header
        self.add_logo_header()
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
    
    def add_logo_header(self):
        """Add logo header to main window"""
        try:
            import os
            from PIL import Image, ImageTk
            
            logo_path = os.path.join("img_logo", "logo.png")
            if os.path.exists(logo_path):
                # Create header frame
                header_frame = ttk.Frame(self.main_frame)
                header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
                
                # Load and resize logo for header - width 3x longer
                img = Image.open(logo_path)
                img = img.resize((192, 64), Image.Resampling.LANCZOS)  # 192 = 64 * 3
                logo_photo = ImageTk.PhotoImage(img)
                
                # Logo label
                logo_label = ttk.Label(header_frame, image=logo_photo)
                logo_label.image = logo_photo  # Keep reference
                logo_label.pack(side=tk.LEFT, padx=(0, 10))
                
                # Title label
                title_label = ttk.Label(
                    header_frame,
                    text="Emotion Recognition App",
                    font=("Arial", 16, "bold")
                )
                title_label.pack(side=tk.LEFT, anchor=tk.W)
                
                # Version label
                version_label = ttk.Label(
                    header_frame,
                    text="v1.0.0",
                    font=("Arial", 10),
                    foreground="gray"
                )
                version_label.pack(side=tk.RIGHT, anchor=tk.E)
                
        except Exception as e:
            print(f"Error adding logo header: {e}")

    def get_main_frame(self):
        """Get main frame for adding components"""
        return self.main_frame
