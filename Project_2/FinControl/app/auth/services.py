from app.models.user import User
from app.extensions import db

class AuthService:
    @staticmethod
    def get_or_create_user(decoded_token: dict) -> tuple[User, bool]:
        """
        Retorna (user, created) — created=True se foi o primeiro login.
        Útil para redirecionar para onboarding futuramente.
        """
        uid = decoded_token['uid']
        email = decoded_token.get('email')
        name = decoded_token.get('name')

        user = User.query.filter_by(firebase_uid=uid).first()
        
        if user:
            return user, False

        user = User(firebase_uid=uid, email=email, name=name)
        db.session.add(user)
        db.session.commit()
            
        return user, True