import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
    BOTPRESS_WEBHOOK_URL = os.environ.get('BOTPRESS_WEBHOOK_URL')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')