# Sentiment Analysis Dashboard 📊

A full-stack Flask web app that analyzes the sentiment of user-submitted text and stores results for review on a dashboard.

## Features
- Real-time text input and sentiment scoring
- Results persisted to a SQLite database
- Dashboard interface to view past sentiment results

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML

## Project Structure
```
Sentiment-Analysis-Dashboard/
├── app.py / main.py     # Flask app and sentiment logic
├── templates/           # HTML templates
├── sentiment.db         # SQLite database
└── requirements.txt     # Python dependencies
```

## Run Locally
```bash
pip install -r requirements.txt
python main.py
```
App runs at `http://localhost:5000`

## Status
Personal project built to practice end-to-end Flask development — from data validation to database persistence to frontend display.

## Author
Madhumitha Arumugam — [GitHub](https://github.com/madhu250205)
