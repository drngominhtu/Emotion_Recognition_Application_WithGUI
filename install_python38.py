"""
Installation script optimized for Python 3.8
"""
import subprocess
import sys
import platform
import pkg_resources

def check_python_version():
    """Check if Python version is 3.8.x"""
    version = sys.version_info
    if version.major != 3 or version.minor != 8:
        print(f"⚠️ Warning: This script is optimized for Python 3.8, you're using {version.major}.{version.minor}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected - Perfect!")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to upgrade pip")
        return False

def install_from_requirements():
    """Install packages from requirements38.txt"""
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements38.txt"
        ])
        print("✅ Successfully installed packages from requirements38.txt")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install from requirements38.txt: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements38.txt not found")
        return False

def install_core_packages():
    """Install core packages one by one with error handling"""
    core_packages = [
        "opencv-python>=4.5.0,<4.9.0",
        "pillow>=8.0.0,<10.0.0", 
        "numpy>=1.19.0,<1.25.0",
    ]
    
    print("\n📦 Installing core packages...")
    success_count = 0
    
    for package in core_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package.split('>=')[0]} installed")
            success_count += 1
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
    
    return success_count == len(core_packages)

def install_ml_packages():
    """Install ML packages with fallback options"""
    ml_packages = [
        ("fer>=22.4.0", "FER"),
        ("deepface>=0.0.75,<0.0.85", "DeepFace"),
        ("mediapipe>=0.8.9,<0.11.0", "MediaPipe"),
        ("transformers>=4.15.0,<4.25.0", "Transformers"),
        ("torch>=1.9.0,<1.14.0", "PyTorch"),
        ("facenet-pytorch>=2.5.0", "FaceNet-PyTorch"),
        ("tensorflow>=2.6.0,<2.11.0", "TensorFlow"),
        ("scikit-learn>=1.0.0,<1.2.0", "Scikit-learn"),
    ]
    
    print("\n🤖 Installing ML packages...")
    installed_packages = []
    
    for package, name in ml_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {name} installed")
            installed_packages.append(name)
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {name}")
            
            # Special handling for problematic packages
            if name == "dlib":
                print("💡 Try: conda install -c conda-forge dlib")
            elif name == "TensorFlow":
                print("💡 Try: pip install tensorflow-cpu (for CPU only)")
    
    return installed_packages

def install_optional_packages():
    """Install optional packages"""
    optional_packages = [
        ("dlib>=19.22.0", "Dlib (may fail without Visual C++)"),
        ("matplotlib>=3.3.0,<3.7.0", "Matplotlib"),
        ("pandas>=1.3.0,<1.6.0", "Pandas"),
        ("tqdm>=4.60.0", "TQDM"),
    ]
    
    print("\n🔧 Installing optional packages...")
    
    for package, name in optional_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {name} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️ {name} failed - continuing without it")

def verify_installations():
    """Verify that key packages can be imported"""
    test_imports = [
        ("cv2", "OpenCV"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
        ("fer", "FER"),
        ("deepface", "DeepFace"),
        ("mediapipe", "MediaPipe"),
        ("transformers", "Transformers"),
        ("torch", "PyTorch"),
        ("sklearn", "Scikit-learn"),
    ]
    
    print("\n🔍 Verifying installations...")
    working_packages = []
    
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
            working_packages.append(name)
        except ImportError:
            print(f"❌ {name} - Failed to import")
    
    return working_packages

def show_system_info():
    """Show system information"""
    print("\n💻 System Information:")
    print(f"Platform: {platform.platform()}")
    print(f"Python: {sys.version}")
    print(f"Architecture: {platform.architecture()[0]}")
    
def main():
    """Main installation process"""
    print("🚀 EMOTION RECOGNITION APP - Python 3.8 Setup")
    print("=" * 60)
    
    show_system_info()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Upgrade pip
    print("\n📥 Upgrading pip...")
    upgrade_pip()
    
    # Try installing from requirements file first
    print("\n📋 Attempting to install from requirements38.txt...")
    if install_from_requirements():
        print("\n🎉 All packages installed from requirements file!")
    else:
        print("\n🔄 Installing packages individually...")
        
        # Install core packages
        if not install_core_packages():
            print("❌ Core packages failed - cannot continue")
            return
        
        # Install ML packages
        installed_ml = install_ml_packages()
        print(f"\n📊 Successfully installed {len(installed_ml)} ML packages")
        
        # Install optional packages
        install_optional_packages()
    
    # Verify installations
    working = verify_installations()
    
    print("\n" + "=" * 60)
    print(f"📈 Installation Summary: {len(working)} packages working")
    
    if len(working) >= 5:
        print("✅ Installation successful! You can run the emotion recognition app.")
    else:
        print("⚠️ Some packages failed. App may have limited functionality.")
    
    print("\n💡 Tips for Python 3.8:")
    print("• Use pip install --only-binary=all for faster installs")
    print("• Install Visual C++ Build Tools for dlib on Windows")
    print("• Consider using conda for problematic packages")
    print("• Some TensorFlow features may require specific versions")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
