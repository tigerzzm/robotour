"""
Test script for motor functionality.
Use this to test motor movement without camera or navigation.
"""

import time
from motor_controller import MotorController
from config import *

def test_basic_movement():
    """Test basic motor movements."""
    print("Testing basic motor movements...")
    
    with MotorController() as motor:
        print("Testing forward movement...")
        motor.move_forward(FORWARD_SPEED, 2.0)
        time.sleep(1)
        
        print("Testing backward movement...")
        motor.move_backward(FORWARD_SPEED, 2.0)
        time.sleep(1)
        
        print("Testing left turn...")
        motor.turn_left(TURN_SPEED, 1.0)
        time.sleep(1)
        
        print("Testing right turn...")
        motor.turn_right(TURN_SPEED, 1.0)
        time.sleep(1)
        
        print("Testing pivot left...")
        motor.pivot_left(TURN_SPEED, 1.0)
        time.sleep(1)
        
        print("Testing pivot right...")
        motor.pivot_right(TURN_SPEED, 1.0)
        time.sleep(1)
        
        print("All basic movements completed")

def test_speed_control():
    """Test motor speed control."""
    print("Testing motor speed control...")
    
    with MotorController() as motor:
        speeds = [25, 50, 75, 100]
        
        for speed in speeds:
            print(f"Testing speed: {speed}%")
            motor.move_forward(speed, 1.0)
            time.sleep(0.5)
        
        print("Speed control test completed")

def test_manual_control():
    """Test manual motor control."""
    print("Manual motor control test")
    print("Commands: w=forward, s=backward, a=left, d=right, q=quit")
    
    with MotorController() as motor:
        try:
            while True:
                command = input("Enter command: ").lower().strip()
                
                if command == 'q':
                    break
                elif command == 'w':
                    print("Moving forward...")
                    motor.move_forward(FORWARD_SPEED, 0.5)
                elif command == 's':
                    print("Moving backward...")
                    motor.move_backward(FORWARD_SPEED, 0.5)
                elif command == 'a':
                    print("Turning left...")
                    motor.turn_left(TURN_SPEED, 0.5)
                elif command == 'd':
                    print("Turning right...")
                    motor.turn_right(TURN_SPEED, 0.5)
                elif command == 'stop':
                    print("Stopping...")
                    motor.stop()
                else:
                    print("Invalid command")
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"Error during manual control: {e}")

if __name__ == "__main__":
    print("=== Motor Test Suite ===")
    
    choice = input("Choose test:\n1. Basic movements\n2. Speed control\n3. Manual control\nEnter choice (1-3): ")
    
    if choice == "1":
        test_basic_movement()
    elif choice == "2":
        test_speed_control()
    elif choice == "3":
        test_manual_control()
    else:
        print("Invalid choice")
