from app.extensions import db
from app.models import Expense
from datetime import date
from sqlalchemy import extract


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
    def get_paid_by_month(user_id: int, year: int, month: int) -> list[Expense]:
        """Movimentações pagas de um mês — para saldo real."""
        return (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                Expense.status  == 'paid',
                extract('year',  Expense.date) == year,
                extract('month', Expense.date) == month,
            )
            .all()
        )

    @staticmethod
    def get_active_by_month(user_id: int, year: int, month: int) -> list[Expense]:
        """Movimentações paid + pending de um mês — para saldo estimado."""
        return (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                Expense.status  != 'cancelled',
                extract('year',  Expense.date) == year,
                extract('month', Expense.date) == month,
            )
            .all()
        )

    @staticmethod
    def get_paid_before_month(user_id: int, year: int, month: int) -> list[Expense]:
        """
        Todas as movimentações pagas de meses anteriores ao informado.
        Usada para calcular o saldo acumulado.
        """
        return (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                Expense.status  == 'paid',
                db.or_(
                    extract('year', Expense.date) < year,
                    db.and_(
                        extract('year',  Expense.date) == year,
                        extract('month', Expense.date) <  month,
                    )
                )
            )
            .all()
        )

    @staticmethod
    def get_paid_all(user_id: int) -> list[Expense]:
        """Todas as movimentações pagas — para saldo real total."""
        return (
            Expense.query
            .filter_by(user_id=user_id, status='paid')
            .all()
        )

    @staticmethod
    def get_active_all(user_id: int) -> list[Expense]:
        """Todas as movimentações não canceladas — para saldo estimado total."""
        return (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                Expense.status  != 'cancelled',
            )
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
        # quebra a auto-referência antes de deletar
        for expense in expenses:
            expense.parent_id = None
        db.session.flush()  # persiste os NULLs sem commitar ainda

        for expense in expenses:
            db.session.delete(expense)
        db.session.commit()