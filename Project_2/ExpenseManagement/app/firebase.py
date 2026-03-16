from functools import wraps
import firebase_admin
from firebase_admin import credentials, auth
from flask import request, jsonify, session, redirect, url_for, flash


def init_firebase(app):
    if not firebase_admin._apps:
        cred = credentials.Certificate(app.config['FIREBASE_JSON_PATH'])
        firebase_admin.initialize_app(cred)


def verify_token(id_token: str) -> dict | None:
    """
    Verifica um ID Token vindo do frontend (login social).
    Retorna os dados do usuário ou None se inválido.
    """
    try:
        return auth.verify_id_token(id_token)
    except Exception:
        return None


def token_required(f):
    """
    Decorator para rotas de API que esperam
    Authorization: Bearer <TOKEN> no header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"message": "Token ausente!"}), 401

        try:
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
        except Exception as e:
            return jsonify({"message": "Token inválido!", "error": str(e)}), 401

        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    """
    Para rotas de PÁGINA (SSR).
    Redireciona para /auth/login se não houver sessão ativa.
    Injeta user_id como primeiro argumento da view.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(session['user_id'], *args, **kwargs)
    return wrapper


def api_login_required(f):
    """
    Para rotas de API (JSON).
    Retorna 401 JSON se não houver sessão ativa — nunca redireciona,
    pois redirecionar quebraria o fetch() do JavaScript.
    Injeta user_id como primeiro argumento da view.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Não autenticado.", "code": "UNAUTHENTICATED"}), 401
        return f(session['user_id'], *args, **kwargs)
    return wrapper