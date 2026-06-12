from app.repositories.financial_repository import FinancialRepository
from datetime import datetime
from collections import defaultdict

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
        lista_receitas = FinancialRepository.get_receitas_by_user(user_id)
        lista_despesas = FinancialRepository.get_despesas_by_user(user_id)
        
        agrupado_receitas = defaultdict(float)
        agrupado_despesas = defaultdict(float)
        todas_chaves = set()

        for r in lista_receitas:
            if not r.data:
                continue
            valor = float(r.valor)
            
            if tipo == 'diario':
                chave = r.data.strftime('%d %b')
            elif tipo == 'semanal':
                chave = f"Semana {r.data.strftime('%U')}"
            elif tipo == 'mensal':
                chave = r.data.strftime('%b/%Y')
            elif tipo == 'anual':
                chave = r.data.strftime('%Y')
            else:
                chave = r.data.strftime('%Y-%m-%d')
                
            agrupado_receitas[chave] += valor
            todas_chaves.add(chave)
        for d in lista_despesas:
            if not d.data:
                continue
            valor = float(d.valor)
            
            if tipo == 'diario':
                chave = d.data.strftime('%d %b')
            elif tipo == 'semanal':
                chave = f"Semana {d.data.strftime('%U')}"
            elif tipo == 'mensal':
                chave = d.data.strftime('%b/%Y')
            elif tipo == 'anual':
                chave = d.data.strftime('%Y')
            else:
                chave = d.data.strftime('%Y-%m-%d')
                
            agrupado_despesas[chave] += valor
            todas_chaves.add(chave)

        labels = sorted(list(todas_chaves))

        valores_receitas = [agrupado_receitas[chave] for chave in labels]
        valores_despesas = [agrupado_despesas[chave] for chave in labels]

        return {
            "labels": labels,
            "receitas": valores_receitas,
            "despesas": valores_despesas
        }