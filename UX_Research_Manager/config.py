"""
UX Research Manager - Database Configuration (Chunk 6)

Database setup and configuration for SQLAlchemy.
Supports SQLite (local) and PostgreSQL (Heroku/AWS).
"""

import os
from pathlib import Path


def load_local_env() -> None:
    """Load key=value pairs from local .env into process environment."""
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        # Do not overwrite explicitly provided environment variables.
        if key and key not in os.environ:
            os.environ[key] = value


load_local_env()


def get_database_url():
    """
    Get database URL from environment or use SQLite default.
    
    Priority:
    1. DATABASE_URL environment variable (Heroku PostgreSQL)
    2. Local SQLite database
    
    For Heroku: DATABASE_URL is automatically set when PostgreSQL add-on is installed
    For AWS: Set DATABASE_URL to your RDS PostgreSQL connection string
    """
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Heroku PostgreSQL URLs start with postgres://
        # SQLAlchemy 1.4+ requires postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    # Local SQLite database
    db_dir = Path(__file__).parent / 'data'
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / 'project.db'
    return f'sqlite:///{db_path}'


class Config:
    """Flask configuration loaded from environment variables."""

    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'false').lower() == 'true'
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'false').lower() == 'true'
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '8000'))
