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
        valor_str = request.form.get('valor')

        if data_str:
            try:
                data_selecionada = datetime.strptime(data_str, '%Y-%m-%d').date()
                if data_selecionada > date.today():
                    flash("Não é permitido registar transações em datas futuras.", "danger")
                    data = FinancialService.get_dashboard_data(current_user.id)
                    return render_template('transacoes.html', data=data)
            except ValueError:
                flash("Formato de data inválido.", "danger")
                data = FinancialService.get_dashboard_data(current_user.id)
                return render_template('transacoes.html', data=data)

        if tipo == 'despesa' and valor_str:
            try:
                valor_despesa = float(valor_str)
                data_atual = FinancialService.get_dashboard_data(current_user.id)
                saldo_atual = data_atual.get('total_receitas', 0.0) - data_atual.get('total_despesas', 0.0)
                
                if saldo_atual <= 0 or valor_despesa > saldo_atual:
                    flash(f"Operação rejeitada. Saldo insuficiente para cobrir esta despesa (Saldo atual: {saldo_atual:,.2f} Kz).", "danger")
                    data = FinancialService.get_dashboard_data(current_user.id)
                    return render_template('transacoes.html', data=data)
            except ValueError:
                pass

        if FinancialService.add_transaction(current_user.id, request.form, tipo):
            return redirect(url_for('dashboard.index')) 
            
    data = FinancialService.get_dashboard_data(current_user.id)
    return render_template('transacoes.html', data=data)

@dashboard_bp.route('/transacao/editar/<string:tipo>/<int:id>', methods=['POST'])
@login_required
def editar_transacao(tipo, id):
    valor_novo = float(request.form.get('valor', 0))
    data_str = request.form.get('data')
    
    if data_str:
        try:
            data_selecionada = datetime.strptime(data_str, '%Y-%m-%d').date()
            if data_selecionada > date.today():
                flash("Não é permitido salvar transações em datas futuras.", "danger")
                return redirect(url_for('dashboard.transacoes'))
        except ValueError:
            flash("Formato de data inválido.", "danger")
            return redirect(url_for('dashboard.transacoes'))

    dados_atuais = FinancialService.get_dashboard_data(current_user.id)
    total_receitas = dados_atuais.get('total_receitas', 0.0)
    total_despesas = dados_atuais.get('total_despesas', 0.0)

    if tipo == 'receita':
        transacao = next((r for r in dados_atuais['receitas'] if r['id'] == id), None)
        if transacao:
            diferenca = valor_novo - float(transacao['valor'])
            if (total_receitas + diferenca - total_despesas) < 0:
                flash("Alteração rejeitada. A redução desta receita deixaria o saldo da conta negativo.", "danger")
                return redirect(url_for('dashboard.transacoes'))
                
    elif tipo == 'despesa':
        transacao = next((d for d in dados_atuais['despesas'] if d['id'] == id), None)
        if transacao:
            diferenca = valor_novo - float(transacao['valor'])
            if (total_receitas - (total_despesas + diferenca)) < 0:
                flash("Alteração rejeitada. O novo valor da despesa excede o saldo disponível na conta.", "danger")
                return redirect(url_for('dashboard.transacoes'))

    if FinancialService.update_transaction(id, current_user.id, request.form, tipo):
        flash("Registo atualizado com sucesso.", "success")
    else:
        flash("Erro ao atualizar o registo.", "danger")
        
    return redirect(url_for('dashboard.transacoes'))

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