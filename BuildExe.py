import PyInstaller.__main__
import shutil
import os

# Build the executable using PyInstaller
scriptName = input("Name of the script to build (without .py): ")
PyInstaller.__main__.run([
    f'{scriptName}.py',
    '--noconfirm',
])

# Copy the .env file to the dist folder
shutil.copy('.env', os.path.join('dist', scriptName, '.env'))