import os
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create directories for the application structure
def setup_project_structure():
    # Create directories
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    # Create CSS file
    with open("static/css/styles.css", "w") as f:
        f.write("""/* CSS content will be here - copy from styles.css artifact */""")
    
    # Create JS file
    with open("static/js/script.js", "w") as f:
        f.write("""// JS content will be here - copy from script.js artifact""")
    
    # Create HTML template
    with open("templates/index.html", "w") as f:
        f.write("""<!-- HTML content will be here - copy from index.html artifact -->""")

# Setup project structure on import
setup_project_structure()

# Create README.md file with instructions
def create_readme():
    readme_content = """# AI Debate Assistant

A professional web application that helps users prepare for debates by generating counterarguments and detecting logical fallacies.

## Features

- Generate balanced counterarguments for any debate topic
- Analyze arguments for logical fallacies
- Powered by DeepSeek AI through OpenRouter API
- Professional, responsive UI design

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn requests jinja2
   ```
3. Set your OpenRouter API key in `main.py`
4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Project Structure

```
ai-debate-assistant/
├── main.py                  # FastAPI backend server
├── static/                  # Static assets
│   ├── css/
│   │   └── styles.css       # CSS styles
│   └── js/
│       └── script.js        # Frontend JavaScript
└── templates/
    └── index.html           # HTML template
```

## API Endpoints

- `GET /`: Main application page
- `POST /analyze`: Backend API endpoint for debate analysis

## Configuration

The application uses DeepSeek through OpenRouter API. Make sure to replace the placeholder API key with your own in `main.py`.

## License

MIT License
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)

# Create README.md
create_readme()

# Create a script to help users set up the project
def create_setup_script():
    setup_script = """#!/bin/bash

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
"""
    
    with open("setup.sh", "w") as f:
        f.write(setup_script)
    
    # Make the script executable
    os.chmod("setup.sh", 0o755)

# Create setup script
create_setup_script()

# Create a .gitignore file
def create_gitignore():
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# Environment variables
.env
.env.local

# Logs
logs/
*.log

# System Files
.DS_Store
Thumbs.db
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)

# Create .gitignore
create_gitignore()

# Print installation instructions
print("""
========================================
AI Debate Assistant Setup Complete!
========================================

To run the application:

1. Make sure you have the required Python packages installed:
   pip install fastapi uvicorn requests jinja2

2. Update the OpenRouter API key in main.py if needed.

3. Start the application:
   uvicorn main:app --reload

4. Open your browser and navigate to:
   http://localhost:8000

Enjoy using AI Debate Assistant!
""")