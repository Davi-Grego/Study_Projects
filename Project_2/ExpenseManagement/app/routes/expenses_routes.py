from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, current_user

from app.models.expenses import Expense
from app.services.expense_services import ExpenseServices
from datetime import datetime

expense_bp = Blueprint('expenseRoute', __name__)

@expense_bp.route('/')
def index():
    if current_user.is_authenticated:
        last_expenses = ExpenseServices.get_last_expenses(current_user.id, limit=2)
        return render_template('index.html', last_expenses=last_expenses)
    else:
        return render_template('index.html')


@expense_bp.route('/dash', methods=['GET', 'POST'])
@login_required
def dash():
    last_expenses = ExpenseServices.get_last_expenses(current_user.id, limit=100)
    return render_template('dash.html', last_expenses=last_expenses)


@expense_bp.route('/addExpense', methods=['GET','POST'])
def AddExpense():
    if request.method == 'POST':
        description = request.form.get("description")
        amont = request.form.get("amont")
        inputDate = request.form.get("date_expense")
        expense_date = datetime.strptime(inputDate, '%Y-%m-%d')
        category = request.form.get("category")
        expense_type = request.form.get("type")
        user_id = current_user.id

        
        ExpenseServices.add_new_expense(description, amont, expense_date, category, expense_type, user_id)
        return redirect('/dash')