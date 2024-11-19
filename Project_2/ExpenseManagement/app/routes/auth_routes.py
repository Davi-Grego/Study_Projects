from flask import Blueprint, request, jsonify, redirect, url_for
from app.models.user import User, db
from flask_login import login_user, login_required, logout_user, current_user


# Criando o Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

    # Verifica se o usuário já existe
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email já cadastrado'}), 400

    # Cria o novo usuário
    novo_usuario = User(nome=nome, email=email, senha=senha)

    # Adiciona ao banco de dados
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário criado com sucesso!'}), 201


# Rota para listar todos os usuários
@auth_bp.route('/users', methods=['GET'])
def get_users():
    usuarios = User.query.all()
    usuarios_list = [usuario.to_dict() for usuario in usuarios]
    return jsonify(usuarios_list), 200 

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    # Verifica se o email e senha foram fornecidos
    if not email or not senha:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400

    # Encontra o usuário pelo email
    usuario = User.query.filter_by(email=email).first()

    if usuario and usuario.check_password(senha):
        # Autentica o usuário
        login_user(usuario)
        return jsonify({'message': 'Login bem-sucedido!'}), 200
        return redirect("/area_logada")
    else:
        return jsonify({'message': 'Email ou senha inválidos'}), 401

# Rota para logout
@auth_bp.route('/logout', methods=['GET'])
@login_required  # Garante que o usuário esteja logado
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso!'}), 200
