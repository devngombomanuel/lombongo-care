from app.database import db
from app.models import Receita, Despesa, InteracaoIA

class FinancialRepository:
    @staticmethod
    def get_receitas_by_user(user_id):
        return Receita.query.filter_by(user_id=user_id).order_by(Receita.data.desc()).all()

    @staticmethod
    def get_despesas_by_user(user_id):
        return Despesa.query.filter_by(user_id=user_id).order_by(Despesa.data.desc()).all()

    @staticmethod
    def get_ia_interactions(user_id):
        return InteracaoIA.query.filter_by(user_id=user_id).order_by(InteracaoIA.id.asc()).all()

    @staticmethod
    def save_ia_interaction(user_id, mensagem, resposta):
        try:
            nova_interacao = InteracaoIA(
                user_id=user_id,
                mensagem=mensagem,
                resposta=resposta
            )
            db.session.add(nova_interacao)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def clear_ia_interactions(user_id):
        try:
            InteracaoIA.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def save_receita(user_id, dados):
        try:
            nova = Receita(
                user_id=user_id,
                valor=dados['valor'],
                descricao=dados['descricao'],
                categoria=dados['categoria'],
                periodicidade=dados['periodicidade'],
                data=dados['data']
            )
            db.session.add(nova)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def save_despesa(user_id, dados):
        try:
            nova = Despesa(
                user_id=user_id,
                valor=dados['valor'],
                descricao=dados['descricao'],
                categoria=dados['categoria'],
                periodicidade=dados['periodicidade'],
                data=dados['data']
            )
            db.session.add(nova)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def update_receita(transacao_id, user_id, dados):
        try:
            r = Receita.query.filter_by(id=transacao_id, user_id=user_id).first()
            if r:
                r.valor = dados['valor']
                r.descricao = dados['descricao']
                r.categoria = dados['categoria']
                r.periodicidade = dados['periodicidade']
                r.data = dados['data']
                db.session.commit()
                return True
            return False
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def update_despesa(transacao_id, user_id, dados):
        try:
            d = Despesa.query.filter_by(id=transacao_id, user_id=user_id).first()
            if d:
                d.valor = dados['valor']
                d.descricao = dados['descricao']
                d.categoria = dados['categoria']
                d.periodicidade = dados['periodicidade']
                d.data = dados['data']
                db.session.commit()
                return True
            return False
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def delete_receita(id, user_id):
        try:
            Receita.query.filter_by(id=id, user_id=user_id).delete()
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def delete_despesa(id, user_id):
        try:
            Despesa.query.filter_by(id=id, user_id=user_id).delete()
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False