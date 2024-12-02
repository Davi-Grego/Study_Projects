from flask import Flask, render_template
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # Importando o Flask-Bcrypt
from flask_login import LoginManager  # Importando o Flask-Login
from flask_bootstrap import Bootstrap4
from app.config import Config
from .routes import init_app
from .db import db




migrate = Migrate()

bcrypt = Bcrypt()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap4(app)

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    init_app(app)

    return app