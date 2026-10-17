from flask import Flask, render_template, jsonify
import os
import requests
from app.routes import bp
import pandas as pd
from flask import send_from_directory

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/api')

@app.route('/')
def index():
    api_key = os.getenv('AI_API_KEY')
    greeting = None
    error = None
    if not api_key:
        error = 'API key missing'
    else:
        try:
            # Call the AI model API to get a greeting
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': api_key,
                    'Content-Type': 'application/json',
                    'anthropic-version': '2023-06-01'
                },
                json={
                    'model': 'claude-sonnet-4-6',
                    'max_tokens_to_sample': 1000,
                    'messages': [{ 'role': 'user', 'content': 'Generate a friendly greeting' }]
                }
            )
            response.raise_for_status()
            data = response.json()
            # Extract greeting from response content
            content = data.get('completion', '')
            greeting = content if content else 'Hello from AI!'
        except Exception as e:
            error = f'AI API call failed: {str(e)}'

    # Attempt to load sample CSV
    csv_error = None
    csv_html = None
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.csv')
        df = pd.read_csv(csv_path)
        csv_html = df.to_html(classes='table', index=False)
    except Exception as e:
        csv_error = f'CSV load failed: {str(e)}'

    # Check Supabase connectivity
    supabase_status = None
    supabase_error = None
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    if not supabase_url or not supabase_key:
        supabase_status = 'Missing SUPABASE_URL or SUPABASE_ANON_KEY'
    else:
        try:
            # Minimal connectivity check: call the Supabase REST root to verify the service is reachable
            resp = requests.get(f"{supabase_url}/rest/v1/", headers={
                'apikey': supabase_key,
                'Authorization': f'Bearer {supabase_key}'
            }, timeout=5)
            # If we get any HTTP response it means we reached the Supabase REST endpoint.
            if resp.status_code >= 200 and resp.status_code < 500:
                supabase_status = f'Reachable (HTTP {resp.status_code})'
            else:
                supabase_status = f'Unexpected response (HTTP {resp.status_code})'
        except Exception as e:
            supabase_error = f'Supabase connectivity check failed: {str(e)}'

    return render_template('index.html', greeting=greeting, error=error, csv_html=csv_html, csv_error=csv_error, supabase_status=supabase_status, supabase_error=supabase_error)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
