"""
Emergency diagnostic for when both motors are not moving.
This indicates a fundamental issue with power, wiring, or GPIO.
"""

import time
import RPi.GPIO as GPIO
from config import *

def check_basic_gpio():
    """Check if GPIO is working at all."""
    print("=== Basic GPIO Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Test a simple GPIO pin
        test_pin = 18  # IN1
        print(f"Testing GPIO {test_pin} (IN1)...")
        
        GPIO.setup(test_pin, GPIO.OUT)
        GPIO.output(test_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(test_pin, GPIO.LOW)
        
        print("✓ Basic GPIO test passed")
        return True
        
    except Exception as e:
        print(f"✗ Basic GPIO test failed: {e}")
        return False

def check_power_supply():
    """Check power supply status."""
    print("=== Power Supply Check ===")
    
    print("CRITICAL POWER CHECKS:")
    print("1. Is the 12V battery connected to LM2596S input?")
    print("2. Is LM2596S output set to 6V?")
    print("3. Is L298N +12V connected to LM2596S output?")
    print("4. Is L298N +5V connected to Pi 5V?")
    print("5. Are ALL ground connections common?")
    print()
    
    print("VOLTAGE MEASUREMENTS (use multimeter):")
    print(f"- Battery voltage: Should be ~{BATTERY_VOLTAGE}V")
    print(f"- LM2596S output: Should be ~{MOTOR_VOLTAGE}V")
    print("- Pi 5V pin: Should be ~5V")
    print("- L298N +5V: Should be ~5V")
    print("- L298N +12V: Should be ~6V")
    print()
    
    print("POWER SUPPLY TROUBLESHOOTING:")
    print("✗ No power to L298N")
    print("✗ LM2596S not working")
    print("✗ Battery dead or disconnected")
    print("✗ Wrong voltage settings")
    print("✗ Loose power connections")
    print()

def check_l298n_connections():
    """Check L298N connections."""
    print("=== L298N Connection Check ===")
    
    print("L298N POWER CONNECTIONS:")
    print("✓ +12V -> LM2596S output (6V)")
    print("✓ +5V -> Pi 5V")
    print("✓ GND -> Pi GND")
    print()
    
    print("L298N MOTOR CONNECTIONS:")
    print("Left Motor:")
    print(f"  - Motor + -> OUT1")
    print(f"  - Motor - -> OUT2")
    print("Right Motor:")
    print(f"  - Motor + -> OUT3")
    print(f"  - Motor - -> OUT4")
    print()
    
    print("L298N GPIO CONNECTIONS:")
    print(f"✓ IN1 -> GPIO {MOTOR_LEFT_FORWARD}")
    print(f"✓ IN2 -> GPIO {MOTOR_LEFT_BACKWARD}")
    print(f"✓ IN3 -> GPIO {MOTOR_RIGHT_FORWARD}")
    print(f"✓ IN4 -> GPIO {MOTOR_RIGHT_BACKWARD}")
    if USE_ENABLE_PINS:
        print(f"✓ ENA -> GPIO {ENA_PIN}")
        print(f"✓ ENB -> GPIO {ENB_PIN}")
    print()
    
    print("COMMON L298N ISSUES:")
    print("✗ L298N not getting power")
    print("✗ Wrong voltage input")
    print("✗ L298N damaged")
    print("✗ Loose connections")
    print("✗ Wrong pin assignments")
    print()

def test_l298n_basic():
    """Test L298N with basic GPIO commands."""
    print("=== L298N Basic Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up all motor pins
        motor_pins = [
            MOTOR_LEFT_FORWARD,
            MOTOR_LEFT_BACKWARD,
            MOTOR_RIGHT_FORWARD,
            MOTOR_RIGHT_BACKWARD
        ]
        
        if USE_ENABLE_PINS:
            motor_pins.extend([ENA_PIN, ENB_PIN])
        
        print("Setting up motor pins...")
        for pin in motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            print(f"✓ GPIO {pin} set as output")
        
        print("\nTesting L298N with direct GPIO commands...")
        
        # Test left motor forward
        print("Testing left motor forward...")
        if USE_ENABLE_PINS:
            GPIO.output(ENA_PIN, GPIO.HIGH)  # Enable left motor
        GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
        GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
        time.sleep(2)
        
        # Test right motor forward
        print("Testing right motor forward...")
        if USE_ENABLE_PINS:
            GPIO.output(ENB_PIN, GPIO.HIGH)  # Enable right motor
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        time.sleep(2)
        
        # Stop all motors
        print("Stopping all motors...")
        for pin in motor_pins:
            GPIO.output(pin, GPIO.LOW)
        
        print("✓ L298N basic test completed")
        return True
        
    except Exception as e:
        print(f"✗ L298N basic test failed: {e}")
        return False

def test_motor_wires():
    """Test motor wires directly."""
    print("=== Motor Wire Test ===")
    
    print("MOTOR WIRE TESTING:")
    print("1. Disconnect motor wires from L298N")
    print("2. Use multimeter to test motor resistance")
    print("3. Should show ~10-50 ohms resistance")
    print("4. If infinite resistance, motor is broken")
    print("5. If 0 resistance, motor is shorted")
    print()
    
    print("MOTOR WIRE CONNECTIONS:")
    print("Left Motor:")
    print("  - Red wire -> L298N OUT1")
    print("  - Black wire -> L298N OUT2")
    print("Right Motor:")
    print("  - Red wire -> L298N OUT3")
    print("  - Black wire -> L298N OUT4")
    print()
    
    print("COMMON MOTOR ISSUES:")
    print("✗ Broken motor wires")
    print("✗ Loose connections")
    print("✗ Wrong wire colors")
    print("✗ Damaged motors")
    print()

def emergency_troubleshooting():
    """Emergency troubleshooting steps."""
    print("=== EMERGENCY TROUBLESHOOTING ===")
    print()
    
    print("STEP 1: CHECK POWER")
    print("1. Verify 12V battery is connected")
    print("2. Check LM2596S output voltage (should be 6V)")
    print("3. Check L298N +5V connection to Pi")
    print("4. Verify all ground connections")
    print()
    
    print("STEP 2: CHECK WIRING")
    print("1. Verify all GPIO connections")
    print("2. Check motor wire connections")
    print("3. Ensure no loose connections")
    print("4. Check for broken wires")
    print()
    
    print("STEP 3: TEST COMPONENTS")
    print("1. Test motors with multimeter")
    print("2. Test L298N with simple GPIO")
    print("3. Test Pi GPIO functionality")
    print("4. Check LM2596S output")
    print()
    
    print("STEP 4: SIMPLIFY SETUP")
    print("1. Connect only one motor")
    print("2. Use direct GPIO control")
    print("3. Test with minimal configuration")
    print("4. Gradually add complexity")
    print()

def run_emergency_diagnostics():
    """Run all emergency diagnostics."""
    print("=== EMERGENCY MOTOR DIAGNOSTICS ===")
    print("Both motors not moving - Critical Issue")
    print()
    
    # Check basic GPIO
    gpio_ok = check_basic_gpio()
    print()
    
    # Check power supply
    check_power_supply()
    
    # Check L298N connections
    check_l298n_connections()
    
    # Test L298N basic
    if gpio_ok:
        l298n_ok = test_l298n_basic()
        print()
    else:
        print("Skipping L298N test - GPIO not working")
        l298n_ok = False
    
    # Test motor wires
    test_motor_wires()
    
    # Emergency troubleshooting
    emergency_troubleshooting()
    
    print("=== DIAGNOSTIC SUMMARY ===")
    print(f"GPIO Test: {'✓ PASS' if gpio_ok else '✗ FAIL'}")
    print(f"L298N Test: {'✓ PASS' if l298n_ok else '✗ FAIL'}")
    
    if not gpio_ok:
        print("\n🔍 ISSUE: GPIO not working")
        print("   - Check Pi power supply")
        print("   - Check Pi is booting properly")
        print("   - Check GPIO permissions")
    elif not l298n_ok:
        print("\n🔍 ISSUE: L298N not working")
        print("   - Check power supply to L298N")
        print("   - Check L298N connections")
        print("   - Check motor connections")
    else:
        print("\n🔍 ISSUE: Motors not responding")
        print("   - Check motor wires")
        print("   - Test motors with multimeter")
        print("   - Check motor power supply")

def main():
    """Main emergency diagnostic function."""
    print("=== EMERGENCY MOTOR DIAGNOSTICS ===")
    print("Both motors not moving - Critical Issue")
    print()
    
    while True:
        print("Emergency Options:")
        print("1. Run all diagnostics")
        print("2. Check power supply")
        print("3. Check L298N connections")
        print("4. Test basic GPIO")
        print("5. Test L298N basic")
        print("6. Test motor wires")
        print("7. Emergency troubleshooting")
        print("8. Exit")
        
        choice = input("Enter choice (1-8): ").strip()
        
        if choice == "1":
            run_emergency_diagnostics()
        elif choice == "2":
            check_power_supply()
        elif choice == "3":
            check_l298n_connections()
        elif choice == "4":
            check_basic_gpio()
        elif choice == "5":
            test_l298n_basic()
        elif choice == "6":
            test_motor_wires()
        elif choice == "7":
            emergency_troubleshooting()
        elif choice == "8":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
