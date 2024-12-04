from flask import current_app
from werkzeug.security import generate_password_hash
from app.db import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    
    # Definindo os campos do modelo
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Construtor da classe 
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.set_password(senha)  # Chama o método para criptografar a senha
    
    # Método para criptografar a senha
    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)
    