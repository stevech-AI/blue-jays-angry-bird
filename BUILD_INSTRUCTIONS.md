# Building Executable for Distribution

This guide explains how to create an executable file from the Angry Birds Python game.

## Prerequisites

- Python 3.9 or higher
- All dependencies installed (pygame, pymunk)
- PyInstaller (will be installed automatically by the build scripts)

## For Windows Users (Creates .exe file)

1. Open Command Prompt or PowerShell in the project directory
2. Run the build script:
   ```
   build_exe.bat
   ```
   
   Or manually:
   ```
   pip install pyinstaller
   pyinstaller angry_birds.spec --clean
   ```

3. The `.exe` file will be created in the `dist` folder
4. You can distribute the entire `dist` folder or just the `.exe` file

## For macOS/Linux Users

**Important:** PyInstaller creates executables for the operating system it runs on. To create a Windows `.exe`, you need to build on a Windows machine.

### Option 1: Build on Windows
- Use a Windows computer or virtual machine
- Follow the Windows instructions above

### Option 2: Build for your current OS (macOS/Linux)
1. Run:
   ```bash
   chmod +x build_exe.sh
   ./build_exe.sh
   ```
   
2. This will create an executable for your current OS (not Windows)

### Option 3: Use GitHub Actions (for Windows .exe from macOS)
You can set up GitHub Actions to automatically build Windows executables. This requires setting up a GitHub Actions workflow file.

## Distribution

### What to Include:
- The executable file (`.exe` on Windows)
- **OR** the entire `dist` folder if PyInstaller created additional files

### Testing Before Distribution:
1. Test the executable on a clean machine (without Python installed)
2. Make sure all images and sounds are included
3. Verify the game runs without errors

## Troubleshooting

### Missing Files Error:
If the game can't find resource files, they might not be bundled correctly. Check the `angry_birds.spec` file's `datas` section.

### Large File Size:
The executable will be large (50-100MB) because it includes Python and all dependencies. This is normal.

### Antivirus Warnings:
Some antivirus software may flag PyInstaller executables as suspicious. This is a false positive. You may need to:
- Sign the executable with a code signing certificate
- Submit it to antivirus vendors for whitelisting

## Customization

### Adding an Icon:
1. Create or obtain an `.ico` file for Windows (or `.icns` for macOS)
2. Update the `icon=None` line in `angry_birds.spec`:
   ```python
   icon='path/to/your/icon.ico',
   ```

### Console Output:
To show console output (for debugging), change in `angry_birds.spec`:
```python
console=True,  # Shows console window
```

