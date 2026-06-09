from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.services.financial_service import FinancialService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    data = FinancialService.get_dashboard_data(current_user.id)
    return render_template('dashboard.html', data=data)

@dashboard_bp.route('/transacoes', methods=['GET', 'POST'])
@login_required
def transacoes():
    if request.method == 'POST':
        tipo = request.form.get('tipo_transacao') 
        if FinancialService.add_transaction(current_user.id, request.form, tipo):
            return redirect(url_for('dashboard.index')) 
    data = FinancialService.get_dashboard_data(current_user.id)
    return render_template('transacoes.html', data=data)

@dashboard_bp.route('/api/dados-graficos')
@login_required
def dados_graficos():
    data = FinancialService.get_dashboard_data(current_user.id)
    return jsonify({
        "categorias": list(data['gastos_por_categoria'].keys()),
        "valores_categorias": list(data['gastos_por_categoria'].values()),
        "total_receitas": data['total_receitas'],
        "total_despesas": data['total_despesas']
    })
    
@dashboard_bp.route('/transacao/remover/<string:tipo>/<int:id>', methods=['POST'])
@login_required
def remover_transacao(tipo, id):
    from app.repositories.financial_repository import FinancialRepository
    if tipo == 'receita':
        FinancialRepository.delete_receita(id, current_user.id)
    elif tipo == 'despesa':
        FinancialRepository.delete_despesa(id, current_user.id)
    return redirect(url_for('dashboard.transacoes'))