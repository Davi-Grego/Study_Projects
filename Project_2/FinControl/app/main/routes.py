from app.firebase import login_required
from app.reports.services import ReportService
from flask import Blueprint, render_template, redirect, url_for
from datetime import date

main_bp = Blueprint('main', __name__, template_folder='templates/main')

@main_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard(user_id):
    today = date.today()
    return render_template('dashboard.html',
        current_year=today.year,
        current_month=today.month,
    )