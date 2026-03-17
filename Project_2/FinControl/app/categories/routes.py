from flask import Blueprint, request, jsonify, render_template
from marshmallow import ValidationError

from app.firebase import login_required, api_login_required
from app.categories.schemas import CategorySchema, CategoryUpdateSchema
from app.categories.services import CategoryService

categories_bp = Blueprint('categories', __name__, url_prefix='/categories', template_folder='templates/categories')

category_schema        = CategorySchema()
category_update_schema = CategoryUpdateSchema()


# ── Páginas (SSR) ─────────────────────────────────────────────────────────────

@categories_bp.route('/')
@login_required
def index(user_id: int):
    """Página de gerenciamento de categorias do usuário."""
    categories = CategoryService.get_user_categories(user_id)
    return render_template('categories.html', categories=categories)


# ── API (JSON) ────────────────────────────────────────────────────────────────

@categories_bp.route('/api', methods=['GET'])
@api_login_required
def api_list(user_id: int):
    """
    Lista globais + do usuário.
    Usada para popular selects nos formulários de movimentação. RF005.
    """
    categories = CategoryService.get_all_visible(user_id)
    return jsonify([c.to_dict() for c in categories]), 200


@categories_bp.route('/api', methods=['POST'])
@api_login_required
def api_create(user_id: int):
    """Cria uma categoria personalizada."""
    try:
        data = category_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    category, error = CategoryService.create(user_id, data)
    if error:
        return jsonify({"error": error}), 409

    return jsonify(category.to_dict()), 201


@categories_bp.route('/api/<int:category_id>', methods=['PUT'])
@api_login_required
def api_update(user_id: int, category_id: int):
    """Edita uma categoria do usuário."""
    try:
        data = category_update_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    category, error = CategoryService.update(user_id, category_id, data)
    if error:
        status = 404 if "não encontrada" in error else 409
        return jsonify({"error": error}), status

    return jsonify(category.to_dict()), 200


@categories_bp.route('/api/<int:category_id>', methods=['DELETE'])
@api_login_required
def api_delete(user_id: int, category_id: int):
    """Exclui uma categoria do usuário — não permite excluir globais."""
    deleted, error = CategoryService.delete(user_id, category_id)
    if not deleted:
        status = 403 if "globais" in error else 404
        return jsonify({"error": error}), status

    return jsonify({"message": "Categoria excluída com sucesso."}), 200
