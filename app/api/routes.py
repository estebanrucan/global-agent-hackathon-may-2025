from flask import request, jsonify, session, current_app
from app.api import bp
from app.agent_core.chat_handler import handle_message
import uuid

@bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No se proporcionó el mensaje'}), 400
    
    user_message = data['message']
    
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4().hex
    if 'user_id' not in session:
        session['user_id'] = session['session_id']

    user_id = session['user_id']
    session_id = session['session_id']

    try:
        response_md = handle_message(user_message, user_id=user_id, session_id=session_id)
        return jsonify({'response': response_md})
    except Exception as e:
        current_app.logger.error(f"Error en la ruta /api/chat al llamar a handle_message: {e}", exc_info=True)
        return jsonify({'error': f'Ocurrió un error interno al procesar tu solicitud.'}), 500 