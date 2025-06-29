# 🐍 Python 3.8 Installation Guide

Hướng dẫn cài đặt tối ưu cho **Python 3.8.x**

## 🚀 Cài đặt nhanh

### Phương pháp 1: Script tự động (Khuyến nghị)
```bash
python install_python38.py
```

### Phương pháp 2: Requirements file
```bash
pip install -r requirements38.txt
```

### Phương pháp 3: Từng bước
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Core packages
pip install opencv-python>=4.5.0,<4.9.0
pip install pillow>=8.0.0,<10.0.0  
pip install numpy>=1.19.0,<1.25.0

# ML packages
pip install fer>=22.4.0
pip install "deepface>=0.0.75,<0.0.85"
pip install "mediapipe>=0.8.9,<0.11.0"
pip install "transformers>=4.15.0,<4.25.0"
pip install "torch>=1.9.0,<1.14.0"
pip install "tensorflow>=2.6.0,<2.11.0"
```

## ⚠️ Python 3.8 Specific Notes

### Version Constraints
- **TensorFlow**: 2.6.0 - 2.10.x (2.11+ drops Python 3.8 support)
- **NumPy**: < 1.25.0 (newer versions require Python 3.9+)
- **MediaPipe**: < 0.11.0 for stability
- **Transformers**: < 4.25.0 for compatibility

### Known Issues & Solutions

#### 1. TensorFlow Installation
```bash
# If latest TensorFlow fails:
pip install tensorflow==2.10.1

# For CPU only (lighter):
pip install tensorflow-cpu==2.10.1
```

#### 2. Dlib on Windows
```bash
# Option 1: Pre-compiled wheel
pip install dlib

# Option 2: If fails, use conda
conda install -c conda-forge dlib

# Option 3: Manual build (requires Visual C++)
# Download Visual C++ Build Tools first
```

#### 3. PyTorch with CUDA (Optional)
```bash
# For CUDA 11.6
pip install torch==1.13.1+cu116 -f https://download.pytorch.org/whl/torch_stable.html

# For CPU only
pip install torch==1.13.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

#### 4. MediaPipe Issues
```bash
# If MediaPipe fails:
pip install mediapipe==0.9.3.0

# Alternative: MediaPipe CPU only
pip install mediapipe-cpu
```

## 🧪 Testing Installation

```python
# test_python38.py
import sys
print(f"Python: {sys.version}")

# Test core packages
try:
    import cv2
    import numpy as np
    import PIL
    print("✅ Core packages OK")
except ImportError as e:
    print(f"❌ Core package error: {e}")

# Test ML packages  
try:
    import fer
    import deepface
    import mediapipe
    print("✅ ML packages OK")
except ImportError as e:
    print(f"⚠️ Some ML packages missing: {e}")
```

## 🐍 Python 3.8 Environment Setup

### Using venv
```bash
# Create virtual environment
python3.8 -m venv emotion_env_38

# Activate (Windows)
emotion_env_38\Scripts\activate

# Activate (Linux/Mac)
source emotion_env_38/bin/activate

# Install requirements
pip install -r requirements38.txt
```

### Using conda
```bash
# Create environment with Python 3.8
conda create -n emotion38 python=3.8

# Activate
conda activate emotion38

# Install packages
conda install -c conda-forge opencv pillow numpy
pip install -r requirements38.txt
```

## 📊 Compatibility Matrix

| Package | Python 3.8 | Status | Notes |
|---------|-------------|--------|-------|
| OpenCV | ✅ | Fully supported | Use 4.5.x - 4.8.x |
| NumPy | ✅ | Use < 1.25 | 1.19.x - 1.24.x |
| TensorFlow | ⚠️ | Limited | Max 2.10.x |
| PyTorch | ✅ | Fully supported | Up to 1.13.x |
| MediaPipe | ✅ | Use < 0.11 | 0.8.9 - 0.10.x |
| FER | ✅ | Fully supported | Latest version |
| DeepFace | ✅ | Use < 0.85 | Some versions unstable |
| Dlib | ⚠️ | May need build tools | Use conda if pip fails |

## 🚨 Troubleshooting

### Error: Microsoft Visual C++ required
```bash
# Download and install:
# Visual C++ Build Tools 2019 or newer
# Or Visual Studio Community with C++ tools
```

### Error: No module named '_ctypes'
```bash
# On Linux, install:
sudo apt-get install libffi-dev
```

### Error: Failed building wheel for dlib
```bash
# Use conda instead:
conda install -c conda-forge dlib

# Or use pre-built wheel:
pip install https://github.com/jloh02/dlib/releases/download/v19.22.0/dlib-19.22.0-cp38-cp38-win_amd64.whl
```

### Memory issues with large models
```python
# In your code, limit memory usage:
import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
```

## 💡 Optimization Tips

1. **Install order**: Core packages first, then ML packages
2. **Use wheels**: `pip install --only-binary=all` for faster installs  
3. **Cache downloads**: `pip install --cache-dir ./pip_cache`
4. **Parallel installs**: Not recommended, can cause conflicts
5. **Version pinning**: Always specify versions for stability

## 🏃‍♂️ Running the App

```bash
# After installation:
python main.py

# Or with logging:
python main.py --verbose

# Check installation:
python install_python38.py
```

---
**Note**: Python 3.8 reached end-of-life in October 2024. Consider upgrading to Python 3.9+ for better package support.
