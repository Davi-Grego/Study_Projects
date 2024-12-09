from werkzeug.security import check_password_hash
from app.db import db
from app.models.user import User

class UserService:

    @staticmethod
    def verify_password(user, senha):
        senha_hash = user.senha_hash
        if not senha_hash:
            return False  
        if check_password_hash(senha_hash, senha):
            return True
        else:
            return False
        
    @staticmethod
    def addNewUser(new_user):
        db.session.add(new_user)
        db.session.commit()


    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    # Método de conversão para dicionário 
    @staticmethod
    def to_dict(user):
        return {
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "data_criacao": user.data_criacao
        }
