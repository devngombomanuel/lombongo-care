class AIService:
    @staticmethod
    def generate_financial_advice(user_id, user_message=None):
        api_key = current_app.config.get('AI_API_KEY')
        
        if not api_key:
            return "Olá! O motor da IA está montado, mas a configuração da AI_API_KEY não foi encontrada."

        # 1. Inicializar o cliente oficial da Google usando a tua chave
        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            return f"Erro ao inicializar o motor da IA: {str(e)[:50]}"

        # 2. Recolher dados financeiros do utilizador
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
        
        # GARANTIA: A variável é explicitamente declarada aqui para o escopo da função
        if user_message:
            prompt_final = f"{prompt_base}{contexto}Pergunta do Utilizador: {user_message}"
        else:
            prompt_final = f"{prompt_base}{contexto}Gere uma análise rápida do meu estado atual e dê uma dica de ouro."

        # 3. Chamar a API usando o modelo de produção atualizado
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_final, # Agora o Pylance já vai reconhecer a variável acima!
            )
            
            if response.text:
                resposta_ia = response.text
                status_sucesso = True
            else:
                resposta_ia = "A IA processou o pedido, mas devolveu um texto vazio."
                status_sucesso = False
                
        except Exception as e:
            resposta_ia = f"Erro na comunicação com o Gemini: {str(e)}"
            status_sucesso = False

        # 4. Guardar no histórico em caso de sucesso
        if user_message and status_sucesso:
            try:
                FinancialRepository.save_ia_interaction(user_id, user_message, resposta_ia)
            except Exception as repo_err:
                current_app.logger.error(f"Erro ao guardar histórico da IA: {repo_err}")
            
        return resposta_ia