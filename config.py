import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # Otras configuraciones pueden ir aquí
    FIRECRAWL_API_KEY = os.environ.get('FIRECRAWL_API_KEY')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') 