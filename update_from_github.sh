#!/bin/bash

# Update script for Raspberry Pi to pull latest changes from GitHub
# Usage: ./update_from_github.sh

echo "=== Updating Robotour from GitHub ==="

# Check if we're in the right directory
if [ ! -f "main_controller.py" ]; then
    echo "Error: Please run this script from the robotour directory"
    exit 1
fi

# Check git status
echo "1. Checking current status..."
git status

echo ""
echo "2. Pulling latest changes from GitHub..."
git pull origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully updated from GitHub!"
    echo ""
    echo "Recent changes:"
    git log --oneline -5
    echo ""
    echo "You can now run your updated code:"
    echo "  python3 test_camera.py"
    echo "  python3 main_controller.py"
else
    echo "❌ Failed to update from GitHub"
    echo "Check your internet connection and try again"
    exit 1
fi
