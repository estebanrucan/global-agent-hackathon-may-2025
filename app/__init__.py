from flask import Flask
from config import Config
import os

def create_app(config_class=Config):
    # Explicitamente definimos template_folder y static_folder relativos a 'app'
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    # Crear directorio de datos si no existe
    # data_dir debe estar fuera de la carpeta app para no ser servido accidentalmente
    # y para facilitar el montaje de volúmenes en contenedores.
    # Si run.py está en la raíz del proyecto, y app es un subdirectorio:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    app.config['DATA_DIR'] = data_dir
    # current_app.logger.info(f"Directorio de datos DATA_DIR: {app.config['DATA_DIR']}")

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Configurar logging si estamos en debug
    if app.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)
        # app.logger.info("Modo DEBUG activado, logging configurado a DEBUG.")

    return app 