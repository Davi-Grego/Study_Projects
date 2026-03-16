from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from marshmallow import ValidationError
from datetime import date

from app.firebase import login_required, api_login_required
from app.expenses.schemas import ExpenseSchema, ExpenseUpdateSchema
from app.expenses.services import ExpenseService

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

expense_schema        = ExpenseSchema()
expense_update_schema = ExpenseUpdateSchema()


# ── Páginas (SSR) ─────────────────────────────────────────────────────────────

@expenses_bp.route('/')
@login_required
def index(user_id: int):
    """
    Página principal de movimentações.
    Carrega o mês atual como dados iniciais — filtros posteriores via API.
    """
    today    = date.today()
    expenses = ExpenseService.get_by_month(user_id, today.year, today.month)
    balance  = ExpenseService.get_balance(user_id)

    return render_template(
        'expenses/index.html',
        expenses=expenses,
        balance=balance,
        current_month=today.month,
        current_year=today.year,
    )


# ── API (JSON) ────────────────────────────────────────────────────────────────

@expenses_bp.route('/api/filter', methods=['GET'])
@api_login_required
def api_filter(user_id: int):
    """
    Filtra movimentações sem recarregar a página. RF014 / RF012.

    Query params:
      ?start=YYYY-MM-DD&end=YYYY-MM-DD  → período personalizado
      ?year=2025&month=6                → mês específico
      ?category_id=3                    → por categoria
    """
    start_str   = request.args.get('start')
    end_str     = request.args.get('end')
    year        = request.args.get('year',        type=int)
    month       = request.args.get('month',       type=int)
    category_id = request.args.get('category_id', type=int)

    if start_str and end_str:
        try:
            start = date.fromisoformat(start_str)
            end   = date.fromisoformat(end_str)
        except ValueError:
            return jsonify({"error": "Datas inválidas. Use YYYY-MM-DD."}), 422

        if (end - start).days > 366:
            return jsonify({"error": "Período máximo permitido é de 1 ano."}), 422

        expenses = ExpenseService.get_by_period(user_id, start, end)

    elif year and month:
        if not (1 <= month <= 12):
            return jsonify({"error": "Mês inválido."}), 422
        expenses = ExpenseService.get_by_month(user_id, year, month)

    elif category_id:
        expenses = ExpenseService.get_by_category(user_id, category_id)

    else:
        expenses = ExpenseService.get_all(user_id)

    return jsonify([e.to_dict() for e in expenses]), 200


@expenses_bp.route('/api/balance', methods=['GET'])
@api_login_required
def api_balance(user_id: int):
    """Saldo atualizado para o JS atualizar o card sem recarregar. RF011."""
    return jsonify(ExpenseService.get_balance(user_id)), 200


@expenses_bp.route('/api', methods=['POST'])
@api_login_required
def api_create(user_id: int):
    """Cria uma movimentação (simples, parcelada ou recorrente). RF003/RF008/RF010."""
    try:
        data = expense_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    created = ExpenseService.create(user_id, data)
    return jsonify([e.to_dict() for e in created]), 201


@expenses_bp.route('/api/<int:expense_id>', methods=['PUT'])
@api_login_required
def api_update(user_id: int, expense_id: int):
    """Edita uma movimentação individual. RF004."""
    try:
        data = expense_update_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    updated = ExpenseService.update(user_id, expense_id, data)
    if not updated:
        return jsonify({"error": "Movimentação não encontrada."}), 404

    return jsonify(updated.to_dict()), 200


@expenses_bp.route('/api/<int:expense_id>', methods=['DELETE'])
@api_login_required
def api_delete(user_id: int, expense_id: int):
    """
    Exclui uma movimentação. RF004.
    ?all=true → exclui todas as parcelas/recorrências do grupo.
    """
    delete_siblings = request.args.get('all', 'false').lower() == 'true'

    deleted = ExpenseService.delete(user_id, expense_id, delete_siblings)
    if not deleted:
        return jsonify({"error": "Movimentação não encontrada."}), 404

    return jsonify({"message": "Movimentação excluída com sucesso."}), 200