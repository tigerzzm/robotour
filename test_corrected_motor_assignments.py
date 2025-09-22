"""
Test corrected left/right motor assignments.
"""

import time
import RPi.GPIO as GPIO
from config import *

def test_motor_assignments():
    """Test the corrected motor assignments."""
    print("=== Corrected Motor Assignment Test ===")
    print("Testing left and right motor assignments...")
    print()
    
    print("CURRENT MOTOR ASSIGNMENTS:")
    print(f"Left Motor:")
    print(f"  - Forward: GPIO {MOTOR_LEFT_FORWARD} (IN3)")
    print(f"  - Backward: GPIO {MOTOR_LEFT_BACKWARD} (IN4)")
    print(f"  - Enable: GPIO {ENB_PIN} (ENB)")
    print()
    print(f"Right Motor:")
    print(f"  - Forward: GPIO {MOTOR_RIGHT_FORWARD} (IN1)")
    print(f"  - Backward: GPIO {MOTOR_RIGHT_BACKWARD} (IN2)")
    print(f"  - Enable: GPIO {ENA_PIN} (ENA)")
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
        
        # Test left motor only
        print("Testing LEFT motor only...")
        print("Expected: Left motor should move forward")
        
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
        
        # Test right motor only
        print("Testing RIGHT motor only...")
        print("Expected: Right motor should move forward")
        
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
        
        ena_pwm.stop()
        enb_pwm.stop()
        
        print("✓ Motor assignment test completed")
        
    except Exception as e:
        print(f"Motor assignment test error: {e}")

def test_forward_movement():
    """Test forward movement with corrected assignments."""
    print("=== Forward Movement Test ===")
    print("Testing forward movement with corrected motor assignments...")
    
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
        
        print("Testing forward movement...")
        print("Expected: Robot should move straight forward")
        
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
        
        # Stop motors
        ena_pwm.ChangeDutyCycle(0)
        enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        ena_pwm.stop()
        enb_pwm.stop()
        
        print("✓ Forward movement test completed")
        
    except Exception as e:
        print(f"Forward movement test error: {e}")

def test_turning():
    """Test turning with corrected assignments."""
    print("=== Turning Test ===")
    print("Testing turning with corrected motor assignments...")
    
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
        
        # Test left turn
        print("Testing LEFT turn...")
        print("Expected: Robot should turn left")
        
        ena_pwm.ChangeDutyCycle(30)  # Right motor
        enb_pwm.ChangeDutyCycle(30)  # Left motor
        
        # Left motor backward
        if REVERSE_LEFT_MOTOR:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        else:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
        
        # Right motor forward
        if REVERSE_RIGHT_MOTOR:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(2)
        
        # Stop motors
        ena_pwm.ChangeDutyCycle(0)
        enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        time.sleep(1)
        
        # Test right turn
        print("Testing RIGHT turn...")
        print("Expected: Robot should turn right")
        
        ena_pwm.ChangeDutyCycle(30)  # Right motor
        enb_pwm.ChangeDutyCycle(30)  # Left motor
        
        # Left motor forward
        if REVERSE_LEFT_MOTOR:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
        else:
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        
        # Right motor backward
        if REVERSE_RIGHT_MOTOR:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        else:
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        
        time.sleep(2)
        
        # Stop motors
        ena_pwm.ChangeDutyCycle(0)
        enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        ena_pwm.stop()
        enb_pwm.stop()
        
        print("✓ Turning test completed")
        
    except Exception as e:
        print(f"Turning test error: {e}")

def main():
    """Main function."""
    print("=== CORRECTED MOTOR ASSIGNMENT TEST ===")
    print("Testing left and right motor assignments after correction")
    print()
    
    while True:
        print("Test Options:")
        print("1. Test motor assignments")
        print("2. Test forward movement")
        print("3. Test turning")
        print("4. Run all tests")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            test_motor_assignments()
        elif choice == "2":
            test_forward_movement()
        elif choice == "3":
            test_turning()
        elif choice == "4":
            test_motor_assignments()
            print()
            test_forward_movement()
            print()
            test_turning()
        elif choice == "5":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
