from app.models import Category
from app.categories.repository import CategoryRepository


# Categorias globais criadas automaticamente no primeiro uso do sistema
DEFAULT_CATEGORIES = [
    {"name": "Alimentação",     "icon": "utensils"},
    {"name": "Transporte",      "icon": "car"},
    {"name": "Moradia",         "icon": "home"},
    {"name": "Saúde",           "icon": "heart"},
    {"name": "Educação",        "icon": "book"},
    {"name": "Lazer",           "icon": "gamepad"},
    {"name": "Vestuário",       "icon": "shirt"},
    {"name": "Salário",         "icon": "briefcase"},
    {"name": "Investimentos",   "icon": "trending-up"},
    {"name": "Outros",          "icon": "more-horizontal"},
]


class CategoryService:

    # ── Setup inicial ─────────────────────────────────────────────────────────

    @staticmethod
    def seed_defaults() -> None:
        """
        Cria as categorias globais padrão se ainda não existirem.
        Chamado uma vez no app/__init__.py após db.create_all().
        """
        existing = {c.name for c in CategoryRepository.get_globals()}
        for cat in DEFAULT_CATEGORIES:
            if cat["name"] not in existing:
                CategoryRepository.save(Category(name=cat["name"], icon=cat["icon"]))

    # ── Leitura ───────────────────────────────────────────────────────────────

    @staticmethod
    def get_all_visible(user_id: int) -> list[Category]:
        """Globais + do usuário — usada nos selects de movimentação. RF005."""
        return CategoryRepository.get_all_visible(user_id)

    @staticmethod
    def get_user_categories(user_id: int) -> list[Category]:
        """Apenas as categorias criadas pelo usuário."""
        return CategoryRepository.get_by_user(user_id)

    # ── Criação ───────────────────────────────────────────────────────────────

    @staticmethod
    def create(user_id: int, data: dict) -> tuple[Category | None, str | None]:
        """
        Retorna (category, None) em caso de sucesso.
        Retorna (None, mensagem_de_erro) se nome já existe.
        """
        if CategoryRepository.name_exists(data['name'], user_id):
            return None, f"Você já tem uma categoria com o nome '{data['name']}'."

        category = Category(
            name=data['name'],
            icon=data.get('icon'),
            user_id=user_id,
        )
        return CategoryRepository.save(category), None

    # ── Edição ────────────────────────────────────────────────────────────────

    @staticmethod
    def update(user_id: int, category_id: int, data: dict) -> tuple[Category | None, str | None]:
        category = CategoryRepository.get_by_id_and_user(category_id, user_id)
        if not category:
            return None, "Categoria não encontrada."

        new_name = data.get('name')
        if new_name and new_name != category.name:
            if CategoryRepository.name_exists(new_name, user_id):
                return None, f"Você já tem uma categoria com o nome '{new_name}'."

        for field, value in data.items():
            if hasattr(category, field):
                setattr(category, field, value)

        return CategoryRepository.save(category), None

    # ── Exclusão ──────────────────────────────────────────────────────────────

    @staticmethod
    def delete(user_id: int, category_id: int) -> tuple[bool, str | None]:
        """
        Não permite excluir categorias globais.
        Retorna (True, None) em sucesso ou (False, mensagem) em erro.
        """
        category = CategoryRepository.get_by_id_and_user(category_id, user_id)
        if not category:
            # tenta buscar sem user_id para dar mensagem mais clara
            global_cat = CategoryRepository.get_by_id(category_id)
            if global_cat:
                return False, "Categorias globais não podem ser excluídas."
            return False, "Categoria não encontrada."

        CategoryRepository.delete(category)
        return True, None
