from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, make_response
from flask_login import login_required, current_user
from app.services.financial_service import FinancialService
from app.services.pdf_service import PDFService
from datetime import datetime, date

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
        data_str = request.form.get('data')

        if data_str:
            try:
                data_selecionada = datetime.strptime(data_str, '%Y-%m-%d').date()
                if data_selecionada > date.today():
                    flash("Não é permitido registar transações em datas futures.", "danger")
                    data = FinancialService.get_dashboard_data(current_user.id)
                    return render_template('transacoes.html', data=data)
            except ValueError:
                flash("Formato de data inválido.", "danger")
                data = FinancialService.get_dashboard_data(current_user.id)
                return render_template('transacoes.html', data=data)

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

@dashboard_bp.route('/api/ai/limpar-historico', methods=['POST'])
@login_required
def limpar_historico_ia():
    from app.models import InteracaoIA
    from app.database import db
    try:
        InteracaoIA.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return jsonify({"status": "sucesso", "mensagem": "Histórico apagado com sucesso."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@dashboard_bp.route('/transacoes/exportar-pdf', methods=['GET'])
@login_required
def exportar_extrato_pdf():
    data = FinancialService.get_dashboard_data(current_user.id)
    try:
        pdf_bytes = PDFService.gerar_extrato_pdf(
            user_name=current_user.nome,
            receitas=data.get('receitas', []),
            despesas=data.get('despesas', []),
            total_receitas=data.get('total_receitas', 0.0),
            total_despesas=data.get('total_despesas', 0.0),
            saldo_atual=data.get('total_receitas', 0.0) - data.get('total_despesas', 0.0)
        )
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=extrato_lombongocare.pdf'
        return response
    except Exception as e:
        return jsonify({"erro": str(e)}), 500