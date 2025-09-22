# L298N Motor Driver Setup Guide

This guide provides detailed instructions for connecting and configuring the L298N motor driver with your Raspberry Pi Zero 2W and 130-type geared motors.

## L298N Pin Configuration

### L298N Module Pins
```
L298N Motor Driver Module:
┌─────────────────────────────────┐
│  +12V  GND  +5V  OUT1  OUT2     │
│    │     │    │     │     │     │
│    │     │    │     │     │     │
│  IN1  IN2  IN3  IN4  ENA  ENB   │
└─────────────────────────────────┘
```

### Raspberry Pi GPIO Connections
| L298N Pin | GPIO Pin | Function | Description |
|-----------|----------|----------|-------------|
| IN1 | GPIO 18 | Left Motor Forward | Controls left motor forward direction |
| IN2 | GPIO 15 | Left Motor Backward | Controls left motor backward direction |
| IN3 | GPIO 22 | Right Motor Forward | Controls right motor forward direction |
| IN4 | GPIO 27 | Right Motor Backward | Controls right motor backward direction |
| ENA | GPIO 14 | Left Motor Enable | PWM speed control for left motor (optional) |
| ENB | GPIO 17 | Right Motor Enable | PWM speed control for right motor (optional) |
| +5V | 5V | Power | 5V power from Pi (for L298N logic) |
| GND | GND | Ground | Common ground |
| +12V | 6V Battery | Motor Power | 6V battery for motors |

## Power Supply Setup

### Motor Power (6V Battery)
- **Voltage**: 6V (matches your motor specifications)
- **Current**: At least 3A capacity (2 motors × 2.8A max stall current)
- **Connection**: Connect to L298N +12V terminal (accepts 6V)

### Logic Power (5V from Pi)
- **Source**: Raspberry Pi 5V pin
- **Purpose**: Powers L298N logic circuits
- **Connection**: Connect to L298N +5V terminal

### Ground Connection
- **Critical**: Connect Pi GND to L298N GND
- **Purpose**: Common reference voltage

## Motor Connections

### Left Motor (Motor A)
- **Motor +**: Connect to L298N OUT1
- **Motor -**: Connect to L298N OUT2

### Right Motor (Motor B)
- **Motor +**: Connect to L298N OUT3
- **Motor -**: Connect to L298N OUT4

## L298N Truth Table

| IN1 | IN2 | Left Motor | IN3 | IN4 | Right Motor |
|-----|-----|------------|-----|-----|-------------|
| 0 | 0 | Stop | 0 | 0 | Stop |
| 1 | 0 | Forward | 1 | 0 | Forward |
| 0 | 1 | Backward | 0 | 1 | Backward |
| 1 | 1 | Brake | 1 | 1 | Brake |

## Voltage Considerations

### L298N Voltage Drop
- **Typical drop**: 2V across the driver
- **Your motors**: 6V rated
- **Effective voltage**: ~4V at motors (6V - 2V drop)
- **Impact**: Motors will run slower but with good torque

### PWM Speed Control
- **Method**: Direct PWM on input pins (IN1-IN4)
- **Frequency**: 1000 Hz (configurable)
- **Duty cycle**: 0-100% (0-100% speed)

## Testing Your Setup

### 1. Basic Connection Test
```bash
python3 test_motors.py
```

### 2. L298N Specific Test
```bash
python3 test_geared_motors.py
```

### 3. 50cm Grid Calibration
```bash
python3 calibrate_50cm_grid.py
```

## Troubleshooting

### Common Issues

#### Motors Not Moving
- Check power connections (6V battery to +12V terminal)
- Verify ground connections (Pi GND to L298N GND)
- Check motor connections (OUT1-OUT4)
- Ensure GPIO pins are correctly connected

#### Motors Running Too Slow
- Check battery voltage (should be 6V or higher)
- Verify PWM duty cycle settings
- Consider L298N voltage drop (2V typical)

#### Motors Running Too Fast
- Reduce PWM duty cycle in config.py
- Check for proper PWM frequency (1000 Hz)

#### Inconsistent Movement
- Check for loose connections
- Verify stable power supply
- Ensure proper grounding

### Voltage Measurements
- **Battery voltage**: Should be 6V or higher
- **Motor voltage**: Should be ~4V (6V - 2V drop)
- **Logic voltage**: Should be 5V from Pi

## Safety Notes

1. **Never connect motors directly to Pi GPIO** - Use L298N driver
2. **Always use common ground** between Pi and L298N
3. **Check polarity** of motor connections
4. **Use appropriate fuse** in power supply line
5. **Allow cooling** - L298N can get warm during operation

## Performance Optimization

### For Your 130-type Motors
- **PWM frequency**: 1000 Hz (good balance of efficiency and control)
- **Duty cycle**: 35-50% for forward movement
- **Duty cycle**: 25-35% for turning
- **Enable pins**: Can be used for additional speed control

### Heat Management
- **L298N heat sink**: Ensure proper heat dissipation
- **Duty cycle**: Lower duty cycles reduce heat generation
- **Ventilation**: Allow air flow around L298N module

## Advanced Configuration

### Using Enable Pins (Optional)
If you want to use the ENA/ENB pins for additional speed control:

```python
# In config.py, uncomment and configure:
# ENA_PIN = 12
# ENB_PIN = 13

# In motor_controller.py, add:
# self.ena_pwm = GPIO.PWM(ENA_PIN, PWM_FREQUENCY)
# self.enb_pwm = GPIO.PWM(ENB_PIN, PWM_FREQUENCY)
```

This provides dual-level speed control but is not necessary for basic operation.

## Final Checklist

- [ ] L298N connected to Pi GPIO pins (18, 23, 24, 25)
- [ ] 6V battery connected to L298N +12V terminal
- [ ] Pi 5V connected to L298N +5V terminal
- [ ] Common ground between Pi and L298N
- [ ] Motors connected to OUT1-OUT4 terminals
- [ ] All connections secure and properly insulated
- [ ] Power supply has adequate current capacity (3A+)
- [ ] L298N heat sink properly attached
- [ ] Test basic motor movement before running full program
