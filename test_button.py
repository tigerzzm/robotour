"""
Test script for the push button functionality.
Use this to test the start button before running the full system.
"""

import time
from button_controller import ButtonController
from config import *

def test_basic_button():
    """Test basic button press detection."""
    print("=== Basic Button Test ===")
    print("Press the start button to test...")
    print("Press Ctrl+C to exit")
    
    button = ButtonController()
    
    try:
        press_count = 0
        while True:
            if button.is_button_pressed():
                press_count += 1
                print(f"Button pressed! (Count: {press_count})")
                button.wait_for_button_release()
                print("Button released!")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print(f"\nTest completed. Total presses: {press_count}")
    finally:
        button.cleanup()

def test_wait_for_press():
    """Test waiting for button press."""
    print("=== Wait for Button Press Test ===")
    print("This will wait for you to press the button...")
    
    button = ButtonController()
    
    try:
        print("Waiting for button press (10 second timeout)...")
        result = button.wait_for_button_press(timeout=10)
        
        if result:
            print("✅ Button press detected successfully!")
        else:
            print("⏰ Timeout reached, no button press detected")
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        button.cleanup()

def test_emergency_stop():
    """Test emergency stop functionality."""
    print("=== Emergency Stop Test ===")
    print("Hold the button for 2+ seconds to test emergency stop...")
    print("Press Ctrl+C to exit")
    
    button = ButtonController()
    
    try:
        while True:
            if button.check_emergency_stop():
                print("🛑 Emergency stop activated!")
                break
            
            if button.is_button_pressed():
                print("Button held...")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        button.cleanup()

def test_button_status():
    """Test button status monitoring."""
    print("=== Button Status Test ===")
    print("Press and release the button to see status changes...")
    print("Press Ctrl+C to exit")
    
    button = ButtonController()
    
    try:
        while True:
            status = button.get_button_status()
            print(f"Button Status: {'PRESSED' if status['pressed'] else 'RELEASED'} | GPIO {status['gpio_pin']}")
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\nTest completed")
    finally:
        button.cleanup()

def interactive_test():
    """Interactive test menu."""
    print("=== Interactive Button Test ===")
    
    while True:
        print("\nChoose test:")
        print("1. Basic button press test")
        print("2. Wait for button press test")
        print("3. Emergency stop test")
        print("4. Button status monitoring")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            test_basic_button()
        elif choice == "2":
            test_wait_for_press()
        elif choice == "3":
            test_emergency_stop()
        elif choice == "4":
            test_button_status()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    print("=== Push Button Test Suite ===")
    print(f"Button configured on GPIO {START_BUTTON_PIN}")
    print("Button is active LOW (pressed = 0, released = 1)")
    print()
    
    interactive_test()
