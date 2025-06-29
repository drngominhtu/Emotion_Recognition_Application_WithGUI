import cv2
import sys

def test_camera():
    """Test camera functionality"""
    print("Testing camera...")
    
    # Try to open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Cannot open camera!")
        print("Please check:")
        print("1. Camera is connected")
        print("2. No other application is using the camera")
        print("3. Try changing camera index (0, 1, 2...)")
        return False
    
    print("Camera opened successfully!")
    print("Press 'q' to quit the test")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Cannot read from camera")
            break
        
        # Display frame
        cv2.imshow('Camera Test - Press Q to quit', frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Camera test completed!")
    return True

if __name__ == "__main__":
    test_camera()
