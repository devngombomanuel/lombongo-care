import re
from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from app import mail
from app.database import db, bcrypt
from app.repositories.user_repository import UserRepository
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

    @staticmethod
    def validar_forca_senha(senha):
        if len(senha) < 8:
            return False, "A palavra-passe deve ter pelo menos 8 caracteres."
        if not re.search(r"[A-Z]", senha):
            return False, "A palavra-passe deve conter pelo menos uma letra maiúscula."
        if not re.search(r"[0-9]", senha):
            return False, "A palavra-passe deve conter pelo menos um número."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            return False, "A palavra-passe deve conter pelo menos um caractere especial."
        return True, ""

    @staticmethod
    def enviar_link_recuperacao(email):
        user = UserRepository.get_by_email(email)
        if not user:
            return False
            
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(user.email, salt='recuperacao-senha-salt')
        link_redefinicao = url_for('auth.redefinir_senha', token=token, _external=True)
        
        msg = Message("Recuperação de Palavra-passe - LombongoCare",
                      recipients=[user.email])
        msg.body = f"""Olá, {user.nome}.
        
Para redefinir a sua palavra-passe no LombongoCare, clique no link abaixo ou copie-o para o seu navegador:
{link_redefinicao}

Este link é válido por 1 hora. Se não fez esta solicitação, ignore este e-mail.
"""
        try:
            mail.send(msg)
            return True
        except Exception:
            return False

    @staticmethod
    def verificar_token_recuperacao(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt='recuperacao-senha-salt', max_age=3600)
            return email
        except (SignatureExpired, BadTimeSignature):
            return None

    @staticmethod
    def atualizar_senha_por_email(email, nova_senha):
        user = UserRepository.get_by_email(email)
        if not user:
            return False
            
        user.password_hash = bcrypt.generate_password_hash(nova_senha).decode('utf-8')
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False