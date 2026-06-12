from app.repositories.financial_repository import FinancialRepository
from datetime import datetime

class FinancialService:
    @staticmethod
    def get_dashboard_data(user_id):
        lista_receitas = FinancialRepository.get_receitas_by_user(user_id)
        lista_despesas = FinancialRepository.get_despesas_by_user(user_id)
        
        receitas_processadas = []
        total_receitas = 0.0
        for r in lista_receitas:
            valor = float(r.valor)
            total_receitas += valor
            receitas_processadas.append({
                'id': r.id,
                'data': r.data.strftime('%d/%m/%Y') if hasattr(r.data, 'strftime') else str(r.data),
                'descricao': r.descricao,
                'categoria': r.categoria,
                'periodicidade': getattr(r, 'periodicidade', 'unica'),
                'valor': valor
            })
            
        despesas_processadas = []
        total_despesas = 0.0
        gastos_por_categoria = {}
        
        for d in lista_despesas:
            valor = float(d.valor)
            total_despesas += valor
            despesas_processadas.append({
                'id': d.id,
                'data': d.data.strftime('%d/%m/%Y') if hasattr(d.data, 'strftime') else str(d.data),
                'descricao': d.descricao,
                'categoria': d.categoria,
                'periodicidade': getattr(d, 'periodicidade', 'unica'),
                'valor': valor
            })
            
            cat = d.categoria if d.categoria else "Geral"
            gastos_por_categoria[cat] = gastos_por_categoria.get(cat, 0.0) + valor

        return {
            'receitas': receitas_processadas,
            'despesas': despesas_processadas,
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'saldo_atual': total_receitas - total_despesas,
            'gastos_por_categoria': gastos_por_categoria
        }

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
    
    @staticmethod
    def get_gastos_por_periodo(user_id, tipo):
        lista_despesas = FinancialRepository.get_despesas_by_user(user_id)
        agrupado = defaultdict(float)

        for d in lista_despesas:
            valor = float(d.valor)
            data_obj = d.data 
            if tipo == 'diario':
              
                chave = data_obj.strftime('%d %b')
            elif tipo == 'semanal':
                
                chave = f"Semana {data_obj.strftime('%U')}"
            elif tipo == 'mensal':
                
                chave = data_obj.strftime('%b/%Y')
            elif tipo == 'anual':
                
                chave = data_obj.strftime('%Y')
            else:
                chave = data_obj.strftime('%Y-%m-%d')

            agrupado[chave] += valor

        labels = list(agrupado.keys())[::-1]
        valores = list(agrupado.values())[::-1]

        return {
            "labels": labels,
            "valores": valores
        }