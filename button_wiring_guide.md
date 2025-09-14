# Push Button Wiring Guide

This guide shows how to wire a push button to your Raspberry Pi Zero 2W for starting the robotic vehicle.

## Button Specifications

- **GPIO Pin**: 16 (configurable in `config.py`)
- **Type**: Momentary push button (normally open)
- **Logic**: Active LOW (pressed = 0V, released = 3.3V)
- **Pull-up**: Internal pull-up resistor enabled

## Wiring Diagram

```
Push Button Wiring:
┌─────────────────┐
│   Push Button   │
│                 │
│  ┌─────────┐    │
│  │    ●    │    │  ← Button (normally open)
│  └─────────┘    │
│                 │
└─────────────────┘
        │
        │
        ▼
┌─────────────────┐
│  Raspberry Pi   │
│                 │
│  GPIO 16 ───────┼─── To one side of button
│                 │
│  GND ───────────┼─── To other side of button
│                 │
└─────────────────┘
```

## Detailed Wiring Instructions

### Step 1: Identify GPIO Pin 16
- **Physical Pin**: Pin 36 on the 40-pin header
- **GPIO Number**: 16 (BCM numbering)
- **Function**: Input with internal pull-up resistor

### Step 2: Connect the Button
1. **One side of button** → **GPIO 16** (Pin 36)
2. **Other side of button** → **GND** (Pin 6, 9, 14, 20, 25, 30, 34, or 39)

### Step 3: Verify Connections
- Button **not pressed**: GPIO 16 reads HIGH (3.3V)
- Button **pressed**: GPIO 16 reads LOW (0V)

## Button Types

### Recommended: Momentary Push Button
- **Type**: Normally Open (NO)
- **Action**: Press to close circuit
- **Release**: Automatically opens circuit
- **Example**: Tactile switch, arcade button

### Alternative: Toggle Switch
- **Type**: On/Off switch
- **Action**: Toggle to change state
- **Note**: Requires different code logic

## Safety Features

### Debouncing
- **Time**: 0.1 seconds (configurable)
- **Purpose**: Prevents multiple triggers from single press
- **Implementation**: Software-based in `button_controller.py`

### Emergency Stop
- **Action**: Hold button for 2+ seconds
- **Function**: Immediately stops robot navigation
- **Safety**: Prevents runaway robot

## Testing Your Button

### 1. Basic Test
```bash
cd /robotour
python3 test_button.py
```

### 2. Choose Test Option 1
- Press and release button
- Should see "Button pressed!" and "Button released!" messages

### 3. Test Emergency Stop
- Hold button for 2+ seconds
- Should see "Emergency stop activated!" message

## Troubleshooting

### Button Not Working
1. **Check wiring**: Ensure button connects GPIO 16 to GND
2. **Check button**: Test with multimeter (should be open when not pressed)
3. **Check GPIO**: Verify pin 36 is GPIO 16
4. **Check pull-up**: Internal pull-up should be enabled

### False Triggers
1. **Loose connections**: Secure all wiring
2. **Noisy signal**: Add external pull-up resistor (10kΩ)
3. **Button bounce**: Increase debounce time in config

### Button Always Pressed
1. **Wiring short**: Check for accidental short to GND
2. **Faulty button**: Test button with multimeter
3. **Wrong pin**: Verify GPIO 16 is correct

## Advanced Configuration

### Change Button Pin
Edit `config.py`:
```python
START_BUTTON_PIN = 20  # Change to different GPIO pin
```

### Adjust Debounce Time
Edit `config.py`:
```python
BUTTON_DEBOUNCE_TIME = 0.2  # Increase for noisy buttons
```

### Add External Pull-up Resistor
If internal pull-up is insufficient:
```
3.3V ──[10kΩ]── GPIO 16 ── Button ── GND
```

## Button Placement

### Recommended Locations
1. **Top of robot**: Easy access during operation
2. **Side panel**: Protected from accidental presses
3. **Back of robot**: Emergency access only

### Mounting Considerations
- **Secure mounting**: Prevent button from moving
- **Accessible**: Easy to press when needed
- **Protected**: Shield from dust and moisture
- **Visible**: Clear indication of button location

## Integration with Robot

### Startup Sequence
1. **Pi boots**: Robot initializes all systems
2. **Button wait**: Robot waits for button press
3. **Navigation starts**: Robot begins grid traversal
4. **Emergency stop**: Button can stop robot anytime

### Status Indicators
- **LED indicators**: Show button state (optional)
- **Console output**: Display button status
- **Audio feedback**: Beep on button press (optional)

## Safety Notes

1. **Always test button** before running robot
2. **Keep button accessible** during operation
3. **Use emergency stop** if robot behaves unexpectedly
4. **Check button regularly** for proper operation
5. **Have backup stop method** (Ctrl+C via SSH)

## Example Button Types

### Tactile Switch (Recommended)
- **Size**: 6x6mm or 12x12mm
- **Force**: 100-300g activation force
- **Life**: 1,000,000+ cycles
- **Cost**: $0.10-$0.50

### Arcade Button
- **Size**: 30mm diameter
- **Force**: Higher activation force
- **Visibility**: Large, easy to see
- **Cost**: $2-$5

### Panel Mount Button
- **Size**: 16mm or 22mm diameter
- **Mounting**: Panel mount with nut
- **Durability**: Industrial grade
- **Cost**: $3-$10
