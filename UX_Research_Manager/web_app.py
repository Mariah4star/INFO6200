"""
UX Research Manager - Web Interface (Chunk 6)

SQLAlchemy-based web application with robust SQL database storage.
Compatible with SQLite (local) and PostgreSQL (Heroku/AWS).
"""

from flask import Flask, render_template, request, jsonify, url_for, redirect
from models import db, Persona, Insight
from config import Config
from UXRM import ai_assistant
from datetime import datetime

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

# Configure database
app.config.from_object(Config)
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Aquatic Color Palette
COLORS = {
    'royal_blue': '#5B72E3',      # Primary Action
    'medium_blue': '#5B9DE3',      # Secondary Interaction
    'bright_turquoise': '#2BB5A5', # AI & Insights
    'sky_blue': '#5BC8E3',         # Categorization & Tags
    'pink': "#EC4899",             # Success & Validation
    'soft_blue': '#A6D7E3',        # UI Accents
    'white': '#FFFFFF'             # Workspace Canvas
}



# Web Routes
@app.route('/')
def dashboard():
    """Dashboard home page."""
    insights = Insight.query.order_by(Insight.timestamp.desc()).all()
    personas = Persona.query.all()
    
    # Get recent insights with persona names
    recent_insights = []
    for insight in insights[:3]:  # First 3 (most recent)
        insight_dict = insight.to_dict()
        recent_insights.append(insight_dict)
    
    return render_template(
        'dashboard.html',
        colors=COLORS,
        insights_count=len(insights),
        personas_count=len(personas),
        recent_insights=recent_insights
    )

@app.route('/insights')
def insights():
    """View all insights."""
    insights_list = Insight.query.order_by(Insight.timestamp.desc()).all()
    personas_list = Persona.query.all()
    
    # Convert to dictionaries for template
    insights_data = [insight.to_dict() for insight in insights_list]
    personas_data = [persona.to_dict() for persona in personas_list]
    
    return render_template(
        'insights.html',
        colors=COLORS,
        insights=insights_data,
        personas=personas_data
    )

@app.route('/insights/<int:insight_id>')
def view_insight(insight_id):
    """View a single insight with full details."""
    insight = Insight.query.get_or_404(insight_id)
    
    return render_template(
        'insight_detail.html',
        colors=COLORS,
        insight=insight.to_dict()
    )

@app.route('/insights/<int:insight_id>/edit', methods=['GET', 'POST'])
def edit_insight(insight_id):
    """Edit an insight."""
    insight = Insight.query.get_or_404(insight_id)
    
    if request.method == 'POST':
        # Handle form submission
        try:
            insight.title = request.form.get('title')
            insight.description = request.form.get('description')
            
            # Handle persona_id
            persona_id = request.form.get('persona_id')
            insight.persona_id = int(persona_id) if persona_id else None
            
            # Handle journey_stage
            journey_stage = request.form.get('journey_stage')
            insight.journey_stage = journey_stage if journey_stage else None
            
            db.session.commit()
            
            return redirect(url_for('view_insight', insight_id=insight_id))
        except Exception as e:
            db.session.rollback()
            return f"Error updating insight: {str(e)}", 400
    
    # GET request - show edit form
    personas_list = Persona.query.all()
    return render_template(
        'edit_insight.html',
        colors=COLORS,
        insight=insight.to_dict(),
        personas=[p.to_dict() for p in personas_list]
    )

@app.route('/insights/<int:insight_id>/delete', methods=['POST'])
def delete_insight(insight_id):
    """Delete an insight."""
    try:
        insight = Insight.query.get(insight_id)
        if not insight:
            return jsonify({'success': False, 'message': 'Insight not found'}), 404
        
        db.session.delete(insight)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/personas')
def personas():
    """View all personas."""
    personas_list = Persona.query.order_by(Persona.timestamp.desc()).all()
    return render_template(
        'personas.html',
        colors=COLORS,
        personas=[p.to_dict() for p in personas_list]
    )

@app.route('/personas/<int:persona_id>')
def view_persona(persona_id):
    """View a single persona with full details."""
    persona = Persona.query.get_or_404(persona_id)
    
    return render_template(
        'persona_detail.html',
        colors=COLORS,
        persona=persona.to_dict()
    )

@app.route('/personas/<int:persona_id>/edit', methods=['GET', 'POST'])
def edit_persona(persona_id):
    """Edit a persona."""
    persona = Persona.query.get_or_404(persona_id)
    
    if request.method == 'POST':
        # Handle form submission
        try:
            persona.name = request.form.get('name')
            persona.description = request.form.get('description')
            
            db.session.commit()
            
            return redirect(url_for('view_persona', persona_id=persona_id))
        except Exception as e:
            db.session.rollback()
            return f"Error updating persona: {str(e)}", 400
    
    # GET request - show edit form
    return render_template(
        'edit_persona.html',
        colors=COLORS,
        persona=persona.to_dict()
    )

@app.route('/personas/<int:persona_id>/delete', methods=['POST'])
def delete_persona(persona_id):
    """Delete a persona."""
    try:
        persona = Persona.query.get(persona_id)
        if not persona:
            return jsonify({'success': False, 'message': 'Persona not found'}), 404
        
        db.session.delete(persona)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/about')
def about():
    """About page."""
    return render_template(
        'about.html',
        colors=COLORS
    )

@app.route('/insights/new')
def new_insight():
    """Show form to create new insight."""
    personas_list = Persona.query.all()
    return render_template(
        'create_insight.html',
        colors=COLORS,
        personas=[p.to_dict() for p in personas_list]
    )

@app.route('/insights', methods=['POST'])
def create_insight():
    """Handle creating a new insight."""
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        persona_id = request.form.get('persona_id')
        journey_stage = request.form.get('journey_stage')
        
        # Convert empty strings to None
        persona_id = int(persona_id) if persona_id else None
        journey_stage = journey_stage if journey_stage else None
        
        # Get AI summary
        ai_summary = ''
        try:
            ai_summary = ai_assistant.summarize_research(description)
        except Exception as e:
            ai_summary = f"Error generating summary: {str(e)}"
        
        # Create new insight
        new_insight = Insight(
            title=title,
            description=description,
            persona_id=persona_id,
            journey_stage=journey_stage,
            ai_summary=ai_summary
        )
        
        db.session.add(new_insight)
        db.session.commit()
        
        return redirect(url_for('insights'))
    except Exception as e:
        db.session.rollback()
        return f"Error creating insight: {str(e)}", 400

@app.route('/personas/new')
def new_persona():
    """Show form to create new persona."""
    return render_template(
        'create_persona.html',
        colors=COLORS
    )

@app.route('/personas', methods=['POST'])
def create_persona():
    """Handle creating a new persona."""
    try:
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Create new persona
        new_persona = Persona(
            name=name,
            description=description
        )
        
        db.session.add(new_persona)
        db.session.commit()
        
        return redirect(url_for('personas'))
    except Exception as e:
        db.session.rollback()
        return f"Error creating persona: {str(e)}", 400

@app.route('/api/insights/<insight_id>/summarize', methods=['POST'])
def summarize_insight_api(insight_id):
    """Generate AI summary for an insight via API."""
    try:
        # Get the insight
        insight = Insight.query.get(int(insight_id))
        if not insight:
            return jsonify({'success': False, 'message': 'Insight not found'}), 404
        
        # Generate summary
        summary = ai_assistant.summarize_research(insight.description)
        
        # Update the insight with the summary
        insight.ai_summary = summary
        db.session.commit()
        
        return jsonify({'success': True, 'summary': summary})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
