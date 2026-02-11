"""
UX Research Manager - Web Interface (Chunk 4)

Replace command-line input with web-based forms that allow users to submit UX research data through a Flask web interface while continuing to use persistent JSON storage.

"""

from flask import Flask, render_template, request, jsonify, url_for, redirect
from UXRM import data_store, ai_assistant
from datetime import datetime

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

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
    insights = data_store.get_all_insights()
    personas = data_store.get_all_personas()
    
    # Add persona names to insights
    recent_insights = []
    for insight in insights[-3:]:  # Last 3 insights
        insight_dict = dict(insight)
        if insight['persona_id']:
            persona = data_store.get_persona(insight['persona_id'])
            insight_dict['persona_name'] = persona['name'] if persona else 'Unknown'
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
    insights_list = data_store.get_all_insights()
    personas = data_store.get_all_personas()
    
    # Add persona names to insights
    for insight in insights_list:
        if insight['persona_id']:
            persona = data_store.get_persona(insight['persona_id'])
            insight['persona_name'] = persona['name'] if persona else 'Unknown'
    
    return render_template(
        'insights.html',
        colors=COLORS,
        insights=insights_list,
        personas=personas
    )

@app.route('/insights/<int:insight_id>')
def view_insight(insight_id):
    """View a single insight with full details."""
    insight = data_store.get_insight(insight_id)
    if not insight:
        return "Insight not found", 404
    
    # Add persona name if exists
    if insight['persona_id']:
        persona = data_store.get_persona(insight['persona_id'])
        insight['persona_name'] = persona['name'] if persona else 'Unknown'
    
    return render_template(
        'insight_detail.html',
        colors=COLORS,
        insight=insight
    )

@app.route('/insights/<int:insight_id>/edit', methods=['GET', 'POST'])
def edit_insight(insight_id):
    """Edit an insight."""
    insight = data_store.get_insight(insight_id)
    if not insight:
        return "Insight not found", 404
    
    if request.method == 'POST':
        # Handle form submission
        try:
            title = request.form.get('title')
            description = request.form.get('description')
            persona_id = request.form.get('persona_id')
            journey_stage = request.form.get('journey_stage')
            
            # Convert empty strings to None
            persona_id = int(persona_id) if persona_id else None
            journey_stage = journey_stage if journey_stage else None
            
            # Update the insight
            data_store.update_insight(
                insight_id,
                title=title,
                description=description,
                persona_id=persona_id,
                journey_stage=journey_stage
            )
            
            return redirect(url_for('view_insight', insight_id=insight_id))
        except Exception as e:
            return f"Error updating insight: {str(e)}", 400
    
    # GET request - show edit form
    personas_list = data_store.get_all_personas()
    return render_template(
        'edit_insight.html',
        colors=COLORS,
        insight=insight,
        personas=personas_list
    )

@app.route('/insights/<int:insight_id>/delete', methods=['POST'])
def delete_insight(insight_id):
    """Delete an insight."""
    try:
        success = data_store.delete_insight(insight_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Insight not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/personas')
def personas():
    """View all personas."""
    personas_list = data_store.get_all_personas()
    return render_template(
        'personas.html',
        colors=COLORS,
        personas=personas_list
    )

@app.route('/personas/<int:persona_id>')
def view_persona(persona_id):
    """View a single persona with full details."""
    persona = data_store.get_persona(persona_id)
    if not persona:
        return "Persona not found", 404
    
    return render_template(
        'persona_detail.html',
        colors=COLORS,
        persona=persona
    )

@app.route('/personas/<int:persona_id>/edit', methods=['GET', 'POST'])
def edit_persona(persona_id):
    """Edit a persona."""
    persona = data_store.get_persona(persona_id)
    if not persona:
        return "Persona not found", 404
    
    if request.method == 'POST':
        # Handle form submission
        try:
            name = request.form.get('name')
            description = request.form.get('description')
            
            # Update the persona
            data_store.update_persona(persona_id, name=name, description=description)
            
            return redirect(url_for('view_persona', persona_id=persona_id))
        except Exception as e:
            return f"Error updating persona: {str(e)}", 400
    
    # GET request - show edit form
    return render_template(
        'edit_persona.html',
        colors=COLORS,
        persona=persona
    )

@app.route('/personas/<int:persona_id>/delete', methods=['POST'])
def delete_persona(persona_id):
    """Delete a persona."""
    try:
        success = data_store.delete_persona(persona_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Persona not found'}), 404
    except Exception as e:
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
    personas = data_store.get_all_personas()
    return render_template(
        'create_insight.html',
        colors=COLORS,
        personas=personas
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
        
        # Add the insight
        data_store.add_insight(
            title=title,
            description=description,
            persona_id=persona_id,
            journey_stage=journey_stage,
            ai_summary=ai_summary
        )
        
        return redirect(url_for('insights'))
    except Exception as e:
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
        
        data_store.add_persona(
            name=name,
            description=description
        )
        
        return redirect(url_for('personas'))
    except Exception as e:
        return f"Error creating persona: {str(e)}", 400

@app.route('/api/insights/<insight_id>/summarize', methods=['POST'])
def summarize_insight_api(insight_id):
    """Generate AI summary for an insight via API."""
    try:
        # Get the insight
        insight = data_store.get_insight(int(insight_id))
        if not insight:
            return jsonify({'success': False, 'message': 'Insight not found'}), 404
        
        # Generate summary
        summary = ai_assistant.summarize_research(insight['description'])
        
        # Update the insight with the summary
        data_store.update_insight(int(insight_id), ai_summary=summary)
        
        return jsonify({'success': True, 'summary': summary})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
