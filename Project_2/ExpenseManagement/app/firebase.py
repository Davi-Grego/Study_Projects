from functools import wraps
import firebase_admin
from firebase_admin import credentials, auth
from flask import request, jsonify, session


def init_firebase(app):
    if not firebase_admin._apps:  # evita inicializar duas vezes (ex: hot reload)
        cred = credentials.Certificate(app.config['FIREBASE_JSON_PATH'])
        firebase_admin.initialize_app(cred)


def verify_token(id_token: str) -> dict | None:
    """
    Verifica um ID Token vindo do frontend (login social).
    Retorna os dados do usuário ou None se inválido.
    """
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception:
        return None


def token_required(f):
    """
    Decorator para rotas protegidas que esperam
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
    Decorator para rotas de página (HTML) que exigem sessão Flask ativa.
    Redireciona para login se não houver sessão.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            from flask import redirect, url_for
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function