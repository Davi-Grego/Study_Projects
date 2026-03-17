from app.extensions import db
from app.models import Category


class CategoryRepository:

    @staticmethod
    def get_by_id(category_id: int) -> Category | None:
        return db.session.get(Category, category_id)

    @staticmethod
    def get_by_id_and_user(category_id: int, user_id: int) -> Category | None:
        """Busca categoria garantindo que pertence ao usuário. RN001."""
        return Category.query.filter_by(id=category_id, user_id=user_id).first()

    @staticmethod
    def get_all_visible(user_id: int) -> list[Category]:
        """
        Retorna categorias globais (user_id IS NULL) +
        categorias criadas pelo próprio usuário.
        Essa é a lista que aparece nos selects de movimentação.
        """
        return (
            Category.query
            .filter(
                db.or_(
                    Category.user_id == user_id,
                    Category.user_id == None,  # noqa: E711 — SQLAlchemy exige == None
                )
            )
            .order_by(Category.user_id.asc(), Category.name.asc())
            .all()
        )

    @staticmethod
    def get_globals() -> list[Category]:
        """Retorna apenas as categorias globais do sistema."""
        return Category.query.filter_by(user_id=None).order_by(Category.name).all()

    @staticmethod
    def get_by_user(user_id: int) -> list[Category]:
        """Retorna apenas as categorias criadas pelo usuário."""
        return Category.query.filter_by(user_id=user_id).order_by(Category.name).all()

    @staticmethod
    def name_exists(name: str, user_id: int) -> bool:
        """Evita categorias duplicadas por usuário."""
        return Category.query.filter_by(name=name, user_id=user_id).first() is not None

    @staticmethod
    def save(category: Category) -> Category:
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def delete(category: Category) -> None:
        db.session.delete(category)
        db.session.commit()
