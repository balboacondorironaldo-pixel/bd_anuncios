from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar Blueprints de tus carpetas
    from app.auth.routes import auth_bp
    from app.usuarios.routes import usuarios_bp
    from app.categorias.routes import categorias_bp
    from app.anuncios.routes import anuncios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(anuncios_bp, url_prefix='/anuncios')

    return app