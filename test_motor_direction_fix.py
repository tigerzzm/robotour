"""
Test script to verify motor direction fix.
This script tests the corrected motor directions.
"""

import time
from motor_controller import MotorController
from config import *

def test_motor_directions():
    """Test motor directions with the fix applied."""
    print("=== Motor Direction Fix Test ===")
    print(f"REVERSE_LEFT_MOTOR: {REVERSE_LEFT_MOTOR}")
    print(f"REVERSE_RIGHT_MOTOR: {REVERSE_RIGHT_MOTOR}")
    print()
    
    motor = MotorController()
    
    try:
        print("Testing forward movement...")
        print("Expected: Both motors should rotate forward")
        motor.move_forward(30, 2.0)
        time.sleep(1)
        
        print("Testing backward movement...")
        print("Expected: Both motors should rotate backward")
        motor.move_backward(30, 2.0)
        time.sleep(1)
        
        print("Testing left turn...")
        print("Expected: Left motor backward, right motor forward")
        motor.turn_left(25, 1.5)
        time.sleep(1)
        
        print("Testing right turn...")
        print("Expected: Left motor forward, right motor backward")
        motor.turn_right(25, 1.5)
        time.sleep(1)
        
        print("✓ Motor direction test completed!")
        print()
        print("If the movements are still incorrect:")
        print("1. Check the REVERSE_RIGHT_MOTOR setting in config.py")
        print("2. Or swap the motor wires on the L298N")
        
    except Exception as e:
        print(f"Error during motor test: {e}")
    finally:
        motor.cleanup()

def test_individual_motors():
    """Test individual motors to verify direction."""
    print("=== Individual Motor Test ===")
    
    motor = MotorController()
    
    try:
        print("Testing left motor only (forward)...")
        if USE_ENABLE_PINS:
            motor.ena_pwm.ChangeDutyCycle(30)
            motor.enb_pwm.ChangeDutyCycle(0)  # Right motor off
            
            if REVERSE_LEFT_MOTOR:
                motor.left_forward_pin.ChangeDutyCycle(0)
                motor.left_backward_pin.ChangeDutyCycle(100)
            else:
                motor.left_forward_pin.ChangeDutyCycle(100)
                motor.left_backward_pin.ChangeDutyCycle(0)
        else:
            if REVERSE_LEFT_MOTOR:
                motor.left_pwm_backward.ChangeDutyCycle(30)
                motor.left_pwm_forward.ChangeDutyCycle(0)
            else:
                motor.left_pwm_forward.ChangeDutyCycle(30)
                motor.left_pwm_backward.ChangeDutyCycle(0)
        
        time.sleep(2)
        motor.stop()
        time.sleep(1)
        
        print("Testing right motor only (forward)...")
        if USE_ENABLE_PINS:
            motor.ena_pwm.ChangeDutyCycle(0)  # Left motor off
            motor.enb_pwm.ChangeDutyCycle(30)
            
            if REVERSE_RIGHT_MOTOR:
                motor.right_forward_pin.ChangeDutyCycle(0)
                motor.right_backward_pin.ChangeDutyCycle(100)
            else:
                motor.right_forward_pin.ChangeDutyCycle(100)
                motor.right_backward_pin.ChangeDutyCycle(0)
        else:
            if REVERSE_RIGHT_MOTOR:
                motor.right_pwm_backward.ChangeDutyCycle(30)
                motor.right_pwm_forward.ChangeDutyCycle(0)
            else:
                motor.right_pwm_forward.ChangeDutyCycle(30)
                motor.right_pwm_backward.ChangeDutyCycle(0)
        
        time.sleep(2)
        motor.stop()
        
        print("✓ Individual motor test completed!")
        
    except Exception as e:
        print(f"Error during individual motor test: {e}")
    finally:
        motor.cleanup()

def main():
    """Main test function."""
    print("=== Motor Direction Fix Verification ===")
    print("This script tests the motor direction correction.")
    print()
    
    while True:
        print("Choose test:")
        print("1. Test motor directions")
        print("2. Test individual motors")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            test_motor_directions()
        elif choice == "2":
            test_individual_motors()
        elif choice == "3":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
