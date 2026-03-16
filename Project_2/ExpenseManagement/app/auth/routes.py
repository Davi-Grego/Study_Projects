from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from flask import session
from app.models import user
from app.firebase import login_required,verify_token
from app.auth.services import AuthService
from flask import request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates/auth')


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login')
def login():  # Exemplo de uso do método get_user_name
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@login_required
@auth_bp.route('/logout')
def logout():
    from flask import session
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route("/firebase-callback", methods=["POST"])
def firebase_callback():
    data = request.get_json()
    decoded = verify_token(data.get("idToken"))

    if not decoded:
        return jsonify({"error": "Token inválido"}), 401

    user, created = AuthService.get_or_create_user(decoded)

    session["user_id"] = user.id        # ID do banco, não o uid do Firebase
    session["email"]   = user.email
    session["name"]    = user.name or ""

    return jsonify({"status": "ok", "new_user": created})