from app.db import db
from app.models.expenses import Expense

class ExpenseService:

    @staticmethod
    def add_new_expense(exepense):
        db.session.add(exepense)
        db.session.commit()
        db.session.refresh()

    @staticmethod
    def get_exepenses(user_id):
        return Expense.query.filter_by(user_id=user_id).all()
    
        

