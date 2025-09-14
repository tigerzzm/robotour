"""
Button controller for the robotic vehicle.
Handles push button input for starting the robot and emergency stop.
"""

import RPi.GPIO as GPIO
import time
from config import *

class ButtonController:
    def __init__(self):
        """Initialize the button controller."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up start button pin
        GPIO.setup(START_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Button state tracking
        self.button_pressed = False
        self.last_press_time = 0
        
        print(f"Button controller initialized - Start button on GPIO {START_BUTTON_PIN}")
        print("Button is active LOW (pressed = 0, released = 1)")
    
    def is_button_pressed(self):
        """Check if the start button is currently pressed."""
        return GPIO.input(START_BUTTON_PIN) == GPIO.LOW
    
    def wait_for_button_press(self, timeout=None):
        """
        Wait for the start button to be pressed.
        
        Args:
            timeout (float): Maximum time to wait in seconds (None for infinite)
        
        Returns:
            bool: True if button was pressed, False if timeout
        """
        print("🤖 Robot ready! Press the START button to begin navigation...")
        print("   (Button is on GPIO 16)")
        
        start_time = time.time()
        
        while True:
            # Check for button press
            if self.is_button_pressed():
                current_time = time.time()
                
                # Debounce check
                if current_time - self.last_press_time > BUTTON_DEBOUNCE_TIME:
                    self.last_press_time = current_time
                    self.button_pressed = True
                    print("🚀 START button pressed! Beginning navigation...")
                    time.sleep(0.5)  # Brief delay to ensure clean press
                    return True
            
            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                print(f"⏰ Timeout reached ({timeout}s). Starting automatically...")
                return False
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.01)
    
    def wait_for_button_release(self):
        """Wait for the button to be released."""
        while self.is_button_pressed():
            time.sleep(0.01)
        time.sleep(0.1)  # Additional debounce delay
    
    def check_emergency_stop(self):
        """
        Check if button is pressed for emergency stop.
        Returns True if emergency stop is requested.
        """
        if self.is_button_pressed():
            current_time = time.time()
            # Hold button for 2 seconds for emergency stop
            if current_time - self.last_press_time > 2.0:
                print("🛑 EMERGENCY STOP activated!")
                return True
        return False
    
    def get_button_status(self):
        """Get current button status for monitoring."""
        return {
            'pressed': self.is_button_pressed(),
            'last_press_time': self.last_press_time,
            'gpio_pin': START_BUTTON_PIN
        }
    
    def cleanup(self):
        """Clean up GPIO resources."""
        GPIO.cleanup()
        print("Button controller cleaned up")

def test_button():
    """Test function for the button controller."""
    print("=== Button Controller Test ===")
    print("Press the start button to test...")
    print("Hold for 2+ seconds for emergency stop test")
    print("Press Ctrl+C to exit")
    
    button = ButtonController()
    
    try:
        while True:
            if button.is_button_pressed():
                print("Button pressed!")
                button.wait_for_button_release()
                print("Button released!")
            
            if button.check_emergency_stop():
                print("Emergency stop detected!")
                break
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        button.cleanup()

if __name__ == "__main__":
    test_button()
