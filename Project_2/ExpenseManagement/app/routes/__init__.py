from flask import Blueprint

# Importando as rotas de cada módulo
from .auth_routes import auth_bp


# Função que registra os Blueprints no aplicativo Flask
def init_app(app):
    # Registrando os Blueprints com um prefixo de URL
    app.register_blueprint(auth_bp)#url_prefix='/auth')    # Prefixo /auth para rotas de autenticação

