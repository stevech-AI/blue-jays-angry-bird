#!/bin/bash
# Build script for macOS/Linux (creates executable for current OS)

echo "Installing PyInstaller if not already installed..."
pip3 install pyinstaller

echo ""
echo "Building executable..."
pyinstaller angry_birds.spec --clean

echo ""
echo "Build complete! The executable should be in the 'dist' folder."
echo "Note: To create a Windows .exe file, you need to run this on a Windows machine."

