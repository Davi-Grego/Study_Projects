from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(100), nullable=False)
    icon    = db.Column(db.String(50), nullable=True)    # ex: 'cart', 'home', 'car'

    # user_id NULL = categoria global do sistema (padrão para todos)
    # user_id preenchido = categoria criada pelo próprio usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    expenses = db.relationship('Expense', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id':      self.id,
            'name':    self.name,
            'icon':    self.icon,
            'user_id': self.user_id,
            'is_global': self.user_id is None,
        }