from app.db import db
from app.models.expenses import Expense

class ExpenseService:

    @staticmethod
    def add_new_expense(expense):
        db.session.add(expense)
        db.session.commit()

    @staticmethod
    def del_expense(expense_id):
        expense = Expense.query.filter_by(id=expense_id).first()
        db.session.delete(expense)


    @staticmethod
    def get_exepenses(user_id):
        return Expense.query.filter_by(user_id=user_id).all()
    
        

