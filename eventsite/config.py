import os

DEBUG = os.environ.get('DEBUG', True)
PORT = int(os.environ.get('PORT', 5000))
SECRET_KEY = os.environ.get('SECRET_KEY', 'foo')
HOST = os.environ.get('HOST', '0.0.0.0')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
AUTH_KEY = os.environ.get('AUTH_KEY', 'secret')
