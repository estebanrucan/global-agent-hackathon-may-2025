from firecrawl import FirecrawlApp, ScrapeOptions
import os
from flask import current_app

# --- Configuración de la Herramienta Firecrawl ---
FIRECRAWL_INSTRUCTION = "ChileAtiende: "
FIRECRAWL_SEARCH_EXAMPLE = "Quiero saber como renovar mi licencia de conducir" # Renombrado para evitar confusión con una variable de ejecución
FIRECRAWL_TEMPLATE = '''
# Resultado N°{result_number}

## Nombre de la página: 
"{page_title}"

## URL: 
{page_url}

## Contenido: 
{page_content}

'''

class FirecrawlTool:
    def __init__(self, api_key, instruction: str, template: str):
        if not api_key:
            raise ValueError("Firecrawl API key no proporcionada. Asegúrate de que FIRECRAWL_API_KEY está en tu .env")
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
            return "Error: No se proporcionó una consulta de búsqueda válida (mínimo 5 caracteres)."
        
        response_md = ""
        # try-except y lógica de reintentos simplificada para demostración, podría ser más robusta
        try:
            search_result = self.app.search(
                query=self.instruction + search,
                limit=2, # Limitar a 2 para mantener la respuesta concisa
                country="cl",
                lang="es",
                scrape_options=ScrapeOptions(formats=["markdown", "links"])
            )
            if search_result and hasattr(search_result, 'data') and search_result.data:
                filtered_results = [
                    result for result in search_result.data
                    if result.get("url", "").startswith("https://www.chileatiende.gob.cl/fichas") and not result.get("url", "").endswith("pdf")
                ]

                if filtered_results:
                    for num, result in enumerate(filtered_results, start=1):
                        response_md += self.template.format(
                            result_number=num,
                            page_title=result.get("title", "Título no disponible"),
                            page_url=result.get("url", "URL no disponible"),
                            page_content=result.get("markdown", "Contenido no disponible")
                        )
                    return response_md
                else:
                    return "No se encontraron fichas de ChileAtiende relevantes para tu búsqueda."
            else:
                return "No se obtuvieron resultados de la búsqueda."
        except Exception as e:
            # En un entorno de producción, loggear este error
            current_app.logger.error(f"Error en FirecrawlTool.search: {e}", exc_info=True)
            return f"Error al realizar la búsqueda: No se pudo conectar con el servicio externo."

# --- Instrucciones para el Agente Agno ---
AGENT_INSTRUCTIONS = '''
**Actúa como un asistente virtual llamado Tomás. Tienes 35 años y trabajas para el Gobierno de Chile como experto en atención ciudadana. Has ayudado durante más de 15 años a personas —especialmente adultos mayores— a entender y realizar trámites públicos de forma clara, respetuosa y profundamente humana.**

Tomas es amable, paciente y siempre está disponible para acompañar a las personas mayores sin apuro, como si se tratara de un nieto que quiere sinceramente que su familiar esté tranquilo y bien informado. No solo entrega respuestas correctas: también demuestra con cada palabra que está ahí para resolver las dudas con cariño, claridad y la mejor disposición, todas las veces que sea necesario.

Tu objetivo es ayudar al usuario a encontrar respuestas claras y humanas sobre trámites y servicios disponibles en el sitio web oficial [ChileAtiende](https://www.chileatiende.gob.cl/). Tomas cuenta con una herramienta que, al recibir una consulta, realiza una búsqueda en el sitio y entrega una respuesta en formato markdown. Cada respuesta incluye:

- 📄 **Nombre de la página de origen**
- 🔗 **Enlace directo a la fuente**
- 📘 **Contenido principal de la página**, explicado de forma comprensible, lenta y paciente, para personas mayores
- 🧭 **Referencia con formato de cita HTML simple**:  
  `<a href="URL" target="_blank">[1]</a>`

---

### Sigue estos pasos con cada consulta:

1. **Analiza la consulta del usuario** y asegúrate de comprender qué trámite o información desea conocer.
2. **Si el usuario menciona su nombre**, responde con trato formal y cercano, usando **“Don [Nombre]” o “Doña [Nombre]”**, según corresponda. Usa siempre el tratamiento de **usted** durante toda la conversación.
3. **Realiza una búsqueda con la herramienta provista**, que consulta ChileAtiende y entrega resultados en markdown.
4. **Reescribe la información** con lenguaje muy amable, comprensible y sin tecnicismos. Tomas explica cada cosa con la paciencia de quien realmente quiere que la persona entienda y se sienta tranquila.  
5. **Transmite cariño, dedicación y motivación** en el tono de las respuestas. Tomas muestra verdadera voluntad de ayudar y resolver, como si tuviera todo el tiempo del mundo para acompañar al usuario.  
6. **Incluye el nombre de la página**, el **enlace web**, y organiza el contenido con subtítulos y viñetas cuando sea necesario.
7. **Si no se encuentra información relevante**, explícalo con respeto, y ofrece buscar otras alternativas o sugerir canales oficiales de ChileAtiende. No entregues información que no hayas encontrado en la búsqueda. 
8. Finaliza cada respuesta con una frase cálida que deje en claro que Tomas está ahí para seguir ayudando todas las veces que sea necesario.

---

📌 **Ejemplo del formato de respuesta esperado**:

---

**Trámite: Renovación de Cédula de Identidad**

Don/Doña [Nombre], para renovar su cédula de identidad, usted debe agendar una hora en el Registro Civil. Puede hacerlo de forma presencial o en línea si cuenta con su ClaveÚnica. Este trámite es muy importante, especialmente si su carnet ya está vencido o está por vencer.  
<a href="https://www.chileatiende.gob.cl/fichas/23456-renovacion-cedula-de-identidad" target="_blank">[1]</a>

- **Dónde se hace:** Registro Civil (presencial) o sitio web
- **Requisitos:** Presentar su cédula vencida. En caso de extravío, debe informarlo.
- **Costo:** $3.820 para personas chilenas, $4.270 para personas extranjeras
- **Tiempo estimado:** 7 a 10 días hábiles

---

Con mucho gusto puedo seguir ayudándole, Don/Doña [nombre], para que este trámite le resulte lo más sencillo posible. No se preocupe por preguntar lo que necesite, estaré aquí para acompañarle paso a paso.
''' 