#!/bin/bash

# Sync script to push changes to Raspberry Pi using scp
# Usage: ./sync_to_pi.sh [optional_sync_message]

echo "=== Syncing Robotour to Raspberry Pi ==="

# Check if we're in the right directory
if [ ! -f "main_controller.py" ]; then
    echo "Error: Please run this script from the robotour directory"
    exit 1
fi

# Get sync message
if [ -z "$1" ]; then
    sync_msg="Sync from $(hostname) $(date '+%Y-%m-%d %H:%M:%S')"
else
    sync_msg="Sync: $1"
fi

echo "Sync message: $sync_msg"

# Create directory on Pi if it doesn't exist
echo "1. Creating /robotour directory on Pi..."
ssh robo@tiger.local "sudo mkdir -p /robotour && sudo chown robo:robo /robotour"

if [ $? -ne 0 ]; then
    echo "Error: Failed to create directory on Pi"
    exit 1
fi

# Sync Python files
echo "2. Syncing Python files..."
scp *.py robo@tiger.local:/robotour/

if [ $? -ne 0 ]; then
    echo "Error: Failed to sync Python files"
    exit 1
fi

# Sync configuration and documentation files
echo "3. Syncing config and documentation files..."
scp *.md *.txt *.sh robo@tiger.local:/robotour/

if [ $? -ne 0 ]; then
    echo "Error: Failed to sync config/documentation files"
    exit 1
fi

# Fix line endings and make files executable on Pi
echo "4. Fixing line endings and setting permissions..."
ssh robo@tiger.local "cd /robotour && dos2unix *.sh 2>/dev/null || true && chmod +x *.py *.sh"

if [ $? -eq 0 ]; then
    echo "✅ Successfully synced to Raspberry Pi!"
    echo "Sync completed: $sync_msg"
else
    echo "❌ Failed to set file permissions on Raspberry Pi"
    exit 1
fi

echo ""
echo "Next steps:"
echo "1. SSH to your Pi: ssh robo@tiger.local"
echo "2. Navigate to project: cd /robotour"
echo "3. Test your changes: python3 test_camera.py"
echo "4. Run main program: python3 main_controller.py"
