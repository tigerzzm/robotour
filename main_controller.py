"""
Main controller for the robotic vehicle navigation system.
Integrates camera, motor control, and navigation components.
"""

import time
import signal
import sys
from motor_controller import MotorController
from camera_controller import CameraController
from navigation_controller import NavigationController
from config import *

class RobotController:
    def __init__(self):
        """Initialize the main robot controller."""
        self.motor_controller = MotorController()
        self.camera_controller = CameraController()
        self.navigation_controller = NavigationController()
        
        self.running = False
        self.paused = False
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("Robot controller initialized")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Start the main control loop."""
        print("Starting robot navigation...")
        self.running = True
        
        try:
            while self.running and not self.navigation_controller.is_navigation_complete():
                if not self.paused:
                    self.navigation_step()
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            
            if self.navigation_controller.is_navigation_complete():
                print("Navigation completed successfully!")
                self.play_completion_sound()
            
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            self.cleanup()
    
    def navigation_step(self):
        """Execute one step of the navigation process."""
        # Capture current image
        image = self.camera_controller.capture_image()
        if image is None:
            print("Failed to capture image")
            return
        
        # Detect current position
        current_row, current_col = self.camera_controller.get_vehicle_position(image)
        if current_row is not None and current_col is not None:
            self.navigation_controller.update_position(current_row, current_col)
            print(f"Current position: ({current_row}, {current_col})")
        
        # Get next target
        next_target = self.navigation_controller.get_next_target()
        if next_target is None:
            print("No more targets to visit")
            return
        
        target_row, target_col = next_target
        print(f"Next target: ({target_row}, {target_col})")
        
        # Calculate and execute movement commands
        commands = self.navigation_controller.get_movement_commands(target_row, target_col)
        self.execute_commands(commands)
        
        # Save debug image
        if DEBUG_MODE:
            self.camera_controller.save_debug_image(image, f"step_{len(self.navigation_controller.visited_cells)}.jpg")
    
    def execute_commands(self, commands):
        """Execute a sequence of movement commands."""
        for command in commands:
            if not self.running:
                break
            
            print(f"Executing command: {command}")
            
            if command == 'move_forward':
                self.motor_controller.move_forward_grid_cell(FORWARD_SPEED)  # Move one grid cell
            elif command == 'move_backward':
                self.motor_controller.move_backward(FORWARD_SPEED, 1.0)
            elif command == 'turn_left':
                self.motor_controller.turn_left_90(TURN_SPEED)  # Turn 90 degrees
            elif command == 'turn_right':
                self.motor_controller.turn_right_90(TURN_SPEED)  # Turn 90 degrees
            elif command == 'pivot_left':
                self.motor_controller.pivot_left_90(TURN_SPEED)  # Pivot 90 degrees
            elif command == 'pivot_right':
                self.motor_controller.pivot_right_90(TURN_SPEED)  # Pivot 90 degrees
            elif command == 'stop':
                self.motor_controller.stop()
            
            # Small delay between commands
            time.sleep(0.2)
    
    def play_completion_sound(self):
        """Play a completion sound (if speaker is connected)."""
        # This could be implemented with a buzzer or speaker
        print("🎉 Navigation completed! 🎉")
        # You could add actual sound here if you have a buzzer connected
    
    def pause(self):
        """Pause the navigation."""
        self.paused = True
        self.motor_controller.stop()
        print("Navigation paused")
    
    def resume(self):
        """Resume the navigation."""
        self.paused = False
        print("Navigation resumed")
    
    def stop(self):
        """Stop the navigation and clean up."""
        self.running = False
        self.motor_controller.stop()
        print("Navigation stopped")
    
    def get_status(self):
        """Get current status of the robot."""
        nav_status = self.navigation_controller.get_navigation_status()
        return {
            'running': self.running,
            'paused': self.paused,
            'navigation': nav_status
        }
    
    def cleanup(self):
        """Clean up all resources."""
        print("Cleaning up resources...")
        self.motor_controller.cleanup()
        self.camera_controller.cleanup()
        print("Cleanup completed")

def main():
    """Main function to run the robot controller."""
    print("=== Robotic Vehicle Navigation System ===")
    print("Press Ctrl+C to stop")
    
    robot = RobotController()
    
    try:
        robot.start()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        robot.cleanup()

if __name__ == "__main__":
    main()
