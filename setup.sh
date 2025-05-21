#!/bin/bash

# Setup script for AI Debate Assistant

echo "Setting up AI Debate Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install fastapi uvicorn requests jinja2

# Prompt for OpenRouter API key
echo ""
echo "To use this application, you need an OpenRouter API key."
echo "You can get one at https://openrouter.ai/"
echo ""
read -p "Enter your OpenRouter API key (or press Enter to skip): " api_key

if [ ! -z "$api_key" ]; then
    # Replace API key in main.py
    echo "Updating API key in main.py..."
    sed -i "s/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/$api_key/g" main.py
else
    echo "Skipping API key update. You'll need to manually update it in main.py."
fi

echo ""
echo "Setup complete! To start the application, run:"
echo "source venv/bin/activate  # If not already activated"
echo "uvicorn main:app --reload"

echo ""
echo "Then open http://localhost:8000 in your browser."
