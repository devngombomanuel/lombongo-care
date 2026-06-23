from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.ai_service import AIService
from app.repositories.financial_repository import FinancialRepository

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/ai/pergunta', methods=['POST'])
@login_required
def perguntar_ia():
    user_message = request.json.get('mensagem')
    if not user_message:
        return jsonify({"erro": "A mensagem não pode estar vazia"}), 400
        
    contexto_perfil = (
        f"[PERFIL SOCIOECONÓMICO DO UTILIZADOR]\n"
        f"Nome: {current_user.nome}\n"
        f"Província: {current_user.provincia or 'Não informada'}\n"
        f"Município: {current_user.municipio or 'Não informado'}\n"
        f"Estado Civil: {current_user.estado_civil or 'Não informado'}\n"
        f"Agregado Familiar: {current_user.agregado_familiar or 'Não informado'} pessoa(s)\n"
        f"Ocupação/Segmento: {current_user.ocupacao or 'Não informada'}\n"
        f"Objetivo Financeiro Primário: {current_user.objetivo_financeiro or 'Não informado'}\n"
    )
    
    mensagem_enriquecida = f"{contexto_perfil}\n[PERGUNTA DO UTILIZADOR]\n{user_message}"
    
    resposta = AIService.generate_financial_advice(current_user.id, mensagem_enriquecida)
    
    FinancialRepository.save_ia_interaction(current_user.id, user_message, resposta)
    
    return jsonify({"resposta": resposta})

@ai_bp.route('/api/ai/historico')
@login_required
def historico_ia():
    historico = FinancialRepository.get_ia_interactions(current_user.id)
    return jsonify([{"mensagem": h.mensagem, "resposta": h.resposta} for h in historico])

@ai_bp.route('/api/ai/limpar-historico', methods=['POST'])
@login_required
def limpar_historico_ia():
    sucesso = FinancialRepository.clear_ia_interactions(current_user.id)
    if sucesso:
        return jsonify({"status": "sucesso", "mensagem": "Histórico apagado com sucesso"})
    return jsonify({"erro": "Não foi possível apagar o histórico"}), 500