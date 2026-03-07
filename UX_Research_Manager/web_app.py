"""
UX Research Manager - Program Security (Chunk 8)

Adds secure user authentication, session management, and per-user data ownership.
"""

import os
from functools import wraps

from flask import Flask, render_template, request, jsonify, url_for, redirect, session, flash
from sqlalchemy import inspect, text

from models import db, User, Persona, Insight
from config import Config
from UXRM import ai_assistant


app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

# Configure database and session secret
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-change-me')
db.init_app(app)


# Aquatic Color Palette
COLORS = {
    'royal_blue': '#5B72E3',      # Primary Action
    'medium_blue': '#5B9DE3',     # Secondary Interaction
    'bright_turquoise': '#2BB5A5',  # AI & Insights
    'sky_blue': '#5BC8E3',        # Categorization & Tags
    'pink': '#EC4899',            # Success & Validation
    'soft_blue': '#A6D7E3',       # UI Accents
    'white': '#FFFFFF'            # Workspace Canvas
}


def ensure_auth_schema() -> None:
    """Add auth ownership columns when migrating existing databases."""
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()

    if 'users' not in table_names:
        User.__table__.create(db.engine, checkfirst=True)

    persona_columns = {col['name'] for col in inspector.get_columns('personas')} if 'personas' in table_names else set()
    insight_columns = {col['name'] for col in inspector.get_columns('insights')} if 'insights' in table_names else set()

    if 'personas' in table_names and 'user_id' not in persona_columns:
        db.session.execute(text('ALTER TABLE personas ADD COLUMN user_id INTEGER'))

    if 'insights' in table_names and 'user_id' not in insight_columns:
        db.session.execute(text('ALTER TABLE insights ADD COLUMN user_id INTEGER'))

    db.session.commit()


with app.app_context():
    db.create_all()
    ensure_auth_schema()


def current_user_id():
    return session.get('user_id')


def get_current_user():
    user_id = current_user_id()
    if not user_id:
        return None
    return User.query.get(user_id)


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user_id():
            flash('Please log in to continue.', 'error')
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_shared_context():
    return {
        'colors': COLORS,
        'current_user': get_current_user()
    }


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user account."""
    if current_user_id():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return render_template('register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with that email already exists.', 'error')
            return render_template('register.html')

        try:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in a user and create a session."""
    if current_user_id():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

        session.clear()
        session['user_id'] = user.id
        flash('Welcome back.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Allow a user to change their password from the login flow."""
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        current_password = request.form.get('current_password') or ''
        new_password = request.form.get('new_password') or ''
        confirm_password = request.form.get('confirm_password') or ''

        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return render_template('change_password.html')

        if len(new_password) < 8:
            flash('New password must be at least 8 characters.', 'error')
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('change_password.html')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(current_password):
            flash('Invalid email or current password.', 'error')
            return render_template('change_password.html')

        try:
            user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating password: {str(e)}', 'error')

    return render_template('change_password.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Log out and clear session state."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# Web Routes
@app.route('/')
@login_required
def dashboard():
    """Dashboard home page scoped to the logged-in user."""
    user_id = current_user_id()
    insights = Insight.query.filter_by(user_id=user_id).order_by(Insight.timestamp.desc()).all()
    personas = Persona.query.filter_by(user_id=user_id).all()

    recent_insights = [insight.to_dict() for insight in insights[:3]]

    return render_template(
        'dashboard.html',
        insights_count=len(insights),
        personas_count=len(personas),
        recent_insights=recent_insights
    )


@app.route('/insights')
@login_required
def insights():
    """View all insights for the logged-in user."""
    user_id = current_user_id()
    insights_list = Insight.query.filter_by(user_id=user_id).order_by(Insight.timestamp.desc()).all()
    personas_list = Persona.query.filter_by(user_id=user_id).all()

    return render_template(
        'insights.html',
        insights=[insight.to_dict() for insight in insights_list],
        personas=[persona.to_dict() for persona in personas_list]
    )


@app.route('/insights/<int:insight_id>')
@login_required
def view_insight(insight_id):
    """View a single insight with full details (owner only)."""
    insight = Insight.query.filter_by(id=insight_id, user_id=current_user_id()).first_or_404()

    return render_template('insight_detail.html', insight=insight.to_dict())


@app.route('/insights/<int:insight_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_insight(insight_id):
    """Edit an insight (owner only)."""
    user_id = current_user_id()
    insight = Insight.query.filter_by(id=insight_id, user_id=user_id).first_or_404()

    if request.method == 'POST':
        try:
            title = (request.form.get('title') or '').strip()
            description = (request.form.get('description') or '').strip()
            persona_id_raw = request.form.get('persona_id')
            journey_stage = (request.form.get('journey_stage') or '').strip() or None

            if not title or not description:
                return 'Title and description are required.', 400

            persona_id = None
            if persona_id_raw:
                persona = Persona.query.filter_by(id=int(persona_id_raw), user_id=user_id).first()
                if not persona:
                    return 'Invalid persona selection.', 400
                persona_id = persona.id

            insight.title = title
            insight.description = description
            insight.persona_id = persona_id
            insight.journey_stage = journey_stage
            db.session.commit()

            return redirect(url_for('view_insight', insight_id=insight_id))
        except Exception as e:
            db.session.rollback()
            return f'Error updating insight: {str(e)}', 400

    personas_list = Persona.query.filter_by(user_id=user_id).all()
    return render_template(
        'edit_insight.html',
        insight=insight.to_dict(),
        personas=[p.to_dict() for p in personas_list]
    )


@app.route('/insights/<int:insight_id>/delete', methods=['POST'])
@login_required
def delete_insight(insight_id):
    """Delete an insight (owner only)."""
    try:
        insight = Insight.query.filter_by(id=insight_id, user_id=current_user_id()).first()
        if not insight:
            return jsonify({'success': False, 'message': 'Insight not found'}), 404

        db.session.delete(insight)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/personas')
@login_required
def personas():
    """View all personas for the logged-in user."""
    user_id = current_user_id()
    personas_list = Persona.query.filter_by(user_id=user_id).order_by(Persona.timestamp.desc()).all()
    return render_template('personas.html', personas=[p.to_dict() for p in personas_list])


@app.route('/personas/<int:persona_id>')
@login_required
def view_persona(persona_id):
    """View a single persona with full details (owner only)."""
    persona = Persona.query.filter_by(id=persona_id, user_id=current_user_id()).first_or_404()
    return render_template('persona_detail.html', persona=persona.to_dict())


@app.route('/personas/<int:persona_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_persona(persona_id):
    """Edit a persona (owner only)."""
    persona = Persona.query.filter_by(id=persona_id, user_id=current_user_id()).first_or_404()

    if request.method == 'POST':
        try:
            name = (request.form.get('name') or '').strip()
            description = (request.form.get('description') or '').strip()

            if not name or not description:
                return 'Name and description are required.', 400

            persona.name = name
            persona.description = description
            db.session.commit()

            return redirect(url_for('view_persona', persona_id=persona_id))
        except Exception as e:
            db.session.rollback()
            return f'Error updating persona: {str(e)}', 400

    return render_template('edit_persona.html', persona=persona.to_dict())


@app.route('/personas/<int:persona_id>/delete', methods=['POST'])
@login_required
def delete_persona(persona_id):
    """Delete a persona (owner only)."""
    try:
        persona = Persona.query.filter_by(id=persona_id, user_id=current_user_id()).first()
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
    return render_template('about.html')


@app.route('/insights/new')
@login_required
def new_insight():
    """Show form to create new insight."""
    personas_list = Persona.query.filter_by(user_id=current_user_id()).all()
    return render_template('create_insight.html', personas=[p.to_dict() for p in personas_list])


@app.route('/insights', methods=['POST'])
@login_required
def create_insight():
    """Handle creating a new insight."""
    user_id = current_user_id()
    try:
        title = (request.form.get('title') or '').strip()
        description = (request.form.get('description') or '').strip()
        persona_id_raw = request.form.get('persona_id')
        journey_stage = (request.form.get('journey_stage') or '').strip() or None

        if not title or not description:
            return 'Title and description are required.', 400

        persona_id = None
        if persona_id_raw:
            persona = Persona.query.filter_by(id=int(persona_id_raw), user_id=user_id).first()
            if not persona:
                return 'Invalid persona selection.', 400
            persona_id = persona.id

        ai_summary = ''
        try:
            ai_summary = ai_assistant.summarize_research(description)
        except Exception as e:
            ai_summary = f'Error generating summary: {str(e)}'

        new_insight = Insight(
            user_id=user_id,
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
        return f'Error creating insight: {str(e)}', 400


@app.route('/personas/new')
@login_required
def new_persona():
    """Show form to create new persona."""
    next_url = request.args.get('next', '')
    return render_template('create_persona.html', next_url=next_url)


@app.route('/personas', methods=['POST'])
@login_required
def create_persona():
    """Handle creating a new persona."""
    try:
        name = (request.form.get('name') or '').strip()
        description = (request.form.get('description') or '').strip()
        next_url = request.form.get('next', '').strip()

        if not name or not description:
            return 'Name and description are required.', 400

        new_persona_record = Persona(
            user_id=current_user_id(),
            name=name,
            description=description
        )

        db.session.add(new_persona_record)
        db.session.commit()

        # Redirect back to the page they came from, or default to personas list
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('personas'))
    except Exception as e:
        db.session.rollback()
        return f'Error creating persona: {str(e)}', 400


@app.route('/api/insights/<insight_id>/summarize', methods=['POST'])
@login_required
def summarize_insight_api(insight_id):
    """Generate AI summary for an insight via API (owner only)."""
    try:
        insight = Insight.query.filter_by(id=int(insight_id), user_id=current_user_id()).first()
        if not insight:
            return jsonify({'success': False, 'message': 'Insight not found'}), 404

        summary = ai_assistant.summarize_research(insight.description)
        insight.ai_summary = summary
        db.session.commit()

        return jsonify({'success': True, 'summary': summary})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
