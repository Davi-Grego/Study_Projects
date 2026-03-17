from flask import Flask, app
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
        from app.models import User, Expense, Goal, Category
        db.create_all() 
        init_firebase(app) 
        
        from app.categories.services import CategoryService
        CategoryService.seed_defaults()

    # 3. Registro de Blueprints (Sua estrutura modular) 
    from app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.expenses.routes import expenses_bp
    app.register_blueprint(expenses_bp)

    from app.categories.routes import categories_bp
    app.register_blueprint(categories_bp)

    from app.goals.routes import goals_bp
    app.register_blueprint(goals_bp)
    
    from app.reports.routes import reports_bp
    app.register_blueprint(reports_bp)
    
    return app