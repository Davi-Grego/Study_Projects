from datetime import datetime
from app import db


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    installment = db.Column(db.Integer, default=1)
    total_installments = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Expense {self.description} - {self.amount}>"