"""
UX Research Manager - Web Interface (Chunk 3)

A Flask web application for the UX Research Manager with a filter-centric dashboard.
Uses the Aquatic color palette for a calm, high-focus research environment.
"""

from flask import Flask, render_template, request, jsonify, url_for
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
    'bright_turquoise': '#5BE3D2', # AI & Insights
    'sky_blue': '#5BC8E3',         # Categorization & Tags
    'seafoam_green': '#5BE3A4',    # Success & Validation
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

@app.route('/personas')
def personas():
    """View all personas."""
    personas_list = data_store.get_all_personas()
    return render_template(
        'personas.html',
        colors=COLORS,
        personas=personas_list
    )

@app.route('/about')
def about():
    """About page."""
    return render_template(
        'about.html',
        colors=COLORS
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

