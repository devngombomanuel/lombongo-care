import requests
from flask import current_app
from app.repositories.financial_repository import FinancialRepository
from app.services.financial_service import FinancialService

class AIService:
    @staticmethod
    def generate_financial_advice(user_id, user_message=None):
        # 1. Recolher contexto financeiro real do utilizador
        data = FinancialService.get_dashboard_data(user_id)
        
        contexto = f"Contexto Financeiro do Utilizador:\n"
        contexto += f"- Saldo Atual: {data['saldo_atual']} Kwanza/Unidades\n"
        contexto += f"- Total de Receitas: {data['total_receitas']}\n"
        contexto += f"- Total de Despesas: {data['total_despesas']}\n"
        contexto += f"- Distribuição de Gastos: {data['gastos_por_categoria']}\n\n"
        
        prompt_base = (
            "Atue como o Assistente de Inteligência Financeira do LombongoCare. "
            "Dê recomendações curtas, diretas, focadas em poupança, corte de despesas supérfluas e aumento de património. "
            "Use linguagem simples e motivadora. Nunca invente dados que não estão no contexto fornecido.\n\n"
        )
        
        if user_message:
            prompt_final = f"{prompt_base}{contexto}Pergunta do Utilizador: {user_message}\nResposta:"
        else:
            prompt_final = f"{prompt_base}{contexto}Gere uma análise automática resumida do padrão de gastos e dê 2 dicas de poupança."

        # Chamada segura para a API de IA (Configurada para Gemini neste exemplo)
        api_key = current_app.config['AI_API_KEY']
        url = f"{current_app.config['AI_API_URL']}?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt_final}]}]
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                resposta_ia = result['candidates'][0]['content']['parts'][0]['text']
            else:
                resposta_ia = "Olá! Atualmente não consigo analisar as suas finanças em tempo real, mas lembre-se: manter as despesas abaixo das receitas é o primeiro passo para a saúde financeira!"
        except Exception:
            resposta_ia = "Olá! Estamos a recalibrar os motores da IA. Tente novamente em instantes para obter os seus insights personalizados."

        # Persistir a interação
        if user_message:
            FinancialRepository.save_ia_interaction(user_id, user_message, resposta_ia)
            
        return resposta_ia