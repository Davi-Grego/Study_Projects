from app.db import db

class Earnings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def _init_(self, description, amount,date, type, source, user_id):
        self.description = description
        self.amount = amount
        self.date = date
        self.source  = source
        self.user_id = user_id
        self.type = type
