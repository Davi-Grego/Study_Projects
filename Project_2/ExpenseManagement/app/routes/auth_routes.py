from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.services.user_services import UserServices



# Criando o Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')

        # Buscar o usuário pelo e-mail
        try:
            user = UserServices.get_user_by_email(email)
            print("USER ENCONTRADO")
        except:
            flash('Usuário não encontrado. Por favor, registre-se.', 'danger')
            return redirect("/registrar")      

        if user and UserServices.verify_password(user, senha):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect('/')
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
        UserServices.addNewUser(user)
        return redirect ("/login")

    return render_template('register.html')