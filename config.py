import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'lombongocare_secret_key_altamente_segura_2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "lombongocare.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # IA Config (Gemini ou OpenAI)
    AI_API_KEY = os.environ.get('AI_API_KEY', 'SUA_API_KEY_AQUI')
    AI_API_URL = os.environ.get('AI_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent')