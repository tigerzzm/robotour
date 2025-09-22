"""
Compare left and right motor functionality to isolate the issue.
"""

import time
import RPi.GPIO as GPIO
from config import *

def test_left_motor_only():
    """Test left motor in isolation."""
    print("=== Left Motor Only Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up left motor pins
        GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
        
        if USE_ENABLE_PINS:
            GPIO.setup(ENA_PIN, GPIO.OUT)
            ena_pwm = GPIO.PWM(ENA_PIN, PWM_FREQUENCY)
            ena_pwm.start(0)
        
        print("Testing left motor forward (30% speed)...")
        if USE_ENABLE_PINS:
            ena_pwm.ChangeDutyCycle(30)
            if REVERSE_LEFT_MOTOR:
                GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
                GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
            else:
                GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        else:
            if REVERSE_LEFT_MOTOR:
                GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
                GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            else:
                GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop motor
        if USE_ENABLE_PINS:
            ena_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        
        print("✓ Left motor test completed")
        return True
        
    except Exception as e:
        print(f"Left motor test error: {e}")
        return False

def test_right_motor_only():
    """Test right motor in isolation."""
    print("=== Right Motor Only Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up right motor pins
        GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
        
        if USE_ENABLE_PINS:
            GPIO.setup(ENB_PIN, GPIO.OUT)
            enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
            enb_pwm.start(0)
        
        print("Testing right motor forward (30% speed)...")
        if USE_ENABLE_PINS:
            enb_pwm.ChangeDutyCycle(30)
            if REVERSE_RIGHT_MOTOR:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
            else:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        else:
            if REVERSE_RIGHT_MOTOR:
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            else:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop motor
        if USE_ENABLE_PINS:
            enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        print("✓ Right motor test completed")
        return True
        
    except Exception as e:
        print(f"Right motor test error: {e}")
        return False

def test_both_motors():
    """Test both motors together."""
    print("=== Both Motors Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up all pins
        GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
        
        if USE_ENABLE_PINS:
            GPIO.setup(ENA_PIN, GPIO.OUT)
            GPIO.setup(ENB_PIN, GPIO.OUT)
            ena_pwm = GPIO.PWM(ENA_PIN, PWM_FREQUENCY)
            enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
            ena_pwm.start(0)
            enb_pwm.start(0)
        
        print("Testing both motors forward (30% speed)...")
        if USE_ENABLE_PINS:
            ena_pwm.ChangeDutyCycle(30)
            enb_pwm.ChangeDutyCycle(30)
            
            # Left motor
            if REVERSE_LEFT_MOTOR:
                GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
                GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
            else:
                GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
            
            # Right motor
            if REVERSE_RIGHT_MOTOR:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
            else:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        else:
            # Direct PWM method
            if REVERSE_LEFT_MOTOR:
                GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
                GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            else:
                GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
            
            if REVERSE_RIGHT_MOTOR:
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            else:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(3)
        
        # Stop all motors
        if USE_ENABLE_PINS:
            ena_pwm.ChangeDutyCycle(0)
            enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        print("✓ Both motors test completed")
        return True
        
    except Exception as e:
        print(f"Both motors test error: {e}")
        return False

def main():
    """Main comparison function."""
    print("=== Motor Comparison Test ===")
    print(f"Control Method: {'ENA/ENB' if USE_ENABLE_PINS else 'Direct PWM'}")
    print(f"REVERSE_LEFT_MOTOR: {REVERSE_LEFT_MOTOR}")
    print(f"REVERSE_RIGHT_MOTOR: {REVERSE_RIGHT_MOTOR}")
    print()
    
    print("This test will help identify if the issue is with:")
    print("- Left motor only")
    print("- Right motor only") 
    print("- Both motors")
    print("- Wiring/power issues")
    print()
    
    input("Press Enter to start the test...")
    
    # Test left motor
    left_result = test_left_motor_only()
    time.sleep(2)
    
    # Test right motor
    right_result = test_right_motor_only()
    time.sleep(2)
    
    # Test both motors
    both_result = test_both_motors()
    
    print("\n=== Test Results ===")
    print(f"Left Motor: {'✓ WORKING' if left_result else '✗ NOT WORKING'}")
    print(f"Right Motor: {'✓ WORKING' if right_result else '✗ NOT WORKING'}")
    print(f"Both Motors: {'✓ WORKING' if both_result else '✗ NOT WORKING'}")
    
    print("\n=== Diagnosis ===")
    if left_result and right_result:
        print("🎉 Both motors are working individually!")
        if not both_result:
            print("⚠️  Issue when running both motors together - check power supply")
    elif left_result and not right_result:
        print("🔍 Right motor issue detected:")
        print("   - Check right motor wiring (OUT3, OUT4)")
        print("   - Check ENB pin connection (GPIO 17)")
        print("   - Check right motor power supply")
        print("   - Test right motor with multimeter")
    elif not left_result and right_result:
        print("🔍 Left motor issue detected:")
        print("   - Check left motor wiring (OUT1, OUT2)")
        print("   - Check ENA pin connection (GPIO 14)")
        print("   - Check left motor power supply")
    else:
        print("🔍 Both motors not working:")
        print("   - Check L298N power supply")
        print("   - Check LM2596S output voltage")
        print("   - Check all GPIO connections")
        print("   - Check common ground connections")

if __name__ == "__main__":
    main()
