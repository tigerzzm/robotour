# Motor Direction Fix Guide

## Problem
The right motor rotates backward when it should go forward, and vice versa.

## Solutions

### Option 1: Hardware Fix (Recommended)
**Swap the motor wires on the L298N:**

**Current (Wrong) Connection:**
- Right Motor + → L298N OUT3
- Right Motor - → L298N OUT4

**Correct Connection:**
- Right Motor + → L298N OUT4  
- Right Motor - → L298N OUT3

### Option 2: Software Fix (Already Applied)
The code has been updated to automatically reverse the right motor direction.

**Configuration in `config.py`:**
```python
REVERSE_LEFT_MOTOR = False   # Set to True if left motor rotates backward
REVERSE_RIGHT_MOTOR = True   # Set to True if right motor rotates backward
```

## Testing the Fix

### 1. Run the Direction Fix Test
```bash
python3 test_motor_direction_fix.py
```

### 2. Run Basic Motor Test
```bash
python3 test_motors.py
```

### 3. Run ENA/ENB Test
```bash
python3 test_ena_enb.py
```

## Expected Behavior After Fix

### Forward Movement
- Both motors should rotate forward
- Robot should move straight forward

### Backward Movement  
- Both motors should rotate backward
- Robot should move straight backward

### Left Turn
- Left motor: backward
- Right motor: forward
- Robot should turn left

### Right Turn
- Left motor: forward  
- Right motor: backward
- Robot should turn right

## Troubleshooting

### If movements are still wrong:
1. **Check the config setting**: Verify `REVERSE_RIGHT_MOTOR = True` in `config.py`
2. **Try hardware fix**: Swap the motor wires instead
3. **Test individual motors**: Use the individual motor test to isolate the issue

### If left motor is also wrong:
1. Set `REVERSE_LEFT_MOTOR = True` in `config.py`
2. Or swap the left motor wires on the L298N

### If both motors are wrong:
1. Check your motor connections to the L298N
2. Verify the L298N is getting proper power
3. Check that the GPIO pins are correctly wired

## GPIO Pin Reference
- IN1 (Left Forward): GPIO 18
- IN2 (Left Backward): GPIO 15  
- IN3 (Right Forward): GPIO 22
- IN4 (Right Backward): GPIO 27
- ENA (Left Enable): GPIO 14
- ENB (Right Enable): GPIO 17

## Power Requirements
- L298N +12V: Connect to LM2596S output (6V)
- L298N +5V: Connect to Pi 5V
- L298N GND: Connect to Pi GND
- LM2596S GND: Connect to Pi GND
