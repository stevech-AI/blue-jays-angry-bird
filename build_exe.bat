@echo off
REM Build script for Windows .exe file
echo Installing PyInstaller if not already installed...
pip install pyinstaller

echo.
echo Building executable...
pyinstaller angry_birds.spec --clean

echo.
echo Build complete! The .exe file should be in the 'dist' folder.
echo You can distribute the entire 'dist' folder or just the .exe file.
pause

