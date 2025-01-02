from app.models.earnings import Earnings
from app.models.expenses import Expense

from sqlalchemy import desc, func
from datetime import datetime, date


from .earnings_services import EarningsServices
from .expense_services import ExpenseServices


class Utils:
    def calculate_balance(user_id):
        total_expenses = (
            Expense.query.with_entities(func.sum(Expense.amount))
            .filter_by(user_id=user_id)
            .scalar()
            or 0
        )
        total_earnings = (
            Earnings.query.with_entities(func.sum(Earnings.amount))
            .filter_by(user_id=user_id)
            .scalar()
            or 0
        )
        balance = total_earnings - total_expenses

        return "{:.2f}".format(balance).replace(".", ",")

    def get_user_transactions(user_id):
        expenses = Expense.query.filter_by(user_id=user_id).all()
        earnings = Earnings.query.filter_by(user_id=user_id).all()

        transactions = [
            {
                "description": expense.description,
                "amount": -expense.amount,
                "date": (
                    expense.date.date()
                    if isinstance(expense.date, datetime)
                    else expense.date
                ),  # Convert datetime to date
                "category": expense.category,
                "type": "Expense",
            }
            for expense in expenses
        ] + [
            {
                "description": earning.description,
                "amount": earning.amount,
                "date": (
                    earning.date.date()
                    if isinstance(earning.date, datetime)
                    else earning.date
                ),  # Convert datetime to date
                "type": "Earning",
            }
            for earning in earnings
        ]

        transactions.sort(key=lambda x: x["date"], reverse=True)  # Sorting by date

        return {
            "transactions": transactions,
            "earnings": earnings,
            "expenses": expenses,
        }
