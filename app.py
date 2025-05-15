import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, render_template, session
from example import handle_message
import uuid # Para generar IDs de sesión únicos

app = Flask(__name__, static_folder='static', template_folder='templates')
# Se necesita una clave secreta para usar sesiones en Flask
app.secret_key = os.urandom(24) 

@app.route('/')
def index():
    # Asegurar que el usuario tenga un session_id
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4().hex
        # Usaremos el session_id también como user_id para este ejemplo
        session['user_id'] = session['session_id'] 
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No se proporcionó el mensaje'}), 400
    
    user_message = data['message']
    
    # Obtener user_id y session_id de la sesión de Flask
    # Si no existen por alguna razón (ej. primera visita directa a /api/chat), crearlos.
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4().hex
        session['user_id'] = session['session_id'] 

    user_id = session['user_id']
    session_id = session['session_id']

    try:
        response_md = handle_message(user_message, user_id=user_id, session_id=session_id)
        return jsonify({'response': response_md})
    except Exception as e:
        # Considerar loggear el error aquí para depuración en el servidor
        print(f"Error al procesar el mensaje: {e}")
        return jsonify({'error': f'Ocurrió un error interno: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 