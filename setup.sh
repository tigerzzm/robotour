#!/bin/bash

# Setup script for the robotic vehicle navigation system
# Run this script to install dependencies and configure the system

echo "=== Robotic Vehicle Navigation System Setup ==="

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    echo "Warning: This script is designed for Raspberry Pi. Some features may not work on other systems."
fi

# Update package list
echo "Updating package list..."
sudo apt update

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Enable camera interface
echo "Enabling camera interface..."
sudo raspi-config nonint do_camera 0

# Create image save directory
echo "Creating image save directory..."
mkdir -p /tmp/robot_images

# Set up GPIO permissions
echo "Setting up GPIO permissions..."
sudo usermod -a -G gpio $USER

# Make scripts executable
echo "Making scripts executable..."
chmod +x *.py

echo "Setup completed!"
echo ""
echo "Next steps:"
echo "1. Reboot your Raspberry Pi: sudo reboot"
echo "2. Connect your motors to the GPIO pins as specified in config.py"
echo "3. Set up your 4x5 grid on the floor"
echo "4. Test individual components:"
echo "   - python3 test_camera.py"
echo "   - python3 test_motors.py"
echo "5. Run the main program: python3 main_controller.py"
echo ""
echo "For detailed instructions, see README.md"
