"""
Test script for camera functionality.
Use this to test camera capture and grid detection without motor movement.
"""

import cv2
import time
from camera_controller import CameraController
from config import *

def test_camera_capture():
    """Test basic camera capture functionality."""
    print("Testing camera capture...")
    
    camera = CameraController()
    
    try:
        for i in range(5):
            print(f"Capturing image {i+1}/5...")
            image = camera.capture_image()
            
            if image is not None:
                print(f"Image captured: {image.shape}")
                
                # Save test image
                filename = f"test_capture_{i+1}.jpg"
                camera.save_debug_image(image, filename)
                
                # Test grid detection
                cells = camera.detect_grid_cells(image)
                print(f"Detected {len(cells)} grid cells")
                
                # Test position detection
                row, col = camera.get_vehicle_position(image)
                if row is not None and col is not None:
                    print(f"Vehicle position: ({row}, {col})")
                else:
                    print("Could not determine vehicle position")
            else:
                print("Failed to capture image")
            
            time.sleep(1)
    
    except Exception as e:
        print(f"Error during camera test: {e}")
    finally:
        camera.cleanup()

def test_grid_detection():
    """Test grid detection with a specific image."""
    print("Testing grid detection...")
    
    camera = CameraController()
    
    try:
        image = camera.capture_image()
        if image is None:
            print("Failed to capture image for grid detection test")
            return
        
        # Preprocess image
        processed = camera.preprocess_image(image)
        if processed is not None:
            camera.save_debug_image(processed, "processed_image.jpg")
            print("Processed image saved")
        
        # Detect grid lines
        h_lines, v_lines = camera.detect_grid_lines(processed)
        print(f"Detected {len(h_lines)} horizontal lines and {len(v_lines)} vertical lines")
        
        # Detect grid cells
        cells = camera.detect_grid_cells(image)
        print(f"Detected {len(cells)} grid cells")
        
        for i, cell in enumerate(cells):
            print(f"Cell {i}: center={cell['center']}, row={cell['row']}, col={cell['col']}")
        
        # Save image with detected cells
        if cells:
            result_image = image.copy()
            for cell in cells:
                center = cell['center']
                cv2.circle(result_image, center, 5, (0, 255, 0), -1)
                cv2.putText(result_image, f"({cell['row']},{cell['col']})", 
                           (center[0] + 10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            camera.save_debug_image(result_image, "detected_cells.jpg")
            print("Image with detected cells saved")
    
    except Exception as e:
        print(f"Error during grid detection test: {e}")
    finally:
        camera.cleanup()

if __name__ == "__main__":
    print("=== Camera Test Suite ===")
    
    choice = input("Choose test:\n1. Basic camera capture\n2. Grid detection\n3. Both\nEnter choice (1-3): ")
    
    if choice == "1":
        test_camera_capture()
    elif choice == "2":
        test_grid_detection()
    elif choice == "3":
        test_camera_capture()
        test_grid_detection()
    else:
        print("Invalid choice")
