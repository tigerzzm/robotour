"""
Motor controller for the robotic vehicle.
Handles movement, turning, and speed control.
"""

import RPi.GPIO as GPIO
import time
from config import *

class MotorController:
    def __init__(self):
        """Initialize the motor controller with GPIO pins for L298N driver."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up motor pins for L298N driver
        self.motor_pins = {
            'left_forward': MOTOR_LEFT_FORWARD,    # IN1
            'left_backward': MOTOR_LEFT_BACKWARD,  # IN2
            'right_forward': MOTOR_RIGHT_FORWARD,  # IN3
            'right_backward': MOTOR_RIGHT_BACKWARD # IN4
        }
        
        # Initialize all motor pins as outputs
        for pin in self.motor_pins.values():
            GPIO.setup(pin, GPIO.OUT)
        
        # Set up PWM for speed control (L298N compatible)
        self.left_pwm_forward = GPIO.PWM(MOTOR_LEFT_FORWARD, PWM_FREQUENCY)
        self.left_pwm_backward = GPIO.PWM(MOTOR_LEFT_BACKWARD, PWM_FREQUENCY)
        self.right_pwm_forward = GPIO.PWM(MOTOR_RIGHT_FORWARD, PWM_FREQUENCY)
        self.right_pwm_backward = GPIO.PWM(MOTOR_RIGHT_BACKWARD, PWM_FREQUENCY)
        
        # Start PWM with 0% duty cycle
        self.left_pwm_forward.start(0)
        self.left_pwm_backward.start(0)
        self.right_pwm_forward.start(0)
        self.right_pwm_backward.start(0)
        
        print("L298N Motor controller initialized")
        print(f"L298N voltage drop: {L298N_VOLTAGE_DROP}V")
        print(f"L298N max current: {L298N_MAX_CURRENT}A per channel")
    
    def stop(self):
        """Stop all motors."""
        self.left_pwm_forward.ChangeDutyCycle(0)
        self.left_pwm_backward.ChangeDutyCycle(0)
        self.right_pwm_forward.ChangeDutyCycle(0)
        self.right_pwm_backward.ChangeDutyCycle(0)
    
    def move_forward(self, speed=DEFAULT_SPEED, duration=None):
        """Move the vehicle forward."""
        self.left_pwm_forward.ChangeDutyCycle(speed)
        self.right_pwm_forward.ChangeDutyCycle(speed)
        self.left_pwm_backward.ChangeDutyCycle(0)
        self.right_pwm_backward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def move_forward_grid_cell(self, speed=FORWARD_SPEED):
        """Move forward by one grid cell distance (optimized for geared motors)."""
        self.move_forward(speed, MOVE_FORWARD_TIME)
    
    def move_backward(self, speed=DEFAULT_SPEED, duration=None):
        """Move the vehicle backward."""
        self.left_pwm_backward.ChangeDutyCycle(speed)
        self.right_pwm_backward.ChangeDutyCycle(speed)
        self.left_pwm_forward.ChangeDutyCycle(0)
        self.right_pwm_forward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def turn_left(self, speed=TURN_SPEED, duration=None):
        """Turn the vehicle left."""
        self.left_pwm_backward.ChangeDutyCycle(speed)
        self.right_pwm_forward.ChangeDutyCycle(speed)
        self.left_pwm_forward.ChangeDutyCycle(0)
        self.right_pwm_backward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def turn_right(self, speed=TURN_SPEED, duration=None):
        """Turn the vehicle right."""
        self.left_pwm_forward.ChangeDutyCycle(speed)
        self.right_pwm_backward.ChangeDutyCycle(speed)
        self.left_pwm_backward.ChangeDutyCycle(0)
        self.right_pwm_forward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def turn_left_90(self, speed=TURN_SPEED):
        """Turn left by 90 degrees (optimized for geared motors)."""
        self.turn_left(speed, TURN_TIME)
    
    def turn_right_90(self, speed=TURN_SPEED):
        """Turn right by 90 degrees (optimized for geared motors)."""
        self.turn_right(speed, TURN_TIME)
    
    def pivot_left(self, speed=TURN_SPEED, duration=None):
        """Pivot left (left wheel backward, right wheel forward)."""
        self.left_pwm_backward.ChangeDutyCycle(speed)
        self.right_pwm_forward.ChangeDutyCycle(speed)
        self.left_pwm_forward.ChangeDutyCycle(0)
        self.right_pwm_backward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def pivot_right(self, speed=TURN_SPEED, duration=None):
        """Pivot right (left wheel forward, right wheel backward)."""
        self.left_pwm_forward.ChangeDutyCycle(speed)
        self.right_pwm_backward.ChangeDutyCycle(speed)
        self.left_pwm_backward.ChangeDutyCycle(0)
        self.right_pwm_forward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def pivot_left_90(self, speed=TURN_SPEED):
        """Pivot left by 90 degrees (optimized for geared motors)."""
        self.pivot_left(speed, PIVOT_TIME)
    
    def pivot_right_90(self, speed=TURN_SPEED):
        """Pivot right by 90 degrees (optimized for geared motors)."""
        self.pivot_right(speed, PIVOT_TIME)
    
    def cleanup(self):
        """Clean up GPIO resources."""
        self.stop()
        self.left_pwm_forward.stop()
        self.left_pwm_backward.stop()
        self.right_pwm_forward.stop()
        self.right_pwm_backward.stop()
        GPIO.cleanup()
        print("Motor controller cleaned up")
