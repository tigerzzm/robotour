"""
Simple camera test with better error handling.
"""

import sys
import time

def test_camera():
    """Test camera with better error handling."""
    print("=== Simple Camera Test ===")
    
    try:
        print("Importing Picamera2...")
        from picamera2 import Picamera2
        print("✓ Picamera2 imported successfully")
        
        print("Initializing camera...")
        camera = Picamera2()
        print("✓ Camera object created")
        
        print("Getting camera info...")
        try:
            info = camera.global_camera_info()
            print(f"✓ Camera info: {info}")
        except Exception as e:
            print(f"⚠️  Could not get camera info: {e}")
        
        print("Creating configuration...")
        config = camera.create_still_configuration(
            main={"size": (640, 480), "format": "RGB888"}
        )
        print("✓ Configuration created")
        
        print("Configuring camera...")
        camera.configure(config)
        print("✓ Camera configured")
        
        print("Starting camera...")
        camera.start()
        print("✓ Camera started")
        
        print("Waiting for camera to stabilize...")
        time.sleep(2)
        
        print("Capturing test image...")
        image = camera.capture_array()
        print(f"✓ Image captured: {image.shape}")
        
        print("Stopping camera...")
        camera.stop()
        camera.close()
        print("✓ Camera stopped and closed")
        
        print("\n🎉 Camera test successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Camera test failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Run: python3 camera_diagnostic.py")
        print("2. Enable camera: sudo raspi-config")
        print("3. Add to video group: sudo usermod -a -G video $USER")
        print("4. Reboot: sudo reboot")
        return False

if __name__ == "__main__":
    test_camera()
