#!/usr/bin/env python3
"""
Emergency motor stop script.
Run this to immediately stop all motors.
"""

import RPi.GPIO as GPIO
import time
from config import *

def stop_all_motors():
    """Stop all motors immediately."""
    print("Stopping all motors...")
    
    try:
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Define all motor pins
        motor_pins = [
            MOTOR_LEFT_FORWARD,
            MOTOR_LEFT_BACKWARD,
            MOTOR_RIGHT_FORWARD,
            MOTOR_RIGHT_BACKWARD
        ]
        
        # Set all motor pins as outputs and LOW
        for pin in motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
        # Set enable pins LOW if using ENA/ENB
        if USE_ENABLE_PINS:
            GPIO.setup(ENA_PIN, GPIO.OUT)
            GPIO.setup(ENB_PIN, GPIO.OUT)
            GPIO.output(ENA_PIN, GPIO.LOW)
            GPIO.output(ENB_PIN, GPIO.LOW)
        
        print("All motors stopped")
    except Exception as e:
        print(f"Error stopping motors: {e}")
    finally:
        try:
            GPIO.cleanup()
        except:
            pass

if __name__ == "__main__":
    stop_all_motors()
