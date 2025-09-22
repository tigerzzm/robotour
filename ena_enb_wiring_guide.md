# ENA/ENB Wiring Guide for L298N Motor Driver

## 🔌 **Complete Wiring Diagram with ENA/ENB**

### **Raspberry Pi Zero 2W to L298N Connections:**

| Raspberry Pi Pin | L298N Pin | Function | Description |
|------------------|-----------|----------|-------------|
| GPIO 14 (Pin 8)  | ENA | Enable A | Left motor speed control (PWM) |
| GPIO 17 (Pin 11) | ENB | Enable B | Right motor speed control (PWM) |
| GPIO 18 (Pin 12) | IN1 | Input 1 | Left motor direction control |
| GPIO 15 (Pin 10) | IN2 | Input 2 | Left motor direction control |
| GPIO 22 (Pin 15) | IN3 | Input 3 | Right motor direction control |
| GPIO 27 (Pin 13) | IN4 | Input 4 | Right motor direction control |
| 5V (Pin 2) | VCC | Power | L298N logic power |
| GND (Pin 6) | GND | Ground | Common ground |

### **L298N to Motors:**

| L298N Pin | Motor Connection | Function |
|-----------|------------------|----------|
| OUT1 | Left Motor + | Left motor positive |
| OUT2 | Left Motor - | Left motor negative |
| OUT3 | Right Motor + | Right motor positive |
| OUT4 | Right Motor - | Right motor negative |

### **Power Supply (LM2596S Buck Converter):**

| Component | Connection | Voltage |
|-----------|------------|---------|
| Battery + | LM2596S IN+ | 12V |
| Battery - | LM2596S IN- | GND |
| LM2596S OUT+ | L298N VIN | 6V (adjusted) |
| LM2596S OUT- | L298N GND | GND |

## ⚡ **ENA/ENB Control Methods**

### **Method 1: ENA/ENB PWM (Current Implementation)**
```
ENA (GPIO 12) ← PWM for Left Motor Speed
ENB (GPIO 13) ← PWM for Right Motor Speed
IN1 ← Digital HIGH/LOW for Left Forward
IN2 ← Digital HIGH/LOW for Left Backward
IN3 ← Digital HIGH/LOW for Right Forward
IN4 ← Digital HIGH/LOW for Right Backward
```

**Advantages:**
- Independent speed control for each motor
- Better for differential steering
- More precise control
- Can implement speed ramping

**Code Example:**
```python
# Set different speeds for each motor
motor.set_motor_speeds(50, 35)  # Left 50%, Right 35%
motor.set_motor_directions(True, True)  # Both forward
```

### **Method 2: Direct PWM (Alternative)**
```
IN1 ← PWM for Left Motor Forward
IN2 ← PWM for Left Motor Backward
IN3 ← PWM for Right Motor Forward
IN4 ← PWM for Right Motor Backward
ENA ← Not connected (or 5V)
ENB ← Not connected (or 5V)
```

**Advantages:**
- Simpler implementation
- Fewer GPIO pins needed
- Direct control of each direction

## 🎛️ **Control Logic**

### **ENA/ENB Method:**
- **ENA/ENB**: Control motor speed (0-100% PWM)
- **IN1-IN4**: Control motor direction (HIGH/LOW)

### **Motor Direction Control:**
| IN1 | IN2 | Left Motor | IN3 | IN4 | Right Motor |
|-----|-----|------------|-----|-----|-------------|
| HIGH | LOW | Forward | HIGH | LOW | Forward |
| LOW | HIGH | Backward | LOW | HIGH | Backward |
| HIGH | HIGH | Brake | HIGH | HIGH | Brake |
| LOW | LOW | Free | LOW | LOW | Free |

## 🔧 **Configuration**

### **Enable ENA/ENB Method:**
```python
# In config.py
USE_ENABLE_PINS = True
ENA_PIN = 14
ENB_PIN = 17
```

### **Enable Direct PWM Method:**
```python
# In config.py
USE_ENABLE_PINS = False
```

## 🧪 **Testing**

### **Test ENA/ENB Functionality:**
```bash
python3 test_ena_enb.py
```

### **Test Individual Motor Control:**
```python
from motor_controller import MotorController

motor = MotorController()

# Test left motor only
motor.set_motor_speeds(50, 0)  # Left 50%, Right 0%
motor.set_motor_directions(True, True)  # Both forward
time.sleep(2)

# Test right motor only
motor.set_motor_speeds(0, 50)  # Left 0%, Right 50%
time.sleep(2)

motor.cleanup()
```

## ⚠️ **Important Notes**

1. **ENA/ENB must be connected** when using ENA/ENB method
2. **ENA/ENB can be left floating** when using direct PWM method (they default to HIGH)
3. **Both methods are compatible** with the same L298N hardware
4. **Switch methods** by changing `USE_ENABLE_PINS` in config.py
5. **Test thoroughly** before using in autonomous mode

## 🔍 **Troubleshooting**

### **Motors not moving:**
- Check ENA/ENB connections
- Verify PWM frequency settings
- Check power supply voltage

### **Motors running at full speed:**
- ENA/ENB might be floating (connect to 5V or use PWM)
- Check PWM duty cycle values

### **Uneven motor speeds:**
- Use `set_motor_speeds()` to calibrate individual motors
- Check for mechanical binding
- Verify motor specifications match

## 📊 **Performance Comparison**

| Feature | ENA/ENB Method | Direct PWM Method |
|---------|----------------|-------------------|
| GPIO Pins Used | 6 | 4 |
| Speed Control | Independent per motor | Per direction |
| Direction Control | Digital | PWM |
| Implementation | More complex | Simpler |
| Precision | Higher | Good |
| Differential Steering | Excellent | Good |

## 🚀 **Advanced Features**

### **Speed Ramping:**
```python
# Gradually increase speed
for speed in range(0, 51, 5):
    motor.set_motor_speeds(speed, speed)
    time.sleep(0.1)
```

### **Differential Steering:**
```python
# Turn by varying motor speeds
motor.set_motor_speeds(40, 60)  # Right motor faster
motor.set_motor_directions(True, True)  # Both forward
```

### **Precise Turns:**
```python
# Sharp turn with one motor stopped
motor.set_motor_speeds(0, 50)  # Only right motor
motor.set_motor_directions(True, True)  # Both forward
```

This implementation gives you maximum flexibility and control over your robotic vehicle! 🎯
