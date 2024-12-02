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
        senha = request.form.get('password')

        # Buscar o usuário pelo e-mail
        try:
            user = User.query.filter_by(email=email).first()
            print("USER ENCONTRADO")
        except:
            flash('Usuário não encontrado. Por favor, registre-se.', 'danger')
            return redirect("/registrar")      

        if user and user.verify_password(senha):
            flash('Login bem-sucedido!', 'success')
            return redirect('/aaaaaaaa')  # Redireciona para a página de perfil
        else:
            print("algo deu errado")
            
    return render_template('login.html')

@auth_bp.route('/registrar', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        user = User(name, email, password)
        User.addNewUser(user)
        return redirect ("/login")

    return render_template('register.html')