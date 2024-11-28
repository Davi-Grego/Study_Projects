from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models import User



# Criando o Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    ...
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Buscar o usuário pelo e-mail
        try:
            user = User.query.filter_by(email=email).first()
        except:
            return redirect('/registrar')

        if user and user.verify_password(senha):
            # Autenticação bem-sucedida
            # Salvar informações do usuário na sessão (exemplo com flask-login)
            # Aqui você poderia usar o Flask-Login para gerenciar sessões de usuários

            # Exemplo básico de como você pode fazer isso:
            # session['user_id'] = user.id  # Isso é apenas um exemplo

            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('user.profile'))  # Redireciona para a página de perfil

        else:
            flash('E-mail ou senha incorretos. Tente novamente.', 'danger')
            return render_template('login.html', error='E-mail ou senha incorretos.')

    return render_template('login.html')

@auth_bp.route('/registrar')
def registrar():
    return render_template('register.html')