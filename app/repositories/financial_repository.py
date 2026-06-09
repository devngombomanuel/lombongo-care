from app.models import Receita, Despesa, InteracaoIA
from app.database import db

class FinancialRepository:
    @staticmethod
    def get_receitas_by_user(user_id):
        return Receita.query.filter_by(user_id=user_id).order_by(Receita.data.desc()).all()

    @staticmethod
    def add_receita(user_id, valor, descricao, categoria, data_obj):
        receita = Receita(user_id=user_id, valor=valor, descricao=descricao, categoria=categoria, data=data_obj)
        db.session.add(receita)
        db.session.commit()
        return receita

    @staticmethod
    def delete_receita(receita_id, user_id):
        receita = Receita.query.filter_by(id=receita_id, user_id=user_id).first()
        if receita:
            db.session.delete(receita)
            db.session.commit()
            return True
        return False

    # Despesas
    @staticmethod
    def get_despesas_by_user(user_id):
        return Despesa.query.filter_by(user_id=user_id).order_by(Despesa.data.desc()).all()

    @staticmethod
    def add_despesa(user_id, valor, descricao, categoria, periodicidade, data_obj):
        despesa = Despesa(user_id=user_id, valor=valor, descricao=descricao, categoria=categoria, periodicidade=periodicidade, data=data_obj)
        db.session.add(despesa)
        db.session.commit()
        return despesa

    @staticmethod
    def delete_despesa(despesa_id, user_id):
        despesa = Despesa.query.filter_by(id=despesa_id, user_id=user_id).first()
        if despesa:
            db.session.delete(despesa)
            db.session.commit()
            return True
        return False


    @staticmethod
    def save_ia_interaction(user_id, mensagem, resposta):
        interacao = InteracaoIA(user_id=user_id, mensagem=mensagem, resposta=resposta)
        db.session.add(interacao)
        db.session.commit()
        return interacao
        
    @staticmethod
    def get_ia_interactions(user_id, limit=10):
        return InteracaoIA.query.filter_by(user_id=user_id).order_by(InteracaoIA.criado_em.asc()).all()