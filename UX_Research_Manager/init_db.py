"""
UX Research Manager - Database Initialization Script (Chunk 6)

Run this script to:
1. Create database tables
2. Optionally migrate data from JSON to SQL database
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from models import db, Persona, Insight
from config import Config
from flask import Flask


def create_app():
    """Create Flask app with database configuration."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


def migrate_json_to_sql(app):
    """Migrate existing JSON data to SQL database."""
    json_file = Path(__file__).parent / 'data' / 'research_data.json'
    
    if not json_file.exists():
        print("No JSON file found. Skipping migration.")
        return
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        personas_data = data.get('personas', [])
        insights_data = data.get('insights', [])
        
        with app.app_context():
            # Check if data already exists
            if Persona.query.first() or Insight.query.first():
                print("Database already contains data. Skipping migration.")
                return
            
            # Migrate personas first (due to foreign key constraints)
            persona_map = {}  # Map old IDs to new Persona objects
            for persona_data in personas_data:
                persona = Persona(
                    name=persona_data['name'],
                    description=persona_data['description']
                )
                db.session.add(persona)
                db.session.flush()  # Get the ID without committing
                persona_map[persona_data['id']] = persona
            
            # Migrate insights
            for insight_data in insights_data:
                persona_id = insight_data.get('persona_id')
                persona_obj = persona_map.get(persona_id) if persona_id else None
                
                insight = Insight(
                    title=insight_data['title'],
                    description=insight_data['description'],
                    persona_id=persona_obj.id if persona_obj else None,
                    journey_stage=insight_data.get('journey_stage'),
                    ai_summary=insight_data.get('ai_summary')
                )
                db.session.add(insight)
            
            db.session.commit()
            print(f"✓ Migrated {len(personas_data)} personas and {len(insights_data)} insights")
            
            # Backup JSON file
            backup_file = json_file.parent / f'research_data_backup_{json_file.stat().st_mtime}.json'
            json_file.rename(backup_file)
            print(f"✓ JSON file backed up to {backup_file.name}")
            
    except Exception as e:
        print(f"✗ Error migrating data: {e}")
        db.session.rollback()


def init_database(migrate=False):
    """Initialize database and optionally migrate JSON data."""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully")
        print(f"✓ Database location: {Config.SQLALCHEMY_DATABASE_URI}")
        
        if migrate:
            print("\nMigrating JSON data to database...")
            migrate_json_to_sql(app)
        
        # Display current counts
        persona_count = Persona.query.count()
        insight_count = Insight.query.count()
        print(f"\n📊 Current database status:")
        print(f"   Personas: {persona_count}")
        print(f"   Insights: {insight_count}")


if __name__ == '__main__':
    # Check for migration flag
    migrate = '--migrate' in sys.argv or '-m' in sys.argv
    
    if migrate:
        print("Database initialization with JSON migration\n")
    else:
        print("Database initialization (no migration)")
        print("Use --migrate or -m flag to migrate JSON data\n")
    
    init_database(migrate=migrate)
    print("\n✓ Database initialization complete!")
