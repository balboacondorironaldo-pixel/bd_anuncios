import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_tablon'
    # Base de datos SQLite local (puedes cambiarla a MySQL si prefieres)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///bd_anuncios.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False