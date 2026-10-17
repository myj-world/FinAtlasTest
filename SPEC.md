# FinAtlas — Stack Smoke Test

## Goal

Build a minimal web app to verify that DevMarketplace can work with the repository and that Python, Flask, Pandas, Supabase, and a hosted AI model API work together.

## Requirements

1. **Web page:** A simple page displaying an AI-generated greeting and a status panel.
2. **Python and Flask:** Serve the page and expose a health-check endpoint.
3. **AI integration:** Call a real hosted AI model API from the Python backend. Ask it to generate a short greeting, such as "Hello from FinAtlas AI!" Display the actual response on the page.
4. **CSV viewer:** Use Pandas to load a small sample CSV and display its contents in a browser table.
5. **Supabase:** Connect to a Supabase project and verify connectivity with a minimal read-only query.
6. **Configuration:** Load AI and Supabase credentials from environment variables. Include `.env.example` with placeholder values. Never expose secrets to browser JavaScript or commit real credentials.
7. **Status panel:** Show separate success or failure statuses for Flask, AI API, CSV loading, and Supabase connectivity, with useful error messages.

## Technology Stack

- HTML, CSS, JavaScript
- Python and Flask
- Pandas
- Supabase Python client
- Hosted AI model API
- Environment variables for configuration

## Scope

No authentication, complex styling, or production features. Keep the app minimal and easy to run locally.

## Success Criteria

- The web page opens successfully.
- Flask's health endpoint responds.
- A real AI API call generates the greeting.
- Pandas loads and displays the sample CSV.
- A real read-only query to Supabase succeeds.
- Setup instructions explain dependencies, environment variables, and how to run the app.

## Implementation Flexibility

Keep the implementation minimal. The AI provider, model, and connection-check methods may be adjusted to fit the available environment, while preserving the core tests.
