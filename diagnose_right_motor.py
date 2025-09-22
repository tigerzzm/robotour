"""
Diagnostic script specifically for right motor not moving issue.
"""

import time
import RPi.GPIO as GPIO
from config import *

def check_gpio_pins():
    """Check if right motor GPIO pins are working."""
    print("=== Right Motor GPIO Pin Check ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Right motor pins
        right_pins = {
            'IN3 (Right Forward)': MOTOR_RIGHT_FORWARD,
            'IN4 (Right Backward)': MOTOR_RIGHT_BACKWARD,
            'ENB (Right Enable)': ENB_PIN
        }
        
        print("Right Motor GPIO Configuration:")
        for name, pin in right_pins.items():
            try:
                GPIO.setup(pin, GPIO.OUT)
                print(f"✓ {name}: GPIO {pin} - OK")
            except Exception as e:
                print(f"✗ {name}: GPIO {pin} - ERROR: {e}")
        
        print()
        
    except Exception as e:
        print(f"GPIO setup error: {e}")
        return False
    
    return True

def test_right_motor_pins():
    """Test right motor pins individually."""
    print("=== Right Motor Pin Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Test IN3 (Right Forward)
        print("Testing IN3 (Right Forward) - GPIO", MOTOR_RIGHT_FORWARD)
        GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        print("✓ IN3 test completed")
        
        # Test IN4 (Right Backward)
        print("Testing IN4 (Right Backward) - GPIO", MOTOR_RIGHT_BACKWARD)
        GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        print("✓ IN4 test completed")
        
        # Test ENB (Right Enable)
        if USE_ENABLE_PINS:
            print("Testing ENB (Right Enable) - GPIO", ENB_PIN)
            GPIO.setup(ENB_PIN, GPIO.OUT)
            GPIO.output(ENB_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(ENB_PIN, GPIO.LOW)
            print("✓ ENB test completed")
        
        print()
        
    except Exception as e:
        print(f"Pin test error: {e}")
        return False
    
    return True

def test_right_motor_pwm():
    """Test PWM on right motor enable pin."""
    if not USE_ENABLE_PINS:
        print("ENA/ENB method not enabled, skipping PWM test")
        return True
    
    print("=== Right Motor PWM Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        print("Testing ENB PWM (Right Motor Enable)...")
        GPIO.setup(ENB_PIN, GPIO.OUT)
        enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
        enb_pwm.start(0)
        
        for duty in [25, 50, 75, 100]:
            print(f"  ENB PWM: {duty}%")
            enb_pwm.ChangeDutyCycle(duty)
            time.sleep(1)
        
        enb_pwm.stop()
        print("✓ ENB PWM test completed")
        print()
        
    except Exception as e:
        print(f"PWM test error: {e}")
        return False
    
    return True

def test_right_motor_only():
    """Test right motor in isolation."""
    print("=== Right Motor Only Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up all pins
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
        
        print("Testing right motor backward (30% speed)...")
        if USE_ENABLE_PINS:
            if REVERSE_RIGHT_MOTOR:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
            else:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        else:
            if REVERSE_RIGHT_MOTOR:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
            else:
                GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
                GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
        
        time.sleep(3)
        
        # Stop motor
        if USE_ENABLE_PINS:
            enb_pwm.ChangeDutyCycle(0)
        GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
        
        print("✓ Right motor test completed")
        print()
        
    except Exception as e:
        print(f"Right motor test error: {e}")
        return False
    
    return True

def check_power_connections():
    """Check power supply connections."""
    print("=== Power Supply Check ===")
    
    print("Power Supply Checklist:")
    print("✓ Check that L298N +12V is connected to LM2596S output (6V)")
    print("✓ Check that L298N +5V is connected to Pi 5V")
    print("✓ Check that L298N GND is connected to Pi GND")
    print("✓ Check that LM2596S GND is connected to Pi GND")
    print()
    
    print("Right Motor Power Connections:")
    print("✓ Check that Right Motor + is connected to L298N OUT3")
    print("✓ Check that Right Motor - is connected to L298N OUT4")
    print("✓ Check that motor wires are not loose or broken")
    print()
    
    print("Voltage Measurements (use multimeter):")
    print(f"- LM2596S output should be ~{MOTOR_VOLTAGE}V")
    print("- L298N +5V should be ~5V")
    print("- L298N OUT3 and OUT4 should show voltage when motor is running")
    print()

def check_wiring_connections():
    """Check wiring connections for right motor."""
    print("=== Right Motor Wiring Check ===")
    
    print("L298N Right Motor Connections:")
    print(f"IN3 (Right Forward) -> GPIO {MOTOR_RIGHT_FORWARD}")
    print(f"IN4 (Right Backward) -> GPIO {MOTOR_RIGHT_BACKWARD}")
    if USE_ENABLE_PINS:
        print(f"ENB (Right Enable) -> GPIO {ENB_PIN}")
    print()
    
    print("Physical Connections:")
    print("Right Motor:")
    print("  - Motor + -> L298N OUT3")
    print("  - Motor - -> L298N OUT4")
    print()
    
    print("Common Issues:")
    print("✗ Loose wire connections")
    print("✗ Wrong GPIO pin assignments")
    print("✗ Broken motor wires")
    print("✗ L298N channel B not working")
    print("✗ Insufficient power supply")
    print()

def run_all_diagnostics():
    """Run all diagnostic tests."""
    print("=== Right Motor Diagnostic Suite ===")
    print(f"Control Method: {'ENA/ENB' if USE_ENABLE_PINS else 'Direct PWM'}")
    print(f"REVERSE_RIGHT_MOTOR: {REVERSE_RIGHT_MOTOR}")
    print()
    
    tests = [
        ("GPIO Pin Check", check_gpio_pins),
        ("Pin Test", test_right_motor_pins),
        ("PWM Test", test_right_motor_pwm),
        ("Right Motor Only", test_right_motor_only)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Test failed with error: {e}")
            results.append((test_name, False))
        print()
    
    print("=== Diagnostic Results ===")
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Check power and wiring connections.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
    
    print()
    check_power_connections()
    check_wiring_connections()

def main():
    """Main diagnostic function."""
    print("=== Right Motor Not Moving - Diagnostic Tool ===")
    print()
    
    while True:
        print("Diagnostic Options:")
        print("1. Check GPIO pins")
        print("2. Test right motor pins")
        print("3. Test right motor PWM")
        print("4. Test right motor only")
        print("5. Check power connections")
        print("6. Check wiring connections")
        print("7. Run all diagnostics")
        print("8. Exit")
        
        choice = input("Enter choice (1-8): ").strip()
        
        if choice == "1":
            check_gpio_pins()
        elif choice == "2":
            test_right_motor_pins()
        elif choice == "3":
            test_right_motor_pwm()
        elif choice == "4":
            test_right_motor_only()
        elif choice == "5":
            check_power_connections()
        elif choice == "6":
            check_wiring_connections()
        elif choice == "7":
            run_all_diagnostics()
        elif choice == "8":
            break
        else:
            print("Invalid choice")
        
        print()

if __name__ == "__main__":
    main()
