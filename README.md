# FinAtlas Flask App

This is the FinAtlas project, a minimal Flask web app that demonstrates AI model integration, CSV loading, and Supabase connectivity checks.

## What changed in this phase
- Added Supabase connectivity check (minimal read-only REST ping) from the backend.
- Display success/failure statuses for Flask, AI API, CSV loading, and Supabase connectivity on the home page.
- Added pyproject.toml to ensure setuptools and wheel are installed first (fixes pandas on Python 3.14).
- Added a Procfile with a gunicorn command for hosting platforms.

## Running the App
1. Install dependencies:
   pip install -r requirements.txt

2. Run the Flask app for development:
   python app/main.py

3. Or run with gunicorn (recommended for hosting):
   gunicorn app.main:app --bind 0.0.0.0:$PORT --workers 2

4. Visit http://localhost:5000/ to see the greeting, CSV, and status panel.

## Environment Variables
See .env.example. Do NOT commit real secrets.

- AI_API_KEY: API key for the AI model (calls Anthropics API in this demo)
- SUPABASE_URL: Your Supabase project URL
- SUPABASE_ANON_KEY: Your Supabase anon key (used for read-only checks)

If AI_API_KEY is missing the web page will show "API key missing" and the status panel will report it.
