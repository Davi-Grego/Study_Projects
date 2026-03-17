from flask import Blueprint, request, jsonify, render_template
from datetime import date

from app.firebase import login_required, api_login_required
from app.reports.services import ReportService

reports_bp = Blueprint('reports', __name__, url_prefix='/reports', template_folder='templates/reports')


# ── Páginas (SSR) ─────────────────────────────────────────────────────────────

@reports_bp.route('/')
@login_required
def index(user_id: int):
    """
    Página de relatórios.
    Carrega o resumo do mês atual como dados iniciais.
    Filtros dinâmicos via API.
    """
    today   = date.today()
    summary = ReportService.monthly_summary(user_id, today.year, today.month)

    return render_template(
        'reports.html',
        summary=summary,
        current_year=today.year,
        current_month=today.month,
    )


# ── API (JSON) ────────────────────────────────────────────────────────────────

@reports_bp.route('/api/monthly', methods=['GET'])
@api_login_required
def api_monthly(user_id: int):
    """
    Resumo mensal. RF012.
    ?year=2025&month=6
    """
    year  = request.args.get('year',  type=int)
    month = request.args.get('month', type=int)

    if not year or not month:
        return jsonify({"error": "Informe year e month."}), 422
    if not (1 <= month <= 12):
        return jsonify({"error": "Mês inválido."}), 422
    if year < 2000 or year > date.today().year + 1:
        return jsonify({"error": "Ano inválido."}), 422

    return jsonify(ReportService.monthly_summary(user_id, year, month)), 200


@reports_bp.route('/api/yearly', methods=['GET'])
@api_login_required
def api_yearly(user_id: int):
    """
    Resumo anual com breakdown mês a mês. RF012.
    ?year=2025
    """
    year = request.args.get('year', type=int)

    if not year:
        return jsonify({"error": "Informe o year."}), 422
    if year < 2000 or year > date.today().year + 1:
        return jsonify({"error": "Ano inválido."}), 422

    return jsonify(ReportService.yearly_summary(user_id, year)), 200


@reports_bp.route('/api/period', methods=['GET'])
@api_login_required
def api_period(user_id: int):
    """
    Resumo por período personalizado. RF012 / RF014.
    ?start=YYYY-MM-DD&end=YYYY-MM-DD
    """
    start_str = request.args.get('start')
    end_str   = request.args.get('end')

    if not start_str or not end_str:
        return jsonify({"error": "Informe start e end."}), 422

    try:
        start = date.fromisoformat(start_str)
        end   = date.fromisoformat(end_str)
    except ValueError:
        return jsonify({"error": "Datas inválidas. Use YYYY-MM-DD."}), 422

    if start > end:
        return jsonify({"error": "A data inicial não pode ser maior que a final."}), 422
    if (end - start).days > 366:
        return jsonify({"error": "Período máximo permitido é de 1 ano."}), 422

    return jsonify(ReportService.period_summary(user_id, start, end)), 200


@reports_bp.route('/api/categories', methods=['GET'])
@api_login_required
def api_categories(user_id: int):
    """
    Breakdown por categoria. RF012.
    ?year=2025           → ano inteiro
    ?year=2025&month=6   → mês específico
    """
    year  = request.args.get('year',  type=int)
    month = request.args.get('month', type=int)

    if not year:
        return jsonify({"error": "Informe o year."}), 422

    return jsonify(ReportService.category_summary(user_id, year, month)), 200
