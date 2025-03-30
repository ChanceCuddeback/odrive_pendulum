#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if the virtual environment already exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists. Skipping creation."
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation complete. To activate the virtual environment, run:"
echo "source venv/bin/activate"