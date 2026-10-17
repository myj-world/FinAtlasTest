from flask import Flask, render_template, jsonify
import os
import requests
from app.routes import bp

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

    return render_template('index.html', greeting=greeting, error=error)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
