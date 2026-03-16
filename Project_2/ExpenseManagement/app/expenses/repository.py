from app.extensions import db
from app.models import Expense
from datetime import date


class ExpenseRepository:

    @staticmethod
    def get_by_id(expense_id: int, user_id: int) -> Expense | None:
        """Busca uma despesa pelo ID garantindo que pertence ao usuário. RN001."""
        return Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    @staticmethod
    def get_all_by_user(user_id: int) -> list[Expense]:
        return (
            Expense.query
            .filter_by(user_id=user_id)
            .order_by(Expense.date.desc())
            .all()
        )

    @staticmethod
    def get_by_period(user_id: int, start: date, end: date) -> list[Expense]:
        """Filtra por período personalizado. RF014."""
        return (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                Expense.date >= start,
                Expense.date <= end,
            )
            .order_by(Expense.date.desc())
            .all()
        )

    @staticmethod
    def get_by_month(user_id: int, year: int, month: int) -> list[Expense]:
        """Movimentações de um mês específico. RF012 / RN002."""
        from sqlalchemy import extract
        return (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                extract('year',  Expense.date) == year,
                extract('month', Expense.date) == month,
            )
            .order_by(Expense.date.desc())
            .all()
        )

    @staticmethod
    def get_by_category(user_id: int, category_id: int) -> list[Expense]:
        """Filtra por categoria. RF012."""
        return (
            Expense.query
            .filter_by(user_id=user_id, category_id=category_id)
            .order_by(Expense.date.desc())
            .all()
        )

    @staticmethod
    def get_children(parent_id: int) -> list[Expense]:
        """Retorna todas as parcelas/recorrências filhas de uma entrada."""
        return Expense.query.filter_by(parent_id=parent_id).all()

    @staticmethod
    def save(expense: Expense) -> Expense:
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def save_many(expenses: list[Expense]) -> list[Expense]:
        db.session.add_all(expenses)
        db.session.commit()
        return expenses

    @staticmethod
    def delete(expense: Expense) -> None:
        db.session.delete(expense)
        db.session.commit()

    @staticmethod
    def delete_many(expenses: list[Expense]) -> None:
        for expense in expenses:
            db.session.delete(expense)
        db.session.commit()