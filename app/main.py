from flask import Flask, render_template, jsonify
import os
import requests
import pandas as pd
from app.routes import bp

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/api')


@app.route('/')
def index():
    # AI API handling
    api_key = os.getenv('AI_API_KEY')
    greeting = None
    ai_status = None
    ai_error = None

    if not api_key:
        ai_status = 'API key missing'
    else:
        try:
            # NOTE: This demo currently uses the public Anthropics endpoint from earlier phases.
            # The project plan moves to Gemini in a later phase. For now we attempt a simple POST
            # to demonstrate connectivity; failures are captured and shown to the user.
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
                },
                timeout=8,
            )
            response.raise_for_status()
            data = response.json()
            # Extract greeting from response content (best-effort)
            content = data.get('completion') or data.get('output') or ''
            greeting = content if content else 'Hello from AI!'
            ai_status = 'OK'
        except requests.exceptions.RequestException as e:
            ai_status = 'Error'
            ai_error = f'AI API call failed: {str(e)}'
        except Exception as e:
            ai_status = 'Error'
            ai_error = f'AI processing failed: {str(e)}'

    # CSV loading
    csv_status = None
    csv_error = None
    csv_html = None
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.csv')
        df = pd.read_csv(csv_path)
        csv_html = df.to_html(classes='table table-striped', index=False)
        csv_status = 'Loaded'
    except Exception as e:
        csv_status = 'Error'
        csv_error = f'CSV load failed: {str(e)}'

    # Supabase connectivity check (minimal)
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
            if 200 <= resp.status_code < 500:
                supabase_status = f'Reachable (HTTP {resp.status_code})'
            else:
                supabase_status = f'Unexpected response (HTTP {resp.status_code})'
        except requests.exceptions.RequestException as e:
            supabase_status = 'Error'
            supabase_error = f'Supabase connectivity check failed: {str(e)}'
        except Exception as e:
            supabase_status = 'Error'
            supabase_error = f'Supabase check failed: {str(e)}'

    return render_template(
        'index.html',
        greeting=greeting,
        ai_status=ai_status,
        ai_error=ai_error,
        csv_html=csv_html,
        csv_status=csv_status,
        csv_error=csv_error,
        supabase_status=supabase_status,
        supabase_error=supabase_error,
    )


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
