# UX Research Manager API Documentation

## Overview
The UX Research Manager provides a RESTful API for programmatic access to research insights and personas. All API endpoints are prefixed with `/api/v1/` and return JSON responses.

## Base URL
- **Local Development**: `http://localhost:8000/api/v1/`
- **Production (Heroku)**: `https://your-app-name.herokuapp.com/api/v1/`

## HTTPS/Security

### Local Development
- Local development runs on HTTP (`http://localhost:8000`)
- The Flask secret key is loaded from the `.env` file
- Sessions are used for authentication

### Production Deployment (Heroku)
- **HTTPS is automatically enabled** when you deploy to Heroku
- Heroku handles SSL/TLS certificates and HTTPS termination automatically
- All requests to `http://` are automatically redirected to `https://`
- No additional HTTPS configuration is needed in the Flask app
- Make sure to set `FLASK_SECRET_KEY` as a Config Var in Heroku settings

### Security Best Practices
1. Always use HTTPS in production (handled by Heroku)
2. Keep your Flask secret key secure and never commit it to version control
3. Use environment variables for sensitive configuration
4. All API endpoints require authentication via session cookies

## Authentication
All protected API endpoints require an active user session. Users must log in through the web interface first at `/login` to establish a session. The session cookie is then used to authenticate API requests.

**Authentication Flow:**
1. Log in via POST to `/login` with email and password
2. Receive session cookie
3. Include session cookie in subsequent API requests
4. Session persists until logout or expiration

**Unauthenticated Access:**
- Attempting to access protected endpoints without a valid session returns HTTP 302 (redirect to login)

## API Endpoints

### Health Check

#### `GET /api/v1/status`
Public endpoint to verify API availability.

**Authentication:** Not required

**Response (200 OK):**
```json
{
  "success": true,
  "message": "UX Research Manager API is running",
  "version": "v1"
}
```

---

### Insights

#### `GET /api/v1/insights`
Retrieve all research insights for the authenticated user.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "insights": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Navigation confusion",
      "description": "Users struggled to find the search feature...",
      "persona_id": 2,
      "persona_name": "Sarah the Researcher",
      "journey_stage": "Consideration",
      "timestamp": "2026-03-07T10:30:00",
      "ai_summary": "Users need more prominent search functionality..."
    }
  ]
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "message": "Database connection error"
}
```

---

#### `GET /api/v1/insights/<insight_id>`
Retrieve a single specific insight by ID (owner only).

**Authentication:** Required

**URL Parameters:**
- `insight_id` (integer) - The unique identifier of the insight

**Response (200 OK):**
```json
{
  "success": true,
  "insight": {
    "id": 1,
    "user_id": 1,
    "title": "Navigation confusion",
    "description": "Users struggled to find the search feature...",
    "persona_id": 2,
    "persona_name": "Sarah the Researcher",
    "journey_stage": "Consideration",
    "timestamp": "2026-03-07T10:30:00",
    "ai_summary": "Users need more prominent search functionality..."
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "message": "Insight not found"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "message": "Database query failed"
}
```

---

### Personas

#### `GET /api/v1/personas`
Retrieve all personas for the authenticated user.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "success": true,
  "count": 1,
  "personas": [
    {
      "id": 2,
      "user_id": 1,
      "name": "Sarah the Researcher",
      "description": "Graduate student conducting UX research for thesis...",
      "timestamp": "2026-03-05T14:20:00"
    }
  ]
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "message": "Database connection error"
}
```

---

#### `GET /api/v1/personas/<persona_id>`
Retrieve a single specific persona by ID (owner only).

**Authentication:** Required

**URL Parameters:**
- `persona_id` (integer) - The unique identifier of the persona

**Response (200 OK):**
```json
{
  "success": true,
  "persona": {
    "id": 2,
    "user_id": 1,
    "name": "Sarah the Researcher",
    "description": "Graduate student conducting UX research for thesis...",
    "timestamp": "2026-03-05T14:20:00"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "message": "Persona not found"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "message": "Database query failed"
}
```

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success - Request completed successfully |
| 302 | Redirect - Not authenticated, redirected to login |
| 404 | Not Found - Requested resource does not exist or user does not have access |
| 500 | Internal Server Error - Server encountered an error processing the request |

## Data Ownership & Access Control

All API endpoints enforce data ownership:
- Users can **only** access their own insights and personas
- Attempting to access another user's data returns 404 (not 403) to avoid information disclosure
- All queries automatically filter by `user_id` from the authenticated session

## Example Usage

### Using cURL

**Get all insights:**
```bash
curl -b cookies.txt https://your-app.herokuapp.com/api/v1/insights
```

**Get specific insight:**
```bash
curl -b cookies.txt https://your-app.herokuapp.com/api/v1/insights/15
```

**Get all personas:**
```bash
curl -b cookies.txt https://your-app.herokuapp.com/api/v1/personas
```

### Using Python `requests`

```python
import requests

# Create a session to persist cookies
session = requests.Session()

# Log in
login_data = {
    'email': 'admin@uxrm.local',
    'password': '@dm1n@cc0unt!'
}
session.post('https://your-app.herokuapp.com/login', data=login_data)

# Get all insights
response = session.get('https://your-app.herokuapp.com/api/v1/insights')
insights = response.json()
print(insights)

# Get specific insight
response = session.get('https://your-app.herokuapp.com/api/v1/insights/1')
insight = response.json()
print(insight)

# Get all personas
response = session.get('https://your-app.herokuapp.com/api/v1/personas')
personas = response.json()
print(personas)
```

### Using JavaScript (Browser)

```javascript
// Assuming user is already logged in via the web interface

// Get all insights
fetch('/api/v1/insights')
  .then(response => response.json())
  .then(data => console.log(data));

// Get specific insight
fetch('/api/v1/insights/1')
  .then(response => response.json())
  .then(data => console.log(data));

// Get all personas
fetch('/api/v1/personas')
  .then(response => response.json())
  .then(data => console.log(data));
```

## Heroku Deployment Notes

### Database Configuration
- The app automatically detects Heroku's `DATABASE_URL` environment variable
- PostgreSQL is used in production (configured in `config.py`)
- SQLite is used for local development

### Environment Variables
Set these in Heroku Config Vars:
```bash
heroku config:set FLASK_SECRET_KEY='your-secret-key-here'
heroku config:set MISTRAL_API_KEY='your-mistral-key-here'
```

### HTTPS Setup
No additional configuration needed - Heroku provides HTTPS automatically:
1. Deploy your app to Heroku
2. Access via `https://your-app-name.herokuapp.com`
3. All HTTP requests are automatically upgraded to HTTPS

### Deployment Commands
```bash
# Initialize Heroku app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main

# Run migrations if needed
heroku run python -c "from web_app import app, db; app.app_context().push(); db.create_all()"

# View logs
heroku logs --tail
```

### Production Deployment Checklist (Chunk 10)
- `requirements.txt` has pinned dependency versions.
- `Procfile` exists with `web: gunicorn web_app:app`.
- `runtime.txt` exists and pins a Heroku-supported Python version.
- `.env.example` documents all required environment variables.
- `.gitignore` excludes `.env`, `*.db`, `__pycache__/`, and `.pytest_cache/`.
- `FLASK_SECRET_KEY` is set in Heroku Config Vars (never hard-coded).
- `FLASK_DEBUG` remains `false` in production.
- `DATABASE_URL` is configured by Heroku Postgres add-on.
- App is accessible over HTTPS (`https://...herokuapp.com`).

Quick verify after deploy:
```bash
heroku config
heroku logs --tail
curl -I https://your-app-name.herokuapp.com/api/v1/status
```

## Future Enhancements

Potential additions for future API versions:
- POST/PUT/DELETE endpoints for creating/updating/deleting resources via API
- API key authentication as an alternative to session cookies
- Rate limiting to prevent abuse
- Pagination for large result sets
- Filtering and sorting query parameters
- Webhook support for real-time notifications
- OpenAPI/Swagger documentation

## Troubleshooting

### "Insight not found" when insight exists
- Make sure you're logged in as the correct user
- Verify the insight belongs to your user account
- Check that the insight ID is correct

### Session expired or not authenticated
- Log in again through the web interface
- Make sure cookies are properly stored and sent with requests
- Check that session hasn't timed out

### HTTPS certificate warnings
- In production on Heroku, certificates are managed automatically
- Local development uses HTTP (no certificate needed)
- Never ignore certificate warnings in production

## Support

For issues or questions:
1. Check this documentation
2. Review the application logs
3. Verify authentication and ownership
4. Contact the development team

---

**Version:** 1.1 (Chunk 10 hardening notes added)  
**Last Updated:** March 18, 2026
