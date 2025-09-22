"""
Fix motors humming but not moving - power supply issue.
"""

import time
import RPi.GPIO as GPIO
from config import *

def test_different_speeds():
    """Test motors at different PWM speeds to find minimum working speed."""
    print("=== Motor Speed Test ===")
    print("Testing different speeds to find minimum working speed...")
    
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
        
        # Test different speeds
        speeds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        
        for speed in speeds:
            print(f"Testing speed: {speed}%")
            
            if USE_ENABLE_PINS:
                # ENA/ENB method
                ena_pwm.ChangeDutyCycle(speed)
                enb_pwm.ChangeDutyCycle(speed)
                
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
            
            time.sleep(2)
            
            # Stop motors
            if USE_ENABLE_PINS:
                ena_pwm.ChangeDutyCycle(0)
                enb_pwm.ChangeDutyCycle(0)
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
            
            time.sleep(1)
        
        if USE_ENABLE_PINS:
            ena_pwm.stop()
            enb_pwm.stop()
        
        print("✓ Speed test completed")
        
    except Exception as e:
        print(f"Speed test error: {e}")

def test_individual_motor_speeds():
    """Test each motor individually at different speeds."""
    print("=== Individual Motor Speed Test ===")
    
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
        
        # Test left motor only
        print("Testing LEFT motor only...")
        speeds = [20, 40, 60, 80, 100]
        
        for speed in speeds:
            print(f"  Left motor speed: {speed}%")
            
            if USE_ENABLE_PINS:
                ena_pwm.ChangeDutyCycle(speed)
                enb_pwm.ChangeDutyCycle(0)  # Right motor off
                
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
            
            time.sleep(2)
            
            # Stop left motor
            if USE_ENABLE_PINS:
                ena_pwm.ChangeDutyCycle(0)
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
            
            time.sleep(1)
        
        # Test right motor only
        print("Testing RIGHT motor only...")
        
        for speed in speeds:
            print(f"  Right motor speed: {speed}%")
            
            if USE_ENABLE_PINS:
                ena_pwm.ChangeDutyCycle(0)  # Left motor off
                enb_pwm.ChangeDutyCycle(speed)
                
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
            
            time.sleep(2)
            
            # Stop right motor
            if USE_ENABLE_PINS:
                enb_pwm.ChangeDutyCycle(0)
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
            
            time.sleep(1)
        
        if USE_ENABLE_PINS:
            ena_pwm.stop()
            enb_pwm.stop()
        
        print("✓ Individual motor speed test completed")
        
    except Exception as e:
        print(f"Individual motor test error: {e}")

def check_power_supply_issues():
    """Check common power supply issues that cause humming."""
    print("=== Power Supply Issue Check ===")
    
    print("COMMON CAUSES OF MOTOR HUMMING:")
    print()
    
    print("1. INSUFFICIENT VOLTAGE:")
    print("   - LM2596S output too low (should be 6V)")
    print("   - Battery voltage too low")
    print("   - Voltage drop across L298N")
    print()
    
    print("2. INSUFFICIENT CURRENT:")
    print("   - LM2596S current limit too low")
    print("   - Battery cannot supply enough current")
    print("   - L298N current limit")
    print()
    
    print("3. WRONG VOLTAGE SETTINGS:")
    print("   - LM2596S set to wrong output voltage")
    print("   - L298N getting wrong input voltage")
    print()
    
    print("4. POWER SUPPLY LIMITATIONS:")
    print("   - LM2596S max current: 3A")
    print("   - LM2596S recommended: 2A")
    print("   - Your motors: 2.8A max stall current")
    print()
    
    print("TROUBLESHOOTING STEPS:")
    print("1. Check LM2596S output voltage with multimeter")
    print("2. Check battery voltage")
    print("3. Try higher PWM speeds (70-100%)")
    print("4. Test one motor at a time")
    print("5. Check for voltage drop under load")
    print()

def test_high_speed():
    """Test motors at high speed to see if they move."""
    print("=== High Speed Test ===")
    print("Testing motors at high speed (80-100%)...")
    
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
        
        # Test at high speed
        high_speeds = [80, 90, 100]
        
        for speed in high_speeds:
            print(f"Testing at {speed}% speed...")
            
            if USE_ENABLE_PINS:
                ena_pwm.ChangeDutyCycle(speed)
                enb_pwm.ChangeDutyCycle(speed)
                
                # Both motors forward
                if REVERSE_LEFT_MOTOR:
                    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
                    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
                else:
                    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
                    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
                
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
            
            # Stop motors
            if USE_ENABLE_PINS:
                ena_pwm.ChangeDutyCycle(0)
                enb_pwm.ChangeDutyCycle(0)
            GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
            
            time.sleep(1)
        
        if USE_ENABLE_PINS:
            ena_pwm.stop()
            enb_pwm.stop()
        
        print("✓ High speed test completed")
        
    except Exception as e:
        print(f"High speed test error: {e}")

def main():
    """Main function."""
    print("=== MOTOR HUMMING FIX ===")
    print("Motors humming but not moving - Power supply issue")
    print()
    
    while True:
        print("Fix Options:")
        print("1. Test different speeds")
        print("2. Test individual motors")
        print("3. Test high speed")
        print("4. Check power supply issues")
        print("5. Run all tests")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            test_different_speeds()
        elif choice == "2":
            test_individual_motor_speeds()
        elif choice == "3":
            test_high_speed()
        elif choice == "4":
            check_power_supply_issues()
        elif choice == "5":
            test_different_speeds()
            print()
            test_individual_motor_speeds()
            print()
            test_high_speed()
            print()
            check_power_supply_issues()
        elif choice == "6":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
