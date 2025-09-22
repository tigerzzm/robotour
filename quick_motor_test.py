"""
Quick motor test - runs automatically without user input.
"""

import time
import RPi.GPIO as GPIO
from config import *

def quick_test():
    """Run a quick test of both motors."""
    print("=== Quick Motor Test ===")
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
        
        # Test 1: Left motor only
        print("Test 1: Left motor only (3 seconds)...")
        ena_pwm.ChangeDutyCycle(0)  # Right motor off
        enb_pwm.ChangeDutyCycle(40)  # Left motor on
        
        if REVERSE_LEFT_MOTOR:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop left motor
        enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        
        time.sleep(1)
        
        # Test 2: Right motor only
        print("Test 2: Right motor only (3 seconds)...")
        ena_pwm.ChangeDutyCycle(40)  # Right motor on
        enb_pwm.ChangeDutyCycle(0)   # Left motor off
        
        if REVERSE_RIGHT_MOTOR:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop right motor
        ena_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(1)
        
        # Test 3: Both motors forward
        print("Test 3: Both motors forward (3 seconds)...")
        ena_pwm.ChangeDutyCycle(40)  # Right motor
        enb_pwm.ChangeDutyCycle(40)  # Left motor
        
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
        
        # Stop all motors
        ena_pwm.ChangeDutyCycle(0)
        enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        ena_pwm.stop()
        enb_pwm.stop()
        
        print("✓ Quick motor test completed!")
        print()
        print("RESULTS:")
        print("- Left motor: Should have moved forward")
        print("- Right motor: Should have moved forward")
        print("- Both motors: Robot should have moved forward")
        print()
        print("If movements are correct, your motor setup is working!")
        
    except Exception as e:
        print(f"Quick test error: {e}")

if __name__ == "__main__":
    quick_test()
