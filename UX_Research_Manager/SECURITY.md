# Security Overview - UX Research Manager (Chunk 8)

This document explains how user data is protected in the application.

## Authentication and Session Security

- Users register with an email and password.
- Passwords are never stored in plaintext.
- Passwords are hashed with Werkzeug's `generate_password_hash` and verified using `check_password_hash`.
- User login creates a server-side session key (`session['user_id']`).
- Logout clears the session state.
- Protected routes require authentication using a `login_required` decorator.

## Data Ownership and Access Control

- Each `Insight` and `Persona` record includes a `user_id` foreign key to `users.id`.
- Queries for listing, viewing, editing, deleting, and AI summarization are filtered by `user_id`.
- Users can only access records they own.
- Attempts to access non-owned records return not found/denied behavior.

## Input Validation

- Registration validates email format and requires passwords with minimum length.
- Registration requires matching password confirmation.
- Login validates credentials before session creation.
- Create and edit flows validate required fields (`title`, `description`, `name`).
- Persona linkage in insights is validated against current user ownership.

## Database Security Design

- `User` table uses unique indexed email values.
- Ownership is enforced via foreign keys in the data model.
- SQLAlchemy ORM is used for query construction to reduce injection risk.

## Operational Recommendations

- Set a strong `FLASK_SECRET_KEY` in environment variables for production.
- Use HTTPS in deployment environments (Heroku/AWS).
- Rotate API keys and keep them in environment variables, not source files.
- Add CSRF protection (Flask-WTF) before production release.
- Add rate limiting on login endpoints for brute-force protection.

## Current Security Scope

Implemented now:
- Registration, login, logout
- Password hashing
- Session-based auth checks
- Per-user ownership enforcement on CRUD and summarize endpoints

Recommended next hardening steps:
- CSRF tokens for all forms
- Password complexity checks and reset flow
- Account lockout / throttling
- Audit logging
