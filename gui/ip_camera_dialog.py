"""
IP Camera configuration dialog
"""
import tkinter as tk
from tkinter import ttk, messagebox

class IPCameraDialog:
    """Dialog for configuring IP camera connection"""
    
    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Cấu hình IP Camera")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_dialog()
        self.center_dialog()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_dialog(self):
        """Setup dialog components"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with small logo
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Small logo
        try:
            import os
            from PIL import Image, ImageTk
            
            logo_path = os.path.join("img_logo", "logo.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                img = img.resize((72, 24), Image.Resampling.LANCZOS)  # 72 = 24 * 3
                logo_photo = ImageTk.PhotoImage(img)
                
                logo_label = ttk.Label(header_frame, image=logo_photo)
                logo_label.image = logo_photo
                logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception:
            pass
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="Cấu hình IP Camera",
            font=("Arial", 12, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Protocol selection
        protocol_frame = ttk.LabelFrame(main_frame, text="Giao thức", padding="10")
        protocol_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.protocol_var = tk.StringVar(value="http")
        protocols = [("HTTP", "http"), ("HTTPS", "https"), ("RTSP", "rtsp"), ("RTMP", "rtmp")]
        
        for i, (text, value) in enumerate(protocols):
            ttk.Radiobutton(
                protocol_frame,
                text=text,
                variable=self.protocol_var,
                value=value
            ).grid(row=0, column=i, padx=5, sticky=tk.W)
        
        # Connection details
        details_frame = ttk.LabelFrame(main_frame, text="Thông tin kết nối", padding="10")
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        # IP Address
        ttk.Label(details_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ip_entry = ttk.Entry(details_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=(5, 0), pady=2, sticky=tk.W)
        self.ip_entry.insert(0, "192.168.1.100")
        
        # Port
        ttk.Label(details_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.port_entry = ttk.Entry(details_frame, width=20)
        self.port_entry.grid(row=1, column=1, padx=(5, 0), pady=2, sticky=tk.W)
        self.port_entry.insert(0, "8080")
        
        # Path
        ttk.Label(details_frame, text="Path:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.path_entry = ttk.Entry(details_frame, width=20)
        self.path_entry.grid(row=2, column=1, padx=(5, 0), pady=2, sticky=tk.W)
        self.path_entry.insert(0, "/video")
        
        # Authentication (optional)
        auth_frame = ttk.LabelFrame(main_frame, text="Xác thực (tùy chọn)", padding="10")
        auth_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(auth_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.username_entry = ttk.Entry(auth_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=(5, 0), pady=2, sticky=tk.W)
        
        ttk.Label(auth_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.password_entry = ttk.Entry(auth_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=(5, 0), pady=2, sticky=tk.W)
        
        # Preview URL
        preview_frame = ttk.LabelFrame(main_frame, text="URL Preview", padding="10")
        preview_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.url_var = tk.StringVar()
        self.url_label = ttk.Label(preview_frame, textvariable=self.url_var, font=("Courier", 9))
        self.url_label.pack(fill=tk.X)
        
        # Bind events to update preview
        for entry in [self.ip_entry, self.port_entry, self.path_entry, self.username_entry, self.password_entry]:
            entry.bind('<KeyRelease>', self.update_preview)
        
        for radio in protocol_frame.winfo_children():
            if isinstance(radio, ttk.Radiobutton):
                radio.configure(command=self.update_preview)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Hủy",
            command=self.cancel
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(
            button_frame,
            text="OK",
            command=self.ok
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame,
            text="Test Connection",
            command=self.test_connection
        ).pack(side=tk.LEFT)
        
        # Update initial preview
        self.update_preview()
    
    def update_preview(self, event=None):
        """Update URL preview"""
        protocol = self.protocol_var.get()
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        path = self.path_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not path.startswith('/'):
            path = '/' + path
        
        if username and password:
            url = f"{protocol}://{username}:{password}@{ip}:{port}{path}"
        else:
            url = f"{protocol}://{ip}:{port}{path}"
        
        self.url_var.set(url)
    
    def test_connection(self):
        """Test camera connection"""
        try:
            import cv2
            url = self.url_var.get()
            
            if not url.strip():
                messagebox.showerror("Lỗi", "URL không hợp lệ!")
                return
            
            # Try to open connection
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    messagebox.showinfo("Thành công", "Kết nối camera thành công!")
                else:
                    messagebox.showerror("Lỗi", "Không thể đọc dữ liệu từ camera!")
                cap.release()
            else:
                messagebox.showerror("Lỗi", "Không thể kết nối đến camera!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi test kết nối: {e}")
    
    def ok(self):
        """OK button clicked"""
        url = self.url_var.get().strip()
        if url:
            self.result = url
            self.dialog.destroy()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập thông tin camera!")
    
    def cancel(self):
        """Cancel button clicked"""
        self.result = None
        self.dialog.destroy()
    
    def center_dialog(self):
        """Center dialog on screen"""
        self.dialog.update_idletasks()
        
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
