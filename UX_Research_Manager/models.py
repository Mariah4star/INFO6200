"""
UX Research Manager - Database Models (Chunk 6)

SQLAlchemy models for research insights and personas.
Designed for SQLite (local) and PostgreSQL (Heroku/AWS).
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Persona(db.Model):
    """User persona model."""
    
    __tablename__ = 'personas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship to insights
    insights = db.relationship('Insight', backref='persona', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert persona to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def __repr__(self):
        return f'<Persona {self.id}: {self.name}>'


class Insight(db.Model):
    """Research insight model."""
    
    __tablename__ = 'insights'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=True)
    journey_stage = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ai_summary = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert insight to dictionary for API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'persona_id': self.persona_id,
            'persona_name': self.persona.name if self.persona else None,
            'journey_stage': self.journey_stage,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'ai_summary': self.ai_summary
        }
    
    def __repr__(self):
        return f'<Insight {self.id}: {self.title}>'
