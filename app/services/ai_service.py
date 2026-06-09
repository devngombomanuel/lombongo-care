import requests
from flask import current_app
from app.services.financial_service import FinancialService
from app.repositories.financial_repository import FinancialRepository

class AIService:
    @staticmethod
    def generate_financial_advice(user_id, user_message=None):
        api_key = current_app.config.get('AI_API_KEY')
        

        if not api_key:
            return "Olá! O motor da IA está montado, mas a configuração da AI_API_KEY não foi encontrada no config.py."

        data = FinancialService.get_dashboard_data(user_id)
        
        contexto = f"Contexto Financeiro do Utilizador:\n"
        contexto += f"- Saldo Atual: {data['saldo_atual']} Kz\n"
        contexto += f"- Total de Receitas: {data['total_receitas']} Kz\n"
        contexto += f"- Total de Despesas: {data['total_despesas']} Kz\n"
        contexto += f"- Gastos por Categoria: {data['gastos_por_categoria']}\n\n"
        
        prompt_base = (
            "Atue como o LombongoIA, um assistente sénior de finanças pessoais angolano. "
            "Dê recomendações curtíssimas (máximo 3 parágrafos), diretas e práticas de poupança baseadas nos dados fornecidos. "
            "Use termos cordiais. Responda em formato de texto limpo sem formatações markdown pesadas ou títulos.\n\n"
        )
        
        if user_message:
            prompt_final = f"{prompt_base}{contexto}Pergunta do Utilizador: {user_message}"
        else:
            prompt_final = f"{prompt_base}{contexto}Gere uma análise rápida do meu estado atual e dê uma dica de ouro."

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": prompt_final}]
            }]
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=12)
            if response.status_code == 200:
                result = response.json()
                

                try:
                    resposta_ia = result['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexType, TypeError):
                    resposta_ia = "Recebi uma resposta da IA, mas o formato dos dados foi inesperado."
            else:
                resposta_ia = f"Erro na API da IA (Código {response.status_code}). O servidor respondeu: {response.text[:120]}"
        except Exception as e:
            resposta_ia = f"Não consegui contactar o cérebro da IA. Erro: {str(e)[:50]}"

        if user_message and response.status_code == 200:
            FinancialRepository.save_ia_interaction(user_id, user_message, resposta_ia)
            
        return resposta_ia