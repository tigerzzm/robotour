#!/bin/bash

# Sync script to push changes from Mac to Raspberry Pi
# Usage: ./sync_to_pi.sh [commit_message]

echo "=== Syncing Robotour to Raspberry Pi ==="

# Check if we're in the right directory
if [ ! -f "main_controller.py" ]; then
    echo "Error: Please run this script from the robotour directory"
    exit 1
fi

# Get commit message
if [ -z "$1" ]; then
    echo "Enter commit message (or press Enter for default):"
    read -r commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Update from Mac $(date '+%Y-%m-%d %H:%M:%S')"
    fi
else
    commit_msg="$1"
fi

echo "Commit message: $commit_msg"

# Commit and push to GitHub
echo "1. Committing changes to git..."
git add .
git commit -m "$commit_msg"
git push origin main

if [ $? -ne 0 ]; then
    echo "Error: Failed to push to GitHub"
    exit 1
fi

echo "2. Pushing to Raspberry Pi..."
ssh robo@tiger.local "cd /robotour && git pull origin main"

if [ $? -eq 0 ]; then
    echo "✅ Successfully synced to Raspberry Pi!"
    echo "You can now SSH to your Pi and run the updated code."
else
    echo "❌ Failed to sync to Raspberry Pi"
    exit 1
fi

echo ""
echo "Next steps:"
echo "1. SSH to your Pi: ssh robo@tiger.local"
echo "2. Navigate to project: cd /robotour"
echo "3. Test your changes: python3 test_camera.py"
echo "4. Run main program: python3 main_controller.py"
