from flask import Blueprint

# Importando as rotas de cada módulo
from .auth_routes import auth_bp
from .expenses_routes import expense_bp
from .earnings_routes import earnings_bp


# Função que registra os Blueprints no aplicativo Flask
def init_app(app):
    # Registrando os Blueprints com um prefixo de URL
    app.register_blueprint(auth_bp)#url_prefix='/auth')    # Prefixo /auth para rotas de autenticação
    app.register_blueprint(expense_bp)
    app.register_blueprint(earnings_bp)