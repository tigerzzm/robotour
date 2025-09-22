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
        
        # Initialize enable pins if using ENA/ENB method
        if USE_ENABLE_PINS:
            GPIO.setup(ENA_PIN, GPIO.OUT)
            GPIO.setup(ENB_PIN, GPIO.OUT)
            
            # Set up PWM for enable pins (speed control)
            self.ena_pwm = GPIO.PWM(ENA_PIN, PWM_FREQUENCY)
            self.enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
            
            # Start enable PWM with 0% duty cycle
            self.ena_pwm.start(0)
            self.enb_pwm.start(0)
            
            # Set up input pins as digital outputs (direction control)
            self.left_forward_pin = GPIO.PWM(MOTOR_LEFT_FORWARD, PWM_FREQUENCY)
            self.left_backward_pin = GPIO.PWM(MOTOR_LEFT_BACKWARD, PWM_FREQUENCY)
            self.right_forward_pin = GPIO.PWM(MOTOR_RIGHT_FORWARD, PWM_FREQUENCY)
            self.right_backward_pin = GPIO.PWM(MOTOR_RIGHT_BACKWARD, PWM_FREQUENCY)
            
            # Start input PWM with 0% duty cycle
            self.left_forward_pin.start(0)
            self.left_backward_pin.start(0)
            self.right_forward_pin.start(0)
            self.right_backward_pin.start(0)
            
            print("L298N Motor controller initialized (ENA/ENB method)")
        else:
            # Set up PWM for speed control (Direct PWM method)
            self.left_pwm_forward = GPIO.PWM(MOTOR_LEFT_FORWARD, PWM_FREQUENCY)
            self.left_pwm_backward = GPIO.PWM(MOTOR_LEFT_BACKWARD, PWM_FREQUENCY)
            self.right_pwm_forward = GPIO.PWM(MOTOR_RIGHT_FORWARD, PWM_FREQUENCY)
            self.right_pwm_backward = GPIO.PWM(MOTOR_RIGHT_BACKWARD, PWM_FREQUENCY)
            
            # Start PWM with 0% duty cycle
            self.left_pwm_forward.start(0)
            self.left_pwm_backward.start(0)
            self.right_pwm_forward.start(0)
            self.right_pwm_backward.start(0)
            
            print("L298N Motor controller initialized (Direct PWM method)")
        
        print(f"L298N voltage drop: {L298N_VOLTAGE_DROP}V")
        print(f"L298N max current: {L298N_MAX_CURRENT}A per channel")
    
    def stop(self):
        """Stop all motors."""
        if USE_ENABLE_PINS:
            # Stop using ENA/ENB method
            self.ena_pwm.ChangeDutyCycle(0)
            self.enb_pwm.ChangeDutyCycle(0)
            self.left_forward_pin.ChangeDutyCycle(0)
            self.left_backward_pin.ChangeDutyCycle(0)
            self.right_forward_pin.ChangeDutyCycle(0)
            self.right_backward_pin.ChangeDutyCycle(0)
        else:
            # Stop using direct PWM method
            self.left_pwm_forward.ChangeDutyCycle(0)
            self.left_pwm_backward.ChangeDutyCycle(0)
            self.right_pwm_forward.ChangeDutyCycle(0)
            self.right_pwm_backward.ChangeDutyCycle(0)
    
    def move_forward(self, speed=DEFAULT_SPEED, duration=None):
        """Move the vehicle forward."""
        if USE_ENABLE_PINS:
            # ENA/ENB method: Set speed on enable pins, direction on input pins
            self.ena_pwm.ChangeDutyCycle(speed)
            self.enb_pwm.ChangeDutyCycle(speed)
            
            # Left motor direction (with reverse option)
            if REVERSE_LEFT_MOTOR:
                self.left_forward_pin.ChangeDutyCycle(0)   # LOW
                self.left_backward_pin.ChangeDutyCycle(100) # HIGH
            else:
                self.left_forward_pin.ChangeDutyCycle(100)  # HIGH
                self.left_backward_pin.ChangeDutyCycle(0)   # LOW
            
            # Right motor direction (with reverse option)
            if REVERSE_RIGHT_MOTOR:
                self.right_forward_pin.ChangeDutyCycle(0)   # LOW
                self.right_backward_pin.ChangeDutyCycle(100) # HIGH
            else:
                self.right_forward_pin.ChangeDutyCycle(100) # HIGH
                self.right_backward_pin.ChangeDutyCycle(0)  # LOW
        else:
            # Direct PWM method
            if REVERSE_LEFT_MOTOR:
                self.left_pwm_backward.ChangeDutyCycle(speed)
                self.left_pwm_forward.ChangeDutyCycle(0)
            else:
                self.left_pwm_forward.ChangeDutyCycle(speed)
                self.left_pwm_backward.ChangeDutyCycle(0)
            
            if REVERSE_RIGHT_MOTOR:
                self.right_pwm_backward.ChangeDutyCycle(speed)
                self.right_pwm_forward.ChangeDutyCycle(0)
            else:
                self.right_pwm_forward.ChangeDutyCycle(speed)
                self.right_pwm_backward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def move_forward_grid_cell(self, speed=FORWARD_SPEED):
        """Move forward by one grid cell distance (optimized for geared motors)."""
        self.move_forward(speed, MOVE_FORWARD_TIME)
    
    def move_backward(self, speed=DEFAULT_SPEED, duration=None):
        """Move the vehicle backward."""
        if USE_ENABLE_PINS:
            # ENA/ENB method: Set speed on enable pins, direction on input pins
            self.ena_pwm.ChangeDutyCycle(speed)
            self.enb_pwm.ChangeDutyCycle(speed)
            
            # Left motor direction (with reverse option)
            if REVERSE_LEFT_MOTOR:
                self.left_forward_pin.ChangeDutyCycle(100)  # HIGH
                self.left_backward_pin.ChangeDutyCycle(0)   # LOW
            else:
                self.left_forward_pin.ChangeDutyCycle(0)    # LOW
                self.left_backward_pin.ChangeDutyCycle(100) # HIGH
            
            # Right motor direction (with reverse option)
            if REVERSE_RIGHT_MOTOR:
                self.right_forward_pin.ChangeDutyCycle(100) # HIGH
                self.right_backward_pin.ChangeDutyCycle(0)  # LOW
            else:
                self.right_forward_pin.ChangeDutyCycle(0)   # LOW
                self.right_backward_pin.ChangeDutyCycle(100)# HIGH
        else:
            # Direct PWM method
            if REVERSE_LEFT_MOTOR:
                self.left_pwm_forward.ChangeDutyCycle(speed)
                self.left_pwm_backward.ChangeDutyCycle(0)
            else:
                self.left_pwm_backward.ChangeDutyCycle(speed)
                self.left_pwm_forward.ChangeDutyCycle(0)
            
            if REVERSE_RIGHT_MOTOR:
                self.right_pwm_forward.ChangeDutyCycle(speed)
                self.right_pwm_backward.ChangeDutyCycle(0)
            else:
                self.right_pwm_backward.ChangeDutyCycle(speed)
                self.right_pwm_forward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def turn_left(self, speed=TURN_SPEED, duration=None):
        """Turn the vehicle left."""
        if USE_ENABLE_PINS:
            # ENA/ENB method: Left motor backward, right motor forward
            self.ena_pwm.ChangeDutyCycle(speed)
            self.enb_pwm.ChangeDutyCycle(speed)
            
            # Left motor backward (with reverse option)
            if REVERSE_LEFT_MOTOR:
                self.left_forward_pin.ChangeDutyCycle(100)  # HIGH
                self.left_backward_pin.ChangeDutyCycle(0)   # LOW
            else:
                self.left_forward_pin.ChangeDutyCycle(0)     # LOW
                self.left_backward_pin.ChangeDutyCycle(100)  # HIGH
            
            # Right motor forward (with reverse option)
            if REVERSE_RIGHT_MOTOR:
                self.right_forward_pin.ChangeDutyCycle(0)   # LOW
                self.right_backward_pin.ChangeDutyCycle(100) # HIGH
            else:
                self.right_forward_pin.ChangeDutyCycle(100)  # HIGH
                self.right_backward_pin.ChangeDutyCycle(0)   # LOW
        else:
            # Direct PWM method
            if REVERSE_LEFT_MOTOR:
                self.left_pwm_forward.ChangeDutyCycle(speed)
                self.left_pwm_backward.ChangeDutyCycle(0)
            else:
                self.left_pwm_backward.ChangeDutyCycle(speed)
                self.left_pwm_forward.ChangeDutyCycle(0)
            
            if REVERSE_RIGHT_MOTOR:
                self.right_pwm_backward.ChangeDutyCycle(speed)
                self.right_pwm_forward.ChangeDutyCycle(0)
            else:
                self.right_pwm_forward.ChangeDutyCycle(speed)
                self.right_pwm_backward.ChangeDutyCycle(0)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def turn_right(self, speed=TURN_SPEED, duration=None):
        """Turn the vehicle right."""
        if USE_ENABLE_PINS:
            # ENA/ENB method: Left motor forward, right motor backward
            self.ena_pwm.ChangeDutyCycle(speed)
            self.enb_pwm.ChangeDutyCycle(speed)
            
            # Left motor forward (with reverse option)
            if REVERSE_LEFT_MOTOR:
                self.left_forward_pin.ChangeDutyCycle(0)   # LOW
                self.left_backward_pin.ChangeDutyCycle(100) # HIGH
            else:
                self.left_forward_pin.ChangeDutyCycle(100)   # HIGH
                self.left_backward_pin.ChangeDutyCycle(0)    # LOW
            
            # Right motor backward (with reverse option)
            if REVERSE_RIGHT_MOTOR:
                self.right_forward_pin.ChangeDutyCycle(100) # HIGH
                self.right_backward_pin.ChangeDutyCycle(0)  # LOW
            else:
                self.right_forward_pin.ChangeDutyCycle(0)    # LOW
                self.right_backward_pin.ChangeDutyCycle(100) # HIGH
        else:
            # Direct PWM method
            if REVERSE_LEFT_MOTOR:
                self.left_pwm_backward.ChangeDutyCycle(speed)
                self.left_pwm_forward.ChangeDutyCycle(0)
            else:
                self.left_pwm_forward.ChangeDutyCycle(speed)
                self.left_pwm_backward.ChangeDutyCycle(0)
            
            if REVERSE_RIGHT_MOTOR:
                self.right_pwm_forward.ChangeDutyCycle(speed)
                self.right_pwm_backward.ChangeDutyCycle(0)
            else:
                self.right_pwm_backward.ChangeDutyCycle(speed)
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
    
    def set_motor_speeds(self, left_speed, right_speed):
        """Set individual motor speeds (ENA/ENB method only)."""
        if USE_ENABLE_PINS:
            self.ena_pwm.ChangeDutyCycle(left_speed)
            self.enb_pwm.ChangeDutyCycle(right_speed)
        else:
            print("Warning: set_motor_speeds() only works with ENA/ENB method")
    
    def set_motor_directions(self, left_forward, right_forward):
        """Set motor directions (ENA/ENB method only)."""
        if USE_ENABLE_PINS:
            if left_forward:
                self.left_forward_pin.ChangeDutyCycle(100)
                self.left_backward_pin.ChangeDutyCycle(0)
            else:
                self.left_forward_pin.ChangeDutyCycle(0)
                self.left_backward_pin.ChangeDutyCycle(100)
            
            if right_forward:
                self.right_forward_pin.ChangeDutyCycle(100)
                self.right_backward_pin.ChangeDutyCycle(0)
            else:
                self.right_forward_pin.ChangeDutyCycle(0)
                self.right_backward_pin.ChangeDutyCycle(100)
        else:
            print("Warning: set_motor_directions() only works with ENA/ENB method")
    
    def get_control_method(self):
        """Get the current control method."""
        return "ENA/ENB" if USE_ENABLE_PINS else "Direct PWM"
    
    def cleanup(self):
        """Clean up GPIO resources."""
        self.stop()
        
        if USE_ENABLE_PINS:
            # Clean up ENA/ENB method PWM
            self.ena_pwm.stop()
            self.enb_pwm.stop()
            self.left_forward_pin.stop()
            self.left_backward_pin.stop()
            self.right_forward_pin.stop()
            self.right_backward_pin.stop()
        else:
            # Clean up direct PWM method
            self.left_pwm_forward.stop()
            self.left_pwm_backward.stop()
            self.right_pwm_forward.stop()
            self.right_pwm_backward.stop()
        
        GPIO.cleanup()
        print("Motor controller cleaned up")
