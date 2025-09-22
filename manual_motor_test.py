"""
Manual motor test with step-by-step instructions.
"""

import time
import RPi.GPIO as GPIO
from config import *

def manual_test():
    """Manual test with step-by-step instructions."""
    print("=== MANUAL MOTOR TEST ===")
    print("This test will guide you through checking each component.")
    print()
    
    # Step 1: Check GPIO
    print("STEP 1: Testing GPIO...")
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Test GPIO 18 (IN1)
        print("Testing GPIO 18 (IN1)...")
        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        print("✓ GPIO 18 working")
        
        # Test GPIO 15 (IN2)
        print("Testing GPIO 15 (IN2)...")
        GPIO.setup(15, GPIO.OUT)
        GPIO.output(15, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(15, GPIO.LOW)
        print("✓ GPIO 15 working")
        
        # Test GPIO 22 (IN3)
        print("Testing GPIO 22 (IN3)...")
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(22, GPIO.LOW)
        print("✓ GPIO 22 working")
        
        # Test GPIO 27 (IN4)
        print("Testing GPIO 27 (IN4)...")
        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(27, GPIO.LOW)
        print("✓ GPIO 27 working")
        
        # Test GPIO 14 (ENA)
        print("Testing GPIO 14 (ENA)...")
        GPIO.setup(14, GPIO.OUT)
        GPIO.output(14, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(14, GPIO.LOW)
        print("✓ GPIO 14 working")
        
        # Test GPIO 17 (ENB)
        print("Testing GPIO 17 (ENB)...")
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(17, GPIO.LOW)
        print("✓ GPIO 17 working")
        
        print("✓ All GPIO pins working!")
        
    except Exception as e:
        print(f"✗ GPIO test failed: {e}")
        return False
    
    print()
    
    # Step 2: Test L298N
    print("STEP 2: Testing L298N...")
    try:
        # Set up all pins
        GPIO.setup(18, GPIO.OUT)  # IN1
        GPIO.setup(15, GPIO.OUT)  # IN2
        GPIO.setup(22, GPIO.OUT)  # IN3
        GPIO.setup(27, GPIO.OUT)  # IN4
        GPIO.setup(14, GPIO.OUT)  # ENA
        GPIO.setup(17, GPIO.OUT)  # ENB
        
        print("Testing left motor (ENA + IN1)...")
        GPIO.output(14, GPIO.HIGH)  # Enable left motor
        GPIO.output(18, GPIO.HIGH)  # IN1 high
        GPIO.output(15, GPIO.LOW)   # IN2 low
        time.sleep(2)
        GPIO.output(14, GPIO.LOW)   # Disable
        GPIO.output(18, GPIO.LOW)   # IN1 low
        print("✓ Left motor test completed")
        
        print("Testing right motor (ENB + IN3)...")
        GPIO.output(17, GPIO.HIGH)  # Enable right motor
        GPIO.output(22, GPIO.HIGH)  # IN3 high
        GPIO.output(27, GPIO.LOW)   # IN4 low
        time.sleep(2)
        GPIO.output(17, GPIO.LOW)   # Disable
        GPIO.output(22, GPIO.LOW)   # IN3 low
        print("✓ Right motor test completed")
        
        print("✓ L298N test completed!")
        
    except Exception as e:
        print(f"✗ L298N test failed: {e}")
        return False
    
    print()
    
    # Step 3: Instructions
    print("STEP 3: Manual Checks")
    print("If motors still don't move, check:")
    print("1. Power supply to L298N (6V from LM2596S)")
    print("2. L298N +5V connection to Pi")
    print("3. All ground connections")
    print("4. Motor wire connections")
    print("5. Motor functionality (test with multimeter)")
    print()
    
    return True

def simple_test():
    """Simple test with minimal code."""
    print("=== SIMPLE MOTOR TEST ===")
    print("Testing with minimal code...")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up pins
        GPIO.setup(14, GPIO.OUT)  # ENA
        GPIO.setup(17, GPIO.OUT)  # ENB
        GPIO.setup(18, GPIO.OUT)  # IN1
        GPIO.setup(15, GPIO.OUT)  # IN2
        GPIO.setup(22, GPIO.OUT)  # IN3
        GPIO.setup(27, GPIO.OUT)  # IN4
        
        print("Testing left motor...")
        GPIO.output(14, GPIO.HIGH)  # Enable
        GPIO.output(18, GPIO.HIGH)  # Forward
        GPIO.output(15, GPIO.LOW)   # Not backward
        time.sleep(3)
        
        print("Testing right motor...")
        GPIO.output(17, GPIO.HIGH)  # Enable
        GPIO.output(22, GPIO.HIGH)  # Forward
        GPIO.output(27, GPIO.LOW)   # Not backward
        time.sleep(3)
        
        # Stop all
        GPIO.output(14, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        
        print("✓ Simple test completed")
        
    except Exception as e:
        print(f"✗ Simple test failed: {e}")

def main():
    """Main function."""
    print("=== MANUAL MOTOR TESTING ===")
    print("Choose test type:")
    print("1. Manual test with instructions")
    print("2. Simple test")
    print("3. Exit")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        manual_test()
    elif choice == "2":
        simple_test()
    elif choice == "3":
        return
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
