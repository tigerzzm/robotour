"""
Calibration script specifically for 50cm x 50cm grid cells.
This script helps determine the exact timing needed for your robot to move
precisely one grid cell (50cm) with the geared motors.
"""

import time
from motor_controller import MotorController
from config import *

def calculate_theoretical_timing():
    """Calculate theoretical timing based on motor specifications."""
    print("=== Theoretical Timing Calculations ===")
    print(f"Grid cell size: {GRID_CELL_SIZE_CM}cm")
    print(f"Wheel diameter: {WHEEL_DIAMETER_CM}cm")
    print(f"Wheel circumference: {WHEEL_CIRCUMFERENCE_CM:.1f}cm")
    print(f"Motor output speed: {MOTOR_OUTPUT_SPEED:.2f} rpm")
    print()
    
    # Calculate revolutions needed for 50cm
    revolutions_needed = GRID_CELL_SIZE_CM / WHEEL_CIRCUMFERENCE_CM
    print(f"Revolutions needed for 50cm: {revolutions_needed:.2f}")
    
    # Calculate time at different speeds
    speeds = [25, 35, 50, 70, 100]  # PWM duty cycles
    
    print("\nTheoretical timing at different PWM speeds:")
    print("PWM% | Speed (rpm) | Time for 50cm")
    print("-" * 35)
    
    for pwm in speeds:
        # Estimate actual speed based on PWM (rough approximation)
        estimated_speed = (MOTOR_OUTPUT_SPEED * pwm / 100) * 0.7  # 70% efficiency
        time_needed = (revolutions_needed / estimated_speed) * 60  # Convert to seconds
        print(f"{pwm:3d}% | {estimated_speed:8.2f} | {time_needed:8.1f}s")
    
    print()

def test_50cm_movement():
    """Test movement for exactly 50cm."""
    print("=== 50cm Movement Calibration ===")
    print("This test will help you find the exact timing for 50cm movement.")
    print("Place your robot at the start of a 50cm distance and run the test.")
    print()
    
    motor = MotorController()
    
    try:
        # Test different PWM speeds and times
        test_configs = [
            (35, 6.0),   # 35% PWM for 6 seconds
            (35, 8.0),   # 35% PWM for 8 seconds
            (35, 10.0),  # 35% PWM for 10 seconds
            (50, 4.0),   # 50% PWM for 4 seconds
            (50, 6.0),   # 50% PWM for 6 seconds
            (50, 8.0),   # 50% PWM for 8 seconds
            (70, 3.0),   # 70% PWM for 3 seconds
            (70, 4.0),   # 70% PWM for 4 seconds
            (70, 5.0),   # 70% PWM for 5 seconds
        ]
        
        for i, (speed, duration) in enumerate(test_configs, 1):
            print(f"\nTest {i}: {speed}% PWM for {duration} seconds")
            input("Press Enter when ready to start test...")
            
            print("Moving forward...")
            motor.move_forward(speed, duration)
            
            result = input("Did the robot move approximately 50cm? (y/n/s for skip): ").lower()
            if result == 'y':
                print(f"✅ Found good settings: {speed}% PWM for {duration}s")
                return speed, duration
            elif result == 's':
                continue
            else:
                print("❌ Not quite right, trying next configuration...")
            
            time.sleep(1)
        
        print("\nNo perfect match found. You may need to adjust the configurations.")
        return None, None
    
    except Exception as e:
        print(f"Error during calibration: {e}")
        return None, None
    finally:
        motor.cleanup()

def test_turn_calibration():
    """Test 90-degree turn calibration."""
    print("=== 90-Degree Turn Calibration ===")
    print("This test will help you find the exact timing for 90-degree turns.")
    print()
    
    motor = MotorController()
    
    try:
        turn_times = [1.5, 2.0, 2.5, 3.0, 3.5]
        
        for turn_time in turn_times:
            print(f"\nTesting turn time: {turn_time} seconds")
            input("Press Enter when ready to start turn test...")
            
            print("Turning left...")
            motor.turn_left(TURN_SPEED, turn_time)
            time.sleep(1)
            
            result = input("Was the turn approximately 90 degrees? (y/n/s for skip): ").lower()
            if result == 'y':
                print(f"✅ Found good turn time: {turn_time}s")
                return turn_time
            elif result == 's':
                continue
            else:
                print("❌ Not quite right, trying next timing...")
            
            time.sleep(1)
        
        print("\nNo perfect turn time found. You may need to adjust manually.")
        return None
    
    except Exception as e:
        print(f"Error during turn calibration: {e}")
        return None
    finally:
        motor.cleanup()

def update_config_file(forward_speed, forward_time, turn_time):
    """Update the config file with calibrated values."""
    if forward_speed and forward_time and turn_time:
        print(f"\n=== Updating Configuration ===")
        print(f"Recommended settings:")
        print(f"  FORWARD_SPEED = {forward_speed}")
        print(f"  MOVE_FORWARD_TIME = {forward_time}")
        print(f"  TURN_TIME = {turn_time}")
        print()
        print("Please update these values in config.py manually.")
        print("Or run this script again after updating the file.")

def manual_50cm_test():
    """Manual test for 50cm movement."""
    print("=== Manual 50cm Test ===")
    print("Commands:")
    print("w = move forward (current config)")
    print("s = move backward")
    print("a = turn left")
    print("d = turn right")
    print("1-9 = move forward with different speeds (10%-90%)")
    print("t = test current forward settings")
    print("x = stop")
    print("quit = exit")
    
    motor = MotorController()
    
    try:
        while True:
            command = input("Enter command: ").lower().strip()
            
            if command == 'quit':
                break
            elif command == 'w':
                print("Moving forward with current config...")
                motor.move_forward_grid_cell(FORWARD_SPEED)
            elif command == 's':
                print("Moving backward...")
                motor.move_backward(FORWARD_SPEED, 2.0)
            elif command == 'a':
                print("Turning left...")
                motor.turn_left_90(TURN_SPEED)
            elif command == 'd':
                print("Turning right...")
                motor.turn_right_90(TURN_SPEED)
            elif command == 't':
                print("Testing current forward settings...")
                motor.move_forward(FORWARD_SPEED, MOVE_FORWARD_TIME)
            elif command.isdigit():
                speed = int(command) * 10
                if 10 <= speed <= 90:
                    print(f"Moving forward at {speed}% PWM for 5 seconds...")
                    motor.move_forward(speed, 5.0)
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
        print(f"Error during manual test: {e}")
    finally:
        motor.cleanup()

if __name__ == "__main__":
    print("=== 50cm Grid Calibration Tool ===")
    print("This tool helps calibrate your robot for 50cm x 50cm grid cells.")
    print()
    
    calculate_theoretical_timing()
    
    while True:
        print("Choose calibration option:")
        print("1. Test 50cm movement")
        print("2. Test 90-degree turns")
        print("3. Manual test")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            forward_speed, forward_time = test_50cm_movement()
            if forward_speed and forward_time:
                turn_time = test_turn_calibration()
                update_config_file(forward_speed, forward_time, turn_time)
        elif choice == "2":
            test_turn_calibration()
        elif choice == "3":
            manual_50cm_test()
        elif choice == "4":
            break
        else:
            print("Invalid choice")
        
        print()
