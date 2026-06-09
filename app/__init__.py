from flask import Flask
from config import Config
from app.database import db, bcrypt, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar Extensões
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Registro de Blueprints (Controllers)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.ai_controller import ai_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ai_bp)

    # Contexto do banco para criação das tabelas no SQLite (MVP)
    with app.app_context():
        db.create_all()

    return app