# Robotic Vehicle Navigation System

A computer vision-based navigation system for a Raspberry Pi Zero 2W robotic vehicle that can navigate through a 4x5 grid.

## Features

- **Computer Vision**: Real-time grid detection using OpenCV
- **Motor Control**: Precise movement control with PWM speed control
- **Navigation Logic**: Intelligent path planning for grid traversal
- **Modular Design**: Separate components for easy testing and modification

## Hardware Requirements

- Raspberry Pi Zero 2W
- Pi Camera Module
- Motor driver (L298N - see L298N_setup_guide.md for detailed wiring)
- 2 DC motors with wheels (130-type geared motors recommended)
- Push button for start/stop control
- Chassis/frame for the robot
- Power supply (12V battery + LM2596S buck converter recommended)

### Recommended Motor Specifications
- **Type**: 130-type geared DC motors
- **Gear Ratio**: 1:120 (for precise, slow movement)
- **Voltage**: 6V rated
- **Speed**: ~1.33 rpm at wheel (after gearing)
- **Torque**: 0.8 kgf.cm max
- **Current**: 2.8A max stall current

## Software Requirements

- Raspberry Pi OS
- Python 3.7+
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download this repository to your Raspberry Pi
2. Install required packages:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Enable the camera interface:
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > Camera > Enable
   ```

4. Configure GPIO pins in `config.py` to match your motor driver connections

## Hardware Setup

### Motor Connections (L298N Driver)
Connect your L298N driver to the GPIO pins as defined in `config.py`:

- IN1 (Left Motor Forward): GPIO 18
- IN2 (Left Motor Backward): GPIO 23
- IN3 (Right Motor Forward): GPIO 24
- IN4 (Right Motor Backward): GPIO 25

**See `L298N_setup_guide.md` for detailed wiring instructions and troubleshooting.**

### Push Button Setup
- **GPIO Pin**: 16 (configurable)
- **Type**: Momentary push button (normally open)
- **Function**: Start navigation and emergency stop
- **Logic**: Active LOW (pressed = 0V, released = 3.3V)

**See `button_wiring_guide.md` for detailed button wiring instructions.**

### Power Supply Setup (LM2596S Buck Converter)
- **Input**: 12V battery (4-40V range supported)
- **Output**: 6V for motors (adjustable 1.25V-37V)
- **Current**: 3A max, 2A recommended
- **Efficiency**: 85-90% typical

**See `LM2596S_power_guide.md` for detailed power management setup.**

### Grid Setup
Create a 4x5 grid on the floor using:
- **Masking tape** on the floor (recommended for better detection)
- **Grid cell size: 50cm x 50cm** (total grid: 2m x 2.5m)
- Grid cells should be approximately 100x100 pixels in the camera view
- Ensure good lighting and contrast for optimal detection
- Use light-colored floor with dark tape for best results

## Usage

### Running the Main Program
```bash
python3 main_controller.py
```

### Testing Individual Components

#### Test Camera
```bash
python3 test_camera.py
```

#### Test Motors
```bash
python3 test_motors.py
```

#### Test Geared Motors (Recommended)
```bash
python3 test_geared_motors.py
```

#### Calibrate for 50cm Grid
```bash
python3 calibrate_50cm_grid.py
```

#### Monitor Power System
```bash
python3 power_monitor.py
```

#### Test Push Button
```bash
python3 test_button.py
```

## Configuration

Edit `config.py` to adjust:
- Camera settings (resolution, FPS)
- Motor control pins
- Grid dimensions
- Movement speeds and timing
- Debug settings

## Project Structure

```
robotour/
├── main_controller.py      # Main control loop
├── motor_controller.py     # Motor control logic
├── camera_controller.py    # Camera and computer vision
├── navigation_controller.py # Path planning and navigation
├── config.py              # Configuration settings
├── test_camera.py         # Camera testing script
├── test_motors.py         # Motor testing script
├── test_geared_motors.py  # Geared motor testing script
├── calibrate_50cm_grid.py # 50cm grid calibration tool
├── L298N_setup_guide.md   # Detailed L298N wiring guide
├── LM2596S_power_guide.md # LM2596S power management guide
├── button_wiring_guide.md # Push button wiring guide
├── power_monitor.py       # Power monitoring utility
├── button_controller.py   # Push button control
├── test_button.py         # Button testing script
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
└── README.md             # This file
```

## How It Works

1. **Camera Capture**: The Pi camera captures images of the grid
2. **Grid Detection**: Computer vision algorithms detect grid lines and intersections
3. **Position Estimation**: The system determines the robot's current position
4. **Path Planning**: Navigation logic calculates the optimal path to the next target
5. **Motor Control**: Commands are sent to the motors to execute movements
6. **Loop**: The process repeats until all grid cells are visited

## Troubleshooting

### Camera Issues
- Ensure the camera is properly connected and enabled
- Check lighting conditions for grid detection
- Verify camera permissions

### Motor Issues
- Check GPIO pin connections to L298N
- Verify motor driver power supply (6V from LM2596S)
- Check L298N voltage drop (2V typical)
- Test individual motors with the test script
- See `L298N_setup_guide.md` for detailed troubleshooting

### Power Issues
- Check 12V battery voltage and connections
- Verify LM2596S output voltage (should be 6V)
- Monitor current draw (keep under 2A)
- Check for overheating (add heat sink if needed)
- See `LM2596S_power_guide.md` for detailed troubleshooting

### Button Issues
- Check button wiring (GPIO 16 to GND)
- Verify button type (normally open)
- Test with multimeter (should be open when not pressed)
- Check for loose connections
- See `button_wiring_guide.md` for detailed troubleshooting

### Grid Detection Issues
- Ensure good contrast between grid lines and background
- Check grid line thickness and spacing
- Adjust detection parameters in `config.py`

## Safety Notes

- Always test motors individually before running the full program
- Ensure the robot has enough space to move safely
- Monitor the robot during operation
- Use the emergency stop (Ctrl+C) if needed

## Customization

### Different Grid Sizes
Modify `GRID_ROWS` and `GRID_COLS` in `config.py`

### Custom Navigation Patterns
Edit the `initialize_target_cells()` method in `navigation_controller.py`

### Motor Calibration
- **For 50cm grid cells**: Use `calibrate_50cm_grid.py` for precise calibration
- Use `test_geared_motors.py` for general motor testing
- Adjust timing and speed values in `config.py` based on your robot's characteristics
- Key parameters to tune:
  - `MOVE_FORWARD_TIME`: Time to move 50cm (one grid cell)
  - `TURN_TIME`: Time for 90-degree turns
  - `FORWARD_SPEED`: PWM duty cycle for forward movement
  - `TURN_SPEED`: PWM duty cycle for turning
  - `WHEEL_DIAMETER_CM`: Actual wheel diameter for distance calculations

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.
