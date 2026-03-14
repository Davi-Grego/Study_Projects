from flask import Blueprint, render_template, session
from app.models.user import get_user_name
from app.auth.routes import login_required

bp = Blueprint('main', __name__, template_folder='templates/main')


@bp.route('/')
@login_required
def index():

    user_name = get_user_name(session.get('user_id'))  # Exemplo de uso do método get_user_name
    return render_template('index.html', user_name=user_name)    