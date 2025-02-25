from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, current_user

from app.models.expenses import Expense
from app.services import ExpenseServices,EarningsServices,Utils
from datetime import datetime

expense_bp = Blueprint('expenseRoute', __name__)

@expense_bp.route('/')
def index():
    if current_user.is_authenticated:
        last_expenses = ExpenseServices.get_last_expenses(current_user.id, limit=2)
        return render_template('index.html', last_expenses=last_expenses)
    else:
        return render_template('index.html')
    
@expense_bp.route('/history', methods=['GET','POST'])
@login_required
def history():
    cat_expenses_list = Utils.get_expenses_by_category("2025-02")
    
    return render_template(
        'history.html',
        expenses=cat_expenses_list
        )


@expense_bp.route('/dash', methods=['GET', 'POST'])
@login_required
def dash():
    user_transactions = Utils.get_user_transactions(current_user.id)
    expenses = user_transactions['expenses']
    earnings = user_transactions['earnings']
    transactions = user_transactions['transactions']

    # Pega o mês e o ano atual
    today = datetime.today()
    month_transactions = [t for t in transactions if t["date"].month == today.month and t["date"].year == today.year]

    return render_template(
        'dash.html', 
        expenses=expenses, 
        earnings=earnings, 
        all_transactions=transactions, 
        transactions=month_transactions  # Adicionando transações do mês
    )


@expense_bp.route('/addExpense', methods=['GET','POST'])
def AddExpense():
    if request.method == 'POST':
        description = request.form.get("description")
        amont = request.form.get("amont")
        inputDate = request.form.get("date")
        date = datetime.strptime(inputDate, '%Y-%m-%d')
        category = request.form.get("category")
        type = request.form.get("type")
        user_id = current_user.id

        print("eu sou o jorge",type)
        ExpenseServices.add_new_expense(description, amont, date, category, type, user_id)
        return redirect('/dash')