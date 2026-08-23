import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'digital-citizen-portal-secret-key-2026-internship-secure'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads', 'documents')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max file upload size
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
