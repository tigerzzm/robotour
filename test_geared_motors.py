"""
Test script specifically designed for 130-type geared motors with 1:120 ratio.
This script helps calibrate the timing and speed for optimal performance.
"""

import time
from motor_controller import MotorController
from config import *

def test_motor_specifications():
    """Test and display motor specifications."""
    print("=== Motor Specifications ===")
    print(f"Motor Type: 130-type geared DC motor")
    print(f"Gear Ratio: 1:{MOTOR_GEAR_RATIO}")
    print(f"Rated Voltage: {MOTOR_RATED_VOLTAGE}V")
    print(f"No-load Speed: {MOTOR_NO_LOAD_SPEED} rpm")
    print(f"Output Speed: {MOTOR_OUTPUT_SPEED:.2f} rpm (at wheel)")
    print(f"Max Torque: 0.8 kgf.cm")
    print(f"Max Stall Current: 2.8A")
    print()

def test_speed_calibration():
    """Test different speeds to find optimal settings."""
    print("=== Speed Calibration Test ===")
    print("Testing different PWM speeds for geared motors...")
    
    motor = MotorController()
    
    try:
        speeds = [20, 30, 40, 50, 60, 70, 80]
        
        for speed in speeds:
            print(f"\nTesting speed: {speed}% PWM")
            print("Moving forward for 2 seconds...")
            motor.move_forward(speed, 2.0)
            time.sleep(1)
            
            print("Moving backward for 2 seconds...")
            motor.move_backward(speed, 2.0)
            time.sleep(1)
            
            response = input("Did the movement look good? (y/n/q to quit): ").lower()
            if response == 'q':
                break
            elif response == 'y':
                print(f"Speed {speed}% works well!")
    
    except Exception as e:
        print(f"Error during speed calibration: {e}")
    finally:
        motor.cleanup()

def test_turn_calibration():
    """Test turn timing for 90-degree turns."""
    print("=== Turn Calibration Test ===")
    print("Testing 90-degree turn timing...")
    
    motor = MotorController()
    
    try:
        turn_times = [1.0, 1.2, 1.5, 1.8, 2.0]
        
        for turn_time in turn_times:
            print(f"\nTesting turn time: {turn_time} seconds")
            print("Turning left...")
            motor.turn_left(TURN_SPEED, turn_time)
            time.sleep(1)
            
            print("Turning right...")
            motor.turn_right(TURN_SPEED, turn_time)
            time.sleep(1)
            
            response = input("Was the turn approximately 90 degrees? (y/n/q to quit): ").lower()
            if response == 'q':
                break
            elif response == 'y':
                print(f"Turn time {turn_time}s works well!")
    
    except Exception as e:
        print(f"Error during turn calibration: {e}")
    finally:
        motor.cleanup()

def test_grid_movement():
    """Test movement for one grid cell distance."""
    print("=== Grid Movement Test ===")
    print("Testing movement for one grid cell...")
    
    motor = MotorController()
    
    try:
        move_times = [1.5, 2.0, 2.5, 3.0]
        
        for move_time in move_times:
            print(f"\nTesting move time: {move_time} seconds")
            print("Moving forward...")
            motor.move_forward(FORWARD_SPEED, move_time)
            time.sleep(1)
            
            response = input("Did the robot move approximately one grid cell? (y/n/q to quit): ").lower()
            if response == 'q':
                break
            elif response == 'y':
                print(f"Move time {move_time}s works well!")
    
    except Exception as e:
        print(f"Error during grid movement test: {e}")
    finally:
        motor.cleanup()

def test_precision_movement():
    """Test precision movements for grid navigation."""
    print("=== Precision Movement Test ===")
    print("Testing precision movements for grid navigation...")
    
    motor = MotorController()
    
    try:
        print("Starting precision test sequence...")
        
        # Test forward movement
        print("1. Moving forward one grid cell...")
        motor.move_forward_grid_cell(FORWARD_SPEED)
        time.sleep(1)
        
        # Test 90-degree turn
        print("2. Turning right 90 degrees...")
        motor.turn_right_90(TURN_SPEED)
        time.sleep(1)
        
        # Test forward again
        print("3. Moving forward one grid cell...")
        motor.move_forward_grid_cell(FORWARD_SPEED)
        time.sleep(1)
        
        # Test another turn
        print("4. Turning left 90 degrees...")
        motor.turn_left_90(TURN_SPEED)
        time.sleep(1)
        
        # Test pivot turn
        print("5. Pivoting right 90 degrees...")
        motor.pivot_right_90(TURN_SPEED)
        time.sleep(1)
        
        print("Precision test sequence completed!")
        
    except Exception as e:
        print(f"Error during precision test: {e}")
    finally:
        motor.cleanup()

def manual_geared_motor_test():
    """Manual test for geared motors with specific commands."""
    print("=== Manual Geared Motor Test ===")
    print("Commands:")
    print("w = move forward grid cell")
    print("s = move backward")
    print("a = turn left 90°")
    print("d = turn right 90°")
    print("q = left pivot 90°")
    print("e = right pivot 90°")
    print("x = stop")
    print("quit = exit")
    
    motor = MotorController()
    
    try:
        while True:
            command = input("Enter command: ").lower().strip()
            
            if command == 'quit':
                break
            elif command == 'w':
                print("Moving forward one grid cell...")
                motor.move_forward_grid_cell(FORWARD_SPEED)
            elif command == 's':
                print("Moving backward...")
                motor.move_backward(FORWARD_SPEED, 1.0)
            elif command == 'a':
                print("Turning left 90°...")
                motor.turn_left_90(TURN_SPEED)
            elif command == 'd':
                print("Turning right 90°...")
                motor.turn_right_90(TURN_SPEED)
            elif command == 'q':
                print("Pivoting left 90°...")
                motor.pivot_left_90(TURN_SPEED)
            elif command == 'e':
                print("Pivoting right 90°...")
                motor.pivot_right_90(TURN_SPEED)
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
    print("=== Geared Motor Test Suite ===")
    print("Designed for 130-type motors with 1:120 gear ratio")
    print()
    
    test_motor_specifications()
    
    while True:
        print("Choose test:")
        print("1. Speed calibration")
        print("2. Turn calibration")
        print("3. Grid movement test")
        print("4. Precision movement test")
        print("5. Manual test")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            test_speed_calibration()
        elif choice == "2":
            test_turn_calibration()
        elif choice == "3":
            test_grid_movement()
        elif choice == "4":
            test_precision_movement()
        elif choice == "5":
            manual_geared_motor_test()
        elif choice == "6":
            break
        else:
            print("Invalid choice")
        
        print()
