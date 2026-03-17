from app.extensions import db
from app.models import Goal


class GoalRepository:

    @staticmethod
    def get_by_id(goal_id: int, user_id: int) -> Goal | None:
        """Busca meta pelo ID garantindo que pertence ao usuário. RN001."""
        return Goal.query.filter_by(id=goal_id, user_id=user_id).first()

    @staticmethod
    def get_all_by_user(user_id: int) -> list[Goal]:
        return (
            Goal.query
            .filter_by(user_id=user_id)
            .order_by(Goal.created_at.desc())
            .all()
        )

    @staticmethod
    def get_active_by_user(user_id: int) -> list[Goal]:
        """Retorna apenas metas ativas — usadas para verificar alertas."""
        return (
            Goal.query
            .filter_by(user_id=user_id, is_active=True)
            .all()
        )

    @staticmethod
    def save(goal: Goal) -> Goal:
        db.session.add(goal)
        db.session.commit()
        return goal

    @staticmethod
    def delete(goal: Goal) -> None:
        db.session.delete(goal)
        db.session.commit()