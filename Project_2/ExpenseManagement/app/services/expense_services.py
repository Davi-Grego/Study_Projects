from app.db import db
from app.models.expenses import Expense
from datetime import datetime
from sqlalchemy import extract


class ExpenseServices:

    @staticmethod
    def add_new_expense(description, amont, date, category, type, user_id):
        try:
            print(type)
            expense = Expense(
                description=description,
                amount=amont,
                date=date,
                category=category,
                type=type,
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
        today = datetime.today()
        expenses = ExpenseServices.get_expenses(user_id)
        total_amount = sum(
            expense.amount for expense in expenses
            if expense.date.month == today.month and expense.date.year == today.year
        )
        return "{:.2f}".format(total_amount).replace('.', ',')
    
    
    
    @staticmethod
    def get_last_expenses(user_id,limit=2):
        return (
            Expense.query.filter_by(user_id=user_id)
            .order_by(Expense.date.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_user_months(user_id):
        # Retorna um set de meses disponíveis (ex: {'2025-01', '2025-02'})
        meses = Expense.query.with_entities(
            extract('year', Expense.date), extract('month', Expense.date)
        ).filter_by(user_id=user_id).distinct().all()
        return {f"{ano}-{str(mes).zfill(2)}" for ano, mes in meses}

    @staticmethod
    def get_expenses_by_month(user_id, mes):
        ano, mes = map(int, mes.split('-'))
        return Expense.query.filter_by(user_id=user_id).filter(
            extract('year', Expense.date) == ano,
            extract('month', Expense.date) == mes
        ).all()