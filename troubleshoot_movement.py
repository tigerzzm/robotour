"""
Comprehensive troubleshooting script for motor movement issues.
This script helps diagnose and fix common problems with basic movements.
"""

import time
import RPi.GPIO as GPIO
from motor_controller import MotorController
from config import *

def check_gpio_setup():
    """Check if GPIO pins are properly configured."""
    print("=== GPIO Setup Check ===")
    
    try:
        # Check if GPIO is already set up
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Check motor pins
        motor_pins = {
            'IN1 (Left Forward)': MOTOR_LEFT_FORWARD,
            'IN2 (Left Backward)': MOTOR_LEFT_BACKWARD,
            'IN3 (Right Forward)': MOTOR_RIGHT_FORWARD,
            'IN4 (Right Backward)': MOTOR_RIGHT_BACKWARD
        }
        
        if USE_ENABLE_PINS:
            motor_pins['ENA (Left Enable)'] = ENA_PIN
            motor_pins['ENB (Right Enable)'] = ENB_PIN
        
        print("GPIO Pin Configuration:")
        for name, pin in motor_pins.items():
            try:
                GPIO.setup(pin, GPIO.OUT)
                print(f"✓ {name}: GPIO {pin} - OK")
            except Exception as e:
                print(f"✗ {name}: GPIO {pin} - ERROR: {e}")
        
        print(f"Control Method: {'ENA/ENB' if USE_ENABLE_PINS else 'Direct PWM'}")
        print()
        
    except Exception as e:
        print(f"GPIO setup error: {e}")
        return False
    
    return True

def test_individual_pins():
    """Test individual GPIO pins to ensure they're working."""
    print("=== Individual Pin Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Test each motor pin individually
        test_pins = [
            ('IN1 (Left Forward)', MOTOR_LEFT_FORWARD),
            ('IN2 (Left Backward)', MOTOR_LEFT_BACKWARD),
            ('IN3 (Right Forward)', MOTOR_RIGHT_FORWARD),
            ('IN4 (Right Backward)', MOTOR_RIGHT_BACKWARD)
        ]
        
        if USE_ENABLE_PINS:
            test_pins.extend([
                ('ENA (Left Enable)', ENA_PIN),
                ('ENB (Right Enable)', ENB_PIN)
            ])
        
        for name, pin in test_pins:
            print(f"Testing {name} (GPIO {pin})...")
            
            try:
                GPIO.setup(pin, GPIO.OUT)
                
                # Test high
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(0.5)
                
                # Test low
                GPIO.output(pin, GPIO.LOW)
                time.sleep(0.5)
                
                print(f"✓ {name} - OK")
                
            except Exception as e:
                print(f"✗ {name} - ERROR: {e}")
        
        print()
        
    except Exception as e:
        print(f"Pin test error: {e}")
        return False
    
    return True

def test_pwm_functionality():
    """Test PWM functionality on enable pins."""
    if not USE_ENABLE_PINS:
        print("ENA/ENB method not enabled, skipping PWM test")
        return True
    
    print("=== PWM Functionality Test ===")
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Test ENA pin
        print("Testing ENA pin PWM...")
        GPIO.setup(ENA_PIN, GPIO.OUT)
        ena_pwm = GPIO.PWM(ENA_PIN, PWM_FREQUENCY)
        ena_pwm.start(0)
        
        for duty in [25, 50, 75, 100]:
            print(f"  ENA PWM: {duty}%")
            ena_pwm.ChangeDutyCycle(duty)
            time.sleep(1)
        
        ena_pwm.stop()
        print("✓ ENA PWM - OK")
        
        # Test ENB pin
        print("Testing ENB pin PWM...")
        GPIO.setup(ENB_PIN, GPIO.OUT)
        enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
        enb_pwm.start(0)
        
        for duty in [25, 50, 75, 100]:
            print(f"  ENB PWM: {duty}%")
            enb_pwm.ChangeDutyCycle(duty)
            time.sleep(1)
        
        enb_pwm.stop()
        print("✓ ENB PWM - OK")
        print()
        
    except Exception as e:
        print(f"PWM test error: {e}")
        return False
    
    return True

def test_motor_controller_initialization():
    """Test motor controller initialization."""
    print("=== Motor Controller Initialization Test ===")
    
    try:
        motor = MotorController()
        print("✓ Motor controller initialized successfully")
        print(f"Control method: {motor.get_control_method()}")
        
        # Test stop function
        motor.stop()
        print("✓ Stop function works")
        
        motor.cleanup()
        print("✓ Cleanup function works")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ Motor controller initialization failed: {e}")
        return False

def test_minimal_movement():
    """Test minimal movement with very low speeds."""
    print("=== Minimal Movement Test ===")
    
    motor = MotorController()
    
    try:
        print("Testing very slow forward movement (10% speed, 1 second)...")
        motor.move_forward(10, 1.0)
        time.sleep(1)
        
        print("Testing very slow backward movement (10% speed, 1 second)...")
        motor.move_backward(10, 1.0)
        time.sleep(1)
        
        print("Testing very slow left turn (5% speed, 0.5 seconds)...")
        motor.turn_left(5, 0.5)
        time.sleep(1)
        
        print("Testing very slow right turn (5% speed, 0.5 seconds)...")
        motor.turn_right(5, 0.5)
        time.sleep(1)
        
        print("✓ Minimal movement test completed")
        return True
        
    except Exception as e:
        print(f"✗ Minimal movement test failed: {e}")
        return False
    finally:
        motor.cleanup()

def test_power_supply():
    """Test power supply and voltage levels."""
    print("=== Power Supply Check ===")
    
    print("Power Supply Configuration:")
    print(f"Battery Voltage: {BATTERY_VOLTAGE}V")
    print(f"Motor Voltage: {MOTOR_VOLTAGE}V")
    print(f"Pi Voltage: {PI_VOLTAGE}V")
    print(f"L298N Voltage Drop: {L298N_VOLTAGE_DROP}V")
    print()
    
    print("Power Supply Checklist:")
    print("✓ Check that 12V battery is connected to LM2596S input")
    print("✓ Check that LM2596S output is set to 6V for motors")
    print("✓ Check that 5V is available for Raspberry Pi")
    print("✓ Check that L298N has 5V logic power")
    print("✓ Check that all ground connections are common")
    print()
    
    print("Voltage Measurements (use multimeter):")
    print(f"- Battery voltage should be ~{BATTERY_VOLTAGE}V")
    print(f"- LM2596S output should be ~{MOTOR_VOLTAGE}V")
    print(f"- Pi 5V pin should be ~{PI_VOLTAGE}V")
    print(f"- L298N +5V should be ~5V")
    print()

def test_wiring_connections():
    """Test wiring connections."""
    print("=== Wiring Connection Check ===")
    
    print("L298N Connections:")
    print(f"IN1 (Left Forward) -> GPIO {MOTOR_LEFT_FORWARD}")
    print(f"IN2 (Left Backward) -> GPIO {MOTOR_LEFT_BACKWARD}")
    print(f"IN3 (Right Forward) -> GPIO {MOTOR_RIGHT_FORWARD}")
    print(f"IN4 (Right Backward) -> GPIO {MOTOR_RIGHT_BACKWARD}")
    
    if USE_ENABLE_PINS:
        print(f"ENA (Left Enable) -> GPIO {ENA_PIN}")
        print(f"ENB (Right Enable) -> GPIO {ENB_PIN}")
    
    print()
    print("Motor Connections:")
    print("Left Motor:")
    print("  - Motor + -> L298N OUT1")
    print("  - Motor - -> L298N OUT2")
    print("Right Motor:")
    print("  - Motor + -> L298N OUT3")
    print("  - Motor - -> L298N OUT4")
    print()
    print("Power Connections:")
    print("  - L298N +12V -> LM2596S output (6V)")
    print("  - L298N +5V -> Pi 5V")
    print("  - L298N GND -> Pi GND")
    print("  - LM2596S GND -> Pi GND")
    print()

def interactive_diagnosis():
    """Interactive diagnosis tool."""
    print("=== Interactive Diagnosis ===")
    
    while True:
        print("\nDiagnosis Options:")
        print("1. Test GPIO setup")
        print("2. Test individual pins")
        print("3. Test PWM functionality")
        print("4. Test motor controller")
        print("5. Test minimal movement")
        print("6. Check power supply")
        print("7. Check wiring")
        print("8. Run all tests")
        print("9. Exit")
        
        choice = input("Enter choice (1-9): ").strip()
        
        if choice == "1":
            check_gpio_setup()
        elif choice == "2":
            test_individual_pins()
        elif choice == "3":
            test_pwm_functionality()
        elif choice == "4":
            test_motor_controller_initialization()
        elif choice == "5":
            test_minimal_movement()
        elif choice == "6":
            test_power_supply()
        elif choice == "7":
            test_wiring_connections()
        elif choice == "8":
            run_all_tests()
        elif choice == "9":
            break
        else:
            print("Invalid choice")

def run_all_tests():
    """Run all diagnostic tests."""
    print("=== Running All Diagnostic Tests ===")
    
    tests = [
        ("GPIO Setup", check_gpio_setup),
        ("Individual Pins", test_individual_pins),
        ("PWM Functionality", test_pwm_functionality),
        ("Motor Controller", test_motor_controller_initialization),
        ("Minimal Movement", test_minimal_movement)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Test failed with error: {e}")
            results.append((test_name, False))
    
    print("\n=== Test Results Summary ===")
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your motor setup should be working.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")

def main():
    """Main troubleshooting function."""
    print("=== Motor Movement Troubleshooting Tool ===")
    print(f"Control Method: {'ENA/ENB' if USE_ENABLE_PINS else 'Direct PWM'}")
    print(f"PWM Frequency: {PWM_FREQUENCY} Hz")
    print(f"Default Speed: {DEFAULT_SPEED}%")
    print()
    
    # Always show power and wiring info first
    test_power_supply()
    test_wiring_connections()
    
    # Run interactive diagnosis
    interactive_diagnosis()

if __name__ == "__main__":
    main()
