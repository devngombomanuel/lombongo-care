from app.repositories.financial_repository import FinancialRepository
from datetime import datetime

class FinancialService:
    @staticmethod
    def get_dashboard_data(user_id):
        return FinancialRepository.get_all_data_by_user(user_id)

    @staticmethod
    def add_transaction(user_id, form_data, tipo):
        try:
            dados = {
                'valor': float(form_data.get('valor')),
                'descricao': form_data.get('descricao'),
                'categoria': form_data.get('categoria'),
                'periodicidade': form_data.get('periodicidade', 'unica'),
                'data': datetime.strptime(form_data.get('data'), '%Y-%m-%d').date()
            }
            if tipo == 'receita':
                return FinancialRepository.save_receita(user_id, dados)
            elif tipo == 'despesa':
                return FinancialRepository.save_despesa(user_id, dados)
        except Exception:
            return False
        return False

    @staticmethod
    def update_transaction(transacao_id, user_id, form_data, tipo):
        try:
            dados = {
                'valor': float(form_data.get('valor')),
                'descricao': form_data.get('descricao'),
                'categoria': form_data.get('categoria'),
                'periodicidade': form_data.get('periodicidade', 'unica'),
                'data': datetime.strptime(form_data.get('data'), '%Y-%m-%d').date()
            }
            if tipo == 'receita':
                return FinancialRepository.update_receita(transacao_id, user_id, dados)
            elif tipo == 'despesa':
                return FinancialRepository.update_despesa(transacao_id, user_id, dados)
        except Exception:
            return False
        return False