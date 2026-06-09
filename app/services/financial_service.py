from app.repositories.financial_repository import FinancialRepository
from datetime import datetime

class FinancialService:
    @staticmethod
    def get_dashboard_data(user_id):
        receitas = FinancialRepository.get_receitas_by_user(user_id)
        despesas = FinancialRepository.get_despesas_by_user(user_id)

        total_receitas = sum(r.valor for r in receitas)
        total_despesas = sum(d.valor for d in despesas)
        saldo_atual = total_receitas - total_despesas

        # Agrupamento por Categoria para Gráficos
        gastos_por_categoria = {}
        for d in despesas:
            gastos_por_categoria[d.categoria] = gastos_por_categoria.get(d.categoria, 0) + d.valor

        return {
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "saldo_atual": saldo_atual,
            "gastos_por_categoria": gastos_por_categoria,
            "receitas": [r.__dict__ for r in receitas],
            "despesas": [d.__dict__ for d in despesas]
        }

    @staticmethod
    def add_transaction(user_id, form_data, tipo):
        try:
            valor = float(form_data.get('valor'))
            descricao = form_data.get('descricao')
            categoria = form_data.get('categoria')
            data_str = form_data.get('data')
            data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()

            if tipo == 'receita':
                return FinancialRepository.add_receita(user_id, valor, descricao, categoria, data_obj)
            else:
                periodicidade = form_data.get('periodicidade', 'mensal')
                return FinancialRepository.add_despesa(user_id, valor, descricao, categoria, periodicidade, data_obj)
        except Exception as e:
            return None