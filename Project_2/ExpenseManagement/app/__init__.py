from flask import Flask, render_template
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # Importando o Flask-Bcrypt
from flask_login import LoginManager  # Importando o Flask-Login
from flask_bootstrap import Bootstrap4
from app.config import Config
from .routes import init_app
from .db import db
from .models import User



migrate = Migrate()

bcrypt = Bcrypt()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap4(app)

    login_manager.init_app(app)
    login_manager.login_view = '/login'  # Ajuste para o nome correto da rota de login
    login_manager.login_message = "Por favor, faça login para acessar esta página."

    @login_manager.user_loader
    def load_user(id):
        print(User.query.get(int(id)))
        return User.query.get(int(id))

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    init_app(app)

    return app