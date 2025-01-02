from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, current_user

from app.models.earnings import Earnings
from app.services.earnings_services import EarningsServices

from datetime import datetime

earnings_bp  = Blueprint('earningRoute', __name__)

@earnings_bp.route('/addEarning', methods=['POST'])
def AddEarning():
    description =  request.form.get('description')
    amount = request.form.get('amount')
    source = request.form.get('source')
    type = request.form.get('type')
    date = request.form.get('date')
    date = datetime.strptime(date, '%Y-%m-%d')
    user_id = current_user.id

    EarningsServices.add_new_earnings(description, amount, date, type, source,user_id)
    return redirect('/dash')


    
