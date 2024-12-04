from app.db import db
from app.models import User

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    expense_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    def __init__(self, description, amount, expense_date, category, expense_type, user_id):
        self.description = description
        self.amount = amount
        self.expense_date = expense_date
        self.category = category
        self.expense_type = expense_type
        self.user_id = user_id
        

    
        


