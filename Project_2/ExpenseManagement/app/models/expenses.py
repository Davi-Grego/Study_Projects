from app.db import db
from app.models import User

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    def __init__(self, description, amount, date, category, type, user_id):
        self.description = description
        self.amount = amount
        self.date = date
        self.category = category
        self.type = type
        self.user_id = user_id
        

    
        


