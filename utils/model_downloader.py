"""
Model downloader utility for downloading pre-trained weights
"""
import os
import urllib.request
from pathlib import Path

def download_dlib_landmarks():
    """Download dlib 68-point facial landmark predictor"""
    url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    filename = "shape_predictor_68_face_landmarks.dat.bz2"
    
    if not os.path.exists("shape_predictor_68_face_landmarks.dat"):
        print("Downloading dlib facial landmark predictor...")
        try:
            urllib.request.urlretrieve(url, filename)
            
            # Extract bz2 file
            import bz2
            with bz2.BZ2File(filename, 'rb') as f_in:
                with open("shape_predictor_68_face_landmarks.dat", 'wb') as f_out:
                    f_out.write(f_in.read())
            
            # Remove compressed file
            os.remove(filename)
            print("Dlib landmark predictor downloaded successfully!")
            
        except Exception as e:
            print(f"Error downloading dlib landmarks: {e}")
    else:
        print("Dlib landmark predictor already exists!")

def download_emotion_models():
    """Download various emotion recognition models"""
    models_dir = Path("emotion_models")
    models_dir.mkdir(exist_ok=True)
    
    # You can add more model downloads here
    print("Model download utility ready!")
    print("Available downloads:")
    print("1. Dlib facial landmarks")
    
    choice = input("Download dlib landmarks? (y/n): ")
    if choice.lower() == 'y':
        download_dlib_landmarks()

if __name__ == "__main__":
    download_emotion_models()
