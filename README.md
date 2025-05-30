# ChileAtiende AI Assistant

## Overview and Business Objective

This project is an artificial intelligence assistant that ingests, indexes, and reasons about all public information on the *chileatiende.gob.cl* website. Its main goal is to provide clear and concise answers to citizens' questions about government services, saving them valuable time, with a special focus on assisting older adults.

The project aims to demonstrate a pipeline where a single AI agent crawls, structures, and continuously refreshes ChileAtiende content, providing reliable, citation-backed answers in natural language.

## Video Demo

LINK: <https://youtu.be/xKKGC60bA4g?si=DN_hUMciPLxKHAjz>

## Project Team

This project was developed by:

*   **Team Lead**: `@estebanrucan` (Data Scientist Engineer)
*   **Team Member**: `@Constanza-Riquelme` (Data Analyst)

*We've built machine-learning solutions for consumer-goods data. Esteban designs end-to-end ML pipelines in telco environments; Constanza analyzes and models high-volume FMCG datasets to inform business decisions.*

## Features

*   **Intelligent Conversational Assistant**: Interacts with users in natural language to resolve queries about ChileAtiende procedures and services.
*   **Firecrawl Integration**: Uses Firecrawl to perform real-time searches on the ChileAtiende site and extract relevant information.
*   **Language Model Processing (LLM)**: Employs Google's Gemini to understand queries and generate coherent, user-friendly responses.
*   **Session-Based Memory**: The agent remembers the conversation context during the user's current session for a smoother and more personalized interaction.
*   **Elderly-Friendly Interface**: Clean frontend design with good readability and easy navigation.
*   **Flask Backend**: Modular and robust structure using Flask and Blueprints.

## Project Structure

The project follows a modular structure to facilitate maintenance and scalability:

```
/chileatiende_assistant
├── app/                    # Main Flask application module
│   ├── __init__.py         # Flask application factory, registers Blueprints
│   ├── main/               # Blueprint for UI routes (serves index.html)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── api/                # Blueprint for the chat API (/api/chat)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── agent_core/         # Core logic for the Agno agent
│   │   ├── __init__.py
│   │   ├── agent_config.py # Agent tool and instruction configuration
│   │   ├── agent_setup.py  # Agent, Models, Storage initialization
│   │   └── chat_handler.py # Logic for handling messages with the agent
│   ├── static/             # Static files (CSS, JS)
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/          # HTML templates (index.html)
├── data/                   # Directory for databases (e.g., agent_sessions.db)
├── config.py               # Flask application configurations (keys, debug)
├── run.py                  # Script to run the application
├── .env                    # File for environment variables (API Keys)
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## Prerequisites

*   Python 3.9 or higher
*   pip (Python package manager)
*   A modern web browser

## Environment Setup

1.  **Navigate to the Project Directory**:
    Open your terminal or command prompt and navigate to the main directory where this project's files are located.
    ```bash
    cd path/to/your/chileatiende_assistant
    ```

2.  **Create a Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    ```
    Activate it:
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies**:
    Ensure you have the `requirements.txt` file in the project root.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    In the project root, you will find a file named `.env.example`.
    Make a copy of this file and name it `.env`:

    *   On Windows (Command Prompt):
        ```bash
        copy .env.example .env
        ```
    *   On macOS/Linux (Terminal):
        ```bash
        cp .env.example .env
        ```
    
    Now, open the `.env` file and fill in your actual API keys and any other necessary configurations:

    ```env
    FIRECRAWL_API_KEY="your_firecrawl_api_key_here"
    GOOGLE_API_KEY="your_google_gemini_api_key_here"
    SECRET_KEY="change_this_to_a_very_long_and_secure_secret_string"
    FLASK_DEBUG=True
    ```
    Replace the placeholder values with your actual credentials and desired settings. The `.env` file is included in `.gitignore` and should not be committed to version control.

## Running the Application

Before running the application, it's crucial to ensure all tests pass.

1.  **Run Tests**:
    Open your terminal in the project root and execute the tests:
    ```bash
    pytest --cov=app
    ```
    If all tests pass, proceed to the next step. If any tests fail, please resolve them before starting the application.

2.  **Start the Application**:
    Once the tests have passed and you are in the project root directory (`chileatiende_assistant`), run the following command in your terminal:
    ```bash
    python run.py
    ```
3.  The Flask application will start (if tests in `run.py` also pass). By default, it will be available at `http://127.0.0.1:5000/` or `http://localhost:5000/`.
4.  Open this URL in your web browser to interact with the assistant.

## Internal Workings

*   **User Interface (`index.html`, `style.css`, `app.js`)**: Provides a simple and accessible chat window. User questions are sent to the backend via JavaScript (`fetch API`).
*   **Backend (Flask)**:
    *   `run.py` starts the Flask application using the `create_app` factory defined in `app/__init__.py`.
    *   `app/__init__.py` configures the application, loads settings from `config.py`, and registers Blueprints.
    *   `app/main/routes.py` serves the main page (`index.html`).
    *   `app/api/routes.py` handles requests to `/api/chat`. It generates/retrieves a `user_id` and `session_id` for the user (using Flask session) and passes the query to the `chat_handler`.
*   **Agent Core (`app/agent_core/`)**:
    *   `agent_config.py`: Contains prompt templates, `FirecrawlTool` configuration.
    *   `agent_setup.py`: Initializes the LLM model (Gemini), `FirecrawlTool` instance, session storage (`SqliteStorage` in the `data/` directory), and the Agno `Agent`. This agent is configured with tools, instructions, and the storage system for history.
    *   `chat_handler.py`: The `handle_message` function receives the user's question and session/user IDs, invokes the agent (`agent.run()`), and returns the generated response.
*   **Memory and State**: `SqliteStorage` is used to maintain a conversation history per session (`user_id`, `session_id`), allowing the agent to have context from previous interactions within the same session.

## Technologies Used

*   **Python**: Main programming language.
*   **Flask**: Web microframework for the backend.
*   **Agno**: Framework for creating AI agents.
*   **Firecrawl SDK**: For interacting with the Firecrawl service and performing web searches.
*   **Google Gemini**: Large language model for natural language processing.
*   **HTML, CSS, JavaScript**: For the chat user interface.
*   **SQLite**: For agent session storage.
*   **python-dotenv**: For managing environment variables.

## Potential Future Improvements

*   Implement a user authentication system for long-term persistent memory.
*   Add more tools to the agent (e.g., querying internal databases, specific service APIs).
*   Enhance error handling and logging.
*   Implement an admin panel for monitoring interactions.
*   Develop more comprehensive unit and integration tests. 

## Testing

This project uses `pytest` for running tests and `coverage.py` (via `pytest-cov`) for measuring test coverage.

### Prerequisites for Testing

Ensure you have installed the development dependencies:

```bash
pip install -r requirements.txt 
# (pytest, pytest-cov, and coverage are included in requirements.txt)
```

### Running Tests

To run all tests and see a quick summary of coverage in the terminal:

```bash
pytest --cov=app
```

To generate a detailed HTML coverage report (after running the command above or just `pytest --cov=app`):

1.  Run pytest with HTML report generation:
    ```bash
    pytest --cov=app --cov-report=html
    ```
2.  Open the generated report in your browser:
    ```
    htmlcov/index.html
    ```

This report will show line-by-line coverage for each file in the `app` module.

The goal is to maintain 100% test coverage. 