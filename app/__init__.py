from flask import Flask
from config import Config
from app.database import db, bcrypt, login_manager
from flask_mail import Mail

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config.setdefault('MAIL_SERVER', 'smtp.gmail.com')
    app.config.setdefault('MAIL_PORT', 587)
    app.config.setdefault('MAIL_USE_TLS', True)
    app.config.setdefault('MAIL_USERNAME', 'seu_email@provedor.com')
    app.config.setdefault('MAIL_PASSWORD', 'sua_app_password')
    app.config.setdefault('MAIL_DEFAULT_SENDER', ('LombongoCare', 'seu_email@provedor.com'))

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.ai_controller import ai_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ai_bp)

    with app.app_context():
        db.create_all()

    return app