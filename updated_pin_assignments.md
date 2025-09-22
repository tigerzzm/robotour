# Updated GPIO Pin Assignments

## 🔌 **New Pin Configuration**

Based on your specifications, the GPIO pin assignments have been updated as follows:

### **L298N Motor Driver Connections:**

| L298N Pin | Raspberry Pi GPIO | Physical Pin | Function |
|-----------|-------------------|--------------|----------|
| **ENA** | **GPIO 14** | Pin 8 | Left Motor Speed Control (PWM) |
| **IN1** | **GPIO 18** | Pin 12 | Left Motor Forward |
| **IN2** | **GPIO 15** | Pin 10 | Left Motor Backward |
| **ENB** | **GPIO 17** | Pin 11 | Right Motor Speed Control (PWM) |
| **IN3** | **GPIO 22** | Pin 15 | Right Motor Forward |
| **IN4** | **GPIO 27** | Pin 13 | Right Motor Backward |

### **Power Connections:**
| Component | Connection | Voltage |
|-----------|------------|---------|
| L298N VCC | Pi 5V | 5V (Pin 2) |
| L298N GND | Pi GND | GND (Pin 6) |
| L298N VIN | LM2596S OUT+ | 6V (adjusted) |
| LM2596S IN+ | Battery + | 12V |
| LM2596S IN- | Battery - | GND |

### **Push Button:**
| Component | Connection | Function |
|-----------|------------|----------|
| Button | GPIO 16 | Start/Stop Control |

## 📋 **Updated Files:**

1. **`config.py`** - Updated all GPIO pin assignments
2. **`ena_enb_wiring_guide.md`** - Updated wiring diagram
3. **`L298N_setup_guide.md`** - Updated pin reference table
4. **`README.md`** - Updated motor connections section

## ✅ **Configuration Summary:**

```python
# Motor control pins (L298N driver)
MOTOR_LEFT_FORWARD = 18   # IN1 on L298N
MOTOR_LEFT_BACKWARD = 15  # IN2 on L298N
MOTOR_RIGHT_FORWARD = 22  # IN3 on L298N
MOTOR_RIGHT_BACKWARD = 27 # IN4 on L298N

# L298N Enable pins for dual-level PWM control
ENA_PIN = 14  # GPIO pin for ENA (Left Motor Enable)
ENB_PIN = 17  # GPIO pin for ENB (Right Motor Enable)
USE_ENABLE_PINS = True  # Set to True to use ENA/ENB, False for direct PWM

# Push button configuration
START_BUTTON_PIN = 16  # GPIO pin for start button
```

## 🧪 **Testing:**

To test the new pin configuration:

```bash
python3 test_ena_enb.py
```

This will verify that all pins are working correctly with the new assignments.

## ⚠️ **Important Notes:**

1. **Double-check wiring** - Ensure all connections match the new pin assignments
2. **Test before autonomous mode** - Run the test scripts to verify functionality
3. **Power considerations** - Make sure your power supply can handle the motor requirements
4. **GPIO conflicts** - These pins should not conflict with other Pi functions

## 🔧 **Troubleshooting:**

If motors don't respond:
1. Check all wiring connections
2. Verify power supply voltage (6V for motors, 5V for L298N logic)
3. Test individual pins with `test_ena_enb.py`
4. Check for loose connections or damaged wires

The system is now configured with your specified pin assignments! 🎯
