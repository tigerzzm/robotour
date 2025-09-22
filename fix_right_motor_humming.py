"""
Fix right motor humming but not moving - specific diagnostic.
"""

import time
import RPi.GPIO as GPIO
from config import *

def test_right_motor_only():
    """Test right motor in isolation with different speeds."""
    print("=== Right Motor Only Test ===")
    print("Testing right motor with different speeds...")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up right motor pins only
        GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
        GPIO.setup(ENB_PIN, GPIO.OUT)
        
        enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
        enb_pwm.start(0)
        
        # Test different speeds
        speeds = [20, 40, 60, 80, 100]
        
        for speed in speeds:
            print(f"Testing right motor at {speed}% speed...")
            
            enb_pwm.ChangeDutyCycle(speed)
            
            # Right motor forward (with reverse setting)
            if REVERSE_RIGHT_MOTOR:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
            else:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
            
            time.sleep(3)
            
            # Stop motor
            enb_pwm.ChangeDutyCycle(0)
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
            
            time.sleep(1)
        
        enb_pwm.stop()
        print("✓ Right motor test completed")
        
    except Exception as e:
        print(f"Right motor test error: {e}")

def test_right_motor_direct():
    """Test right motor with direct GPIO control (no PWM)."""
    print("=== Right Motor Direct Test ===")
    print("Testing right motor with direct GPIO control...")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up right motor pins
        GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
        GPIO.setup(ENB_PIN, GPIO.OUT)
        
        print("Testing right motor forward (direct control)...")
        
        # Enable right motor
        GPIO.output(ENB_PIN, GPIO.HIGH)
        
        # Right motor forward
        if REVERSE_RIGHT_MOTOR:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop motor
        GPIO.output(ENB_PIN, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        print("✓ Right motor direct test completed")
        
    except Exception as e:
        print(f"Right motor direct test error: {e}")

def test_right_motor_wiring():
    """Test right motor wiring connections."""
    print("=== Right Motor Wiring Test ===")
    
    print("RIGHT MOTOR WIRING CHECKLIST:")
    print()
    
    print("1. L298N CONNECTIONS:")
    print(f"   - IN3 (Right Forward) -> GPIO {MOTOR_RIGHT_FORWARD}")
    print(f"   - IN4 (Right Backward) -> GPIO {MOTOR_RIGHT_BACKWARD}")
    print(f"   - ENB (Right Enable) -> GPIO {ENB_PIN}")
    print()
    
    print("2. MOTOR CONNECTIONS:")
    print("   - Right Motor + -> L298N OUT3")
    print("   - Right Motor - -> L298N OUT4")
    print()
    
    print("3. POWER CONNECTIONS:")
    print("   - L298N +12V -> LM2596S output (6V)")
    print("   - L298N +5V -> Pi 5V")
    print("   - L298N GND -> Pi GND")
    print()
    
    print("4. COMMON ISSUES:")
    print("   ✗ Loose wire connections")
    print("   ✗ Wrong GPIO pin assignments")
    print("   ✗ Broken motor wires")
    print("   ✗ L298N channel B not working")
    print("   ✗ Insufficient power supply")
    print()

def test_right_motor_power():
    """Test right motor power supply."""
    print("=== Right Motor Power Test ===")
    
    print("POWER SUPPLY CHECKLIST:")
    print()
    
    print("1. VOLTAGE MEASUREMENTS (use multimeter):")
    print("   - LM2596S output: Should be ~6V")
    print("   - L298N +12V: Should be ~6V")
    print("   - L298N +5V: Should be ~5V")
    print("   - L298N OUT3/OUT4: Should show voltage when motor running")
    print()
    
    print("2. CURRENT REQUIREMENTS:")
    print("   - Right motor: 2.8A max stall current")
    print("   - LM2596S: 3A max total")
    print("   - If both motors running: 5.6A max (exceeds 3A limit)")
    print()
    
    print("3. POWER SUPPLY ISSUES:")
    print("   ✗ LM2596S output too low")
    print("   ✗ Insufficient current supply")
    print("   ✗ Voltage drop under load")
    print("   ✗ L298N channel B not working")
    print()

def test_swap_motor_connections():
    """Test by swapping left and right motor connections."""
    print("=== Motor Connection Swap Test ===")
    
    print("This test will help identify if the issue is with:")
    print("- The right motor itself")
    print("- The L298N channel B")
    print("- The wiring connections")
    print()
    
    print("TEST PROCEDURE:")
    print("1. Disconnect right motor from L298N OUT3/OUT4")
    print("2. Connect right motor to L298N OUT1/OUT2 (left motor connections)")
    print("3. Run left motor test - if right motor moves, issue is with L298N channel B")
    print("4. If right motor still doesn't move, issue is with the motor itself")
    print()
    
    print("ALTERNATIVE TEST:")
    print("1. Disconnect left motor from L298N OUT1/OUT2")
    print("2. Connect left motor to L298N OUT3/OUT4 (right motor connections)")
    print("3. Run right motor test - if left motor moves, L298N channel B is working")
    print()

def main():
    """Main function."""
    print("=== RIGHT MOTOR HUMMING FIX ===")
    print("Right motor humming but not moving")
    print(f"REVERSE_RIGHT_MOTOR: {REVERSE_RIGHT_MOTOR}")
    print()
    
    while True:
        print("Right Motor Fix Options:")
        print("1. Test right motor only")
        print("2. Test right motor direct")
        print("3. Check right motor wiring")
        print("4. Check right motor power")
        print("5. Test motor connection swap")
        print("6. Run all tests")
        print("7. Exit")
        
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == "1":
            test_right_motor_only()
        elif choice == "2":
            test_right_motor_direct()
        elif choice == "3":
            test_right_motor_wiring()
        elif choice == "4":
            test_right_motor_power()
        elif choice == "5":
            test_swap_motor_connections()
        elif choice == "6":
            test_right_motor_only()
            print()
            test_right_motor_direct()
            print()
            test_right_motor_wiring()
            print()
            test_right_motor_power()
            print()
            test_swap_motor_connections()
        elif choice == "7":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
