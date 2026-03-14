from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import db, migrate
from app.firebase import init_firebase

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializa Extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from app.models import User
        db.create_all() 
        init_firebase(app)    
    

    # 3. Registro de Blueprints (Sua estrutura modular) 
    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp)


    return app