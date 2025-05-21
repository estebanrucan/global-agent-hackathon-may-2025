from flask import current_app
from .agent_setup import get_agent

def handle_message(message: str, user_id: str, session_id: str) -> str:
    """Procesa el mensaje con el agente usando IDs de usuario/sesión y devuelve la respuesta en formato Markdown."""
    agent = get_agent() # Obtiene la instancia configurada del agente
    
    try:
        # La opción markdown=True para la respuesta ya está implícita si el agente está configurado para Markdown.
        # Si necesitas forzarlo o el agente no lo tiene por defecto, puedes añadirlo.
        result = agent.run(
            message=message, 
            user_id=user_id, 
            session_id=session_id,
            markdown=True # Aseguramos respuesta en Markdown
        )
        
        # Verificar si result tiene el atributo content y no es None
        if hasattr(result, 'content') and result.content is not None:
            return result.content
        elif isinstance(result, str): # Si agent.run devuelve directamente un string (caso de algunos errores simples)
            return result
        else:
            current_app.logger.error(f"Respuesta inesperada del agente: {result}")
            return "Lo siento, ocurrió un error inesperado al procesar tu solicitud."
            
    except Exception as e:
        current_app.logger.error(f"Error en handle_message: {e}", exc_info=True) # exc_info=True para loggear el traceback
        return f"Lo siento, ocurrió un error al procesar tu mensaje: {str(e)}" 