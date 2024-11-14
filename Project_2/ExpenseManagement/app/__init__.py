from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # Importando o Flask-Bcrypt
from flask_login import LoginManager  # Importando o Flask-Login
from app.config import Config



db = SQLAlchemy()

migrate = Migrate()

bcrypt = Bcrypt()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app