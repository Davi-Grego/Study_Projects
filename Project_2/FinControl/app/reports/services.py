from datetime import date
from sqlalchemy import extract, func

from app.extensions import db
from app.models import Expense, Category


class ReportService:

    # ── Por mês ───────────────────────────────────────────────────────────────

    @staticmethod
    def monthly_summary(user_id: int, year: int, month: int) -> dict:
        """
        Resumo completo de um mês: totais, saldo e breakdown por categoria.
        RF012 — relatório por mês.
        """
        expenses = (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                extract('year',  Expense.date) == year,
                extract('month', Expense.date) == month,
            )
            .all()
        )

        income  = sum(e.amount for e in expenses if e.type == 'income')
        outcome = sum(e.amount for e in expenses if e.type == 'expense')

        return {
            'year':              year,
            'month':             month,
            'income':            round(income, 2),
            'outcome':           round(outcome, 2),
            'balance':           round(income - outcome, 2),
            'by_category':       ReportService._group_by_category(expenses),
            'by_payment_type':   ReportService._group_by_payment_type(expenses),
            'transactions':      [e.to_dict() for e in expenses],
        }

    # ── Por ano ───────────────────────────────────────────────────────────────

    @staticmethod
    def yearly_summary(user_id: int, year: int) -> dict:
        """
        Resumo anual com breakdown mês a mês.
        RF012 — relatório por ano.
        """
        expenses = (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                extract('year', Expense.date) == year,
            )
            .all()
        )

        income  = sum(e.amount for e in expenses if e.type == 'income')
        outcome = sum(e.amount for e in expenses if e.type == 'expense')

        # agrupa por mês para o gráfico de linha — RF013
        months_data = {}
        for e in expenses:
            m = e.date.month
            if m not in months_data:
                months_data[m] = {'month': m, 'income': 0.0, 'outcome': 0.0}
            if e.type == 'income':
                months_data[m]['income']  = round(months_data[m]['income']  + e.amount, 2)
            else:
                months_data[m]['outcome'] = round(months_data[m]['outcome'] + e.amount, 2)

        # garante todos os 12 meses mesmo os sem movimentação
        monthly_breakdown = []
        for m in range(1, 13):
            entry = months_data.get(m, {'month': m, 'income': 0.0, 'outcome': 0.0})
            entry['balance'] = round(entry['income'] - entry['outcome'], 2)
            monthly_breakdown.append(entry)

        return {
            'year':             year,
            'income':           round(income, 2),
            'outcome':          round(outcome, 2),
            'balance':          round(income - outcome, 2),
            'monthly_breakdown': monthly_breakdown,
            'by_category':      ReportService._group_by_category(expenses),
            'by_payment_type':  ReportService._group_by_payment_type(expenses),
        }

    # ── Por período personalizado ─────────────────────────────────────────────

    @staticmethod
    def period_summary(user_id: int, start: date, end: date) -> dict:
        """
        Resumo de um período personalizado.
        RF012 — relatório por período / RF014 — filtro por período.
        """
        expenses = (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                Expense.date >= start,
                Expense.date <= end,
            )
            .order_by(Expense.date.asc())
            .all()
        )

        income  = sum(e.amount for e in expenses if e.type == 'income')
        outcome = sum(e.amount for e in expenses if e.type == 'expense')

        return {
            'start':           start.isoformat(),
            'end':             end.isoformat(),
            'income':          round(income, 2),
            'outcome':         round(outcome, 2),
            'balance':         round(income - outcome, 2),
            'by_category':     ReportService._group_by_category(expenses),
            'by_payment_type': ReportService._group_by_payment_type(expenses),
            'transactions':    [e.to_dict() for e in expenses],
        }

    # ── Por categoria ─────────────────────────────────────────────────────────

    @staticmethod
    def category_summary(user_id: int, year: int, month: int | None = None) -> list[dict]:
        """
        Breakdown de gastos por categoria.
        RF012 — relatório por categoria.
        """
        query = (
            Expense.query
            .filter(
                Expense.user_id == user_id,
                Expense.type == 'expense',
                extract('year', Expense.date) == year,
            )
        )
        if month:
            query = query.filter(extract('month', Expense.date) == month)

        expenses = query.all()
        return ReportService._group_by_category(expenses)

    # ── Helpers de agregação ──────────────────────────────────────────────────

    @staticmethod
    def _group_by_category(expenses: list[Expense]) -> list[dict]:
        """
        Agrupa saídas por categoria.
        Retorna lista ordenada do maior para o menor gasto — útil para gráfico de pizza.
        RF013.
        """
        groups: dict[str, dict] = {}

        for e in expenses:
            if e.type != 'expense':
                continue

            # categoria pode ser None se não foi definida
            cat_id   = e.category_id or 0
            cat_name = e.category.name if e.category else 'Sem categoria'

            if cat_id not in groups:
                groups[cat_id] = {
                    'category_id':   cat_id or None,
                    'category_name': cat_name,
                    'total':         0.0,
                    'count':         0,
                }

            groups[cat_id]['total'] = round(groups[cat_id]['total'] + e.amount, 2)
            groups[cat_id]['count'] += 1

        return sorted(groups.values(), key=lambda x: x['total'], reverse=True)

    @staticmethod
    def _group_by_payment_type(expenses: list[Expense]) -> dict:
        """
        Agrupa por forma de pagamento.
        RF012 — relatório por forma de pagamento.
        """
        groups = {
            'single':      {'label': 'À vista',    'total': 0.0, 'count': 0},
            'installment': {'label': 'Parcelado',   'total': 0.0, 'count': 0},
            'recurring':   {'label': 'Recorrente',  'total': 0.0, 'count': 0},
        }

        for e in expenses:
            if e.type != 'expense':
                continue
            pt = e.payment_type or 'single'
            if pt in groups:
                groups[pt]['total'] = round(groups[pt]['total'] + e.amount, 2)
                groups[pt]['count'] += 1

        return groups