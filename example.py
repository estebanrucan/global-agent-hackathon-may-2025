from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from IPython.display import Markdown, display
#from agno.tools.duckduckgo import DuckDuckGoTool

load_dotenv()

# --- Configuración de Memoria y Almacenamiento ---
# Crear directorio si no existe (aunque ya lo hicimos con mkdir)
os.makedirs('data', exist_ok=True)

agent_storage = SqliteStorage(
    table_name="agent_sessions", db_file="data/agent_sessions.db"
)

# Opcional: Limpiar memoria al iniciar (para pruebas)
# memory.clear()
# -----------------------------------------------

class FirecrawlTool:
    def __init__(self, api_key, instruction: str, template: "str"):
        self.app = FirecrawlApp(api_key=api_key)
        self.instruction = instruction
        self.template = template

    def search(self, search: str) -> str:
        """Hace una busqueda en el sitio web de ChileAtiende y devuelve el contenido en formato Markdown.
        Args:
            search (str): La consulta de búsqueda que se desea realizar, obligatorio.
        
        Returns:
            str: El contenido en formato Markdown de los resultado de la búsqueda.
        """

        if not search or len(search) < 5:
            return "Error: No se proporcionó una consulta de búsqueda."
        
        response = ""
        finished = False
        trials = 0
        limit = 2
        while not finished and trials < 2:
            trials += 1
            try:
                self.search_result = self.app.search(
                    query = self.instruction + search,
                    limit=limit,
                    country="cl",
                    lang="es",
                    scrape_options=ScrapeOptions(formats=["markdown", "links"])
                )
                if len(self.search_result.data) > 0:
                    # Filtra los resultados para obtener solo los que son fichas de ChileAtiende
                    filtered_results = [
                        result for result in self.search_result.data
                        if result["url"].startswith("https://www.chileatiende.gob.cl/fichas") and not result["url"].endswith("pdf")
                    ]

                    if len(filtered_results) > 0:
                        # Devuelve el contenido en Markdown del primer resultado filtrado
                        for num, result in enumerate(filtered_results, start=1):
                            response += self.template.format(
                                result_number = num,
                                page_title=result["title"],
                                page_url=result["url"],
                                page_content=result["markdown"]
                            )
                        return response
                    else:
                        limit += 2
                        continue
                else:
                    limit += 2
                    if trials == 2:
                        return "Error: No se encontraron resultados."
                    return "Error: No se pudo obtener una respuesta razonable."
            except Exception as e:
                return f"Error al usar Firecrawl: {str(e)}"
FIRECRAWL_INSTRUCTION = "ChileAtiende: " 
FIRECRAWL_SEARCH = "Quiero saber como renovar mi licencia de conducir"
FIRECRAWL_TEMPLATE = """
# Resultado N°{result_number}

## Nombre de la página: 
"{page_title}"

## URL: 
{page_url}

## Contenido: 
{page_content}

"""
# Inicializa la herramienta Firecrawl
firecrawl_tool = FirecrawlTool(
    api_key=os.getenv("FIRECRAWL_API_KEY"),
    instruction=FIRECRAWL_INSTRUCTION,
    template=FIRECRAWL_TEMPLATE
)
# Comentamos la ejecución de búsqueda de ejemplo al importar
# search_example = firecrawl_tool.search(FIRECRAWL_SEARCH)

AGENT_INSTRUCTIONS = """
**Actúa como un asistente virtual experto en atención ciudadana del Gobierno de Chile. Has trabajado durante 20 años ayudando a personas —especialmente adultos mayores— a entender y realizar trámites públicos de forma clara, amable y eficiente. Eres paciente, empático, y siempre entregas información precisa, detallada y en un lenguaje sencillo.**

Tu objetivo es ayudar al usuario a encontrar respuestas claras sobre trámites y servicios disponibles en el sitio web oficial [ChileAtiende](https://www.chileatiende.gob.cl/). Cuentas con una herramienta que, al recibir una consulta, realiza una búsqueda en el sitio y entrega una respuesta en formato markdown. Cada respuesta incluye:

- 📄 **Nombre de la página de origen**
- 🔗 **Enlace directo a la fuente**
- 📘 **Contenido principal de la página** (explicado de forma comprensible para personas mayores)
- 🧭 **Referencia con formato de cita** tal como se muestra en el ejemplo.

### Sigue estos pasos:

1. **Analiza la consulta del usuario** y asegúrate de comprender qué trámite o información desea conocer.
2. **Realiza una búsqueda con la herramienta provista** que recibe una consulta entrega resultados desde ChileAtiende en formato markdown.
3. **Reescribe la información** en un tono muy amable, cercano y sin tecnicismos, pensando que estás ayudando a una persona mayor que no está familiarizada con procesos digitales.
4. **Incluye el nombre de la página**, el **enlace web** como referencia, y presenta el **contenido en un formato claro y estructurado**, usando subtítulos y viñetas si es necesario.
5. Finaliza siempre con una nota de apoyo, ofreciendo continuar la ayuda si lo necesita.

📌 **Ejemplo del formato de respuesta esperado**:

---

**Trámite: Renovación de Cédula de Identidad**

Para renovar tu cédula de identidad, debes agendar una hora en el Registro Civil. Puedes hacerlo de forma presencial o en línea si tienes ClaveÚnica. Este proceso es muy importante, sobre todo si tu carnet ya está vencido o por vencer<sup><a href="https://www.chileatiende.gob.cl/fichas/23456-renovacion-cedula-de-identidad">1</a></sup>.

- **Dónde se hace:** Registro Civil (presencial) o sitio web
- **Requisitos:** Presentar tu cédula vencida. En caso de extravío, debes informar eso.
- **Costo:** $3.820 para chilenos, $4.270 para extranjeros
- **Tiempo estimado:** 7 a 10 días hábiles

**Fuentes:**
1. https://www.chileatiende.gob.cl/fichas/23456-renovacion-cedula-de-identidad
"""


model = Gemini(
    api_key=os.getenv("GOOGLE_API_KEY"),
    id="gemini-2.0-flash", # Opcional, Gemini usa un modelo por defecto si no se especifica
)

agent = Agent(
    model=model, # Opcional, Agno usa un modelo por defecto si no se especifica
    tools=[
        firecrawl_tool.search, # Añade la función de scrape de Firecrawl como herramienta,
        #DuckDuckGoTool()
    ],
    instructions=AGENT_INSTRUCTIONS,
    show_tool_calls=True, # Muestra las llamadas a herramientas en la consola
    # --- Añadir configuración de memoria/almacenamiento ---
    storage=agent_storage,
    add_history_to_messages=True
    # ---------------------------------------------------
)
# Comentamos la demo al importar
# response = agent.run(
#     message="¿Cómo puedo renovar mi licencia de conducir?",
#     markdown=True
# )
# display(Markdown(response.content))

# Función para manejar mensajes desde el backend
def handle_message(message: str, **kwargs) -> str:
    """Procesa el mensaje con el agente usando IDs de usuario/sesión y devuelve la respuesta en formato Markdown."""
    result = agent.run(message=message, markdown=True)
    return result.content if hasattr(result, "content") else str(result)

if __name__ == "__main__":
    # Ejemplo de uso (necesitaría user_id y session_id para funcionar correctamente con memoria)
    test_user_id = "test_user"
    test_session_id = "test_session_1"
    print(f"Ejecutando demo con User ID: {test_user_id}, Session ID: {test_session_id}")
    response_md = handle_message(FIRECRAWL_SEARCH, user_id=test_user_id, session_id=test_session_id)
    display(Markdown(response_md))