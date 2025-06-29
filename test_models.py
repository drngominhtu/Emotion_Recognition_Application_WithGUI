"""
Test script to check which emotion recognition models are available
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_models():
    """Test each model individually"""
    print("=" * 60)
    print("EMOTION RECOGNITION MODELS TEST")
    print("=" * 60)
    
    # Test individual models
    models_to_test = [
        ("OpenCV Basic", "models.opencv_detector", "OpenCVDetector"),
        ("FER", "models.fer_detector", "FERDetector"),
        ("DeepFace", "models.deepface_detector", "DeepFaceDetector"),
        ("MediaPipe", "models.mediapipe_detector", "MediaPipeTransformersDetector"),
        ("MTCNN", "models.mtcnn_detector", "MTCNNDetector"),
        ("Dlib", "models.dlib_detector", "DlibDetector"),
        ("Simple CNN", "models.simple_cnn_detector", "SimpleCNNDetector"),
    ]
    
    available_models = []
    
    for model_name, module_name, class_name in models_to_test:
        print(f"\nTesting {model_name}...")
        try:
            module = __import__(module_name, fromlist=[class_name])
            model_class = getattr(module, class_name)
            model_instance = model_class()
            
            if model_instance.is_available():
                print(f"✅ {model_name}: AVAILABLE - {model_instance.get_model_name()}")
                available_models.append(model_instance.get_model_name())
            else:
                print(f"❌ {model_name}: NOT AVAILABLE")
                
        except ImportError as e:
            print(f"❌ {model_name}: IMPORT ERROR - {e}")
        except Exception as e:
            print(f"❌ {model_name}: ERROR - {e}")
    
    # Test ModelManager
    print(f"\n{'='*60}")
    print("TESTING MODEL MANAGER")
    print("=" * 60)
    
    try:
        from models.model_manager import ModelManager
        mm = ModelManager()
        manager_models = mm.get_available_models()
        
        print(f"✅ ModelManager initialized successfully!")
        print(f"📊 Available models via ModelManager: {len(manager_models)}")
        
        for model in manager_models:
            print(f"   - {model}")
            
        if not manager_models:
            print("⚠️  No models available! Please install emotion recognition libraries:")
            print("   pip install fer deepface mediapipe facenet-pytorch dlib")
            
    except Exception as e:
        print(f"❌ ModelManager ERROR: {e}")
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print("=" * 60)
    print(f"Total available models: {len(available_models)}")
    
    if available_models:
        print("✅ Ready to run emotion recognition!")
    else:
        print("❌ No models available. Please install dependencies:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    test_models()
