"""
Test script for ENA/ENB motor control functionality.
This script demonstrates the dual-level PWM control method.
"""

import time
from motor_controller import MotorController
from config import *

def test_control_method():
    """Test and display the current control method."""
    print("=== Motor Control Method Test ===")
    
    motor = MotorController()
    
    print(f"Current control method: {motor.get_control_method()}")
    print(f"USE_ENABLE_PINS: {USE_ENABLE_PINS}")
    print(f"ENA Pin: GPIO {ENA_PIN}")
    print(f"ENB Pin: GPIO {ENB_PIN}")
    print()

def test_basic_movements():
    """Test basic movements with current control method."""
    print("=== Basic Movement Test ===")
    
    motor = MotorController()
    
    try:
        print("Testing forward movement...")
        motor.move_forward(35, 2.0)
        time.sleep(1)
        
        print("Testing backward movement...")
        motor.move_backward(35, 2.0)
        time.sleep(1)
        
        print("Testing left turn...")
        motor.turn_left(25, 1.0)
        time.sleep(1)
        
        print("Testing right turn...")
        motor.turn_right(25, 1.0)
        time.sleep(1)
        
        print("Basic movement test completed!")
    
    except Exception as e:
        print(f"Error during movement test: {e}")
    finally:
        motor.cleanup()

def test_ena_enb_specific():
    """Test ENA/ENB specific functionality."""
    if not USE_ENABLE_PINS:
        print("ENA/ENB method not enabled. Set USE_ENABLE_PINS = True in config.py")
        return
    
    print("=== ENA/ENB Specific Test ===")
    
    motor = MotorController()
    
    try:
        print("Testing individual motor speed control...")
        
        # Test different speeds for each motor
        print("Left motor 50%, Right motor 25%")
        motor.set_motor_speeds(50, 25)
        motor.set_motor_directions(True, True)  # Both forward
        time.sleep(3)
        
        print("Left motor 25%, Right motor 50%")
        motor.set_motor_speeds(25, 50)
        time.sleep(3)
        
        print("Testing different directions...")
        motor.set_motor_directions(True, False)  # Left forward, right backward
        time.sleep(3)
        
        motor.set_motor_directions(False, True)  # Left backward, right forward
        time.sleep(3)
        
        print("ENA/ENB specific test completed!")
    
    except Exception as e:
        print(f"Error during ENA/ENB test: {e}")
    finally:
        motor.cleanup()

def test_speed_comparison():
    """Compare different speed settings."""
    print("=== Speed Comparison Test ===")
    
    motor = MotorController()
    
    try:
        speeds = [25, 35, 50, 70]
        
        for speed in speeds:
            print(f"Testing speed: {speed}%")
            motor.move_forward(speed, 2.0)
            time.sleep(1)
        
        print("Speed comparison test completed!")
    
    except Exception as e:
        print(f"Error during speed test: {e}")
    finally:
        motor.cleanup()

def interactive_ena_enb_test():
    """Interactive test for ENA/ENB control."""
    if not USE_ENABLE_PINS:
        print("ENA/ENB method not enabled. Set USE_ENABLE_PINS = True in config.py")
        return
    
    print("=== Interactive ENA/ENB Test ===")
    print("Commands:")
    print("w = move forward")
    print("s = move backward")
    print("a = turn left")
    print("d = turn right")
    print("q = left motor forward only")
    print("e = right motor forward only")
    print("z = left motor backward only")
    print("c = right motor backward only")
    print("1-9 = set speed (10%-90%)")
    print("x = stop")
    print("quit = exit")
    
    motor = MotorController()
    
    try:
        while True:
            command = input("Enter command: ").lower().strip()
            
            if command == 'quit':
                break
            elif command == 'w':
                print("Moving forward...")
                motor.move_forward(35, 0.5)
            elif command == 's':
                print("Moving backward...")
                motor.move_backward(35, 0.5)
            elif command == 'a':
                print("Turning left...")
                motor.turn_left(25, 0.5)
            elif command == 'd':
                print("Turning right...")
                motor.turn_right(25, 0.5)
            elif command == 'q':
                print("Left motor forward only...")
                motor.set_motor_speeds(35, 0)
                motor.set_motor_directions(True, True)
            elif command == 'e':
                print("Right motor forward only...")
                motor.set_motor_speeds(0, 35)
                motor.set_motor_directions(True, True)
            elif command == 'z':
                print("Left motor backward only...")
                motor.set_motor_speeds(35, 0)
                motor.set_motor_directions(False, True)
            elif command == 'c':
                print("Right motor backward only...")
                motor.set_motor_speeds(0, 35)
                motor.set_motor_directions(True, False)
            elif command.isdigit():
                speed = int(command) * 10
                if 10 <= speed <= 90:
                    print(f"Setting speed to {speed}%...")
                    motor.set_motor_speeds(speed, speed)
                else:
                    print("Invalid speed (use 1-9 for 10%-90%)")
            elif command == 'x':
                print("Stopping...")
                motor.stop()
            else:
                print("Invalid command")
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error during interactive test: {e}")
    finally:
        motor.cleanup()

def main():
    """Main test function."""
    print("=== ENA/ENB Motor Control Test Suite ===")
    print(f"Control Method: {'ENA/ENB' if USE_ENABLE_PINS else 'Direct PWM'}")
    print()
    
    while True:
        print("Choose test:")
        print("1. Control method info")
        print("2. Basic movements")
        print("3. ENA/ENB specific test")
        print("4. Speed comparison")
        print("5. Interactive ENA/ENB test")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            test_control_method()
        elif choice == "2":
            test_basic_movements()
        elif choice == "3":
            test_ena_enb_specific()
        elif choice == "4":
            test_speed_comparison()
        elif choice == "5":
            interactive_ena_enb_test()
        elif choice == "6":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
