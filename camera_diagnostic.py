"""
Camera diagnostic script to troubleshoot camera issues.
"""

import subprocess
import os
import sys

def check_camera_interface():
    """Check if camera interface is enabled."""
    print("=== Camera Interface Check ===")
    
    try:
        # Check if camera is enabled in config
        result = subprocess.run(['vcgencmd', 'get_camera'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Camera status: {result.stdout.strip()}")
            if "detected=1" in result.stdout:
                print("✓ Camera hardware detected")
            else:
                print("✗ Camera hardware not detected")
                
            if "supported=1" in result.stdout:
                print("✓ Camera interface supported")
            else:
                print("✗ Camera interface not supported")
        else:
            print("✗ Could not check camera status")
            
    except Exception as e:
        print(f"Error checking camera interface: {e}")

def check_camera_permissions():
    """Check camera permissions."""
    print("\n=== Camera Permissions Check ===")
    
    try:
        # Check if user is in video group
        result = subprocess.run(['groups'], capture_output=True, text=True)
        if result.returncode == 0:
            groups = result.stdout.strip()
            print(f"User groups: {groups}")
            if "video" in groups:
                print("✓ User is in video group")
            else:
                print("✗ User is not in video group")
                print("  Run: sudo usermod -a -G video $USER")
                print("  Then logout and login again")
        else:
            print("✗ Could not check user groups")
            
    except Exception as e:
        print(f"Error checking permissions: {e}")

def check_camera_processes():
    """Check if camera is being used by other processes."""
    print("\n=== Camera Process Check ===")
    
    try:
        # Check for processes using camera
        result = subprocess.run(['lsof', '/dev/video0'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Camera is being used by:")
            print(result.stdout)
        else:
            print("✓ Camera is not being used by other processes")
            
    except Exception as e:
        print(f"Error checking camera processes: {e}")

def test_picamera2_import():
    """Test if Picamera2 can be imported."""
    print("\n=== Picamera2 Import Test ===")
    
    try:
        from picamera2 import Picamera2
        print("✓ Picamera2 imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Picamera2 import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Picamera2 import error: {e}")
        return False

def test_picamera2_initialization():
    """Test Picamera2 initialization."""
    print("\n=== Picamera2 Initialization Test ===")
    
    try:
        from picamera2 import Picamera2
        
        print("Attempting to initialize Picamera2...")
        camera = Picamera2()
        print("✓ Picamera2 initialized successfully")
        
        # Try to get camera info
        try:
            info = camera.global_camera_info()
            print(f"Camera info: {info}")
        except Exception as e:
            print(f"Could not get camera info: {e}")
        
        # Try to create configuration
        try:
            config = camera.create_still_configuration(
                main={"size": (640, 480), "format": "RGB888"}
            )
            print("✓ Camera configuration created successfully")
        except Exception as e:
            print(f"✗ Camera configuration failed: {e}")
        
        camera.close()
        return True
        
    except Exception as e:
        print(f"✗ Picamera2 initialization failed: {e}")
        return False

def test_simple_camera_capture():
    """Test simple camera capture."""
    print("\n=== Simple Camera Capture Test ===")
    
    try:
        from picamera2 import Picamera2
        import numpy as np
        
        print("Initializing camera...")
        camera = Picamera2()
        
        print("Creating configuration...")
        config = camera.create_still_configuration(
            main={"size": (640, 480), "format": "RGB888"}
        )
        
        print("Configuring camera...")
        camera.configure(config)
        
        print("Starting camera...")
        camera.start()
        
        print("Capturing image...")
        image = camera.capture_array()
        
        print(f"✓ Image captured successfully: {image.shape}")
        
        print("Stopping camera...")
        camera.stop()
        camera.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Simple camera capture failed: {e}")
        return False

def main():
    """Main diagnostic function."""
    print("=== Camera Diagnostic Tool ===")
    print("Troubleshooting camera issues...")
    print()
    
    # Run all diagnostic tests
    check_camera_interface()
    check_camera_permissions()
    check_camera_processes()
    
    if test_picamera2_import():
        if test_picamera2_initialization():
            test_simple_camera_capture()
    
    print("\n=== Diagnostic Summary ===")
    print("If camera is still not working:")
    print("1. Enable camera interface: sudo raspi-config")
    print("2. Add user to video group: sudo usermod -a -G video $USER")
    print("3. Reboot the Pi: sudo reboot")
    print("4. Check camera connection")
    print("5. Try a different camera module")

if __name__ == "__main__":
    main()
