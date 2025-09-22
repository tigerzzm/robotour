"""
Check power supply voltage and current capabilities.
"""

import time
import RPi.GPIO as GPIO
from config import *

def check_voltage_levels():
    """Check voltage levels at different points."""
    print("=== Voltage Level Check ===")
    
    print("VOLTAGE MEASUREMENTS NEEDED:")
    print("Use a multimeter to measure these voltages:")
    print()
    
    print("1. BATTERY VOLTAGE:")
    print(f"   - Should be ~{BATTERY_VOLTAGE}V")
    print("   - If below 11V, battery is low")
    print()
    
    print("2. LM2596S OUTPUT:")
    print(f"   - Should be ~{MOTOR_VOLTAGE}V")
    print("   - If below 5.5V, adjust LM2596S")
    print()
    
    print("3. L298N +12V INPUT:")
    print("   - Should be same as LM2596S output")
    print("   - If lower, check connection")
    print()
    
    print("4. L298N +5V:")
    print("   - Should be ~5V")
    print("   - If lower, check Pi 5V connection")
    print()
    
    print("5. L298N OUTPUT (when motor running):")
    print("   - OUT1/OUT2: Should show voltage when left motor running")
    print("   - OUT3/OUT4: Should show voltage when right motor running")
    print()

def check_current_requirements():
    """Check current requirements vs supply."""
    print("=== Current Requirements Check ===")
    
    print("CURRENT REQUIREMENTS:")
    print(f"- Your motors: 2.8A max stall current each")
    print(f"- Total max: 5.6A (both motors stalled)")
    print(f"- Normal operation: ~0.5-1A each")
    print()
    
    print("POWER SUPPLY CAPABILITIES:")
    print(f"- LM2596S max current: {LM2596S_MAX_CURRENT}A")
    print(f"- LM2596S recommended: {LM2596S_RECOMMENDED_CURRENT}A")
    print(f"- L298N max current: {L298N_MAX_CURRENT}A per channel")
    print()
    
    print("CURRENT ANALYSIS:")
    print("✓ LM2596S can handle 3A max")
    print("✓ L298N can handle 2A per channel")
    print("⚠️  Your motors need 2.8A max each")
    print("⚠️  Total max current (5.6A) exceeds LM2596S (3A)")
    print()
    
    print("SOLUTIONS:")
    print("1. Use higher current power supply")
    print("2. Run motors at lower speeds")
    print("3. Use one motor at a time")
    print("4. Add current limiting")
    print()

def test_voltage_under_load():
    """Test voltage under load."""
    print("=== Voltage Under Load Test ===")
    
    print("This test will check if voltage drops when motors are running.")
    print("You'll need a multimeter to measure voltage during the test.")
    print()
    
    input("Press Enter when you're ready to start the test...")
    
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
        
        print("Test 1: No load (motors off)")
        print("Measure LM2596S output voltage now...")
        time.sleep(3)
        
        print("Test 2: Light load (30% speed)")
        if USE_ENABLE_PINS:
            ena_pwm.ChangeDutyCycle(30)
            enb_pwm.ChangeDutyCycle(30)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
        
        print("Measure LM2596S output voltage now...")
        time.sleep(3)
        
        print("Test 3: Medium load (60% speed)")
        if USE_ENABLE_PINS:
            ena_pwm.ChangeDutyCycle(60)
            enb_pwm.ChangeDutyCycle(60)
        
        print("Measure LM2596S output voltage now...")
        time.sleep(3)
        
        print("Test 4: High load (100% speed)")
        if USE_ENABLE_PINS:
            ena_pwm.ChangeDutyCycle(100)
            enb_pwm.ChangeDutyCycle(100)
        
        print("Measure LM2596S output voltage now...")
        time.sleep(3)
        
        # Stop motors
        if USE_ENABLE_PINS:
            ena_pwm.ChangeDutyCycle(0)
            enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        
        if USE_ENABLE_PINS:
            ena_pwm.stop()
            enb_pwm.stop()
        
        print("✓ Voltage under load test completed")
        print()
        print("ANALYSIS:")
        print("- If voltage drops significantly under load, power supply is insufficient")
        print("- If voltage stays stable, issue is elsewhere")
        print()
        
    except Exception as e:
        print(f"Voltage test error: {e}")

def main():
    """Main function."""
    print("=== POWER SUPPLY DIAGNOSTIC ===")
    print("Motors humming but not moving - Power supply issue")
    print()
    
    while True:
        print("Power Supply Options:")
        print("1. Check voltage levels")
        print("2. Check current requirements")
        print("3. Test voltage under load")
        print("4. Run all checks")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            check_voltage_levels()
        elif choice == "2":
            check_current_requirements()
        elif choice == "3":
            test_voltage_under_load()
        elif choice == "4":
            check_voltage_levels()
            print()
            check_current_requirements()
            print()
            test_voltage_under_load()
        elif choice == "5":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
