from app.models import Goal
from app.goals.repository import GoalRepository


class GoalService:

    # ── Criação ───────────────────────────────────────────────────────────────

    @staticmethod
    def create(user_id: int, data: dict) -> Goal:
        goal = Goal(
            user_id=user_id,
            name=data['name'],
            target_amount=data['target_amount'],
            deadline=data.get('deadline'),
            spending_limit=data.get('spending_limit'),
        )
        return GoalRepository.save(goal)

    # ── Leitura ───────────────────────────────────────────────────────────────

    @staticmethod
    def get_all(user_id: int) -> list[Goal]:
        return GoalRepository.get_all_by_user(user_id)

    @staticmethod
    def get_by_id(user_id: int, goal_id: int) -> Goal | None:
        return GoalRepository.get_by_id(goal_id, user_id)

    # ── Edição ────────────────────────────────────────────────────────────────

    @staticmethod
    def update(user_id: int, goal_id: int, data: dict) -> Goal | None:
        goal = GoalRepository.get_by_id(goal_id, user_id)
        if not goal:
            return None

        for field, value in data.items():
            if hasattr(goal, field):
                setattr(goal, field, value)

        return GoalRepository.save(goal)

    # ── Exclusão ──────────────────────────────────────────────────────────────

    @staticmethod
    def delete(user_id: int, goal_id: int) -> bool:
        goal = GoalRepository.get_by_id(goal_id, user_id)
        if not goal:
            return False
        GoalRepository.delete(goal)
        return True

    # ── Progresso manual ─────────────────────────────────────────────────────

    @staticmethod
    def add_progress(user_id: int, goal_id: int, amount: float) -> Goal | None:
        """
        Adiciona valor ao progresso atual da meta.
        Usado quando o usuário registra manualmente quanto guardou.
        """
        goal = GoalRepository.get_by_id(goal_id, user_id)
        if not goal:
            return None

        goal.current_amount = round(goal.current_amount + amount, 2)

        # garante que não ultrapassa o target
        if goal.current_amount >= goal.target_amount:
            goal.current_amount = goal.target_amount
            goal.is_active = False  # meta atingida — desativa automaticamente

        return GoalRepository.save(goal)

    # ── Alertas ───────────────────────────────────────────────────────────────

    @staticmethod
    def check_goal_impact(user_id: int, expense_amount: float) -> list[dict]:
        """
        Verifica se um novo gasto impacta as metas ativas do usuário.
        Chamado pelo ExpenseService após criar uma saída (type='expense').

        Retorna lista de alertas — cada alerta tem 'type' e 'goal'.
        RF016 — alerta ao registrar gasto que impacte a meta.
        RF017 — alerta quando limite de gasto for atingido.
        RN005 — considera o valor restante da meta no período ativo.
        """
        goals = GoalRepository.get_active_by_user(user_id)
        alerts = []

        for goal in goals:
            remaining = goal.remaining

            # RF016 — gasto consome mais de 10% do valor restante da meta
            if remaining > 0 and expense_amount >= (remaining * 0.10):
                alerts.append({
                    'type':    'goal_impact',
                    'goal_id': goal.id,
                    'message': (
                        f"O gasto de R$ {expense_amount:.2f} representa "
                        f"{(expense_amount / remaining * 100):.0f}% do valor "
                        f"restante da sua meta '{goal.name}' "
                        f"(R$ {remaining:.2f} restantes)."
                    ),
                })

            # RF017 — limite de gasto definido pelo usuário foi atingido
            if goal.spending_limit and expense_amount >= goal.spending_limit:
                alerts.append({
                    'type':    'spending_limit',
                    'goal_id': goal.id,
                    'message': (
                        f"Você atingiu o limite de gasto de R$ {goal.spending_limit:.2f} "
                        f"definido para a meta '{goal.name}'."
                    ),
                })

        return alerts