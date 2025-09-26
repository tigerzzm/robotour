"""
Camera controller for capturing and processing images from the Pi camera.
"""

import cv2
import numpy as np
import os
import time
from picamera2 import Picamera2
from config import *

class CameraController:
    def __init__(self):
        """Initialize the camera controller."""
        self.camera = Picamera2()
        
        # Configure camera for Pi Camera v1 (OV5647)
        self.camera_config = self.camera.create_still_configuration(
            main={"size": (CAMERA_WIDTH, CAMERA_HEIGHT), "format": "RGB888"},
            lores={"size": (320, 240), "format": "YUV420"}
        )
        
        # Set sensor mode for optimal performance
        if hasattr(self, 'camera') and hasattr(self.camera, 'sensor_modes'):
            try:
                # Use sensor mode 2 for 640x480@60fps on Pi Camera v1
                self.camera.sensor_mode = CAMERA_SENSOR_MODE
            except:
                pass
        
        self.camera.configure(self.camera_config)
        
        # Set camera properties for better image quality
        try:
            # Wait for camera to stabilize
            time.sleep(2)
            
            # Set exposure and gain for Pi Camera v1
            self.camera.set_controls({
                "ExposureTime": 50000,   # 50ms exposure (longer for better light)
                "AnalogueGain": 2.0,     # Higher gain for better sensitivity
                "DigitalGain": 1.0,      # No digital gain
                "AeEnable": True,        # Enable auto exposure
                "AwbEnable": True,      # Enable auto white balance
            })
            
            # Give camera time to adjust
            time.sleep(1)
            
        except Exception as e:
            print(f"Camera control warning: {e}")
            pass  # Some controls might not be available
        
        self.camera.start()
        
        # Create image save directory if it doesn't exist
        if SAVE_IMAGES and not os.path.exists(IMAGE_SAVE_PATH):
            os.makedirs(IMAGE_SAVE_PATH)
        
        print("Camera controller initialized")
    
    def capture_image(self):
        """Capture an image from the camera."""
        try:
            # Wait for camera to stabilize
            time.sleep(0.5)
            
            # Capture image
            image = self.camera.capture_array()
            
            # Check if image is valid (not all black)
            if image is not None and image.size > 0:
                # Convert from RGB to BGR for OpenCV
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Check if image is too dark
                mean_brightness = np.mean(image)
                if mean_brightness < 10:  # Very dark image
                    print(f"Warning: Image is very dark (brightness: {mean_brightness:.1f})")
                    print("Try improving lighting or camera settings")
                
                return image
            else:
                print("Error: Captured image is None or empty")
                return None
                
        except Exception as e:
            print(f"Error capturing image: {e}")
            return None
    
    def preprocess_image(self, image):
        """Preprocess the image for grid detection."""
        if image is None:
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh
    
    def detect_grid_lines(self, image):
        """Detect grid lines in the image using Hough line detection."""
        if image is None:
            return [], []
        
        try:
            # Detect horizontal lines
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
            horizontal_lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, horizontal_kernel)
            
            # Detect vertical lines
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
            vertical_lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, vertical_kernel)
            
            # Find contours for horizontal lines
            h_contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            h_lines = []
            for contour in h_contours:
                if len(contour) > 0:  # Check if contour is valid
                    x, y, w, h = cv2.boundingRect(contour)
                    if w > MIN_LINE_LENGTH:  # Filter short lines
                        h_lines.append((x, y, x + w, y + h))
            
            # Find contours for vertical lines
            v_contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            v_lines = []
            for contour in v_contours:
                if len(contour) > 0:  # Check if contour is valid
                    x, y, w, h = cv2.boundingRect(contour)
                    if h > MIN_LINE_LENGTH:  # Filter short lines
                        v_lines.append((x, y, x + w, y + h))
            
            return h_lines, v_lines
            
        except Exception as e:
            print(f"Error in grid line detection: {e}")
            return [], []
    
    def find_grid_intersections(self, h_lines, v_lines):
        """Find intersections between horizontal and vertical lines."""
        intersections = []
        
        # Check if we have valid lines
        if not h_lines or not v_lines:
            return intersections
        
        for h_line in h_lines:
            # Validate horizontal line has 4 coordinates
            if len(h_line) < 4:
                continue
                
            h_y = (h_line[1] + h_line[3]) / 2  # Middle Y of horizontal line
            
            for v_line in v_lines:
                # Validate vertical line has 4 coordinates
                if len(v_line) < 4:
                    continue
                    
                v_x = (v_line[0] + v_line[2]) / 2  # Middle X of vertical line
                
                # Check if lines intersect (with some tolerance)
                if (h_line[0] <= v_x <= h_line[2] and 
                    v_line[1] <= h_y <= v_line[3]):
                    intersections.append((int(v_x), int(h_y)))
        
        return intersections
    
    def detect_grid_cells(self, image):
        """Detect grid cells and return their positions."""
        try:
            # Preprocess image
            processed = self.preprocess_image(image)
            if processed is None:
                return []
            
            # Detect grid lines
            h_lines, v_lines = self.detect_grid_lines(processed)
            print(f"Detected {len(h_lines)} horizontal lines and {len(v_lines)} vertical lines")
            
            # Find intersections
            intersections = self.find_grid_intersections(h_lines, v_lines)
            print(f"Found {len(intersections)} intersections")
            
            # Filter intersections to reduce noise (keep only well-spaced ones)
            if len(intersections) > 100:  # Too many intersections, filter them
                print("Too many intersections, filtering...")
                filtered_intersections = []
                min_distance = 20  # Minimum distance between intersections
                
                for intersection in intersections:
                    too_close = False
                    for existing in filtered_intersections:
                        distance = ((intersection[0] - existing[0]) ** 2 + (intersection[1] - existing[1]) ** 2) ** 0.5
                        if distance < min_distance:
                            too_close = True
                            break
                    if not too_close:
                        filtered_intersections.append(intersection)
                
                intersections = filtered_intersections
                print(f"Filtered to {len(intersections)} intersections")
        
            # Group intersections into grid cells
            cells = []
            if len(intersections) >= 4:  # Need at least 4 corners for a cell
                print(f"Processing {len(intersections)} intersections...")
                
                # Sort intersections by position
                intersections.sort(key=lambda x: (x[1], x[0]))  # Sort by Y, then X
                print("Intersections sorted")
                
                # Group into rows and columns
                rows = []
                current_row = []
                last_y = intersections[0][1] if intersections else 0
                print(f"Starting with last_y: {last_y}")
                
                for idx, (x, y) in enumerate(intersections):
                    print(f"Processing intersection {idx}: ({x}, {y})")
                    if abs(y - last_y) > 10:  # New row
                        if current_row:
                            rows.append(sorted(current_row, key=lambda p: p[0]))
                            print(f"Added row with {len(current_row)} points")
                        current_row = [(x, y)]
                    else:
                        current_row.append((x, y))
                    last_y = y
                
                if current_row:
                    rows.append(sorted(current_row, key=lambda p: p[0]))
                    print(f"Added final row with {len(current_row)} points")
                
                print(f"Total rows: {len(rows)}")
                for i, row in enumerate(rows):
                    print(f"Row {i}: {len(row)} points")
                
                # Create grid cells from intersections
                print("Creating grid cells...")
                for i in range(len(rows) - 1):
                    print(f"Processing row {i}...")
                    # Find the minimum number of points between current and next row
                    min_points = min(len(rows[i]), len(rows[i + 1]))
                    print(f"  Row {i} has {len(rows[i])} points, row {i+1} has {len(rows[i+1])} points")
                    print(f"  Using {min_points} points for cell creation")
                    
                    for j in range(min_points - 1):
                        print(f"  Processing cell at row {i}, col {j}")
                        if j < len(rows[i]) and j < len(rows[i + 1]) and j + 1 < len(rows[i]) and j + 1 < len(rows[i + 1]):
                            print(f"    Accessing rows[{i}][{j}] and rows[{i+1}][{j}]")
                            top_left = rows[i][j]
                            top_right = rows[i][j + 1]
                            bottom_left = rows[i + 1][j]
                            bottom_right = rows[i + 1][j + 1]
                            
                            cell_center_x = (top_left[0] + top_right[0] + bottom_left[0] + bottom_right[0]) // 4
                            cell_center_y = (top_left[1] + top_right[1] + bottom_left[1] + bottom_right[1]) // 4
                            
                            cells.append({
                                'center': (cell_center_x, cell_center_y),
                                'corners': [top_left, top_right, bottom_left, bottom_right],
                                'row': i,
                                'col': j
                            })
                            print(f"    Created cell at ({cell_center_x}, {cell_center_y})")
                        else:
                            print(f"    Skipping cell - insufficient points in rows")
            
            print(f"Returning {len(cells)} cells")
            return cells
        
        except Exception as e:
            print(f"Error in grid detection: {e}")
            print("Trying simplified grid detection...")
            return self.simple_grid_detection(image)
    
    def simple_grid_detection(self, image):
        """Simplified grid detection that's more robust."""
        try:
            print("Using simplified grid detection...")
            
            # Just return a basic grid based on image dimensions
            # This is a fallback when complex detection fails
            cells = []
            cell_width = CAMERA_WIDTH // GRID_COLS
            cell_height = CAMERA_HEIGHT // GRID_ROWS
            
            for row in range(GRID_ROWS):
                for col in range(GRID_COLS):
                    center_x = col * cell_width + cell_width // 2
                    center_y = row * cell_height + cell_height // 2
                    
                    cells.append({
                        'center': (center_x, center_y),
                        'corners': [
                            (col * cell_width, row * cell_height),
                            ((col + 1) * cell_width, row * cell_height),
                            (col * cell_width, (row + 1) * cell_height),
                            ((col + 1) * cell_width, (row + 1) * cell_height)
                        ],
                        'row': row,
                        'col': col
                    })
            
            print(f"Simple grid detection created {len(cells)} cells")
            return cells
            
        except Exception as e:
            print(f"Error in simple grid detection: {e}")
            return []
    
    def get_vehicle_position(self, image):
        """Estimate vehicle position relative to the grid."""
        cells = self.detect_grid_cells(image)
        
        if not cells:
            return None, None
        
        # Find the cell closest to the center of the image
        image_center_x = CAMERA_WIDTH // 2
        image_center_y = CAMERA_HEIGHT // 2
        
        closest_cell = min(cells, key=lambda cell: 
            ((cell['center'][0] - image_center_x) ** 2 + 
             (cell['center'][1] - image_center_y) ** 2) ** 0.5)
        
        return closest_cell['row'], closest_cell['col']
    
    def save_debug_image(self, image, filename):
        """Save an image for debugging purposes."""
        if SAVE_IMAGES and image is not None:
            filepath = os.path.join(IMAGE_SAVE_PATH, filename)
            cv2.imwrite(filepath, image)
            print(f"Debug image saved: {filepath}")
    
    def cleanup(self):
        """Clean up camera resources."""
        self.camera.stop()
        self.camera.close()
        print("Camera controller cleaned up")
