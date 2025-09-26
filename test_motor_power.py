#!/usr/bin/env python3
"""
Test motor power levels to find the minimum speed for movement.
"""

import time
from motor_controller import MotorController
from config import *

def test_motor_power_levels():
    """Test different power levels to find minimum for movement."""
    print("=== Motor Power Level Test ===")
    print("Testing different power levels to find minimum for movement...")
    
    with MotorController() as motor:
        # Test power levels from 30% to 70%
        power_levels = [30, 35, 40, 45, 50, 55, 60, 65, 70]
        
        for power in power_levels:
            print(f"\nTesting {power}% power...")
            print("  Moving forward for 2 seconds...")
            
            try:
                motor.move_forward(power, 2.0)
                print(f"  ✅ {power}% power: Motor moved successfully")
            except Exception as e:
                print(f"  ❌ {power}% power: Error - {e}")
            
            time.sleep(1)  # Pause between tests
        
        print("\n=== Power Test Complete ===")
        print("Note the minimum power level where motors actually move")
        print("Update config.py with the working minimum speed")

def test_ramp_up():
    """Test gradual speed increase."""
    print("\n=== Ramp-up Test ===")
    print("Testing gradual speed increase to overcome starting torque...")
    
    with MotorController() as motor:
        print("Testing ramp-up from 0% to 50%...")
        try:
            # Set direction first
            if USE_ENABLE_PINS:
                motor.ena_pwm.ChangeDutyCycle(0)
                motor.enb_pwm.ChangeDutyCycle(0)
                # Set direction pins
                motor.left_forward_pin.ChangeDutyCycle(100)
                motor.left_backward_pin.ChangeDutyCycle(0)
                motor.right_forward_pin.ChangeDutyCycle(100)
                motor.right_backward_pin.ChangeDutyCycle(0)
            
            # Ramp up speed
            motor.ramp_up_motor(50, 1.0)
            time.sleep(2)
            motor.stop()
            print("  ✅ Ramp-up test completed")
        except Exception as e:
            print(f"  ❌ Ramp-up test failed: {e}")

if __name__ == "__main__":
    test_motor_power_levels()
    test_ramp_up()
