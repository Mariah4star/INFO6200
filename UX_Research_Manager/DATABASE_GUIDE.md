# Database Management Guide - UX Research Manager

## Overview
The UX Research Manager now uses SQLAlchemy with SQL database storage, replacing the previous JSON file system. The database is configured to work seamlessly across:
- **Local Development**: SQLite (`data/project.db`)
- **Heroku Deployment**: PostgreSQL (automatic via DATABASE_URL)
- **AWS Migration**: PostgreSQL RDS (via DATABASE_URL)

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
# Create empty database tables
python init_db.py

# Or migrate existing JSON data to database
python init_db.py --migrate
```

### 3. Run Application
```bash
python web_app.py
```

---

## Database Files

### Core Files
- **`models.py`** - SQLAlchemy models (Persona, Insight)
- **`config.py`** - Database configuration
- **`init_db.py`** - Database initialization & migration script
- **`data/project.db`** - SQLite database file (local only)

---

## Database Models

### Persona
```python
- id: Integer (Primary Key)
- name: String (200 chars)
- description: Text
- timestamp: DateTime
- insights: Relationship to Insight
```

### Insight
```python
- id: Integer (Primary Key)
- title: String (200 chars)
- description: Text
- persona_id: Integer (Foreign Key to Persona)
- journey_stage: String (100 chars)
- timestamp: DateTime
- ai_summary: Text
```

---

## Common Tasks

### View Database Contents (SQLite)
```bash
# Using sqlite3 command-line
sqlite3 data/project.db

# Sample queries
SELECT * FROM personas;
SELECT * FROM insights;
SELECT i.title, p.name FROM insights i LEFT JOIN personas p ON i.persona_id = p.id;
```

### Migrate JSON Data to Database
```bash
python init_db.py --migrate
```
This will:
1. Load data from `data/research_data.json`
2. Create Persona and Insight records
3. Backup the JSON file with timestamp
4. Preserve all relationships

### Reset Database
```bash
# Delete database and recreate
rm data/project.db
python init_db.py
```

### Database Administration Tools

**For SQLite (Local):**
- [DB Browser for SQLite](https://sqlitebrowser.org/) - GUI tool
- `sqlite3` command-line tool (built into macOS/Linux)

**For PostgreSQL (Heroku/AWS):**
- [pgAdmin](https://www.pgadmin.org/) - Full-featured GUI
- `psql` command-line tool
- Heroku Dashboard - View data via Heroku web interface

---

## Deployment

### Heroku Setup

1. **Add PostgreSQL Add-on**
```bash
heroku addons:create heroku-postgresql:mini
```
This automatically sets the `DATABASE_URL` environment variable.

2. **Initialize Database on Heroku**
```bash
heroku run python init_db.py
```

3. **View Database on Heroku**
```bash
heroku pg:info
heroku pg:psql
```

### AWS RDS Setup

1. **Create PostgreSQL RDS Instance**
   - Use AWS Console or CLI
   - Note the connection string

2. **Set Environment Variable**
```bash
export DATABASE_URL="postgresql://username:password@host:5432/dbname"
```

3. **Initialize Database**
```bash
python init_db.py
```

---

## Environment Variables

### `DATABASE_URL`
- **Not set**: Uses SQLite at `data/project.db`
- **Set**: Uses specified database (PostgreSQL for production)

Example PostgreSQL URLs:
```
# Heroku (auto-set)
postgres://user:pass@host.compute.amazonaws.com:5432/dbname

# AWS RDS
postgresql://admin:password@mydb.rds.amazonaws.com:5432/uxresearch
```

---

## Troubleshooting

### "No module named 'flask_sqlalchemy'"
```bash
pip install flask-sqlalchemy
```

### "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Database Not Found
```bash
python init_db.py
```

### Migration Issues
Check that `data/research_data.json` exists and is valid JSON.

### Foreign Key Errors
Ensure personas are created before insights that reference them.

---

## Database Schema Changes

If you need to modify the database schema:

1. Update models in `models.py`
2. Drop and recreate database:
   ```bash
   rm data/project.db
   python init_db.py
   ```

For production, consider using database migrations with [Flask-Migrate](https://flask-migrate.readthedocs.io/).

---

## Data Backup

### SQLite Backup
```bash
cp data/project.db data/project_backup_$(date +%Y%m%d).db
```

### PostgreSQL Backup (Heroku)
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

### PostgreSQL Backup (AWS)
Use AWS RDS automated backups or manual snapshots.

---

## AI Features

AI summarization continues to work with the new database:
- Summaries generated on insight creation
- On-demand summary generation via "Generate AI Summary" button
- Summaries stored in `ai_summary` field

---

## Performance

### SQLite (Local)
- Excellent for development and small deployments
- No additional server needed
- File-based storage

### PostgreSQL (Production)
- Better concurrency and performance
- Required for Heroku/AWS
- ACID compliant with robust transaction support

---

## Support

For issues or questions about database management:
1. Check this guide
2. Review `models.py` and `config.py`
3. Test with `init_db.py`

---

**Last Updated**: Chunk 6 - Data Migration Complete
