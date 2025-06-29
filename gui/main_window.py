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
        
        # Set window icon if available
        try:
            # You can add an icon file here
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass
        
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
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
    
    def get_main_frame(self):
        """Get main frame for adding components"""
        return self.main_frame
