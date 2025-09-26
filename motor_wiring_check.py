#!/usr/bin/env python3
"""
Motor wiring diagnostic script.
Checks GPIO pin states and motor control.
"""

import RPi.GPIO as GPIO
import time
from config import *

def check_motor_wiring():
    """Check motor wiring and pin states."""
    print("=== Motor Wiring Diagnostic ===")
    
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Check motor pins
    motor_pins = {
        'Left Forward (IN3)': MOTOR_LEFT_FORWARD,
        'Left Backward (IN4)': MOTOR_LEFT_BACKWARD,
        'Right Forward (IN1)': MOTOR_RIGHT_FORWARD,
        'Right Backward (IN2)': MOTOR_RIGHT_BACKWARD
    }
    
    print("\n1. Setting all motor pins to LOW...")
    for name, pin in motor_pins.items():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        print(f"   {name} (GPIO {pin}): LOW")
    
    # Check enable pins
    if USE_ENABLE_PINS:
        print(f"\n2. Setting enable pins to LOW...")
        GPIO.setup(ENA_PIN, GPIO.OUT)
        GPIO.setup(ENB_PIN, GPIO.OUT)
        GPIO.output(ENA_PIN, GPIO.LOW)
        GPIO.output(ENB_PIN, GPIO.LOW)
        print(f"   ENA (GPIO {ENA_PIN}): LOW")
        print(f"   ENB (GPIO {ENB_PIN}): LOW")
    
    print("\n3. Testing motor control...")
    print("   If right motor is still running, the issue is hardware-level")
    print("   Check these connections:")
    print("   - ENA (GPIO 14) to L298N pin 6")
    print("   - ENB (GPIO 17) to L298N pin 11")
    print("   - All motor pins to L298N inputs")
    print("   - Common ground between Pi and L298N")
    
    # Test individual motor control
    print("\n4. Testing individual motor control...")
    print("   Testing right motor forward...")
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    
    print("   Testing right motor backward...")
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(MOTOR_RIGHT_BACKWARD, GPIO.LOW)
    
    print("   Testing left motor forward...")
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)
    
    print("   Testing left motor backward...")
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(MOTOR_LEFT_BACKWARD, GPIO.LOW)
    
    print("\n5. All motors should now be stopped")
    GPIO.cleanup()

if __name__ == "__main__":
    check_motor_wiring()
