# FinAtlas Flask App

This is the initial phase of the FinAtlas project, a minimal Flask web app.

## Phase 1: Basic Flask Setup and Health Check Endpoint

- A simple Flask backend is set up.
- A health-check endpoint at `/health` returns status "healthy".

## Running the App

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask app:
   ```
   python app/main.py
   ```

3. Visit `http://localhost:5000/health` to see the health status.

## Environment Variables

- Use the `.env.example` file as a template.
- Add actual API keys and credentials in the Secrets panel.

## Next Steps

- Integrate AI model API to generate greetings.
- Load and display CSV data.
- Connect to Supabase and verify connectivity.
- Implement status panel on the frontend.
