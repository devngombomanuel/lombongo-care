# Colocar no topo ou em ficheiro apropriado de inicialização de dados
from app.database import login_manager
from app.repositories.user_repository import UserRepository

@login_manager.user_loader
def load_user(user_id):
    return UserRepository.get_by_id(user_id)

from app.models import User
from app.database import db

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(int(user_id))

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(nome, email, password_hash):
        user = User(nome=nome, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user