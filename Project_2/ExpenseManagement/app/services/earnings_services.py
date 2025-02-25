from app.models.earnings import Earnings
from app.db import db
from datetime import datetime
from sqlalchemy import extract

class EarningsServices:
    @staticmethod
    def add_new_earnings(description, amount, date, type, source,user_id):
        try:
            earning = Earnings(
                description = description,
                amount = amount,
                date = date,
                type = type,
                source = source,
                user_id = user_id,
            )

            db.session.add(earning)
            db.session.commit()
        except Exception as e:
            db.session.rollback() 
            print(f"Erro ao adicionar receita: {e}")

    @staticmethod
    def get_earnings(user_id):
        return Earnings.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_total_amount(user_id):
        today = datetime.today()
        earnings = EarningsServices.get_earnings(user_id)
        total_amount = sum(
            earning.amount for earning in earnings
            if earning.date.month == today.month and earning.date.year == today.year
        )
        return "{:.2f}".format(total_amount).replace('.', ',')
    
    @staticmethod
    def get_user_months(user_id):
        meses = Earnings.query.with_entities(
            extract('year', Earnings.date), extract('month', Earnings.date)
        ).filter_by(user_id=user_id).distinct().all()
        return {f"{ano}-{str(mes).zfill(2)}" for ano, mes in meses}

    @staticmethod
    def get_earnings_by_month(user_id, mes):
        ano, mes = map(int, mes.split('-'))
        return Earnings.query.filter_by(user_id=user_id).filter(
            extract('year', Earnings.date) == ano,
            extract('month', Earnings.date) == mes
        ).all()