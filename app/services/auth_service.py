from app.repositories.user_repository import UserRepository
from app.database import bcrypt
from flask_login import login_user, logout_user

class AuthService:
    @staticmethod
    def register_user(nome, email, password):
        if UserRepository.get_by_email(email):
            return None, "Este email já se encontra registado."
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = UserRepository.create(nome, email, hashed_password)
        return user, "Utilizador registado com sucesso."

    @staticmethod
    def login_user(email, password):
        user = UserRepository.get_by_email(email)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            return True
        return False

    @staticmethod
    def logout_user():
        logout_user()