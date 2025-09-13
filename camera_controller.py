"""
Camera controller for capturing and processing images from the Pi camera.
"""

import cv2
import numpy as np
import os
from picamera2 import Picamera2
from config import *

class CameraController:
    def __init__(self):
        """Initialize the camera controller."""
        self.camera = Picamera2()
        self.camera_config = self.camera.create_still_configuration(
            main={"size": (CAMERA_WIDTH, CAMERA_HEIGHT), "format": "RGB888"},
            lores={"size": (320, 240), "format": "YUV420"}
        )
        self.camera.configure(self.camera_config)
        self.camera.start()
        
        # Create image save directory if it doesn't exist
        if SAVE_IMAGES and not os.path.exists(IMAGE_SAVE_PATH):
            os.makedirs(IMAGE_SAVE_PATH)
        
        print("Camera controller initialized")
    
    def capture_image(self):
        """Capture an image from the camera."""
        try:
            # Capture image
            image = self.camera.capture_array()
            
            # Convert from RGB to BGR for OpenCV
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            return image
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
            x, y, w, h = cv2.boundingRect(contour)
            if w > MIN_LINE_LENGTH:  # Filter short lines
                h_lines.append((x, y, x + w, y + h))
        
        # Find contours for vertical lines
        v_contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        v_lines = []
        for contour in v_contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h > MIN_LINE_LENGTH:  # Filter short lines
                v_lines.append((x, y, x + w, y + h))
        
        return h_lines, v_lines
    
    def find_grid_intersections(self, h_lines, v_lines):
        """Find intersections between horizontal and vertical lines."""
        intersections = []
        
        for h_line in h_lines:
            h_y = (h_line[1] + h_line[3]) / 2  # Middle Y of horizontal line
            
            for v_line in v_lines:
                v_x = (v_line[0] + v_line[2]) / 2  # Middle X of vertical line
                
                # Check if lines intersect (with some tolerance)
                if (h_line[0] <= v_x <= h_line[2] and 
                    v_line[1] <= h_y <= v_line[3]):
                    intersections.append((int(v_x), int(h_y)))
        
        return intersections
    
    def detect_grid_cells(self, image):
        """Detect grid cells and return their positions."""
        # Preprocess image
        processed = self.preprocess_image(image)
        if processed is None:
            return []
        
        # Detect grid lines
        h_lines, v_lines = self.detect_grid_lines(processed)
        
        # Find intersections
        intersections = self.find_grid_intersections(h_lines, v_lines)
        
        # Group intersections into grid cells
        cells = []
        if len(intersections) >= 4:  # Need at least 4 corners for a cell
            # Sort intersections by position
            intersections.sort(key=lambda x: (x[1], x[0]))  # Sort by Y, then X
            
            # Group into rows and columns
            rows = []
            current_row = []
            last_y = intersections[0][1]
            
            for x, y in intersections:
                if abs(y - last_y) > 10:  # New row
                    if current_row:
                        rows.append(sorted(current_row, key=lambda p: p[0]))
                    current_row = [(x, y)]
                else:
                    current_row.append((x, y))
                last_y = y
            
            if current_row:
                rows.append(sorted(current_row, key=lambda p: p[0]))
            
            # Create grid cells from intersections
            for i in range(len(rows) - 1):
                for j in range(len(rows[i]) - 1):
                    if j < len(rows[i + 1]):
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
        
        return cells
    
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
