# Asistente de IA Multiagente ChileAtiende

## Resumen y Objetivo Comercial

Este proyecto es un sistema de inteligencia artificial multiagente que ingiere, indexa y razona sobre toda la información pública del sitio web *chileatiende.gob.cl*. Su objetivo principal es proporcionar respuestas claras y concisas a las preguntas de los ciudadanos sobre los servicios gubernamentales, ahorrándoles un tiempo valioso, con un enfoque especial en ayudar a los adultos mayores.

El proyecto tiene como objetivo demostrar un flujo de trabajo donde agentes autónomos rastrean, estructuran y actualizan continuamente el contenido de ChileAtiende, mientras que un agente conversacional proporciona respuestas fiables y respaldadas por citas en lenguaje natural.

## Equipo del Proyecto

Este proyecto fue desarrollado por:

*   **Líder de Equipo**: `@estebanrucan` (Ingeniero Científico de Datos)
*   **Miembro del Equipo**: `@Constanza-Riquelme` (Analista de Datos)

*Hemos construido soluciones de aprendizaje automático para datos de bienes de consumo. Esteban diseña flujos de trabajo de ML de extremo a extremo en entornos de telecomunicaciones; Constanza analiza y modela conjuntos de datos FMCG de gran volumen para informar decisiones comerciales.*

## Características

*   **Asistente Conversacional Inteligente**: Interactúa con los usuarios en lenguaje natural para resolver consultas sobre trámites y servicios de ChileAtiende.
*   **Integración con Firecrawl**: Utiliza Firecrawl para realizar búsquedas en tiempo real en el sitio de ChileAtiende y extraer información relevante.
*   **Procesamiento con Modelos de Lenguaje (LLM)**: Emplea Gemini de Google para comprender consultas y generar respuestas coherentes y amigables para el usuario.
*   **Memoria Basada en Sesión**: El agente recuerda el contexto de la conversación durante la sesión actual del usuario para una interacción más fluida y personalizada.
*   **Interfaz Amigable para Adultos Mayores**: Diseño de frontend limpio con buena legibilidad y fácil navegación.
*   **Backend Flask**: Estructura modular y robusta utilizando Flask y Blueprints.

## Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar el mantenimiento y la escalabilidad:

```
/chileatiende_assistant
├── app/                    # Módulo principal de la aplicación Flask
│   ├── __init__.py         # Fábrica de la aplicación Flask, registra Blueprints
│   ├── main/               # Blueprint para rutas de la UI (sirve index.html)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── api/                # Blueprint para la API de chat (/api/chat)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── agent_core/         # Lógica central para el agente Agno
│   │   ├── __init__.py
│   │   ├── agent_config.py # Configuración de herramientas e instrucciones del agente
│   │   ├── agent_setup.py  # Inicialización del Agente, Modelos, Almacenamiento
│   │   └── chat_handler.py # Lógica para manejar mensajes con el agente
│   ├── static/             # Archivos estáticos (CSS, JS)
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/          # Plantillas HTML (index.html)
├── data/                   # Directorio para bases de datos (ej., agent_sessions.db)
├── config.py               # Configuraciones de la aplicación Flask (claves, debug)
├── run.py                  # Script para ejecutar la aplicación
├── .env                    # Archivo para variables de entorno (API Keys)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo (versión en inglés)
└── README_es.md            # Versión en español de este archivo
```

## Prerrequisitos

*   Python 3.9 o superior
*   pip (gestor de paquetes de Python)
*   Un navegador web moderno

## Configuración del Entorno

1.  **Clonar el Repositorio (si aplica)**:
    ```bash
    git clone <url-del-repositorio>
    cd chileatiende_assistant
    ```

2.  **Crear un Entorno Virtual** (recomendado):
    ```bash
    python -m venv venv
    ```
    Actívalo:
    *   En Windows:
        ```bash
        venv\Scripts\activate
        ```
    *   En macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Instalar Dependencias**:
    Asegúrate de tener el archivo `requirements.txt` en la raíz del proyecto.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno**:
    En la raíz del proyecto, encontrarás un archivo llamado `.env.example`.
    Haz una copia de este archivo y llámala `.env`:

    *   En Windows (Símbolo del sistema):
        ```bash
        copy .env.example .env
        ```
    *   En macOS/Linux (Terminal):
        ```bash
        cp .env.example .env
        ```
    
    Ahora, abre el archivo `.env` y completa tus claves API reales y cualquier otra configuración necesaria:

    ```env
    FIRECRAWL_API_KEY="tu_clave_api_firecrawl_aqui"
    GOOGLE_API_KEY="tu_clave_api_google_gemini_aqui"
    SECRET_KEY="cambia_esto_por_una_cadena_secreta_muy_larga_y_segura"
    FLASK_DEBUG=True
    ```
    Reemplaza los valores de ejemplo con tus credenciales reales y configuraciones deseadas. El archivo `.env` está incluido en `.gitignore` y no debe ser subido al control de versiones.

## Ejecución de la Aplicación

Una vez que el entorno esté configurado y las dependencias instaladas:

1.  Asegúrate de estar en el directorio raíz del proyecto (`chileatiende_assistant`).
2.  Ejecuta el siguiente comando en tu terminal:
    ```bash
    python run.py
    ```
3.  La aplicación Flask se iniciará. Por defecto, estará disponible en `http://127.0.0.1:5000/` o `http://localhost:5000/`.
4.  Abre esta URL en tu navegador web para interactuar con el asistente.

## Funcionamiento Interno

*   **Interfaz de Usuario (`index.html`, `style.css`, `app.js`)**: Proporciona una ventana de chat simple y accesible. Las preguntas del usuario se envían al backend mediante JavaScript (`API fetch`).
*   **Backend (Flask)**:
    *   `run.py` inicia la aplicación Flask utilizando la fábrica `create_app` definida en `app/__init__.py`.
    *   `app/__init__.py` configura la aplicación, carga los ajustes desde `config.py` y registra los Blueprints.
    *   `app/main/routes.py` sirve la página principal (`index.html`).
    *   `app/api/routes.py` maneja las solicitudes a `/api/chat`. Genera/recupera un `user_id` y `session_id` para el usuario (usando la sesión de Flask) y pasa la consulta al `chat_handler`.
*   **Núcleo del Agente (`app/agent_core/`)**:
    *   `agent_config.py`: Contiene plantillas de prompts, configuración de `FirecrawlTool`.
    *   `agent_setup.py`: Inicializa el modelo LLM (Gemini), la instancia de `FirecrawlTool`, el almacenamiento de sesión (`SqliteStorage` en el directorio `data/`) y el `Agent` de Agno. Este agente se configura con herramientas, instrucciones y el sistema de almacenamiento para el historial.
    *   `chat_handler.py`: La función `handle_message` recibe la pregunta del usuario y los IDs de sesión/usuario, invoca al agente (`agent.run()`) y devuelve la respuesta generada.
*   **Memoria y Estado**: Se utiliza `SqliteStorage` para mantener un historial de conversación por sesión (`user_id`, `session_id`), permitiendo que el agente tenga contexto de interacciones previas dentro de la misma sesión.

## Tecnologías Utilizadas

*   **Python**: Lenguaje de programación principal.
*   **Flask**: Microframework web para el backend.
*   **Agno**: Framework para crear agentes de IA.
*   **SDK de Firecrawl**: Para interactuar con el servicio Firecrawl y realizar búsquedas web.
*   **Google Gemini**: Modelo de lenguaje grande para procesamiento de lenguaje natural.
*   **HTML, CSS, JavaScript**: Para la interfaz de usuario del chat.
*   **SQLite**: Para el almacenamiento de sesiones del agente.
*   **python-dotenv**: Para gestionar variables de entorno.

## Posibles Mejoras Futuras

*   Implementar un sistema de autenticación de usuarios para memoria persistente a largo plazo.
*   Añadir más herramientas al agente (ej., consulta de bases de datos internas, APIs de servicios específicos).
*   Mejorar el manejo de errores y el logging.
*   Implementar un panel de administración para monitorizar interacciones.
*   Desarrollar pruebas unitarias y de integración más completas. 