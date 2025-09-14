"""
Configuration file for the robotic vehicle navigation system.
"""

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Grid settings
GRID_ROWS = 4
GRID_COLS = 5
GRID_CELL_SIZE_CM = 50  # centimeters - actual physical size
GRID_CELL_SIZE = 100  # pixels (approximate in camera view)

# Motor control pins (GPIO pins on Raspberry Pi) - L298N Driver
# L298N has 4 input pins: IN1, IN2, IN3, IN4
# IN1, IN2 control Motor A (Left), IN3, IN4 control Motor B (Right)
MOTOR_LEFT_FORWARD = 18   # IN1 on L298N
MOTOR_LEFT_BACKWARD = 23  # IN2 on L298N
MOTOR_RIGHT_FORWARD = 24  # IN3 on L298N
MOTOR_RIGHT_BACKWARD = 25 # IN4 on L298N

# L298N Driver specifications
L298N_VOLTAGE_DROP = 2.0  # Voltage drop across L298N (typical)
L298N_MAX_CURRENT = 2.0   # Maximum current per channel (A)
L298N_ENABLE_PINS = [12, 13]  # ENA, ENB pins (optional PWM control)

# Push button configuration
START_BUTTON_PIN = 16  # GPIO pin for start button (with pull-up resistor)
BUTTON_DEBOUNCE_TIME = 0.1  # seconds to debounce button press

# LM2596S DC Buck Converter specifications
LM2596S_INPUT_VOLTAGE_MIN = 4.0   # Minimum input voltage (V)
LM2596S_INPUT_VOLTAGE_MAX = 40.0  # Maximum input voltage (V)
LM2596S_OUTPUT_VOLTAGE_MIN = 1.25 # Minimum output voltage (V)
LM2596S_OUTPUT_VOLTAGE_MAX = 37.0 # Maximum output voltage (V)
LM2596S_MAX_CURRENT = 3.0         # Maximum output current (A)
LM2596S_RECOMMENDED_CURRENT = 2.0 # Recommended current limit (A)

# Power supply configuration
BATTERY_VOLTAGE = 12.0     # Input battery voltage (V) - 12V recommended
MOTOR_VOLTAGE = 6.0        # Output voltage for motors (V)
PI_VOLTAGE = 5.0           # Voltage for Raspberry Pi (V)

# PWM settings for motor speed control
PWM_FREQUENCY = 1000
DEFAULT_SPEED = 40  # PWM duty cycle (0-100) - reduced for geared motors

# Motor specifications (130-type geared motors, 1:120 ratio)
MOTOR_RATED_VOLTAGE = 6.0  # V
MOTOR_NO_LOAD_SPEED = 160  # rpm at 6V
MOTOR_GEAR_RATIO = 120
MOTOR_OUTPUT_SPEED = MOTOR_NO_LOAD_SPEED / MOTOR_GEAR_RATIO  # ~1.33 rpm at wheel

# Robot physical specifications
WHEEL_DIAMETER_CM = 6.5  # Typical wheel diameter for small robots (adjust as needed)
WHEEL_CIRCUMFERENCE_CM = WHEEL_DIAMETER_CM * 3.14159  # ~20.4 cm
DISTANCE_PER_REVOLUTION_CM = WHEEL_CIRCUMFERENCE_CM

# Navigation settings optimized for 50cm grid cells
TURN_ANGLE = 90  # degrees
MOVE_DISTANCE_CM = GRID_CELL_SIZE_CM  # 50cm per grid cell
TURN_SPEED = 25  # PWM duty cycle for turning (reduced for precision)
FORWARD_SPEED = 35  # PWM duty cycle for forward movement (reduced for control)

# Timing calculations for 50cm grid cells
# At 1.33 rpm (0.022 rps), it takes ~45 seconds for one full wheel revolution
# For 50cm movement: 50cm / 20.4cm per revolution = ~2.45 revolutions
# Time needed: 2.45 revolutions / 0.022 rps = ~111 seconds (too slow!)
# We need to increase speed or use higher PWM duty cycle

# Optimized timing for 50cm grid cells (adjust based on testing)
MOVE_FORWARD_TIME = 8.0  # seconds to move forward 50cm (will need calibration)
TURN_TIME = 2.0  # seconds for 90-degree turn
PIVOT_TIME = 1.5  # seconds for pivot turn

# Computer vision settings
GRID_DETECTION_THRESHOLD = 0.8
LINE_DETECTION_THRESHOLD = 50
MIN_LINE_LENGTH = 50
MAX_LINE_GAP = 10

# Debug settings
DEBUG_MODE = True
SAVE_IMAGES = True
IMAGE_SAVE_PATH = "/tmp/robot_images/"
