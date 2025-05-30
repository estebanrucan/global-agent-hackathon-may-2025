from flask import current_app
from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
import os

# Importar configuraciones y herramientas específicas del agente
from .agent_config import (
    FirecrawlTool,
    FIRECRAWL_INSTRUCTION,
    FIRECRAWL_TEMPLATE,
    AGENT_INSTRUCTIONS
)

# Variable global para el agente, inicializada una vez
_agent = None
_agent_storage = None

def get_agent_storage():
    """Inicializa y/o devuelve la instancia de SqliteStorage."""
    global _agent_storage
    if _agent_storage is None:
        data_dir = current_app.config['DATA_DIR']
        db_file_path = os.path.join(data_dir, "agent_sessions.db")
        _agent_storage = SqliteStorage(
            table_name="agent_sessions", 
            db_file=db_file_path
        )
    return _agent_storage

def get_agent():
    """Inicializa y/o devuelve la instancia del Agente Agno configurado."""
    global _agent
    if _agent is None:
        google_api_key = current_app.config.get('GOOGLE_API_KEY')
        firecrawl_api_key = current_app.config.get('FIRECRAWL_API_KEY')

        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY no configurada en .env")
        if not firecrawl_api_key:
            # FirecrawlTool ya lanza un error si no hay key, por lo que el warning aquí es redundante.
            # current_app.logger.warning("FIRECRAWL_API_KEY no configurada. La herramienta Firecrawl podría no funcionar.")
            pass # FirecrawlTool.__init__ will raise an error if key is missing.

        # Inicializar el modelo
        model = Gemini(
            api_key=google_api_key,
            id="gemini-2.0-flash" # Puedes cambiar el modelo si es necesario
        )

        # Inicializar la herramienta Firecrawl
        firecrawl_tool = FirecrawlTool(
            api_key=firecrawl_api_key,
            instruction=FIRECRAWL_INSTRUCTION,
            template=FIRECRAWL_TEMPLATE
        )

        # Obtener el storage
        storage = get_agent_storage()

        # Crear el Agente
        _agent = Agent(
            model=model,
            tools=[
                firecrawl_tool.search,
                # Aquí podrías añadir más herramientas si es necesario
            ],
            instructions=AGENT_INSTRUCTIONS,
            storage=storage,
            add_history_to_messages=True, # Para usar el storage y mantener historial
            show_tool_calls=current_app.config.get('DEBUG', False) # Mostrar logs de herramientas en modo debug
        )
        current_app.logger.info("Agente Agno inicializado.")
    return _agent 