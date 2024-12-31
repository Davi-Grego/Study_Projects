from app.models.earnings import Earnings
from app.db import db

class EarningsServices:

    @staticmethod
    def add_new_earnings(description, amount, date, source,user_id):
        try:
            earning = Earnings(
                description = description,
                amount = amount,
                date = date ,
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
        earnings = EarningsServices.get_earnings(user_id)
        total_amount = sum(earning.amount for earning in earnings)
        total_amount = "{:.2f}".format(total_amount).replace('.', ',')
        return total_amount
