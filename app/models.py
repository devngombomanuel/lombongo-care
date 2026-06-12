from datetime import datetime
from app.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    receitas = db.relationship('Receita', backref='user', lazy=True, cascade="all, delete-orphan")
    despesas = db.relationship('Despesa', backref='user', lazy=True, cascade="all, delete-orphan")
    interacoes_ia = db.relationship('InteracaoIA', backref='user', lazy=True, cascade="all, delete-orphan")

class Receita(db.Model):
    __tablename__ = 'receitas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    periodicidade = db.Column(db.String(50), nullable=False, default='unica')
    data = db.Column(db.Date, nullable=False)

class Despesa(db.Model):
    __tablename__ = 'despesas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    periodicidade = db.Column(db.String(50), nullable=False, default='unica')
    data = db.Column(db.Date, nullable=False)

class InteracaoIA(db.Model):
    __tablename__ = 'interacoes_ia'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)