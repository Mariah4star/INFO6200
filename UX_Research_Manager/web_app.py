"""
UX Research Manager - Minimal Web Interface (Chunk 3)

This is a minimal Flask web application that serves as the first step
in transitioning from CLI to web interface.
"""

from UXRM import flask_app

if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
