# BloomBot 🌱

A Flask-based plant care web app with user registration, login, and a dashboard for tracking plant health and watering schedules.

## Features
- User registration and login (session-based authentication)
- Dashboard view summarizing plant health stats
- Dedicated pages for plant management, health tracking, watering reminders, and watering schedules
- Frontend built with HTML, CSS, and JavaScript

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Configured for Heroku-style deployment (Procfile included)

## Project Structure
```
BloomBot/
├── app.py            # Flask app and routes
├── static/           # CSS/JS assets
├── templates/        # HTML templates
├── Procfile          # Deployment config
└── requirements.txt  # Python dependencies
```

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
App runs at `http://localhost:5000`

## Status
Personal learning project — actively being improved. Current focus areas: moving from in-memory user storage to a persistent database, and adding password hashing.

## Author
Madhumitha Arumugam — [GitHub](https://github.com/madhu250205)
