from app.models.earnings import Earnings
from app.models.expenses import Expense

from .earnings_services import EarningsServices
from .expense_services import ExpenseServices


class Utils:
    def calculate_balance(user_id):
        expenses = Expense.query.filter_by(user_id=user_id).all()
        earnings = Earnings.query.filter_by(user_id=user_id).all()
        total_expenses = sum(expense.amount for expense in expenses)
        total_earnings = sum(earning.amount for earning in earnings)
        balance = total_earnings - total_expenses
        return "{:.2f}".format(balance).replace('.', ',')