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
        
    resposta = AIService.generate_financial_advice(current_user.id, user_message)
    return jsonify({"resposta": resposta})

@ai_bp.route('/api/ai/historico')
@login_required
def historico_ia():
    historico = FinancialRepository.get_ia_interactions(current_user.id)
    return jsonify([{"mensagem": h.mensagem, "resposta": h.resposta} for h in historico])