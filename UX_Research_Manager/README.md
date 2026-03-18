# UX Research Manager

UX Research Manager is a Flask app for storing UX insights and personas, with authentication, ownership-based access, AI summaries, and a REST API under `/api/v1`.

## Quick Start (Local)

1. Create/activate virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create local env file from template:
```bash
cp .env.example .env
```

3. Set required values in `.env`:
- `FLASK_SECRET_KEY`
- `MISTRAL_API_KEY`

4. Run the app:
```bash
python web_app.py
```

5. Open:
- App UI: `http://127.0.0.1:8000`
- API health: `http://127.0.0.1:8000/api/v1/status`

## Heroku Deploy (Production)

1. Create app and database:
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
```

2. Set required config vars:
```bash
heroku config:set FLASK_SECRET_KEY='replace-with-strong-secret'
heroku config:set MISTRAL_API_KEY='replace-with-api-key'
heroku config:set FLASK_DEBUG='false'
```

3. Deploy:
```bash
git push heroku main
```

4. Verify:
```bash
heroku logs --tail
curl https://your-app-name.herokuapp.com/api/v1/status
```

## Deployment Notes

- WSGI server is configured via `Procfile`: `web: gunicorn web_app:app`
- Python runtime is pinned in `runtime.txt`
- Secrets are environment-driven (do not hard-code)
- HTTPS is provided by Heroku automatically

## Troubleshooting

- `FLASK_SECRET_KEY is required`:
	- Make sure `.env` exists locally and includes `FLASK_SECRET_KEY`, or set it in shell/Heroku config vars.
- `MISTRAL_API_KEY` errors:
	- Confirm the key is set in `.env` locally or with `heroku config:set MISTRAL_API_KEY=...`.
- App starts but API returns redirect/unauthorized:
	- Log in first to establish a session cookie before calling protected `/api/v1/*` endpoints.
- Database connection issues on Heroku:
	- Verify Postgres add-on is attached and `DATABASE_URL` exists in `heroku config`.
- Static/runtime boot issues after deploy:
	- Confirm `Procfile` is present, `gunicorn` is in `requirements.txt`, and Python version in `runtime.txt` is supported.
