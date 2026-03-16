from datetime import date
from dateutil.relativedelta import relativedelta

from app.models import Expense
from app.expenses.repository import ExpenseRepository
from app.goals.services import GoalService


class ExpenseService:

    # ── Criação ──────────────────────────────────────────────────────────────

    @staticmethod
    def create(user_id: int, data: dict) -> list[Expense]:
        """
        Cria uma ou mais entradas dependendo do payment_type.
        Retorna lista com todos os registros criados.
        """
        payment_type = data.get('payment_type', 'single')

        if payment_type == 'installment':
            return ExpenseService._create_installments(user_id, data)

        if payment_type == 'recurring':
            return ExpenseService._create_recurring(user_id, data)

        # pagamento simples
        expense = Expense(
            user_id=user_id,
            description=data['description'],
            amount=data['amount'],
            date=data['date'],
            type=data['type'],
            payment_type='single',
            installment_number=1,
            total_installments=1,
            category_id=data.get('category_id'),
        )
        saved = ExpenseRepository.save(expense)

        # verifica impacto na meta — RF016
        if saved.type == 'expense':
            GoalService.check_goal_impact(user_id, saved.amount)

        return [saved]

    @staticmethod
    def _create_installments(user_id: int, data: dict) -> list[Expense]:
        """
        Gera N registros, um por parcela, cada um com a data do mês correspondente.
        RN002 — cada parcela impacta apenas o seu mês.
        """
        total = data['total_installments']
        base_date: date = data['date']
        installment_amount = round(data['amount'] / total, 2)

        expenses = []
        parent_id = None

        for i in range(total):
            installment_date = base_date + relativedelta(months=i)
            exp = Expense(
                user_id=user_id,
                description=f"{data['description']} ({i + 1}/{total})",
                amount=installment_amount,
                date=installment_date,
                type=data['type'],
                payment_type='installment',
                installment_number=i + 1,
                total_installments=total,
                category_id=data.get('category_id'),
                parent_id=parent_id,
            )
            expenses.append(exp)

        saved = ExpenseRepository.save_many(expenses)

        # define o parent_id da primeira como ela mesma para agrupar
        saved[0].parent_id = saved[0].id
        for s in saved[1:]:
            s.parent_id = saved[0].id
        ExpenseRepository.save_many(saved)

        # verifica impacto na meta com o valor total — RF016
        if data['type'] == 'expense':
            GoalService.check_goal_impact(user_id, data['amount'])

        return saved

    @staticmethod
    def _create_recurring(user_id: int, data: dict) -> list[Expense]:
        """
        Gera registros recorrentes até recurrence_end_date.
        Se não houver end_date, gera 12 meses à frente. RF010 / RN003.
        """
        recurrence_type    = data['recurrence_type']
        base_date: date    = data['date']
        end_date: date     = data.get('recurrence_end_date')

        delta_map = {
            'weekly':  relativedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'yearly':  relativedelta(years=1),
        }
        delta = delta_map[recurrence_type]

        # sem end_date → gera 12 ocorrências
        if not end_date:
            occurrences = 12
            dates = [base_date + delta * i for i in range(occurrences)]
        else:
            dates = []
            current = base_date
            while current <= end_date:
                dates.append(current)
                current += delta

        expenses = []
        for i, occurrence_date in enumerate(dates):
            exp = Expense(
                user_id=user_id,
                description=data['description'],
                amount=data['amount'],
                date=occurrence_date,
                type=data['type'],
                payment_type='recurring',
                installment_number=i + 1,
                total_installments=len(dates),
                is_recurring=True,
                recurrence_type=recurrence_type,
                recurrence_end_date=end_date,
                category_id=data.get('category_id'),
            )
            expenses.append(exp)

        saved = ExpenseRepository.save_many(expenses)

        # agrupa pelo id da primeira ocorrência
        saved[0].parent_id = saved[0].id
        for s in saved[1:]:
            s.parent_id = saved[0].id
        ExpenseRepository.save_many(saved)

        return saved

    # ── Leitura ───────────────────────────────────────────────────────────────

    @staticmethod
    def get_all(user_id: int) -> list[Expense]:
        return ExpenseRepository.get_all_by_user(user_id)

    @staticmethod
    def get_by_period(user_id: int, start: date, end: date) -> list[Expense]:
        return ExpenseRepository.get_by_period(user_id, start, end)

    @staticmethod
    def get_by_month(user_id: int, year: int, month: int) -> list[Expense]:
        return ExpenseRepository.get_by_month(user_id, year, month)

    # ── Edição ────────────────────────────────────────────────────────────────

    @staticmethod
    def update(user_id: int, expense_id: int, data: dict) -> Expense | None:
        """
        Edita apenas o registro individual — não propaga para parcelas irmãs.
        """
        expense = ExpenseRepository.get_by_id(expense_id, user_id)
        if not expense:
            return None

        for field, value in data.items():
            if hasattr(expense, field):
                setattr(expense, field, value)

        return ExpenseRepository.save(expense)

    # ── Exclusão ──────────────────────────────────────────────────────────────

    @staticmethod
    def delete(user_id: int, expense_id: int, delete_siblings: bool = False) -> bool:
        """
        delete_siblings=True → apaga todas as parcelas/recorrências do grupo.
        delete_siblings=False → apaga só o registro individual. RF004.
        """
        expense = ExpenseRepository.get_by_id(expense_id, user_id)
        if not expense:
            return False

        if delete_siblings and expense.parent_id:
            siblings = ExpenseRepository.get_children(expense.parent_id)
            # inclui o próprio parent se ele existir separado
            parent = ExpenseRepository.get_by_id(expense.parent_id, user_id)
            targets = siblings + ([parent] if parent and parent.id != expense.id else [])
            targets.append(expense)
            ExpenseRepository.delete_many(list({e.id: e for e in targets}.values()))
        else:
            ExpenseRepository.delete(expense)

        return True

    # ── Saldo ─────────────────────────────────────────────────────────────────

    @staticmethod
    def get_balance(user_id: int) -> dict:
        """
        Calcula saldo atual do usuário. RF011 / RN004.
        Saldo = soma das entradas - soma das saídas confirmadas.
        """
        expenses = ExpenseRepository.get_all_by_user(user_id)
        income  = sum(e.amount for e in expenses if e.type == 'income')
        outcome = sum(e.amount for e in expenses if e.type == 'expense')
        return {
            'income':  round(income, 2),
            'outcome': round(outcome, 2),
            'balance': round(income - outcome, 2),
        }