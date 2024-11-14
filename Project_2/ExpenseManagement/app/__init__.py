from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # Importando o Flask-Bcrypt
from flask_login import LoginManager  # Importando o Flask-Login
from app.config import Config
from app.routes.auth_routes import auth_bp

# Inicializa o banco de dados
db = SQLAlchemy()

# Inicializa o Flask-Migrate
migrate = Migrate()

# Inicializa o Flask-Bcrypt
bcrypt = Bcrypt()

# Inicializa o Flask-Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa o banco de dados com a aplicação
    db.init_app(app)

    # Inicializa o Flask-Migrate com a aplicação e o banco de dados
    migrate.init_app(app, db)

    # Inicializa o Flask-Bcrypt e Flask-Login com a aplicação
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Definir o endpoint de login
    login_manager.login_view = "auth.login"

    # Registra o Blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
