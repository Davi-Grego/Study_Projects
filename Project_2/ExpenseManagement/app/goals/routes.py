from flask import Blueprint, request, jsonify, render_template
from marshmallow import ValidationError

from app.firebase import login_required, api_login_required
from app.goals.schemas import GoalSchema, GoalUpdateSchema
from app.goals.services import GoalService

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

goal_schema        = GoalSchema()
goal_update_schema = GoalUpdateSchema()


# ── Páginas (SSR) ─────────────────────────────────────────────────────────────

@goals_bp.route('/')
@login_required
def index(user_id: int):
    """Página de metas com dados iniciais já renderizados."""
    goals = GoalService.get_all(user_id)
    return render_template('goals/index.html', goals=goals)


# ── API (JSON) ────────────────────────────────────────────────────────────────

@goals_bp.route('/api', methods=['GET'])
@api_login_required
def api_list(user_id: int):
    """Lista todas as metas do usuário."""
    goals = GoalService.get_all(user_id)
    return jsonify([g.to_dict() for g in goals]), 200


@goals_bp.route('/api', methods=['POST'])
@api_login_required
def api_create(user_id: int):
    """Cria uma nova meta. RF015."""
    try:
        data = goal_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    goal = GoalService.create(user_id, data)
    return jsonify(goal.to_dict()), 201


@goals_bp.route('/api/<int:goal_id>', methods=['PUT'])
@api_login_required
def api_update(user_id: int, goal_id: int):
    """Edita uma meta existente."""
    try:
        data = goal_update_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    goal = GoalService.update(user_id, goal_id, data)
    if not goal:
        return jsonify({"error": "Meta não encontrada."}), 404

    return jsonify(goal.to_dict()), 200


@goals_bp.route('/api/<int:goal_id>/progress', methods=['POST'])
@api_login_required
def api_add_progress(user_id: int, goal_id: int):
    """
    Registra progresso manual na meta.
    Body: { "amount": 500.00 }
    """
    data = request.get_json(silent=True) or {}
    amount = data.get('amount')

    if not amount or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Informe um valor válido maior que zero."}), 422

    goal = GoalService.add_progress(user_id, goal_id, float(amount))
    if not goal:
        return jsonify({"error": "Meta não encontrada."}), 404

    return jsonify(goal.to_dict()), 200


@goals_bp.route('/api/<int:goal_id>', methods=['DELETE'])
@api_login_required
def api_delete(user_id: int, goal_id: int):
    """Exclui uma meta."""
    deleted = GoalService.delete(user_id, goal_id)
    if not deleted:
        return jsonify({"error": "Meta não encontrada."}), 404

    return jsonify({"message": "Meta excluída com sucesso."}), 200