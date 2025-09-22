"""
Test both motor directions after fixing the left motor.
"""

import time
import RPi.GPIO as GPIO
from config import *

def test_both_motors():
    """Test both motors with corrected directions."""
    print("=== Both Motors Direction Test ===")
    print(f"REVERSE_LEFT_MOTOR: {REVERSE_LEFT_MOTOR}")
    print(f"REVERSE_RIGHT_MOTOR: {REVERSE_RIGHT_MOTOR}")
    print()
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up all pins
        GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
        GPIO.setup(ENA_PIN, GPIO.OUT)
        GPIO.setup(ENB_PIN, GPIO.OUT)
        
        ena_pwm = GPIO.PWM(ENA_PIN, PWM_FREQUENCY)
        enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
        ena_pwm.start(0)
        enb_pwm.start(0)
        
        # Test forward movement
        print("Testing FORWARD movement...")
        print("Expected: Both motors should rotate forward")
        
        ena_pwm.ChangeDutyCycle(40)
        enb_pwm.ChangeDutyCycle(40)
        
        # Left motor forward
        if REVERSE_LEFT_MOTOR:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        
        # Right motor forward
        if REVERSE_RIGHT_MOTOR:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop motors
        ena_pwm.ChangeDutyCycle(0)
        enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(1)
        
        # Test backward movement
        print("Testing BACKWARD movement...")
        print("Expected: Both motors should rotate backward")
        
        ena_pwm.ChangeDutyCycle(40)
        enb_pwm.ChangeDutyCycle(40)
        
        # Left motor backward
        if REVERSE_LEFT_MOTOR:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        else:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
        
        # Right motor backward
        if REVERSE_RIGHT_MOTOR:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        else:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        
        time.sleep(3)
        
        # Stop motors
        ena_pwm.ChangeDutyCycle(0)
        enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        ena_pwm.stop()
        enb_pwm.stop()
        
        print("✓ Both motors direction test completed")
        
    except Exception as e:
        print(f"Both motors test error: {e}")

def test_individual_motors():
    """Test each motor individually."""
    print("=== Individual Motor Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up all pins
        GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
        GPIO.setup(ENA_PIN, GPIO.OUT)
        GPIO.setup(ENB_PIN, GPIO.OUT)
        
        ena_pwm = GPIO.PWM(ENA_PIN, PWM_FREQUENCY)
        enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
        ena_pwm.start(0)
        enb_pwm.start(0)
        
        # Test left motor only
        print("Testing LEFT motor only...")
        ena_pwm.ChangeDutyCycle(50)
        enb_pwm.ChangeDutyCycle(0)  # Right motor off
        
        if REVERSE_LEFT_MOTOR:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop left motor
        ena_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        
        time.sleep(1)
        
        # Test right motor only
        print("Testing RIGHT motor only...")
        ena_pwm.ChangeDutyCycle(0)  # Left motor off
        enb_pwm.ChangeDutyCycle(50)
        
        if REVERSE_RIGHT_MOTOR:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop right motor
        enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        ena_pwm.stop()
        enb_pwm.stop()
        
        print("✓ Individual motor test completed")
        
    except Exception as e:
        print(f"Individual motor test error: {e}")

def main():
    """Main function."""
    print("=== BOTH MOTORS DIRECTION TEST ===")
    print("Testing corrected motor directions")
    print()
    
    while True:
        print("Test Options:")
        print("1. Test both motors together")
        print("2. Test individual motors")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            test_both_motors()
        elif choice == "2":
            test_individual_motors()
        elif choice == "3":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
