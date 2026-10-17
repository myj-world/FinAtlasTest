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
                'https://api.example.com/generate_greeting',
                headers={'Authorization': f'Bearer {api_key}'},
                json={'prompt': 'Generate a friendly greeting'}
            )
            response.raise_for_status()
            data = response.json()
            greeting = data.get('greeting', 'Hello from AI!')
        except Exception as e:
            error = f'AI API call failed: {str(e)}'

    return render_template('index.html', greeting=greeting, error=error)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
