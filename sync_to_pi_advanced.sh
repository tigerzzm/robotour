#!/bin/bash

# Advanced sync script for Robotour project
# Handles directory persistence and selective file syncing
# Usage: ./sync_to_pi_advanced.sh [file_pattern] [commit_message]

echo "=== Advanced Robotour Sync to Pi ==="

# Check if we're in the right directory
if [ ! -f "main_controller.py" ]; then
    echo "Error: Please run this script from the robotour directory"
    exit 1
fi

# Get parameters
FILE_PATTERN="${1:-*}"  # Default to all files
COMMIT_MSG="${2:-Sync from $(hostname) $(date '+%Y-%m-%d %H:%M:%S')}"

echo "File pattern: $FILE_PATTERN"
echo "Sync message: $COMMIT_MSG"

# Create and setup directory on Pi (persistent)
echo "1. Setting up /robotour directory on Pi..."
ssh robo@tiger.local "
    sudo mkdir -p /robotour
    sudo chown robo:robo /robotour
    echo 'Directory /robotour is ready'
"

if [ $? -ne 0 ]; then
    echo "Error: Failed to setup directory on Pi"
    exit 1
fi

# Sync files based on pattern
echo "2. Syncing files to Pi..."
if [ "$FILE_PATTERN" = "*" ]; then
    # Sync all files
    echo "   Syncing all files..."
    scp *.py *.md *.txt *.sh robo@tiger.local:/robotour/
else
    # Sync specific files
    echo "   Syncing files matching: $FILE_PATTERN"
    scp $FILE_PATTERN robo@tiger.local:/robotour/
fi

if [ $? -ne 0 ]; then
    echo "Error: Failed to sync files to Pi"
    exit 1
fi

# Fix line endings and permissions
echo "3. Fixing line endings and setting permissions..."
ssh robo@tiger.local "
    cd /robotour
    dos2unix *.sh 2>/dev/null || true
    chmod +x *.py *.sh
    echo 'Files processed successfully'
"

if [ $? -eq 0 ]; then
    echo "✅ Successfully synced to Raspberry Pi!"
    echo "Sync completed: $COMMIT_MSG"
    echo ""
    echo "Next steps:"
    echo "1. SSH to your Pi: ssh robo@tiger.local"
    echo "2. Navigate to project: cd /robotour"
    echo "3. Test your changes: python3 test_camera.py"
    echo "4. Run main program: python3 main_controller.py"
else
    echo "❌ Failed to process files on Raspberry Pi"
    exit 1
fi
