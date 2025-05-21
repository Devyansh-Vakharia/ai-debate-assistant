# AI Debate Assistant

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
