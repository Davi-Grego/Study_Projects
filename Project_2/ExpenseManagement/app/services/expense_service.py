from app.db import db
from app.models.expenses import Expense

class ExpenseService:

    @staticmethod
    def add_new_expense(description, amont, expense_date, category, expense_type, user_id):
        try:
            expense = Expense(
                description=description,
                amount=amont,
                expense_date=expense_date,
                category=category,
                expense_type=expense_type,
                user_id=user_id
            )

            db.session.add(expense)
            db.session.commit()
        except Exception as e:
            db.session.rollback() 
            print(f"Erro ao adicionar despesa: {e}")

    @staticmethod
    def del_expense(expense_id):
        expense = Expense.query.filter_by(id=expense_id).first()
        db.session.delete(expense)


    
    def get_expenses(user_id):
        return Expense.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_total_amount(user_id):
        expenses = ExpenseService.get_expenses(user_id)
        total_amount = sum(expense.amount for expense in expenses)

        return total_amount

