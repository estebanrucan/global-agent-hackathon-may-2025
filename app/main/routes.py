from flask import render_template, session, current_app
from app.main import bp
import uuid
import os # Para os.path

@bp.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4().hex
    if 'user_id' not in session: 
        session['user_id'] = session['session_id'] 
    return render_template('index.html') 